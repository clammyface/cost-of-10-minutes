# 15. Post-Launch Analysis & Iteration

> ## ⚠️ These results are MODELLED, not measured
>
> Smart Cart was never shipped to real Blinkit users — this is a portfolio case study, not work done
> inside Eternal Ltd. The numbers below are **projections**, derived by applying published e-commerce
> benchmarks for threshold-nudge and cost-transparency features to the real baselines established in
> [01](01_product_market.md) and the real complaint distribution in [02](02_user_research.md).
>
> They demonstrate **how a launch would be read and acted on** — the analysis method is the deliverable.
> They are not evidence that this feature works. Any claim of real shipped impact would be false.
>
> Everything upstream of this document — the 40,671-review corpus, the taxonomy, the complaint
> frequencies, the competitive and financial data — is **real and verifiable**.

---

## 15.1 Modelled results vs pre-registered criteria

Read on weeks 2–3, with week 1 excluded for novelty decay, per [13 §13.4](13_experimentation.md).

### Primary

| Metric | Baseline | Target | **Modelled** | Verdict |
| --- | --- | --- | --- | --- |
| **Net AOV** | ₹518 | ≥ ₹535 (+3.3%) | **₹530 (+2.4%)** | ⚠️ **Below MDE, directionally positive** |

### Secondary

| Metric | Target | Modelled | Verdict |
| --- | --- | --- | --- |
| Threshold-cross rate | ≥ 12% | **14.2%** | ✅ Beat |
| Items per basket | Should rise with AOV | **+0.31 (+7.1%)** | ✅ Real basket growth, not price mix |
| Fee complaint share | ≤ 15% | **16.8%** | ⚠️ Improved from 20.2%, missed target |
| Fee-related support contacts | −25% | **−19%** | ⚠️ Missed |

### Guardrails

| Guardrail | Stop condition | Modelled | Verdict |
| --- | --- | --- | --- |
| Cart abandonment | > +1.5pp | **+0.9pp** | ✅ Within — but real |
| Fee revenue / order | < 100% | **101.2%** | ✅ Held |
| Orders below ₹200 | > −5% | **−2.1%** | ✅ Within |
| Time to order | > +8s | **+3.1s** | ✅ Within |
| Contribution margin | Any decrease | **+0.4%** | ✅ Held |

**Decision: ship at 100%.** Under the pre-registered criteria in [13 §13.7](13_experimentation.md), AOV
+1–3% with green guardrails is an explicit ship condition. It is a qualified win, not a triumph.

## 15.2 What worked

**1. The mechanism is real.** Threshold-cross beat target (14.2% vs 12%) and **items per basket rose 7.1%
against a 2.4% AOV rise.** That ratio matters: baskets grew because users added *more goods*, not pricier
ones. The counter-metric from [07 §7.5](07_metrics.md) — "AOV up because small orders were suppressed" —
is ruled out, with orders below ₹200 down only 2.1%.

**2. Fee revenue held (101.2%).** The core strategic constraint — fix the grievance without giving up
revenue at 0.6% margin — was satisfied. This is the finding that makes the approach repeatable.

**3. Reorder-history ranking carried the result.** 64% of accepted suggestions came from the user's own
90-day history, clearing the 60% bar in FR3. The alternative — margin-ranked filler — would likely have
confirmed the opportunism the feature exists to dispel.

## 15.3 What failed, and why

### Failure 1 — AOV missed the MDE (+2.4% vs +3.3%)

Effect concentrated almost entirely in **near-threshold carts (gap ≤ ₹100), which showed +6.8% AOV**.
Far-from-threshold carts were flat. The ₹300 suppression rule in FR3 was correct — but it meant the
feature simply **had no mechanism for a large share of carts.**

The MDE was set from a blended average while the mechanism only operates on a subset. **The target was
mis-specified, not merely missed.** A better pre-registration would have set the MDE on the addressable
segment and forecast blended impact from its share.

### Failure 2 — Disclosure-only carts got worse

The cleanest analysis in the design ([13 §13.5](13_experimentation.md)) — carts already above the
threshold, receiving **S1 transparency with no S5/S6 agency**:

| Segment | Abandonment vs control |
| --- | --- |
| Near-threshold (nudge + suggestions) | **−0.4pp** (improved) |
| Already above threshold (disclosure only) | **+2.1pp** ⚠️ |
| Far-from-threshold (disclosure, suppressed suggestions) | **+1.8pp** ⚠️ |
| **Blended** | +0.9pp |

**The blended guardrail passed while two segments breached it.** Averaging concealed a real harm.

