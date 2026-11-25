"""Rasd API (Flask). The analysis itself lives in engine.py; this file only exposes it."""
import hmac
import json
import os
import re
import time
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()
from common import db, init_db, norm  # noqa: E402
import engine  # noqa: E402
import messages  # noqa: E402
import netinfo  # noqa: E402

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
ORIGINS = [o.strip() for o in os.getenv("FRONTEND_ORIGIN", "*").split(",")]
ADMIN_KEY = os.getenv("ADMIN_KEY", "")
TYPES = ["Phishing", "Financial scam", "Malware", "Brand impersonation", "Other"]
XON_BASE = os.getenv("XON_BASE_URL", "https://api.xposedornot.com")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

app = Flask(__name__)
CORS(app, origins=ORIGINS)
init_db()

# On free hosting the database can be wiped on restart, so reload the links file at startup.
LINKS_FILE = os.getenv("LINKS_FILE", "suspicious_links.txt")
with db() as _c:
    _empty = _c.execute("SELECT COUNT(*) FROM bad_links").fetchone()[0] == 0
if _empty and os.path.exists(LINKS_FILE):
    from import_links import load_file
    print("[startup] imported links:", load_file(LINKS_FILE, "startup-file"))

_hits, _email_hits, _deep_hits, _api_hits = {}, {}, {}, {}


def client_ip():
    return (request.headers.get("X-Forwarded-For", request.remote_addr) or "").split(",")[0].strip()


def too_many(ip, limit=5, window=600, bucket=None):
    bucket = _hits if bucket is None else bucket
    now = time.time()
    arr = [t for t in bucket.get(ip, []) if now - t < window]
    if len(arr) >= limit:
        bucket[ip] = arr
        return True
    arr.append(now)
    bucket[ip] = arr
    return False


def defang(u):
    """So nobody taps a malicious link by accident inside Telegram."""
    return u.replace("http", "hxxp").replace(".", "[.]")


