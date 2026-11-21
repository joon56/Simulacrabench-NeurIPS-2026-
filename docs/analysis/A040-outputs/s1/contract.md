# A040 — conditional execution contract, not an implemented candidate

**HOLD_SPECIFIC_INPUT.** The specification below is technically grounded but
conditional on resolving one current HSCC policy ambiguity in [closeout](closeout.md).
No fit, output generation, fixture, release or submission was performed/authorized.

## Distinct hypothesis and counterevidence

Frozen TabICLv2 may add useful complete-answer probabilities through a different
pretrained tabular prior and full visible context. E041 already learns nonlinear
functions. Neither interaction capacity nor disagreement alone is new evidence.
The proposed intervention covers **all213 UNHCR PREDICT heads**, including ordinary
content and gate-sentinel outcomes. UNICEF/WB remain the E041 snapshot path.

| Prior | Observed evidence retained | Difference and limitation for A040 |
|---|---|---|
| E041 | Nonlinear shared trunk, ladder, retrieval metric and recursive gate renderer; current hosted Grand.6433333333 / .52/.49/.92 | Comparator is the actual final E041 distribution, not E025 or a linear substitute. E041's old local adoption rejection and subsequent exploratory hosted success are both history. |
| E048 | TabPFN-v2, four parents,512 references. Adult standalone supported-head skill differences−.009697424/−.008079412 vs logistic. Query/section oracle mean-equivalent+.008285992/+.007461967; constant-section+.001362032/+.001414845 failed its .005 gate | PFN is not automatically useful. Per-query hindsight overstates the constant-policy family. No universal foundation-model/UNHCR ceiling follows. |
| E049 | Four-parent,512-reference, respondent-dependent policy. Reused Adult oracle mean-equivalent+.008298155/+.007547830; actual guarded policy+.000579804/0 | Oracle-to-policy gap is central. No new respondent router here. Current score ledger reports Grand.6433333333 / .52/.49/.92, equal E041's released values; not proof of zero effect or inactivity. |
| E051 | GIVEN-only direct complete-distribution trees already tested. Actual-E041 Adult oracle mean-equivalent .00041780435381531643/.00038021850656629557; STOP before selection/audit | Complete distributions alone are not novelty. A040 changes pretrained prior/context, not the old STOP. Eight-head timing was not full runtime. |
| E061 | Hosted Grand.6400000000 / .52/.49/.91, adverse versus E041 | Synthetic/technical PASS did not establish ERPIS utility. E061 stays parked. |

Sources: existing experiment records and current score ledger in
[local-source-hashes](local-source-hashes.json). E025 historical .79/.10 is not
an E041 loss decomposition. No .65 forecast, effect-size forecast or universal
.005 threshold. The new hypothesis fails operationally if the full fixed policy
cannot fit the resource contract or fails comparable hosted readings; unavailable
oracle evidence and flat rounded scores remain unresolved, not universal falsification.

## Frozen version and offline lifecycle

Use code commit `0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3`; checkpoint
`tabicl-classifier-v2-20260212.ckpt` at HF revision
`4dcd344ece2c00be9e831fdd35bed57b5ad83e19`. Advertised checkpoint identity and
license evidence are in [source-register](source-register.md). Package semver was
not established; a moving PyPI/latest install cannot represent this code pin.

Code permits BSD3 redistribution with notices/conditions/disclaimer and no
endorsement; weight metadata independently declares BSD3. Preserve both provenance
records. Forecast-specific Apache notice is not a license for unrelated weights.
Future acquisition must verify actual checkpoint bytes against the advertised
SHA256 before any deserialization. No checkpoint was acquired here.

Proposed packaging mechanism, if later authorized: pinned source package bundled
locally, frozen compatible named dependencies, one local checkpoint. No git URL
requirement or moving `models.txt` revision. Archive feasibility remains untested:
110MB of weight alone being below1GB says nothing about complete package/build.
Python>=3.10 and3.13 are declared upstream; runtime compatibility is not measured.
Core dependencies: torch>=2.2, scikit-learn>=1.3, numpy, scipy, einops>=.7, psutil,
tqdm>=4.64, huggingface-hub; pandas needed for proposed categorical input. Exact
pins/build proof remain a later isolated technical prerequisite, not installed now.

