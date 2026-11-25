"""Builds allowlist.txt (big trusted sites) from the Tranco list, to cut false alarms on famous sites.
1) download the Tranco top-sites CSV from tranco-list.eu   2) python make_allowlist.py top-1m.csv --n 10000"""
import argparse

from common import reg_domain
from engine import SHARED_HOSTS

ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("--n", type=int, default=10000)
ap.add_argument("--out", default="allowlist.txt")
a = ap.parse_args()
seen, out = set(), []
with open(a.csv, encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        d = line.strip().split(",")[-1].strip().lower()
        r = reg_domain(d) if d and d != "domain" else None
        if r and r not in seen and r not in SHARED_HOSTS:
            seen.add(r)
            out.append(r)
        if len(out) >= a.n:
            break
with open(a.out, "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print(f"wrote {len(out)} trusted domains to {a.out}")