def send_telegram(text):
    if not TOKEN or not CHAT_ID:
        print("[telegram] TOKEN or CHAT_ID is empty. Check your .env file")
        return False
    try:
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          json={"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True}, timeout=25)
        if not r.ok:
            print("[telegram] FAILED:", r.status_code, r.text)
        return r.ok
    except requests.RequestException as e:
        print("[telegram] network error:", e)
        return False


@app.get("/api/health")
def health():
    return jsonify(ok=True)


@app.post("/api/check")
def check():
    """Older, lighter endpoint: database + domain age only."""
    data = request.get_json(silent=True) or {}
    n = norm(data.get("url"))
    if not n:
        return jsonify(error="invalid url"), 400
    source, reports = engine.db_lookup(n[0], n[1])
    return jsonify(known=source is not None, source=source, reports=reports, age_days=netinfo.domain_age_days(n[0]))


@app.post("/api/analyze")
def analyze_api():
    """The full report: risk score, verdict and reasons (rules, database, AI with explanation, domain, page forms)."""
    data = request.get_json(silent=True) or {}
    ip = client_ip()
    if too_many(ip, limit=60, window=60, bucket=_api_hits):
        return jsonify(error="too many requests"), 429
    deep = bool(data.get("deep"))
    if deep and too_many(ip, limit=10, window=600, bucket=_deep_hits):
        return jsonify(error="too many deep scans, try later"), 429
    src = str(data.get("source") or "web")
    res = engine.analyze_url(data.get("url", ""), deep=deep, source=src if src in ("web", "extension", "api") else "web")
    if res is None:
        return jsonify(error="invalid url"), 400
    return jsonify(res)


@app.post("/api/message")
def message_api():
    """Checks a whole SMS / WhatsApp text: scam wording + every link inside it."""
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", ""))[:3000]
    if not text.strip():
        return jsonify(error="empty text"), 400
    if too_many(client_ip(), limit=30, window=60, bucket=_api_hits):
        return jsonify(error="too many requests"), 429
    return jsonify(messages.analyze_message(text, lambda u: engine.analyze_url(u, False, "web")))


@app.post("/api/report")
def report():
    data = request.get_json(silent=True) or {}
    n = norm(data.get("url"))
    if not n:
        return jsonify(error="invalid url"), 400
    ip = client_ip()
    if too_many(ip):
        return jsonify(error="too many reports, try later"), 429
    host = n[0]
    try:
        t = TYPES[int(data.get("type", 4))]
    except (ValueError, IndexError):
        t = TYPES[4]
    notes = str(data.get("notes", ""))[:500]
    url = str(data.get("url")).strip()
    with db() as c:
        c.execute("INSERT INTO reports(url,host,type,notes,ip) VALUES(?,?,?,?,?)", (url, host, t, notes, ip))
        total = c.execute("SELECT COUNT(*) FROM reports WHERE host=?", (host,)).fetchone()[0]
    msg = f"New Rasd report\nType: {t}\nLink: {defang(url)}\nTimes reported: {total}\nNotes: {notes or '-'}"
    return jsonify(ok=True, telegram=send_telegram(msg))


@app.post("/api/email-check")
def email_check():
    """Does the email appear in known public data breaches (XposedOrNot free API)? Not stored, not logged."""
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip()
    if len(email) > 254 or not EMAIL_RE.match(email):
        return jsonify(error="invalid email"), 400
    if too_many(client_ip(), limit=10, window=600, bucket=_email_hits):
        return jsonify(error="too many requests"), 429
    try:
        r = requests.get(f"{XON_BASE}/v1/check-email/{quote(email, safe='')}", timeout=15,
                         headers={"User-Agent": "Rasd-student-project"})
    except requests.RequestException:
        return jsonify(error="service unavailable"), 502
    if r.status_code == 404:
        return jsonify(found=False, count=0, breaches=[])
    if r.status_code == 429:
        return jsonify(error="rate limited by provider"), 429
    if not r.ok:
        return jsonify(error="provider error"), 502
    try:
        raw = r.json().get("breaches") or []
    except (ValueError, AttributeError):
        return jsonify(error="bad response"), 502
    names = []
    for item in raw:
        names.extend(str(x) for x in item) if isinstance(item, list) else names.append(str(item))
    return jsonify(found=bool(names), count=len(names), breaches=names[:30])


@app.get("/api/admin/stats")
def admin_stats():
    """Dashboard numbers. Needs the header X-Admin-Key equal to ADMIN_KEY in .env (disabled if ADMIN_KEY is empty)."""
    if not ADMIN_KEY:
        return jsonify(error="admin disabled: set ADMIN_KEY in .env"), 404
    if not hmac.compare_digest(request.headers.get("X-Admin-Key", ""), ADMIN_KEY):
        return jsonify(error="forbidden"), 403
    with db() as c:
        q = lambda sql: [dict(r) for r in c.execute(sql).fetchall()]
        out = {
            "scans_total": c.execute("SELECT COUNT(*) FROM scans").fetchone()[0],
            "by_verdict": {r["verdict"]: r["n"] for r in q("SELECT verdict, COUNT(*) n FROM scans GROUP BY verdict")},
            "by_source": {r["source"]: r["n"] for r in q("SELECT source, COUNT(*) n FROM scans GROUP BY source")},
            "per_day": q("SELECT substr(created,1,10) day, COUNT(*) n FROM scans GROUP BY day ORDER BY day DESC LIMIT 14")[::-1],
            "top_flagged": q("SELECT host, COUNT(*) n FROM scans WHERE verdict!='safe' GROUP BY host ORDER BY n DESC LIMIT 10"),
            "reports_total": c.execute("SELECT COUNT(*) FROM reports").fetchone()[0],
            "reports_by_type": {r["type"]: r["n"] for r in q("SELECT type, COUNT(*) n FROM reports GROUP BY type")},
            "latest_reports": q("SELECT host, type, created FROM reports ORDER BY id DESC LIMIT 10"),
            "db_links": c.execute("SELECT COUNT(*) FROM bad_links").fetchone()[0],
        }
    try:
        with open("model_metrics.json", encoding="utf-8") as f:
            out["model"] = json.load(f)
    except OSError:
        out["model"] = None
    return jsonify(out)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
