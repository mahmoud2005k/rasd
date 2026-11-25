"""Fetches a page SAFELY (it is only parsed as text, never executed) and analyzes its forms."""
import ipaddress
import re
import socket
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

from common import reg_domain

import os

MAX_BYTES = 500_000
NET_TIMEOUT = float(os.getenv("NET_TIMEOUT", "10"))
UA = "Mozilla/5.0 (compatible; RasdBot/1.0; student project)"


def _is_public(host):
    """Blocks localhost, private networks and cloud metadata addresses (SSRF protection)."""
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError):
        return False
    return bool(infos) and all(ipaddress.ip_address(i[4][0]).is_global for i in infos)


def fetch(url, max_redirects=3):
    cur = url
    for _ in range(max_redirects + 1):
        p = urlparse(cur)
        if p.scheme not in ("http", "https") or not p.hostname:
            return None, "unsupported link"
        if p.port not in (None, 80, 443):
            return None, "port blocked"
        if not _is_public(p.hostname):
            return None, "address blocked or not found"
        try:
            r = requests.get(cur, timeout=NET_TIMEOUT, allow_redirects=False, stream=True, headers={"User-Agent": UA})
        except requests.RequestException as e:
            print(f"[page] {cur} -> {type(e).__name__}: {e}")
            return None, f"unreachable: {type(e).__name__}"
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location")
            r.close()
            if not loc:
                return None, "bad redirect"
            cur = urljoin(cur, loc)
            continue
        if "html" not in r.headers.get("Content-Type", "").lower():
            r.close()
            return None, "not an HTML page"
        data = b""
        for chunk in r.iter_content(8192):
            data += chunk
            if len(data) > MAX_BYTES:
                break
        enc = r.encoding or "utf-8"
        r.close()
        return (data.decode(enc, errors="replace"), cur), None
    return None, "too many redirects"


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms, self.cur = [], None
        self.pw_total = self.hidden_iframes = 0
        self.refresh = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "form":
            self.cur = {"action": a.get("action", "").strip(), "password": 0, "email": 0, "inputs": 0}
            self.forms.append(self.cur)
        elif tag == "input":
            t, n = a.get("type", "text").lower(), a.get("name", "").lower()
            if t == "password":
                self.pw_total += 1
            if self.cur is not None:
                self.cur["inputs"] += 1
                if t == "password":
                    self.cur["password"] += 1
                if t == "email" or "mail" in n or "user" in n:
                    self.cur["email"] += 1
        elif tag == "iframe":
            st = a.get("style", "").replace(" ", "").lower()
            if a.get("width") in ("0", "1") or a.get("height") in ("0", "1") or "display:none" in st or "visibility:hidden" in st:
                self.hidden_iframes += 1
        elif tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            m = re.search(r"url=(.+)", a.get("content", ""), re.I)
            if m:
                self.refresh = m.group(1).strip().strip("'\"")

    def handle_endtag(self, tag):
        if tag == "form":
            self.cur = None


def _flag(k, sev, pts, ar, en):
    return {"k": k, "sev": sev, "pts": pts, "ar": ar, "en": en}


def parse_html(html, page_url):
    """Form Action Analysis: where does the typed data (login button) actually go?"""
    p = _Parser()
    try:
        p.feed(html)
    except Exception:
        pass
    page_host = (urlparse(page_url).hostname or "").lower()
    page_dom = reg_domain(page_host)
    flags, sensitive = [], 0
    for f in p.forms:
        if not (f["password"] or (f["email"] and f["inputs"] >= 2)):
            continue
        sensitive += 1
        act = f["action"]
        if act.lower().startswith("mailto:"):
            flags.append(_flag("mailto_form", "h", 35, "نموذج الإدخال يرسل بياناتك إلى بريد إلكتروني (mailto).",
                               "The input form sends your data to an email address (mailto)."))
            continue
        full = urljoin(page_url, act) if act else page_url
        ap = urlparse(full)
        if ap.scheme not in ("http", "https"):
            continue
        ah = (ap.hostname or "").lower()
        if re.fullmatch(r"[\d.]+", ah) and ah != page_host:
            flags.append(_flag("ip_form", "h", 30, f"نموذج الإدخال يرسل البيانات إلى عنوان IP مباشر: {ah}",
                               f"The input form posts data to a raw IP address: {ah}"))
        elif reg_domain(ah) != page_dom:
            flags.append(_flag("xdomain_form", "h", 30, f"نموذج تسجيل الدخول يرسل بياناتك إلى موقع آخر: {ah}",
                               f"The login form sends your data to a different site: {ah}"))
        elif ap.scheme == "http" and urlparse(page_url).scheme == "https":
            flags.append(_flag("insecure_form", "m", 15, "نموذج الإدخال يرسل البيانات بدون تشفير HTTPS.",
                               "The input form sends data without HTTPS encryption."))
    if p.pw_total and not sensitive:
        flags.append(_flag("pw_no_form", "m", 10, "الصفحة فيها حقل كلمة سر بدون نموذج واضح (قد يُرسل بالجافاسكربت).",
                           "The page has a password field without a clear form (may be sent by JavaScript)."))
    if sensitive and not flags:
        flags.append(_flag("form_ok", "g", 0, "نموذج الإدخال يرسل البيانات إلى نفس الموقع.",
                           "The input form posts data to the same site."))
    if p.hidden_iframes:
        flags.append(_flag("hidden_iframe", "m", 10, f"الصفحة فيها إطارات مخفية (iframe) عددها {p.hidden_iframes}.",
                           f"The page contains {p.hidden_iframes} hidden iframe(s)."))
    if p.refresh:
        rd = urlparse(urljoin(page_url, p.refresh)).hostname or ""
        if reg_domain(rd.lower()) != page_dom:
            flags.append(_flag("meta_refresh", "m", 10, f"الصفحة تحوّلك تلقائياً إلى موقع آخر: {rd}",
                               f"The page automatically redirects you to another site: {rd}"))
    return {"forms": len(p.forms), "sensitive_forms": sensitive, "password_fields": p.pw_total, "flags": flags}


def analyze_page(url):
    got, err = fetch(url)
    if got is None:
        return {"fetched": False, "error": err, "flags": []}
    html, final = got
    out = parse_html(html, final)
    out.update({"fetched": True, "final_url": final})
    return out
