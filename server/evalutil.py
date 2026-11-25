"""Shared helpers for evaluate_system.py and report_figures.py (fresh links never used in training)."""
import csv
import random
import re

import numpy as np

import ml
import rules
from common import reg_domain
from engine import ALLOW
from features import extract


def read_labeled(path, url_col="url", label_col="type", phish="phishing", legit="benign"):
    ph, lg = [], []
    with open(path, encoding="utf-8-sig", errors="ignore", newline="") as f:
        for row in csv.DictReader(f):
            u, lab = (row.get(url_col) or "").strip(), (row.get(label_col) or "").strip().lower()
            if u and lab == phish:
                ph.append(u)
            elif u and lab == legit:
                lg.append(u)
    return ph, lg


def fresh_sample(path, n=2000, train_n=5000, **kw):
    """Rebuilds the exact training sample of train_model.py (seed 42) and returns links OUTSIDE it."""
    ph, lg = read_labeled(path, **kw)
    ph, lg = sorted(set(ph)), sorted(set(lg))
    k = min(train_n, len(ph), len(lg))
    rnd = random.Random(42)
    used = set(rnd.sample(ph, k)) | set(rnd.sample(lg, k))
    rnd2 = random.Random(7)
    fp = [u for u in ph if u not in used]
    fl = [u for u in lg if u not in used]
    m = min(n, len(fp), len(fl))
    urls = rnd2.sample(fp, m) + rnd2.sample(fl, m)
    return urls, np.array([1] * m + [0] * m)


def neutral(u):
    """The dataset stores many links without http(s)://. Give every link https:// so the scheme rule is neutral."""
    return "https://" + re.sub(r"^https?://", "", u.strip(), flags=re.I)


def score_all(urls):
    """Offline scores (no network): rules, AI probability and the hybrid score used by the real system."""
    b = ml.load()
    if b is None:
        raise SystemExit("model.joblib not found. Train the model first (train_model.py).")
    urls = [neutral(u) for u in urls]
    X = np.array([[extract(u)[n] for n in b["features"]] for u in urls], dtype=float)
    p = b["model"].predict_proba(X)[:, 1]
    rule, hybrid = [], []
    for u, pi in zip(urls, p):
        got = rules.evaluate(u, ALLOW)
        rs = got[0] if got else 0
        pts = round(max(0.0, (pi - 0.5) * 2) * 45)
        reg = reg_domain(re.sub(r"^https?://", "", u).split("/")[0])
        if reg in rules.OFFICIAL or reg in ALLOW:
            pts = round(pts * 0.4)
        rule.append(rs)
        hybrid.append(min(100, rs + pts))
    return {"rules": np.array(rule), "ml": p * 100, "hybrid": np.array(hybrid)}
