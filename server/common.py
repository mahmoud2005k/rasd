import os, re, sqlite3
from urllib.parse import urlparse

DB_PATH = os.getenv("DB_PATH", "rasd.db")


def db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS bad_links(
            url_norm TEXT PRIMARY KEY, host TEXT, path_empty INTEGER, source TEXT);
        CREATE INDEX IF NOT EXISTS i_bad_host ON bad_links(host);
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, host TEXT,
            type TEXT, notes TEXT, ip TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS i_rep_host ON reports(host);
        CREATE TABLE IF NOT EXISTS scans(
            id INTEGER PRIMARY KEY AUTOINCREMENT, host TEXT, verdict TEXT, score INTEGER,
            source TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE INDEX IF NOT EXISTS i_scan_day ON scans(created);
        """)


def norm(url):
    """Return (host, normalized_url, path_empty) or None if invalid."""
    url = (url or "").strip()
    if not url or len(url) > 2000:
        return None
    if "://" not in url:
        url = "http://" + url
    try:
        p = urlparse(url)
        host = (p.hostname or "").lower()
    except ValueError:
        return None
    if not host or "." not in host:
        return None
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/")
    query = ("?" + p.query) if p.query else ""
    return host, host + path + query, int(path == "" and not p.query)


def reg_domain(host):
    """Registered domain (last 2 labels, or 3 for names like example.com.ly)."""
    host = (host or "").lower().strip("[]")
    if ":" in host or re.fullmatch(r"[\d.]+", host):
        return None
    parts = host.split(".")
    if len(parts) < 2:
        return None
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in {"com", "net", "org", "edu", "gov", "co", "ac"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])
