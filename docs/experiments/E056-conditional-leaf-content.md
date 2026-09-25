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

Registration18ab9e6 preceded fitting/scoring; tested library527ddd2 and final
score-persistence revisiondbb0ac6 preceded all actual runs. Original registration
bytes are retained in docs/analysis/E056-outputs/registration.md. No original
E041/E055 model, threshold, grid or snapshot was changed. Existing group cache
passed code/data/role/masking/coverage checks; zero additional E041 fits.

Six fixed trees fitted on564 asked fit rows each; observed class counts in
schema order: DT148/416, BIR38/526, OS199/365, NST106/458, OTH101/463, COR29/535.
All6078 non-fit rows' candidate predictions were frozen before any new score.

| Stage | Persons / SSUID groups | Result |
| --- | ---: | --- |
| Oracle |1872 /1395|Baseline skill .668734958501; finite optimum .669613180434; delta +.000878221932, skill/3 +.000292740644. Feasibility PASS only.|
| Selection |1148 /869|Only BIR retains alpha=.5. Paired log mean .002826004258 > cluster SE .001210878893. DT/OS best arms fail their one-SE guards; other heads choose zero.|
| Audit |1192 /872|Baseline .676908504136; selected .677560456922; delta +.000651952785, skill/3 +.000217317595. Bootstrap95% [.000202805542,.001195519933]. Follow-up research criterion PASS.|

Audit changes1192/8344 vectors (14.2857%), all on the one selected leaf;
parent and other five leaves remain exact E041. The114 actually asked audit
respondents have BIR conditional loss .227919199841 -> .178259232573.
This is secondary descriptive evidence, not an additional selection test.
Raw sentinel difference0; max total-mass and post-floor sentinel differences
2.220446049250313e-16. Under this fixed linear floor, the latter is roundoff,
not a material gate-probability intervention.

All nine E056 tests passed; nineteen tests including A014/E055 boundaries
passed before the final score-persistence addition, then nine E056 tests passed
again. A separate frozen-array verifier confirms56 source hashes,42546 cached
identity vectors, the full729-way finite optimum, selection SE/choices and
the2000-draw audit interval. No response-label re-access or additional fit in
verification. This is independent arithmetic code, not an independent sample
or separate human/subagent review.

Additional real-data fit wall .215791100s (six trees); all four monitored
worker stages total44.897293s, peak process-tree RSS430350336bytes (~.401GiB).
Worker clocks start after module imports; they exclude interpreter/import,
tool scheduling and development/wait time. These are diagnostic costs, not a
complete hosted predictor runtime. Root remained inside the registered90-minute
research cap. All E056 workers exited successfully; no background E056 job.
The separate A018 verification was observed and allowed to finish before fits.

Domain verdict: complementary conditional errors exist for one leaf on this
fixed US hospital proxy. The effect is narrow and small in seven-head pooled
units. It supports investigating the operation, not inferring refugee content
signal, gate repair or a readable Grand increase. Six targets from one star,
only114 asked audit persons, prior shared-source oracle exposure, edited exact
gates and unweighted sampling limit transfer. The conditional bootstrap omits
training/selection variability, survey-design weights and domain shift.

Artifacts: docs/analysis/E056-outputs/{manifest,oracle,selection,audit,
frozen-verification}.json, resource records, exact executed script/registration,
exposure-ledger.md and next-session.ko.md. Restricted rows/arrays remain only
in ignored external/e056/. Library SHA256
db6dd6fbe32bc6e53073541b576bb2fda175877ec475d93a8adfe87734b33534.

## Decision

**Positive research screen; parked pending distinct UNHCR implementation.**
Technical diagnostic checks PASS; production technical qualification and release
no-regression are NOT RUN. DEV exploration is not package-ready; no S2 handoff
or new ZIP. TEST adoption is not supported by this proxy alone. E041 incumbent,
E025 fallback and E054 parked remain this study's dispositions; separate S3
decisions, if made, belong to their owner and are not overwritten here.

The positive branch exhausts this S1 handoff's allowed work. Backup trigger
(invalid/STOP/inconclusive/over-cap) did not occur; no backup report, refit or
rebuild. Next: register UNHCR leaf scope, honest selection/refit behavior and
runtime gate before implementing any production candidate. Do not transplant
BIR's .5 or select humanitarian items by this proxy's winning head. Current
audit is now development evidence for future work, never an untouched audit
again. Preserve every prior STOP, including E055's +.005 failure.
