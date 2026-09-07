# E024 — evidence-input net as the base inside E022's mixture
parent: E022
status: parked
date: 2026-09-08

## Hypothesis

E020's idea (co-respondent evidence as network input, to learn
cross-item household structure) kept, but as the BASE model inside
E022's replay-calibrated mixture instead of replacing it: if the net
ignores the extra inputs the model is E022; if real households carry
cross-item structure (a co-respondent's answer to A informing B,
household-level items identical across members) the net can use it.

## Domain check

Pre-registered 2026-09-08. (a) overfitting bounded by the inner
early-stopping split (evidence built identically there); (b) household-
level items (housing, documents, assistance, income) are shared facts —
cross-item structure is plausible in real data; (c) the household sim
has no cross-item structure by construction, so the local check is
NO-HARM only; a gain is a leaderboard question.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Household sim (ρ ∈ [0.2, 0.8]): +0.0004 log vs E022 — no harm, no
gain (as the sim allows). Clean sandbox: 0.4440 / 0.5001 / 0.4533 /
0.5616 vs E022 0.4429 / 0.5006 / 0.4549 / 0.5627 — every instrument
slightly DOWN (3-inst −0.0011; wb −0.0016): on duplicate-free data the
evidence block is a noise feature the net does not fully ignore.
Runtime 216 s local (evidence for all rows on unicef's 16k pool).

## Decision

**Parked.** Small measured harm where households are absent, no
measurable upside, runtime above the comfort ceiling — not worth a slot
ahead of leaderboard-backed compositions. Revive as a pre-registered
A/B if the layer family stalls again, ideally after restricting the
extra block to rows with a concentrated posterior (which would remove
the duplicate-free harm).
