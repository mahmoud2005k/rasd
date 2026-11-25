"""Rule engine: Python port of the page's rules (same weights, same texts), so the API alone returns the full report."""
import math
import re
from collections import Counter

from features import (BAD_TLD, BRANDS as _B, INVISIBLE, KEYWORDS, OFFICIAL as _O, SHORT, split_url)
from rule_texts import RULE_TEXT

BRANDS = dict(_B)
BRANDS.update({"youtube": "youtube.com", "gmail": "gmail.com", "outlook": "outlook.com", "linkedin": "linkedin.com",
               "snapchat": "snapchat.com", "aliexpress": "aliexpress.com", "spotify": "spotify.com",
               "mastercard": "mastercard.com"})
OFFICIAL = set(_O) | {"youtube.com", "gmail.com", "outlook.com", "linkedin.com", "snapchat.com", "aliexpress.com",
                      "spotify.com", "mastercard.com"}


def lev(a, b):
    """Edit distance with swaps (Damerau-Levenshtein, restricted)."""
    m, n = len(a), len(b)
    d = [[i] + [0] * n for i in range(m + 1)]
    d[0] = list(range(n + 1))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[m][n]


def _entropy(t):
    n = len(t)
    return -sum(v / n * math.log2(v / n) for v in Counter(t).values()) if n else 0.0


def evaluate(raw, trusted=frozenset()):
    """Returns (score 0-100, reasons) or None when the text is not a usable link."""
    raw = raw or ""
    t0 = raw.strip()
    if not t0:
        return None
    u = split_url(t0)
    has_scheme = bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", t0))
    s = t0 if has_scheme else "http://" + t0
    host_raw = INVISIBLE.sub("", u["host"])
    h = host_raw
    if any(ord(c) > 127 for c in h):
        try:
            h = h.encode("idna").decode("ascii")  # what the browser does: non-ASCII names become xn--
        except UnicodeError:
            pass
    if "." not in h and not h.startswith("["):
        return None
    parts = h.split(".")
    tld = parts[-1]
    base = ".".join(parts[-2:])
    subs = max(0, len(parts) - 2)
    name = ".".join(parts[:-1])
    path, query = u["path"] or "/", u["query"]
    search = ("?" + query) if query else ""
    ok_domain = base in OFFICIAL or base in trusted

    reasons, total = [], 0

    def add(k, pts, sev, x=""):
        nonlocal total
        total += pts
        ar, en = RULE_TEXT[k]
        reasons.append({"k": k, "sev": sev, "pts": pts, "x": str(x) if x else "",
                        "ar": ar + (str(x) if x else ""), "en": en + (str(x) if x else "")})

    # hidden characters and look-alike attacks (checked on the original text)
    inv = INVISIBLE.findall(t0)
    if inv:
        add("invisible", 35, "h", ", ".join(dict.fromkeys("U+%04X" % ord(c) for c in inv)))
    if any(re.search("[a-z]", lab, re.I) and re.search("[\u0370-\u03ff\u0400-\u04ff]", lab) for lab in host_raw.split(".")):
        add("homograph", 40, "h")
    if len(re.findall(r"[!$'()*+,;~|\\^`{}\[\]<>]", t0)) >= 3:
        add("symbols", 8, "m")

    if has_scheme and u["scheme"] == "http":
        add("nohttps", 15, "m")          # only when "http://" was typed on purpose
    elif has_scheme:
        add("https", 0, "g")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", h) or h.startswith("["):
        add("ip", 30, "h")
    if "xn--" in h:
        add("puny", 25, "h")
    if u["user"]:
        add("at", 25, "h")
    if tld in BAD_TLD:
        add("tld", 15, "m", "." + tld)
    if base in SHORT:
        add("short", 20, "m")
    if subs >= 3:
        add("sub", 15, "m")
    if len(raw) > 100:
        add("len", 10, "m")
    if name.replace("xn--", "").count("-") >= 3:
        add("hy", 10, "m")
    if sum(c.isdigit() for c in name) >= 4 or re.search(r"[a-z]\d[a-z]", name):
        add("dg", 12, "m")

    flat = name.replace("0", "o").replace("1", "l").replace("3", "e").replace("$", "s").replace("rn", "m").replace("vv", "w")
    if not ok_domain:
        for b, dom in BRANDS.items():
            if b in flat and base != dom and not h.endswith("." + dom):
                add("brand", 35, "h", b)
                break
    found = [k for k in KEYWORDS if k in (h + path + search).lower()]
    if found:
        add("kw", min(24, len(found) * 8), "h" if len(found) > 1 else "m", ", ".join(found[:4]))
    if u["port"] not in ("", "80", "443"):
        add("port", 10, "m")
    if len(re.findall(r"%[0-9a-f]{2}", s, re.I)) > 5:
        add("enc", 8, "m")

    rep = re.sub(r"^www\.", "", name)
    if re.search(r"([a-z])\1\1|([0-9])\2{3,}", rep):
        add("charrep", 10, "m")
    labels = [p for p in parts[:-1]]
    label = max(labels, key=len) if labels else ""
    letters = re.sub(r"[^a-z]", "", label)
    cons_ratio = len(re.sub(r"[aeiouy]", "", letters)) / max(1, len(letters))
    if (not label.startswith("xn--") and len(label) >= 10 and _entropy(label) >= 3.4
            and (re.search(r"\d", label) or cons_ratio > 0.8)):
        add("random", 15, "m")
    if re.search(r"[bcdfghjklmnpqrstvwxz]{6,}", label):
        add("cons", 10, "m")
    if len(h) > 30:
        add("longhost", 8, "m")

    ex = re.search(r"\.(exe|apk|scr|bat|msi|vbs|jar|cmd|ps1|iso|dmg)$", path, re.I)
    ar_ = re.search(r"\.(zip|rar|7z)$", path, re.I)
    if ex:
        add("file", 25, "h", "." + ex.group(1).lower())
    elif ar_:
        add("archive", 10, "m", "." + ar_.group(1).lower())
    if re.search(r"https?(:|%3a)(//|%2f%2f)", search, re.I):
        add("redir", 15, "m")

    low = (path + search).lower()
    if not any(r["k"] == "brand" for r in reasons) and not ok_domain:
        for b, dom in BRANDS.items():
            if b in low and base != dom and not h.endswith("." + dom):
                add("brandpath", 15, "m", b)
                break
    if not any(r["k"] == "brand" for r in reasons) and not ok_domain:
        toks = [x for x in re.split(r"[.\-_]", rep) if len(x) >= 6]
        for b in BRANDS:
            if len(b) < 5:
                continue
            lim = 1 if len(b) <= 8 else 2
            hit = next((x for x in toks if x != b and abs(len(x) - len(b)) <= lim and lev(x, b) <= lim), None)
            if hit:
                add("typo", 30, "m", f"{hit} → {b}")
                break

    if all(r["sev"] == "g" for r in reasons):
        add("clean", 0, "g")
    return min(100, total), reasons
