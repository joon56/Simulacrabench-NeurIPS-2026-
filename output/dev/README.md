# DEV research archive

**E041.zip is technically valid but failed performance qualification. Do not
submit it as the next qualified improvement.** It changes UNHCR only; E025
remains incumbent. No leaderboard upload has been made.

The official phase-1 scorer passes all three schemas, extracted archive and
source predictions match exactly, and clean regression stays within .002.
However, the existing household simulation loses .002025811 UNHCR skill;
external observed-data gains are small and uncertain. No .64/.65 forecast
is supported by these measurements.

See [scorecard](../../submissions/2026-09-19-E041/SCORES.md),
[verification](../../submissions/2026-09-19-E041/verification.json), and
[experiment decision](../../docs/experiments/E041-supervised-retrieval.md).

Rebuild: `.venv/Scripts/python.exe scripts/assemble_e041.py`.
