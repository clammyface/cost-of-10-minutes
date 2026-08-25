# 10. Feature Prioritization

---

## 10.1 Method

**RICE**, scored consistently across all 15 candidates from [09](09_solution_ideation.md):

```
RICE = (Reach × Impact × Confidence) ÷ Effort
```

| Factor | Scale |
| --- | --- |
| **Reach** | Share of monthly carts touched (0–1.0) × 100 |
| **Impact** | 0.25 minimal · 0.5 low · 1 medium · 2 high · 3 massive |
| **Confidence** | 50% low · 80% medium · 100% high — evidence-based, not optimism |
| **Effort** | Person-months (design + eng + data) |

**Reach basis:** ~3.6M daily orders ≈ 108M monthly. Reach 100 = every cart. Fee-bearing carts are the
majority given the ₹199 free-delivery threshold against a **₹518 net AOV** — many baskets sit near the
line, which is what makes threshold mechanics high-reach.

**Confidence is evidence-graded**, not vibes:

- **100%** — users are already doing it manually (S5, S6) or it is a pure information display (S1)
- **80%** — strong analogues elsewhere in e-commerce
- **50%** — behavioural response genuinely unknown

## 10.2 Scores

| # | Solution | Reach | Impact | Conf | Effort | **RICE** | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **S5** | **Free-delivery progress bar** | 85 | 2 | 100% | 1.0 | **170.0** | **P0** |
| **S1** | **Landed-cost preview in cart** | 100 | 2 | 100% | 1.5 | **133.3** | **P0** |
| **S6** | **Smart basket completion** | 70 | 2 | 100% | 1.5 | **93.3** | **P0** |
| S3 | "Why this fee?" explainer | 60 | 1 | 100% | 0.5 | **120.0** | P1 |
| S9 | Cart-level price lock | 40 | 1 | 80% | 1.0 | 32.0 | P1 |
| S7 | "Wait and save" surge timer | 25 | 1 | 80% | 1.5 | 13.3 | P1 |
| S10 | Remove small-cart fee | 35 | 3 | 100% | 0.5 | **210.0** | **Rejected — strategy** |
| S11 | Remove handling fees | 90 | 3 | 100% | 0.5 | **540.0** | **Rejected — strategy** |
| S13 | Monthly fee cap | 20 | 2 | 50% | 3.0 | 6.7 | P2 |
| S12 | Loyalty credits offset fees | 40 | 1 | 50% | 4.0 | 5.0 | P2 |
| S2 | Fee-inclusive prices on tiles | 100 | 1 | 50% | 2.0 | 25.0 | P2 |
| S4 | Pre-cart delivery banner | 100 | 0.5 | 50% | 0.5 | 100.0 | P2 — see note |
| S14 | Membership expansion | 30 | 2 | 50% | 6.0 | 5.0 | P2 |
| S8 | Scheduled zero-fee delivery | 15 | 1 | 50% | 4.0 | 1.9 | P3 |
| S15 | Price-match guarantee | 50 | 1 | 50% | 2.0 | 12.5 | P3 |

## 10.3 Reading the table honestly

**RICE does not pick the winner here, and pretending it did would be dishonest.**

The two highest-scoring items are **S11 (540) and S10 (210) — removing fees.** They score highest because
RICE rewards high reach, high impact, and low effort, and deleting a fee is all three. RICE has no term
for *"this destroys the company's margin."*

They are rejected on strategy, not score: at **0.6% adjusted EBITDA margin**, fee removal inverts
profitability built over five consecutive quarters ([06 §6.2](06_strategy_okrs.md)). Zepto can afford
that; a listed, newly profitable Blinkit cannot.

They are scored and shown anyway, because a prioritisation framework that quietly omits the options you
already decided against is theatre. **The framework's job is to make the trade-off visible, not to
manufacture agreement.**

Two further caveats:

