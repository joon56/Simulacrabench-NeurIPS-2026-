# E050/E051 candidate-library independent review

Date: 2026-09-24. Scope: `src/eval/recursive_candidates.py`,
`scripts/screen_e050_e051.py`, `tests/test_recursive_candidates.py`, and
`tmp/e050-library-diff.txt`. Read CLAUDE.md, current status, the top three log
entries, the candidate-selection plan, and both experiment registrations.
Read the relevant original renderer, layout, agreement, retrieval, metric and
Adult loader dependencies. No source edits, commits, training, or test reruns.

**Specification verdict: PASS for preregistered oracle screening.**
**Quality verdict: no blocking findings.** This is not a production-release,
measured-gain, or runtime qualification.

## Verified contracts

- The private renderer copies `link_sharp.predict` globals and wraps fitting
  products in private caches. Each E050 call creates fresh caches. Ladder
  tables distinguish item and full/conditional option tuple. Neither the
  original renderer nor its function bindings are replaced. The identity
  arm is the original first render, returned without numerical transformation.
- The actual E041 generic renderer uses `supervised_retrieval.supervised_layer`
  and `hh_cap.CONFIGS`. This avoids the public E041 wrapper's Adult fallback.
  Cached evidence is captured once; no E049 imports or dormant extraction.
- Registered identity, zero, half, toward-one and one transformations cover
  both concentration buckets of captured items; missing lambda means zero.
  Every altered arm traverses the unchanged recursive renderer.
- Component separation is exact for this renderer: query beliefs influence
  other heads only through gate parents; agreement tables and fitted model,
  ladder, and evidence products are fixed. PREDICT gate edges join connected
  components, including cross-section descendants. Observed GIVEN parents
  separate components. The tests compare composed component outputs against
  a full mixed recursive render and exercise a changed descendant.
- Adult uses exactly 2600 visible rows and 2400 whole-block masked queries,
  ordered as 800 oracle, 800 selection, 800 audit. Both libraries receive the
  same masked frame. HistGBM labels and marginal counts come only from visible
  rows. Features use GIVEN fields; source IDs are metadata only.
- Tree parameters, two threads, explicit categorical/ordinal handling,
  complete schema class mapping, singleton behavior and .01 Laplace marginal
  mixture match E051. Shares are exactly 0, .25 and .5. Zero share preserves
  the original E041 raw vectors.
- All query predictions are serialized and hashed before oracle scoring.
  Source and frame hashes are captured before fitting. Cache reuse verifies
  the authoritative pickle hash and source/frame/protocol provenance.
- The oracle restricts arrays to its 800 rows. Selection/audit labels are not
  passed to scoring or any fitted selector. Each component chooses one arm
  by pooled row/head log score, then the final metric pools all cells. This
  is the exact maximum over all registered constant component-arm
  combinations, not query-wise hindsight or a continuous-family bound.
  Whole-arm scores are also reported. Normalization and .001 flooring match
  the current registered cases and local official-metric helper.

## Evidence and limits

The current test file contains 11 focused tests, including freeze-before-score
and cache reuse coverage added after the initial review package. Root relayed
the implementer's result: 11 passed in 6.57 seconds. This review did not rerun
tests or independently reproduce costly E041 fits. The requested implementer
report file was not yet present when inspected.

No genuine requirement conflict found. Interpret "audit unread" precisely:
audit outcome labels remain unscored and absent from model fitting, while the
explicitly registered full-sample vocabulary and profile deduplication read
raw sampled values during preparation. This exception is disclosed in both
the registration and output metadata; do not describe the data-loading path
as never accessing audit values at all.

The normal original E041 call still updates its existing LAST_DIAGNOSTICS
object; the new code does not monkeypatch original modules. Diagnostics are
copied into the library after the call. This does not affect probabilities.

The reusable e051_library helper validates query positions and predicted head
order, not equality of every fit value. The reviewed screen supplies the same
frame object to both libraries, satisfying the current contract. A future
independent cache consumer must preserve this alignment.

Downstream work remains conditional on both observed oracle gates. The screen
itself does not train selectors or enforce release gates. No audit-informed
parameter changes, adoption conclusion, or hosted improvement claim follows
from this review.
