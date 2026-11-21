# A036 — E061 adverse hosted result: S0 disposition

Date: 2026-09-29 KST. Role: S0, document review only.
Decision: **ACCEPT_COMPARABLE_DECLINE_KEEP_PARKED**.
E041 incumbent/E025 fallback retained. Fixed E061 leaves the active retry queue;
this does not exclude all future parameter-sharing research or select TEST.

## Evidence and limits

Reviewed the [S2 handoff](E061-outputs/s2/post-result-handoff.ko.md),
[normalized user API object](E061-outputs/s2/user-reported-949956.json),
[result receipt](E061-outputs/s2/post-result.json),
[post-result verification](E061-outputs/s2/post-result-verification.json),
and the original/updated [scorecard](../../submissions/2026-09-28-E061/SCORES.md).
All 24 document hashes in S2's post-result verification match current files.
The verification file itself is separately identified in the
[entry](A036-outputs/entry.json). These are document checks, not release reruns.

| Released value | E041 ID933094 | E061 ID949956 | Difference |
| --- | ---: | ---: | ---: |
| Grand | .6433333333 | .6400000000 | -.0033333333 |
| UNICEF | .52 | .52 | .00 |
| World Bank | .49 | .49 | .00 |
| UNHCR | .92 | .91 | -.01 |

Both user-supplied records identify Finished, Development/phase29772 and the
same four score keys with precision2. This supports the preregistered
**Comparable Grand decline** arm at the supplied metadata level. Screen .64
equality is not API equality. UNHCR .91 is directly reported, not reconstructed.
S0 accepts S2's adverse operational reading for this fixed run.

No independent platform authentication was performed. E041's sanitized record
does not establish an identical hosted scorer version. Actual uploaded bytes,
remote hash and selected local path remain unconfirmed. No separate best-update
event was supplied; leaderboard membership is not update history. These gaps
remain explicit, without inventing a contradiction or exact artifact identity.

The differences are released readings, not unnoised causal effects. Additional
Grand decimals do not add measurement precision. Unchanged institution readings
do not prove identical hosted predictions. Tying, changed RNG consumption,
refitting and recomputed lambda are not separately identified by this comparison.

## Priority decision

The fixed candidate has no positive synthetic gain and now an adverse hosted
observation. This lowers its operational priority. Do not spend another slot or
fit on the same policy, a new seed, threshold/head rescue or an outcome-driven
partial reversal. Keep E061 parked and preserve its scientific and release records.

S1 qualification and S2 release PASS remain valid historical technical findings.
A qualified exploratory submission can fail to improve; that outcome does not
justify retroactively changing gates or requiring a synthetic gain as a universal
target-efficacy test. One agreeing direction between synthetic and hosted results
does not validate the synthetic proxy for UNHCR or refute the whole tying hypothesis.

DEV retention and TEST selection are separate. No E061 promotion evidence was
obtained; there is also no automatic permanent TEST exclusion or S3 reopening.

## Next recommendation, not execution authority

**Main:** one bounded S0 review of existing experiment records and released
institution-level API history, asking whether an untested mechanism has a
distinguishable, prospectively readable intervention. Proposed budget: at most
45 minutes of document review; no new web search, model/data access or candidate
implementation. This review was not executed as part of A036.

Its required output is at most one separate-S1 proposal specifying: the mechanism
and evidence; differences from prior tested/STOP/HOLD policies; opposing evidence;
an allowed observation channel and its exposure; fixed comparison and outcome
arms; and bounded implementation/whole-run cost. Lower absolute UNICEF/WB scores
alone do not justify changing institutional scope. An exploratory DEV proposal
need not claim an independent ERPIS efficacy oracle, but must label that limitation
and explain what its noisy observation can actually change.

**Backup:** if no defensible proposal passes that review, record the concrete
missing input and close the review. Do not start another identical HOLD review.
The VAF route resumes only on new identifiable provider documentation/approval
whose terms and metadata can be examined within a separate authorized scope;
approval alone is not permission for response access or model execution.

No new mechanism or executable S1 task has been established by this result intake.
Accordingly, A036 creates no S1 execution prompt, new candidate or E record.
This is not a blanket HOLD on all research. A materially new mechanism/input can
support a later scoped handoff. A concrete identity/execution discrepancy could
instead warrant a document provenance review, not an automatic rerun.

## Access, preservation and closeout

Workflow read receipt: revision2026-09-27-r4; ordered AGENTS/CLAUDE/status/latest
three log entries/workflow, followed by the named handoff and result documents.
Actual tool-read references, workflow SHA256 and initial document hashes are in
the entry. HEAD remains a43f4379ec78dbc2de260463eef67bb1d567d7e1.
CIM process inspection was denied; Get-Process showed no visible python/uv
processes. This limited check does not prove the whole machine idle.

Only A036 and status/log are written. Existing dirty work, tree, source, scorecards,
experiment records and prior manifests remain untouched. No protected responses,
Parquet/keys/NPZ/cache or ZIP were read/rehashed. No fit/predict/score, tests,
successful checks, platform access, upload, commit/push or S3/TEST action occurred.

Preserve E057/E060/E061 parked, E058 STOP/E059 STOP_SELECTION, A023/A024 empirical
HOLD and all other STOP/HOLDs. A_half remains unpromoted; A018 remains user-unconfirmed.
Preserve prior17999people/12339SSUID and aggregate exposure; A022 original roles
are not reassigned. E059 consumed oracle1918/1124 and selection2007/1130 remain
development evidence; audit2074/1177 and calibration1866 remain protected.
No new S2 candidate. [Document preservation check](A036-outputs/verification.json).
