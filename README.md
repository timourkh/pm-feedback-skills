# pm-feedback

Claude skills for turning product feedback into backlog work, built around how I run TeAmour: a solo-built consumer app with a bi-weekly demo to my co-founder/investor and regular moderated user tests.

## The problem

Every two weeks I come out of a demo or a test session with a messy transcript. I used to paste it into Claude and ask for user stories. That worked, but:

- **Nothing accumulated.** Each session was processed on its own, so a complaint raised by four people across three sessions looked the same as a one-off remark.
- **Claude filled gaps silently.** Some of those guesses were real product decisions (scope, roles, monetization) that I should have made.
- **Format drifted** from session to session, so the output couldn't feed anything downstream.
- **Real names and personal details** from matchmaking test sessions ended up in working notes.

## The design

The pipeline is four small skills rather than one big one. Each step has its own trigger, its own output and its own test, and a running log carries state between sessions, because Claude has no memory between conversations.

```
transcript ─▶ feedback-extract ─▶ feedback-log.csv ─▶ feedback-triage ─▶ story-writer ─▶ ticket-breakdown
               (v0.1, this repo)    (shared state)       (planned)          (planned)        (planned)
                                                         ▲ PM approves       ▲ PM answers
                                                           what's promoted     must-ask questions
```

Each step's job:

- **feedback-extract:** captures feedback faithfully. One row per observation per person, anonymized, tagged by area, type and severity. Ambiguous asks get a question for the PM instead of a guess.
- **feedback-triage:** reads the whole log and sorts themes into promote, watch or noise, weighing recurrence, severity and reach.
- **story-writer:** writes stories in house format and separates safe assumptions from decisions the PM must make.
- **ticket-breakdown:** splits signed-off stories into engineering tickets and creates them in GitHub.

## What's in v0.1: `feedback-extract`

```
skills/feedback-extract/
├── SKILL.md                    the routine and what to keep or leave out
├── references/
│   ├── log-schema.md           log columns, allowed values, type and severity definitions
│   ├── app-areas.md            product areas (one per row; triage counts by area)
│   └── anonymization.md        pseudonyms, third parties, sensitive details
├── scripts/
│   └── append_feedback.py      writes rows: IDs, pseudonyms, validation, name-leak check
└── evals/
    ├── evals.json              3 output tests, 27 assertions
    ├── trigger-evals.json      20 trigger tests (10 should fire, 10 near-misses)
    └── files/                  synthetic transcripts with planted traps
```

Judgement stays in the instructions. Mechanics live in the script:

- **Claude decides** what counts as feedback, who said it, how to classify it, and when to ask instead of guess.
- **The script enforces** column order, unique IDs, stable pseudonyms across sessions, allowed values, and a hard stop if a known real name is still in the text.

## How it was tested

See [docs/eval-results.md](docs/eval-results.md). In short:

- **Output tests:** 3 synthetic sessions with planted traps, each run with the skill and without it. The skill passed 27/27 assertions; the same model without the skill passed 20/27. The misses were inconsistent schema, real names in the log, a religious detail kept, a business question logged as product feedback, and ambiguous asks resolved by guessing instead of asking.
- **Iteration:** round 1 exposed uneven treatment of short remarks between participants. The fix ("apply rules evenly; leading-question answers aren't requests") held in round 2.
- **Triggering:** 20 queries, including near-misses like "summarize this standup" and "turn these promoted items into stories". Results and a note on a harness pitfall are in the results doc.

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
3. After a session, paste the transcript or point to the file and say something like "log the feedback from today's demo".
4. Answer the clarification questions Claude lists. Those answers are what the story step needs.

## Conventions for adding skills

- **One skill = one step** with one trigger. Name it `<noun>-<verb>`, for example `feedback-extract` or `feedback-triage`.
- **Every skill ships with `evals/`:** output tests with assertions, plus a trigger set whose near-misses share keywords with the skill.
- **Deterministic work goes in `scripts/`.** Long reference material goes in `references/` and is loaded only when needed.
- **Bump the version and update `CHANGELOG.md`** with every behavior change. Re-run the evals before merging.
