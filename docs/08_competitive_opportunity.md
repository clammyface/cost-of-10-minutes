# 8. Competitive & Opportunity Analysis

---

## 8.1 How each competitor handles the fee problem

| | Approach | Result | Cost to them |
| --- | --- | --- | --- |
| **Zepto** | **Eliminated** all handling and surge fees; free delivery above ₹99 | Fee complaints **11.0%** — roughly half Blinkit's | Direct margin sacrifice, funded by VC capital while loss-making |
| **Swiggy Instamart** | Retains delivery + handling + surge, bundles benefits into Swiggy One | **18.8%** — nearly as bad as Blinkit | None, but the grievance is unaddressed and CM is still −1.8% |
| **bigbasket** | Membership absorbs delivery cost; scheduled slots, not per-order fees | **8.7%** — best in class | Requires membership adoption; weaker on immediacy |
| **Blinkit** | Full fee stack: delivery ≤₹30, handling ₹4–11, small cart ~₹20, surge/rain | **20.2%** — worst of the four | None directly, but the largest exposed flank |

Same sampling method and same rules applied to all four, so the column is comparable
([02 §2.7](02_user_research.md)).

## 8.2 What the comparison actually proves

Two conclusions, and they point in opposite directions:

**1. The complaint is controllable.** Zepto and bigbasket both roughly halve it. This is not an
immutable category cost — it responds to design decisions.

**2. Both proven solutions are expensive.** Zepto pays in margin. bigbasket pays in immediacy — its
membership model works because users plan a weekly shop, which is precisely *not* Blinkit's top-up use
case. Neither route is open to a listed company running 0.6% EBITDA margin whose core value is unplanned
convenience.

### The gap

Every competitor treats fee grievance as a **pricing** problem — charge less, or bundle it into a
subscription. **Nobody has treated it as an information and control problem.**

That is the whole opportunity, and it exists because the reviews say the objection is about *sequence and
agency*, not arithmetic. Users itemise the fees accurately in their complaints — the information was
technically available. What they lacked was seeing it **before effort was sunk**, and any means of
**acting on it**. No competitor addresses either.

## 8.3 Opportunity map — user needs vs existing solutions

| User need (JTBD) | Blinkit | Zepto | Instamart | bigbasket | **Gap** |
| --- | --- | --- | --- | --- | --- |
| **See real total before building cart** (JTBD-1) | ✗ | ~ (fewer fees to hide) | ✗ | ~ (membership = predictable) | **OPEN — nobody solves this** |
| **Act to avoid an avoidable fee** (JTBD-2) | ✗ | n/a (no fees) | ✗ | n/a | **OPEN — nobody solves this** |
| **Understand why a fee exists** (JTBD-3) | ✗ | n/a | ✗ | n/a | **OPEN** |
| Feel the total is competitive (JTBD-4) | ✗ | ✓ price | ✗ | ~ | Closed by price — not matchable |
| Reach a human (JTBD-5) | ✗ | ✗ | ✗ | ~ | Open, but ops-heavy |
| Know when refund lands (JTBD-6) | ✗ | ✗ | ✗ | ~ | Open — best P1 |

Read the "n/a" cells carefully, because they are the strategic point. **Zepto has not solved JTBD-1, 2 and
3 — it has made them irrelevant by removing the fees.** That is a different thing, and it is contingent: it
holds only as long as Zepto keeps burning capital to sustain zero fees. If Zepto reinstates fees under
margin pressure, it inherits every one of these unsolved jobs with no product answer.

A transparency-and-control solution is therefore:

- **available to Blinkit now**, without touching margin
- **defensible**, because it compounds with data and merchandising rather than with spend
- **durable**, because it survives — and improves relative to — a competitor's return to fees

## 8.4 Positioning

| | Fees hidden | Fees transparent |
| --- | --- | --- |
| **Fees high** | **Blinkit today** · Instamart | *(the opportunity)* |
| **Fees low/none** | — | Zepto · bigbasket |

Blinkit cannot move down the vertical axis — 0.6% margin forbids it. It **can** move right, and the
right-hand column is empty at the high-fee row.

The positioning claim that follows is not *"Blinkit is cheapest"* — that is false and unwinnable. It is:

> **"You always know what it costs, and you always have a way to pay less."**

That is true, defensible, and achievable without a single fee changing.

## 8.5 Risks

| Risk | Assessment |
| --- | --- |
| **Zepto sustains zero fees indefinitely** | Possible while capital is available. Transparency does not beat free — but it narrows the gap, and the fee-complaint data suggests a large share of the grievance is about opacity rather than amount. |
| **Transparency backfires — early cost disclosure suppresses orders** | The single biggest risk. Directly tested as the primary guardrail ([13](13_experimentation.md)). |
| **Competitors copy quickly** | UI patterns are copyable in a quarter. The durable advantage is the personalisation layer behind the nudge, not the progress bar. |
| **Regulatory action on surge/fee disclosure** | Would *help* — Blinkit would already be compliant and ahead. |

---

*Fee complaint rates: `data/processed/theme_frequency.csv`. Competitor fee policies from 2026 press
coverage. Zepto and bigbasket financials are press-reported estimates — neither publishes audited
quick-commerce segment results.*
