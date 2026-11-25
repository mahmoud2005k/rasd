"""The analysis engine: ONE function that builds the full report (rules + database + AI + domain + page)."""
import copy
import os
import time

import ml
import netinfo
import rules
from common import db, norm, reg_domain
from features import extract
from page_analysis import analyze_page

TTL = 600
_cache = {}


# Free hosting / user-content platforms: anyone can publish a page under them (paypal-login.weebly.com),
# so they must NEVER count as "trusted", even if they are very popular.
SHARED_HOSTS = {
    "blogspot.com", "blogger.com", "weebly.com", "wixsite.com", "github.io", "githubusercontent.com", "herokuapp.com",
    "netlify.app", "vercel.app", "pages.dev", "workers.dev", "web.app", "firebaseapp.com", "azurewebsites.net",
    "000webhostapp.com", "glitch.me", "repl.co", "replit.app", "onrender.com", "ngrok.io", "ngrok-free.app",
    "trycloudflare.com", "myshopify.com", "square.site", "carrd.co", "godaddysites.com", "webflow.io",
    "framer.website", "notion.site", "tumblr.com", "wordpress.com", "sharepoint.com", "bit.ly", "tinyurl.com",
    "t.co", "cutt.ly", "is.gd", "rb.gy", "ow.ly", "s3.amazonaws.com", "storage.googleapis.com",
}


def _load_allowlist():
    path = os.getenv("ALLOWLIST_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowlist.txt"))
    try:
        with open(path, encoding="utf-8") as f:
            return {l.strip().lower() for l in f if l.strip() and not l.startswith("#")} - SHARED_HOSTS
    except OSError:
        return set()


ALLOW = _load_allowlist()


def verdict_of(score):
    return "dangerous" if score >= 50 else "suspicious" if score >= 20 else "safe"


def db_lookup(host, url_norm):
    with db() as c:
        row = c.execute("SELECT source FROM bad_links WHERE url_norm=? OR (host=? AND path_empty=1) LIMIT 1",
                        (url_norm, host)).fetchone()
        reports = c.execute("SELECT COUNT(DISTINCT ip) FROM reports WHERE host=?", (host,)).fetchone()[0]  # different reporters
    return (row["source"] if row else None), reports


def _R(k, sev, pts, ar, en):
    return {"k": k, "sev": sev, "pts": pts, "x": "", "ar": ar, "en": en}


