I started a new `feedback-log.csv` and logged **13 items (FB-0001 to FB-0013)** from your two moderated user tests on Sep 11 (build 1.4.1, captured_by `tee`). The testers are now **U-01** (Session A) and **U-02** (Session B). Their real names are only in `participants.private.json`, and I added that file to `.gitignore`.

**By type:** 4 praise, 4 friction, 2 request, 2 demand, 1 bug
**By area:** scout 3, onboarding 2, invites 2, chat 2, positioning 2, team 1, matches 1

**Most severe items**
- **Blocker (FB-0008):** U-02's verification code never arrived, even after waiting about 90 seconds, tapping resend and trying again. He said he'd delete the app. You logged him in with a test account so he could continue. U-01's code arrived without trouble, and I logged that as praise (FB-0001).
- **Major (FB-0002):** U-01 couldn't find the wingman invite. She spent about 40 seconds in settings and her profile and thought the small plus was for adding photos. U-02 had the same problem without saying anything: he went Matches, back, Matches, Chat, back before he found the plus. I logged his as a separate **observed** row (FB-0009) and marked it minor because he showed no frustration.
- **Major (FB-0004):** On the Scout suggestions screen, U-01 couldn't tell whether she was the candidate or a wingman, and you had to tell her.

**Questions to answer before triage**
- FB-0004: Should the role label appear only on the Scout suggestions screen, or should the candidate/wingman role show throughout the app?
- FB-0005: Is the dealbreaker request a preference field that only Scout reads, or should those preferences also be shown to wingmen when they suggest matches?
- FB-0010: Does "only three, I'd want to scroll" mean more suggestions per batch, or a continuous scrollable feed?
- FB-0011: Was "same template / Loves travel" about the wording of the suggestion summaries, or about the suggested people being too similar?

**Choices you might disagree with**
- **Leading question left out:** U-01's "Uh, sure, I guess" to "Would you prefer a bigger button?" is not logged as a request. It's mentioned only in the invite friction row.
- **Personal details removed:**
  - U-01's religion. Her row (FB-0005) is now a general request to tell Scout and wingmen about a core dealbreaker.
  - The full name of the friend she would invite.
  - The detail about U-02's sister's divorce. His row (FB-0013) says a family member who distrusts dating apps would use it.
- **Demand signals:** I logged "who I'd invite" (U-01) and "my sister would use this" (U-02) as positive demand under `positioning`. Both are weak signals.
- **Praise rows:** I logged "easy" or "fast" praise for chat from both testers so the count is even.
- **Severity:** Severity is my reading of the session, not a priority.

No items went into the `other` area. Once you have another session or two logged, triage is the next step.
