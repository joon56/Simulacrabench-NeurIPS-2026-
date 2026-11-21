---
name: paper-session
description: One-paper study session protocol for the SimulacraBench domain reading list. Use when the user starts a paper study session — says "/paper-session", "논문 세션", "X 시작" naming a paper or a guide number like "3.2", or asks to study an entry from docs/domain-study-guide.ko.md.
---

# Paper study session protocol

One session = one paper (or one guide entry). The user reads; you structure,
answer, and close with a deliverable. Speak Korean unless asked otherwise
(technical terms, code, and paper titles stay in English).

## Source of truth

- Complete the repository entry reads and apply `docs/workflow.md` and the user's
  current scope. This shared protocol also serves the Codex skill wrapper.
- `docs/domain-study-guide.ko.md` — the entry's tier ([구현]/[설계]/[스킴]/[사전]),
  deliverable, and time box. The tier is the budget; do not exceed it.
- `docs/domain.md` — full bibliography and the competition-relevance rationale.
- The argument to this skill (or the user's first message) names the paper:
  a guide number ("3.2"), an author-year ("Guo 2017"), or a title fragment.

## Protocol

**1. Open (you, immediately, without being asked):**
- Identify the entry in the guide; state its tier and deliverable.
- Present a reading map of the PAPER'S OWN internal sections: which sections
  to read, which to skip, and why — specific to this paper, not generic.
  If you are not certain of the paper's internal section layout, fetch the
  paper (use the available web tool on the arXiv/DOI link from the guide) rather
  than guessing. Do not assume a tool named WebFetch exists in every agent.
- Give exactly 3 self-check questions the user should be able to answer
  after pass 2. Questions must be answerable from the assigned sections only
  and must connect to THIS competition (log-loss metric, NA_GATED, gates,
  hedging), not generic comprehension.

**2. During (guided, section by section):**
- Work through the assigned sections ONE AT A TIME, in reading-map order.
  The user is still building paper-reading skill — don't leave them alone
  with the map.
- Per section: (a) before the user reads it, give a DETAILED briefing — the
  user is new to this field, so teach, don't just point: explain each anchor
  concept/equation from scratch in plain language with a worked example,
  state what question the section answers, and what to skim past. A briefing
  that only lists terms is too short. (b) the user reads and asks questions —
  answer grounded in the paper's actual content, fetch it if needed, never
  bluff; (c) close the section with a 1–2 line "what you should have taken"
  check, then move to the next.
- The 3 self-check questions are NOT asked per section — they stay a single
  Q&A checkpoint after the whole reading map is done (start of the Close).
- Pace follows the user: they say when a section is done. Skipped sections
  get one line on why they're skippable, not a briefing.
- If a question reveals the reading map was wrong (e.g. the method is in a
  different section), say so and correct the map.

**3. Close (when the user says they're done reading, or asks to wrap up):**
- Ask the 3 self-check questions if the user hasn't addressed them; brief
  discussion of gaps. Keep it short — this is a check, not an exam.
- Produce the deliverable together, per tier:
  - [구현]: within the user's authorized implementation scope, draft the code
    (location per the guide, e.g. `src/eval/`) and run scoped permitted checks.
    If fit/score or data access is outside scope, hand off the implementation
    and missing validation; do not label it verified or start the harness.
  - [설계]: write the design-decision note (3–5 lines) destined for the
    experiment file or guide entry it feeds.
  - [스킴]: 3-line summary only.
- Record completion in `docs/domain-study-guide.ko.md`: prefix the entry's
  first line with `✅ (YYYY-MM-DD)` and append a 3-line `요약:` block the user
  agrees with (their words preferred over yours).
- Commit/push only when authorized by the active user scope. When a commit is
  authorized, use `study: <guide-id> <short-title> — <deliverable>` in English.
  Neither finishing a paper nor end of day grants git authorization.

## Rules

- One paper per session. If the user tries to chain a second paper, suggest
  a fresh session (context quality drops).
- Tier discipline: never turn a [스킴] into a deep read. A [구현] deliverable
  without permitted execution remains unvalidated, with the missing check named.
- If the paper contradicts something in `docs/domain.md` or the guide,
  flag it and update the doc — the reading list must stay honest.
- An experiment idea surfacing mid-session goes into the experiment queue
  (mention it in the close, suggest an E0XX), not into scope creep now.
