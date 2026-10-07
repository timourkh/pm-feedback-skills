# Feedback log schema (v2)

The log is a CSV file, one row per feedback item, appended session by session by everyone on the team. Column order is fixed; the script enforces it.

| Column | Filled by | Allowed values / format | Notes |
|---|---|---|---|
| `id` | script | `FB-0001`, `FB-0002`, ... | Never reused, never edited. |
| `session_date` | Claude | `YYYY-MM-DD` | Date the session happened, not the date it was logged. |
| `session_type` | Claude | `stakeholder-demo`, `user-test`, `prospect-research` | Add new types here (and in the script) before using them. |
| `build` | Claude | free text | Version or build shown. Blank if none (common for prospect research). |
| `source_ref` | Claude | free text | File name or link of the transcript/notes, so rows can be traced back. |
| `captured_by` | Claude | short team handle, or `unknown` | Who ran the session or took the notes, e.g. `tee`, `ux`, `gtm`. Not a participant. |
| `participant` | script | `S-01`, `U-01`, `P-01`, ... | Pseudonym from the private map: `S-` stakeholders, `U-` users, `P-` prospects. |
| `area` | Claude | see `app-areas.md` | One area per row. |
| `type` | Claude | `bug`, `friction`, `request`, `question`, `demand`, `praise` | See definitions below. |
| `basis` | Claude | `stated`, `observed` | `observed` = behavior seen but not voiced. |
| `severity_hint` | Claude | `blocker`, `major`, `minor`, `none` | What the session shows, not a priority. |
| `paraphrase` | Claude | one or two sentences | Neutral restatement in third person. No real names. |
| `evidence` | Claude | short snippet, max ~25 words | Words from the source (anonymized) that support the row. |
| `needs_clarification` | Claude | short question, or blank | For asks that could mean a small fix or a bigger change. |
| `status` | script | `new` | Later steps change this to `triaged`, `promoted`, `parked`, `noise`. |
| `logged_at` | script | ISO timestamp | When the row was written. |

Logs written by v0.1 of this skill have no `captured_by` column. Run the script once with `--migrate` to upgrade them; old rows get a blank `captured_by`.

## Type definitions

- **bug**: the product did something wrong (crash, error, wrong data, broken screen).
- **friction**: the product or message works as built, but the participant struggled, hesitated, misread, or needed help.
- **request**: the participant asks for something new or different.
- **question**: the participant asks how something works, and the question itself reveals a gap (in the UI, the copy, or the concept).
- **demand**: a signal about whether the participant would use, pay for, recommend or sign up, or why not. Includes objections ("my friends wouldn't bother"), willingness to pay, and who they'd use it with. Mostly from prospect research, but users and stakeholders can give demand signals too.
- **praise**: a specific thing that works well and should be kept.

When a row could be two types, prefer the one closest to what happened: someone who couldn't find the invite button and then asked for a bigger one experienced *friction*; the request is their proposed fix and belongs in the paraphrase. A prospect who "doesn't get how it's different from Hinge" is *friction* in `positioning`; one who says "so I wouldn't switch" is *demand*.

## Severity hints

- **blocker**: could not finish what they were trying to do; or, for prospects, says this would stop them signing up or using it.
- **major**: finished only with help or a workaround, showed clear frustration, or raised a strong objection.
- **minor**: small irritation, polish, wording, mild doubt.
- **none**: praise, neutral questions, positive demand signals, ideas with no pain attached.
