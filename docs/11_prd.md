# 11. PRD — Smart Cart

| | |
| --- | --- |
| **Feature** | Smart Cart — landed-cost transparency with threshold assist |
| **Components** | S1 (cost preview) + S5 (progress bar) + S6 (basket completion) |
| **Priority** | P0 |
| **Effort** | ~4 person-months |
| **Author** | Product |
| **Status** | Ready for build |

---

## 11.1 Problem statement

Fees and pricing opacity drive **20.2% of Blinkit's negative reviews (2,363 of 11,729)** — 44% more than
the next theme and more than three times the rate of delivery lateness. The objection is not that fees are
too high; it is that they are **revealed after the cart is built** and feel **uncontrollable**. A ₹98
product becomes ₹152 at checkout.

Users already perform the missing job manually — adding filler items to clear thresholds, waiting out
surge. Meanwhile **Zepto has removed all handling and surge fees** and carries roughly **half** Blinkit's
fee complaint rate, while Blinkit's **AOV is falling (₹521 → ₹518)** against a **0.6% EBITDA margin** that
makes fee reduction impossible.

Full derivation: [05_problem_definition.md](05_problem_definition.md).

## 11.2 Goals

| | Goal | Metric | Target |
| --- | --- | --- | --- |
| G1 | Make landed cost visible before effort is sunk | Carts showing full cost pre-checkout | ≥ 90% |
| G2 | Give users a way to act on fees | Eligible carts crossing threshold after nudge | ≥ 12% |
| G3 | Reverse the AOV decline | Net AOV | ₹518 → ≥ ₹535 |
| G4 | Reduce the grievance | Fee share of negative reviews | 20.2% → ≤ 15% |
| G5 | Protect fee revenue | Fee revenue per order | ≥ 100% of control |

## 11.3 Non-goals

Explicitly out of scope — each was considered and rejected:

- **Reducing or removing any fee.** Not a pricing change ([06 §6.6](06_strategy_okrs.md)).
- **Changing surge *levels*.** Only how surge is explained.
- **Fee-inclusive prices on product tiles (S2)** or **pre-cart cost banners (S4)** — P2, gated on this
  experiment's abandonment result.
- **Refunds, support, cold chain.** Real P1 problems, different teams ([05 §5.3](05_problem_definition.md)).
- **Membership or loyalty changes.**

## 11.4 Target users

**Primary — Priya, the Fee-Resentful Regular** ([03 §3.2](03_personas.md)). Orders several times weekly,
baskets ₹150–₹400, leaves 2–3★ reviews, still using the app. Fee complaints run **25.8% among 3★ reviewers
vs 14.1% among 1★** — this segment is dissatisfied but retained, and mentions other problems at half the
base rate. One objection, otherwise happy.

**Secondary — Vikram, the Comparison Shopper.** Cross-app price checker; the user Zepto's zero-fee move
directly targets.

**Guardrail — Anjali, the Late-Night Loyalist.** Urgency-driven, price-insensitive at the moment of need.
**Must not be slowed down.**

## 11.5 User stories

| # | Story | Priority |
| --- | --- | --- |
| US1 | As a shopper, I want to see the full amount including fees as I add items, so I am not surprised at checkout. | P0 |
| US2 | As a shopper below the free-delivery threshold, I want to know exactly how much more I need, so I can decide whether to add. | P0 |
| US3 | As a shopper near the threshold, I want relevant suggestions to close the gap, so adding is useful rather than wasteful. | P0 |
| US4 | As a shopper, I want the fee breakdown itemised, so I can see what I am paying for. | P0 |
| US5 | As a returning shopper, I want suggestions drawn from things I actually buy, so it does not feel like an upsell. | P0 |
| US6 | As an urgent shopper, I want to ignore all of this and check out immediately. | P0 (guardrail) |
| US7 | As a shopper facing surge, I want to know why and how long, so I can decide to wait. | P1 |

## 11.6 Functional requirements

### FR1 — Live landed-cost preview (S1)

- Persistent cart summary showing **item total, delivery fee, handling fee, small-cart fee, surge/rain fee,
  and grand total**
- Recalculates on every cart mutation, **≤ 300 ms** perceived latency
- Fee rows itemised and individually labelled; zero-value fees hidden, not shown as ₹0
- Tapping any fee row opens a one-line explanation (shared component with S3 in P1)
- **Fallback:** if the fee service is unavailable, show item total with *"Fees calculated at checkout"* —
  never a wrong number, never a blocked cart

### FR2 — Threshold progress (S5)

- When cart is below the free-delivery threshold, show remaining amount and a progress bar:
  *"Add ₹47 more to save ₹30 on delivery"*
