# 13. Experimentation & A/B Testing

---

## 13.1 Hypothesis

> **If** shoppers see their true landed cost from the first item added, along with how close they are to
> free delivery and relevant suggestions to close that gap,
>
> **then** net AOV will rise by at least 3.3% (₹518 → ₹535) and fee-related complaints will fall,
>
> **because** the grievance in 20.2% of negative reviews is about fees being revealed too late and feeling
> uncontrollable — not about their amount — and users already close thresholds manually when they can.

### The null result that would be genuinely informative

If AOV is flat but abandonment is also flat, the transparency thesis is wrong in its *commercial* claim
but safe: fees can be disclosed early without harm, which unlocks the P2 backlog (S2, S4).

If abandonment **rises**, the thesis is wrong in a way that matters: users were completing carts partly
*because* they had not yet seen the total. That would be an uncomfortable finding and an important one —
and it would kill S4 permanently.

Both outcomes are worth knowing. The experiment is designed so either is legible.

## 13.2 Design

| | |
| --- | --- |
| **Type** | Two-arm randomised, user-level |
| **Unit** | User ID — *not* session or cart |
| **Split** | 50/50 within the exposed population |
| **Randomisation** | Deterministic hash of user_id + experiment salt |

**Why user-level, not cart-level:** a user seeing Smart Cart on one order and not the next would learn
nothing consistent, and the carryover would contaminate both arms. Basket habits form across orders, so
the unit of assignment must be the unit that forms the habit.

### Arms

| | Control (A) | Treatment (B) |
| --- | --- | --- |
| Cart display | Item total only; fees at checkout | **Full landed cost, itemised, live** |
| Threshold | None | **Progress bar: "Add ₹47 more to save ₹30"** |
| Suggestions | None | **3–5 gap-closing items, reorder-history ranked** |
| Checkout | Unchanged | Unchanged — one tap, never blocked |

Fees are **identical in both arms.** Nothing about pricing changes. The experiment isolates *information
and control*, which is the only way to attribute a result to the actual hypothesis.

## 13.3 Metrics

### Primary

**Net AOV.** MDE **+3.3%** (₹518 → ₹535).

Chosen over the North Star (WOPAC, [07](07_metrics.md)) deliberately: order frequency responds over
months, and this experiment must conclude in weeks. AOV is the metric the mechanism moves first and most
directly. WOPAC is read as a long-horizon follow-up, not a gate.

### Secondary

| Metric | Expectation |
| --- | --- |
| Threshold-cross rate | ≥ 12% of eligible carts |
| Items per basket | Should rise with AOV — if AOV rises alone, users bought pricier goods, a weaker result |
| Fee-related support contacts / 1k orders | −25% |
| Checkout completion rate | Flat or up |

### Guardrails — hard stops

| Guardrail | Stop condition |
| --- | --- |
| **Cart abandonment** | **> +1.5pp vs control** |
| **Fee revenue per order** | **< 100% of control** |
| Orders below ₹200 | > −5% |
| Time from open to order | > +8 seconds |
| Contribution margin per order | Any decrease |
| Crash / ANR rate | Any increase |

Any guardrail breach **halts rollout regardless of AOV**. A version of this feature that hits its AOV
target by suppressing small orders or by giving fees away has failed the strategy even while passing the
primary metric.

## 13.4 Sample size and duration

**Primary (AOV).** Assuming σ ≈ ₹400 on order value and MDE ₹17.1, at 80% power and α = 0.05:

```
n ≈ 16σ²/Δ² = 16 × 160,000 / 292 ≈ 8,800 orders per arm
```

**Guardrail (abandonment).** Baseline ~30%, MDE 1.5pp:

```
n ≈ 16 × p(1−p)/Δ² = 16 × 0.21 / 0.000225 ≈ 14,900 users per arm
```

**This experiment is not sample-limited.** At ~3.6M daily orders, even a 5% exposure yields ~180k
orders/day — both thresholds clear within hours.

