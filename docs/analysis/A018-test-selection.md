# A018 — Frozen TEST selection and delivery

Date: 2026-09-25. Integration owner: S3 session, restricted to A018 outputs
until concurrent-session ownership is resolved. Input HEAD: 4166130.
Existing dirty user files, A017 outputs and E056 work are not owned by S3.

## Prospective contract — fixed before additional evaluation

Decision: select one existing predictor for TEST and preserve a separate fallback.
No new model, ensemble, calibration, hyperparameter search, hosted upload or
private response access. Main task: compare qualified candidates, close phase-2
engineering gaps and freeze matching model/method/release artifacts. Backup:
unchanged E025 if E041 fails a mandatory technical or resource gate; if both
fail, declare delivery blocked rather than weaken a threshold.

Comparison set: E025, E041, E044, E045, E047, E049 and E052, at their historical
dated submission bytes. These have completed submission qualification, not
necessarily phase-2 qualification. E044 remains an adverse control, not promoted
because it is included. E054 is an intentional measurement ablation, excluded
from performance selection. E042/E043/E046/E048/E050/E051/E053/E055 have no
qualified replacement release; E056 is ongoing research, excluded even if a
concurrent proxy result arrives. Older superseded variants add no distinct
supported finalist beyond E025; their historical records remain unchanged.

Selection order (qualitative, no invented gain forecast):
1. Valid archive, exact predictor provenance/parity, three-schema official
   phase-2 validation, no hidden-label access, compatible licensing/disclosure.
2. Absolute clean phase-2 skill difference <= .002 per instrument versus E025,
   plus relevant E041 comparison. This is release policy, not transfer evidence.
3. Target relevance and actual hosted evidence, including adverse/flat readings,
   selection exposure and conflicting observed/synthetic channels. A single
   rounded DEV best is insufficient by itself; no claim of a precise TEST gain.
4. TRAIN+DEV retraining behavior, activation/rollback semantics, calibration
   leakage, reproducibility, full-run time and memory, and dependency burden.
5. Prefer E041 if it closes engineering gaps and no alternate has stronger
   transferable evidence with comparable risk; otherwise E025. No extra fits of
   flat/adverse candidates merely to rank synthetic scores.

Known evidence before this protocol: status/log, A012 phase-2 scorecards,
E041 method and source, experiment qualification summaries through E055.
E041 hosted .64/.52/.49/.92 versus E025 .63/.52/.49/.89, user-reported;
E044 .63 adverse; E045/E047/E049/E052 .64 without best update unresolved.
A012 phase-2 E041-E025 0/0/-.000508448996; 442425-vector exact parity;
367.177 s separate-process official total. None is confidential TEST evidence.

Allowed data: public schemas and existing synthetic TRAIN/DEV/TEST fixtures.
Synthetic TEST already exposed for engineering, never called untouched.
No Adult/SIPP label access, new proxy score, or E056 score access in this task.
Model runtime may use visible TRAIN+DEV labels and all GIVEN values; whole
synthetic TEST PREDICT blocks must be masked before predict. New local results
may reject unsafe delivery, never tune predictors or reselect on sandbox gain.

Compute cap: one heavy process at a time; at most two unchanged all-three
single-process rehearsals (E041/E025), plus one official all-three E041 run,
35 minutes total model execution. Existing unchanged official/source evidence
may be reused only after hashes and raw parity are reverified. Each full run
must finish <3600 s and local process peak working set/private commitment
<16,000,000,000 bytes; report Windows CPU limitations and lack of hosted H100
measurement. Stop our own worker on the limit. No competing fits permitted.

Engineering change cutoff: 2026-11-12 00:00 UTC / 09:00 KST. Preferred user upload
by 2026-11-13 00:00 UTC / 09:00 KST. Current artifact freezes at this session's
manifest timestamp. Before cutoff, reopening needs a separately registered
decision and full revalidation; after cutoff only organizer-required contract
fixes with logged revalidation. Live rules must be checked again at upload.
Official API checked this session: TEST Nov 1 00:00 UTC to Nov 14 00:00 UTC,
one submission/team, 3600 seconds. No TEST upload is authorized here.

## Execution plan

- [x] Freeze candidate/source/archive and scorer/data hashes; save minimal
  official schedule/terms evidence and inspect candidate records.
- [x] Reverify A012 frozen parity/provenance; rehearse E041/E025 sequential
  three-instrument calls in one process and record peak memory/activation.
- [x] Check final archive layout and official phase-2 all-three E041 results;
  retain E025 historical official qualification with its explicit limitations.
- [x] Reconcile and visually verify four-page E041/E025 methods with code,
  development disclosures and current rules; prepare scoped MIT proposal.
- [ ] Owner choice of effective source license remains pending. This blocks
  award-stage source delivery, not local TEST preparation; no grant inferred.
