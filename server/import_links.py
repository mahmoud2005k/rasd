"""Import a list of suspicious links into the Rasd database.

Usage:
    python import_links.py links.txt --source urlhaus
Accepted files: .txt (one link per line, # = comment) or .csv (column named url, or first column).
"""
import argparse, csv
from common import db, init_db, norm


def read_links(path):
    with open(path, encoding="utf-8-sig", errors="ignore", newline="") as f:
        if path.lower().endswith(".csv"):
            rows = list(csv.reader(f))
            col = 0
            if rows and "url" in [h.strip().lower() for h in rows[0]]:
                col = [h.strip().lower() for h in rows[0]].index("url")
                rows = rows[1:]
            for r in rows:
                if len(r) > col:
                    yield r[col]
        else:
            for line in f:
                yield line


def load_file(path, source="import"):
    """Import a file into the database. Returns (valid, skipped)."""
    init_db()
    ok = bad = 0
    with db() as c:
        for line in read_links(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            n = norm(line)
            if not n:
                bad += 1
                continue
            c.execute("INSERT OR IGNORE INTO bad_links VALUES(?,?,?,?)", (n[1], n[0], n[2], source))
            ok += 1
    return ok, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--source", default="import")
    a = ap.parse_args()
    ok, bad = load_file(a.file, a.source)
    with db() as c:
        total = c.execute("SELECT COUNT(*) FROM bad_links").fetchone()[0]
    print(f"read: {ok} valid, {bad} skipped. Database now holds {total} links.")


if __name__ == "__main__":
    main()
