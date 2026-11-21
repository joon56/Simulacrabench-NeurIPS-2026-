# A023 — Candidate construction boundary and complete cost contract
date-started: 2026-09-27
status: done — TECHNICAL_PASS / EMPIRICAL_HOLD
relates-to: A021 / A022 / E041

## Authorization and decision, before fixtures

Explicit user instruction executes the previously held S1 prompt. Sole owner:
root. HEAD `1d223340d4e1fa3993b411dc5daafab9cb37d0cd`; A023 unused at entry.
A020/E059/A021/A022 and user changes remain uncommitted and protected.
A022 manifest SHA256 `04bff9c8c375c1126886f222da83c105e3b6b8a5f34842fb95ab99908d1267e2`.
79 permitted input hashes match; four Parquet hashes inherited, NOT rechecked.
No Python/WSL jobs at entry. Initial sandbox process listing denied; elevated
read-only listing succeeded. No actual computation failed in that check.

Decision: specify a prospective real-schema candidate family and the missing
production adapter, enforce its information/freeze boundary with injected stubs,
and account for complete normal/failure execution from source. This is NOT an
implementation or qualification of a trained candidate. P differs from R/E041;
D-P compares controlled objectives, D-R compares complete procedures.

Session: 17:07:00–18:07:00 UTC, 60 minutes; CPU2; owned fixture process tree
RSS AND commitment each <2GiB. No GPU, installation, network, paid resources.
Before fixtures, use the existing standard-library Windows MemoryTree monitor;
sample at 0.1s, enforce a 60s fixture subprocess limit and the session deadline.
Failure to measure, resource breach, unexpected leakage/freeze/semantic failure
is technical STOP; preserve outputs. Expected negative-test rejections are not
failures. No statistical rescue, alternate seeds, or lowered thresholds.

No source/key Parquet read, response access, cache decode, production import,
real fit/optimizer/predict/score, E060, ZIP, commit/push or S3. Only permitted
A023 documentation/outputs/checker/tests and additive status/log edits.
Main: boundary + cost contract. Only backup: missing-condition closeout.

## Fixed design and implementation plan

Apply brainstorming/writing-plans/karpathy-guidelines/test-driven-development
within the user's already approved scope; no extra approval or commit workflow.
The plan lives here, not in an unauthorized directory.

1. Record entry hashes and source cost anchors; derive schema-only masks.
2. Write focused boundary tests first, then a pure standard-library injected
   stub in `scripts/check_a023_candidate_boundary.py`. Tests live in
   `tests/test_a023_candidate_boundary.py`. No probability-table recalculation.
3. Verify forbidden response stages, candidate/lambda identity and freezing,
   no selection-to-builder feedback, and identical P/D construction budget.
   Stub selectors return prescribed IDs, not scores or learned decisions.
4. Source-only cost audit plus one monitored fixture verification. Record
   hashes/access events/zero actual calls, limitations, and S0 handoff.

TECHNICAL_PASS means this bounded stub contract and static accounting passed.
EMPIRICAL_HOLD remains regardless. No actual upstream nonleakage, model parity,
effect, power, runtime feasibility or S2 qualification follows from stub PASS.

## Prospective finite family — public structure only

Use the unchanged production grouping regex `s(\d+[a-z]?)_`, with `other`
fallback. Preserve schema item and option order. Let X contain all section
groups owning a PREDICT parent with a PREDICT child in another group; let Y
contain all endpoint groups of these cross-section edges. Fixed candidate order:

| ID | Active sections | Reason |
| --- | --- | --- |
| legacy | empty | Controlled inactive fallback; not exact R |
| upstream | X | Change cross-section ancestors, observe downstream propagation |
| endpoints | Y | Change both ends of the same structural dependencies |

No scores select these masks. Entire sections activate, not favorable heads.
Deduplicate identical masks in this order before any training; if fewer than
two distinct masks remain, mechanism is structurally unidentified: HOLD.
UNHCR expected X={3}, Y={3,7a,7b,7c}; verify from public schema. These are
prospective specifications, not empirical registration/permission. The A021
C0..C3 toy tables are not reused as real candidates. Single-section SIPP
collapses this family; do not invent sections or infer UNHCR impossibility.

## Inputs, trained artifacts and outputs

Future role registry must be group-disjoint and frozen before responses:
T_reference, T_fit, C_legacy, C_replay, S, E. No actual assignments here.
All non-T PREDICT blocks must be fully masked BEFORE any P/D base helper,
including ladder selection, neural tuning, final neural training and conditional
gate agreement. GIVEN may be passed for rendering, but label-bearing tables
must be explicit capabilities, never a unified unmasked frame.

| Stage | Permitted response capability | Required artifact |
| --- | --- | --- |
| P/D base | T_reference + T_fit only | ladder columns/kappas/tables; neural config/epoch/net/blend; full and asked-conditional distributions; gate agreement |
| Metric construction | T_reference donor answers, T_fit fitting answers | reference+.5 priors, common GIVEN weights, ordered pools, section weights and old/new proxy shares |
| Lambda | C_legacy + C_replay only | both buckets for every head/candidate, zero if unavailable |
| Render | no query responses | GIVEN-only P and globally recursive D outputs |
| Selection | S only, library already frozen | P/D choices bound to one library/rules/budget digest |
| Evaluation | E only, both choices frozen | independent paired D-P and D-R evaluation; no learner callback |
| Exact R comparator | T_reference + T_fit + both C + S; E masked | independent original pipeline and frozen outputs |

