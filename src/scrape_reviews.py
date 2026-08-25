"""
Scrape public user reviews for Indian quick-commerce apps.

Source is the Google Play Store. Because Blinkit alone has ~1.2M reviews, we do NOT
pull everything -- we pull a *stratified* sample: an equal quota per star rating,
across two sort orders. That deliberately over-samples 1-3 star reviews relative to
their true share, because the complaint taxonomy in docs/02 needs enough negative
text to cluster on.

Two sort orders are used on purpose:
  NEWEST         -- recent reviews, so the trend analysis has a dense recent window.
  MOST_RELEVANT  -- Play's own high-signal ranking, which reaches further back in
                    time and surfaces long, detailed reviews that NEWEST misses.

This is a sampling choice, not a random sample, and every downstream document that
quotes a proportion has to say so. `data/processed/sampling_note.md` is written out
by clean.py to keep that caveat attached to the data.

SOURCES THAT DID NOT WORK (checked 2026-08-25, documented so nobody retries them):
  Apple App Store -- the public customerreviews RSS feed still returns HTTP 200 but
    with zero review entries for every app and region tested. Apple has moved review
    access behind the authenticated App Store Connect API. Not usable without a
    developer account for the app in question, which we do not have.
  Reddit -- www.reddit.com/*.json now returns HTTP 403 to unauthenticated clients,
    and old.reddit.com serves an HTML interstitial instead of JSON. Reddit requires
    OAuth app credentials. Out of scope for the time budget.
Both omissions are disclosed in README.md and docs/02_user_research.md rather than
being papered over.

Usage:
    python src/scrape_reviews.py            # full run
    python src/scrape_reviews.py --quick    # small run, for testing the pipeline
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from google_play_scraper import Sort, app, reviews

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

# Verified live via google_play_scraper.app() -- see docs/02 for retrieval date.
APPS = {
    "blinkit": "com.grofers.customerapp",
    "zepto": "com.zeptoconsumerapp",
    "instamart": "in.swiggy.android",
    "bigbasket": "com.bigbasket.mobileapp",
}

FOCAL = "blinkit"

SORTS = {"newest": Sort.NEWEST, "relevant": Sort.MOST_RELEVANT}

# Per-star, per-sort quota. Blinkit gets the deep pull; competitors only need enough
# to support the comparison matrix and the opportunity map.
QUOTA_FOCAL = 3000
QUOTA_OTHER = 1000
PAGE = 200
SLEEP = 0.35


def _write(name: str, payload) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / name
    path.write_text(json.dumps(payload, indent=1, default=str, ensure_ascii=False), encoding="utf-8")
    return path


def scrape_play(slug: str, package: str, quota: int) -> list[dict]:
    """Pull `quota` reviews per star rating (1-5), for each sort order."""
    collected: list[dict] = []
    for sort_name, sort_mode in SORTS.items():
        per_sort = 0
        for star in range(1, 6):
            token = None
            got = 0
            while got < quota:
                want = min(PAGE, quota - got)
                try:
                    batch, token = reviews(
                        package,
                        lang="en",
                        country="in",
                        sort=sort_mode,
                        count=want,
                        filter_score_with=star,
                        continuation_token=token,
                    )
                except Exception as exc:  # transient network / throttle
                    print(f"    ! {slug} {sort_name} {star}*: {type(exc).__name__}: {exc}; backing off")
                    time.sleep(4)
                    break

                if not batch:
                    break

                for r in batch:
                    r["app"] = slug
                    r["source"] = "google_play"
                    r["sort_mode"] = sort_name
                    r["star_bucket"] = star
                collected.extend(batch)
                got += len(batch)

                if token is None:
                    break
                time.sleep(SLEEP)

            per_sort += got
        print(f"    {slug} [{sort_name}]: {per_sort}")

    return collected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="tiny run to smoke-test the pipeline")
    args = parser.parse_args()

    global QUOTA_FOCAL, QUOTA_OTHER
    if args.quick:
        QUOTA_FOCAL, QUOTA_OTHER = 60, 40

    print("[1/2] app metadata")
    meta = {}
    for slug, package in APPS.items():
        try:
            d = app(package, lang="en", country="in")
            meta[slug] = {
                "package": package,
                "title": d["title"],
                "score": d["score"],
                "ratings": d["ratings"],
                "reviews": d["reviews"],
                # True 1-5 star distribution across ALL ratings. Our scraped corpus is
                # stratified and cannot report this -- any real distribution claim uses
                # this field, not the corpus.
                "histogram": d.get("histogram"),
                "installs": d["installs"],
                "released": d.get("released"),
                "updated": d.get("updated"),
            }
            print(f"    {slug}: {d['title']} | {d['score']:.2f} | {d['ratings']:,} ratings")
        except Exception as exc:
            print(f"    ! {slug}: {type(exc).__name__}: {exc}")
    _write("app_metadata.json", meta)

    print("[2/2] google play reviews (stratified by star x sort order)")
    total = 0
    for slug, package in APPS.items():
        quota = QUOTA_FOCAL if slug == FOCAL else QUOTA_OTHER
        rows = scrape_play(slug, package, quota)
        _write(f"play_{slug}.json", rows)
        total += len(rows)
        print(f"    -> play_{slug}.json: {len(rows)} rows (pre-dedupe)")

    print(f"\ndone. {total:,} raw rows in data/raw/. Run clean.py next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