def _compute(raw, n, deep):
    host, url_norm, _ = n
    reg = reg_domain(host)
    trusted = reg in rules.OFFICIAL or reg in ALLOW
    source, reports = db_lookup(host, url_norm)
    known = source is not None
    reasons = []
    if known:
        reasons.append(_R("known", "h", 0, f"الرابط موجود في قاعدة الروابط المشبوهة المعروفة. المصدر: {source}",
                          f"The link is in the known suspicious links database. Source: {source}"))
    rule_score, rule_reasons = 0, []
    got = rules.evaluate(raw, ALLOW)
    if got:
        rule_score, rule_reasons = got
    reasons += rule_reasons

    ml_res, ml_score, ml_points = None, None, None
    try:
        ml_res = ml.predict(raw)
    except Exception as e:
        print("[ml] prediction failed:", e)
    if ml_res:
        ml_score = round(ml_res["probability"] * 100)
        # AI gives at most 45 points: alone it can only make a link "suspicious"; "dangerous" needs other evidence
        ml_points = round(max(0.0, (ml_res["probability"] - 0.5) * 2) * 45)

    flag_pts = 0

    def flag(r):
        nonlocal flag_pts
        flag_pts += r["pts"]
        reasons.append(r)

    age = netinfo.domain_age_days(host)
    if age is not None:
        if age < 30:
            flag(_R("newdom", "h", 35, f"الدومين حديث الإنشاء جداً، عمره {age} يوماً.", f"The domain is brand new, only {age} days old."))
        elif age < 90:
            flag(_R("newdom", "m", 20, f"الدومين حديث الإنشاء، عمره {age} يوماً.", f"The domain is recent, {age} days old."))
        elif age >= 730:
            reasons.append(_R("olddom", "g", 0, f"الدومين قديم ومستقر، عمره {age} يوماً.", f"The domain is old and established, {age} days."))
    if ml_points is not None:
        if trusted:
            ml_points = 0  # famous trusted site: the AI estimate is ignored (it is weak on bare home pages)
            reasons.append(_R("mldamp", "g", 0, "الدومين موثوق ومعروف، لذلك لم يُحتسب تقدير الذكاء الاصطناعي.",
                              "The domain is a known trusted one, so the AI estimate was not counted."))
        elif age is not None and age >= 730:
            ml_points = round(ml_points * 0.4)
            reasons.append(_R("mldamp", "g", 0, "الدومين قديم ومستقر، لذلك خُفّض وزن تقدير الذكاء الاصطناعي.",
                              "The domain is old and established, so the AI estimate was given less weight."))
        else:
            for f in ml_res["factors"][:3]:
                reasons.append(_R("ml", "m", 0, "عامل في نموذج الذكاء الاصطناعي: " + f["ar"], "AI model factor: " + f["en"]))
    if reports:
        if trusted:  # one wrong or malicious report must never turn a famous site into a "dangerous" one
            reasons.append(_R("rep", "g", 0, f"بلّغ عنه {reports} مستخدم، لكنه موقع معروف وموثوق فلم تُحتسب البلاغات.",
                              f"{reports} user(s) reported it, but it is a well-known trusted site, so reports were not counted."))
        else:
            flag(_R("rep", "m", min(40, 15 * reports), f"بلّغ عنه {reports} مستخدماً مختلفاً من قبل.",
                    f"{reports} different user(s) reported it before."))
    dns = netinfo.dns_info(host)
    if not dns["resolves"]:
        flag(_R("nodns", "m", 10, "الدومين لا يستجيب في نظام DNS (قد يكون محذوفاً أو وهمياً).",
                "The domain does not resolve in DNS (it may be taken down or fake)."))
    page = None
    if deep:
        page = analyze_page(raw.strip() if "://" in raw else "http://" + raw.strip())
        for f in page.get("flags", []):
            f.setdefault("x", "")
            flag(f)

    if known:
        risk = 100
    else:
        risk = min(100, rule_score + (ml_points or 0) + flag_pts)
    if not any(r["sev"] != "g" for r in reasons) and not any(r["k"] == "clean" for r in reasons):
        pass
    return {
        "url": raw.strip(), "risk_score": risk, "verdict": verdict_of(risk), "reasons": reasons,
        "known": known, "reports": reports, "rules_included": True, "rule_score": rule_score,
        "ml_score": ml_score, "ml_points": ml_points or 0, "flag_points": flag_pts,
        "ml": {"available": bool(ml_res), "probability": ml_res["probability"] if ml_res else None,
               "factors": ml_res["factors"] if ml_res else []},
        "database": {"known": known, "source": source, "reports": reports},
        "domain": {"age_days": age, "dns": dns, "trusted": trusted}, "page": page, "features": extract(raw),
    }


def _log_scan(host, verdict, score, source):
    """Statistics only: the host, the verdict and the score. No full link, no IP address."""
    try:
        with db() as c:
            c.execute("INSERT INTO scans(host, verdict, score, source) VALUES(?,?,?,?)", (host, verdict, score, source))
    except Exception as e:
        print("[scan log]", e)


def analyze_url(raw, deep=False, source="api"):
    raw = str(raw or "")
    n = norm(raw.strip())
    if not n:
        return None
    key = (raw.strip(), bool(deep))
    hit = _cache.get(key)
    if hit and time.time() < hit[0]:
        res = copy.deepcopy(hit[1])
    else:
        res = _compute(raw, n, bool(deep))
        if len(_cache) > 500:
            _cache.clear()
        _cache[key] = (time.time() + TTL, copy.deepcopy(res))
    _log_scan(n[0], res["verdict"], res["risk_score"], source)
    return res
