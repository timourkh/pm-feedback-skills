---
name: feedback-extract
description: Pull product and market feedback out of a raw session — stakeholder demo, user/usability test, or GTM prospect research (demand interviews, message or landing-page tests, waitlist follow-ups) — given as a transcript, meeting notes or rough notes, and append it to the team's shared feedback log, anonymized and tagged by area, type and severity. Use this whenever someone hands over such a session (their own or a teammate's) and wants the feedback captured, logged, extracted or "processed" — even if they just say "here's today's demo, log it" or "log Nadia's prospect calls". It is the first step of the feedback → triage → stories → tickets chain. Do not use it to summarize a meeting, write user stories or tickets, analyze trends across already-logged sessions, write interview scripts or surveys, or process transcripts that aren't feedback (sales calls, job interviews, standups).
---

# Feedback extract

Turn one messy feedback session into clean, anonymized rows in a shared feedback log. This skill only *captures*. It does not decide what becomes a story, rank anything, or propose solutions. Those are later steps (triage, story writing), and they work well only if this step records faithfully what was said, by whom (pseudonymously), and how strongly.

Several people feed the same log: whoever runs stakeholder demos, whoever runs usability tests, whoever runs go-to-market research with prospects. Their notes arrive in different shapes and at different fidelity. The log is where that difference disappears: one row per observation, the same categories, the same severity scale, the same anonymization, no matter who captured it. The person who builds from the log can then compare a prospect's objection with a tester's struggle as two rows about the same thing. Claude forgets between conversations, so "this has come up three times" is only knowable if every session lands in the same log in the same shape. Consistency of the rows matters more than eloquence.

## Inputs

- A session: transcript, auto-generated meeting notes, or someone's rough notes. Expect noise: small talk, crosstalk, filler, a facilitator narrating or pitching.
- Session metadata, if not obvious from the input:
  - date,
  - session type: `stakeholder-demo`, `user-test`, or `prospect-research`,
  - build or version shown (blank for prospect research without a build),
  - **captured_by**: the team member who ran the session or took the notes.

  The person handing you the file is not necessarily the one who ran the session ("here are Nadia's notes from Friday"). Ask for date, session type and who captured it if you can't tell. If nobody can answer, use `unknown` for captured_by and say so.
- The log location. Default: `feedback-log.csv` in the project/repo root, with the private name map at `participants.private.json` beside it. If the user has a different location, use theirs.

## The routine

1. **Read the whole session before extracting anything.** People circle back, revise and retract. An item mentioned early may be withdrawn twenty minutes later.

2. **Identify who is who.** Separate participants (the people giving feedback) from the facilitator (whoever ran the demo, test or interview; often not the person logging it). The facilitator's own remarks are not feedback. Log them only if a participant explicitly agrees with or adopts them, and then attribute the item to that participant. Participants have one of three roles:
   - `stakeholder`: co-founders, investors, internal reviewers,
   - `user`: people testing or using the product,
   - `prospect`: people who are not users yet (GTM interviews, message tests, waitlist sign-ups).

