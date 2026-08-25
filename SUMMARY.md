# Project Summary

A complete 0→1 product management case study on **Blinkit** (India's largest quick-commerce app), built
entirely from **40,671 real Google Play reviews** instead of surveys or invented research. Covers all 15
requirements in [sarasvati.txt](sarasvati.txt).

**Case study site:** [index.html](index.html) — publishes to
`https://clammyface.github.io/cost-of-10-minutes/` via GitHub Pages
**Prototype:** [prototype/index.html](prototype/index.html)
**Resume bullets:** [RESUME.md](RESUME.md)

---

## The argument in five steps

The whole case study is one chain of reasoning. Each link is load-bearing.

**1. The complaint isn't what you'd assume.**
Fees drive **20.2%** of negative Blinkit reviews. Late delivery ranks **9th, at 6.1%**. A company built on
ten-minute delivery has solved speed — the competitive frontier moved to what that speed costs.

**2. The grievance is about sequence, not amount.**
Users itemise the fees accurately in their own complaints — *"product charges only 98 But Delivery Charges
30 Handling Charges 5 Small cart Fee 20"*. The information was never hidden. It arrived after three
minutes of shopping, at the one moment the only remaining action was to cancel.

**3. The complainers are the good customers.**
Fee complaints *rise* as anger falls (25.8% of 3★ reviews vs 14.1% of 1★), and fee complainers mention
every other problem at roughly **half** the base rate. These are habituated, profitable users with exactly
one objection — the most winnable segment in the dataset.

**4. But cutting fees is off the table.**
Blinkit runs **0.6% adjusted EBITDA margin** with **AOV falling ₹521 → ₹518**. Zepto scrapped all handling
and surge fees and carries **11.0%** fee complaints against Blinkit's 20.2% — but Zepto is private and
loss-making. Blinkit is listed and newly profitable. It cannot win that war and shouldn't enter it.

**5. So: fix perception, not price.**
**Smart Cart** — show the real total early, show the gap to free delivery, make closing that gap useful.
It resolves the complaint *and* raises AOV, because helping a user clear a threshold means a bigger
basket. **Not a single fee changes.**

---

## The 15 documents

### Research (1–5)

| # | Document | Core content |
| --- | --- | --- |
| **01** | [Product & Market](docs/01_product_market.md) | Blinkit as a "latency promise." Unit economics: 2,443 dark stores, ₹17,132 Cr NOV, +₹102 Cr EBITDA on 0.6% margin, AOV ₹518 and falling. Four-way competitor matrix. Names the strategic vice — thin margin, shrinking baskets, a competitor attacking on fees. |
| **02** | [User Research](docs/02_user_research.md) | The corpus: 40,671 reviews, 4 apps, 2018–2026. Star-stratified sampling. 14-theme keyword taxonomy, chosen over clustering with reasoning. **Hand-validation: 68% precision, 32% recall gap.** Full limitations. Cross-app fee comparison. |
| **03** | [Personas](docs/03_personas.md) | Four personas sized from the corpus — **Priya the Fee-Resentful Regular** (primary), Rahul the Betrayed First-Timer, Anjali the Late-Night Loyalist (guardrail), Vikram the Comparison Shopper. Opens with the two segmentation findings that reframe the target. |
| **04** | [Jobs-to-be-Done](docs/04_jtbd.md) | 10 JTBD statements, each traced to source reviews. JTBD-1 (know the real total) and JTBD-2 (avoid an avoidable fee) selected — users *already perform JTBD-2 manually*, the highest-confidence feature signal available. |
| **05** | [Problem Definition](docs/05_problem_definition.md) | Frequency × severity × business-impact scoring across all 14 themes. Top three land within 1 point (12.00 / 11.81 / 11.09), so the tie-break is made explicitly on four criteria. Problem statement, HMW, success criteria. |

### Strategy (6–8)

| # | Document | Core content |
| --- | --- | --- |
| **06** | [Strategy & OKRs](docs/06_strategy_okrs.md) | Vision: *"the app you open without doing arithmetic first."* Why fee-matching is a trap. Three OKRs — transparency, AOV reversal, protection. KR2.3 (fee revenue ≥ 100%) is the integrity check. Explicit non-goals. |
| **07** | [Metrics](docs/07_metrics.md) | North Star: **Weekly Orders per Active Customer**, with four rejected candidates and why. Metric tree, guardrails with stop conditions, and **counter-metrics** — what "success" might be hiding. Notes the North Star is *not* this experiment's primary metric. |
| **08** | [Competitive & Opportunity](docs/08_competitive_opportunity.md) | Every competitor treats fees as a *pricing* problem. **Nobody treats it as information and control.** Opportunity map showing JTBD-1/2/3 open across all four apps. Positioning grid — the high-fee/transparent quadrant is empty. |

### Execution (9–12)

| # | Document | Core content |
| --- | --- | --- |
| **09** | [Solution Ideation](docs/09_solution_ideation.md) | 15 solutions across 4 mechanism groups (information / agency / pricing / structural). Argues Group A alone is *harmful*, and Group B is the only one where user and business incentives align. |
| **10** | [Prioritization](docs/10_prioritization.md) | RICE across all 15. **Fee removal scores highest (540, 210) and is rejected on strategy** — shown rather than hidden, because a framework that omits what you already decided against is theatre. Explains why S1+S5+S6 must ship together. |
| **11** | [PRD](docs/11_prd.md) | Smart Cart. Goals, non-goals, 7 user stories, FR1–FR4, **10 edge cases**, dependencies, risks, acceptance criteria in given/when/then form. Includes the rule that suggestions are never margin-ranked. |
| **12** | [UX & Prototype](docs/12_ux_prototype.md) | Current journey (breaks at 3m45s) vs proposed (decision moves to 2m10s, *with an action in hand*). Screen spec, seven design decisions with reasoning, all 8 states, accessibility. |

### Measurement (13–15)

| # | Document | Core content |
| --- | --- | --- |
| **13** | [Experimentation](docs/13_experimentation.md) | Hypothesis plus the null results that would still be informative. User-level 50/50 split. Sample sizing (~8,800/arm for AOV, ~14,900 for abandonment) — **not sample-limited**, so duration is set by novelty decay and weekly seasonality, not power. Six decision rules. |
| **14** | [Analytics & Launch](docs/14_analytics_launch.md) | 12-event tracking spec, mechanism funnel plus counter-funnel, six cohorts, phased 5→25→50→100% with gates. GTM positioning ("Know what you'll pay. Always.") and an explicit *what not to say*. |
| **15** | [Post-Launch](docs/15_post_launch.md) | **⚠️ Modelled, clearly labelled.** A qualified win: AOV +2.4% (below MDE), threshold-cross 14.2% (beat), guardrails green. Then four failures — including that the **blended guardrail passed while two segments breached it**. Kills S4, blocks S2, creates two new P0s. |

---

## The published site

A seven-section narrative page designed around a **receipt motif** — the ₹98 → ₹152 grievance rendered as
an itemised bill with dotted leaders and tabular numerals.

| Section | Content |
| --- | --- |
| Hero | The thesis and four corpus stats |
| 01 The moment it breaks | The receipt, the verbatim review, the sequence-not-amount argument |
| 02 What 11,729 reviews say | Native HTML bar chart, fees highlighted, lateness 9th |
| 03 Three findings | The rating paradox, the isolation finding, the Zepto comparison |
| 04 The strategic vice | Financials showing why fee-cutting is impossible |
| 05 The answer | Smart Cart's three components, and why transparency alone harms |
| 06 The deliverable | All 15 documents plus the method loop |
| 07 Limitations | Four honest caveats, stated up front |

Type is Bricolage Grotesque + IBM Plex Sans + IBM Plex Mono. The accent colour is inherited from the
validated chart palette so page and figures agree. Full light and dark support.

---

## Repository

```
README.md · SUMMARY.md · RESUME.md · requirements.txt · .gitignore
docs/01..15_*.md          15 documents, ~15,800 words
prototype/index.html      clickable, 3 cart states, self-contained
src/scrape_reviews.py     star-stratified × 2 sort orders
src/clean.py              58,200 → 40,671
src/analyze.py            14-theme taxonomy, TF-IDF validation, severity model
src/charts.py             10 charts, light + dark, CVD-validated palette
data/processed/           10 files, committed so every number is checkable
charts/                   rendered figures
```

**Three dependencies.** No scikit-learn — TF-IDF is implemented directly in ~30 lines, because scipy's
compiled extensions are blocked by Application Control policy on this machine.

```bash
pip install -r requirements.txt
python src/scrape_reviews.py && python src/clean.py && python src/analyze.py && python src/charts.py
```

---

## Reference numbers

| | |
| --- | --- |
| Reviews analysed | 40,671 (58,200 raw) |
| Blinkit / Zepto / bigbasket / Instamart | 19,424 / 7,244 / 7,270 / 6,733 |
| Negative Blinkit reviews | 11,729 |
| Date range | 2018-09-12 → 2026-08-24 |
| Fee complaints by app | **Blinkit 20.2%** · Instamart 18.8% · Zepto 11.0% · bigbasket 8.7% |
| Fee complaints by rating | 14.1% (1★) → 23.4% (2★) → 25.8% (3★) |
| Taxonomy validation | 68% precision · 32.9% untagged |
| Blinkit real Play rating | 4.58★ across ~9.0M ratings |
| Blinkit Q1 FY27 | ₹17,132 Cr NOV · ₹518 AOV · +₹102 Cr EBITDA (0.6%) · 2,443 dark stores |

---

## Three caveats to carry into interviews

1. **20.2% is a share of negative reviews, not of users.** The corpus is deliberately skewed toward 1–3★
   so the taxonomy had enough negative text to cluster on. Blinkit's real average is 4.58★.
2. **Document 15 is modelled, not measured.** Smart Cart never shipped. Everything upstream of it is real
   and verifiable.
3. **Recall is 68%**, so every theme share is a floor, not a ceiling. The *ranking* is sturdier than the
   absolute levels.

All three are stated in the README and the documents themselves. Volunteering them is what makes the work
read as rigorous rather than oversold.

---

## Method

```
RESEARCH    40,671 reviews · 14-theme taxonomy · validated          [02]
    ↓
PROBLEM     Fees 20.2% of negative reviews · ranked #1              [05]
    ↓
STRATEGY    Fix perception, not price — 0.6% margin forbids cuts    [06]
    ↓
PRIORITISE  15 solutions · RICE · fee removal scored #1, rejected   [10]
    ↓
BUILD       Smart Cart PRD + clickable prototype               [11][12]
    ↓
MEASURE     Pre-registered A/B · 6 guardrails · 5→25→50→100%   [13][14]
    ↓
LEARN       Transparency without agency harms · roadmap changed     [15]
    ↓
ITERATE ────┘
```

The loop closes on a **negative** finding that changed the roadmap. A case study where every hypothesis
was confirmed would be less useful and less believable — real launches mostly produce qualified results,
and reading one correctly is the skill being demonstrated.
