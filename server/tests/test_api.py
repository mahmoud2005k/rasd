import os
import sys
import tempfile
import unittest
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_dir = tempfile.mkdtemp()
os.environ.update({"ADMIN_KEY": "secret", "LINKS_FILE": os.path.join(_dir, "none.txt"), "TELEGRAM_BOT_TOKEN": "", "TELEGRAM_CHAT_ID": ""})
if "flask_cors" not in sys.modules:
    try:
        import flask_cors  # noqa: F401
    except ImportError:
        m = types.ModuleType("flask_cors"); m.CORS = lambda *a, **k: None; sys.modules["flask_cors"] = m

import common  # noqa: E402
common.DB_PATH = os.path.join(_dir, "test.db")   # never touch the real database
import app as appmod  # noqa: E402
import engine  # noqa: E402
import ml  # noqa: E402
import netinfo  # noqa: E402

netinfo.domain_age_days = lambda host: 8000 if "old" in host else 5
netinfo.dns_info = lambda host: {"resolves": True, "ips": [], "ns": [], "mx": []}
ml.predict = lambda url: None
engine.analyze_page = lambda url: {"fetched": True, "final_url": url, "flags": [
    {"k": "xdomain_form", "sev": "h", "pts": 30, "ar": "ع", "en": "e"}]}
common.init_db()


