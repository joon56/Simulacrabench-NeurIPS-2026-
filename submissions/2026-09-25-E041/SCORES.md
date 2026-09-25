# E041 — TEST selection and frozen delivery

Status: preparation; never uploaded to TEST. A018 fixes the seven-candidate
comparison and decision rules before additional evaluation. This snapshot
uses unchanged E041 main.py (SHA256
22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073).
The new ZIP includes a full starter-kit MIT notice; predictor bytes are unchanged.
Archive hashes: ../../docs/analysis/A018-outputs/archives.json.

Pair `submissions/2026-09-25-E041.zip` only with this directory's
`method-4p.pdf`. E025 and its matching method are separately preserved at
`submissions/2026-09-25-E025.zip` and `submissions/2026-09-25-E025/method-4p.pdf`.

## Selection and validation

E041 has the strongest favorable target-pipeline evidence among the fixed
eligible candidates, plus unchanged controls and manageable deployment
complexity. Later qualified alternatives have adverse/unresolved DEV readings
and weak/conflicting transfer evidence. E025 is the simpler fallback. The
complete rationale, leakage/refit/activation analysis and residual uncertainty
are in ../../docs/analysis/A018-test-selection.md. No numeric TEST expectation
or winning probability is supported.

Historical A012 official phase-2 skills: .490197770701 / .462029504790 /
.564665364947. Paired E025 deltas: 0 / 0 / -.000508448996, all absolute <=.002.
A018 reverified all A012 artifact/input hashes and all 442425 raw vectors.
Fresh E041 single-process all3 reproduced every source vector exactly,
including active UNHCR retrieval (seven of eight sections); 336.554468 seconds
including imports/data/scoring/parity, 1493135360-byte peak working set and
1604792320-byte peak commitment. Windows CPU, two numerical threads, no CUDA.
These synthetic local measurements are neither hidden TEST performance nor a
hosted H100 guarantee. Current validation outputs and final hashes live in A018.

Final ZIP extracted and freshly run through official score.py --phase 2:
all three PASS with the skills above, all 442425 raw vectors exact to modular
source references. Official seconds sum359.448694; inclusive orchestration
wall364.340160 seconds, within the shared3600-second limit. Final ZIP checker
PASS for both E041 and E025. Three existing phase-2 guard concerns were reviewed;
see A018's code-review.md for corrections and historical-execution scope.

## Prospective TEST result and failure arms

| Observation | Interpretation and action |
| --- | --- |
| Valid TEST score, any value | Record Grand, instrument scores, ID, timestamp and runtime if available. Different respondent roles prevent a controlled TEST-minus-DEV model A/B. No score-driven resubmission. |
| TEST below historical DEV .64/.52/.49/.92 | Describe discrepancy and generalization uncertainty; no inference of hidden labels, exact component failure or selector inactivity. |
| Pre-upload E041 technical/resource defect | Before the one submission is spent, switch to separately verified E025 plus its own method; log reason and recheck the live kit. Do not invent an ensemble or retune on TEST. |
| Participant-side contract/runtime failure after upload | Preserve sanitized error and reproduction; no assumed second submission with E025. |
| Documented organizer infrastructure failure | Follow clause 12 and explicit organizer retry instructions; retain frozen artifact unless instructed otherwise. |
| Kit/schema/rule changes before upload | Reopen affected engineering checks and provenance. Do not upload a stale certificate. |

Model-change cutoff: 2026-11-12 00:00 UTC / 09:00 KST; preferred user upload
by Nov 13 00:00 UTC. Official TEST end: Nov 14 00:00 UTC / 09:00 KST, verified
2026-09-25. Recheck at upload. No upload authorization is implied here.

## Release and actual outcome

Four-page method required for every TEST entry. Team source license is an
explicit scoped proposal pending owner choice; award-stage source release
requires an effective license permitting non-commercial research reproduction.
Third-party conditions and historical development disclosures are retained in
../../docs/analysis/A018-outputs/release-notes.md. No public repository release.

Actual upload timestamp, submission ID and TEST scores: none.
