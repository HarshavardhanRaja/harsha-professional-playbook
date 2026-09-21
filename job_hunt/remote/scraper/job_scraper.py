#!/usr/bin/env python3
from __future__ import annotations
"""
Remote DE Job Scraper
=====================
Fetches remote Data Engineering jobs from 9 sources, filters for India-compatible
roles, deduplicates against all previous runs, and writes only fresh leads to a
timestamped CSV.

Usage:
    pip install -r requirements.txt
    python job_scraper.py

Output:
    ../leads/jobs_YYYY-MM-DD.csv
"""

import csv
from typing import Optional
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import requests

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG  ← Edit these without touching anything else
# ─────────────────────────────────────────────────────────────────────────────

# Job title keywords to INCLUDE (case-insensitive, any match = pass)
ROLE_KEYWORDS = [
    "data engineer",
    "analytics engineer",
    "data platform engineer",
    "data infrastructure engineer",
    "analytics engineering",
    "data pipeline",
    "etl engineer",
    "elt engineer",
    "data architect",
]

# Terms in title/description that HARD-EXCLUDE the job
EXCLUDE_TERMS = [
    "us only",
    "united states only",
    "w-2",
    "w2 only",
    "must be based in us",
    "must be located in us",
    "americas only",
    "north america only",
    "est required",
    "pst required",
    "cst required",
    "us citizens",
    "must be eligible to work in the us",
]

# Terms that signal India/APAC compatibility (boost india_ok score)
INDIA_OK_SIGNALS = [
    "india",
    "apac",
    "worldwide",
    "global",
    "async-first",
    "async first",
    "async culture",
    "open to all timezones",
    "timezone flexible",
    "all timezones",
    "remote global",
    "fully remote",
    "work from anywhere",
]

# Skip jobs older than this many days (0 = no limit)
FRESHNESS_DAYS = 60

# Paths (relative to this script)
SCRIPT_DIR = Path(__file__).parent
SEEN_FILE = SCRIPT_DIR / "seen_jobs.json"
COMPANIES_FILE = SCRIPT_DIR / "companies.txt"
LEADS_DIR = SCRIPT_DIR.parent / "leads"
LEADS_DIR.mkdir(parents=True, exist_ok=True)

# HTTP request timeout (seconds)
REQUEST_TIMEOUT = 15

# Delay between per-company API calls (seconds) to avoid rate limiting
PER_COMPANY_DELAY = 0.4

# ─────────────────────────────────────────────────────────────────────────────
# SEEN JOBS  — persistent deduplication across runs
# ─────────────────────────────────────────────────────────────────────────────

def load_seen() -> dict:
    """Load the seen-jobs store from disk."""
    if SEEN_FILE.exists():
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {"urls": [], "pairs": []}


def save_seen(seen: dict) -> None:
    """Persist the seen-jobs store to disk."""
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)


def is_duplicate(job: dict, seen: dict) -> bool:
    """Return True if this job was seen in any previous run."""
    url_key = job.get("url", "").strip().lower()
    pair_key = _pair_key(job)
    return url_key in seen["urls"] or pair_key in seen["pairs"]


def mark_seen(job: dict, seen: dict) -> None:
    """Add this job to the seen store (in memory; call save_seen() after loop)."""
    url_key = job.get("url", "").strip().lower()
    pair_key = _pair_key(job)
    if url_key and url_key not in seen["urls"]:
        seen["urls"].append(url_key)
    if pair_key and pair_key not in seen["pairs"]:
        seen["pairs"].append(pair_key)


def _pair_key(job: dict) -> str:
    company = re.sub(r"\s+", " ", job.get("company", "").lower().strip())
    title = re.sub(r"\s+", " ", job.get("role", "").lower().strip())
    return f"{company}||{title}"

# ─────────────────────────────────────────────────────────────────────────────
# FILTER ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def passes_role_filter(job: dict) -> bool:
    """Title must contain at least one role keyword."""
    title = job.get("role", "").lower()
    return any(kw in title for kw in ROLE_KEYWORDS)


def passes_exclude_filter(job: dict) -> bool:
    """Return False if any hard-exclusion term is found in title or description."""
    text = (job.get("role", "") + " " + job.get("_description", "")).lower()
    return not any(term in text for term in EXCLUDE_TERMS)


