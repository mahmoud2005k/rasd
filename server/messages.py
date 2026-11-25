"""Message check: finds links and scam wording in an SMS / WhatsApp text (port of the page's logic)."""
import re

from msg_data import CATS, CAT_TEXT, TLDS

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
_MAP = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ة": "ه", "ئ": "ي", "ؤ": "و"})
LINK_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"'،]+|(?<![a-z0-9-])(?:[a-z0-9-]+\.)+(?:" + TLDS + r")(?![a-z0-9])(?:/[^\s<>\"'،]*)?",
                     re.I)
SEV = {k: v["sev"] for k, v in CATS.items()}


def norm_ar(x):
    x = str(x).lower()
    x = re.sub("[\u064b-\u0652\u0640]", "", x)
    return x.translate(_MAP).translate(_DIGITS)


_PHRASES = {k: [(w, norm_ar(w)) for w in v["w"]] for k, v in CATS.items()}


def extract_links(text):
    out = []
    for m in LINK_RE.findall(text or ""):
        m = re.sub(r"[.,;:!?)\]}،؟]+$", "", m)
        if m and m not in out:
            out.append(m)
    return out


def _has(txt, p):
    if re.fullmatch(r"[a-z0-9 ]+", p):
        return re.search(r"\b" + re.escape(p) + r"\b", txt, re.A) is not None
    return p in txt


def scan_message(text):
    txt = norm_ar(text)
    cats, score = [], 0
    for k, words in _PHRASES.items():
        found = [w for w, p in words if _has(txt, p)]
        if found:
            cats.append({"k": k, "words": found[:4]})
            if k != "brand":
                score += CATS[k]["pts"]
    links = extract_links(text)
    if any(c["k"] == "brand" for c in cats) and (links or score > 0):
        score += CATS["brand"]["pts"]
    return {"cats": cats, "score": score, "links": links}


def verdict_of(score):
    return "dangerous" if score >= 50 else "suspicious" if score >= 20 else "safe"


def analyze_message(text, analyze_fn, max_links=5):
    """analyze_fn(url) -> engine report or None."""
    m = scan_message(text)
    items = []
    for link in m["links"][:max_links]:
        res = analyze_fn(link)
        if res:
            items.append({"url": link, "risk_score": res["risk_score"], "verdict": res["verdict"],
                          "reasons": [r for r in res["reasons"] if r["k"] not in ("https", "clean")][:3]})
    total = min(100, m["score"] + max((i["risk_score"] for i in items), default=0))
    return {"risk_score": total, "verdict": verdict_of(total), "text_score": m["score"],
            "flags": [{"k": c["k"], "sev": SEV[c["k"]], "words": c["words"], "ar": CAT_TEXT["ar"][c["k"]],
                       "en": CAT_TEXT["en"][c["k"]]} for c in m["cats"]],
            "links": items}