R uses the same overall development information, differently allocated. Its
permission to use S does not extend to the P/D builder. No refit in this design.

Metric adapter must extract the fitting-only part of `fit_sections` (source
63–106) without calling its combined fit/select interface: it currently reads
selection labels to form arrays and decide activity. Fit all schema sections
once on T, retain weights and shares even when original R would not activate
them. Preserve L-BFGS-B objective/penalty/bounds/maxiter50/ftol1e-7 and original
old-share grid {0,.25,.5,.75,.9,.98}. r_old retains source first10-of32 fitting
definition; r_new is fitted expit share. Controlled P uses A021's unchanged
formula `(1-r)*reference_prior + r*candidate_evidence`, choosing old/new r by
mask. Inactive evidence is actual legacy top10, so r_old's fitting surrogate
and its controlled P evidence can differ. This is explicit approximation,
NOT exact R or a new proxy objective. Never substitute toy share .5.

Common rarity/household weights are frozen on T GIVEN only. Reference-only
donor bank for both P/D calibration and S/E rendering; T_fit is query-only
for metric fitting. This deliberately differs from R's deployment visible bank.
Legacy top10 uses existing argsort slice/self-exclusion order; metric top32
uses sorted bank, argpartition membership, then score-desc/ID-asc lexsort within
the selected subset. Boundary ties are not globally ID-stable. Freeze actual
donor IDs/order, source/numerical versions and input row order; never equate
legacy10 with first10-of32. No donor answers from C/S/E.

Compute every candidate's lambda before S. Inactive heads use C_legacy union
C_replay; active heads use only C_replay. Both buckets derive exclusively from
legacy top10 common-weight max posterior >=.5, even for active learned evidence.
Preserve original grid 0,.1,...,.9,.95,.98, strict tie retention, full marginal
model replay objective (not recursive D), truth probability floor and bucket
minimum30. Fewer than30 gives lambda0; no sparsity rescue or learned rebucketing.
Nonfinite metric artifact makes a structurally active candidate unavailable
before S; do not silently change its mask. This is a construction STOP, not a
new score guard. Future empirical registration must retain an explicit failure
arm; technical fixture does not simulate numerical optimizer success.

D renders ALL heads in schema order, storing final parent belief after evidence
mixing before rendering children, including cross-section descendants. P uses
all scored cells as in A021. Official normalization/floor applies to both;
do not add standalone section gains or use fixed-parent leaf replacement.
Candidate identities bind masks, learned artifacts, lambda/bucket rules, donor
ordering, schema, role registry, source and construction budget. Freeze library
before S. Same .003/group2SE rule, candidate-order tie and legacy fallback for
P/D; selection sees no constructor capability. Freeze both choices before E.
No new objective, guard, extra training or winner-conditioned lambda/refit.

The stub records tokens for these artifacts and access events only. It does
not compute donors, weights, lambda, recursive predictions or objective values.
Real source extraction/masking/parity and actual fitted serialization remain
unimplemented, untested and separately unauthorized.

## Observations and scoped disposition

Registered text preserved in `A023-outputs/registration.md`; no responses or
scores informed this specification. Public schema confirms155 PREDICT-parent
edges,71 crossing sections. Candidate active-item counts0/61/135; all213 items
still belong to each whole-output candidate. Full target lists are in
`A023-outputs/schema-audit.json`; no head was selected from an observed gain.

13 focused tests PASS in.10s. Monitored wrapper.6082997s including worker imports,
peak owned-tree RSS70479872bytes, commitment40534016bytes. Expected missing-module
RED separately took1.1747911s, peak RSS73527296/commitment44376064bytes. These are
tiny fixture costs only. No actual training/prediction/score/cache/key/response
operation ran. Source AST independently checked2 config entries, one tuning-loop
`_train` call and one final call:2 target pipelines imply6 normal neural calls.
Full source-derived counts and failure paths: [cost record](A023-cost-accounting.md).

Tests reject C/S/E capabilities in fitting, S/E in lambda construction, forged
role tags, cross-role group overlap, changed lambda/library bytes, repeated
construction/selection, E responses during selection, S during evaluation,
unknown choices and R access to E. P/D receive the same frozen library, rules
and budget. Injected lambda/render outputs are opaque tokens; arithmetic,
per-head eligibility execution, actual donor isolation and upstream equivalence
are NOT established. Existing A021 arithmetic fixtures were not rerun.

**TECHNICAL_PASS / EMPIRICAL_HOLD.** The boundary specification and narrow stub
checks are complete. A real production adapter remains to be implemented and
qualified under separate authorization. Target-channel suitability, role
authorization, evaluation precision/multiplicity and measured complete model
cost remain unresolved. No S2 candidate, release qualification or benefit claim.
See [closeout](A023-outputs/closeout.md) and [S0 handoff](A023-outputs/s0-handoff.ko.md).
