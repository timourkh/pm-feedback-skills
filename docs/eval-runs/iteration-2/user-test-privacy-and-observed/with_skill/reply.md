I logged 11 items from the two Sep 11 user tests (build 1.4.1) as FB-0001 to FB-0011. They're in a new `feedback-log.csv`. The two testers are U-01 and U-02, and their real names are only in `participants.private.json`. Keep that file out of the repo.

**By type:** 4 praise, 3 friction, 2 requests, 1 question, 1 bug.
**By area:** 3 scout, 2 onboarding, 2 invites, 2 chat, 1 team, 1 matches. No item needed the `other` area.

**Most serious**
- **FB-0007 (blocker):** U-02's verification code never arrived, even after waiting and resending twice. He couldn't sign up and said he'd delete the app. You had to log him in with a test account.
- **FB-0002 (major):** U-01 couldn't find how to invite a wingman. She took the small plus at the top for an "add photos" button.
- **FB-0008 (minor):** U-02 had the same invite trouble but never said anything. He went through Matches twice and then Chat before finding the plus. I logged this as `observed`, not `stated`.

**Questions for you (logged as asked, I didn't pick an answer)**
1. **FB-0003:** Should the "am I the candidate or the wingman?" label appear only on the Scout screen, or everywhere in the team space?
2. **FB-0004:** Should a candidate's personal preference be an instruction to Scout only, a preference all wingmen can see, or a hard match filter?
3. **FB-0009:** By "only three, I'd want to scroll," does U-02 mean more suggestions per batch or a feed he can keep scrolling?
4. **FB-0010:** Is the "same template" complaint about how Scout words its summaries, or about the prospects themselves being too alike?

**Choices I made that you might disagree with**
- **No "bigger invite button" request.** U-01 only said "sure, I guess" when you asked if she'd prefer one. I mentioned that in the friction row and didn't log it as her request.
- **Personal details removed.** The friend U-01 named, U-01's religion and U-02's comment about his sister's divorce aren't in the log. FB-0004 calls it "a personal preference" so the request still makes sense without the detail. Nothing was logged from the sister comment, since it says nothing about the product.
- **Short "easy" and "done" remarks logged for both testers.** That's 2 chat-praise rows plus U-01's easy sign-up. Triage can count them evenly, and U-02 had no sign-up praise because his sign-up failed.
- **Severity calls:** I marked U-01's invite trouble `major` because she struggled for about 40 seconds and said she couldn't find it. U-02's silent detour is `minor`.
- **Area list is still a draft.** `references/app-areas.md` is a first version you haven't confirmed yet. The role-confusion question went under `team`.

Once one or two more sessions are logged, I can run triage on the log.