- [x] Record selection, residual uncertainties, exact paths/hashes, immutable
  freeze manifest and result/failure arms; preserve fallback separately.
- Integration: S1/S2 close commits settled at3c96b14; S3 owns the final handoff.
  Commit only owned work, push and check remote HEAD. The Git commit/remote
  receipt records completion separately from this self-hashed freeze. Never
  upload to TEST.

## Results

E041 selected for the frozen delivery; E025 separately preserved as fallback.
The outcomes below do not change the prospective comparison set, gates or caps.

### Execution provenance and disclosed deviations

- Prospective protocol SHA256 df627f4d2965c8219bcaab1b3f61c0b4f993059827d5117e6a1064099e93d890
  was recorded in preflight.json at 07:48:22 UTC before new model execution.
  `selection-registration.md` preserves its exact text (recovered later from
  the append-only result document and matched to that pre-run hash).
- Concurrent S2 owned A017 and S1 owned E056. Their commits advanced HEAD
  after entry; none of their files was staged by S3. S1's handoff subsequently
  stated its workers finished and S3 owns A018/release files. Shared handoff
  integration waits for that session's final write/commit to settle.
- No independent Python fit was observed at E041 launch or interim monitoring;
  E041 completed at 16:56:59 KST. A later slot check found an E056 library
  process. The first E025 attempt was inadvertently launched after that check
  in the same orchestration call; stopped only S3's E025 processes immediately
  on review. It produced no instrument result and its empty log is preserved
  as E025-aborted-concurrent.log. This is a scheduling deviation, not a failed
  statistical gate. The same unchanged E025 run resumed once no other Python
  remained; no threshold, model or score-based retry changed. Count aborted
  execution toward the 35-minute compute cap; at most two complete rehearsals.
- A later shared-status read incidentally exposed the parallel E056 aggregate
  research summary. No E056 artifacts/labels were opened; its candidate
  exclusion was already frozen and remains unchanged. This is a disclosure
  of aggregate-score exposure, not a claim that the summary was unseen. E056
  still lacks production/release qualification and cannot enter this delivery.
- Initial E025 method expansion rendered five pages. Removed redundant history,
  preserving method, limits and disclosures. Both methods then rendered four
  pages. Visual review found the shared renderer hardcoded E041 in the E025
  footer; an A018-local renderer corrects model label/title without touching
  the shared renderer or historical PDFs.

### Candidate evidence and disposition

The frozen hashes are in `A018-outputs/preflight.json`. All seven archive mains
equal their dated source bytes. This rechecks packaging, not each candidate's
phase-2 behavior. Existing A012 source/official raw vectors were compared again
in full, with all recorded artifact and synthetic input hashes unchanged.

| Candidate | Actual evidence beyond DEV rank | Risk and decision |
| --- | --- | --- |
| E025 | Hosted .63/.52/.49/.89; validated phase-2 baseline; E032-E034 component evidence belongs to this model only. | Simpler reference. Self-excluded donor replay still fits base on its own calibration rows. Preserve separate fallback. |
| E041 | Hosted best update .64/.52/.49/.92; controls unchanged. Observed Adult audit gains +.000595/+.000427 skill have intervals including zero. Clean and household synthetic comparisons are adverse. A012 phase-2 parity and absolute .002 release gate pass. | Most direct favorable target evidence among technically viable finalists, with no external weights and modest extra runtime. Preferred if shared-process resource checks pass. No isolated metric-effect or TEST-gain claim. |
| E044 | Same-pipeline initial-weight control; official phase-1 all3 and parity pass; hosted .63 adverse under its registered arm. | Supports retaining E041's learned metric in that intervention, but no independent replication. Not selected. |
| E045 | Union retrieval qualified; Adult mean-equivalent audit gains +.000142/+.000165, weak; clean/household small losses; hosted .64 no update. | Changes coverage and selector, increases cost (historical official all3 395.852 s). No demonstrated transferable advantage. Preserve parked status; no new phase-2 fits. |
| E047 | Output calibration qualified, active assembly tested; Adult +.000274/0 skill, interval includes zero, prior oracle exposure plus acceptance on audit. Household +.002325 UNHCR is assumption-dependent. Hosted .64 no update. | Extra internal acceptance does not make the external research path untouched. Historical official 515.180 s. Additional calibration complexity without established target benefit; not selected. |
| E049 | TabPFN parent correction qualified; reused Adult audit +.001739/0 skill, interval includes zero; clean/household return E041. Forced active path is technical evidence only. Hosted .64 no update. | Extra package, weight provenance/license and offline dependency burden. Historical forced-active all3 estimate 753.797 s; no phase-2 resource certificate. Not selected. |
| E052 | Evidence-after-gates intervention qualified; clean UNHCR +.000167 but household -.001080 versus E041; actual active-path parity tested. Hosted .64 no update. | Simpler intervention than added calibrators but conflicting channels and no favorable target reading; historical official 402.795 s. Not selected. |

