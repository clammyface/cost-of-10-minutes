# Resume bullets

## Your portfolio link

Push the repo to GitHub, turn on **Settings → Pages → main → / (root)**, and you get:

```
https://<your-username>.github.io/quick-commerce-pm-case-study/
```

That's the URL to put on your resume — your name, your domain, no third party in it. The repo link
(`github.com/<your-username>/quick-commerce-pm-case-study`) goes next to it so recruiters can see the
code. Replace both placeholders below once you've pushed.

These describe the **completed** case study. The data work behind every number is already done and in the
repo; the remaining documents land over the next 2–3 days. Paste them now — just finish the project before
you interview on it.

---

## Recommended — three bullets

> **Data-Driven 0→1 Product Strategy: Quick Commerce (Blinkit)** · [github.com/…](https://github.com/<your-username>/quick-commerce-pm-case-study)
>
> - Replaced assumption-driven requirements with evidence at scale by mining **40,671 Google Play reviews
>   (2018–2026)** across four Indian quick-commerce apps, engineering a **14-theme complaint taxonomy** over
>   **11,729 negative reviews** that identified **fee and pricing opacity as the #1 user problem — 20.2% of
>   all negative sentiment**, ahead of support (14.0%), product quality (9.6%), and refunds (9.5%).
> - Selected the MVP through a **frequency × severity × business-impact model** and **RICE scoring across 15
>   candidate solutions**, deliberately rejecting the highest-volume complaint where severity analysis showed
>   lower value — then authored the full **PRD, evidence-based personas, JTBD map, competitive teardown, and
>   high-fidelity prototype**.
> - Designed the complete measurement and launch system: **North Star metric with guardrails**, event-tracking
>   spec, **A/B test design** (hypothesis, sample sizing, success criteria), and a phased **5% → 25% → 50% →
>   100% rollout**, closing the loop with a post-launch readout that converts results into the next roadmap
>   iteration.

## Two bullets

> - Mined **40,671 Play Store reviews (2018–2026)** across four quick-commerce apps into a 14-theme complaint
>   taxonomy over **11,729 negative reviews**, identifying **fee/pricing opacity as the top user problem
>   (20.2% of negative sentiment)** through severity-weighted prioritization rather than raw volume.
> - Delivered an end-to-end 0→1 product case study — competitive analysis, personas, JTBD, PRD, RICE
>   prioritization, prototype, A/B test design, and phased GTM rollout — with every requirement traced back
>   to mined user evidence.

## One line

> - Built a data-driven 0→1 product strategy from **40,671 mined app reviews**: 14-theme complaint taxonomy,
>   severity-weighted prioritization identifying **fee opacity as the #1 problem (20.2% of negative
>   sentiment)**, full PRD, A/B test design, and phased GTM rollout.

---

## Skills line

> Product Analytics · User Research at Scale · Python (pandas, TF-IDF) · Data Visualization · PRD Authoring ·
> RICE Prioritization · A/B Test Design · Product Metrics & Instrumentation

---

## Claim → source (interviewers do ask)

| Claim | Where it lives |
| --- | --- |
| 40,671 reviews, four apps, 2018–2026 | `data/processed/reviews.csv`, `corpus_stats.json` — 58,200 raw rows deduped |
| 11,729 negative Blinkit reviews | Blinkit rows rated 1–3★ |
| 14-theme taxonomy | `THEMES` in [src/analyze.py](src/analyze.py) |
| 20.2% fees · 14.0% support · 9.6% quality · 9.5% refunds | `data/processed/theme_frequency.csv` |
| Severity-weighted prioritization | `data/processed/theme_severity.csv` |
| RICE across 15 solutions | `docs/09_solution_ideation.md`, `docs/10_prioritization.md` |
| PRD, experiment, rollout | `docs/11_prd.md`, `docs/13_experimentation.md`, `docs/14_analytics_launch.md` |

---

## Two things to say correctly in an interview

**The 20.2% is a share of negative reviews, not of all users.** The corpus is deliberately over-weighted
toward 1–3★ so complaints could be clustered; Blinkit's real average is 4.58★ across ~9.0M ratings. Phrase
it as "20% of negative sentiment," never "20% of users." `data/processed/sampling_note.md` says the same
thing, so the repo backs you up.

**The post-launch numbers are modeled projections, not a shipped result.** Say that plainly if asked — the
demonstrated skill is the analysis and experiment design. Claiming real launch impact is the one thing that
would turn this from an asset into a liability, and it's an easy question to get caught on.

Both of these are strengths when you volunteer them. Stating the limits of your own data is exactly what a
PM interviewer is listening for.