At process module import: load the verified local checkpoint once, construct
frozen model/config, eval mode. Network must already be disabled. Every wrapper
sets an explicit local model_path and allow_auto_download=False. Environment
offline flags are additional defense, not evidence of socket isolation.

**Stock classifier is not a drop-in import-only loader.** Its fit calls
`_load_model()` unconditionally, including `torch.load` for a local path. A small
version-bound adapter must inject the one imported frozen model/config into each
fresh estimator without reloading weights. Use an explicit adapter, no global
monkeypatch. Private loader hook compatibility and shared-module mutable state
must be tested before use. Sequential estimators, fresh encoder/ensemble state,
clear any model cache between heads; no concurrent fits. No model optimizer or
pretrained-weight updates in the added expert.

Fixed prospective expert settings: n_estimators8, norm_methods[`none`,`power`],
feature shuffle`latin`, class shuffle`shift`, random_state42, temperature.9,
average_logits=True, support_many_classes=True, batch_size8, kv_cache=False,
device`cuda`, use_amp=True, use_fa3=False, offload_mode=False, n_jobs2, verbose=False.
These retain the main default probability family and remove automatic FA3/offload
switches from the first technical trial. No parameter sweep. Failure at this
explicit memory policy is a scoped stop; changing ensemble/context/offload needs
a new S0 decision before another trial, not automatic rescue.

## Input, labels and probability contract

1. Seventeen schema-ordered UNHCR GIVEN columns only. No respondent_id, role,
   excluded key, other PREDICT answer, actual asked indicator or target-derived
   feature. All213 targets receive the same eligible context rows. A gated
   head's NA_GATED is an ordinary target class; do not discard skipped rows.
2. Encode target values as their complete schema option indices. Options are
   declared values followed by NA_GATED only for gated items. `LabelEncoder`
   returns sorted observed classes, which may omit schema options. Scatter each
   predict_proba column through `classes_` into the full K-column zero-initialized
   vector; never assume column j is schema option j. Unobserved options get raw0.
3. Single observed class: explicit one-hot constant path, no neural fit/forward.
   Zero usable context: exact retained E041 head distribution, count the fallback.
   Invalid labels, NaN target in a declared fit row, nonfinite/negative/all-zero
   probabilities, bad alignment or zero usable features are technical failures,
   not silently repaired evidence. No training on NaN sentinel substitutes.
4. GIVEN columns are categorical strings/object DataFrame columns. The upstream
   encoder fits ordinal mappings on F only, unknown/missing categories map to−1;
   numeric imputation is fitted only if a numeric column is explicitly supported.
   UNHCR schema says there are no genuine null cells. Missing GIVEN in tiny
   engineering cases tests error/encoder handling, not real-data imputation need.
   Constant-feature removal, power transforms and permutation choices fit on F.
5. With observed classes exceeding model.max_classes, the wrapper allows a
   mixed-radix/hierarchical route when support_many_classes=True and cache=False.
   Nominal native cap10 is documented; actual checkpoint config is uninspected.
   Public schema has four heads over10, including two with15 complete classes.
   These must be tested, never silently dropped. Hierarchical internals are not
   reviewed or timed by this source-only session.
6. predict_proba reverses class shuffles, aggregates logits and applies the fixed
   temperature before row normalization. It is a predictive distribution, not a
   guarantee of probability calibration. Shared weights are reusable; y-dependent
   cache/ensemble states are not X-only shared work. Cache building passes y_train;
   cache modes also reject above-native-cap classes. Minimum design disables cache.
7. Normalize valid raw q and raw E041 final p; mix `(1-alpha)*p + alpha*q` at
   the final complete-distribution layer, then evaluate with
   `floor + (1-K*floor)*p_mix`, floor=.001. Return raw mixtures; the official
   grader floors once. Do not double-floor, or rerender gates after this mixture.
   Sentinel mass may change; this is not the sentinel-preserving E056/E057 family.
