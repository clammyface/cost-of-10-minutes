# 1. Product & Market Understanding

**Product under study: Blinkit** (Eternal Ltd., formerly Zomato) — India's largest quick-commerce platform.

---

## 1.1 What the product is

Blinkit delivers groceries and household items in roughly 10–20 minutes from a network of **2,443 dark
stores across 300+ cities** (Q1 FY27, Apr–Jun 2026). A dark store is a small warehouse — no walk-in
customers — stocking 2,000–7,000 SKUs positioned so a rider can reach most addresses in its catchment
within minutes.

The product is not really "an app that sells groceries." It is a **latency promise**. Users pay a premium
over a neighbourhood kirana or a scheduled-delivery service specifically to collapse the gap between
wanting something and having it. Every strategic question in this case study follows from that: the moment
the latency promise stops feeling worth its premium, the category's whole value proposition weakens.

## 1.2 Business model

| Revenue stream | Mechanics |
| --- | --- |
| Product margin | Blinkit largely operates a 1P inventory model — it buys and resells, booking full product value as revenue. This is why Q1 FY27 revenue jumped **552% YoY to ₹15,664 Cr** while NOV grew 86%: an accounting model shift, not a demand explosion. |
| Customer fees | Delivery fee (up to ₹30), handling fee (₹4–₹11), small-cart fee (~₹20), plus rain/surge surcharges. Blinkit charges **zero platform fee**. |
| Advertising | Brands pay for placement, search ranking, and banners — high-margin and a growing share of profit. |
| Seller/partner income | Commissions and fulfilment charges on marketplace items. |

**Unit economics as of Q1 FY27:**

| Metric | Value | Direction |
| --- | --- | --- |
| Net Order Value (NOV) | ₹17,132 Cr | ▲ 86% YoY, 19% QoQ |
| Net AOV | **₹518** | ▼ from ₹521 YoY |
| Adjusted EBITDA | **+₹102 Cr (0.6% of NOV)** | ▲ 5th consecutive quarter of margin improvement |
| Dark stores | 2,443 | ▲ 200 net adds in the quarter |
| Daily orders | ~3.6M | ▲ |

Two things in that table matter more than the rest, and they pull against each other:

1. **Profitability is real but paper-thin.** 0.6% of NOV is a margin that a single pricing mistake erases.
2. **AOV is falling.** Growth is coming from more users ordering more often, not from bigger baskets.
   Order-level costs (rider, packing, last-mile) are largely fixed per order, so a shrinking basket against
   a fixed cost-to-serve squeezes exactly the margin Blinkit just fought to win.

This is the strategic vice the product sits inside, and it is what makes the user problem identified in
[05_problem_definition.md](05_problem_definition.md) commercially interesting rather than merely annoying.

## 1.3 Market

- India's quick-commerce market crossed **$7B GMV in 2025**, tracking toward **~$14B by 2027**; one
  published forecast puts it at **$12.97B by 2029**.
- The top three hold **85%+ of the market**.
- Growth is shifting from metro saturation to **tier-2 expansion** and from grocery into adjacent
  categories (electronics, beauty, pharmacy, festive/gifting).

### Market share (Datum Intelligence, January 2026)

| Player | Share |
| --- | --- |
| **Blinkit** | **46%** |
| Swiggy Instamart | 24% |
| Zepto | 22% |
| Others (BigBasket, JioMart, Amazon Now, Flipkart Minutes) | ~8% |

## 1.4 Competitor comparison matrix

| | **Blinkit** | **Zepto** | **Swiggy Instamart** | **BigBasket** |
| --- | --- | --- | --- | --- |
| Parent | Eternal Ltd (listed) | Independent (VC-backed) | Swiggy Ltd (listed) | Tata Digital |
| Market share | **46%** | 22% | 24% | Small in q-comm |
| Dark stores | **2,443** (300+ cities) | ~1,000+ (est.) | 1,143 (129 cities) | Hybrid model |
| Profitability | **Adj. EBITDA +₹102 Cr** | Loss-making (private) | CM −1.8%, pre-breakeven | Loss-making |
| Consumer fees | Delivery ≤₹30 · handling ₹4–11 · small cart ~₹20 · surge/rain | **All handling & surge fees scrapped; free delivery >₹99** | Delivery + handling + surge | Membership-led |
| Play Store rating | 4.58★ (9.0M) | **4.64★ (4.8M)** | 4.50★ (13.3M)¹ | **4.74★ (2.5M)** |
| Positioning | Scale + reliability + selection | **Price/fee transparency** | Bundled with food delivery | Planned weekly shop, quality |
| Key strength | Store density → coverage & speed | Aggressive fee removal | Swiggy One cross-sell | Private label, trust |
| Key weakness | **Fee load and its perception** | Cash burn, thinner network | Weakest unit economics | Slower, not truly q-comm |

¹ The Swiggy app rating covers food delivery, Instamart, and Dineout together — not Instamart alone.

> **The competitive fact that drives this entire case study:** Zepto has eliminated all handling and surge
> fees and dropped free delivery to a ₹99 threshold. Blinkit has not. Blinkit's own users name fees as
> their **#1 complaint (20.2% of negative reviews** — see [02](02_user_research.md)). A competitor is
> attacking the market leader precisely where its users are already unhappy.

Blinkit cannot simply match it. At 0.6% NOV margin with a falling AOV, blanket fee removal would erase
profitability that took five quarters to build. The interesting product question is therefore **not**
"should we cut fees?" but **"how do we make fees feel fair and predictable without giving up the
revenue?"** — which is what [09](09_solution_ideation.md) and [10](10_prioritization.md) resolve.

## 1.5 Key user segments

Derived from behaviour visible in the review corpus; sized and evidenced in
[03_personas.md](03_personas.md).

| Segment | Behaviour | What they optimise for |
| --- | --- | --- |
| **Urban convenience regulars** | Several small orders a week, top-ups | Speed and reliability; most fee-exposed because small baskets trigger small-cart fees |
| **Household stock-up buyers** | Larger, less frequent baskets | Price, quality, completeness of order |
| **Emergency/late-night buyers** | Rare, urgent, price-insensitive | Availability at odd hours — the strongest retention hook |
| **Price-comparison shoppers** | Switch between apps per order | Landed total price; the segment Zepto's fee removal directly targets |

---

## Sources

- Eternal Q1 FY27 and Q4 FY26 results and shareholder letters (NOV, AOV, dark stores, adjusted EBITDA)
- Swiggy Q4 FY26 press release and shareholder letters (Instamart GOV, dark stores, contribution margin)
- Datum Intelligence market-share estimates, January 2026
- Play Store metadata retrieved 2026-08-25, `data/raw/app_metadata.json`
- Fee structures from 2026 press coverage of Blinkit, Zepto, and Instamart pricing changes

Zepto is privately held and publishes no audited financials; its store count and losses are
**press-reported estimates** and are labelled as such wherever used.
