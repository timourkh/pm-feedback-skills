# Anonymization rules

The feedback log is meant to live in a repo and be read by whoever works on the backlog, so it must not identify anyone. The private name map is the only place real names exist, and it stays out of version control.

## Participants

- Every participant gets a stable pseudonym from `participants.private.json`: `S-01`, `S-02`... for stakeholders (co-founders, investors, internal reviewers), `U-01`, `U-02`... for users and testers, `P-01`, `P-02`... for prospects in GTM research.
- The map is shared by everyone who logs feedback, so a prospect who later becomes a tester keeps one identity. In that case, add the tester's name as an alias of the existing `P-` entry rather than creating a new `U-` label, and mention it in your report.
- The script assigns these. Pass the name as it appears in the session in the `participant` field; the script looks it up or creates the next label.
- If the same person appears under two spellings or a nickname ("Mike" / "Michael"), add the variant as an alias in the map so they keep one label. Ask the user if you are unsure whether two names are the same person, because merging two people would inflate one person into a "trend" and splitting one person would hide a repeat.
- If a session only labels people generically ("Tester 2"), use that label as the name. It still goes through the map.

## Inside the text fields

Apply to `paraphrase`, `evidence` and `needs_clarification`:

- Replace participants' names with their pseudonym or with "the participant".
- Remove names of anyone else mentioned (a friend, an ex, a colleague): use "a friend", "her sister", etc.
- Remove contact details, exact addresses, workplaces, schools, and anything else that would identify a person.
- Remove sensitive personal details people share in passing (age, health, relationship history, religion and similar). Matchmaking sessions and prospect interviews invite this. If the detail matters to the feedback, generalize it: "wants to filter by a lifestyle preference" rather than the specific preference tied to the person.
- Keep product facts: screens, buttons, flows, numbers, error messages, prices mentioned.

## Team members

`captured_by` holds a short handle for the teammate who ran the session (`tee`, `ux`, `gtm`). Teammates are not participants and don't go in the private map. Their remarks during a session are facilitator remarks, not feedback.

## The map file

`participants.private.json` looks like:

```json
{
  "S-01": {"name": "Marina", "aliases": ["Mar"], "role": "stakeholder"},
  "U-01": {"name": "Tester 1", "aliases": [], "role": "user"}
}
```

Add it to `.gitignore`. The script refuses to write a row whose text fields contain any name or alias from the map, as a last line of defence. It cannot catch names that are not in the map (third parties), so those depend on the rules above.
