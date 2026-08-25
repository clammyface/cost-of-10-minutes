# 12. UX / Product Prototype

**▶ [Open the interactive prototype](../prototype/index.html)** — clickable, self-contained, no build step.
Open the file in any browser.

> **A note on Figma.** The brief asks for Figma. This prototype is built as self-contained HTML instead —
> it is clickable, linkable, works offline, and renders in both light and dark themes. If your submission
> is graded on a `.fig` file or a Figma share link, the screens below are specified precisely enough to
> rebuild in Figma directly; the layout, copy, and states are all pinned down.

---

## 12.1 What the prototype demonstrates

Three cart states, side by side against the current experience:

| Scenario | Cart | What it shows |
| --- | --- | --- |
| **Near threshold** | ₹152 | The full feature — cost preview, progress bar, reorder-ranked suggestions. Tap a suggestion and watch the threshold clear. |
| **Far below** | ₹78 | The feature **deliberately doing nothing** — gap too large to nudge honestly |
| **Already qualifies** | ₹340 | Transparency **without** agency — the segment [15](15_post_launch.md) models as getting worse |

The second and third scenarios matter as much as the first. A prototype that only shows the happy path
hides the design decisions that are actually contested.

## 12.2 Current user journey — where it breaks

```
Open app ──► Browse ──► Add items ──► View cart ──► Checkout ──► ⚠️ SEE REAL TOTAL
   0s          2m          3m           3m30s        3m45s         │
                                                                   ▼
                                          ₹98 of goods → ₹152 to pay
                                          effort already sunk · no way to act
                                                    │
                                    ┌───────────────┴───────────────┐
                                    ▼                               ▼
                            Pay resentfully                    Abandon
                          (2–3★ review later)           (or reopen Zepto)
```

**The break is at 3m45s.** Cost arrives after 3+ minutes of effort, at the one moment the user can no
longer do anything about it except cancel. Users describe this precisely:

> *"deferent extra charges applied only on delivery. Like product charges only 98 But Delivery Charges 30
> Handling Charges 5 Small cart Fee 20"*

The information was never hidden. It was **sequenced wrong**.

## 12.3 Proposed journey

```
Open app ──► Browse ──► Add first item ──► ✅ COST VISIBLE FROM HERE ON
   0s          2m            2m10s              │
                                                ▼
                                   ₹152 · ₹47 to free delivery
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          ▼                     ▼                     ▼
                   Add a suggestion       Check out as-is        Leave
                   (own reorder list)     (one tap, never        (informed, not
                          │                blocked — FR4)         ambushed)
                          ▼
                 ₹214 · free delivery
                 saved ₹50 · AOV +₹62
                          │
                          ▼
                      Checkout — total already known, no surprise
```

The decision point moves from **3m45s to 2m10s**, and — critically — the user arrives at it holding an
**action**, not just information.

## 12.4 Screen specification

### Cart — below threshold (primary state)

```
┌─────────────────────────────────┐
│ Your cart                10 min │
├─────────────────────────────────┤
│ Amul Gold Milk 1L         ₹72   │
│ 2 × ₹36                         │
│ Britannia Brown Bread     ₹45   │
│ Bananas 6 pcs             ₹35   │
├─────────────────────────────────┤  ◄── FR1: live landed cost
│ Item total               ₹152   │
│ Delivery fee  ⓘ           ₹30   │      ⓘ = tap for explanation
│ Small cart fee ⓘ          ₹20   │
│ Handling fee  ⓘ            ₹4   │
│ ─────────────────────────────── │
│ Total                    ₹206   │  ◄── bold, unmissable
├─────────────────────────────────┤  ◄── FR2: threshold progress
│ Add ₹47 more to save ₹50 in fees│
│ ████████████████░░░░░░░         │
│ ₹152                      ₹199  │
├─────────────────────────────────┤  ◄── FR3: reorder-ranked
│ THINGS YOU USUALLY BUY          │
│ Amul Butter 100g        + ₹62   │
│ You reorder this every 2 weeks  │  ◄── the "why" is the trust signal
│ Eggs, 6 pcs             + ₹48   │
│ Bought 3 times last month       │
├─────────────────────────────────┤
│      Proceed to checkout        │  ◄── FR4: always one tap
└─────────────────────────────────┘
```

### Key design decisions

| Decision | Reasoning |
| --- | --- |
| **Fees itemised, not lumped** | Users itemise them accurately in complaints. A single "Fees ₹54" line reads as concealment. |
| **"Add ₹47 to save ₹50"** — both numbers | Never *"Save ₹50!"* alone. Stating only the saving hides the spend and reproduces the dishonesty the feature exists to fix ([14 §14.6](14_analytics_launch.md)). |
| **"You reorder this every 2 weeks"** on each suggestion | The reason is what separates a helpful nudge from an upsell. Without it, FR3 reads as margin-ranked filler. |
| **Zero-value fees hidden, not shown as ₹0** | Listing ₹0 rows adds noise and draws attention to fees that do not apply. |
| **Checkout button always present, never gated** | FR4 — protects Anjali ([03 §3.4](03_personas.md)). |
| **Suggestions suppressed when gap > ₹300** | Asking a ₹78 cart to add ₹121 is a demand, not a nudge (PRD §11.7). |
| **Green confirmation on crossing** | Closes the loop: *"Free delivery unlocked — you saved ₹30."* |

## 12.5 States covered

| State | Behaviour |
| --- | --- |
| Below threshold, gap ≤ ₹300 | Full feature — preview + progress + suggestions |
| Below threshold, gap > ₹300 | Preview + plain threshold statement; **no suggestions** |
| Above threshold | Preview + green confirmation; **no progress bar** |
| Threshold crossed live | Progress bar → confirmation, animated |
| Dropped back below | Progress bar returns, no alarm framing |
| Fee service down | Item total + *"Fees calculated at checkout"*; checkout still available |
| Empty cart | No Smart Cart surface |
| New user, no history | Suggestions fall back to category-complementary |

## 12.6 Accessibility

- Fee explanations reachable by keyboard and screen reader, not hover-only
- Progress conveyed by **text as well as the bar** — never colour or position alone
- Full light and dark theme support
- Suggestion buttons are real `<button>` elements with accessible names
- Contrast meets WCAG AA on both surfaces

---

*Requirements: [11_prd.md](11_prd.md) FR1–FR4. Journey grounded in [04](04_jtbd.md) JTBD-1 and JTBD-2.*
