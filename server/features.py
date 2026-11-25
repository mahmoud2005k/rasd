"""URL feature extraction. The SAME code is used for training and for the API,
so the model always sees the same features."""
import math
import re
from collections import Counter

BRANDS = {"paypal": "paypal.com", "google": "google.com", "facebook": "facebook.com", "instagram": "instagram.com",
          "whatsapp": "whatsapp.com", "telegram": "telegram.org", "apple": "apple.com", "microsoft": "microsoft.com",
          "amazon": "amazon.com", "netflix": "netflix.com", "binance": "binance.com", "libyana": "libyana.ly",
          "almadar": "almadar.ly", "tiktok": "tiktok.com", "twitter": "twitter.com"}
OFFICIAL = {"microsoft.com", "microsoftonline.com", "live.com", "office.com", "google.com", "googleusercontent.com",
            "googleapis.com", "facebook.com", "fb.com", "instagram.com", "whatsapp.com", "whatsapp.net", "amazon.com",
            "amazonaws.com", "apple.com", "icloud.com", "paypal.com", "paypal.me", "netflix.com", "telegram.org",
            "t.me", "tiktok.com", "binance.com", "twitter.com", "x.com", "libyana.ly", "almadar.ly"}
BAD_TLD = {"xyz", "top", "click", "icu", "gq", "tk", "ml", "cf", "ga", "work", "loan", "zip", "mov", "rest", "cam",
           "monster", "buzz"}
SHORT = {"bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd", "rb.gy", "shorturl.at", "goo.gl", "ow.ly", "tiny.cc"}
KEYWORDS = ["login", "signin", "verify", "secure", "update", "account", "password", "bank", "wallet", "gift", "prize",
            "free", "bonus", "confirm", "suspend", "urgent", "claim", "otp"]
# zero-width, bidi controls, soft hyphen, and odd space characters
INVISIBLE = re.compile("[\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\u00ad\u180e\u00a0\u2000-\u200a\u3000]")
EXEC_EXT = re.compile(r"\.(exe|apk|scr|bat|msi|vbs|jar|cmd|ps1|iso|dmg|zip|rar|7z)$", re.I)

FEATURE_TEXT = {
    "url_len": ("طول الرابط الكلي", "Total URL length"),
    "host_len": ("طول اسم الدومين", "Domain name length"),
    "path_len": ("طول مسار الرابط", "Path length"),
    "query_len": ("طول معاملات الرابط", "Query string length"),
    "n_dots": ("عدد النقاط في الدومين", "Dots in the domain"),
    "n_hyphens": ("عدد الشرطات في الدومين", "Hyphens in the domain"),
    "n_digits_host": ("عدد الأرقام في الدومين", "Digits in the domain"),
    "digit_ratio": ("نسبة الأرقام في الدومين", "Digit ratio in the domain"),
    "n_subdomains": ("عدد الدومينات الفرعية", "Number of subdomains"),
    "is_ip": ("استخدام عنوان IP بدل اسم", "Uses an IP address instead of a name"),
    "has_at": ("وجود رمز @", "Contains @"),
    "is_https": ("لا يستخدم HTTPS", "Does not use HTTPS"),
    "nonstd_port": ("منفذ غير معتاد", "Unusual port"),
    "bad_tld": ("امتداد دومين شائع في الاحتيال", "Scam-prone domain extension"),
    "tld_len": ("طول امتداد الدومين", "Extension length"),
    "is_shortener": ("رابط مختصر", "URL shortener"),
    "entropy_host": ("عشوائية اسم الدومين", "Randomness of the domain name"),
    "entropy_path": ("عشوائية مسار الرابط", "Randomness of the path"),
    "max_run": ("أطول تكرار لحرف واحد", "Longest run of one repeated character"),
    "triple_letters": ("تكرار ثلاثة أحرف متطابقة", "Triple repeated letters"),
    "cons_run": ("حروف ساكنة متتالية طويلة", "Long consonant run"),
    "vowel_ratio": ("نسبة الحروف المتحركة", "Vowel ratio"),
    "has_puny": ("دومين Punycode", "Punycode domain"),
    "non_ascii_host": ("حروف غير لاتينية في الدومين", "Non-ASCII characters in the domain"),
    "invisible_chars": ("أحرف أو مسافات مخفية", "Invisible characters or spaces"),
    "mixed_script": ("خلط أبجديات (هجوم تطابق بصري)", "Mixed scripts (homograph attack)"),
    "brand_spoof": ("انتحال اسم جهة معروفة", "Brand impersonation"),
    "brand_in_path": ("اسم جهة معروفة في المسار", "Brand name in the path"),
    "kw_count": ("كلمات استدراج", "Lure keywords"),
    "redirect_param": ("رابط داخل الرابط (تحويل)", "Link inside the link (redirect)"),
    "exec_ext": ("ملف تنفيذي في الرابط", "Executable file in the link"),
    "n_params": ("عدد المعاملات", "Number of parameters"),
    "path_depth": ("عمق المسار", "Path depth"),
    "pct_encoded": ("ترميز كثيف", "Heavy percent-encoding"),
    "special_chars": ("رموز خاصة", "Special characters"),
    "leet_host": ("استبدال حروف بأرقام", "Letter-to-digit swaps"),
    "longest_label": ("طول أطول جزء في الدومين", "Longest domain label"),
}


