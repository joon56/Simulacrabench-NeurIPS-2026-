# E056 — Sentinel-preserving conditional leaf content
parent: E041
status: parked
date: 2026-09-25

## Hypothesis and domain check

Independent asked-only GIVEN trees complement E041's existing conditional
neural/ladder heads on gated leaves. Conditional factorization is not new.
E051 fitted full-answer trees, including sentinel; E055 varied existing donor
shares inside recursion. Neither bounds this newly fitted content library.
Their STOPs remain unchanged and weaken prior enthusiasm for another tree.

A016/S1 handoff is the authorized scope. Demographic interactions for being
asked and for asked content may differ; complementary errors are unverified.
SIPP US hospital reasons, edited exact gates, imputation and rare asked rows
do not represent approximate refugee-survey gates or establish TEST headroom.
No presumed new household recurrence or refugee demographic fact. Historical
E025 loss maps do not decompose E041. Oracle/learned/hosted evidence stay separate.

## Session contract and reference

Decision: does this fixed library merit later UNHCR implementation research?
Input HEAD 4166130 (S0 documentation only relative to technical HEAD 7f712e1).
Main: one existing group-view cache, at most six fixed asked-only tree fits,
finite feasibility screen, guarded selection, then one conditional audit.
Backup on invalid/STOP/inconclusive/over-cap: <=30 minutes reviewing frozen
E041/E025 TEST readiness, without fits, rebuilt packages or final selection.
Main research wall <=90 minutes from 2026-09-25 07:36 UTC; cumulative fit wall
<=1200 seconds, two numerical CPU threads, no GPU, process-tree RSS <=8 GiB.
One heavy fit at a time; E041 at most one fit, zero if cache validates.
Monitor own process tree RSS every .25 seconds; abort at memory cap, fit cap
or 4800 worker seconds (remaining session time reserved for records). Persist
resource/abort record; never kill unrelated processes. No data download, paid
resource, environment change, production model, assembly, ZIP or upload.

Comparator: unchanged generic link_sharp + supervised_layer + hh_cap.CONFIGS,
not the small-schema public-wrapper fallback or E055 selected oracle output.
E041 main SHA256 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073;
ZIP SHA256 1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50.
Inspect E055 manifest/source/roles/masking/coverage before cache reuse; freeze
exact source hashes and installed versions with the prediction library.

## Frozen data and label exposure

Only screen_e055.prepare('group'): original 12000-person E055 hash sample,
A014 SSUID group namespaces and roles, six existing demographic GIVEN fields.
Verify sample hash, all role positions, source hash, masked-frame identity,
cache hashes and no SSUID overlap between any roles. Keys used only for audit,
never features. All non-fit PREDICT blocks masked before all model fits.
Actual non-sentinel status selects asked rows only within fit, never queries.
No parent, other target, flag or ID becomes an input. Preserve person-view.
Previously exposed E055 oracle/sample aggregates are development evidence;
new split names do not make this an untouched population. Calibration remains
masked and unscored. Selection scores open only after oracle PASS. Audit opens
once after choices are frozen, and only if at least one share is nonzero.
Raw source, keys, row arrays, models stay ignored under external/e056/.
Tracked outputs contain hashes, aggregate metrics and reproduction commands.

## Fixed library and Oracle scope

Leaves: six original EHREAS_* children; HOSPITALIZED and every other output
remain unchanged. Fit one HistGradientBoostingClassifier per eligible leaf on
fit non-sentinel rows only. Copy E051 TREE_PARAMETERS: max_iter=40,
max_leaf_nodes=15, learning_rate=.1, l2_regularization=1,
early_stopping=False, random_state=0, max_bins=255. Public schema category
encoding; all six GIVEN fields categorical (each <=255 levels). No search.
Fewer than100 asked fit rows or fewer than2 observed classes: exact E041.
Align probabilities to full answer schema order, then q=.99*tree+.01*marginal;
marginal=(asked-fit class counts+1)/(asked count+number of answer classes).

