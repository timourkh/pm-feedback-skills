I've added Nadia's two prospect calls to the log as **FB-0015 to FB-0024** (10 rows). Both prospects are in `participants.private.json` as **P-01** (Rachel K.) and **P-02** (Jordan). The CSV itself has no names in it.

**What came out of the calls**
- **Friends not taking part is the biggest risk (FB-0016, major).** Rachel came back to it twice: "Nobody's going to fill out a questionnaire for me." Her ~$10/mo only holds "if my friends actually showed up for it" (FB-0017). Jordan's question about whether friends can help by text instead of installing the app is the same worry (FB-0023).
- **Adding a friend is hard to find, again (FB-0018, major).** Rachel ended up in settings and only found the + after Nadia pointed her to it. That's the third session in a row with this problem, after FB-0001, FB-0006 and FB-0011.
- **The headline isn't landing (FB-0020, major).** Jordan couldn't see how it differs from Hinge until the wingman part was explained. To him, "Date with your friends' help" sounded like a group chat.
- **Things that worked:** Rachel understood the idea right away (FB-0015). She called the friend vouching "the safety thing for me" (FB-0019). Jordan said the match card makes sense (FB-0024).
- **Matches (FB-0022):** Jordan wants to see which friend suggested a match, or "it's just another algorithm." The card already shows this, so I logged it as support for the current design rather than a new request.
- **Weak signal on Scout (FB-0021):** Jordan said "sounds cool, I'd try it" after a 3-minute verbal pitch and asked nothing else. I marked it as unvalidated interest.

**Choices I made**
- **Date:** I used 2026-09-26. Sep 26 2026 is actually a Saturday, not a Friday. Tell me if the calls were on Fri Sep 25 and I'll change the date on all 10 rows.
- **Session details:** session type is `prospect-interview`, a new value. The build is "clickable prototype" because the notes don't give a version number.
- **New values:** I added the area `positioning` and two types, `concern` and `signal`. The existing types (friction, praise, request, question, bug) didn't fit doubts about the product's value or pricing interest. If you'd rather keep the original list, I can map them back.
- **How quotes are marked:** these are Nadia's notes, not a transcript. Evidence is a direct quote only where she recorded one. Otherwise it's marked `[notes]`. Things Nadia saw them do are marked `observed`.
- **Left out on purpose:**
  - Rachel's age and marital history, which are personal and not product feedback.
  - Jordan's "uses Hinge, it's fine," which is background.
  - The waitlist A/B test and Nadia's own idea to lead onboarding with vouching/safety. Those are her observations, not prospect feedback. Worth passing to whoever owns onboarding and messaging.
- **Open questions:** five rows have notes in `needs_clarification` to check with Nadia. For example: does the wingman flow actually include a questionnaire, and did Jordan try adding a friend?
