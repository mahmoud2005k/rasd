import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import rules  # noqa: E402


def keys(url, **kw):
    score, reasons = rules.evaluate(url, **kw)
    return score, {r["k"] for r in reasons}


class RulesTest(unittest.TestCase):
    def test_clean_links_score_zero(self):
        for u in ("https://google.com", "https://github.com/user/repo", "https://en.wikipedia.org/wiki/Phishing"):
            score, k = keys(u)
            self.assertEqual(score, 0, u)
            self.assertIn("clean", k)

    def test_invisible_characters(self):
        score, k = keys("http://goo\u200bgle.com/login")
        self.assertIn("invisible", k)
        self.assertGreaterEqual(score, 35)

    def test_homograph_cyrillic(self):
        score, k = keys("http://p\u0430ypal.com/login")
        self.assertIn("homograph", k)
        self.assertGreaterEqual(score, 60)

    def test_typosquatting(self):
        _, k = keys("https://instagrarm.com")
        self.assertIn("typo", k)
        _, k = keys("https://instagram.com")
        self.assertNotIn("typo", k)

    def test_official_domains_are_exempt(self):
        _, k = keys("https://www.microsoftonline.com")
        self.assertNotIn("brand", k)
        _, k = keys("https://login.microsoftonline.com")
        self.assertNotIn("brand", k)

    def test_trusted_set_exempts_brand_rules(self):
        _, k = keys("https://faceboook.com")
        self.assertIn("typo", k)
        _, k = keys("https://faceboook.com", trusted={"faceboook.com"})
        self.assertNotIn("typo", k)

    def test_repeated_characters(self):
        _, k = keys("http://gooogle-login.xyz")
        self.assertIn("charrep", k)

    def test_executable_file_and_ip(self):
        self.assertIn("file", keys("http://evil.com/download/setup.exe")[1])
        self.assertIn("ip", keys("http://192.0.2.54/paypal/verify")[1])

    def test_brand_impersonation_is_dangerous(self):
        score, k = keys("http://paypa1-secure.xyz/verify")
        self.assertIn("brand", k)
        self.assertGreaterEqual(score, 50)

    def test_missing_scheme_is_not_punished(self):
        self.assertNotIn("nohttps", keys("google.com/x")[1])
        self.assertIn("nohttps", keys("http://example.com")[1])
        self.assertIn("https", keys("https://example.com")[1])

    def test_invalid_input(self):
        for bad in ("", "   ", "not a url", "http://localhost"):
            self.assertIsNone(rules.evaluate(bad), bad)

    def test_score_is_capped(self):
        score, _ = keys("http://p\u0430ypal-login-verify-secure-account.xyz/verify?url=http://x.com&a=(b)(c)(d)")
        self.assertLessEqual(score, 100)

    def test_levenshtein(self):
        self.assertEqual(rules.lev("instagram", "instagrarm"), 1)
        self.assertEqual(rules.lev("abc", "acb"), 1)  # swap counts as one edit
        self.assertEqual(rules.lev("same", "same"), 0)


if __name__ == "__main__":
    unittest.main()
