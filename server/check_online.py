"""Tests a running Rasd server (local or online).   python check_online.py https://your-api.onrender.com
The first call to a sleeping free server can take up to a minute."""
import sys
import time

import requests

base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000").rstrip("/")


def call(name, method, path, expect, **kw):
    t = time.time()
    try:
        r = requests.request(method, base + path, timeout=120, **kw)
        data = r.json()
        ok = expect(data)
        print(f"[{'OK  ' if ok else 'FAIL'}] {name} ({time.time() - t:.1f}s)", "" if ok else data)
    except Exception as e:
        print(f"[FAIL] {name} ({time.time() - t:.1f}s) -> {type(e).__name__}: {e}")


call("health", "GET", "/api/health", lambda d: d.get("ok") is True)
call("safe link (instagram.com)", "POST", "/api/analyze", lambda d: d["verdict"] == "safe", json={"url": "instagram.com"})
call("phishing-looking link", "POST", "/api/analyze", lambda d: d["verdict"] == "dangerous", json={"url": "http://paypa1-secure.xyz/verify"})
call("hidden character", "POST", "/api/analyze", lambda d: any(r["k"] == "invisible" for r in d["reasons"]), json={"url": "http://goo\u200bgle.com/login"})
call("scam message", "POST", "/api/message", lambda d: d["verdict"] in ("suspicious", "dangerous"),
     json={"text": "مبروك فزت بجائزة! أرسل رمز التحقق http://libyana-bonus.top/claim"})
print("\nDone. If every line says OK, the server is ready.")
