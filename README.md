# pm-feedback

Claude skills for turning product feedback into backlog work, built for the TeAmour team: a builder PM who implements with Claude Code, a UX designer running usability tests, and a GTM lead running prospect research. They all feed one backlog.

## The problem

Feedback reaches the backlog from three directions:

- stakeholder demos (the PM, every two weeks),
- usability tests (UX),
- prospect interviews, message tests and waitlist follow-ups (GTM).

Each person used to paste their notes into Claude and ask for a summary or stories, each in their own way. That broke down in four places:

- **Nothing accumulated or connected.** A complaint four people raised across three sessions looked the same as a one-off remark. A prospect's objection and a tester's struggle with the same screen never met.
- **Every person's output had a different shape.** The builder PM, who turns the backlog into code, had to reconcile three formats before building anything.
- **Claude filled gaps silently.** Some guesses were real product decisions (scope, roles, monetization) that a person should have made.
- **Names and personal details leaked.** Matchmaking and dating-prospect conversations are full of them, and they ended up in working notes.

The skill doesn't make Claude smarter about feedback; a strong model already makes most single-session calls well (see the evals). What it adds is one gate everyone passes through. Messy input of any shape and fidelity goes in. What comes out is always the same five things:

- one row per observation,
- the same categories,
- the same severity scale,
- the same anonymization,
- a question instead of a guess on real decisions.

## The design

Capture is distributed and consumption is centralized. Anyone on the team logs a session the moment it's done; the builder PM reads the accumulated log once a sprint. The pipeline is four small skills rather than one big one. Each step has its own trigger, its own output and its own test, and a running log carries state between sessions, because Claude has no memory between conversations.

```
demo notes  (PM)  ─┐
usability notes (UX) ─┼─▶ feedback-extract ─▶ feedback-log.csv ─▶ feedback-triage ─▶ story-writer ─▶ ticket-breakdown
prospect notes (GTM) ─┘    (this repo)          (shared state)       (planned)          (planned)        (planned)
                                                                      ▲ builder PM         ▲ builder PM answers
                                                                        approves promos      must-ask questions
```

Each step's job:

- **feedback-extract:** captures feedback faithfully. One row per observation per person, anonymized, tagged by area, type and severity. Ambiguous asks get a question for the PM instead of a guess.
- **feedback-triage:** reads the whole log and sorts themes into promote, watch or noise, weighing recurrence, severity and reach.
- **story-writer:** writes stories in house format and separates safe assumptions from decisions the PM must make.
- **ticket-breakdown:** splits signed-off stories into engineering tickets and creates them in GitHub.

## What ships now: `feedback-extract` (v0.2)

```
skills/feedback-extract/
├── SKILL.md                    the routine and what to keep or leave out
├── references/
│   ├── log-schema.md           log columns, allowed values, type and severity definitions
│   ├── app-areas.md            product areas (one per row; triage counts by area)
│   └── anonymization.md        pseudonyms (S-/U-/P-), third parties, sensitive details, team handles
├── scripts/
│   └── append_feedback.py      writes rows: IDs, pseudonyms, captured_by, validation, name-leak check, v0.1 migration
└── evals/
    ├── evals.json              4 output tests, 40 assertions
    ├── trigger-evals.json      24 trigger tests (12 should fire, 12 near-misses)
    └── files/                  synthetic transcripts and notes with planted traps
```

Judgement stays in the instructions. Mechanics live in the script:

- **Claude decides** what counts as feedback, who said it, how to classify it, and when to ask instead of guess.
- **The script enforces** column order, unique IDs, stable pseudonyms across sessions and teammates, who captured each session, allowed values, and a hard stop if a known real name is still in the text.

## How it was tested

See [docs/eval-results.md](docs/eval-results.md). In short:

- **Output tests (v0.1):** 3 synthetic sessions with planted traps, each run with the skill and without it. With the skill: 27/27 assertions. Without it, the same model scored 20/27. The baseline misses were:
  - inconsistent schema,
  - real names in the log,
  - a religious detail kept,
  - a business question logged as product feedback,
  - ambiguous asks resolved by guessing.
- **Team version (v0.2):** a fourth test logs a GTM teammate's low-fidelity prospect-call notes into the existing log. With the skill: 10/10. Without it: 6/10. The baseline invented its own session type and feedback types, recorded nobody as the capturer, and left the log in a different shape from everyone else's. All earlier tests still pass after the changes (30/30). Overall: 40/40.
- **Iteration:** round 1 exposed uneven treatment of short remarks between participants. The fix ("apply rules evenly; pitched or leading-question agreement isn't a request or demand") held in later rounds.
- **Triggering:** 24 queries, 3 runs each, with 72/72 correct. They include GTM queries and near-misses like "write a demand interview script" and "turn these findings into a GTM memo". The results doc also covers a harness pitfall I hit and how I confirmed it.

## Install

Team members add the marketplace once, then install the plugin:

```
/plugin marketplace add <git-url-of-this-repo>
/plugin install pm-feedback@tkthrive-pm-skills
```

Updates ship by bumping `version` in `.claude-plugin/plugin.json` and the marketplace entry, tagging the release (`claude plugin tag`), and having teammates run `/plugin update`.

For the Claude apps, `skills/feedback-extract/` can be zipped and uploaded as a skill, or provisioned by an org admin.

## Using it

1. Put the log at your project root (or tell Claude where it is). The first run creates `feedback-log.csv` and `participants.private.json`.
2. Keep `participants.private.json` out of version control. It's the only place real names exist.
3. After a session, anyone on the team pastes the transcript or notes, or points to the file, and says something like "log the feedback from today's demo" or "log Nadia's prospect calls". No format is required. Say who ran the session if it wasn't you; it's recorded as `captured_by`.
4. Answer the clarification questions Claude lists, or forward them to whoever ran the session. Those answers are what the story step needs.
5. Upgrading from v0.1: the first run on an old log upgrades it (`--migrate`). It adds the `captured_by` column and keeps every row.

## Conventions for adding skills

- **One skill = one step** with one trigger. Name it `<noun>-<verb>`, for example `feedback-extract` or `feedback-triage`.
- **Every skill ships with `evals/`:** output tests with assertions, plus a trigger set whose near-misses share keywords with the skill.
- **Deterministic work goes in `scripts/`.** Long reference material goes in `references/` and is loaded only when needed.
- **Bump the version and update `CHANGELOG.md`** with every behavior change. Re-run the evals before merging.
