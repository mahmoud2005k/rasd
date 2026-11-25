import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import messages  # noqa: E402


class MessagesTest(unittest.TestCase):
    def test_scam_message_is_flagged(self):
        m = messages.scan_message("مبروك! فزت بجائزة من ليبيانا. أرسل رمز التحقق خلال ٢٤ ساعة: http://libyana-bonus.top/claim")
        cats = {c["k"] for c in m["cats"]}
        self.assertTrue({"prize", "data", "urg"} <= cats, cats)
        self.assertEqual(m["links"], ["http://libyana-bonus.top/claim"])
        self.assertGreaterEqual(m["score"], 50)

    def test_normal_message_is_clean(self):
        m = messages.scan_message("مرحباً، موعدنا غداً الساعة 5 مساءً")
        self.assertEqual((m["cats"], m["links"], m["score"]), ([], [], 0))

    def test_link_extraction(self):
        links = messages.extract_links("see bit.ly/abc123, and www.example.com/x. also file.txt e.g. test.")
        self.assertIn("bit.ly/abc123", links)
        self.assertIn("www.example.com/x", links)
        self.assertNotIn("file.txt", links)

    def test_arabic_normalization(self):
        self.assertEqual(messages.norm_ar("خلال ٢٤ ساعة"), messages.norm_ar("خلال 24 ساعة"))
        self.assertEqual(messages.norm_ar("جائزة"), messages.norm_ar("جايزه"))

    def test_latin_words_need_word_boundaries(self):
        self.assertFalse(any(c["k"] == "data" for c in messages.scan_message("I am shipping the order")["cats"]))
        self.assertTrue(any(c["k"] == "data" for c in messages.scan_message("send your otp now")["cats"]))

    def test_analyze_message_combines_text_and_links(self):
        fake = lambda u: {"risk_score": 80, "verdict": "dangerous", "reasons": [{"k": "tld", "ar": "a", "en": "b"}]}
        r = messages.analyze_message("فزت بجائزة! http://x.top/a", fake)
        self.assertEqual(r["verdict"], "dangerous")
        self.assertEqual(r["links"][0]["risk_score"], 80)
        self.assertLessEqual(r["risk_score"], 100)


if __name__ == "__main__":
    unittest.main()