def india_ok_score(job: dict) -> int:
    """
    Return 0–3 India-compatibility confidence score.
    3 = explicitly India/APAC/worldwide
    2 = async-first / no restriction / globally remote
    1 = no signal either way
    0 = hard exclusion found (should already be filtered, but safety net)
    """
    text = (
        job.get("role", "") + " " +
        job.get("location_tag", "") + " " +
        job.get("_description", "")
    ).lower()

    # Hard exclusions → 0
    if any(term in text for term in EXCLUDE_TERMS):
        return 0

    # Count positive signals
    hits = sum(1 for sig in INDIA_OK_SIGNALS if sig in text)
    if hits >= 2:
        return 3
    if hits == 1:
        return 2
    return 1


def is_fresh(job: dict) -> bool:
    """Return True if job is within the freshness window (or FRESHNESS_DAYS=0)."""
    if FRESHNESS_DAYS == 0:
        return True
    posted = job.get("posted_date")
    if not posted:
        return True  # unknown date → include
    try:
        dt = datetime.strptime(posted, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc) - timedelta(days=FRESHNESS_DAYS)
        return dt >= cutoff
    except ValueError:
        return True


def normalize_date(raw) -> str:
    """Convert various date formats to YYYY-MM-DD string."""
    if not raw:
        return ""
    # Already a string
    if isinstance(raw, str):
        # Try ISO 8601
        for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw[:19], fmt[:len(fmt)]).\
                    strftime("%Y-%m-%d")
            except ValueError:
                continue
        # Try RSS/email format from feedparser
        try:
            import email.utils
            ts = email.utils.parsedate_to_datetime(raw)
            return ts.strftime("%Y-%m-%d")
        except Exception:
            pass
        return raw[:10]
    # Unix timestamp (int or float)
    if isinstance(raw, (int, float)):
        # Lever uses milliseconds
        if raw > 1e12:
            raw = raw / 1000
        return datetime.fromtimestamp(raw, tz=timezone.utc).strftime("%Y-%m-%d")
    return ""

# ─────────────────────────────────────────────────────────────────────────────
# HTTP HELPER
# ─────────────────────────────────────────────────────────────────────────────

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (compatible; RemoteDEJobScraper/1.0; "
        "personal job search tool)"
    )
})


def get_json(url: str, **kwargs) -> Optional[object]:
    try:
        r = SESSION.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"    ⚠ HTTP error for {url}: {e}")
        return None


def get_rss(url: str) -> list:
    try:
        feed = feedparser.parse(url)
        return feed.entries
    except Exception as e:
        print(f"    ⚠ RSS error for {url}: {e}")
        return []

# ─────────────────────────────────────────────────────────────────────────────
# SOURCE FETCHERS
# ─────────────────────────────────────────────────────────────────────────────

def fetch_remotive() -> list[dict]:
    """Remotive public API — category=data"""
    data = get_json("https://remotive.com/api/remote-jobs?category=data&limit=200")
    if not data:
        return []
    jobs = []
    for item in data.get("jobs", []):
        jobs.append({
            "company": item.get("company_name", ""),
            "role": item.get("title", ""),
            "url": item.get("url", ""),
            "source": "Remotive",
            "posted_date": normalize_date(item.get("publication_date", "")),
            "salary": item.get("salary", ""),
            "location_tag": item.get("candidate_required_location", ""),
            "_description": item.get("description", ""),
        })
    return jobs


def fetch_remoteok() -> list[dict]:
    """RemoteOK JSON API — tag=data-engineer"""
    # First item is a legal/metadata object — skip it
    data = get_json(
        "https://remoteok.com/api?tag=data-engineer",
        headers={"Accept": "application/json"},
    )
    if not data or not isinstance(data, list):
        return []
    jobs = []
    for item in data[1:]:  # skip first metadata item
        if not isinstance(item, dict):
            continue
        salary = ""
        s_min = item.get("salary_min", 0)
        s_max = item.get("salary_max", 0)
        if s_min and s_max:
            salary = f"${s_min:,}–${s_max:,}"
        elif s_min:
            salary = f"${s_min:,}+"
        jobs.append({
            "company": item.get("company", ""),
            "role": item.get("position", ""),
            "url": item.get("url", ""),
            "source": "RemoteOK",
            "posted_date": normalize_date(item.get("epoch")),
            "salary": salary,
            "location_tag": item.get("location", ""),
            "_description": item.get("description", ""),
        })
    return jobs


