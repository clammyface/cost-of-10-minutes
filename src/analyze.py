"""
Turn the review corpus into the evidence base for docs/02 - docs/05.

Input : data/processed/reviews.csv
Output: data/processed/reviews_tagged.csv     one row per review + theme flags
        data/processed/theme_frequency.csv    theme x app, share of negative reviews
        data/processed/theme_trend.csv        theme x month, for the trend chart
        data/processed/theme_severity.csv     frequency x severity x business impact
        data/processed/theme_terms.csv        top TF-IDF terms per theme (validation)
        data/processed/validation_sample.csv  100 random reviews for hand-labelling

METHOD
------
Themes are assigned by curated keyword rules, not by unsupervised clustering.
That is a deliberate choice: k-means over TF-IDF on short review text produced
clusters dominated by generic sentiment words ("good", "worst", "app") that do not
map onto actionable product problems. Keyword rules are auditable, reproducible,
and map 1:1 onto things a product team can own.

TF-IDF is still used, but for *validation*: it surfaces the top distinguishing terms
per theme so a human can check the rule set is catching the right language, and it
surfaces high-frequency terms that no rule matched (candidate missing themes).

A review can carry multiple themes. Untagged reviews are counted and reported --
a high untagged rate would mean the taxonomy is incomplete.

SEVERITY
--------
Frequency alone is a bad prioritisation signal: "app is slow" is common but mild,
"my refund never came" is rarer but a churn event. Each theme therefore carries a
hand-assigned severity (1-5) and business-impact weight (1-5), documented in
docs/05 with the reasoning. Priority score = normalised frequency x severity x impact.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

# cp1252 consoles choke on the rupee sign and Indic script in review text.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

# theme -> (regex, severity 1-5, business impact 1-5, label)
# Severity  = how bad it is for the user when it happens (5 = lost money / lost trust)
# Impact    = how directly it drives churn / cost / repeat-rate for the business
THEMES: dict[str, tuple[str, int, int, str]] = {
    "delivery_delay": (
        r"\b(?:late|delay(?:ed|s)?|slow(?:er)? deliver|took (?:an? )?hour|hours? late|"
        r"not on time|beyond .{0,10}minutes?|10 ?min(?:ute)?s? (?:is|was)? ?(?:a )?"
        r"(?:lie|joke|fake)|eta|time increas|still (?:not|didn'?t) (?:arriv|deliver|come)|"
        r"deliver\w* (?:is |are |was |very )?(?:slow|late)|no longer (?:fast|quick)|"
        r"takes? (?:so |too )?(?:much |long)|waiting (?:for )?(?:hours?|long))\b",
        4, 5, "Delivery is late / ETA not met",
    ),
    "refund_issues": (
        r"\b(?:refund|money (?:not|never) (?:return|credit|receiv)|amount deduct|"
        r"deducted|not credited|cashback|money stuck|charged twice|double charg|"
        r"money (?:back|lost)|no refund)\b",
        5, 5, "Refunds delayed, denied, or untraceable",
    ),
    "item_quality": (
        r"\b(?:rotten|stale|spoil(?:ed|t)|expir(?:ed|y)|damag(?:ed|e)|"
        r"smell(?:s|ed|ing)?(?: bad)?|fungus|mould|mold|worm|insect|not fresh|"
        r"leak(?:ed|ing|age)|melted|crushed|(?:bad|poor|worst|low|cheap|third class) quality|"
        r"quality (?:is |has |was )?(?:bad|poor|degrad|down|deteriorat|worst|drop)|"
        r"quality issue|compromis\w* (?:on |with )?quality)\b",
        5, 4, "Product arrives spoiled, expired, or damaged",
    ),
    "missing_wrong_items": (
        r"\b(?:missing|not deliver(?:ed)?|wrong (?:item|product|order)|"
        r"different (?:item|product)|item(?:s)? (?:were |was )?(?:not|never)|"
        r"half (?:the )?order|incomplete order|"
        r"didn'?t (?:receive|get) (?:the |my )?(?:item|product|order)|"
        r"less (?:item|quantity|product)|short (?:deliver|quantity))\b",
        5, 5, "Items missing from order or wrong item sent",
    ),
    "pricing_charges": (
        # Deliberately broad on "charge(s)"/"fee": in a negative review of a delivery
        # app this is essentially always a pricing complaint, and the untagged-term
        # audit showed bare "charges" was the single largest miss.
        r"\b(?:expensive|costl(?:y|ier)|overpric|price(?:s)? (?:is |are |has |have )?"
        r"(?:high|increas|hike|gone up|too much)|high(?:er)? (?:price|charge|rate|mrp)|"
        r"surge|handling|delivery (?:fee|charge)|rain fee|small cart|hidden charge|"
        r"extra (?:charge|fee|money)|charges?\b|\bfees?\b|mrp|loot|"
        r"cheat(?:ing)? (?:on )?price|discount(?:s)? (?:are |is )?(?:less|gone|stopped|reduc)|"
        r"no (?:more )?(?:offers?|discount)|offers? (?:are |is )?(?:gone|stopped|reduc|less)|"
        r"(?:better|more|good) (?:offers?|discount|price)|cheaper (?:on|in|at)|"
        r"(?:offers?|discount|price)(?:s)? than\b)\b",
        3, 4, "Prices and added fees feel unfair or opaque",
    ),
    "payment_issues": (
        r"\b(?:payment (?:fail|issue|problem|not|error|stuck|declin|option|method)|"
        r"transaction fail|\bupi\b|wallet|"
        r"money (?:is )?(?:stuck|debited|deducted) (?:but|and)|"
        r"paid but|amount (?:debited|deducted) but|pay ?later|"
        r"pay(?:ing|s)? twice|charged twice|"
        r"cod (?:not|option|unavailable)|cash on delivery (?:not|option))\b",
        5, 5, "Payment fails or money is debited without an order",
    ),
    "returns_replacement": (
        r"\b(?:return(?:s|ed|ing)? (?:policy|request|option|not|is|was|the)|"
        r"no return|replace(?:ment)?|exchang(?:e|ed)|"
        r"won'?t (?:take|accept) (?:it |the )?back|take (?:it )?back)\b",
        4, 4, "Returns and replacements are hard or refused",
    ),
    "app_bugs": (
        r"\b(?:crash(?:es|ed|ing)?|bug(?:s|gy)?|not working|doesn'?t work|hang(?:s|ing)|"
        r"stuck|freez(?:e|es|ing)|error|glitch|login (?:issue|problem|fail)|"
        r"otp (?:not|issue)|app (?:is |very |so )?slow|force clos|"
        r"(?:app|update) (?:is )?(?:worst|useless|broken))\b",
        3, 3, "App crashes, errors, or fails to load",
    ),
    "customer_support": (
        # "service" alone is excluded on purpose -- it collides with "delivery service
        # is slow", which is a delay complaint, not a support one.
        r"\b(?:customer (?:support|care|service|executive)|support team|chat ?bot|"
        r"no (?:response|reply|resolution)|no one (?:respond|repli|answer|help)|"
        r"helpline|complaint|raise(?:d)? (?:a )?ticket|unresponsive|no help|"
        r"support (?:is |was )?(?:bad|poor|worst|useless|pathetic|zero)|"
        r"cannot (?:reach|contact)|can'?t (?:reach|contact) (?:anyone|them|support)|"
        r"no human|no way to (?:resolve|reach|contact)|(?:issue|problem) (?:not |un)resolv|"
        r"nobody (?:responds?|answers?|helps?))\b",
        4, 4, "Support is unreachable or unhelpful",
    ),
    "delivery_partner": (
        r"\b(?:delivery (?:boy|man|partner|agent|guy|person)|rider|rude|misbehav|"
        r"behaviour|behavior|abus(?:e|ive)|argu(?:e|ing)|shout(?:ed|ing)?|"
        r"fake deliver|marked (?:as )?deliver|without (?:calling|informing))\b",
        4, 3, "Delivery partner behaviour or fake delivery marking",
    ),
    "stock_availability": (
        r"\b(?:out of stock|not available|unavailable|no stock|sold out|"
        r"never (?:in )?stock|item(?:s)? (?:are |is )?(?:not )?availab|"
        r"limited (?:stock|option|variety)|less (?:variety|option))\b",
        3, 4, "Wanted items are unavailable",
    ),
    "cancellation": (
        r"\b(?:cancel(?:led|ling|lation)?|auto ?cancel|order (?:was )?cancel|"
        r"cancelled (?:my|the) order (?:without|automatically))\b",
        4, 4, "Orders cancelled unexpectedly or cancellation blocked",
    ),
    "membership": (
        r"\b(?:subscription|membership|bistro pass|super ?saver|prime|"
        r"auto ?renew|cancel (?:my )?(?:subscription|membership))\b",
        3, 3, "Membership / subscription friction",
    ),
    "packaging": (
        r"\b(?:packag(?:e|ing)|bag (?:was |is )?(?:torn|broken)|poorly packed|"
        r"no (?:proper )?packing|plastic waste|not (?:separately |properly )?packed|"
        r"dumped|soggy)\b",
        2, 2, "Packaging quality",
    ),
}

STOP_EXTRA = {
    "app", "blinkit", "zepto", "swiggy", "instamart", "bigbasket", "order", "orders",
    "ordered", "please", "good", "nice", "bad", "worst", "best", "very", "just",
    "like", "dont", "don", "im", "ive", "get", "got", "use", "using", "one", "also",
}

STOP_BASE = {
    "the", "and", "for", "are", "but", "not", "you", "your", "was", "were", "this",
    "that", "with", "have", "has", "had", "they", "them", "their", "there", "then",
    "from", "will", "would", "can", "could", "should", "what", "when", "which", "who",
    "why", "how", "all", "any", "been", "being", "its", "it's", "our", "out", "about",
    "after", "again", "because", "before", "did", "does", "doing", "here", "into",
    "more", "most", "only", "other", "over", "same", "some", "such", "than", "too",
    "under", "until", "very", "each", "few", "him", "his", "her", "hers", "she",
    "myself", "yourself", "itself", "these", "those", "having", "does", "doesn",
    "even", "still", "want", "give", "take", "make", "made", "much", "many", "back",
    "well", "know", "need", "time", "times", "day", "days", "now", "always", "never",
    "every", "per", "due", "via", "yet", "may", "must",
}
STOPWORDS = STOP_BASE | STOP_EXTRA

TOKEN = re.compile(r"[a-z]{3,}")


def tokenize(text: str) -> list[str]:
    """Unigrams + bigrams, stopwords stripped. Bigrams keep phrases like 'handling charge'."""
    words = [w for w in TOKEN.findall(text.lower()) if w not in STOPWORDS]
    grams = list(words)
    grams += [f"{a} {b}" for a, b in zip(words, words[1:])]
    return grams


def top_terms(docs: list[str], mask: list[bool], idf: dict[str, float], k: int = 12):
    """Mean TF-IDF of each term across the masked subset, highest first.

    Implemented directly rather than via scikit-learn: scipy's compiled extensions are
    blocked by an Application Control policy on this machine, and a 40k-row corpus does
    not need a sparse-matrix library for what is a term-ranking sanity check.
    """
    totals: Counter[str] = Counter()
    n = 0
    for doc, keep in zip(docs, mask):
        if not keep:
            continue
        n += 1
        counts = Counter(tokenize(doc))
        if not counts:
            continue
        length = sum(counts.values())
        for term, c in counts.items():
            if term in idf:
                totals[term] += (c / length) * idf[term]
    if not n:
        return []
    return [(t, v / n) for t, v in totals.most_common(k)]


def build_idf(docs: list[str], min_df: int = 5) -> dict[str, float]:
    df_counts: Counter[str] = Counter()
    for doc in docs:
        df_counts.update(set(tokenize(doc)))
    n = len(docs)
    return {
        t: math.log(n / (1 + c)) + 1.0
        for t, c in df_counts.items()
        if c >= min_df
    }


def tag(df: pd.DataFrame) -> pd.DataFrame:
    for theme, (pattern, *_rest) in THEMES.items():
        rx = re.compile(pattern, re.IGNORECASE)
        df[f"t_{theme}"] = df["text"].str.contains(rx, na=False)
    cols = [f"t_{t}" for t in THEMES]
    df["theme_count"] = df[cols].sum(axis=1)
    df["untagged"] = df["theme_count"] == 0
    df["themes"] = df[cols].apply(
        lambda r: "|".join(c[2:] for c in cols if r[c]), axis=1
    )
    return df


def main() -> int:
    src = PROC / "reviews.csv"
    if not src.exists():
        raise SystemExit("data/processed/reviews.csv missing. Run src/clean.py first.")

    print("[1/6] loading + tagging")
    df = pd.read_csv(src, parse_dates=["reviewed_at"])
    df["text"] = df["text"].fillna("").astype(str)
    df = tag(df)
    df.to_csv(PROC / "reviews_tagged.csv", index=False, encoding="utf-8")

    neg = df[df["rating"] <= 3].copy()
    print(f"    {len(df):,} reviews | {len(neg):,} negative | "
          f"untagged among negative: {neg['untagged'].mean():.1%}")

    print("[2/6] theme frequency (within negative reviews, per app)")
    rows = []
    for app_name, g in neg.groupby("app"):
        for theme, (_p, sev, imp, label) in THEMES.items():
            hits = int(g[f"t_{theme}"].sum())
            rows.append({
                "app": app_name,
                "theme": theme,
                "label": label,
                "negative_reviews": len(g),
                "hits": hits,
                "share_of_negative": round(hits / len(g), 4) if len(g) else 0.0,
                "severity": sev,
                "business_impact": imp,
            })
    freq = pd.DataFrame(rows).sort_values(["app", "share_of_negative"], ascending=[True, False])
    freq.to_csv(PROC / "theme_frequency.csv", index=False, encoding="utf-8")

    print("[3/6] severity-weighted priority (focal app)")
    focal = freq[freq["app"] == "blinkit"].copy()
    if len(focal):
        top = focal["share_of_negative"].max() or 1.0
        focal["freq_norm"] = focal["share_of_negative"] / top
        focal["priority_score"] = (
            focal["freq_norm"] * focal["severity"] * focal["business_impact"]
        ).round(2)
        focal = focal.sort_values("priority_score", ascending=False)
        focal.to_csv(PROC / "theme_severity.csv", index=False, encoding="utf-8")
        for _, r in focal.head(6).iterrows():
            print(f"    {r['priority_score']:6.2f}  {r['theme']:22} "
                  f"{r['share_of_negative']:6.1%} of negative  sev={r['severity']} imp={r['business_impact']}")

    print("[4/6] theme trend over time")
    # Quarterly, not monthly. Monthly buckets in the sparse early years (a few dozen
    # reviews) swing between 0% and 55% purely on sample noise, which reads as a trend
    # that isn't there. Quarters with fewer than MIN_PERIOD negative reviews are dropped
    # rather than plotted at low confidence.
    MIN_PERIOD = 40
    trend_rows = []
    neg_q = neg[neg["reviewed_at"].notna()].copy()
    neg_q["period"] = neg_q["reviewed_at"].dt.to_period("Q").astype(str)
    dropped = 0
    for (app_name, period), g in neg_q.groupby(["app", "period"]):
        if len(g) < MIN_PERIOD:
            dropped += 1
            continue
        rec = {"app": app_name, "period": period, "negative_reviews": len(g)}
        for theme in THEMES:
            rec[theme] = round(float(g[f"t_{theme}"].mean()), 4)
        trend_rows.append(rec)
    trend = pd.DataFrame(trend_rows).sort_values(["app", "period"])
    trend.to_csv(PROC / "theme_trend.csv", index=False, encoding="utf-8")
    kept = len(trend[trend["app"] == "blinkit"]) if len(trend) else 0
    print(f"    {kept} blinkit quarters kept, {dropped} periods dropped (<{MIN_PERIOD} negative reviews)")

    print("[5/6] TF-IDF validation terms")
    term_rows = []
    focal_neg = neg[neg["app"] == "blinkit"]
    if len(focal_neg) > 50:
        docs = focal_neg["text"].tolist()
        idf = build_idf(docs)
        print(f"    vocabulary: {len(idf):,} terms (min_df=5)")

        for theme in THEMES:
            mask = focal_neg[f"t_{theme}"].tolist()
            if sum(mask) < 10:
                continue
            for term, score in top_terms(docs, mask, idf, k=12):
                term_rows.append({"theme": theme, "term": term, "tfidf": round(score, 5)})

        # Terms concentrated in reviews that NO rule caught -- these are the candidate
        # missing themes. If something actionable shows up here, the taxonomy has a hole.
        un = focal_neg["untagged"].tolist()
        if sum(un) >= 10:
            for term, score in top_terms(docs, un, idf, k=25):
                term_rows.append({"theme": "__UNTAGGED__", "term": term, "tfidf": round(score, 5)})
    pd.DataFrame(term_rows).to_csv(PROC / "theme_terms.csv", index=False, encoding="utf-8")

    print("[6/6] validation sample (100 reviews for hand-labelling)")
    pool = df[(df["app"] == "blinkit") & (df["word_len"] >= 6)]
    sample = pool.sample(n=min(100, len(pool)), random_state=42)
    sample[["review_id", "rating", "reviewed_at", "text", "themes", "untagged"]].assign(
        manual_label=""
    ).to_csv(PROC / "validation_sample.csv", index=False, encoding="utf-8")

    summary = {
        "total_reviews": len(df),
        "negative_reviews": len(neg),
        "untagged_share_of_negative": round(float(neg["untagged"].mean()), 4),
        "mean_themes_per_negative": round(float(neg["theme_count"].mean()), 2),
        "top_themes_blinkit": focal.head(6)[["theme", "share_of_negative", "priority_score"]].to_dict("records")
        if len(focal) else [],
    }
    (PROC / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n  wrote 7 files to data/processed/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
