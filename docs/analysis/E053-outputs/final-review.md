# E053 final frozen-artifact review

Reviewed 2026-09-24 after both registered seeds completed. No model fits or
source/result modifications performed by reviewer. Root executed the reviewer-
authored tmp/e053-frozen-artifact-probe.py in the working runtime; its JSON log
was independently inspected here. That probe only rescored the existing oracle
slice from frozen outputs, never selection/audit labels.

## Decision

STOP is correct on both registered splits. No learned calibrator, production
module, ZIP or threshold relaxation follows. These are conditional ungated Adult
proxy-family results, not estimates or upper bounds for nonlinear gated UNHCR.

| Seed | E050 five-arm skill/3 | Returned continuous skill/3 | Uncensored continuous skill/3 | Gate |
| --- | ---: | ---: | ---: | --- |
| 54 | .000434552631120119 | .000523121586708092 | .000523121586708092 | STOP |
| 55 | .000003739795029599 | .000172892177510713 | .000172892177510713 | STOP |

Primary numerical upper estimates are .000523121586708029 and
.000172892177510682, both far below .005. They sit below attained estimates by
about 6.3e-17 and 3.1e-17 respectively from floating-point aggregation order.
This is within the declared numerical tolerance, not a substantive certificate
failure or threshold ambiguity. Report them as numerically coincident bounds;
do not describe their printed ordering as an exact real-arithmetic inequality.
Stored nonnegative pooled gap is zero after its roundoff clamp.

## What naturally activated

Both seeds selected the single generic Adult retrieval section, index0. Its
internal section-selection gain_log was .02692612986706674 (SE .006718766632088159)
for seed54 and .034020916299602966 (SE .006264330240758936) for seed55. These are
legacy fit/selection proxy diagnostics, not independent E053 learned gains.

Original E041 returned evidence in both seeds. Uncensored materialization was
false in both. Each of the eight heads had evidence for all2400 outer query rows,
so returned-only and uncensored families are exactly identical on these runs.
All2400 query rows, including all800 oracle rows, were diffuse bucket0; bucket1
had zero rows. Both natural dormancy recovery and independent concentrated-
bucket freedom were therefore unexercised. Synthetic tests cover the former
code path, but these observed runs supply no empirical benefit estimate for it.

The effective observed expansion over E050 was per-item continuous absolute
weights on existing evidence in one occupied bucket. The registered family is
still distinct, but neither major structural distinction can be advertised as
an observed successful mechanism. E050's lambda1 arm is outside E053's .98 cap,
so five-arm and continuous families should not be called strictly nested.

Changed-vector counts5600/6400 are raw-equality diagnostics, not counts of
substantive evidence improvements. They may include endpoint normalization-only
changes; seed54 capital_gain_positive selected lambda0 with such a change.

## Frozen artifact verification

Reviewer PowerShell checks passed for both seeds: capture compressed hashes,
NPZ hashes, registration hashes, every declared current source hash and every
prior exposure-manifest hash. Both registration archives have SHA-256:
08c2f15d49a6934dcc9976834823479ea70c229dd52ffaa4435e567d24d74a5d.

Root execution of the reviewer-authored frozen-artifact probe passed:

- Compressed and decompressed capture hashes; every capture/NPZ array exact.
- Reconstructed schema/frame/masked-frame hashes and known role intersections.
- Query positions exactly2600..4999; oracle-only positions0..799 within them.
- Donor indices and banks belong to2600 fit positions; two archived query donor
  records per seed, covering initial top-k and selected-metric candidate IDs.
- All three oracle summaries recompute exactly with the frozen implementation.
- Independent official-probability pooling at saved selected lambdas yields
  skill/3 .0005231215867081213 and .00017289217751072748, agreeing within1e-12.
- Original lambda reconstruction error is exactly0 in both captures.
- Both saved records name oracle as the only scored partition and mark
  selection_or_audit_evaluated false; static scorer control flow confirms this.

The earlier reviewer-authored scalar probe, also executed by root, passed80
synthetic objective checks against an independent scipy optimizer with maximum
score difference1.7763568394002505e-15, metadata checks and51 prior source hashes.
These are separate numerical checks, not new fits or hosted validation.

## Limits retained

The samples overlap prior public Adult experiments and one another; source-role
intersections are archived, nonexhaustive, and correctly disclosed. Fresh seeds
are not globally untouched confirmation. Whole outer answer blocks were hidden
for first-stage fitting, and inspected A011 rows were not silently relabeled as
independent audit evidence. Selection/audit remain unscored in E053.

The preregistered resource-allocation stop is satisfied. It does not establish a
universal calibration ceiling, prove legacy replay optimal, test dormant evidence
benefit in a naturally dormant sample, or bound full recursive survey repair.
No further fitting or output replacement is necessary to make this decision.
