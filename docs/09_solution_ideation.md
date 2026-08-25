# 9. Solution Ideation

Fifteen candidate solutions to the HMW from [05 §5.5](05_problem_definition.md). The point of generating
this many is to **compare approaches before committing to one** — a single "obvious" feature chosen early
is usually a local optimum.

Solutions are grouped by the mechanism they use, because the mechanism determines the risk profile.

---

## Group A — Reveal cost earlier (information)

### S1 — Landed-cost preview in the cart
Running total including all fees, visible and itemised from the first item added, updating live.
**User impact:** High — directly answers JTBD-1. **Business impact:** Neutral to positive; risk of early
abandonment. **Effort:** Low.

### S2 — Fee-inclusive prices on product tiles
Show each item's effective cost with fees amortised across the basket.
**User impact:** Medium. **Business:** Risky — makes headline prices look higher than Zepto's in search
results, where comparison is sharpest. **Effort:** Medium.

### S3 — "Why this fee?" explainer
Tap any fee for a one-line explanation and its duration (for surge/rain).
**User impact:** Medium — answers JTBD-3. **Business:** Neutral. **Effort:** Low.

### S4 — Pre-cart delivery-cost banner
Show the applicable delivery fee and threshold on entering the store, before shopping.
**User impact:** Medium. **Business:** Highest abandonment risk of the group — cost shown before any
value is perceived. **Effort:** Low.

---

## Group B — Give the user control (agency)

### S5 — Free-delivery progress bar ★
*"Add ₹47 more to unlock free delivery"* with a live progress indicator.
**User impact:** High — answers JTBD-2, the job users already perform manually.
**Business impact:** High — **raises AOV**, directly countering the ₹521 → ₹518 decline. **Effort:** Low.

### S6 — Smart basket completion ★
Alongside S5, suggest items that close the gap — drawn from the user's own reorder history first, not
random high-margin filler.
**User impact:** High — converts a penalty into a useful purchase. **Business:** High — AOV plus
merchandising surface. **Effort:** Medium.

### S7 — "Wait and save" surge timer
Show when surge is expected to end, with an optional reminder.
**User impact:** Medium — reframes surge as a condition, not opportunism. **Business:** Mixed — shifts
demand off-peak (good for ops) but defers some fee revenue. **Effort:** Medium.

### S8 — Scheduled delivery at zero fee
Let users pick a later slot to avoid fees entirely.
**User impact:** Medium. **Business:** Risky — cannibalises the immediacy premium that *is* the product.
**Effort:** High.

### S9 — Cart-level price lock
Freeze the quoted total for 10 minutes so it cannot move while shopping.
**User impact:** Medium — removes a specific betrayal. **Business:** Neutral. **Effort:** Medium.

---

## Group C — Change the fee structure (pricing)

### S10 — Remove the small-cart fee
**User impact:** High. **Business:** **Direct revenue loss** at 0.6% margin. **Effort:** Low to build,
expensive to run.

### S11 — Remove handling fees (match Zepto)
**User impact:** High. **Business:** Margin inversion. Explicitly ruled out in
[06 §6.2](06_strategy_okrs.md).

### S12 — Loyalty credits that offset fees
Earn credits on frequency, spend them on fees.
**User impact:** Medium-High. **Business:** Positive on retention, but a discount in disguise.
**Effort:** High.

### S13 — Monthly fee cap for frequent users
*"You'll never pay more than ₹150/month in delivery fees."*
**User impact:** High for regulars. **Business:** Caps downside for heaviest users — the ones already most
profitable. **Effort:** High.

---

## Group D — Reduce the need to care

### S14 — Membership expansion (bigbasket model)
Subscription absorbing all fees.
**User impact:** High for regulars, nil for occasional users. **Business:** Predictable revenue, but
cannibalises fee income from the users who currently pay most. **Effort:** High.

### S15 — Price-match guarantee vs Zepto
**User impact:** Medium. **Business:** Cedes pricing control to a competitor and invites a race to the
bottom. **Effort:** Medium.

---

## 9.1 Comparing the approaches

| Group | Mechanism | Fixes complaint? | Revenue effect | Reversible? |
| --- | --- | --- | --- | --- |
| **A — Information** | Show cost earlier | Partly — addresses sequence, not agency | Neutral, some abandonment risk | Yes |
| **B — Agency** | Let users act on cost | **Yes — sequence *and* control** | **Positive (AOV)** | Yes |
| **C — Pricing** | Charge less | Yes | **Negative** | Hard — fee reinstatement is a PR event |
| **D — Structural** | Restructure the model | Partly | Mixed, cannibalising | Very hard |

Three observations drive the prioritisation:

1. **Group C is ruled out by strategy, not by scoring.** At 0.6% EBITDA margin, cutting fees is not a
   product decision that lost on merit — it is outside the solution space
   ([06 §6.2](06_strategy_okrs.md)). It is scored in [10](10_prioritization.md) anyway, so the rejection
   is visible rather than assumed.
2. **Group A alone is insufficient and possibly harmful.** Showing costs earlier without giving users a
   way to act just delivers bad news sooner. Information without agency is the abandonment risk with none
   of the upside.
3. **Group B is the only mechanism where user and business incentives align.** Helping a user avoid a ₹20
   fee by adding ₹47 of goods they wanted resolves the grievance *and* grows the basket. Nothing has to be
   traded away.

## 9.2 The combination worth testing

**S1 + S5 + S6** form one coherent product rather than three features:

- **S1** shows the true total from the first item (sequence — JTBD-1)
- **S5** shows the gap to the next threshold (control — JTBD-2)
- **S6** makes closing that gap effortless and useful (agency, and the AOV mechanism)

S1 alone carries abandonment risk. S5 and S6 are what convert that risk into upside: the user learns the
cost *and* immediately sees what to do about it. Shipping S1 without S5/S6 would be the single most
likely way to make this project fail.

Formally scored in [10_prioritization.md](10_prioritization.md).

---

*Grounded in JTBD from [04](04_jtbd.md), constraints from [06](06_strategy_okrs.md), competitive gaps from
[08](08_competitive_opportunity.md).*
