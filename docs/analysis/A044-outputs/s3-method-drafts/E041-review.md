# Calibrated survey completion with section-specific retrieval

**REVIEW DRAFT — NOT FINAL TEST SELECTION**

HSCC / SimulacraBench 2026 | E041 provisional reference | 23 October 2026

## 1. Task, evidence and approximate gates

We predict categorical PREDICT answers from held-out respondents' GIVEN blocks in UNICEF Faith & Immunisation, World Bank Skills Assessment and UNHCR ERPIS. EXCLUDE items are omitted; every hidden PREDICT cell is scored, including gated sentinels. Phase 1 shows TRAIN and scores DEV; phase 2 shows TRAIN+DEV and scores TEST. The pinned public kit describes seeded respondent shuffling, stratified by country for UNICEF and balanced by survey round/country for UNHCR, with plain permutation for World Bank. This is not an unseen-country or chronological holdout. [1,6]

One self-contained predictor fits separately per instrument at runtime. E041 adds supervised section retrieval for UNHCR; UNICEF and World Bank use E025 unchanged. It bundles no fitted weights or external response data. E041 is a DEV incumbent and provisional TEST reference. The user has not confirmed a final TEST model. E025 remains a separately preserved alternative, and E064 is parked pending a user-controlled DEV submission, with no actual hosted result yet. [6,7]

The user-provided released E041 API record ID933094 reports Grand 0.6433333333, UNICEF 0.52, World Bank 0.49 and UNHCR 0.92; the interface displays Grand 0.64. E025 historically read 0.63/0.52/0.49/0.89. These values come from retained development records, not a new platform query. Phase-1 Laplace noising and 0.01 rounding still apply: serialized decimals do not provide ten-decimal measurement accuracy. This adaptively developed pipeline comparison is neither an isolated retrieval-metric effect nor independent replication. No real TEST score is available. [6]

