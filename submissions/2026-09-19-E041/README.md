# E041 DEV best archive

**User-reported DEV result on 2026-09-19: Grand .64 / UNICEF .52 / WB .49 /
UNHCR .92. E041 is the new DEV incumbent.** Displayed gain over E025: Grand
+.01, UNHCR +.03; controls unchanged. This is one rounded/noised hosted result,
not an exact unnoised gain estimate. Archive bytes remain frozen.

The official phase-1 scorer passes all three schemas, extracted archive and
source predictions match exactly, and clean regression stays within .002.
However, the existing household simulation loses .002025811 UNHCR skill;
external observed-data gains are small and uncertain. These local outcomes
remain unchanged; the subsequent positive evidence comes from the hosted
reading. No .65 forecast is established.

The earlier local rejection and exploratory-slot decision are preserved in
the scorecard and experiment record. The actual result selects the .64 arm:
retain the snapshot as DEV best. E025 remains the separately validated phase-2
fallback; E041 has not received that phase's validation or method update.

Archive: [2026-09-19-E041.zip](../2026-09-19-E041.zip).
Relocated from `output/dev/E041.zip` on 2026-09-19 without byte changes.
Future ZIPs follow `submissions/YYYY-MM-DD-E0XX.zip`.

See [scorecard](SCORES.md),
[verification](verification.json), and
[experiment decision](../../docs/experiments/E041-supervised-retrieval.md).

Rebuild: `.venv/Scripts/python.exe scripts/assemble_e041.py`.
