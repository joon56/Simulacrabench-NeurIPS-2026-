# E049 independent release review

Date: 2026-09-23. Verdict: **No blocking findings for the frozen, technically qualified exploratory submission.** E049 remains parked; this review does not establish adoption, a hosted score forecast, or permission to describe forced activation as learned efficacy. No upload was performed by this reviewer.

## Scope and artifact identity

Reviewed E048/E049 registrations and oracle results, source-label isolation, E047 confidence helpers, final E049 production source, focused tests, AST assembly, archive verification, timing observer, forced active assembly fixture, and full-size forced active runtime. Independently checked the current source dependency digest, all five archive-member hashes, ZIP hash, checkpoint hash, official scorer hash, runtime script hash, and final manifest/result consistency. Model tests and expensive inference were executed by the implementation/validation agents; this reviewer inspected their code and recorded evidence rather than rerunning them. The cheap frozen-array normalization audit was rerun by this reviewer.

- Production source SHA256: `5ea710593814ea93cc86d7fd4c5f83bdb1bc3d89a7759decffeeb5ec1362bc77`.
- Full local source dependency digest: `9e5cce1907ea4e2712bdee91fa4be0f6a4b34f2492755c732b7931372632c18b`.
- Assembled main SHA256: `a15e497d90e9cd26ae16ce55901ead704d5457163047c4d090574f9641a56cb8`.
- ZIP SHA256: `8490852563a3b621346b8ab6633da4e593139cc3e418b2d5723cfcbf5feff19b`.
- Original V2 checkpoint SHA256: `f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f`.

The package is `submissions/2026-09-23-E049.zip`; its manifest is `submissions/2026-09-23-E049/verification.json`. Archive source and weights are unchanged through final verification. Requirements, license and attribution files match their manifest hashes.

## Final executed release evidence

Official `score.py` reports **PASS** for UNICEF, World Bank and UNHCR. Raw source/archive probability difference is exactly0 for every instrument. The ZIP checker passes. Official result and timing JSON files agree exactly with the final manifest.

| Instrument | Skill | Delta vs E041 | Delta vs E025 | Offline execution seconds |
| --- | ---: | ---: | ---: | ---: |
| UNICEF | 0.5006484230707156 | 0 | 0 | 47.32652340000095 |
| World Bank | 0.45471730736298255 | 0 | 0 | 112.13575479999963 |
| UNHCR | 0.5624627288576414 | 0 | -0.0004861448473750807 | 480.0544195000002 |

All clean outputs equal E041 exactly; both control instruments also equal E025 exactly. UNHCR's skill regression against E025 is below the registered `.002` guard. Honest clean selection rejects all four correction groups. The household diagnostic also rejects all groups and equals E041. These results provide pipeline and regression evidence, not measured efficacy.

Official execution totals **639.5166977000008s**, below900s. Full official elapsed time, including three fresh environment builds and grading, remains separately recorded as1059.8495259284973s. The timing wrapper executes untouched `score.py` with `runpy`; profiling observes entry/return of environment preparation and submission execution without changing arguments or results. Excluding dependency installation is consistent with the stated execution budget. Each measured submission interval includes child launch, import, checkpoint loading, prediction, serialization and collection.

The full-size active runtime artifact uses8279 visible rows,621 queries,213 predicted items and132273 output vectors. It runs the honest confidence fitter before overriding selection only to exercise all four final branches. Eight actual PFN fits occur, each with512 references. Official raw-vector, floored-vector and finite-score checks pass. UNHCR main import plus prediction is579.4750503000014s; all setup and validation included is594.3348814000001s. Adding separately measured official control times gives **753.7971596000007s**, below900s. The final manifest binds this artifact by SHA256 `1d8b0c739272e8b5bb5010d6364fc8ea42be98703d78fd26d5c319dc0de778a2`; the reviewer independently verified the hash and arithmetic. This is a local CPU observation, not a hosted runtime guarantee.

The smaller active assembly fixture executes16 actual PFN fits and produces exact source/archive parity. Its active source/E041 probability difference is `3.878835867107361e-6`; inactive vectors equal E041 exactly. Forced selection is explicitly labeled an engineering check in both active artifacts. Fifteen E049 tests and fourteen unchanged E047-helper tests are reported passing.

## Scientific and implementation assessment

E048's registered constant-mixture policy remains stopped: its tighter finite constant-section bound fails `.005` on both seeds. The historical permissive `oracle-summary.json` decision is explicitly superseded by `E048-outputs/decision.json`, preserving original evidence and hashes.

E049 reuses previously screened Adult rows and discloses that reuse. First-stage queries were excluded from logistic and PFN references; correction fit, selection and audit remain disjoint. Policy features are label-free; scaling/coefficients use correction-fit labels only. Selection and final audit guards use their assigned partitions. Audit-based acceptance prevents untouched-confirmatory interpretation. Adult's full-sample option vocabulary is disclosed schema emulation, not train-only vocabulary fitting.

The finite grid is a screening family, not by itself an upper bound on a continuous confidence policy. The supplemental continuous alpha `[0,.5]` oracle correctly contains the E047 policy and supplies a concavity tangent-gap certificate below `1e-15` nats. Both bounds apply only to the frozen Adult family; neither bounds actual UNHCR improvement or establishes learnability.

Review corrected finite-grid endpoint normalization to match E047's unchanged mixture family. Maximum floored-vector change was `1.1929834491775093e-8`; finite oracle skill/3 changed by less than `3.5e-11`. Corrected finite oracle gains are `.008298155185119671` and `.007547830320856301`; continuous gains remain `.008300688563294023` and `.007549227665776925`. Zero audit respondent/section oracle choices changed. Actual learned Adult skill gains remain `.0017394126947405386` and0. The grid, thresholds, policy and production artifact were unchanged.

Production applies seed4901 shadow masking before first-stage fitting, keeps all outer rows out of PFN references, uses GIVEN-only PFN inputs, selects complete-schema class counts including gate sentinels, and requires disjoint PREDICT descendant closures. Endpoint renderers share frozen first-stage products and evidence through private cached function globals. Full parent-belief replacement preserves existing descendant soft-routing coefficients. E047 policies freeze before final refit. Control/fallback paths delegate to immutable E041; final singleton roots preserve raw E041 vectors. No static leakage or routing blocker was found.

All initial findings are resolved or explicitly scoped. The evidence supports a technically qualified exploratory artifact only. It does not meet the `.005` adoption criterion or justify a `.65` forecast.
