# E042 — Final-output evidence blend ceiling
parent: E025
status: parked
date: 2026-09-18

## Hypothesis

An independently calibrated evidence blend after the final E025 distribution
can recover useful neighbour mass suppressed by its in-sample pre-gate replay.

## Domain check

Pre-registered before the oracle. E034 measured an approximately .10 evidence
contribution, so this investigates an observed information source. It assumes
neither extra household recurrence nor a new overlap mechanism. Technical:
the oracle optimizes one fixed extra mixture share per item over frozen E025
and unchanged E025 donor evidence, with the official uniform floor. The family
does not propagate changed parents back into descendants and must be described
as such. It is an optimistic in-sample selector, never submitted settings.
Measure on the existing household sim, not a new favourable simulator; clean
sandbox is a separate no-regression channel. If the oracle log gain is at most
.005, park without an estimator. If above, build only an out-of-sample selector
and judge actual held-out pipeline gain independently. Report both log/skill.

## Change

Only a ceiling diagnostic is authorized by the oracle-first step so far.
No production estimator or submission snapshot exists at registration.

## Result

Existing household sim, seed 13, final-output fixed-share grid oracle:
delta log +.004569680, UNHCR skill +.003621694, three-instrument equivalent
+.001207231. 163 items selected a nonzero share. Runtime 11.685 s.
Full grid and measurements: `../analysis/A008-outputs/e042-postblend-oracle.json`.
This is the best in-sample selection within the recorded finite grid and
frozen donor family; it is not an upper bound over every possible calibrator.

Domain verdict: no new assumed population mechanism was needed. Even
optimistically selecting shares on the existing directional channel does
not establish enough gain to warrant building this estimator.

## Decision

Parked at the registered oracle gate: log gain .004570 <= .005. No estimator,
submission archive or hosted slot. E025 remains incumbent. Reopening requires
a materially different family or evidence channel, not finer share tuning.