def fetch_himalayas() -> list[dict]:
    """Himalayas API — Data Engineering category, cursor-paginated"""
    jobs = []
    cursor = None
    pages = 0
    while pages < 5:  # max 5 pages = 100 jobs
        url = "https://himalayas.app/jobs/api?categories=Data-Engineering&limit=20"
        if cursor:
            url += f"&cursor={cursor}"
        data = get_json(url)
        if not data:
            break
        for item in data.get("jobs", []):
            salary = ""
            s_min = item.get("minSalary")
            s_max = item.get("maxSalary")
            period = item.get("salaryPeriod", "")
            currency = item.get("currency", "USD") or "USD"
            if s_min and s_max:
                salary = f"{currency} {s_min:,}–{s_max:,}/{period}"
            elif s_min:
                salary = f"{currency} {s_min:,}+/{period}"

            loc = ", ".join(item.get("locationRestrictions") or [])
            jobs.append({
                "company": item.get("companyName", ""),
                "role": item.get("title", ""),
                "url": item.get("applicationLink", ""),
                "source": "Himalayas",
                "posted_date": normalize_date(item.get("pubDate")),
                "salary": salary,
                "location_tag": loc,
                "_description": item.get("description", ""),
            })
        cursor = data.get("nextCursor")
        if not cursor:
            break
        pages += 1
        time.sleep(0.5)
    return jobs


def fetch_weworkremotely() -> list[dict]:
    """We Work Remotely RSS — Data & Analytics category"""
    entries = get_rss(
        "https://weworkremotely.com/categories/remote-data-science-jobs.rss"
    )
    jobs = []
    for entry in entries:
        jobs.append({
            "company": entry.get("author", ""),
            "role": entry.get("title", ""),
            "url": entry.get("link", ""),
            "source": "WeWorkRemotely",
            "posted_date": normalize_date(entry.get("published", "")),
            "salary": "",
            "location_tag": "",
            "_description": entry.get("summary", ""),
        })
    return jobs


def fetch_jobicy() -> list[dict]:
    """Jobicy RSS — data-engineer category, worldwide"""
    entries = get_rss(
        "https://jobicy.com/?feed=job_feed"
        "&job_categories=data-engineer"
        "&job_types=full-time"
        "&search_region=worldwide"
    )
    jobs = []
    for entry in entries:
        jobs.append({
            "company": entry.get("author", ""),
            "role": entry.get("title", ""),
            "url": entry.get("link", ""),
            "source": "Jobicy",
            "posted_date": normalize_date(entry.get("published", "")),
            "salary": "",
            "location_tag": "worldwide",
            "_description": entry.get("summary", ""),
        })
    return jobs


def fetch_arbeitnow() -> list[dict]:
    """Arbeitnow API — filter remote: true only"""
    jobs = []
    page = 1
    while page <= 3:  # paginate up to 3 pages
        data = get_json(f"https://arbeitnow.com/api/job-board-api?page={page}")
        if not data:
            break
        items = data.get("data", [])
        if not items:
            break
        for item in items:
            if not item.get("remote", False):
                continue
            jobs.append({
                "company": item.get("company_name", ""),
                "role": item.get("title", ""),
                "url": item.get("url", ""),
                "source": "Arbeitnow",
                "posted_date": normalize_date(item.get("created_at")),
                "salary": "",
                "location_tag": item.get("location", "Remote"),
                "_description": item.get("description", ""),
            })
        page += 1
        time.sleep(0.5)
    return jobs