This is the most valuable finding in the launch, and it confirms the
[09 §9.1](09_solution_ideation.md) prediction exactly: **information without agency delivers bad news
sooner.** Where users could act, transparency *helped*. Where they could not, it hurt.

**Consequence: S4 (pre-cart cost banner) is dead**, and S2 (fee-inclusive tile prices) must not ship in
its current form. Both are pure disclosure with no remedy. The P2 backlog was gated on this read and the
gate closed — which is exactly what gating is for.

### Failure 3 — New users underserved

New users have no reorder history, so FR3 fell back to category-complementary ranking. Suggestion
acceptance was **11% for new users vs 24% for returning**. The fallback is materially weaker and was
treated as an afterthought in the PRD.

### Failure 4 — Complaint share missed (16.8% vs ≤15%)

Two plausible causes, not separable with current data:
- Review sentiment lags product change — reviews reference experiences weeks old
- The residual grievance is about fee **amount**, not presentation — the part transparency cannot fix

Distinguishing these requires another quarter of review mining.

## 15.4 Learnings

| # | Learning | Evidence |
| --- | --- | --- |
| 1 | **Transparency without agency is harmful.** Cost disclosure helps only when paired with a way to act. | +2.1pp abandonment in disclosure-only vs −0.4pp where nudges applied |
| 2 | **Blended guardrails hide segment harm.** Segment-level stop conditions are needed, not just aggregate. | Guardrail passed at +0.9pp while two segments breached |
| 3 | **Set the MDE on the addressable segment.** A blended target understates a mechanism that only reaches part of the population. | +6.8% near-threshold vs +2.4% blended |
| 4 | **Personalisation is the feature, not the packaging.** Ranking source drove a 2× gap in acceptance. | 24% returning vs 11% new |
| 5 | **Review sentiment lags behavioural metrics.** Do not gate a launch decision on it. | Complaints −3.4pp while behaviour moved more |

## 15.5 Next hypothesis

> **If** we replace pure cost disclosure with **agency in every cart state** — giving above-threshold and
> far-from-threshold users an action too (a next savings tier, a bundle, a wait-and-save option) —
>
> **then** the +2.1pp abandonment in disclosure-only carts will reverse and blended AOV will reach the
> original +3.3%,
>
> **because** the segment analysis shows the harm tracks the *absence of a remedy*, not the presence of
> information.

### Roadmap iteration

| Priority | Change | Source |
| --- | --- | --- |
| **P0** | **Next-tier nudges for above-threshold carts** — *"Add ₹120 for ₹50 off"* — so no cart is disclosure-only | Failure 2 |
| **P0** | **Cold-start ranking for new users** — category affinity from session behaviour, not generic popularity | Failure 3 |
| **P1** | **Segment-level guardrails** in the experiment platform, not just blended | Learning 2 |
| **P1** | S3 "Why this fee?" — proceed as planned; explanation may address residual amount-grievance | Failure 4 |
| **P2** | S7 wait-and-save — gives far-from-threshold users an action | Failure 2 |
| **Killed** | **S4 pre-cart banner** — pure disclosure, now evidenced as harmful | Failure 2 |
| **Blocked** | S2 fee-inclusive tiles — redesign to include a remedy before reconsidering | Failure 2 |

## 15.6 The complete PM loop

```
RESEARCH      40,671 reviews mined, 14-theme taxonomy, validated at 68% precision   [02]
    ↓
PROBLEM       Fees = 20.2% of negative reviews; severity-weighted to #1              [05]
    ↓
STRATEGY      Fix perception, not price — 0.6% margin forbids fee cuts               [06]
    ↓
PRIORITISE    15 solutions, RICE; fee removal scored highest and rejected on strategy [10]
    ↓
BUILD         Smart Cart PRD — S1 + S5 + S6 as one coherent feature                  [11]
    ↓
MEASURE       Pre-registered A/B, 6 guardrails, phased 5→25→50→100%                   [13][14]
    ↓
LEARN         Transparency without agency harms; blended guardrails hide harm         [15]
    ↓
ITERATE       Agency in every cart state → next hypothesis ──────────┐
    ↑                                                                │
    └────────────────────────────────────────────────────────────────┘
```

The loop closes on a **negative** finding that changed the roadmap — S4 killed, S2 blocked, two new P0s
created. A case study where every hypothesis was confirmed would be less useful and less believable: real
launches mostly produce qualified results, and the skill being demonstrated is reading one correctly.

---

*Modelled from real baselines: Eternal Q1 FY27 (AOV ₹518, ~3.6M daily orders);
`data/processed/theme_frequency.csv` (20.2%). Benchmarks for threshold-nudge lift and cost-disclosure
abandonment drawn from published e-commerce studies. **No real launch occurred.***
