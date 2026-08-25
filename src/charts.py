"""
Render the figures used in README.md and docs/.

Every chart renders twice -- light and dark -- so the GitHub README stays legible in
both themes via <picture><source media="(prefers-color-scheme: dark)">.

Palette is the validated categorical set (slots 1-4), checked with the dataviz
validator in both modes:
    light #2a78d6 #eb6834 #1baf7a #eda100  -> all checks pass, contrast WARN
    dark  #3987e5 #d95926 #199e70 #c98500  -> all checks pass
The light-mode contrast warning obligates *visible direct labels* on every mark
(the "relief rule"), which is why each bar carries its own value label.

Chart forms follow the data's job:
    theme frequency / priority  -> horizontal bar (magnitude, ranked, long labels)
    cross-app comparison        -> grouped horizontal bar (identity x magnitude)
    theme trend                 -> line (change over time), direct-labelled, capped at 4
    true rating distribution    -> horizontal bar from Play metadata, NOT the corpus
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
OUT = ROOT / "charts"

THEMES_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
THEMES_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500"]

MODES = {
    "light": {
        "surface": "#fcfcfb", "text": "#0b0b0b", "text2": "#52514e",
        "muted": "#8a8880", "grid": "#e6e5e0", "series": THEMES_LIGHT,
    },
    "dark": {
        "surface": "#1a1a19", "text": "#ffffff", "text2": "#c3c2b7",
        "muted": "#8a8880", "grid": "#333331", "series": THEMES_DARK,
    },
}

APP_LABEL = {"blinkit": "Blinkit", "zepto": "Zepto", "instamart": "Instamart", "bigbasket": "bigbasket"}


def style(mode: str):
    m = MODES[mode]
    plt.rcParams.update({
        "figure.facecolor": m["surface"], "axes.facecolor": m["surface"],
        "savefig.facecolor": m["surface"], "text.color": m["text"],
        "axes.labelcolor": m["text2"], "xtick.color": m["text2"], "ytick.color": m["text2"],
        "axes.edgecolor": m["grid"], "grid.color": m["grid"],
        "font.size": 10.5, "axes.titlesize": 13, "axes.titleweight": "bold",
        "figure.dpi": 160, "savefig.bbox": "tight",
    })
    return m


def finish(fig, ax, m, title, subtitle=None, xlabel=None):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(m["grid"])
    ax.tick_params(length=0)
    head = title if not subtitle else f"{title}\n"
    ax.set_title(head, loc="left", pad=14 if subtitle else 10, color=m["text"])
    if subtitle:
        ax.text(0, 1.015, subtitle, transform=ax.transAxes, fontsize=9.5,
                color=m["text2"], va="bottom")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9.5, labelpad=8)
    fig.tight_layout()


def save(fig, name, mode):
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = "" if mode == "light" else "-dark"
    path = OUT / f"{name}{suffix}.png"
    fig.savefig(path)
    plt.close(fig)
    return path


# ---------------------------------------------------------------- charts

def chart_theme_frequency(mode: str):
    m = style(mode)
    freq = pd.read_csv(PROC / "theme_frequency.csv")
    d = freq[freq["app"] == "blinkit"].sort_values("share_of_negative").tail(10)
    if d.empty:
        return None

    fig, ax = plt.subplots(figsize=(9, 5.4))
    y = range(len(d))
    ax.barh(y, d["share_of_negative"] * 100, height=0.62, color=m["series"][0], zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(d["label"], fontsize=10)
    ax.xaxis.grid(True, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    for i, v in zip(y, d["share_of_negative"] * 100):
        ax.text(v + 0.6, i, f"{v:.1f}%", va="center", fontsize=9.5,
                color=m["text2"], fontweight="medium")
    ax.set_xlim(0, (d["share_of_negative"].max() * 100) * 1.16)

    finish(fig, ax, m, "What Blinkit users complain about",
           f"Share of {int(d['negative_reviews'].iloc[0]):,} negative reviews (1-3★) mentioning each theme · reviews can carry more than one",
           "% of negative reviews")
    return save(fig, "01-complaint-themes", mode)


def chart_priority(mode: str):
    m = style(mode)
    path = PROC / "theme_severity.csv"
    if not path.exists():
        return None
    d = pd.read_csv(path).sort_values("priority_score").tail(10)

    fig, ax = plt.subplots(figsize=(9, 5.4))
    y = range(len(d))
    ax.barh(y, d["priority_score"], height=0.62, color=m["series"][1], zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(d["label"], fontsize=10)
    ax.xaxis.grid(True, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    for i, (v, sev, imp) in zip(y, d[["priority_score", "severity", "business_impact"]].values):
        ax.text(v + max(d["priority_score"]) * 0.015, i, f"{v:.1f}   sev {int(sev)} · impact {int(imp)}",
                va="center", fontsize=9, color=m["text2"])
    ax.set_xlim(0, d["priority_score"].max() * 1.34)

    finish(fig, ax, m, "Which complaint to actually solve",
           "Priority = normalised frequency × severity × business impact · frequency alone over-rates mild, common gripes",
           "priority score")
    return save(fig, "02-problem-priority", mode)


def chart_by_app(mode: str):
    m = style(mode)
    freq = pd.read_csv(PROC / "theme_frequency.csv")
    top = (freq[freq["app"] == "blinkit"]
           .sort_values("share_of_negative", ascending=False)["theme"].head(5).tolist())
    apps = [a for a in ["blinkit", "zepto", "instamart", "bigbasket"] if a in set(freq["app"])]
    d = freq[freq["theme"].isin(top)]
    if d.empty:
        return None

    labels = {t: freq[freq["theme"] == t]["label"].iloc[0] for t in top}
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    n = len(apps)
    height = 0.72 / n

    for k, app_name in enumerate(apps):
        vals, ys = [], []
        for j, theme in enumerate(top[::-1]):
            row = d[(d["app"] == app_name) & (d["theme"] == theme)]
            vals.append(float(row["share_of_negative"].iloc[0]) * 100 if len(row) else 0.0)
            ys.append(j + (k - (n - 1) / 2) * height)
        # 2px surface gap between adjacent fills
        ax.barh(ys, vals, height=height * 0.88, color=m["series"][k],
                label=APP_LABEL[app_name], zorder=3, edgecolor=m["surface"], linewidth=1.0)
        for yv, v in zip(ys, vals):
            if v > 0:
                ax.text(v + 0.5, yv, f"{v:.0f}", va="center", fontsize=8,
                        color=m["text2"])

    ax.set_yticks(range(len(top)))
    ax.set_yticklabels([labels[t] for t in top[::-1]], fontsize=10)
    ax.xaxis.grid(True, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, d["share_of_negative"].max() * 100 * 1.16)
    leg = ax.legend(frameon=False, ncol=n, loc="lower right",
                    bbox_to_anchor=(1.0, 1.005), fontsize=9.5)
    for t in leg.get_texts():
        t.set_color(m["text2"])

    finish(fig, ax, m, "The same complaints, across every quick-commerce app",
           "Share of each app's negative reviews · all four sampled identically, so columns are comparable",
           "% of negative reviews")
    return save(fig, "03-theme-by-app", mode)


def chart_trend(mode: str):
    m = style(mode)
    path = PROC / "theme_trend.csv"
    if not path.exists():
        return None
    d = pd.read_csv(path)
    d = d[d["app"] == "blinkit"].sort_values("period").reset_index(drop=True)
    if len(d) < 4:
        return None

    # Keep only the longest run of CONSECUTIVE quarters. Early years survive the volume
    # floor as isolated points (2019Q3, 2020Q3, then nothing until 2022Q1); plotting them
    # on a categorical axis draws a straight line across a two-year hole and reads as a
    # real trend. Better to show a shorter, honest window.
    qi = d["period"].str.slice(0, 4).astype(int) * 4 + d["period"].str.slice(5, 6).astype(int)
    run_id = (qi.diff().fillna(1) != 1).cumsum()
    longest = run_id.value_counts().idxmax()
    dropped_periods = int((run_id != longest).sum())
    d = d[run_id == longest].reset_index(drop=True)
    if len(d) < 4:
        return None
    if dropped_periods:
        print(f"    trend: dropped {dropped_periods} isolated quarter(s) outside the "
              f"continuous run ({d['period'].iloc[0]}–{d['period'].iloc[-1]})")

    freq = pd.read_csv(PROC / "theme_frequency.csv")
    fb = freq[freq["app"] == "blinkit"].sort_values("share_of_negative", ascending=False)
    top = [t for t in fb["theme"].head(4).tolist() if t in d.columns]
    short = {
        "pricing_charges": "Fees & pricing", "customer_support": "Support",
        "item_quality": "Product quality", "refund_issues": "Refunds",
        "delivery_partner": "Rider behaviour", "missing_wrong_items": "Missing items",
        "delivery_delay": "Late delivery", "returns_replacement": "Returns",
        "stock_availability": "Out of stock", "cancellation": "Cancellations",
    }

    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    x = list(range(len(d)))
    ends = []
    for k, theme in enumerate(top):
        ax.plot(x, d[theme] * 100, linewidth=2, color=m["series"][k], zorder=3,
                marker="o", markersize=5, markeredgecolor=m["surface"], markeredgewidth=1.2,
                label=short.get(theme, theme))
        ends.append([float(d[theme].iloc[-1]) * 100, k, theme])

    # De-collide the end labels: walk them in ascending y and push each up until it
    # clears the one below by MIN_GAP. Without this the lower two labels overprint.
    ends.sort(key=lambda e: e[0])
    span = max(e[0] for e in ends) - min(e[0] for e in ends)
    min_gap = max(2.0, span * 0.18)
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i - 1][0] < min_gap:
            ends[i][0] = ends[i - 1][0] + min_gap
    for y_pos, k, theme in ends:
        ax.text(len(d) - 0.7, y_pos, f"  {short.get(theme, theme)}",
                fontsize=9.5, color=m["series"][k], va="center", fontweight="bold")

    step = max(1, len(d) // 10)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(d["period"].iloc[::step], rotation=45, ha="right", fontsize=9)
    ax.yaxis.grid(True, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(-0.4, len(d) + 3.6)
    ax.set_ylim(0, None)
    # Legend below the plot: anchored above the axes it overprints the subtitle.
    # The series are also direct-labelled at the line ends, so identity never
    # depends on colour alone.
    leg = ax.legend(frameon=False, ncol=4, loc="upper center",
                    bbox_to_anchor=(0.45, -0.22), fontsize=9.5)
    for t in leg.get_texts():
        t.set_color(m["text2"])

    finish(fig, ax, m, "Are the top complaints getting better or worse?",
           "Share of Blinkit negative reviews per quarter · quarters with under 40 negative reviews omitted as too noisy",
           None)
    ax.set_ylabel("% of negative reviews", fontsize=9.5, color=m["text2"])
    fig.tight_layout()
    return save(fig, "04-theme-trend", mode)


def chart_true_ratings(mode: str):
    """The REAL Play Store distribution -- from app metadata, not our stratified corpus."""
    m = style(mode)
    meta_path = RAW / "app_metadata.json"
    if not meta_path.exists():
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    hist = (meta.get("blinkit") or {}).get("histogram")
    if not hist:
        return None

    total = sum(hist)
    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    y = range(5)
    shares = [h / total * 100 for h in hist]
    ax.barh(y, shares, height=0.6, color=m["series"][0], zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{s}★" for s in range(1, 6)], fontsize=10)
    for i, (s, h) in enumerate(zip(shares, hist)):
        ax.text(s + 1, i, f"{s:.1f}%   ({h/1e6:.2f}M)", va="center", fontsize=9.5, color=m["text2"])
    ax.set_xlim(0, max(shares) * 1.30)
    ax.xaxis.grid(True, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    score = (meta.get("blinkit") or {}).get("score", 0)
    finish(fig, ax, m, f"Blinkit's real rating distribution — {score:.2f}★ across {total/1e6:.1f}M ratings",
           "Population figures from Play Store metadata · the analysis corpus is deliberately over-weighted to 1-3★ and is NOT this shape",
           "% of all ratings")
    return save(fig, "00-true-rating-distribution", mode)


def main() -> int:
    made = []
    for mode in ("light", "dark"):
        for fn in (chart_true_ratings, chart_theme_frequency, chart_priority,
                   chart_by_app, chart_trend):
            try:
                p = fn(mode)
                if p:
                    made.append(p.name)
            except Exception as exc:
                print(f"  ! {fn.__name__} ({mode}): {type(exc).__name__}: {exc}")
    print(f"  rendered {len(made)} files into charts/")
    for n in sorted(made):
        print(f"    {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