3. **Extract feedback items.** One item = one distinct observation from one participant. Keep:
   - problems they hit (bugs, crashes, wrong behavior),
   - friction or confusion (hesitation, wrong taps, "where do I...?", misreading a screen or a message),
   - requests and suggestions,
   - questions that reveal a gap in understanding,
   - demand signals: whether and why they would or wouldn't use, pay for, or recommend it, and their objections ("my friends are too busy for this"),
   - praise that is specific ("the match card is clear"), because knowing what works protects it from being "fixed".

   Leave out:
   - pleasantries, scheduling, and anything not about the product or its market,
   - ideas the participant floated and then talked themselves out of in the same session (note the withdrawal, don't log the idea),
   - things already fixed or decided during the session, unless they still report the problem,
   - generic praise with nothing to act on ("looks great"),
   - business questions aimed at the team rather than reactions to the product (an investor asking about retention numbers).

   Apply these rules evenly across participants. If you log one tester's short "that was easy" about a task, log the equivalent remark from the others too, because triage counts how many people said something and an uneven cut distorts that count.

   Agreement the facilitator led someone into is weak evidence. Examples are an answer to a leading question ("Would you prefer a bigger button?" / "Sure, I guess") or polite assent after a pitch ("Yeah, sounds cool"). Don't log these as the participant's own request or as demand. Mention them in the paraphrase of a related item if useful, or skip them. This matters most in prospect research, where a warm reaction to a pitch is easy to mistake for demand.

   Observed behavior counts even when unspoken. If a tester taps the wrong button three times, that is friction even if they never complain. Mark it `observed` rather than `stated`.

   Low-fidelity input is fine. Bullet notes give thinner rows than a full transcript. Record what is there; don't pad it or invent context. When notes don't say whether something was the participant's view or the note-taker's, say so in the paraphrase ("per the interviewer's notes").

4. **Merge repeats within the session.** If the same person raises the same point twice, it is one item (note "raised twice" in the paraphrase if the repetition signals strength). If two different people raise the same point, that is two items. Cross-person and cross-session counting is what triage relies on, so don't collapse different people into one row.

5. **Classify each item** using `references/log-schema.md` (fields and allowed values) and `references/app-areas.md` (areas). If an item spans two areas, pick the one where the change would most likely land. Use `positioning` for reactions to the concept, value proposition, differentiation and messaging, inside or outside the app. If no area fits, use `other` and mention it in your summary so the area list can be updated.

6. **Severity is a hint, not a verdict.** Record what the session shows, using the definitions in the schema. In short:
   - `blocker`: could not complete what they were doing, or a prospect says this would stop them signing up or using it,
   - `major`: real frustration, a workaround, or a strong objection,
   - `minor`: small irritations, polish, mild doubts,
   - `none`: praise, neutral questions, positive demand signals.

   Triage decides priority later, so don't inflate.

7. **Flag ambiguity instead of resolving it.** When feedback could mean a small fix or a much bigger change ("adding friends should be easier"), log it faithfully and set `needs_clarification` to a short question ("copy tweak on the invite button, or a redesigned invite flow?"). Do not pick an interpretation. Guessing here is how a sprint goes in the wrong direction. If the person logging didn't run the session, frame the question so they can pass it to whoever did.

8. **Anonymize.** Follow `references/anonymization.md`. In short: real names never go into the log, the paraphrase, or the evidence. Participants get stable pseudonyms (`S-01` stakeholders, `U-01` users, `P-01` prospects) through the private map, so the same person keeps the same label across sessions and across teammates. Strip names of third parties people mention, and personal details about anyone (age, relationship history, health, religion and the like). Prospect and matchmaking conversations invite these.

9. **Write the rows with the script.** Put the session metadata and items in a JSON file and run:

   ```bash
   python <skill-dir>/scripts/append_feedback.py --items items.json --log feedback-log.csv --map participants.private.json
   ```

   - Run with `--dry-run` first if the log already has rows you haven't seen.
   - If the script reports the log is in the older format without `captured_by`, rerun with `--migrate`. It adds the column (blank for old rows) and keeps every existing row.
   - The script assigns IDs and pseudonyms, validates every field, refuses rows that still contain a mapped real name, and prints a session summary.

   Using the script rather than editing the CSV by hand keeps IDs unique and the format identical across sessions and people, which triage depends on. If the script isn't available (e.g. in a chat without code execution), produce the rows as a CSV block in the exact column order from the schema and tell the user to paste them into the log.

10. **Report back briefly** to the person who asked:
    - how many items were logged, by type and area, and whose session it was (captured_by),
    - the `needs_clarification` questions, listed so they can answer them or forward them to whoever ran the session,
    - anything you deliberately left out that they might disagree with (a withdrawn idea, a facilitator suggestion, pitched agreement),
    - any item marked `other` for area.

    Do not write user stories, priorities or solutions in this report. Offer triage as the next step if the log now has several sessions.

## Items JSON format (input to the script)

```json
{
  "session": {
    "date": "2026-10-03",
    "type": "prospect-research",
    "build": "",
    "source_ref": "prospect-calls-2026-10-03.md",
    "captured_by": "nadia"
  },
  "items": [
    {
      "participant": "Prospect 2",
      "role": "prospect",
      "area": "positioning",
      "type": "demand",
      "basis": "stated",
      "severity_hint": "major",
      "paraphrase": "Doubts friends would put in the effort to act as wingmen; sees it as the main reason she wouldn't sign up.",
      "evidence": "would my friends actually do this? they're all busy",
      "needs_clarification": ""
    }
  ]
}
```

`participant` is the name or label as it appears in the session; the script swaps it for the pseudonym. `captured_by` is a short team handle (first name or role, e.g. `tee`, `ux`, `gtm`), not a participant. Every other field is written in already-anonymized form.

## What good output looks like

- Every row is traceable: someone reading the evidence snippet could find the moment in the source, and `captured_by` says whose session it came from.
- Nothing in the log identifies a participant.
- Different people saying the same thing produce separate rows; one person repeating themselves produces one.
- Rows from a usability test, a demo and a prospect call about the same problem share an area and read as comparable.
- Ambiguous asks carry a question, not a guess.
- The summary fits on one screen.
