"""Tests Telegram alone, without the website. Run: python test_telegram.py"""
import os, requests
from dotenv import load_dotenv

print("Looking for .env in:", os.getcwd())
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN", "")
chat = os.getenv("TELEGRAM_CHAT_ID", "")
print("token found:", bool(token), "| length:", len(token), "| chat_id:", repr(chat))

if not token or not chat:
    raise SystemExit("STOP: .env is missing or the names are wrong")

r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
print("1) getMe ->", r.status_code, r.text)
if not r.ok:
    raise SystemExit("STOP: the token is wrong")

r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                  json={"chat_id": chat, "text": "Rasd test message"}, timeout=10)
print("2) sendMessage ->", r.status_code, r.text)
print("OK: check your Telegram" if r.ok else "STOP: read the description above")