No flat reading establishes zero effect or hidden selector inactivity. These
comparisons are dependent development observations, not seven independent
trials. Synthetic ranking was not used to choose the winner. E041's broader
support is limited: favorable target pipeline observation, unchanged controls,
structural plausibility, passing phase-2 engineering and lower dependency cost
than the later calibrated/PFN alternatives. E025 is a credible downside hedge,
not an empirically proven better TEST predictor.

### TRAIN+DEV refit, activation and leakage audit

No fitted weights are frozen in E025/E041. Both retrain per instrument from
the supplied complete visible rows; TEST PREDICT remains missing. Visible
counts grow UNICEF 14885 to 16373 (+10.00%), WB 5195 to 5715 (+10.01%),
UNHCR 8279 to 8900 (+7.50%). Held-out counts become 3473/1212/1449. Added DEV
labels may change marginal/asked heads, ladder ordering/shrinkage, neural
architecture/epochs and network mixture, approximate-gate coefficients,
matching rarity/EM weights, calibration lambdas and active retrieval sections.
Unchanged code therefore does not mean unchanged fitted predictor.

E041 dispatches on the exact schema key `s3_11_intent_return_12m_lbl`.
UNICEF/WB use E025 directly. UNHCR needs >=500 complete rows and a nonempty
held-out set for the learned layer; otherwise legacy evidence is used. No
usable GIVEN signature returns no evidence. Seed 4101 partitions full visible
rows into fit/selection/replay/reference. Phase 1 UNHCR sizes are
1200/800/800/5479; phase 2 1200/800/800/6100. Partition membership can change
when DEV is added, even with the same seed. Reference bank grows about 11.33%.
Section gain must exceed `max(.003, 2*SE)` on the selection proxy. Production
uses the full visible donor bank, 32 candidates for active sections, original
top-ten concentration buckets, and replay-selected item lambdas. Each bucket
needs 30 rows; no positive lambda yields the base only. Inactive sections retain
legacy evidence. CPU fallback catches GPU training exceptions, but neither a
whole-run timeout nor arbitrary selector error triggers an E025 model swap.

Metric-fit, selection and new-metric replay query sets are disjoint; the metric
reference bank excludes them. This protects query-weight fitting, not the
entire calibration pipeline: base distributions refit on all visible rows,
then participate in replay containing their training labels. Donor
self-exclusion does not fix this optimistic calibration. The selector's
marginal/evidence proxy and mixture share differ from deployed recursion and
item lambdas. Their generalization cost is unknown; do not label it repaired.
Initial matching uses all GIVEN frequencies, including TEST GIVEN: permitted
transductive covariates, not hidden-response leakage. Target identifiers are
not used. Repeated DEV feedback selected this complete method; the same DEV
then legally joins final training, so no fresh independent DEV claim exists.

The full SIPP/Adult research paths and historical second-account probe are
disclosed. No proxy row, fitted proxy artifact, TabPFN weight/output or
confidential response enters either final predictor. SIPP exact US gates
cannot validate approximate UNHCR/refugee gates. E055 STOP remains scoped;
parallel E056 does not enter this selection or justify a last-minute replacement.

### Rules, disclosure and release boundaries

Live Codabench API evidence is saved at `A018-outputs/official-rules.json`.
Development ends 2026-10-31 00:00 UTC; use Oct 30 operationally. TEST opens
Nov 1 00:00 UTC and closes Nov 14 00:00 UTC (both 09:00 KST), not end-of-day
Nov 14. Test quota is one per team; shared budget is 3600 seconds. Clause 7
requires a four-page method for every TEST submission and source licensed for
non-commercial research reproduction from top three at award stage. The site
summary is less specific; apply the actual agreement. Whole-repository public
release is not expressly required. No source is published by this session.

Clause 9 requires external pretrained weights to be public at a specified fixed
commit before TEST opens, under a compatible license. Neither finalist uses
such weights; historical TabPFN development is nevertheless disclosed. Clause
12 allows documented organizer-infrastructure retries; participant failures
are not assumed retryable. The retired second account remains a disclosed
historical compliance uncertainty, not a permission or an adjudicated waiver.

Starter kit remote HEAD remains ee427a94f6cc6a0d9d653b6be68c835a032e7552.
Preserve the complete MIT copyright notice for any substantial kit material.
Adult is CC BY 4.0 with Becker/Kohavi attribution; transformed proxy work is
described and rows are not redistributed. SIPP is Census public-use research
data, not competition data; record source/use without asserting a new blanket
license. TabPFN's own weight license stays with its historical package, never
relicensed under the team's code license. Runtime dependencies stay under
their own licenses; no dependency binaries are redistributed in final mains.

### New shared-process resource and parity results