8. Return canonical row order and schema item order for every blank cell, complete
   option order including sentinel. Do not infer output order from frame columns.
   UNICEF/WB and alpha0 UNHCR return the original E041 vectors without a new
   normalization/rounding pass. Exact fallback is a specific parity obligation.

The frozen expert may depend on the collection of query X through internal
attention/normalization. No unverified query-batch invariance claim. Shadow query
batch is the ordered S+E union, once; final query batch is all entitled held-out
respondents, once. No query label enters either batch. Large-query chunking is
not an uncosted optimization; it requires a separately checked contract.

## Conditional scientific policy

One global mixture weight in `{0,.25,.5}` for all213 heads; no head/section or
respondent selector. Prospective split/selection/independent check/refit are fully
specified in [observation-plan](observation-plan.md). No output exists today,
therefore no numerical oracle or empirical preregistration result exists.

Two expert contexts if accepted: F-only shadow and all-visible final context.
Both use all eligible rows, not512. Same frozen checkpoint, independent fitted
preprocessors and y mappings. Shadow-to-refit probabilities may differ; retain
selected alpha, never reselect after refit. The original E041 path similarly
needs shadow F-only and final all-visible computations; existing inner learning
and replay limitations remain and are not repaired by renaming outer roles.

## One minimum future technical task — PLAN ONLY

Entry: S0 resolves the policy condition and user authorizes a separate named
S1 technical task, including any package/checkpoint acquisition and H100 access.
No paid resource authorization inferred. No E record or implementation now.

Use only generated fake values and the public schemas. One fixed generation
seed4000; no real response, old synthetic files, protected keys or model caches.
Keep the schema/gate imperfections explicit: synthetic answers are engineering
fixtures, not simulated evidence about ERPIS.

- One small fixture suite, cumulative model wall<=120s: absent schema classes,
  singleton/zero-context branches, all15 classes, categorical unknown/missing,
  permuted frame columns, cross-target contamination, raw/floored vectors and
  alpha0 parity. Stock-versus-injected loader comparison only on small fake data,
  with extra stock load counted inside this suite, not the all3 runtime claim.
- Access instrumentation fails if S/E response blocks reach any fit/preprocessor;
  E responses become accessible only after alpha is frozen. Reject hidden DEV/TEST
  answers by construction. No implementation-mirroring tests replace these checks.
- One full-shape phase1 all3 run, including fresh import, one checkpoint load,
  shadow, selection/check, all-visible context rebuild and final output. Force
  alpha=.25 only in this explicitly marked engineering fixture to exercise the
  maximal active path even if fake selection rejects. Evaluate inactive return
  parity from retained E041 vectors, without a second full fit. Fake context
  covers every public class, including15; no four-head timing extrapolation.
- One instrumented baseline-only all3 comparison, fresh process, same fake data
  and fixed source, for actual E041 output parity. Separate measured baseline cost
  does not count toward candidate hosted900s, but counts toward task budget.
- At most3 process invocations above; small suite120s + candidate900s + comparator900s
  = cumulative model wall1920s. Task wall60min, CPU8 maximum (TabICL threads2),
  one explicitly authorized H100, no parallel heavy jobs, host limit16,000,000,000
  bytes process-tree commitment/RSS with1s watchdog; CUDA allocated/reserved peak
  and device capacity recorded separately. Kill process tree on any limit/failure.
  No silent CPU retry for the new expert. E041's existing GPU-to-CPU retry is
  instrumented and counted, never treated as free.
- Candidate run must complete under900s including import/all3 and satisfy every
  output/parity/isolation check. No measurement available means technical check
  unfinished, not PASS. No head/context/seed/threshold rescue after failure.

Unchanged E041 on the same deterministic fake input must produce identical
vectors on deterministic paths; candidate control branch returns those vectors
unmodified. If CUDA baseline itself is nondeterministic, record that limitation
and do not waive exact-control qualification by inventing a post-result tolerance.
Offline failure or shared-state mismatch stops the task. Weight hash/load count,
whole-process timings and source identities must accompany results.

This minimum technical task covers DEV scale only. Phase2 accounting is listed
below; 3600s TEST-scale measurement, release packaging/source parity/official
all3 checks and S0 authorization remain separate later work. No TEST choice.
