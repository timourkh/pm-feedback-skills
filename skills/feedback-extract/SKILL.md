---
name: feedback-extract
description: Pull product feedback out of a raw stakeholder-demo or user-testing session (transcript, recording notes, or rough notes) and append it to the running feedback log, anonymized and tagged by app area, type and severity. Use this whenever the user hands over a demo, user test, usability session, customer call or co-founder/investor walkthrough and wants the feedback captured, logged, extracted or "processed" — even if they just say "here's today's demo, log it" or "pull the feedback out of this call". It is the first step of the feedback → triage → stories → tickets chain. Do not use it to summarize a meeting, write user stories directly, analyze trends across sessions, or process transcripts that aren't product feedback (sales calls, interviews, standups).
---

# Feedback extract

Turn one messy feedback session into clean, anonymized rows in a shared feedback log. This skill only *captures*. It does not decide what becomes a story, rank anything, or propose solutions. Those are later steps (triage, story writing), and they work well only if this step records faithfully what was said, by whom (pseudonymously), and how strongly.

The log is the memory of the whole process. Claude forgets between conversations, so "this has come up three times" is only knowable if every session lands in the same log in the same shape. Consistency of the rows matters more than eloquence.

## Inputs

- A session: transcript, auto-generated meeting notes, or the PM's rough notes. Expect noise: small talk, crosstalk, filler, the PM narrating while demoing.
- Session metadata, if not obvious from the input: date, session type (`stakeholder-demo` or `user-test`), build/version shown. Ask for the date and session type if you cannot tell. Everything else can be blank.
- The log location. Default: `feedback-log.csv` in the project/repo root, with the private name map at `participants.private.json` beside it. If the user has a different location, use theirs.

## The routine

1. **Read the whole session before extracting anything.** People circle back, revise and retract. An item mentioned early may be withdrawn twenty minutes later.

2. **Identify who is who.** Separate participants (the people giving feedback) from the facilitator (usually the PM running the demo or test). The facilitator's own remarks are not feedback. Log them only if a participant explicitly agrees with or adopts them, and then attribute the item to that participant.

3. **Extract feedback items.** One item = one distinct observation about the product from one participant. Keep:
   - problems they hit (bugs, crashes, wrong behavior),
   - friction or confusion (hesitation, wrong taps, "where do I...?", misreading a screen),
   - requests and suggestions,
   - questions that reveal a gap in understanding,
   - praise that is specific ("the match card is clear"), because knowing what works protects it from being "fixed".

   Leave out:
   - pleasantries, scheduling, and anything not about the product,
   - ideas the participant floated and then talked themselves out of in the same session (note the withdrawal, don't log the idea),
   - things already fixed or decided during the session, unless they still report the problem,
   - generic praise with nothing to act on ("looks great").

   Apply these rules evenly across participants. If you log one tester's short "that was easy" about a task, log the equivalent remark from the others too, because triage counts how many people said something and an uneven cut distorts that count.

   Answers to a facilitator's leading question ("Would you prefer a bigger button?" / "Sure, I guess") are not the participant's own request. Mention them in the paraphrase of the underlying problem if useful, but don't log them as a request.

   Observed behavior counts even when unspoken. If a tester taps the wrong button three times, that is friction even if they never complain. Mark it `observed` rather than `stated`.

4. **Merge repeats within the session.** If the same person raises the same point twice, it is one item (note "raised twice" in the paraphrase if the repetition signals strength). If two different people raise the same point, that is two items. Cross-person and cross-session counting is what triage relies on, so don't collapse different people into one row.

5. **Classify each item** using `references/log-schema.md` (fields and allowed values) and `references/app-areas.md` (the product's areas). If an item spans two areas, pick the one where the change would most likely land. If no area fits, use `other` and mention it in your summary so the area list can be updated.

6. **Severity is a hint, not a verdict.** Record what the session shows: `blocker` if the participant could not complete what they were doing, `major` for real frustration or a workaround, `minor` for small irritations or polish, `none` for praise and neutral questions. Triage decides priority later, so don't inflate.

7. **Flag ambiguity instead of resolving it.** When feedback could mean a small fix or a much bigger change ("adding friends should be easier"), log it faithfully and set `needs_clarification` to a short question for the PM ("copy tweak on the invite button, or a redesigned invite flow?"). Do not pick an interpretation. Guessing here is how a sprint goes in the wrong direction.

8. **Anonymize.** Follow `references/anonymization.md`. In short: real names never go into the log, the paraphrase, or the evidence. Participants get stable pseudonyms (`S-01` for stakeholders, `U-01` for users) through the private map, so the same person keeps the same label across sessions. Strip names of third parties people mention, and any personal details about them.

9. **Write the rows with the script.** Put the session metadata and items in a JSON file and run:

   ```bash
   python <skill-dir>/scripts/append_feedback.py --items items.json --log feedback-log.csv --map participants.private.json
   ```

   Run with `--dry-run` first if the log already has rows you haven't seen. The script assigns IDs and pseudonyms, validates every field, refuses rows that still contain a mapped real name, and prints a session summary. Using the script rather than editing the CSV by hand keeps IDs unique and the format identical across sessions, which triage depends on. If the script isn't available (e.g. in a chat without code execution), produce the rows as a CSV block in the exact column order from the schema and tell the user to paste them into the log.

10. **Report back briefly.** Tell the user:
    - how many items were logged, by type and area,
    - the `needs_clarification` questions, listed so they can answer them,
    - anything you deliberately left out that they might disagree with (a withdrawn idea, a facilitator suggestion),
    - any item marked `other` for area.

    Do not write user stories, priorities or solutions in this report. Offer triage as the next step if the log now has several sessions.

## Items JSON format (input to the script)

```json
{
  "session": {
    "date": "2026-10-03",
    "type": "stakeholder-demo",
    "build": "1.4.0 (Scout)",
    "source_ref": "demo-2026-10-03.txt"
  },
  "items": [
    {
      "participant": "Marina",
      "role": "stakeholder",
      "area": "invites",
      "type": "request",
      "basis": "stated",
      "severity_hint": "minor",
      "paraphrase": "Wants adding wingmen to be easier; unclear whether she means the button copy or the whole invite flow.",
      "evidence": "it should be easier to add friends",
      "needs_clarification": "Copy/placement tweak on the invite button, or a redesigned invite flow?"
    }
  ]
}
```

`participant` is the name or label as it appears in the session; the script swaps it for the pseudonym. Every other field is written in already-anonymized form.

## What good output looks like

- Every row is traceable: someone reading the evidence snippet could find the moment in the source.
- Nothing in the log identifies a real person.
- Different people saying the same thing produce separate rows; one person repeating themselves produces one.
- Ambiguous asks carry a question, not a guess.
- The summary to the user fits on one screen.