def _load_companies() -> list[tuple[str, str]]:
    """Parse companies.txt → list of (slug, platform) tuples."""
    companies = []
    if not COMPANIES_FILE.exists():
        return companies
    with open(COMPANIES_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                slug, platform = line.split("|", 1)
                companies.append((slug.strip(), platform.strip().lower()))
    return companies


def fetch_greenhouse() -> list[dict]:
    """Greenhouse per-company API."""
    jobs = []
    for slug, platform in _load_companies():
        if platform != "greenhouse":
            continue
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        data = get_json(url)
        if not data:
            time.sleep(PER_COMPANY_DELAY)
            continue
        for item in data.get("jobs", []):
            location = item.get("location", {})
            loc_name = location.get("name", "") if isinstance(location, dict) else str(location)
            jobs.append({
                "company": slug.replace("-", " ").title(),
                "role": item.get("title", ""),
                "url": item.get("absolute_url", ""),
                "source": "Greenhouse",
                "posted_date": normalize_date(item.get("updated_at", "")),
                "salary": "",
                "location_tag": loc_name,
                "_description": item.get("content", ""),
            })
        time.sleep(PER_COMPANY_DELAY)
    return jobs


def fetch_lever() -> list[dict]:
    """Lever per-company API."""
    jobs = []
    for slug, platform in _load_companies():
        if platform != "lever":
            continue
        url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
        data = get_json(url)
        if not data or not isinstance(data, list):
            time.sleep(PER_COMPANY_DELAY)
            continue
        for item in data:
            categories = item.get("categories", {})
            loc = categories.get("location", "") if isinstance(categories, dict) else ""
            commitment = categories.get("commitment", "") if isinstance(categories, dict) else ""
            # Skip non-remote postings
            if commitment and "remote" not in commitment.lower() and loc and "remote" not in loc.lower():
                continue
            job_url = f"https://jobs.lever.co/{slug}/{item.get('id', '')}"
            desc_parts = [
                item.get("descriptionPlain", ""),
                " ".join(
                    s.get("content", "") if isinstance(s, dict) else ""
                    for s in item.get("lists", [])
                ),
            ]
            jobs.append({
                "company": item.get("company", slug.replace("-", " ").title()),
                "role": item.get("text", ""),
                "url": item.get("hostedUrl", job_url),
                "source": "Lever",
                "posted_date": normalize_date(item.get("createdAt")),
                "salary": "",
                "location_tag": loc,
                "_description": " ".join(desc_parts),
            })
        time.sleep(PER_COMPANY_DELAY)
    return jobs


def fetch_ashby() -> list[dict]:
    """Ashby per-company API."""
    jobs = []
    for slug, platform in _load_companies():
        if platform != "ashby":
            continue
        url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
        data = get_json(url)
        if not data:
            time.sleep(PER_COMPANY_DELAY)
            continue
        for item in data.get("jobPostings", []):
            loc = item.get("locationName", "")
            if item.get("isRemote"):
                loc = loc or "Remote"
            elif "remote" not in loc.lower():
                continue  # skip onsite
            jobs.append({
                "company": item.get("organizationName", slug.replace("-", " ").title()),
                "role": item.get("title", ""),
                "url": item.get("jobPostingUrl", ""),
                "source": "Ashby",
                "posted_date": normalize_date(item.get("publishedDate", "")),
                "salary": "",
                "location_tag": loc,
                "_description": item.get("descriptionPlain", ""),
            })
        time.sleep(PER_COMPANY_DELAY)
    return jobs

# ─────────────────────────────────────────────────────────────────────────────
# ALL SOURCES
# ─────────────────────────────────────────────────────────────────────────────

SOURCES = [
    ("Remotive",        fetch_remotive),
    ("RemoteOK",        fetch_remoteok),
    ("Himalayas",       fetch_himalayas),
    ("WeWorkRemotely",  fetch_weworkremotely),
    ("Jobicy",          fetch_jobicy),
    ("Arbeitnow",       fetch_arbeitnow),
    ("Greenhouse",      fetch_greenhouse),
    ("Lever",           fetch_lever),
    ("Ashby",           fetch_ashby),
]

# ─────────────────────────────────────────────────────────────────────────────
# CSV WRITER
# ─────────────────────────────────────────────────────────────────────────────

CSV_COLUMNS = [
    "company",
    "role",
    "url",
    "source",
    "posted_date",
    "scraped_date",
    "salary",
    "location_tag",
    "india_ok",
    "application_status",
    "notes",
]


def write_csv(jobs: list[dict], output_path: Path) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(jobs)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = LEADS_DIR / f"jobs_{today}.csv"

    # If we already ran today, load existing jobs so we can append only new ones
    existing_today = []
    if output_path.exists():
        with open(output_path, encoding="utf-8") as f:
            existing_today = list(csv.DictReader(f))
        print(f"📂 Found existing file for today with {len(existing_today)} jobs. Appending new ones only.\n")

    seen = load_seen()

    # Re-mark today's existing jobs as seen so we don't duplicate within the day
    for job in existing_today:
        mark_seen(job, seen)

    print("=" * 60)
    print("  Remote DE Job Scraper")
    print(f"  Run date : {today}")
    print(f"  Freshness: {FRESHNESS_DAYS} days")
    print("=" * 60)
    print()

    all_new_jobs = []
    total_fetched = 0
    total_dupes = 0
    total_filtered = 0

    for source_name, fetcher in SOURCES:
        print(f"[{source_name}]", end=" ", flush=True)
        try:
            raw_jobs = fetcher()
        except Exception as e:
            print(f"✗ Error: {e}")
            continue

        new_for_source = []
        for job in raw_jobs:
            total_fetched += 1

            # Role keyword filter
            if not passes_role_filter(job):
                total_filtered += 1
                continue

            # Exclude filter
            if not passes_exclude_filter(job):
                total_filtered += 1
                continue

            # Freshness filter
            if not is_fresh(job):
                total_filtered += 1
                continue

            # Deduplication
            if is_duplicate(job, seen):
                total_dupes += 1
                continue

            # Score india_ok
            score = india_ok_score(job)

            # Build output row
            row = {
                "company": job.get("company", "").strip(),
                "role": job.get("role", "").strip(),
                "url": job.get("url", "").strip(),
                "source": job.get("source", source_name),
                "posted_date": job.get("posted_date", ""),
                "scraped_date": today,
                "salary": job.get("salary", ""),
                "location_tag": job.get("location_tag", ""),
                "india_ok": score,
                "application_status": "not_applied",
                "notes": "",
            }

            mark_seen(job, seen)
            new_for_source.append(row)

        print(f"✓  {len(new_for_source)} new jobs")
        all_new_jobs.extend(new_for_source)

    # Sort by india_ok descending, then posted_date descending
    all_new_jobs.sort(
        key=lambda j: (-(j["india_ok"]), j.get("posted_date", "") or ""),
        reverse=False,
    )
    # Actually sort correctly: india_ok desc, posted_date desc
    all_new_jobs.sort(key=lambda j: j.get("posted_date", "") or "", reverse=True)
    all_new_jobs.sort(key=lambda j: j["india_ok"], reverse=True)

    # Combine with existing today's jobs (existing first, new appended)
    combined = existing_today + all_new_jobs

    # Write CSV
    write_csv(combined, output_path)

    # Persist seen store
    save_seen(seen)

    # Summary
    print()
    print("─" * 60)
    print(f"  Total fetched      : {total_fetched}")
    print(f"  Role-filtered out  : {total_filtered}")
    print(f"  Duplicates skipped : {total_dupes}")
    print(f"  New leads found    : {len(all_new_jobs)}")
    print(f"  Saved to           : {output_path}")
    print("─" * 60)

    if len(all_new_jobs) == 0:
        print("\n✅ No new jobs this run — you're fully up to date!")
    else:
        # Quick stats
        high_conf = sum(1 for j in all_new_jobs if j["india_ok"] == 3)
        med_conf  = sum(1 for j in all_new_jobs if j["india_ok"] == 2)
        low_conf  = sum(1 for j in all_new_jobs if j["india_ok"] <= 1)
        print(f"\n  india_ok=3 (confirmed) : {high_conf}")
        print(f"  india_ok=2 (likely)    : {med_conf}")
        print(f"  india_ok=1 (unclear)   : {low_conf}")
        print(f"\n  🎯 Tip: Filter india_ok >= 2 for best leads ({high_conf + med_conf} jobs)")
    print()


if __name__ == "__main__":
    main()
