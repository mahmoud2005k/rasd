"""Telegram bot: send it a link or a whole SMS / WhatsApp message and it replies with the verdict.
Run (keep the window open):  python bot.py"""
import os
import re
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()
import engine  # noqa: E402
import messages  # noqa: E402

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
LIMIT, WINDOW = 20, 3600  # messages per chat per hour
_seen = {}

VERDICT = {"ar": {"dangerous": "🔴 خطير", "suspicious": "🟠 مشبوه", "safe": "🟢 يبدو آمناً"},
           "en": {"dangerous": "🔴 Dangerous", "suspicious": "🟠 Suspicious", "safe": "🟢 Looks safe"}}
TXT = {
    "ar": {"help": "أهلاً بك في رصد.\nأرسل لي رابطاً، أو رسالة SMS أو واتساب كاملة، وأخبرك هل هي احتيال ولماذا.\nلا تفتح الروابط المشبوهة أبداً.",
           "flags": "علامات في نص الرسالة:", "links": "الروابط:", "none": "لم أجد رابطاً ولا علامات احتيال واضحة. أرسل الرسالة كاملة مع الرابط إن وُجد.",
           "foot": "نتيجة تقديرية وليست ضماناً. إذا شككت فلا تدخل أي بيانات.", "limit": "عدد كبير من الرسائل، حاول بعد قليل.", "text": "أرسل لي نصاً أو رابطاً."},
    "en": {"help": "Welcome to Rasd.\nSend me a link, or a whole SMS / WhatsApp message, and I will tell you if it looks like a scam and why.\nNever open suspicious links.",
           "flags": "Signs in the message text:", "links": "Links:", "none": "I found no link and no clear scam signs. Send the full message with its link if any.",
           "foot": "This is an estimate, not a guarantee. If in doubt, do not enter any data.", "limit": "Too many messages, try again shortly.", "text": "Send me some text or a link."},
}


def defang(u):
    return u.replace("http", "hxxp").replace(".", "[.]")


def lang_of(text):
    return "ar" if re.search("[\u0600-\u06ff]", text or "") else "en"


def limited(chat):
    now = time.time()
    arr = [t for t in _seen.get(chat, []) if now - t < WINDOW]
    if len(arr) >= LIMIT:
        _seen[chat] = arr
        return True
    arr.append(now)
    _seen[chat] = arr
    return False


def handle_text(text):
    """Builds the reply for one message (pure function: easy to test)."""
    lang = lang_of(text)
    t, v = TXT[lang], VERDICT[lang]
    res = messages.analyze_message(text, lambda u: engine.analyze_url(u, False, "bot"), max_links=3)
    if not res["flags"] and not res["links"]:
        return t["none"]
    lines = [f"{v[res['verdict']]} ({res['risk_score']}/100)"]
    if res["flags"]:
        lines += ["", t["flags"]] + [f"• {f[lang]}{'، '.join(f['words'])}" for f in res["flags"]]
    if res["links"]:
        lines += ["", t["links"]]
        for i, l in enumerate(res["links"], 1):
            lines.append(f"{i}) {defang(l['url'])}  {l['risk_score']}/100 {v[l['verdict']]}")
            lines += [f"   - {r[lang]}" for r in l["reasons"][:2]]
    lines += ["", t["foot"]]
    return "\n".join(lines)[:3500]


def reply_for(chat, text):
    if not text:
        return TXT["ar"]["text"]
    if text.strip().lower() in ("/start", "/help"):
        return TXT["ar"]["help"] + "\n\n" + TXT["en"]["help"]
    if limited(chat):
        return TXT[lang_of(text)]["limit"]
    return handle_text(text[:3000])


def send(chat, text):
    try:
        requests.post(f"{API}/sendMessage", json={"chat_id": chat, "text": text, "disable_web_page_preview": True}, timeout=30)
    except requests.RequestException as e:
        print("[bot] send failed:", type(e).__name__)


def main():
    if not TOKEN:
        sys.exit("TELEGRAM_BOT_TOKEN is missing in .env")
    offset = None
    print("[bot] running. Press Ctrl+C to stop.")
    while True:
        try:
            r = requests.get(f"{API}/getUpdates", params={"timeout": 25, "offset": offset}, timeout=45)
            data = r.json()
        except (requests.RequestException, ValueError) as e:
            print("[bot] network problem:", type(e).__name__)
            time.sleep(5)
            continue
        for u in data.get("result", []):
            offset = u["update_id"] + 1
            msg = u.get("message") or {}
            chat = (msg.get("chat") or {}).get("id")
            if chat is None:
                continue
            try:
                send(chat, reply_for(chat, msg.get("text")))
            except Exception as e:  # never let one bad message stop the bot
                print("[bot] error:", type(e).__name__, e)


if __name__ == "__main__":
    main()