Both unchanged archived predictors ran all three official phase-2 synthetic
frames sequentially in one process, using two numerical threads and CPU
(Python 3.13.14, torch 2.13.0+cpu). Official `check`, `floored`, and `score`
functions validated each result. Every one of 442425 raw vectors per model
equals its A012 reference exactly; these are complete comparisons,
not rounded-score parity. Frame hashes also match. E041's reference vectors
had already been re-compared with the original official archive predictions.
For E025 the A012 worker loaded the frozen assembled main, not modular source.
Thus its fresh equality is assembly-to-frozen-assembly. Its historical official
report preserves main/ZIP hashes and score parity to then-current source, but
no raw official vectors/scorer/data hashes. Historical official UNICEF/WB minus
A012 are +.000007983303/-.000012753036, cause unassigned. E025's historical
official qualification is retained with that limitation, not advertised as a
fresh official raw-parity certificate. E041's current full release checks are
stronger; no extra E025 refit was silently added to the registered compute plan.

| Model | Inclusive all3 seconds | Peak working set bytes | Peak commitment bytes |
| --- | ---: | ---: | ---: |
| E041 | 336.554468 | 1493135360 | 1604792320 |
| E025 | 332.782386 | 1469911040 | 1557315584 |

Inclusive time includes imports/model load, input construction, prediction,
official scoring and all-vector cache comparison. OS lifetime peak counters
include retained objects across successive instruments; not merely isolated
per-instrument memory maxima. E041 predicts in 37.874/86.829/191.594 seconds;
E025 in 36.751/88.179/188.200 seconds. Windows peak commitment and working set
are local process observations, not Linux cgroup/RAM or H100 VRAM guarantees.
Hidden-data optimizer duration, approximate gates and CPU/GPU numerical
differences remain unmeasured. Runtime cannot be forecast by simple linear
scaling from TRAIN to TRAIN+DEV or by this small timing difference.

E041 phase-2 synthetic activation: section indices 0,1,3,4,5,6,7 of eight;
fit1200/selection800/replay800/reference6100. This confirms the real learned
path executes in rehearsal, not hosted activation or its causal contribution.
Current paired clean deltas versus E025 remain 0/0/-.000508448996, satisfying
the preregistered absolute .002 release policy without implying transfer gain.

### Final archive verification, freeze and remaining limits

Final E041 ZIP extracted and freshly passed official `score.py --phase 2` on
all three schemas: .490197770701/.462029504790/.564665364947. All442425 raw
vectors exact to modular-source references, absolute .002 E025 gate PASS.
Official seconds sum359.448694, inclusive orchestration364.340160. Both final
ZIPs pass the official checker. Two four-page PDFs have clean text bounds and
all pages visually reviewed; E025 footer/title corrected to its own model.
Eight lightweight phase-2/resource-guard tests PASS. No production model edit.

Independent review found no high-severity defect and three medium issues;
all addressed in `A018-outputs/code-review.md`. Completed runs used preserved
`.executed.py` scripts. Future tools enforce remaining whole-run time, terminate
owned process trees and monitor memory during execution. These post-run guard
changes do not change measured results; initial enforcement limitations remain
disclosed. Total completed model-rehearsal wall1033.677015 seconds, plus the
aborted E025 attempt (under60s), below the registered35-minute cap.

| Role | ZIP | SHA256 |
| --- | --- | --- |
| Selected E041 | submissions/2026-09-25-E041.zip | bd5d2b7df3c39338f68cb08f125f85695073f37c9f4be3f6adcb8961941cd132 |
| Fallback E025 | submissions/2026-09-25-E025.zip | 142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f |

Matching methods: each dated source directory's `method-4p.pdf`. Their exact
hashes, freeze UTC timestamp, original-byte checks, executed/current verifier
hashes, rules evidence and complete artifact list are in
`A018-outputs/freeze-manifest.json`. Each ZIP contains unchanged main.py plus
LICENSE-starter-kit.txt only; the method is a separate attachment. Original
E025/E041 mains, ZIPs and preparation methods are preserved byte-for-byte.

Residual uncertainty: one noised favorable target pipeline reading is not
replication; internal base/replay optimism persists; TRAIN+DEV may alter fits
and selection; hidden approximate gates/populations differ from proxies; no
hosted H100 time/memory or actual TEST result exists. E025 historical official
provenance is weaker than E041's fresh certificate. Retired second-account
history is disclosed but no organizer adjudication is asserted. Public code
license remains an owner decision before award delivery. These limitations
are not repaired by synthetic parity, a draft license, or independent review.

Selection is frozen for this delivery. Future E056-derived work needs separate
production qualification and an explicit prospective reopening before the
Nov12 00:00UTC engineering cutoff. No automatic adoption, extra TEST upload,
ensemble or score-driven retry. User alone controls upload; none occurred.