class ApiTest(unittest.TestCase):
    def setUp(self):
        engine._cache.clear()
        for b in (appmod._hits, appmod._email_hits, appmod._deep_hits, appmod._api_hits):
            b.clear()
        self.c = appmod.app.test_client()

    def post(self, path, **body):
        return self.c.post(path, json=body)

    def test_health(self):
        self.assertEqual(self.c.get("/api/health").json, {"ok": True})

    def test_analyze_returns_a_full_report(self):
        r = self.post("/api/analyze", url="https://www.old-example.com/page").json
        self.assertTrue(r["rules_included"])
        self.assertEqual(r["verdict"], "safe")
        self.assertEqual(r["domain"]["age_days"], 8000)
        self.assertTrue({"risk_score", "verdict", "reasons", "ml", "database", "domain", "page", "features"} <= set(r))

    def test_new_domain_adds_points(self):
        r = self.post("/api/analyze", url="https://brand-new.example").json
        self.assertIn("newdom", {x["k"] for x in r["reasons"]})
        self.assertGreaterEqual(r["risk_score"], 35)

    def test_phishing_rules_reach_dangerous(self):
        r = self.post("/api/analyze", url="http://paypa1-secure.xyz/verify").json
        self.assertEqual(r["verdict"], "dangerous")

    def test_known_link_is_100(self):
        with common.db() as c:
            c.execute("INSERT OR IGNORE INTO bad_links VALUES(?,?,?,?)", ("known-bad.example/x", "known-bad.example", 0, "test"))
        r = self.post("/api/analyze", url="http://known-bad.example/x").json
        self.assertEqual(r["risk_score"], 100)
        self.assertTrue(r["known"])

    def test_trusted_site_ignores_the_ai_estimate(self):
        old_age, old_ml = netinfo.domain_age_days, ml.predict
        netinfo.domain_age_days = lambda host: 9000
        ml.predict = lambda url: {"probability": 0.97, "factors": []}
        try:
            r = self.post("/api/analyze", url="instagram.com").json      # typed without https://
        finally:
            netinfo.domain_age_days, ml.predict = old_age, old_ml
        self.assertEqual((r["risk_score"], r["ml_points"], r["verdict"]), (0, 0, "safe"))

    def test_allowlist_never_trusts_free_hosting_platforms(self):
        path = os.path.join(_dir, "allow.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("bbc.com\nweebly.com\ngithub.io\n# comment\n")
        os.environ["ALLOWLIST_FILE"] = path
        try:
            self.assertEqual(engine._load_allowlist(), {"bbc.com"})
        finally:
            del os.environ["ALLOWLIST_FILE"]

    def test_invalid_url_is_400(self):
        self.assertEqual(self.post("/api/analyze", url="not a url").status_code, 400)

    def test_deep_scan_adds_page_flags_and_is_rate_limited(self):
        r = self.post("/api/analyze", url="https://old-site.example/login", deep=True).json
        self.assertIn("xdomain_form", {x["k"] for x in r["reasons"]})
        codes = [self.post("/api/analyze", url=f"https://old{i}.example/l", deep=True).status_code for i in range(12)]
        self.assertEqual(codes[-1], 429)

    def test_message_endpoint(self):
        r = self.post("/api/message", text="مبروك فزت بجائزة! أرسل رمز التحقق http://libyana-bonus.top/claim").json
        self.assertIn(r["verdict"], ("suspicious", "dangerous"))
        self.assertEqual(len(r["links"]), 1)
        self.assertEqual(self.post("/api/message", text="  ").status_code, 400)

    def test_email_check_with_stubbed_provider(self):
        class R:
            def __init__(s, code, js=None): s.status_code, s._js, s.ok = code, js, code < 400
            def json(s): return s._js
        orig = appmod.requests.get
        try:
            appmod.requests.get = lambda url, **k: R(200, {"breaches": [["Adobe"], ["LinkedIn"]]})
            self.assertEqual(self.post("/api/email-check", email="a@b.com").json["breaches"], ["Adobe", "LinkedIn"])
            appmod.requests.get = lambda url, **k: R(404)
            self.assertFalse(self.post("/api/email-check", email="a@b.com").json["found"])
            self.assertEqual(self.post("/api/email-check", email="bad").status_code, 400)
        finally:
            appmod.requests.get = orig

    def test_report_is_saved(self):
        appmod.send_telegram = lambda text: True
        self.assertTrue(self.post("/api/report", url="http://bad.example/x", type=0).json["ok"])
        self.assertEqual(self.post("/api/report", url="nonsense").status_code, 400)

    def test_reports_count_distinct_reporters_and_add_points(self):
        appmod.send_telegram = lambda text: True
        for ip in ("1.1.1.1", "1.1.1.1", "2.2.2.2"):
            self.c.post("/api/report", json={"url": "http://reported.example/x", "type": 0}, headers={"X-Forwarded-For": ip})
        r = self.post("/api/analyze", url="http://reported.example/x").json
        self.assertEqual(r["reports"], 2)                       # the same reporter counts once
        rep = [x for x in r["reasons"] if x["k"] == "rep"][0]
        self.assertEqual(rep["pts"], 30)

    def test_reports_never_turn_a_trusted_site_dangerous(self):
        appmod.send_telegram = lambda text: True
        old = netinfo.domain_age_days
        netinfo.domain_age_days = lambda host: 8000
        try:
            for ip in ("3.3.3.3", "4.4.4.4", "5.5.5.5", "6.6.6.6"):
                self.c.post("/api/report", json={"url": "https://instagram.com", "type": 0}, headers={"X-Forwarded-For": ip})
            r = self.post("/api/analyze", url="instagram.com").json
        finally:
            netinfo.domain_age_days = old
        self.assertEqual(r["verdict"], "safe", r["reasons"])
        self.assertEqual([x["pts"] for x in r["reasons"] if x["k"] == "rep"], [0])

    def test_admin_stats_needs_the_key(self):
        self.post("/api/analyze", url="https://stats-check.example")
        self.assertEqual(self.c.get("/api/admin/stats").status_code, 403)
        r = self.c.get("/api/admin/stats", headers={"X-Admin-Key": "secret"})
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.json["scans_total"], 1)
        with common.db() as c:   # privacy: only host / verdict / score are stored for scans
            cols = [row[1] for row in c.execute("PRAGMA table_info(scans)")]
        self.assertEqual(cols, ["id", "host", "verdict", "score", "source", "created"])


if __name__ == "__main__":
    unittest.main()
