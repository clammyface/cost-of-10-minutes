# 7. Product Metrics

---

## 7.1 North Star Metric

> ## Weekly Orders per Active Customer (WOPAC)

**Definition** — for customers who ordered at least once in the trailing 28 days, the mean number of orders
placed per week.

### Why this one

Quick commerce is a **habit business**. Its economics turn on frequency, not on any single transaction:
dark-store fixed costs amortise across order volume in a catchment, and Blinkit's own Q1 FY27 commentary
attributes growth to *"a large increase in MTU and increased frequency of transactions"* rather than to
basket size.

WOPAC also has the property a good North Star needs: **it cannot be gamed in a way that hurts the
business.** Frequency rises only if users keep choosing Blinkit — which requires the delivery to work, the
goods to arrive intact, *and* the total to feel fair. It is a composite of everything the product must get
right.

### Candidates rejected, and why

| Candidate | Why not |
| --- | --- |
| **GMV / NOV** | A lagging business output, not a product metric. Grows with discounting and with acquisition spend — tells you nothing about whether the product improved. |
| **AOV** | Directly targeted by this project's Objective 2, which disqualifies it as the *North* Star — optimising the metric you are intervening on invites tunnel vision. It is a supporting KPI, not the compass. Also trivially gamed by suppressing small orders, which would destroy the top-up habit that makes Blinkit valuable. |
| **MTU** | Measures acquisition more than product quality. A marketing push moves it without the product changing. |
| **Retention (D30)** | Good, but slow and coarse. WOPAC moves earlier and with more resolution. |
| **NPS / rating** | Too noisy, too laggy, and — as [02](02_user_research.md) shows — a 4.58★ average hides the entire complaint structure. |

### The honest caveat

WOPAC is **not the metric this project moves fastest.** A cart-level fee-transparency feature shows up in
AOV and complaint rate within weeks; it shows up in frequency over months, through the slower mechanism of
reduced grievance and improved retention. WOPAC is the right compass for the *product*, and the wrong
primary metric for *this experiment* — which is why [13](13_experimentation.md) uses AOV as the primary
and treats WOPAC as a longer-horizon read.

Conflating "our North Star" with "our experiment's primary metric" is a common and expensive mistake.

## 7.2 Metric tree

```
                    Weekly Orders per Active Customer
                                  │
        ┌─────────────────────────┼─────────────────────────┐
   ACQUISITION                ACTIVATION                RETENTION
   new MTU                first-order completion      repeat rate D7/D30
                          time-to-first-order         fee-grievance rate ◄── this project
                                  │
                          ┌───────┴────────┐
                     PER-ORDER VALUE    PER-ORDER TRUST
                     AOV ◄── this project   on-time %
                     items per basket       order accuracy
                     fee revenue/order      refund SLA
                     threshold-cross rate   support contacts/1k
```

## 7.3 Supporting KPIs

### Directly targeted by this project

| KPI | Definition | Baseline | Target |
| --- | --- | --- | --- |
| **Net AOV** | Order value net of discounts | **₹518** | ≥ ₹535 |
| **Threshold-cross rate** | Eligible carts crossing free-delivery after a nudge | 0% | ≥ 12% |
| **Fee grievance rate** | Fee share of negative reviews | **20.2%** | ≤ 15% |
| **Fee-related contacts / 1k orders** | Support contacts tagged fee/pricing | TBD | −25% |
| **Landed-cost visibility** | Carts where full cost shown pre-checkout | ~0% | ≥ 90% |

### Health metrics — watched, not targeted

| KPI | Why it is watched |
| --- | --- |
| Items per basket | Distinguishes *real* basket growth from price-mix effects. If AOV rises but items/basket is flat, users bought pricier goods rather than more goods — a weaker result. |
| Repeat rate D7 / D30 | The mechanism by which this project eventually reaches WOPAC |
| On-time delivery % | Category hygiene |
| Order accuracy | Feeds the quality/missing-items themes |
| Refund SLA | The P1 problem this project deliberately did not take on |

## 7.4 Guardrail metrics

Guardrails have **stop conditions**, not targets. Breaching one halts rollout regardless of how well the
primary metric is doing.

| Guardrail | Stop condition | What it protects against |
| --- | --- | --- |
| **Cart abandonment rate** | **> +1.5pp** vs control | The central risk: showing costs earlier suppresses orders that would have completed |
| **Fee revenue per order** | **< 100%** of control | "Success" achieved by giving fees away |
| **Contribution margin per order** | Any decrease | Margin erosion at 0.6% NOV |
| **Time from open to order placed** | **> +8 seconds** | Anjali — urgency-driven users must not be slowed ([03 §3.4](03_personas.md)) |
| **Orders below ₹200** | **> −5%** | Suppressing the small top-up order — the habit that makes Blinkit valuable |
| **App crash / ANR rate** | Any increase | Standard release hygiene |

The last one deserves emphasis. A feature that raises AOV by **discouraging small baskets** would look
like a win on every primary metric while destroying the top-up habit that drives frequency — and frequency
is the North Star. AOV and WOPAC can be pulled against each other, and this guardrail is what stops that
happening quietly.

## 7.5 Counter-metrics — what "success" might be hiding

| If we see… | It might actually mean… | Check |
| --- | --- | --- |
| AOV up | Small orders suppressed, not baskets grown | Orders below ₹200; items per basket |
| Fee complaints down | Fee-sensitive users churned rather than reconciled | Repeat rate among prior fee complainers |
| Threshold-crossing high | Users adding unwanted filler to dodge a fee | Return rate and post-purchase rating on nudged items |
| Support contacts down | Users gave up rather than got helped | Complaint rate in reviews, which is independent of the support channel |

The last row is why review-mining stays part of the measurement plan after launch: **review sentiment is
the one channel Blinkit does not control.** Support-ticket volume can fall because the contact path got
harder; Play Store complaints cannot be suppressed that way.

---

*Baselines: Eternal Q1 FY27 (AOV ₹518); `data/processed/theme_frequency.csv` (20.2%).*
