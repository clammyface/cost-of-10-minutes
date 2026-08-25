# 3. User Segmentation & Personas

Personas below are built from behaviour visible in the corpus — rating, theme co-occurrence, and language
— not from imagination. Each carries the evidence that produced it.

---

## 3.1 The segmentation insight that drives everything

Before the personas, two findings from the 11,729 negative Blinkit reviews that overturn the obvious
assumption.

### Finding 1 — Fee complaints rise as anger falls

| Rating | Fee complaints as share | n |
| --- | --- | --- |
| 1★ | **14.1%** | 5,092 |
| 2★ | 23.4% | 2,742 |
| 3★ | **25.8%** | 3,895 |

The angriest users are *least* likely to be complaining about fees — they are dealing with rotten produce,
vanished refunds, missing items. **Fee complaints concentrate among the moderately dissatisfied.**

### Finding 2 — Fee complaints arrive alone

Users who complain about fees mention every other problem **below** the base rate:

| Also mentioned by fee complainers | Fee complainers | All negative reviews |
| --- | --- | --- |
| Support unreachable | 5.3% | 14.0% |
| Product quality | 3.7% | 9.6% |
| Refunds | 4.1% | 9.5% |
| Missing items | 2.6% | 6.3% |
| Rider behaviour | 5.8% | 9.1% |

Every single one is roughly **half** the base rate. Fee complaints are not part of a general "everything
is broken" grievance — they are a **standalone objection from users whose experience is otherwise fine.**

### Why this matters

The fee complainer is **not a churning hater. They are a satisfied user with one specific, fixable
grievance.** They got their order, on time, in good condition — and resented what they paid for it.

That makes this segment unusually valuable:

- They already have the habit. No reacquisition needed.
- They have exactly one objection, and it is a **product/pricing-design** problem, not an ops problem.
- They are the segment **Zepto's zero-fee positioning is built to capture** — and they are the most
  portable, because nothing else is holding them.

A fee fix therefore defends revenue from users who are currently ordering, currently profitable, and
currently one competitor promotion away from leaving.

---

## 3.2 Persona 1 — Priya, the Fee-Resentful Regular ★ primary

> *"Delivery is very fast and only for that reason I am ordering in your app. If you can work on prices
> and delivery charges…"* — 4★ review

| | |
| --- | --- |
| **Segment size** | ~25.8% of 3★ and 23.4% of 2★ negative reviews; **2,363 fee complaints** in corpus |
| **Behaviour** | Orders several times a week, small top-up baskets (₹150–₹400), habit formed |
| **Rating she leaves** | 2–3★ — still using it, still annoyed |

**Goals** — get small essentials fast without feeling overcharged; know the real total before committing.

**Pain points**
- A ₹98 product becomes ₹152 after ₹30 delivery + ₹20 small cart + ₹4 handling
- Fees appear at checkout, after the basket is built — the effort is already sunk
- Surge and rain fees are unpredictable and unexplained
- Zepto shows a lower landed total for the identical basket

**Behaviour that reveals intent** — she games the system rather than leaving: adds a filler item to clear
the small-cart threshold, waits out surge windows, price-checks against Zepto before ordering. *Users
gaming a fee structure are telling you the structure is wrong, not that they are cheap.*

**What would change her mind** — seeing the full landed cost early, and being given a way to *act* on it.

---

## 3.3 Persona 2 — Rahul, the Betrayed First-Timer

> *"Very bad products. I had ordered 6 kulfis and all were delivered melted and in very bad condition.
> With great difficulty [got a refund]"* — 1★ review

| | |
| --- | --- |
| **Segment size** | Bulk of the 5,092 1★ reviews; quality 9.6%, refunds 9.5%, missing items 6.3% |
| **Behaviour** | Low order count, one catastrophic experience, high churn risk |

**Goals** — receive what he ordered, in good condition; get his money back when that fails.

**Pain points** — spoiled or melted goods; items missing with no clear remedy; refunds that take days with
no visible status; support that cannot be reached by a human (14.0% of negative reviews).

**Note** — his problems are **operational**, not pricing. He is a real and important segment, but he is not
who this case study's MVP targets. Fixing dark-store cold chain and refund SLAs is a different program of
work, correctly scoped out in [05](05_problem_definition.md).

---

## 3.4 Persona 3 — Anjali, the Late-Night Loyalist

> *"at night 2am I'm hungry I checked out all apps everything is closed last I found blinkit thank u so
> much blinkit ♥️"* — 4★ review

| | |
| --- | --- |
| **Segment size** | Visible across 4–5★ reviews citing odd-hours availability |
| **Behaviour** | Infrequent but extremely high intent; price-insensitive at the moment of need |

**Goals** — availability when nothing else is open. **Pain points** — items out of stock at night (6.3%),
surge fees at exactly the hours she needs it most.

**Why she matters** — the strongest retention hook in the category and the segment where fees are *least*
resented, because urgency dominates. **She is the argument against blanket fee removal:** some users
genuinely will pay for urgency. The goal is charging the right user at the right moment, not charging
everyone always.

---

## 3.5 Persona 4 — Vikram, the Comparison Shopper

> *"it's good but not better offers than zepto"* · *"It's quite good, but costlier then other apps"*

| | |
| --- | --- |
| **Segment size** | Explicit cross-app comparisons throughout the fee theme |
| **Behaviour** | Keeps all three apps installed, checks landed total per order, no loyalty |

**Goals** — lowest total for this basket, right now. **Pain points** — Blinkit's total is often higher once
fees land; no reason to prefer it when speed is comparable.

**Why he matters** — the **direct target of Zepto's zero-fee move**, and the clearest measurable leak.
Winning him back requires either a genuinely lower total or a credible reason the total is fair.

---

## 3.6 Prioritisation

| Persona | Size | Churn risk | Fixable by product | Priority |
| --- | --- | --- | --- | --- |
| **Priya — Fee-Resentful Regular** | Largest | Medium (rising) | **High** — pricing UX | **P0** |
| Vikram — Comparison Shopper | Medium | High | Medium — needs price or clarity | P1 |
| Rahul — Betrayed First-Timer | Large | Very high | Low — ops, cold chain, refund SLA | P1 (separate program) |
| Anjali — Late-Night Loyalist | Small | Low | Protect, don't disrupt | Guardrail |

**Priya is the target.** She is the biggest reachable segment, her problem is genuinely a product problem,
she is already profitable, and she is the one a competitor is actively courting. Anjali becomes a
**guardrail**: whatever ships must not degrade the experience of users who are happy to pay for urgency.

---

*Evidence: `data/processed/reviews_tagged.csv`, `theme_frequency.csv`. Shares are of negative reviews and
are lower bounds — see [02 §2.4](02_user_research.md).*
