"""
Normalise the raw Play Store pulls into one tidy corpus.

Input : data/raw/play_*.json
Output: data/processed/reviews.csv
        data/processed/corpus_stats.json
        data/processed/sampling_note.md   <- the caveat that must travel with the data

Cleaning decisions, all deliberate and all disclosed in docs/02:
  * dedupe on reviewId (the same review is reachable from both sort orders)
  * drop reviews under MIN_CHARS -- "good", "nice", "worst" carry no analysable signal
  * drop reviews that are majority non-Latin script (Devanagari etc). We keep
    ROMANISED Hindi/Hinglish, which is most of the Indian corpus and is readable
    by the keyword taxonomy. This biases the corpus toward English-literate users
    and that limitation is stated in docs/02.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

# Review text carries the rupee sign and Indic punctuation; the default Windows
# console codepage (cp1252) raises UnicodeEncodeError on both.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"

MIN_CHARS = 15
LATIN = re.compile(r"[A-Za-z]")
NON_LATIN_SCRIPT = re.compile(r"[ऀ-ॿঀ-৿஀-௿ఀ-౿ಀ-೿ഀ-ൿ]")


def latin_ratio(text: str) -> float:
    """Share of alphabetic characters that are Latin. 1.0 = pure Latin script."""
    latin = len(LATIN.findall(text))
    other = len(NON_LATIN_SCRIPT.findall(text))
    total = latin + other
    return latin / total if total else 0.0


def load_raw() -> pd.DataFrame:
    frames = []
    for path in sorted(RAW.glob("play_*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if rows:
            frames.append(pd.DataFrame(rows))
        print(f"  loaded {path.name}: {len(rows):,}")
    if not frames:
        raise SystemExit("No raw review files found. Run src/scrape_reviews.py first.")
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    PROC.mkdir(parents=True, exist_ok=True)

    print("[1/4] loading raw")
    df = load_raw()
    raw_n = len(df)

    print("[2/4] normalising")
    df = df.rename(
        columns={
            "reviewId": "review_id",
            "content": "text",
            "score": "rating",
            "thumbsUpCount": "thumbs_up",
            "reviewCreatedVersion": "app_version",
            "at": "reviewed_at",
            "replyContent": "developer_reply",
        }
    )
    keep = [
        "review_id", "app", "rating", "text", "reviewed_at",
        "app_version", "thumbs_up", "developer_reply", "sort_mode",
    ]
    df = df[[c for c in keep if c in df.columns]].copy()

    df["text"] = df["text"].fillna("").astype(str).str.strip()
    df["reviewed_at"] = pd.to_datetime(df["reviewed_at"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Int64")
    df["thumbs_up"] = pd.to_numeric(df["thumbs_up"], errors="coerce").fillna(0).astype(int)
    df["has_dev_reply"] = df.get("developer_reply").notna() if "developer_reply" in df else False

    print("[3/4] filtering")
    steps = {"raw_rows": raw_n}

    df = df.drop_duplicates(subset=["review_id"])
    steps["after_dedupe"] = len(df)

    df = df[df["reviewed_at"].notna() & df["rating"].notna()]
    steps["after_valid_date_rating"] = len(df)

    df["char_len"] = df["text"].str.len()
    df = df[df["char_len"] >= MIN_CHARS]
    steps["after_min_length"] = len(df)

    df["latin_ratio"] = df["text"].map(latin_ratio)
    df = df[df["latin_ratio"] >= 0.5]
    steps["after_script_filter"] = len(df)

    df["year"] = df["reviewed_at"].dt.year
    df["year_month"] = df["reviewed_at"].dt.to_period("M").astype(str)
    df["word_len"] = df["text"].str.split().str.len()
    df["is_negative"] = df["rating"] <= 3

    df = df.sort_values(["app", "reviewed_at"]).reset_index(drop=True)
    df = df.drop(columns=["latin_ratio"])

    out = PROC / "reviews.csv"
    df.to_csv(out, index=False, encoding="utf-8")

    print("[4/4] writing stats")
    focal = df[df["app"] == "blinkit"]
    stats = {
        "filter_funnel": steps,
        "final_rows": len(df),
        # json.dumps rejects numpy.int64 dict keys, so cast every key explicitly.
        "by_app": {str(k): int(v) for k, v in df.groupby("app").size().items()},
        "by_app_rating": {
            str(a): {str(int(r)): int(n) for r, n in g.groupby("rating").size().items()}
            for a, g in df.groupby("app")
        },
        "by_year": {str(int(k)): int(v) for k, v in df.groupby("year").size().items()},
        "date_range": {
            "min": str(df["reviewed_at"].min()),
            "max": str(df["reviewed_at"].max()),
        },
        "blinkit_rows": len(focal),
        "blinkit_negative_rows": int(focal["is_negative"].sum()),
        "median_words": float(df["word_len"].median()),
    }
    (PROC / "corpus_stats.json").write_text(json.dumps(stats, indent=2, default=str), encoding="utf-8")

    (PROC / "sampling_note.md").write_text(
        "# Sampling note — read before quoting any percentage\n\n"
        "This corpus is **not a random sample** of Play Store reviews and its rating\n"
        "distribution must not be read as the app's true rating distribution.\n\n"
        "Reviews were pulled with an equal quota per star rating (1-5) across two sort\n"
        "orders (newest, most-relevant). 1-3 star reviews are therefore massively\n"
        "over-represented relative to reality — Blinkit's real Play Store average is\n"
        "**4.58/5** across ~9.0M ratings, which is the number to cite for overall\n"
        "satisfaction.\n\n"
        "That over-sampling is deliberate: the complaint taxonomy needs enough negative\n"
        "text to cluster on. It means this corpus is valid for:\n\n"
        "* **relative** complaint frequency — which problems dominate *within* negative reviews\n"
        "* complaint themes, phrasing, and severity\n"
        "* cross-app comparison, since every app was sampled the same way\n\n"
        "It is **not** valid for: overall satisfaction rates, absolute share of users\n"
        "affected, or any claim of the form \"X% of Blinkit users experience Y\".\n\n"
        "Where absolute reach is needed, it is estimated by combining the *relative*\n"
        "theme share here with published totals (order volume, MTU) from the Eternal\n"
        "shareholder letters, and labelled as an estimate.\n\n"
        "## Excluded sources\n\n"
        "* **Apple App Store** — the public customerreviews RSS feed returns HTTP 200 with\n"
        "  zero entries for all apps/regions tested (checked 2026-08-25). Apple has moved\n"
        "  review access behind the authenticated App Store Connect API.\n"
        "* **Reddit** — `.json` endpoints return HTTP 403 to unauthenticated clients and\n"
        "  old.reddit.com serves HTML. Requires OAuth credentials.\n\n"
        "The corpus is therefore Android-only, which skews away from iOS users (who in\n"
        "India skew higher-income). Stated as a limitation in docs/02.\n",
        encoding="utf-8",
    )

    print(f"\n  {raw_n:,} raw -> {len(df):,} clean")
    for k, v in steps.items():
        print(f"    {k:28} {v:,}")
    print(f"\n  by app: {stats['by_app']}")
    print(f"  blinkit: {len(focal):,} ({stats['blinkit_negative_rows']:,} negative)")
    print(f"  dates:   {stats['date_range']['min'][:10]} .. {stats['date_range']['max'][:10]}")
    print(f"\n  -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
