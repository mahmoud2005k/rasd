import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test")
import bot  # noqa: E402


class BotTest(unittest.TestCase):
    def setUp(self):
        bot._seen.clear()
        bot.engine.analyze_url = lambda u, deep=False, source="bot": {
            "risk_score": 80, "verdict": "dangerous",
            "reasons": [{"k": "tld", "ar": "امتداد مشبوه", "en": "Scam-prone extension"}]}

    def test_arabic_scam_message(self):
        r = bot.handle_text("مبروك فزت بجائزة! أرسل رمز التحقق http://x.top/a")
        self.assertIn("خطير", r)
        self.assertIn("hxxp://x[.]top/a", r)       # links are defanged so nobody taps them by accident
        self.assertNotIn("http://x.top", r)

    def test_english_message_gets_english_reply(self):
        self.assertIn("Dangerous", bot.handle_text("you won a prize! send your otp http://x.top/a"))

    def test_nothing_found(self):
        self.assertIn("لم أجد", bot.handle_text("مرحباً كيف حالك"))

    def test_start_and_rate_limit(self):
        self.assertIn("رصد", bot.reply_for(1, "/start"))
        replies = [bot.reply_for(2, "مرحبا كيف الحال") for _ in range(bot.LIMIT + 1)]
        self.assertNotIn("عدد كبير", replies[0])
        self.assertIn("عدد كبير", replies[-1])


if __name__ == "__main__":
    unittest.main()
