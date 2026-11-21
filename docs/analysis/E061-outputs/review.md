# E061 pre-run source review

Root review, not independent human/subagent review. No DEV score access yet.

- Original files unchanged. New module uses existing tune_fn injection;
  no runtime reassignment of model globals. Tests alone mock training/dispatch.
- TiedNet inherits original trunk/full-head construction with cond_dims empty;
  schema map selects ordinary logits in conditional option order. Sentinel stays
  a learned full class. Fewer modules changes initialization RNG consumption;
  fixed seed0 remains. No additional architectural configuration or weight.
- Original _pooled_ce/_targets helpers reused by reference. Static AST comparison
  of _train/_train_on/tune_and_train passes after removing precisely the new
  schema-map argument/assignment and TiedNet constructor substitution. See
  source-review.json. Config/epoch/patience/selection/blend/refit otherwise exact.
- Original supervised_layer/renderer and control dispatch retained. Production
  source versus snapshot output parity is still to be measured on controls.
- Nine focused tests passed. Three autograd.grad evaluations per successful
  suite; six across the two pre-run suites. Three injected fake training calls
  per suite, zero actual optimizer fits. RED was expected missing module.
  Second suite adds deliberate held-out-target rejection and removes a harmless
  scalar-conversion warning. No successful full-stack run has been repeated.
- Harness reads only named synthetic files and filters TRAIN/DEV; official
  sample_rows builds model frame, masks every DEV PREDICT cell. Runtime trace
  rejects any held-out row passed to _targets. Trace is observational and does
  not replace production functions. All vectors are persisted before scoring.
- Official check/floored/score functions imported without CLI/installation.
  Original caches, generator execution, phase2/TEST and packaging absent.
- Resource controller observes owned tree before startup and every.1s; rejects
  measurement failure, deadline, cumulative1800s, candidate900s or8GiB. Parent
  includes interpreter startup; function timers separately show component costs.
  Counters are conservative sums of per-process peak RSS/commitment, not a
  continuously sampled instantaneous peak. Local performance is not hosted proof.
- Every full-stack entry and neural call is counted across attempt logs, including
  failures;9/27 caps enforced. Metric iterations, selected epochs, lambda activity
  and target-access checks are recorded. Scientific failures cannot trigger retry.
- S2 source/assembly parity, ZIP checker, official all3, package/import resources
  and SCORES provenance remain outside S1. No efficacy/TEST adoption claim.
