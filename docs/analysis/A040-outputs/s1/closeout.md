# A040 S1 closeout — HOLD_SPECIFIC_INPUT

2026-10-01. S1 information task finished; **no model candidate or S2 handoff**.
Return to S0. No automatic technical execution, inquiry, upload, commit or push.

## Decision and one specific missing fact

Current [official README](https://raw.githubusercontent.com/SituatedEvals/public/main/README.md)
states at saved line171:

> There is no runtime training hook, and training must happen **offline**.

The actual retained E041 snapshot performs Adam training inside `predict`
(`_train_on`, lines445 onward) and UNHCR metric optimization (`fit_sections`,
1026 onward). The proposed honest shadow/refit procedure adds another such E041
pipeline. TabICLv2 fit itself does not optimize pretrained weights, but does fit
encoders/preprocessing and build a labeled context at runtime. These operations
must be distinguished; renaming a function does not resolve the contract.

**Missing fact:** does the current HSCC policy permit visible-TRAIN-dependent
context/preprocessing/selection and the retained E041 neural/metric fitting
inside `predict`, or does its offline-only sentence prohibit that procedure?

Source needed: an applicable current official rule/FAQ or organizer clarification
covering those actual operations, not just row matching or import-time weight
loading. Evidence owner: HSCC organizers; acquisition/review owner: S0/user under
separate authority. No message sent or account accessed here. S0 may first supply
existing applicable official evidence; contacting organizers is not automatic.

Resume condition: record the official interpretation and its version/scope. If
permitted, S0 can assess a separate named synthetic-only technical task using the
frozen conditional contract. If prohibited, the present E041-preserving procedure
is NO_GO under that rule; do not silently replace the comparator, shrink heads or
invent offline actual-TRAIN access. Ambiguous wording remains this exact HOLD;
do not repeat a broad model survey or demand the same information again.

Historical E041/E049 hosted success does not settle the meaning of today's
documentation. Conversely this wording alone does **not** prove an organizer
violation, revoke the incumbent, or establish scientific failure. This is a new,
specific policy reconciliation condition for A040, not a VAF metadata HOLD.

## Facts, interpretation and limits

| Area | Observed/source fact | Judgment |
|---|---|---|
| Identity | Exact code commit; checkpoint revision, filename, advertised size/SHA256; BSD3 code and separate weight-license metadata | Version-bound research specification possible; no downloaded-byte/build proof |
| Probability API | classes_ alignment, fitted categorical preprocessing, target-dependent cache, many-class route in wrapper | Plausible213-head interface with explicit adapter/checks; no upstream/model numerical PASS |
| Scope |213 heads,156 gated,17 GIVEN,834 columns;4 heads K>10, max complete K15 | Public inventory complete; observed classes/support unknown |
| Load lifecycle | Stock fit reloads checkpoint; cache uses y | Import-only injected model required; not implemented or tested |
| Full cost | Active plan:426 context fits/predict calls,4 E041 pipelines,12 normal neural training calls,16 metric minimizations | Whole900s/16GB feasibility unknown; no small-head extrapolation |
| Effect reading | Conditional F/S/E policy and single global-alpha family defined; bounded hosted whole-procedure readings | Credible design if runtime operations permitted, not currently established authorization or empirical evidence |
| Research status | No new probabilities, response access or scores | Numerical oracle absent; no UNHCR effect estimate; no .65 forecast |

Therefore **HOLD_SPECIFIC_INPUT**, not CONTRACT_READY, technical PASS, NO_GO from
cost, or release/adoption approval. Unknown measured runtime is a future check;
the present blocking fact is the official operational interpretation above.

## Deliverables and actual work

- [Contract and prior-experiment comparison](contract.md): E048 standalone losses,
  E049 oracle-to-policy gap, E051 direct-distribution STOP retained; one prospective
  synthetic-only technical task, with exact scope/call/time/memory caps.
- [Cost accounting](cost-accounting.md), [213-head inventory](schema-accounting.json),
  [conditional observation plan](observation-plan.md).
- [Official source ledger](source-register.md), [local source hashes](local-source-hashes.json),
  [exposure ledger](exposure-ledger.md), [verification](verification.json),
  [S0 handoff](s0-handoff.ko.md).

12 official resources, including2 failed guessed source paths; no source expansion
after cap. Small documentation text/metadata saved. No weights/install/import,
fit/optimizer/predict/score, fixture/test or protected-data/cache access. Initial
metadata command errors were corrected, not reported as scientific test results.
Read-only Git initially required a per-command safe.directory override because
the sandbox identity differs from checkout owner; no Git config was changed.

The immutable baseline is E041 main.py SHA256
`22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.
HEAD remains `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; its score-only update is
accepted, not rolled back. Current dirty work and prior S0 artifacts preserved.
Workflow r4 read evidence and SHA256 are in entry.json; closeout verification
separates allowed status/log edits from protected records.

E041 incumbent/E025 fallback; E057/E060/E061 parked. Every prior STOP/HOLD,
E058 STOP/E059 STOP_SELECTION, A_half nonpromotion, protected roles and cumulative
17999/12339 exposure remain. A018 TEST selection remains user-unconfirmed; S3
stopped. No S2 candidate. Next action belongs to S0's review of the specific
official interpretation, not another model or immediate implementation.
