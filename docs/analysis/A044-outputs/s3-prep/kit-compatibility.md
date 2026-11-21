# S3-PREP-A044 — public kit compatibility

Old A018/local HEAD: `ee427a94f6cc6a0d9d653b6be68c835a032e7552`.
Current official main observed: `f980ef5059360fcf977ed7971af5c00ee5c1962f`,
commit date2026-10-08T02:31:57Z, message “Clarified row shuffling”.
Evidence: saved [commit metadata](upstream-commit.json), [official compare](upstream-diff.json),
[local/current hashes](kit-hashes.json), [A018 identity checks](identity-checks.json).
No fetch/pull, external checkout edits, imports, tests or generator execution.

Local Windows files and saved upstream UTF-8 text differ in byte hashes due to
CRLF/LF on otherwise identical files. `lf_text_equal` explicitly compares text
after CRLF→LF only, preserving ordering and all other characters. This is not
byte equality. The GitHub compare independently reports no changes to scorer,
three schemas, checker, requirements or license between the pinned commits.

| Boundary | Observed comparison | Decision for old phase2 / B01 |
|---|---|---|
| Schema items/options/order/gates/split | All three full schema texts equal after newline normalization | Compatible; no new item/gate/order boundary to revalidate |
| Mask and role selection | score.py text equal; whole hidden PREDICT block becomes NaN; visible TRAIN(+DEV) complete; canonical row then item order unchanged | Compatible; do not regenerate roles or expose protected rows |
| Runtime schema normalization | make_sandbox diff is8 added docstring lines only; `load_schema` injects config.gated_value, options append sentinel for gated items | Executable behavior unchanged; raw JSON lacking top-level sentinel is normal |
| Probability floor / normalization | score.py unchanged: normalize p, then `.001+(1-K*.001)*p` | Compatible; no clipping-only substitute |
| Pooled denominator and score | Cell-mean logp; U=mean logK over scored items including sentinel; skill1+logp/U; Grand mean of3 | Compatible; old score certificate remains scoped to old inputs, not new TEST efficacy |
| API / checker / requirements | `predict(frame,schema)` and full checker text equal after newline normalization; requirements unchanged | No new API/package rerun justified solely by upstream changes |
| Resource / offline contract |900/3600 shared seconds,CPU8/RAM16GB/H100x1/offline unchanged | Local CPU evidence is not hosted resource certification |
| Config | Only3 added calendar keys in official compare | Recheck schedule; no model or score invalidation |
| Generator | Documentation added before assign_roles; no executable change. `trait_scale:2.0` already in old local config | No new generator default; do not regenerate existing frozen synthetic inputs |
| README / FAQ | Added date table and randomized respondent-role clarification | Update generalization discussion; no new response evidence or model family |

README/FAQ say roles were assigned after a fixed-seed shuffle: UNICEF stratified
by country, UNHCR balanced by survey round/country, WB plain permutation. No country
is held out. Thus chronological or new-country TEST shift must not be asserted as
the intended split. This supports same-population validation relevance, not an
independent gain estimate for E041 or a guarantee after adaptive DEV selection.

## B01 reuse decision

**COMPATIBLE for the inspected public contract.** E064's completed S1 is not
invalidated by these document/calendar changes. The S2 executor may reuse this
comparison after checking pinned identity and its own handoff entry gates. It must
still establish authorized input/raw/source/environment provenance under B01;
this S3 deliberately did not open/re-hash NPZ, Parquet, keys or caches.

**UNKNOWN:** exact currently deployed private scorer/image/version and current
Codabench Terms; mutable hosted dependencies, native GPU numerics and hidden-data
runtime. These were not silently certified by comparing public source. Any actual
semantic contract change discovered at execution entry goes back to S0 with the
affected boundary; do not automatically repeat all S1 work.

Both E041/E025 archives omit requirements.txt and use hosted preinstalls. README
explicitly lists NumPy/pandas/PyTorch/scikit-learn/SciPy. E041 also directly imports
threadpoolctl, normally a scikit-learn dependency but not explicitly listed in the
hosted table. Historical successful imports do not prove future image identity.
Do not add pins or rebuild ZIPs in this document task; record the environment gap.