The grader normalizes each raw vector, then enforces floor f=0.001 by mixing uniform mass. The metric pools cells within an instrument; Grand gives the three instrument skills equal weight.

    p'_k = f + (1 - K*f) * p_k / sum_j(p_j)
    skill = 1 + mean_cells(log p'_[true answer]) / U
    U = mean_scored_items(log K_i), including the gate sentinel

Vectors follow schema item and option order, with NA_GATED last for gated items. NaN marks a target; refusal remains an ordinary answer. Parents decode before descendants, and visible parents give one-hot beliefs. For a gated item i, r_i is parent mass on observed-if values; asked-only and unrestricted full heads are mixed as follows.

    hard_i = [r_i * asked_conditional_i, 1 - r_i]
    base_i = a_i(x) * hard_i + (1 - a_i(x)) * full_i

UNHCR schema agreement is approximate (median 0.83, range 0.29-0.98). The scalar coefficient (k_i+20*m)/(n_i+20) shrinks toward median observed agreement m, not one. At most one GIVEN column of cardinality at most 12 is selected per child on an internal 20% split; value-specific rates shrink toward that scalar. This avoids treating an approximate survey gate as deterministic. [1,6]

<!-- pagebreak -->

## 2. Base predictor and section-specific evidence

**Hierarchical backoff.** A smoothed global marginal anchors a ladder adding GIVEN columns. On a 20% visible split, greedy held-out log score selects column order, depth up to three and shrinkage kappa in {1,3,10,30,100}. Candidate columns have at most 12 levels. Asked-only heads use the same ladder; unseen cells fall back to broader cells.

    p_L(v | cell) = (n_L(v) + kappa_L*p_(L-1)(v)) / (N_L+kappa_L)

**Shared neural trunk.** One-hot GIVEN inputs feed a Linear-ReLU trunk and separate softmax full heads, plus asked-only heads for gated items. Full-batch Adam uses learning rate 0.003, weight decay 0.0001, at most 500 epochs and inner-validation patience 30. An outer split selects two 64-unit layers/no dropout or two 128-unit layers/dropout 0.1. The selected epoch count is refitted on all complete visible rows. One instrument-level network/ladder mixture weight from {0,0.1,...,1} is selected on the outer split and applies to both head types. Base split and network seeds are zero.

**E025 donor evidence.** All complete visible respondents are potential donors. GIVEN agreement starts with negative-log random-agreement weights, using available GIVEN frequencies including held-out covariates. At least 30 provisional pairs with top posterior mass at least 0.5 permit one Fellegi-Sunter-style agreement-weight update; otherwise rarity weights remain. Softmax over the top ten donor candidates averages their answer vectors. Respondent IDs are not features; this is not external identity linkage or proof of household relationships.

Self-excluded replay over at most 6,000 visible queries chooses item-specific lambda from {0,0.1,...,0.9,0.95,0.98}, separately below/above maximum donor mass 0.5. A bucket requires 30 observations; insufficient support leaves lambda zero. The final belief (1-lambda)*base + lambda*evidence is applied after gate mixing and before descendants decode. No positive lambdas means base-only prediction.

**E041's additional UNHCR layer.** PREDICT items are grouped by section-name prefix. Each section learns nonnegative diagonal weights on GIVEN equality features and reranks 32 candidates retrieved under the initial E025 metric. Seed 4101 partitions complete visible rows into metric-fit (up to 1,200), selection (up to 800), new-metric replay (up to 800), and a disjoint reference bank. Query labels fit the metric; reference-bank labels supply donor evidence. No hidden PREDICT labels enter these roles.

Metric fitting optimizes officially floored log loss plus squared-distance regularization toward initial weights (penalty 0.001), using L-BFGS-B for at most 50 iterations. Weight bounds are [0,12]; a sigmoid parameter controls a fitted proxy mixture share. Selection compares learned 32-candidate evidence with initial-metric top-ten evidence. A section activates only if mean log gain exceeds max(0.003,2*estimated SE). This heuristic is not a multiple-testing-adjusted population guarantee.

Active sections replace evidence and choose their item/bucket lambdas on new-metric replay rows; inactive items retain legacy replay. Deployment uses the full visible donor bank. Concentration buckets still use initial top-ten posterior mass. Dispatch requires the exact schema key s3_11_intent_return_12m_lbl; fewer than 500 complete rows or no held-out rows invokes legacy evidence, and no usable GIVEN signature returns no evidence. Historical synthetic phase 2 activated seven of eight sections; hosted activity is unknown. [6]

<!-- pagebreak -->

## 3. Refitting, evaluation limits and engineering evidence

Disjoint metric-fit/selection/replay queries do not cross-fit the entire pipeline. Base distributions are refitted on all visible rows, including replay labels; donor self-exclusion does not remove that calibration optimism. The selector uses a marginal/evidence proxy and fitted mixture share that differ from deployed recursive base distributions and item lambdas. Repeated DEV feedback also influenced method retention. Legal reuse of DEV for final fitting does not restore independent validation.

Phase-2 visible counts become 16,373/5,715/8,900. For UNHCR the reference bank grows from 5,479 to 6,100 while caps 1,200/800/800 remain. No trained state is frozen: adding DEV can change architecture, epochs, ladder/gate choices, rarity/agreement weights, partition membership, active sections and lambdas. Fixed seeds do not remove row-order or numerical-reduction sensitivity. GPU training exceptions can fall back to CPU; an arbitrary failure or timeout does not swap the whole model to E025 or create another TEST attempt. [6]

Counterevidence includes historical E041-minus-E025 UNHCR skill of -0.000486 on phase-1 synthetic data and -0.002026 on a household simulation. Adult audit gains +0.000595/+0.000427 had paired intervals including zero; Adult lacks UNHCR's approximate gates. A011 replay contrasts did not establish recoverable gain. E053 ungated-Adult and E055 exact-gate-SIPP oracle STOPs are scoped bounds, not UNHCR ceilings. E056-E059 supplied no deployed component; E059 STOP_SELECTION and the ban on promoting A_half remain. Later E060/E062/E063 released ties leave effects unresolved; E061's adverse reading applies to its complete pipeline. E064 engineering qualification is not a hosted result. [6]

**New E025 provenance, reused E041 reference.** A separate authorized S3 run on 23 October established unchanged modular E025 versus its preserved ZIP: all 442,425 ordered probability vectors were exactly equal, vector validity passed and stock official phase 2 passed all three instruments. Before models, the E041 frozen-raw reuse gate checked exact input/frame/order/source/scorer/completion identities and recorded Python/six-package versions. E041 was not rerun. [7]

| Instrument / cells | E025 skill | Reused E041 skill |
|---|---:|---:|
| UNICEF / 41,676 | 0.490197770701 | 0.490197770701 |
| World Bank / 92,112 | 0.462029504790 | 0.462029504790 |
| UNHCR / 308,637 | 0.565173813942 | 0.564665364947 |

E025-minus-E041 is 0/0/+0.000508448996, within the fixed absolute 0.002 engineering criterion for each instrument. It does not establish E025 TEST superiority or select either model. The new E025 source/official whole-all3 walls were 429.930/450.277 seconds under separate shared 900-second local caps, CPU2/GPU0. Maximum sampled tree RSS/private were 2.035/2.067 decimal GB, with final samples checked and largest sample gap 0.221341 seconds. These are local sampled observations, not instantaneous or hosted guarantees. [7]

Historical E041 A018 all3 took 336.554 seconds, with working-set/commitment peaks 1.493/1.605 GB; final archived official scoring took 359.449 seconds (364.340 seconds orchestration). These measurements have different scopes and dates and are not a controlled speed comparison with the new E025 run. A012 provenance was collected post-run; historical environment omissions and older E025 UNICEF/WB drift remain unresolved. [6,7]

<!-- pagebreak -->

## 4. Reproducibility, disclosure and pending delivery decisions

This method describes unchanged submissions/2026-09-25-E041/main.py. The companion document-pairing.json records its full SHA256 and links this draft's Markdown/PDF to the inherited preserved ZIP identity. ZIP bytes were not opened or rehashed for this document task. The package contains main.py and the complete starter-kit MIT notice, according to retained certificates. No requirements.txt, models.txt, fitted artifact, external dataset, pretrained weight or network call is bundled. Runtime imports use NumPy, pandas, PyTorch and scikit-learn, plus SciPy and threadpoolctl for E041. Exact private hosted versions and native GPU behavior remain unverified. [6,7]

The retained public rules and user-supplied organizer clarification permit visible-row fitting, internal selection and refit within the same execution clock. The saved public Final contract is 3,600 seconds shared across imports and all three instruments, with eight CPUs, one H100 and 16 GB RAM. Local CPU measurements do not certify the private image, hidden-data activation or execution time. This review session performed no model import, fitting, scoring, raw/data/cache access or new ZIP work.

**External work used during development.** Recoded, profile-constrained UCI Adult observations (Becker and Kohavi, 1996; CC BY 4.0) and Census 2023 SIPP public-use observations supported separate proxy studies. Prior Labs TabPFN V2 weights were used in separate experiments. A040 used TabICLv2 for separate fake-data technical work. VAF/HOST document and approved-header intake did not resolve empirical linkage/asked-state HOLD. None of those rows, weights, outputs or proxy-fitted artifacts enters E041 or E025; the unchanged predictors predate later SIPP/TabICL/VAF work. Public survey descriptions informed hypotheses, not fitted response priors. No access approval is treated as redistribution permission. [3-6]

**Development exposure and failures.** Internal split selection and repeated DEV feedback influenced the retained pipeline; not every development choice was prospectively fixed. E032-E034 aggregate component probes describe E025 only, not an E041 loss decomposition. E032's initial reading used a second account, later retired and recorded as a likely Terms violation; no organizer adjudication, waiver or independent replication is asserted. A012 scored before some raw saves, and its supplementary provenance followed fitting. A018 retains an aborted concurrent run and post-run guard repairs. The new E025 source outputs were frozen before dedicated truth evaluation; its stock official scorer retained the original truth-handling sequence and gave only masked frames to the predictor. Historical failures are not erased. [6,7]

**Rights and delivery remain open.** The starter-kit MIT notice stays intact; third-party runtime software retains its own licenses. Prior Labs License 1.1 includes additional attribution conditions and is not team MIT. Actual team-code copyright holders and a scoped grant remain owner decisions. The earlier MIT proposal is not effective; this draft grants no license or whole-repository publication permission.

The retained October public snapshot lists DEV through 13 November and Final 14-18 November 2026, as dates only. Current platform timestamps/timezone and latest Terms are unconfirmed. Website winner-only method wording differs from September Terms requiring a method for every TEST entry; this task does not resolve that conflict. Final model, source-license scope, current obligations, account/slot and upload remain separate decisions. The old November 14 00:00 UTC closing claim is not reused. [2,6]

**References and evidence.** [1] [Public kit, pinned f980ef5](https://github.com/SituatedEvals/public/tree/f980ef5059360fcf977ed7971af5c00ee5c1962f). [2] [Official site](https://simulacrabench.org/) and [Codabench](https://www.codabench.org/competitions/17822/), retained snapshots only. [3] [Adult, UCI](https://archive.ics.uci.edu/dataset/2/adult). [4] [Census 2023 SIPP](https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html). [5] [TabPFN weight license](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt). [6] Repository A018 and A044 s3-prep records: prior methods, rules, license inventory and limitations. [7] A044 s3-e025-provenance closeout/comparison and S0 acceptance, 23 October 2026. Web links are cited from retained records, not freshly fetched. The companion evidence-map.md locates exact documentary sources.
