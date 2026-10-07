# Changelog

## 0.2.0 — 2026-10-07

Team version: the log is now fed by three people (builder PM, UX, GTM), not one.

- **GTM prospect research:**
  - new session type `prospect-research`,
  - participant role `prospect` (`P-` pseudonyms),
  - feedback type `demand` (would they use, pay, recommend, or why not),
  - area `positioning` (concept, value prop, messaging, landing page, waitlist, store listing).
- **Who captured it:**
  - new required `captured_by` column (team handle of whoever ran the session),
  - `--migrate` upgrades v0.1 logs in place, keeping every row,
  - a prospect who later becomes a tester keeps one pseudonym.
- **Logging a teammate's session:** the instructions no longer assume the person logging ran the session. Clarification questions are framed so they can be forwarded to whoever did.
- **New guidance:**
  - agreement after a pitch is weak evidence, not demand,
  - low-fidelity notes give thinner rows, with nothing invented,
  - business questions aimed at the team are not feedback.
- **Evals:**
  - new GTM fixture (teammate's prospect-call notes), 10 assertions: 10/10 with the skill, 6/10 without,
  - regression on the three earlier fixtures plus `captured_by` checks: 30/30,
  - trigger set grown to 24 (adds 2 GTM positives and 2 GTM near-misses): 72/72 runs correct.
- **Fixture:** prospect-call notes dated Fri Sep 25. The first draft said Fri Sep 26, which is a Saturday; the run outputs in `docs/eval-runs/iteration-3` still carry the old date.


## 0.1.0 — 2026-10-07

- `feedback-extract`: first release.
  - Log schema, app areas (draft), anonymization rules.
  - `append_feedback.py`: IDs, stable pseudonyms, field validation, name-leak guard.
  - Eval round 1 (with skill vs without, 3 fixtures, 27 assertions): 27/27 vs 20/27.
  - Fix after round 1: apply keep/leave rules evenly across participants, and treat answers to a facilitator's leading question as context rather than requests. Round 2: 27/27, with the uneven-praise issue resolved.
  - Fixture dates moved from October to September 2026 so sessions are in the past relative to test runs.
