# 6. Product Strategy & Goals

---

## 6.1 Product vision

> **Blinkit should be the app you open without doing arithmetic first.**
>
> Speed is no longer the differentiator — the category has commoditised 10-minute delivery, and Blinkit's
> own users rank lateness 9th among their complaints. The next competitive frontier is **trust in the
> total**: the confidence that what you see is what you pay, and that you were never quietly penalised for
> ordering a small basket on a rainy Tuesday.

## 6.2 The strategic situation

Three facts define the board:

| | |
| --- | --- |
| **Margin is real but fragile** | Adjusted EBITDA **+₹102 Cr = 0.6% of NOV** (Q1 FY27), fifth consecutive quarter of improvement. A pricing mistake erases it. |
| **AOV is declining** | Net AOV **₹518**, down from ₹521. Growth comes from more users ordering more often, not bigger baskets. Per-order costs are largely fixed — a shrinking basket against fixed cost-to-serve squeezes margin. |
| **A competitor has attacked the weak point** | **Zepto scrapped all handling and surge fees**, free delivery above ₹99. Its fee complaint rate is **11.0% vs Blinkit's 20.2%**. |

### The strategic trap, stated plainly

The obvious response — match Zepto and cut fees — is the wrong move, and it is worth being explicit about
why. Fee revenue at roughly ₹30–54 per fee-bearing order sits against a **0.6% margin**. Removing it does
not dent profitability; it **inverts** it. Zepto can absorb that because it is private, loss-making, and
buying share with investor capital. Blinkit is listed, newly profitable, and judged quarterly on the
margin trajectory it has spent five quarters building.

**Blinkit cannot win a fee-elimination war and should not enter one.**

But it cannot ignore the flank either — 20.2% of its negative reviews are already about fees, and its most
portable users are precisely the ones Zepto is courting.

## 6.3 Strategic objective

> **Neutralise the fee grievance through product design rather than price reduction — converting an
> opaque penalty into a transparent, controllable choice — and use the same mechanism to reverse the AOV
> decline.**

The strategy's whole leverage sits in one insight from [04](04_jtbd.md): the intervention that fixes the
user's complaint (*show me the total and let me control it*) is the **same** intervention that grows the
basket (*add ₹47 more and the fee disappears*). User need and business need point the same way, so no
trade-off has to be brokered.

### Why this is defensible

Zepto's move is easy to copy and expensive to sustain — it is a **price** position, and price positions
are matched or outspent. Making cost legible and controllable is a **product** position: it compounds with
data, personalisation, and merchandising, and it does not require Blinkit to be the cheapest. It also
degrades gracefully — if Zepto later reinstates fees under margin pressure, Blinkit's transparency
advantage remains.

## 6.4 Connecting user problem to business objective

| User problem | Product response | Business outcome |
| --- | --- | --- |
| "Fees appear after I've built my cart" (JTBD-1) | Landed cost visible from first item | Fewer abandoned checkouts, less fee-shock churn |
| "I'd have avoided that fee if I'd known" (JTBD-2) | Threshold progress + relevant add-ons | **AOV up** — directly counters ₹521 → ₹518 |
| "Surge feels like opportunism" (JTBD-3) | Explain the fee, bound it, offer to wait | Fee revenue defended, complaints fall |
| "Zepto is cheaper" (JTBD-4) | Fair, predictable total | Retention against a zero-fee competitor |

## 6.5 OKRs — one quarter

### Objective 1 — Make total cost transparent and controllable

*Own the grievance directly.*

| KR | Baseline | Target |
| --- | --- | --- |
| KR1.1 Fee share of negative reviews | 20.2% | **≤ 15%** |
| KR1.2 Users seeing landed cost before checkout | ~0% | **≥ 90%** of carts |
| KR1.3 Fee-related support contacts per 1,000 orders | baseline TBD at instrumentation | **−25%** |

### Objective 2 — Reverse the AOV decline without cutting fees

*Prove the mechanism pays for itself.*

| KR | Baseline | Target |
| --- | --- | --- |
| KR2.1 Net AOV | ₹518 | **≥ ₹535 (+3.3%)** |
| KR2.2 Carts crossing free-delivery threshold after a nudge | 0% | **≥ 12%** of eligible carts |
| KR2.3 Fee revenue per order | baseline | **≥ 100%** — must not fall |

KR2.3 is the one that keeps this honest. Any version of this feature that hits its AOV target by quietly
giving away fees has failed, not succeeded.

### Objective 3 — Protect what already works

*Guardrails, not aspirations.*

| KR | Target |
| --- | --- |
| KR3.1 Cart abandonment | **No increase** vs control |
| KR3.2 Time from app-open to order placed | **No increase** (protects Anjali, [03 §3.4](03_personas.md)) |
| KR3.3 Contribution margin per order | **No decrease** |

Objective 3 exists because the core risk of this strategy is self-inflicted: **showing costs earlier could
suppress orders that would otherwise have completed.** That risk is tested, not assumed
([13](13_experimentation.md)).

## 6.6 What this strategy explicitly does not do

Naming the non-goals prevents scope drift:

- **Does not reduce or remove any fee.** Not a pricing project.
- **Does not chase Zepto on price.** That contest is unwinnable at 0.6% margin.
- **Does not fix refunds, support, or cold chain.** Real problems (P1/P2), different teams, different
  quarter — see [05 §5.3](05_problem_definition.md).
- **Does not touch surge *levels*.** Only how surge is explained and whether users can wait it out.

---

*Financials: Eternal Q1 FY27 results. Complaint data: `data/processed/theme_frequency.csv`.*