- **S4 scores 100 but is a trap.** High reach, trivial effort — and it shows delivery cost *before the
  user perceives any value*. It is the purest form of the abandonment risk from
  [09 §9.1](09_solution_ideation.md). Held at P2 pending the P0 experiment result, which will tell us
  whether early cost disclosure helps or hurts.
- **S3 scores 120, above S6's 93.** It is genuinely cheap and good, and it is the first P1. It is not P0
  because explaining a fee without letting the user avoid it addresses JTBD-3 while leaving JTBD-2
  untouched — and JTBD-2 is where the AOV upside lives.

## 10.4 The P0 decision

**P0 = S5 + S1 + S6, shipped together as one feature.**

Sequencing them separately would be a mistake, for a reason worth stating explicitly:

| Shipped alone | Result |
| --- | --- |
| **S1 only** | Users learn the total is higher than expected, with no way to act. **Delivers bad news sooner.** Pure abandonment risk, no upside. |
| **S5 only** | A progress bar toward a threshold whose cost the user still cannot see in full. Incoherent. |
| **S6 only** | Suggestions to add items with no stated reason. Reads as an upsell, which is exactly the opportunism users already resent. |
| **S1 + S5 + S6** | See the true cost → see the gap → close it usefully. **Coherent, and the only combination where the AOV upside offsets the abandonment risk.** |

This is the case where RICE's per-item scoring is actively misleading: the three items are **complements,
not alternatives**, and their combined value exceeds the sum of the parts. Scoring them independently
understates the bundle and would have produced the wrong roadmap.

### Total P0 effort: ~4 person-months

| Role | Scope |
| --- | --- |
| Design | 0.5 pm — cart redesign, progress bar, suggestion tray |
| Frontend | 1.5 pm — live fee calc, progress UI, suggestion rail |
| Backend | 1.0 pm — fee-preview API, threshold logic, suggestion ranking |
| Data | 1.0 pm — event instrumentation, experiment pipeline, dashboards |

## 10.5 Roadmap

| Phase | Items | Rationale |
| --- | --- | --- |
| **P0 — Q1** | S1 + S5 + S6 | The bundle. Resolves JTBD-1 and JTBD-2, tests the core hypothesis. |
| **P1 — Q2** | S3, S9, then S7 | Completes fee *comprehension* once fee *control* is proven. S3 first — cheapest, highest RICE of the P1s. |
| **P2 — Q3** | S2, S4, S13 | Gated on the P0 abandonment read. If early cost disclosure proves safe, S2/S4 become attractive; if it proves harmful, both are dead and that is a valuable finding. |
| **P3** | S8, S15 | Low value or strategically undesirable. |
| **Never** | S10, S11 | Fee removal. Revisit only if margin structurally improves. |

## 10.6 Dependencies and risks

| Dependency | Why it matters |
| --- | --- |
| Real-time fee calculation API | S1 needs the full fee stack — including surge — computable at cart level, live. If surge is only resolved at checkout today, this is the critical path. |
| Recommendation service | S6 must rank from the user's **own reorder history first**. Generic high-margin filler would confirm the opportunism users already complain about. |
| Event instrumentation | Must ship **before** the experiment, not alongside it ([14](14_analytics_launch.md)). |

| Risk | Mitigation |
| --- | --- |
| **Early cost disclosure raises abandonment** | Primary guardrail, hard stop at +1.5pp ([13](13_experimentation.md)) |
| **S6 reads as an upsell** | Rank from own reorder history; frame as *"add ₹47 to save ₹30"*, never *"you may also like"* |
| **AOV rises by suppressing small orders** | Guardrail on orders below ₹200 ([07 §7.4](07_metrics.md)) |
| **Surge unavailable at cart time** | Scope S1 to fixed fees in v1; add surge when the API supports it |

---

*Reach from Eternal Q1 FY27 (~3.6M daily orders, ₹518 net AOV). Impact and confidence grounded in
[02](02_user_research.md) and [04](04_jtbd.md).*
