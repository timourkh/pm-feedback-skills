# Feedback log schema

The log is a CSV file, one row per feedback item, appended session by session. Column order is fixed; the script enforces it.

| Column | Filled by | Allowed values / format | Notes |
|---|---|---|---|
| `id` | script | `FB-0001`, `FB-0002`, ... | Never reused, never edited. |
| `session_date` | Claude | `YYYY-MM-DD` | Date the session happened, not the date it was logged. |
| `session_type` | Claude | `stakeholder-demo`, `user-test` | Add new types here before using them. |
| `build` | Claude | free text | Version or build shown. Blank if unknown. |
| `source_ref` | Claude | free text | File name or link of the transcript, so rows can be traced back. |
| `participant` | script | `S-01`, `U-01`, ... | Pseudonym from the private map. Stakeholders `S-`, users `U-`. |
| `area` | Claude | see `app-areas.md` | One area per row. |
| `type` | Claude | `bug`, `friction`, `request`, `question`, `praise` | See definitions below. |
| `basis` | Claude | `stated`, `observed` | `observed` = behavior seen but not voiced. |
| `severity_hint` | Claude | `blocker`, `major`, `minor`, `none` | What the session shows, not a priority. |
| `paraphrase` | Claude | one or two sentences | Neutral restatement in third person. No real names. |
| `evidence` | Claude | short snippet, max ~25 words | Words from the source (anonymized) that support the row. |
| `needs_clarification` | Claude | short question, or blank | For asks that could mean a small fix or a bigger change. |
| `status` | script | `new` | Later steps change this to `triaged`, `promoted`, `parked`, `noise`. |
| `logged_at` | script | ISO timestamp | When the row was written. |

## Type definitions

- **bug**: the product did something wrong (crash, error, wrong data, broken screen).
- **friction**: the product works as built, but the participant struggled, hesitated, misread, or needed help.
- **request**: the participant asks for something new or different.
- **question**: the participant asks how something works, and the question itself reveals a gap (in the UI, the copy, or the concept).
- **praise**: a specific thing that works well and should be kept.

When a row could be two types, prefer the one closest to what happened: someone who couldn't find the invite button and then asked for a bigger one experienced *friction*; the request is their proposed fix and belongs in the paraphrase.

## Severity hints

- **blocker**: could not finish what they were trying to do.
- **major**: finished only with help or a workaround, or showed clear frustration.
- **minor**: small irritation, polish, wording.
- **none**: praise, neutral questions, ideas with no pain attached.
