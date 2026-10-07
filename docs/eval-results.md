# feedback-extract: eval results

Run on 2026-10-07 with Claude Opus 5.5. All transcripts are synthetic and written for testing; the names in them are fictional. Raw outputs from every run (the log each run produced plus its reply to the user) are in `docs/eval-runs/`.

## Method

**Output tests.** There are three sessions, each with planted traps:

1. **Stakeholder demo:**
   - an idea the co-founder withdraws in the same breath,
   - the PM's own opinion,
   - a bug already fixed during the call,
   - one concern raised twice by the same person,
   - a scope-ambiguous ask ("it should be easier to add friends"),
   - a third party's name.
2. **Moderated user test with two participants:**
   - the same problem hit by both (once spoken, once only observed),
   - a blocker,
   - a leading question from the moderator,
   - a friend's full name,
   - a religious detail,
   - a relative's divorce.
3. **Follow-up demo appended to an existing 14-row log:**
   - the co-founder appears under a nickname,
   - a new investor joins,
   - a repeat complaint from last session,
   - a business-metrics question,
   - confirmation that an earlier bug is fixed.

Each session ran twice in parallel: once with the skill, and once as a baseline with no skill (same prompt, same files). Each run was scored against written assertions, 27 in total. Name and privacy checks were scripted (grep over the log); the rest were graded by reading the log rows.

**Trigger tests.** 20 realistic requests were each run 3 times:

- 10 that should fire the skill, phrased in different ways (demo transcripts, usability notes, WhatsApp beta feedback, rough dinner notes).
- 10 near-misses that share words with the skill but need something else: summarize a standup, write stories from promoted items, analyze trends in the log, reply to app-store reviews, write a feedback survey, split a story into tickets.

## Results: output tests

| Session | With skill (round 1) | Without skill | With skill (round 2, after fix) |
|---|---|---|---|
| Stakeholder demo | 10/10 | 6/10 | 10/10 |
| User test (2 participants) | 9/9 | 7/9 | 9/9 |
| Follow-up demo, existing log | 8/8 | 7/8 | 8/8 |
| **Total** | **27/27 (100%)** | **20/27 (74%)** | **27/27 (100%)** |

### Where the baseline failed

| Assertion | Baseline result |
|---|---|
| Log follows the shared schema | Invented its own columns, which differed between runs. One user-test log had 14 columns, one demo log had 11. Triage can't count across logs that differ. |
| No real names in the log | The co-founder's name appeared in all 5 rows of the demo log. |
| Ambiguous ask carries a question, not a guess | Logged "add friends should be easier" as a discoverability issue, with no question to the PM. |
| Reply lists the decisions the PM must make | No clarification questions at all. |
| Religious detail stays out | Kept "shared faith" in the request text. |
| Users get user pseudonyms | Used its own P1/P2 labels, which don't persist across sessions. |
| Business question isn't logged as product feedback | Logged the investor's retention question and invented a new area for it. |

The baseline also leaked the co-founder's name in the follow-up demo. That wasn't covered by an assertion, but it's visible in `docs/eval-runs/`.

### What the baseline already did well

20 of the 27 assertions passed with and without the skill, including:

- dropping the withdrawn idea,
- ignoring the PM's own remark,
- skipping the fixed bug,
- merging one person's repeat,
- spotting the observed-only friction,
- recognizing the nickname.

This is an honest finding. A strong model already makes most single-session judgement calls well. The skill's measurable value is in **consistency** (one schema, stable IDs and pseudonyms, so the log accumulates), **privacy**, and **asking instead of guessing**. Those three are what a downstream triage step depends on.

### Round 1 → round 2

Round 1 passed every assertion, but reading the outputs showed one inconsistency:

- **Uneven short remarks.** In the user test, one tester's "fast, nice" about chat was logged and the other's equivalent "easy, done" was not. That undercounts agreement in triage.
- **Leading questions.** The SKILL.md had no explicit rule for answers to a facilitator's leading question.

Both rules were added. In round 2, both testers' remarks were logged and the leading-question answer was kept out of the requests. It's still 27/27, with the inconsistency gone.

## Results: trigger tests

| Run | Should fire (10 × 3) | Should not fire (10 × 3) |
|---|---|---|
| Final, sequential | 30/30 fired | 0/30 fired |

All 20 queries passed on every run.

### Harness pitfall worth knowing about

The first two trigger runs reported almost no triggering (recall of 0–11%). That result was wrong.

The harness registers a uniquely named copy of the skill for each query in a shared folder. With 10 workers in parallel, Claude saw ten identical copies and often invoked another worker's copy, so the run was scored as a miss.

Two checks confirmed this:

- **Recording the first tool call directly:** the skill fired first in 12 of 12 probes.
- **Rerunning with one worker:** results were 60 of 60 correct.

Two related lessons for test design:

- **Use self-contained trigger queries.** A query that points to a file that doesn't exist makes Claude go looking for the file first, which a strict "first tool call" check counts as a miss.
- **Isolate test environments.** A trigger test that runs a session to completion inherits whatever connected tools that environment has.

## Not yet tested

- **Real transcripts.** Next is 3–5 anonymized real TeAmour sessions, compared against the stories that were actually written from them.
- **Long transcripts.** These include 45–60 minute sessions with crosstalk and multiple facilitators.
- **The area list.** It is still a draft that the PM hasn't confirmed.