Duration is therefore governed by **behaviour, not power**:

| Constraint | Requirement |
| --- | --- |
| Weekly seasonality | ≥ 2 full weeks — weekday and weekend basket behaviour differ materially |
| Novelty decay | ≥ 2 weeks — a new UI element draws attention that fades |
| Reorder cycle | ≥ 2 weeks — a user must place several orders for basket habits to show |

**Planned duration: 3 weeks**, minimum 2. Results are read on weeks 2–3 with week 1 reported separately,
so novelty effects are visible rather than baked into the headline.

The temptation with this much traffic is to call the result in 48 hours on a significant p-value. That
would measure novelty, not behaviour change.

## 13.5 Segmentation

Read separately — the average will hide the mechanism:

| Segment | Why |
| --- | --- |
| **Carts near threshold (within ₹100)** | Where the feature can act. Effect should concentrate here; if it doesn't, the mechanism isn't what we think. |
| Carts far below (> ₹300 gap) | Suggestions suppressed — should be neutral. A negative here means cost disclosure alone hurts. |
| Carts already above threshold | Cost preview only. **Isolates S1 from S5/S6** — the cleanest read on whether transparency alone is safe. |
| New vs returning | Returning users get reorder-history ranking; new users get fallback. Tests FR3 ranking quality. |
| Late-night (11pm–5am) | Anjali guardrail — urgency users must not be slowed. |

The third row is the most valuable analysis in the experiment: users already above the threshold receive
transparency **without** agency, which is exactly the S1-alone scenario that [09](09_solution_ideation.md)
predicted would be harmful. It answers the P2 gating question at no extra cost.

## 13.6 Rollout

| Stage | Exposure | Gate |
| --- | --- | --- |
| Internal | Employees | Instrumentation verified, no crashes |
| **5%** | 3 days | No guardrail breach; events firing correctly |
| **25%** | 1 week | AOV trending ≥ 0; abandonment within +1.5pp |
| **50%** | 1 week | Primary metric significant or trending; all guardrails green |
| **100%** | — | Full read on weeks 2–3, decision documented |

Detailed launch plan: [14_analytics_launch.md](14_analytics_launch.md).

## 13.7 Decision criteria

| Outcome | Decision |
| --- | --- |
| AOV **+3.3%**, guardrails green | **Ship to 100%.** Proceed to P1 (S3, S9, S7). |
| AOV **+1–3%**, guardrails green | **Ship.** Below MDE but positive with no downside; iterate on S6 ranking. |
| AOV **flat**, abandonment flat | **Ship the transparency half.** Thesis wrong on revenue, right on safety — unlocks S2/S4 at P2. |
| AOV up, **abandonment > +1.5pp** | **Halt.** Investigate whether the effect concentrates in far-from-threshold carts; consider gating disclosure. |
| AOV up, **orders < ₹200 down > 5%** | **Halt.** AOV gain came from suppressing top-ups — damages the frequency habit that is the North Star. |
| **Fee revenue down** | **Halt.** Fees were given away; the strategy constraint was violated. |

## 13.8 Analysis plan

- Two-sample t-test on AOV; Mann-Whitney U as a robustness check (order value is right-skewed)
- Two-proportion z-test on abandonment and threshold-cross rates
- **Bonferroni correction across the six guardrails** — with six comparisons, an uncorrected 5% threshold
  yields roughly a 26% chance of at least one spurious breach
- CUPED variance reduction using pre-period AOV, to tighten the estimate
- **Pre-register** the primary metric, MDE, and stop conditions before launch. No post-hoc metric
  switching; any additional analysis is labelled exploratory.
- Week 1 reported separately from weeks 2–3 to expose novelty decay

---

*Baselines: Eternal Q1 FY27 (AOV ₹518, ~3.6M daily orders). Complaint data:
`data/processed/theme_frequency.csv`.*