- Framed as **savings unlocked**, never as a penalty incurred
- On crossing, confirm explicitly: *"Free delivery unlocked — you saved ₹30"*
- Hidden entirely when the cart already qualifies or no threshold applies
- Must reflect the **net** benefit: if crossing saves ₹30 delivery but the user must add ₹47, state both
  numbers honestly. Never imply crossing is free.

### FR3 — Smart basket completion (S6)

- Show **3–5 suggestions** priced to close the gap
- **Ranking, in strict order:**
  1. Items from the user's own reorder history (last 90 days)
  2. Items previously viewed but not purchased
  3. Category-complementary items
  4. Generic popular items *(last resort)*
- Each suggestion shows price and the resulting new total
- **Never rank by margin.** Margin-ranked suggestions would confirm the opportunism this feature exists to
  dispel — the reputational downside dwarfs the incremental margin.
- One-tap add, no modal, no navigation away from cart

### FR4 — Speed preservation (US6)

- Checkout remains reachable in one tap at all times
- Smart Cart never blocks, gates, or interstitials the checkout path
- No suggestion may auto-add to cart under any circumstance

## 11.7 Edge cases

| Case | Behaviour |
| --- | --- |
| Fee service down | Item total only + *"Fees calculated at checkout"*. Never guess. |
| Surge activates mid-session | Update total, show a non-blocking notice. Never silently change the total. |
| Cart already above threshold | Hide progress bar entirely; keep cost preview |
| Suggestion goes out of stock mid-flow | Remove and backfill silently |
| User removes items and drops below threshold | Re-show progress bar without alarm framing |
| Threshold unreachable (gap > ₹300) | Suppress suggestions — nudging toward an implausible basket reads as manipulative |
| New user, no order history | Fall back to category-complementary ranking |
| Cart empty | No Smart Cart surface |
| Multiple fees waived by promo | Show original struck through and waived amount |
| Very large cart | Cost preview collapses to summary; expandable |

The "threshold unreachable" case matters more than it looks. A user with a ₹120 cart facing a ₹399
threshold should not be told to add ₹279 — that is not a nudge, it is a demand, and it converts a helpful
feature into the exact opportunism the project is meant to cure.

## 11.8 Dependencies

| Dependency | Owner | Risk |
| --- | --- | --- |
| Cart-level fee API incl. surge | Backend | **Critical path** — if surge only resolves at checkout today, v1 scopes to fixed fees |
| Recommendation service with reorder history | Data/ML | High — ranking quality determines whether S6 helps or offends |
| Event instrumentation | Data | **Must ship before the experiment**, not with it |
| Design system: progress bar, fee rows | Design | Low |

## 11.9 Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| **Early cost disclosure raises abandonment** | **High** | Primary guardrail, hard stop at +1.5pp. This is the central hypothesis under test. |
| Suggestions read as upsell | High | Reorder-history-first ranking; savings framing; never margin-ranked |
| AOV rises by suppressing small orders | Medium | Guardrail on orders below ₹200 |
| Fee calc latency slows cart | Medium | 300 ms budget; optimistic UI; async surge |
| Threshold gaming (add then remove) | Low | Monitor; acceptable — the user still got their goods |

## 11.10 Success metrics

**Primary:** Net AOV ≥ ₹535 (+3.3%)

**Secondary:** threshold-cross rate ≥ 12% · fee complaint share ≤ 15% · fee-related support contacts −25%

**Guardrails (hard stops):** cart abandonment ≤ +1.5pp · fee revenue/order ≥ 100% · orders under ₹200
≥ −5% · time-to-order ≤ +8s · contribution margin not decreased

Full experiment design: [13_experimentation.md](13_experimentation.md).

## 11.11 Acceptance criteria

**FR1** — Given items in cart, when the cart is viewed, then item total, every applicable fee, and grand
total are displayed within 300 ms; and when an item is added or removed, the total updates within 300 ms;
and when the fee service errors, then item total plus *"Fees calculated at checkout"* is shown and checkout
remains available.

**FR2** — Given a cart ₹47 below threshold, when viewed, then *"Add ₹47 more to save ₹30 on delivery"* is
shown with a proportional progress bar; and when the threshold is crossed, then a confirmation states the
amount saved; and when the gap exceeds ₹300, then no suggestions are shown.

**FR3** — Given a returning user below threshold, when suggestions render, then ≥ 60% are drawn from
90-day reorder history where available; and each shows price and resulting new total; and no suggestion
adds to cart without an explicit tap.

**FR4** — Given any Smart Cart state, when the user intends to check out, then checkout is reachable in
one tap and is never blocked by a Smart Cart surface.

**Instrumentation** — All events in [14](14_analytics_launch.md) fire with correct payloads, verified in
staging before the experiment starts.

---

*Evidence: [02](02_user_research.md), [03](03_personas.md), [04](04_jtbd.md),
[05](05_problem_definition.md). Prioritisation: [10](10_prioritization.md).*
