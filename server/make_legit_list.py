"""Builds legit_links.txt from the Tranco top-sites list (download the CSV from tranco-list.eu).
    python make_legit_list.py top-1m.csv --n 5000
WARNING: Tranco has domains only. Phishing links usually have paths, so a model could learn
'has a path = phishing'. Use --paths to add typical paths (synthetic augmentation, say so in
your report), or better, use a real labeled dataset with train_model.py --csv."""
import argparse
import random

ap = argparse.ArgumentParser()
ap.add_argument("csv")
ap.add_argument("--n", type=int, default=5000)
ap.add_argument("--out", default="legit_links.txt")
ap.add_argument("--paths", action="store_true")
a = ap.parse_args()

PATHS = ["", "/", "/about", "/contact", "/login", "/account/login", "/signin", "/products", "/search?q=news",
         "/en/index.html", "/blog/2024/post", "/help/support", "/cart", "/user/profile", "/download", "/pricing"]
rnd = random.Random(42)
domains = []
with open(a.csv, encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        parts = line.strip().split(",")
        d = parts[-1].strip().lower()
        if d and "." in d and d != "domain":
            domains.append(d)
        if len(domains) >= a.n * 3:
            break
rnd.shuffle(domains)
with open(a.out, "w", encoding="utf-8") as out:
    for d in domains[:a.n]:
        out.write(f"https://{d}{rnd.choice(PATHS) if a.paths and rnd.random() < 0.7 else '/'}\n")
print(f"wrote {min(a.n, len(domains))} links to {a.out}", "(with synthetic paths)" if a.paths else "(domains only)")
