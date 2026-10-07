# Changelog

## 0.1.0 — 2026-10-07

- `feedback-extract`: first release.
  - Log schema, app areas (draft), anonymization rules.
  - `append_feedback.py`: IDs, stable pseudonyms, field validation, name-leak guard.
  - Eval round 1 (with skill vs without, 3 fixtures, 27 assertions): 27/27 vs 20/27.
  - Fix after round 1: apply keep/leave rules evenly across participants, and treat answers to a facilitator's leading question as context rather than requests. Round 2: 27/27, with the uneven-praise issue resolved.
  - Fixture dates moved from October to September 2026 so sessions are in the past relative to test runs.
