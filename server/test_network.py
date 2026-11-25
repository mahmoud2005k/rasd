"""Finds out why the domain-age and deep-scan checks fail on your network.
Run inside the server folder:  python test_network.py"""
import socket
import time

import requests

UA = {"User-Agent": "Mozilla/5.0 (compatible; RasdBot/1.0; student project)"}


def step(name, fn):
    t = time.time()
    try:
        out = fn()
        print(f"[OK  ] {name} ({time.time() - t:.1f}s) {out}")
    except Exception as e:
        print(f"[FAIL] {name} ({time.time() - t:.1f}s) -> {type(e).__name__}: {e}")


print("Proxy settings seen by Python:", requests.utils.getproxies() or "none")
step("DNS github.com", lambda: sorted({i[4][0] for i in socket.getaddrinfo("github.com", None)})[:4])
step("DNS rdap.org", lambda: sorted({i[4][0] for i in socket.getaddrinfo("rdap.org", None)})[:4])
step("HTTPS api.telegram.org", lambda: requests.get("https://api.telegram.org", timeout=15).status_code)
step("HTTPS github.com/login", lambda: requests.get("https://github.com/login", timeout=15, headers=UA, allow_redirects=False).status_code)
step("HTTPS example.com", lambda: requests.get("https://example.com", timeout=15, headers=UA).status_code)


def rdap(url):
    r = requests.get(url, timeout=20, headers={"Accept": "application/rdap+json"})
    ev = [e.get("eventDate") for e in r.json().get("events", []) if e.get("eventAction") == "registration"] if r.ok else None
    return f"HTTP {r.status_code}, registration: {ev}"


step("RDAP via rdap.org", lambda: rdap("https://rdap.org/domain/example.com"))
step("RDAP via Verisign directly", lambda: rdap("https://rdap.verisign.com/com/v1/domain/example.com"))
print("\nCopy everything above and send it to me.")
