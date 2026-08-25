# 14. Product Analytics & Launch Strategy

---

## 14.1 Event tracking specification

Instrumentation ships **before** the experiment, verified in staging. An experiment launched on unverified
events produces a result nobody can trust and a rerun nobody budgeted for.

### Core events

| Event | Fires when | Key properties |
| --- | --- | --- |
| `cart_viewed` | Cart surface rendered | `cart_value`, `item_count`, `variant`, `fees_shown`, `threshold_gap` |
| `fee_preview_shown` | Landed cost rendered | `delivery_fee`, `handling_fee`, `small_cart_fee`, `surge_fee`, `total`, `render_ms` |
| `fee_row_expanded` | User taps a fee for explanation | `fee_type` |
| `threshold_nudge_shown` | Progress bar rendered | `gap_amount`, `fee_saved_if_crossed`, `cart_value` |
| `threshold_suggestion_shown` | Suggestion tray rendered | `suggestion_ids`, `ranking_source`, `position` |
| `threshold_suggestion_added` | User adds a suggestion | `item_id`, `price`, `ranking_source`, `position`, `new_cart_value` |
| `threshold_crossed` | Cart crosses free-delivery line | `crossed_via` (suggestion / organic), `fee_saved`, `added_amount` |
| `threshold_uncrossed` | Cart drops back below | `removed_item_id` |
| `checkout_started` | Checkout entered | `cart_value`, `total_fees`, `variant` |
| `order_placed` | Order confirmed | `order_value`, `item_count`, `total_fees`, `variant` |
| `cart_abandoned` | 30 min inactive with items | `cart_value`, `last_screen`, `fees_shown` |
| `fee_service_degraded` | Fee API times out | `fallback_shown` |

`ranking_source` on the suggestion events is what makes FR3 auditable — it distinguishes reorder-history
suggestions from generic fallbacks, so "did the personalisation work?" is answerable rather than assumed.

### Global properties on every event

`user_id` · `session_id` · `experiment_variant` · `platform` · `app_version` · `city` · `dark_store_id` ·
`is_surge_active` · `timestamp`

## 14.2 Funnels

### Primary — the mechanism funnel

```
cart_viewed
   └─► fee_preview_shown          (target ≥ 90% — G1)
        └─► threshold_nudge_shown  (eligible carts only)
             └─► threshold_suggestion_shown
                  └─► threshold_suggestion_added
                       └─► threshold_crossed       (target ≥ 12% — G2)
                            └─► order_placed
```

Each step isolates a failure mode. Nudge shown but suggestions never added means **ranking is bad** (FR3).
Suggestions added but threshold never crossed means the **gap sizing is wrong**. Threshold crossed but no
order means the nudge produced a bigger cart the user then abandoned — the worst outcome, and invisible
without this funnel.

### Counter-funnel — the abandonment path

```
cart_viewed → fee_preview_shown → cart_abandoned
```

Segmented by `threshold_gap`. If abandonment concentrates in **far-from-threshold** carts, the problem is
cost disclosure without a remedy — which validates the [09](09_solution_ideation.md) prediction and kills
S4 permanently.

## 14.3 Cohorts

| Cohort | Purpose |
| --- | --- |
| Near-threshold (gap ≤ ₹100) | Where the feature acts — effect should concentrate here |
| Far-from-threshold (gap > ₹300) | Suggestions suppressed; tests disclosure in isolation |
| Already above threshold | **S1 without S5/S6** — the clean read on transparency alone |
| Prior fee complainers | Do the people who complained actually behave differently? |
| New vs returning | Tests reorder-history ranking against fallback |
| Late-night (11pm–5am) | Anjali guardrail |

## 14.4 Feature-adoption metrics

| Metric | Target |
| --- | --- |
| Fee preview coverage | ≥ 90% of carts |
| Nudge eligibility rate | % of carts below threshold (descriptive) |
| Suggestion engagement | ≥ 20% of shown trays get a tap |
| Reorder-history share of accepted suggestions | ≥ 60% for returning users |
| Threshold-cross rate | ≥ 12% of eligible carts |
| Fee explainer tap rate | Descriptive — informs P1 sizing for S3 |

## 14.5 Phased rollout

| Stage | Exposure | Duration | Gate to advance |
| --- | --- | --- | --- |
| **Internal** | Employees | 3 days | All events verified in staging; zero crash regression |
| **5%** | 5% of users | 3 days | No guardrail breach; event payloads correct in production |
| **25%** | 25% | 1 week | AOV trending ≥ 0; abandonment within +1.5pp; margin stable |
| **50%** | 50% | 1 week | Primary metric significant or clearly trending; all guardrails green |
| **100%** | All | — | Full read on weeks 2–3; decision documented |

**Rollback:** a single feature flag reverts to control instantly. Any hard guardrail breach triggers
automatic rollback to the previous stage, not a debate.

City-level staging within the 5% and 25% stages — start in two metros with high order density so signal
accumulates fast, then broaden. Dark-store-level fee variation makes city a real confounder, so
`dark_store_id` is on every event.

## 14.6 Go-to-market

### Positioning

> **"Know what you'll pay. Always."**

Not *"we lowered our fees"* — that is false, and the correction would cost more trust than the campaign
buys. The claim is transparency and control, which is true and, per [08](08_competitive_opportunity.md),
unoccupied.

### Audience and messaging

| Audience | Message | Channel |
| --- | --- | --- |
| **Priya — fee-resentful regulars** | *"See your full total from the first item. Know exactly how to save on delivery."* | In-app, push to prior fee complainers |
| **Vikram — comparison shoppers** | *"No surprises at checkout."* | Performance marketing, app store copy |
| **Anjali — urgency users** | Nothing. Do not interrupt. | — |
| Press / investors | AOV mechanism and margin-neutral fee strategy | Earnings commentary |

### Launch sequence

1. **Silent launch** through the experiment stages — no marketing until the result is in. Marketing an
   unvalidated feature commits the company to keeping it.
2. **In-app education** at 50% — a single non-blocking coach mark on first cart view.
3. **Full campaign** post-100%, only if the result held.
4. **Support enablement** before 25% — CS needs to answer *"why does my cart show fees now?"*

### What not to say

- Never *"lower fees"* or *"cheaper"* — fees are unchanged.
- Never frame the nudge as a discount. *"Add ₹47 to save ₹30"* is honest arithmetic; *"Save ₹30!"* alone
  is not, because it hides the ₹47.

## 14.7 Post-launch monitoring

| Cadence | What |
| --- | --- |
| Real-time | Guardrail dashboard with automated alerting on stop conditions |
| Daily (during rollout) | Funnel conversion, AOV, abandonment by cohort |
| Weekly | Segment reads, suggestion ranking quality, support contact tags |
| Monthly | **Review-mining rerun** — `python src/analyze.py` on fresh reviews to track the fee theme |

The monthly review rerun is the honest check. Support-ticket volume can fall because the contact path got
harder; **Play Store complaints are the one channel Blinkit does not control**, so the fee theme share is
the least gameable measure of whether the grievance actually shrank.

---

*Targets from [07](07_metrics.md). Experiment design: [13](13_experimentation.md).*