def _entropy(t):
    if not t:
        return 0.0
    n = len(t)
    return -sum(v / n * math.log2(v / n) for v in Counter(t).values())


def split_url(raw):
    s = raw.strip()
    m = re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", s)
    scheme = m.group(0)[:-3].lower() if m else "http"
    rest = s[m.end():] if m else s
    k = re.search(r"[/?#]", rest)
    authority = rest[:k.start()] if k else rest
    tail = rest[k.start():] if k else ""
    userinfo, at, hostport = authority.rpartition("@")
    host, port = hostport, ""
    if hostport.startswith("["):
        end = hostport.find("]")
        if end != -1:
            host = hostport[:end + 1]
            port = hostport[end + 2:] if hostport[end + 1:end + 2] == ":" else ""
    elif ":" in hostport:
        host, _, port = hostport.rpartition(":")
    tail = tail.split("#", 1)[0]
    path, _, query = tail.partition("?")
    return {"scheme": scheme, "host": host.lower(), "port": port, "user": userinfo if at else "",
            "path": path, "query": query}


def _mixed_script(host):
    for label in host.split("."):
        latin = re.search(r"[a-z]", label, re.I)
        other = re.search("[\u0370-\u03ff\u0400-\u04ff]", label)
        if latin and other:
            return True
    return False


def extract(raw):
    raw = raw or ""
    u = split_url(raw)
    host, path, query = u["host"], u["path"], u["query"]
    h = host.strip("[]")
    if h.startswith("www."):
        h = h[4:]  # "www." and the scheme are ignored so equal sites give equal features
    canon = h + path + (("?" + query) if query else "")
    labels = [x for x in h.split(".") if x]
    tld = labels[-1] if labels else ""
    base = ".".join(labels[-2:]) if len(labels) >= 2 else h
    name = ".".join(labels[:-1]) if len(labels) > 1 else h
    name_nw = re.sub(r"^www\.", "", name)
    longest = max(labels, key=len) if labels else ""
    is_ip = bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", h)) or ":" in h
    flat = name.replace("0", "o").replace("1", "l").replace("3", "e").replace("$", "s").replace("rn", "m").replace("vv", "w")
    low_path = (path + "?" + query).lower()
    spoof = any(b in flat and base != d and not h.endswith("." + d) and base not in OFFICIAL for b, d in BRANDS.items())
    in_path = (not spoof) and any(b in low_path and base != d and not h.endswith("." + d) and base not in OFFICIAL
                                  for b, d in BRANDS.items())
    letters = re.sub(r"[^a-z]", "", longest)
    digits = sum(c.isdigit() for c in h)
    return {
        "url_len": len(canon), "host_len": len(h), "path_len": len(path), "query_len": len(query),
        "n_dots": h.count("."), "n_hyphens": h.count("-"), "n_digits_host": digits,
        "digit_ratio": digits / max(1, len(h)), "n_subdomains": max(0, len(labels) - 2),
        "is_ip": int(is_ip), "has_at": int(bool(u["user"]) or "@" in raw), "is_https": int(u["scheme"] == "https"),
        "nonstd_port": int(u["port"] not in ("", "80", "443")), "bad_tld": int(tld in BAD_TLD), "tld_len": len(tld),
        "is_shortener": int(base in SHORT), "entropy_host": _entropy(name_nw), "entropy_path": _entropy(path + query),
        "max_run": max((len(m.group(0)) for m in re.finditer(r"(.)\1*", h)), default=0),
        "triple_letters": len(re.findall(r"([a-z])\1\1", name_nw)),
        "cons_run": max((len(m) for m in re.findall(r"[bcdfghjklmnpqrstvwxz]+", h)), default=0),
        "vowel_ratio": sum(c in "aeiouy" for c in letters) / max(1, len(letters)),
        "has_puny": int("xn--" in h), "non_ascii_host": sum(ord(c) > 127 for c in host),
        "invisible_chars": len(INVISIBLE.findall(raw.strip())), "mixed_script": int(_mixed_script(host)),
        "brand_spoof": int(spoof), "brand_in_path": int(in_path),
        "kw_count": sum(k in (h + low_path) for k in KEYWORDS),
        "redirect_param": int(bool(re.search(r"https?(:|%3a)(//|%2f%2f)", query, re.I))),
        "exec_ext": int(bool(EXEC_EXT.search(path))),
        "n_params": (query.count("&") + 1) if query else 0,
        "path_depth": len([p for p in path.split("/") if p]),
        "pct_encoded": len(re.findall(r"%[0-9a-fA-F]{2}", canon)),
        "special_chars": len(re.findall(r"[!$'()*+,;~|\\^`{}\[\]<>]", raw)),
        "leet_host": int(bool(re.search(r"[a-z][0-9][a-z]", name_nw))),
        "longest_label": len(longest),
    }


FEATURE_NAMES = list(extract("http://a.com").keys())
# The scheme (http/https) is NOT given to the AI model: in public datasets it is an artifact
# (e.g. many legitimate links are stored without it), which makes the model unreliable.
MODEL_FEATURES = [n for n in FEATURE_NAMES if n != "is_https"]
