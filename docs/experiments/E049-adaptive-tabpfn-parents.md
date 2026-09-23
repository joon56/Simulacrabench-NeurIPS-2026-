# E049 — Adaptive TabPFN gate-parent challenger
parent: E041
status: parked
date: 2026-09-23

Model: TabPFN-HSCC E049. Built with PriorLabs-TabPFN.

## Hypothesis

GIVEN-only TabPFN-v2 parent predictions complement E041 unevenly across
respondents; an honestly trained confidence selector can exploit that
complementarity and propagate better parent beliefs to UNHCR descendants.

## Domain check

Registered after E048's frozen-library results but BEFORE E049 oracle/learner
execution or production implementation. E048's constant-mixture bound failed;
its per-query/section bound did not. These motivate a different policy family,
not permission to change E048's settings or claim that the oracle is learnable.
E047 changed use of existing retrieval. Here the added signal is an independent
pretrained predictor, with effects through parent routing as well as content.

Background: ERPIS return-intention, social-network and economic gate parents
describe different aspects of refugee respondents across four host countries
and two rounds; prediction confidence can differ across respondent profiles.
Approximate real gates mean improved parents need not improve every descendant
(CLAUDE.md; docs/domain.md section9; official schema descriptions). Keep E041's
soft gates and learned retrieval. Historical E025 .79 base/.10 evidence and
.079 gated residual locate the target, not E041's measured decomposition.

Ceiling before estimator: reuse E048's frozen, hash-bound observed Adult
probabilities (seeds49/50). Split its1200 out-of-sample queries into first400
correction-fit, next400 selection, last400 audit. All were excluded from both
first-stage fits. Recompute the finite query/section alpha{0,.25,.5} oracle on
the last400; require skill/3 >.005 on both. Then fit the existing E047 seven-
feature, L2=.01 bounded logistic confidence policy per section (extra share
<=.5), using the frozen PFN predictions as the candidate. Retain E047 fit/
selection/audit guards unchanged. No tuning to the resulting audits.
These rows were previously screened, so this is an exploratory reuse, not
an untouched holdout or evidence that refugee transfer is established.
The finite grid maximum is an upper bound only for that finite library and
a feasible lower bound on the continuous-alpha oracle. Review clarification
before production fitting: also compute the exact continuous [0,.5] scalar
oracle by concave derivative bisection, reporting the tangent gap. This
contains the sigmoid policy family; no selection setting or pass bar changes.

Production: UNHCR only, four highest-direct-child-count PREDICT parents with
<=10 complete schema classes, schema order ties. Form each parent's descendant
closure including itself; selected closures must be disjoint (if not, use
exact E041). Evaluate a full PFN-parent renderer and original E041 renderer
with exactly the same fitted first stage/evidence. Treat those final subtree
vectors as the two alternatives for E047's existing confidence policy. Since
the selected roots have no ancestors among themselves and all routing and
evidence coefficients are fixed, convex blending these subtree alternatives
propagates the chosen root mixture consistently. Tests must verify this
linearity against direct rendering; otherwise do not submit.

Visible-row shuffle seed4901: correction-fit min(800,n//10), selection
min(600,n//10), audit min(400,n//10); all three groups completely hidden before
shadow E041 fitting and excluded from PFN references. PFN uses first512
remaining shuffled visible rows, one estimator, original public V2 weights,
categorical GIVEN indices, CPU, random_state0. On final refit use first512 of
the seed4901 visible shuffle. Reject small cases with <512 references to E041.
Apply E047's unchanged per-section gain >max(.001,2SE), overall audit >SE,
L2=.01, maxiter50, coefficient bounds[-6,6]. Freeze policies before final refit.
UNICEF/WB exactly E041. No new weight fitted outside visible container data.

## Change

New src/models/adaptive_tabpfn_parents.py only after oracle pass. Reuse the
unchanged E047 confidence helpers and E041 renderer via local cached copies;
never mutate their modules. Locally load exact public weight once at import,
disable telemetry and downloads. Exact package pins and attribution/license
in the dated submission; original V2 artifact hash remains E048's.

## Result

Observed reused Adult audits: finite oracle skill/3 +.008298155/+.007547830;
supplemental continuous oracle +.008300689/+.007549228, maximum tangent gap
<1e-15 nats. Actual guarded estimator skill +.001739413/0 (mean-equivalent
+.000579804/0); only seed49 employment selected. Its descriptive 95% paired
respondent interval includes zero. No adoption threshold met. E048 standalone
PFN losses remain evidence against unconditional use.

Fifteen E049 tests and fourteen unchanged E047-helper tests pass. An independent
review checked partition isolation, flooring, exact private cached renderer,
AST assembly, offline packaging and oracle scope. No static functional blocker.
Real active assembly contract: forced alpha.25,16 actual PFN fits,34 vectors,
8 active and26 unchanged; source/archive maxabs0, source/E041 difference
3.8788358671073612e-6. Runtime44.2566s including imports. This is a forced
engineering fixture, NOT learned activation or efficacy evidence.

Clean all3 raw-exact E041: .500648423071/.454717307363/.562462728858.
UNHCR delta -.000486144847 vs E025, within .002. All four local groups reject;
source total639.2682122s with concurrent diagnostics. Existing household
diagnostic .552012531240, exact E041; all reject,699.5266095s. No directional
sim gain. Official score.py all3 PASS, raw source/archive parity0 and exact
E041 outputs. Official offline execution 639.517s <900s; environment
installation excluded. Full-size forced-active UNHCR uses8 real PFN fits,
132273 vectors and passes official raw/floor/grade checks. Main import+predict
579.475s; setup/validation included594.335s. Combined with official controls,
conservative active-path total 753.797s <900s. ZIP checker PASS.
Forced activation is an engineering check, not learned activation or efficacy.
Concurrent local CPU timing is not a hosted runtime guarantee.

Review corrected finite-grid endpoint normalization to exactly match the
continuous E047 mixture family. Max floored probability change1.193e-8,
finite oracle skill/3 changes<4e-11; zero choices and no learned gains changed.
This numerical alignment changes neither policy, grid nor screening threshold.

## Decision

Parked; technically qualified as submission #29, not uploaded. Adoption
requires three-instrument mean skill gain >.005. Exploratory
packaging requires clean <=.002 regression vs E041/E025, exact control parity,
source/archive parity, ZIP checker, score.py all3 PASS, total <900s. Hosted
score arms must be registered before upload. No .65 forecast is justified.