For raw p, final sentinel g, non-sentinel mass M: retain p'[g]=p[g]; set
p'[answers]=(1-alpha)*p[answers]+alpha*M*q. Shares {0,.25,.5}, constant per
leaf. alpha=0 returns original directly; M=0 preserves the whole row. Preserve
raw sentinel and total mass; validate finite/nonnegative positive-total output.
No parent/descendant rerendering. Apply exact official .001 uniform floor.
Record raw and post-floor sentinel differences; do not assume post-floor
equality. In exact arithmetic preserved total plus raw sentinel imply it under
the current fixed linear floor; floating-point differences are still measured.

Freeze predictions for every non-fit role, registration, source provenance and
manifests before mapping any evaluation labels to scores. Optimize oracle sum
of log probabilities independently per leaf: parent fixed and no cross-leaf
edges, so this equals all 3^6 constant-share assignments. This bounds only this
finite fitted library on these oracle rows, not per-person weights, new trees,
other populations or TEST. Pooled seven-head skill uses U=mean(log K), K=2 for
parent and3 for each child. Delta skill/3 is descriptive, never a Grand forecast.
Oracle delta skill <=1e-10: STOP. Larger: numerical feasibility only, continue
to cheap selection. This is not significance/adoption and does not revise
E055's failed +.005 gate for its different frozen prediction family.

## Selection, uncertainty and one-shot audit

Selection chooses each leaf's highest log-score share, exact ties smaller
alpha. For its paired row log-score differences d_i versus E041, let N be
persons, G distinct SSUIDs, n_g group size, S_g=sum(d_i in group), m=sum(d_i)/N.
Cluster SE = sqrt([G/(G-1)] * sum_g(S_g-n_g*m)^2 / N^2).
If G<2 force zero. Keep nonzero only if m>0 AND m>SE; otherwise zero.
This is a conservative operational guard, not multiplicity-adjusted testing.
Freeze chosen shares and selection result before audit label scoring.
All zero: no-intervention STOP, audit unopened.

Otherwise audit all seven heads exactly once. Primary paired delta skill;
SSUID cluster bootstrap draws G groups with replacement, retaining all persons
in each drawn group. Ratio of resampled sums to resampled person counts, divided
by7U, gives pooled delta skill. 2000 draws, numpy default_rng(5601), linear
2.5/97.5 percentile endpoints. Fixed training/selection; no survey weights,
training variation, multiplicity or domain-shift uncertainty represented.
Report raw/official-floor sentinel differences, changed-vector fraction over
all seven heads, asked fit counts, tree count, time/RSS and conditional asked
log loss (normalize post-floor non-sentinel vector) as descriptive secondary.
Audit delta>0 AND lower95%>0: warrants follow-up UNHCR research only. Otherwise
nonpositive/inconclusive STOP. No seed, threshold, predictor or selector revision.

## Implementation and verification plan

- [ ] Freeze this registration in Git before score access or any new fit.
- [ ] Add tests/test_e056_conditional_content.py before diagnostic code: exact
  alpha0/zero-mass parity, sentinel/total mass, reversed class order and missing
  classes, fallback thresholds, whole-block masking, independent 3^6 maximum,
  hand-calculated cluster SE, group bootstrap, selection/audit access order,
  parent preservation and actual official floored parity.
- [ ] Add scripts/screen_e056.py only (helper module only if needed). Validate
  existing cache, fit fixed library, freeze all outputs, then oracle. Separate
  selection/audit entry points enforce frozen manifests and score boundaries.
- [ ] Run focused tests, inspect source, commit reviewed diagnostic before fit.
- [ ] Execute once with monitored caps. Verify frozen arithmetic without fits
  or new labels. Record results/exposure; do justified backup if triggered.
- [ ] Render tree, update status/log, write next-session prompt, commit task
  files only, push origin and verify remote HEAD. Preserve unrelated user edits.

## Result

Pending; this section contains no empirical outcome at preregistration.

## Decision

Technical diagnostic qualification pending. No production/release qualification,
DEV candidate or TEST adoption follows from this protocol. E041 incumbent,
E025 fallback, E054 parked. A positive research screen requires a separate
UNHCR implementation/runtime/no-regression session, not S2-ready packaging.
