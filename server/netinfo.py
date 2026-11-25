"""Network facts about a domain: age (RDAP / WHOIS) and DNS."""
import os
import re
import socket
import time
from datetime import datetime, timezone

import requests

from common import reg_domain

NET_TIMEOUT = float(os.getenv("NET_TIMEOUT", "10"))
RDAP_DIRECT = {"com": "https://rdap.verisign.com/com/v1/domain/{d}", "net": "https://rdap.verisign.com/net/v1/domain/{d}"}
_age_cache = {}


def _rdap_days(url):
    try:
        r = requests.get(url, timeout=NET_TIMEOUT, headers={"Accept": "application/rdap+json", "User-Agent": "Rasd-student-project"})
    except requests.RequestException as e:
        print(f"[rdap] {url} -> {type(e).__name__}: {e}")
        return None
    if not r.ok:
        print(f"[rdap] {url} -> HTTP {r.status_code}")
        return None
    try:
        for ev in r.json().get("events", []):
            if ev.get("eventAction") == "registration":
                dt = datetime.fromisoformat(str(ev["eventDate"]).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return max(0, (datetime.now(timezone.utc) - dt).days)
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        print(f"[rdap] bad data from {url}: {e}")
    return None


def domain_age_days(host):
    """Age in days: registry RDAP (fast for com/net), rdap.org, then python-whois. None if unknown."""
    d = reg_domain(host)
    if not d or not re.fullmatch(r"[a-z0-9.-]+", d):
        return None
    hit = _age_cache.get(d)
    if hit and time.time() < hit[0]:
        return hit[1]
    tld = d.rsplit(".", 1)[-1]
    days = _rdap_days(RDAP_DIRECT[tld].format(d=d)) if tld in RDAP_DIRECT else None
    if days is None:
        days = _rdap_days(f"https://rdap.org/domain/{d}")
    if days is None:
        try:
            import whois
            cd = whois.whois(d).creation_date
            cd = cd[0] if isinstance(cd, list) else cd
            if cd:
                if cd.tzinfo is None:
                    cd = cd.replace(tzinfo=timezone.utc)
                days = max(0, (datetime.now(timezone.utc) - cd).days)
        except Exception as e:
            print(f"[whois] {d} -> {type(e).__name__}: {e}")
    print(f"[age] {d} -> {days} days" if days is not None else f"[age] {d} -> unknown")
    _age_cache[d] = (time.time() + (86400 if days is not None else 300), days)
    return days


def dns_info(host):
    h = host.strip("[]")
    out = {"resolves": False, "ips": [], "ns": [], "mx": []}
    try:
        out["ips"] = sorted({i[4][0] for i in socket.getaddrinfo(h, None)})[:6]
        out["resolves"] = bool(out["ips"])
    except (socket.gaierror, UnicodeError):
        pass
    d = reg_domain(h)
    if d:
        try:
            import dns.resolver
            res = dns.resolver.Resolver()
            res.lifetime = res.timeout = 3
            for rt, key, attr in (("NS", "ns", "target"), ("MX", "mx", "exchange")):
                try:
                    out[key] = sorted(str(getattr(r, attr)).rstrip(".") for r in res.resolve(d, rt))[:5]
                except Exception:
                    pass
        except ImportError:
            pass
    return out
