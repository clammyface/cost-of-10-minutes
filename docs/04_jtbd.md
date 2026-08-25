# 4. Jobs-to-be-Done

Complaints describe what broke. Jobs describe what the user was *trying to accomplish* when it broke. This
document converts the taxonomy from [02](02_user_research.md) into JTBD statements, each traced to the
review language that produced it.

Format: **When** [situation], **I want to** [motivation], **so I can** [expected outcome].

---

## 4.1 Fee and pricing jobs — the primary cluster

**20.2% of negative reviews · 2,363 reviews**

### JTBD-1 — Know the real total before I invest effort ★ primary

> **When** I start filling my cart, **I want to** see the actual amount I will pay including every fee,
> **so I can** decide whether it is worth it before I have spent ten minutes shopping.

*Evidence:* `"deferent extra charges applied only on delivery. Like product charges only 98 But Delivery
Charges 30 Handling Charges 5 Small cart Fee 20"`

The grievance is **sequence**, not amount. The user itemises the fees accurately — the information was
available. What they object to is discovering it *after* the effort was sunk. This is a
classic sunk-cost-then-surprise pattern, and it converts a fair price into a feeling of being tricked.

### JTBD-2 — Avoid a fee I could have avoided ★ primary

> **When** my cart is just below a fee threshold, **I want to** know how close I am and what would clear
> it, **so I can** choose to add something useful instead of paying ₹20 for nothing.

*Evidence:* users describe adding filler items to dodge small-cart fees, and a widely shared "trick" for
avoiding small-cart and rain charges circulates publicly.

**Users are already doing this job manually.** The product does not support it — so they route around it.
A job users perform *despite* the product is the highest-confidence feature signal available, because
demand is already demonstrated rather than assumed.

### JTBD-3 — Understand why a fee exists

> **When** I am charged a surge or rain fee, **I want to** understand what it is for and how long it
> lasts, **so I can** decide to wait or accept it rather than feel exploited.

*Evidence:* `"sometimes it takes extra money for surge hours"` · `"Various Surge Fees and forcing the
customer to regularly order above Rs.500 is a bit too much"`

An unexplained variable charge reads as opportunism. The same charge, explained and bounded, reads as a
condition of service.

### JTBD-4 — Confirm I am not overpaying versus alternatives

> **When** I am about to order, **I want to** feel confident the total is competitive, **so I can** stop
> checking three apps every time.

*Evidence:* `"not better offers than zepto"` · `"costlier then other apps"` · `"Variation in the MRP as
compare to market"`

---

## 4.2 Trust and recovery jobs

**Support 14.0% · refunds 9.5% · returns 6.5%**

### JTBD-5 — Reach a human when the system fails

> **When** something has gone wrong that the app cannot fix, **I want to** reach a person who can decide,
> **so I can** stop repeating myself to a bot.

*Evidence:* `"no human support and no way to resolve any issue"` · `"there is NO customer [support]"`

### JTBD-6 — Know when my money is coming back

> **When** my refund has been approved, **I want to** see exactly when it will land, **so I can** stop
> worrying and stop contacting support.

*Evidence:* `"money deducted"`, `"not credited"`, `"with great difficulty"` recur throughout the refund
theme. Note the business consequence: refund uncertainty **manufactures support tickets**. Two of the top
four themes are causally linked, and JTBD-6 is the cheaper place to intervene.

### JTBD-7 — Return something that arrived wrong

> **When** an item arrives spoiled or wrong, **I want to** start a return without negotiating,
> **so I can** get the outcome I already deserve.

*Evidence:* `"missing product and no platform to return or cash back"`

---

## 4.3 Core delivery jobs

### JTBD-8 — Get an ETA I can plan around

> **When** I am told delivery takes 10 minutes, **I want to** the estimate to hold, **so I can** plan
> around it rather than treat it as marketing.

*Evidence:* `"very difficult to trust their delivery timelines. 23 mins delivery usually turns out to be
45 mins"`

At 6.1% this ranks 9th — **Blinkit has largely solved the job it was founded on.** The remaining grievance
is about the *credibility* of the estimate, not raw speed.

### JTBD-9 — Receive what I ordered, intact
### JTBD-10 — Pay with the method I have

*Evidence:* `"cash on delivery is not applicable"` · `"Pluxee card cannot be added before payment"`

---

## 4.4 Job map — which jobs to serve

| Job | Cluster | Frequency | Severity | Product-fixable | Priority |
| --- | --- | --- | --- | --- | --- |
| **JTBD-1** Know the real total upfront | Fees | **20.2%** | Medium | **High** | **P0** |
| **JTBD-2** Avoid an avoidable fee | Fees | **20.2%** | Medium | **High** | **P0** |
| JTBD-3 Understand why a fee exists | Fees | 20.2% | Medium | High | P1 |
| JTBD-6 Know when my refund lands | Trust | 9.5% | **High** | High | P1 |
| JTBD-5 Reach a human | Trust | 14.0% | High | Medium (ops cost) | P1 |
| JTBD-7 Return something | Trust | 6.5% | High | Medium | P2 |
| JTBD-4 Confirm competitiveness | Fees | 20.2% | Low | Low (pricing, not UX) | P2 |
| JTBD-8 ETA I can plan around | Delivery | 6.1% | Medium | Medium | P2 |
| JTBD-9 Receive intact | Delivery | 9.6% | **High** | Low (ops/cold chain) | Separate |
| JTBD-10 Pay with my method | Payment | 2.8% | High | High | P2 |

**JTBD-1 and JTBD-2 are the target.** Together they define one coherent job — *"let me see and control what
this actually costs, before I have committed"* — and they share a single surface: the cart.

Two properties make them unusually attractive:

1. **Neither requires changing a single fee.** They change *when* cost is revealed and *what the user can
   do about it*. That matters enormously given Blinkit's 0.6% NOV margin ([01](01_product_market.md)) —
   the whole intervention is available without touching revenue.
2. **JTBD-2 can raise AOV while resolving the complaint.** Helping a user clear a threshold means a bigger
   basket. Blinkit's AOV is *falling* (₹521 → ₹518). The user's job and the business's need point the same
   direction — a rare alignment, and the reason this is the right place to build.

---

*Every quoted review is drawn verbatim from `data/processed/reviews.csv`.*
