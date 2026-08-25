# Sampling note — read before quoting any percentage

This corpus is **not a random sample** of Play Store reviews and its rating
distribution must not be read as the app's true rating distribution.

Reviews were pulled with an equal quota per star rating (1-5) across two sort
orders (newest, most-relevant). 1-3 star reviews are therefore massively
over-represented relative to reality — Blinkit's real Play Store average is
**4.58/5** across ~9.0M ratings, which is the number to cite for overall
satisfaction.

That over-sampling is deliberate: the complaint taxonomy needs enough negative
text to cluster on. It means this corpus is valid for:

* **relative** complaint frequency — which problems dominate *within* negative reviews
* complaint themes, phrasing, and severity
* cross-app comparison, since every app was sampled the same way

It is **not** valid for: overall satisfaction rates, absolute share of users
affected, or any claim of the form "X% of Blinkit users experience Y".

Where absolute reach is needed, it is estimated by combining the *relative*
theme share here with published totals (order volume, MTU) from the Eternal
shareholder letters, and labelled as an estimate.

## Excluded sources

* **Apple App Store** — the public customerreviews RSS feed returns HTTP 200 with
  zero entries for all apps/regions tested (checked 2026-08-25). Apple has moved
  review access behind the authenticated App Store Connect API.
* **Reddit** — `.json` endpoints return HTTP 403 to unauthenticated clients and
  old.reddit.com serves HTML. Requires OAuth credentials.

The corpus is therefore Android-only, which skews away from iOS users (who in
India skew higher-income). Stated as a limitation in docs/02.
