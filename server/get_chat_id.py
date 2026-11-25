"""Run after you send any message to your bot (or add it to a group and write there)."""
import os, requests
from dotenv import load_dotenv
load_dotenv()
r = requests.get(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/getUpdates", timeout=10).json()
seen = set()
for u in r.get("result", []):
    m = u.get("message") or u.get("channel_post") or {}
    ch = m.get("chat", {})
    if ch.get("id") not in seen:
        seen.add(ch.get("id"))
        print("chat_id:", ch.get("id"), "|", ch.get("title") or ch.get("first_name"))
if not seen:
    print("Nothing found. Send a message to the bot first, then run again.")
