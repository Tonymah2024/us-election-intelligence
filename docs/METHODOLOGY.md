# Methodology

This document states every assumption used by the app. Notation: a *margin* is the
Democratic (or leading non-Republican) candidate's share minus the leading Republican
candidate's share, in percentage points. Positive values favour the non-Republican side.
This is a sign convention only.

## 1. Kinds of numbers

| Kind | Examples | Where it comes from |
|---|---|---|
| **Poll observation** | an individual poll's shares, sample size, field dates | Wikipedia tables (2026), 538 archive (1998–2022) |
| **Aggregator observation** | RealClearPolitics/DDHQ/Silver Bulletin averages as listed on Wikipedia; 538 daily averages (2020, 2024) | third-party published averages, stored separately |
| **Certified result** | MEDSL state results 1976–2024; ME/NE district results | official counts compiled by MEDSL / Wikipedia |
| **Modelled estimate** | weighted average, LOWESS, Bayesian average, house effects | computed in `uei.analysis` |
| **Conditional scenario** | seat / electoral-vote totals under user assumptions | computed in `uei.scenarios` |

The app never reports a probability of victory or names a likely winner.

## 2. Poll handling

* **Variants.** When a table lists several versions of one poll (with/without leaners,
  different candidate lists), the un-footnoted row is primary; others are kept with
  `is_variant = 1` and excluded from averages.
* **Populations.** If a poll reports LV and RV versions, LV is preferred (configurable).
* **Matchup.** Each race's *main matchup* is the head-to-head with the most polls in the
  90 days before its latest poll. Hypothetical matchups are stored but not used as a base.
* **Non-Republican side.** Within each matchup table, the non-Republican candidate (D or
  independent) with the highest mean share is used; races where that candidate is an
  independent are counted as "I" in seat totals.
* **Validation** rejects (never repairs): missing/unparseable dates, field dates in the
  future, start after end, shares outside 0–100 or summing above 106%, non-positive
  sample sizes, MoE outside (0, 25].
* **Duplicates and revisions.** `poll_key` = hash(race, matchup, pollster, dates, n,
  population) + version index. A later run with the same key but different numbers is a
  *revision*; a key that disappears from a re-scraped race is *removed* (kept in history).

## 3. Averages

Weighted average over the last 45 days (all polls if none):

    w_i = 0.5^(age_i / h) · sqrt(min(n_i, 1500)) / sqrt(1500) · 1/sqrt(k_i)

`h` = 14-day half-life; `k_i` = polls by the same pollster in the window (limits flooding).
Missing n is replaced by the median n of the window for weighting only.

Interval for the average: `SE = sqrt(max(D²/n_eff, Σ w_i² s_i²))` where D is the weighted
poll-to-poll SD, `n_eff = 1/Σw_i²`, and `s_i²` the multinomial sampling variance of the
margin: `[p_D(1−p_D) + p_R(1−p_R) + 2 p_D p_R] / n`. 90% interval = ±1.645 SE.

Moving averages (7/14/30 days): trailing simple and √n-weighted means by field end date.
LOWESS: statsmodels, frac = 0.4.

## 4. Bayesian average

Local-level state space model, solved exactly by a Kalman filter and RTS smoother:

    x_t = x_{t−1} + η_t,          η_t ~ N(0, 0.25²)   per day
    y_i = x_{t_i} + ε_i,          ε_i ~ N(0, s_i² + τ²),  τ = 2 pts non-sampling error

Prior: previous result for the seat (Senate/President) with SD 15, else N(0, 15²).
The credible band describes the polling average, **not** the election result.

## 5. House effects

`residual_i = margin_i − √n-weighted mean of other pollsters' polls in the same race within
±14 days` (needs ≥2 others). Effect = mean residual × n/(n+4). Positive = more Democratic
than other pollsters. This measures relative lean, not accuracy.

## 6. LV vs RV

* Paired: mean (LV − RV) for polls publishing both from the same fieldwork.
* Unpaired: OLS `margin ~ LV + race fixed effects` (confounded by pollster choice).

## 7. Historical polling error

From 538's archive (polls in the final 21 days, with certified results), per race:
`error = result − √n-weighted poll average`. Summaries by cycle and office: bias (mean
error), RMSE, SD, share of races where the poll leader lost. Error components (races with
|avg| < 20): shared cycle-wide SD = SD of cycle mean errors; race-specific SD = SD of
within-cycle deviations; implied correlation = shared² / (shared² + race²).
These are the default Monte Carlo SDs.

## 8. Scenarios

Per unit (state elector block, ME/NE district, seat, district):

    scenario = base + national + regional[region] + state[state]
             + undecided · (2a − 1) + third_party · (1 − 2f)
             + demographic_shift[state] + replacement[unit]
    (or an absolute override)

* `a` = share of undecideds breaking to the non-Republican side (0.5 = no change).
* `f` = share of hypothetical third-party support drawn from that side.
* Demographic shift: `Σ_g (w'_g − w_g) m_g` with `w_g` = CVAP share, `w'_g ∝ w_g(1+Δ_g)`,
  and `m_g` = **user-assumed** group margin (default 0; no exit-poll data are included).
  Equal baseline turnout across groups is a simplification.

**Bases**

* Senate/Governor 2026: main-matchup polling average; seats with no 2026 polls use the
  previous result for that seat, or the 2024 presidential margin if that result lacks
  party labels (each labelled). Seats not on the ballot come from Wikipedia's current
  senators list (MEDSL fallback).
* House 2026: `relative lean + generic-ballot environment`, where relative lean =
  2024 presidential margin under 2026 lines − 2024 national margin (22 districts listed),
  otherwise 2 × 2026 Cook PVI. Environment = mean of the latest aggregator generic-ballot
  averages. Candidate effects, incumbency and uncontested seats are not modelled.
* President: certified results of the chosen year, or final polling averages (538 2020;
  538 2024 snapshot to 2024-09-12; archived final-21-day polls for 2016 and states not in
  the snapshot). ME/NE districts: district result + the same shift as the state.

**Electoral College.** Winner-take-all except ME (2 + 2 districts) and NE (2 + 3).
Apportionment: 2010 census for 2012–2020, 2020 census for 2024–2028.

**Monte Carlo.** `e_u = e_nat + e_region + e_state (+ e_unit)`, independent normals.
Correlation within a region = (σ_nat² + σ_reg²)/σ²; across regions = σ_nat²/σ².
Output: percentiles of the total and 90% ranges per unit. Normal tails understate
extreme misses; outputs are conditional on the SDs chosen.

**Sensitivity.** Totals as an extra uniform shift varies from −10 to +10, and the
break-even shift at which the non-Republican side reaches the majority threshold.

## 9. Change explanation

For each race with new/revised/removed polls: previous vs new weighted average,
difference, `z = Δ / sqrt(SE_old² + SE_new²)` (conservative because averages share polls),
a composition check (average using only pollsters present before), the LV share, and the
share of partisan-sponsored new polls. Movements with |z| < 1.645 are described as
consistent with noise.

## 10. Backtests (tests/test_integration_backtest.py)

* Certified results reproduce pledged electoral votes exactly: 2016 R 306 / D 232,
  2020 D 306 / R 232, 2024 R 312 / D 226 (with ME/NE districts).
* National popular-vote margins: 2016 D+2.1, 2020 D+4.45, 2024 R+1.5 (±0.2–0.3).
* 65 Senate seats are not on the 2026 ballot; 35 are (33 Class 2 + OH, FL specials).
* Archived final presidential polls overstated Democratic margins in 2016 and 2020
  (negative mean error), matching the published post-election reviews.
