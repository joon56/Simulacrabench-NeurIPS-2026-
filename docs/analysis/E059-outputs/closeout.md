# E059 closeout - paired increment fails selection guard

**STOP_SELECTION; audit unopened.** B_half passed the E041 comparison, but its
increment over the matched additive control did not exceed2SE. Both comparisons
were required. Retain R; no automatic promotion of A or B and no S2 candidate.

## Observations

| Stage | B_half minus R | B_half minus A_half | Registered result |
| --- | ---: | ---: | --- |
| Oracle delta skill | +.000581212357158 | +.000035103682240 | Both >1e-10; continue |
| Selection delta skill | +.000401117267398 | +.000009324998360 | Descriptive conversion of the log contrasts |
| Selection mean log difference | +.000417438208276 | +.000009704420438 | Both positive |
| Selection cluster SE | .000165281866166 | .000012167985061 | Only first contrast passes mean>2SE; STOP |
| Audit | Unopened | Unopened | No estimate or bootstrap interval |

Oracle1918people/1124SSUIDs; selection2007/1130; audit2074/1177. All fixed A019
roles,7 heads pooled. R/A_half/B_half oracle skills:.627550414239/.628096522914/
.628131626596; selection:.640874352695/.641266144964/.641275469963. These are
public SIPP proxy results, not hosted scores or humanitarian gain forecasts.

This comparison conditions on frozen original first-order weights, donor32,
lambda pairs, concentration buckets, base and parent. R contrast includes the
additive replacement as well as beta. The beta-specific comparison failed the
registered guard; the positive R comparison cannot establish a beta benefit.
No alternate family, favorable seed, threshold change or extra diagnostic arm.

## Implementation and technical evidence

New scripts/screen_e059.py and tests/test_e059_interactions.py only. Production
sources/submissions/E058/A019 unchanged. Original active=[] preserved; separate
A/B research outputs use only original lambda-positive BIR/OTH/COR leaves.
All other heads/zero buckets retain exact R. Query donor32 computed once under
the unchanged GIVEN-only candidate rule and frozen for A/B; metric donor32
reused from the existing cache.15 lexicographic pair terms; no pool expansion.

Preflight:59 source hashes and5 artifact hashes PASS;11921 rows=5922fit+5999query,
masked query labels, original inner roles, schema/options, legacy lambdas,
saved signatures/weights/share, group roles, donor membership and R/library
alignment verified. Pair features not all donor-constant, allowing one fit.
Original5922 fit labels only; objective uses1184 metric-fit and3554 reference
rows. Stored inner selection/replay labels were not rescored.

10 fixtures PASS in4.87s: pair order/gradient/beta0, direct leaf mixture algebra,
unchanged heads/buckets, donor/query isolation, official floor, cluster SE,
shared-draw bootstrap and exclusive stage guards. Expected RED first confirmed
the missing module. No optimizer or real cache in tests. No real-stage errors.

Beta optimizer ran once,3 iterations, successful projected-gradient convergence.
Beta0=A exact; R identity and unchanged heads/buckets exact; direct algebra
maximum error1.1102230246251565e-16 versus registered1e-12. Algebra reconstructs
G from R/legacy evidence and lambda; G was not independently persisted by E058.
Unchanged source structure justifies the leaf equation; no fresh full renderer
was invoked. Raw validity checked without clipping negative values.

Before any outer response: R,A_half,B_half frozen; changed B vectors8839/41993
against R and8876/41993 against A_half. Finite-output, label-free oracle upper
bounds were.009801188698 and.000698872391; neither proved the gate impossible.
They concern only these trained/frozen outputs, not all beta or UNHCR.

## Resources and exposure

| Monitored stage | Parent-inclusive wall seconds |
| --- | ---: |
| Semantic preflight + donor construction |5.9118325 |
| Beta + rendering + freeze |5.2712132 |
| Oracle |5.0838697 |
| Selection |4.8498749 |
| Total, each stage import included |21.1167903 |

Beta optimization.0229319s; new base fits0, beta fits1. Peak aggregate process
tree RSS512618496bytes (.477GiB), commitment531894272bytes (.495GiB), sampled.2s
with parent harness and owned descendants. CPU2;8GiB and120s beta caps respected.
No GPU/install/paid resource. Local sequential-stage cost, not official all3.
Session starts conservatively12:10UTC; final verification timestamp is recorded
in session-close.json. Reading/coding/testing/recording counted toward60min.

Oracle and selection responses now consumed development evidence. Audit remains
unopened; no new CI. Old nonfit roles/calibration1866 remain closed. Same source
had prior aggregate exposure and E058 GIVEN query use; no independent-new-data
claim. See exposure-ledger.md. No real private DEV/TEST access.

## Frozen provenance and commands

Actual HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd, unchanged. A020 documents were
already uncommitted at entry. Local E059 changes are also deliberately uncommitted;
no staging, commit, push, ZIP, method, official all3 or upload this session.

| Artifact | SHA256 |
| --- | --- |
| Original registration.md |0de9835b3053a5410e98ec5a1327c60aabfc0587071efb52725c4c7d44d8dc9a |
| scripts/screen_e059.py |31ee84558932e3ef45871c6b53919ec59882044f8fec57ba4635e2242712c5f2 |
| tests/test_e059_interactions.py |746d52ed0de056d5789441c2df6f9bf0c70767638c2b9e765f019bc29e82e65c |
| external/e059/prepared.pkl |fe4e0889ba9a23d139d5c265df48167e00d267fc5a3e0a45f25c7efe7b6d9102 |
| external/e059/library.npz |56748de6d0ad5a0323476a0b19aed87f79d7d4aabbc227888efc7196ad70a187 |

preflight.json binds original data,5 artifacts, code and donor-order hashes;
fit.json binds learned beta, output and registration. oracle/selection.json bind
their ignored score arrays. verification.json checks frozen files and unopened
markers without any new labels or rescoring. Row data stays ignored external/e059.

Executed commands, from repository root:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_e059_interactions.py -q
.venv/Scripts/python.exe scripts/screen_e059.py run preflight
.venv/Scripts/python.exe scripts/screen_e059.py run fit
.venv/Scripts/python.exe scripts/screen_e059.py run oracle
.venv/Scripts/python.exe scripts/screen_e059.py run selection
.venv/Scripts/python.exe scripts/render_tree.py
```

Historical execution record, not permission to repeat. Exclusive markers refuse
reruns. Audit is forbidden by this STOP. Do not delete markers or extend deadline.
Documentation-only tree generation initially rejected the new title's hyphen;
the live record title was corrected to the required em dash and tree generation
completed. Immutable registration bytes stayed unchanged; no study stage reran.

## Disposition and S0 decision

Local technical checks PASS within this research scope. Two-comparison research
gate fails; release policy, DEV exploration qualification and TEST adoption are
not established. No automatic A promotion or S2 delivery. Follow-up needs a new
S0 decision that acknowledges the failed incremental comparison and consumed
oracle/selection roles. Do not open audit to rescue this study.

E041 incumbent/E025 fallback, E057 parked, E058/prior STOPs, S3 stopped and A018
user-unconfirmed state preserved. All owned workers finished. No backup started.
Next-session prompt: s0-handoff.ko.md.
