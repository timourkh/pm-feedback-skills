I added 7 rows from the Oct 17 demo (build 1.4.2) to `feedback-log.csv` as FB-0015 to FB-0021. Rows FB-0001 to FB-0014 are unchanged.

**What was logged**
- **FB-0015 (Marina, invites, friction, minor):** she still can't find how to add friends. She raised this in FB-0001 and it isn't in 1.4.2.
- **FB-0016 (Dmitri, metrics, question):** he asked about week-one retention. You told him it's too early to say.
- **FB-0017 (Dmitri, onboarding, friction, minor):** the first screen doesn't show how this is different from Hinge. He wants to see it, not read it. Marina agreed.
- **FB-0018 (Marina, scout, praise):** with the new 8-question interview, Scout's suggestions sound like the person. This answers her FB-0002 complaint.
- **FB-0019 (Dmitri, scout, request, minor):** Scout is the interesting part and he'd lead with it.
- **FB-0020 (Dmitri, notifications, friction, major):** the push notification asking a wingman to do a Scout interview has no context. He said he wouldn't open it.
- **FB-0021 (Marina, notifications, praise):** the chat unread badge now clears, so the FB-0005 bug is fixed.

**Choices I made**
- **"Mar" is Marina (S-01).** I added "Mar" to her aliases in `participants.private.json`.
- **Dmitri is the new participant S-02**, with the role "investor". I kept his real name only in the private file, like everyone else.
- **I added a new area, `metrics`, for the retention question.** None of the existing areas fit. You could also leave it out because it's not product feedback.
- **I rated FB-0020 as major.** The notification is how wingmen get pulled into Scout, and Dmitri said outright he wouldn't open it.
- **FB-0019 has a note in `needs_clarification`.** It's unclear whether he meant leading with Scout in the app's first screen or in the pitch. If it's the app, it ties in with FB-0017.
- **The two praise rows that close out earlier items reference them** (FB-0018 to FB-0002, FB-0021 to FB-0005). I didn't change the status of the old rows.
- **What I left out:** small talk, "Send me the deck", and "That's a good point" (counted as Marina agreeing in FB-0017 rather than its own row).
- **`logged_at` is today's real time (Oct 7).** The session date is Oct 17 as you gave it, which is in the future. If that's a typo, the `session_date` on these 7 rows needs fixing.

Dmitri asked for the deck, so that's a follow-up for you.
