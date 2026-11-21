# Calibrated survey completion with visible-row evidence

**REVIEW DRAFT — NOT FINAL TEST SELECTION**

HSCC / SimulacraBench 2026 | E025 preserved alternative | 23 October 2026

## 1. Task, evidence and schema handling

We predict categorical survey answers from each held-out respondent's GIVEN block for UNICEF Faith & Immunisation, World Bank Skills Assessment and UNHCR ERPIS. Every PREDICT cell is blanked and scored; EXCLUDE items are omitted. One self-contained predictor learns separately per instrument using complete visible respondents, combining hierarchical smoothing, a shared neural network, approximate skip logic and similar-row donor evidence. No fitted state is bundled.

E025 is a preserved alternative to provisional E041, not a user-selected final TEST model. Its historical user-reported DEV readings were Grand 0.63, UNICEF 0.52, World Bank 0.49 and UNHCR 0.89. E041's later released API record ID933094 reports 0.6433333333/0.52/0.49/0.92 (Grand displayed as 0.64). These retained readings remain subject to phase-1 Laplace noise and 0.01 rounding. Extra serialized decimals do not establish precise effects. They compare adaptively developed complete pipelines, not independent component trials. No real TEST score exists; E064 is parked awaiting DEV delivery, with no actual hosted result. [6,7]

Phase 1 shows TRAIN and scores DEV; phase 2 shows TRAIN+DEV and scores TEST. The pinned kit describes shuffled respondent roles, stratified by country for UNICEF and balanced by survey round/country for UNHCR, with ordinary permutation for World Bank. This is not a chronological or new-country holdout. Same-population split relevance does not guarantee refit gain or repair adaptive DEV selection. [1,6]

The official metric averages log probabilities over all scored cells within an instrument, then scales by schema-only uniform surprisal U. Grand is the equally weighted mean of the three instrument skills. K includes the sentinel for gated items. Confident errors are costly.

    p'_k = 0.001 + (1 - K*0.001) * p_k / sum_j(p_j)
    skill = 1 + mean_cells(log p'_[true answer]) / U
    U = mean_scored_items(log K_i)

Vectors follow schema item/option order, adding NA_GATED as the last option for gated items. NaN means predict; refusal and other non-response categories remain ordinary answers. Decoding passes parents' final beliefs, including donor evidence, to descendants. A visible parent gives a one-hot belief. For gated item i, r_i is parent mass on observed-if values.

    hard_i = [r_i * asked_conditional_i, 1 - r_i]
    base_i = a_i(x) * hard_i + (1 - a_i(x)) * full_i

Asked-conditional heads train on asked rows; unrestricted full heads include the sentinel. UNHCR gate agreement is approximate (median 0.83, range 0.29-0.98), so hard coupling can be wrong even with a known parent. Scalar agreement (k_i+20*m)/(n_i+20) shrinks toward median observed agreement m, not one. For each child, an internal 20% split can select one GIVEN column of cardinality at most 12; its value-specific rates shrink toward the scalar. Without improvement the scalar remains. [1,6]

<!-- pagebreak -->

## 2. Runtime prediction, donor matching and replay

**Hierarchical backoff.** A smoothed global marginal anchors a ladder, with each level adding a GIVEN column. Column order, depth up to three and kappa in {1,3,10,30,100} are selected greedily by held-out log score on 20% of complete visible rows. Candidate columns have at most 12 levels. Asked-only distributions use the same ladder; sparse cells borrow strength and unseen cells back off.

    p_L(v | cell) = (n_L(v) + kappa_L*p_(L-1)(v)) / (N_L+kappa_L)

**Shared trunk.** One-hot GIVEN inputs feed a Linear-ReLU network with softmax full heads for PREDICT items and separate asked-only heads for gated items. Masked cross-entropy pools observed full and conditional targets. Full-batch Adam uses learning rate 0.003, weight decay 0.0001, at most 500 epochs and patience 30 on an inner split. An outer split chooses two 64-unit layers/no dropout or two 128-unit layers/dropout 0.1. The selected epoch count is refitted on all complete visible rows. One instrument-level network/ladder mixing weight from {0,0.1,...,1} is selected on the outer split and shared by full and conditional heads. Fixed split and network seeds are zero.

**Visible-row evidence.** Every complete visible respondent is a potential donor, without a cross-round restriction. Matching uses GIVEN values, never respondent identifiers. Initial weights are -log(u_j), where u_j is random agreement estimated from available GIVEN frequencies, including held-out GIVEN covariates. That covariate use does not include held-out PREDICT responses.

A preliminary match identifies provisional pairs with top posterior mass at least 0.5. With at least 30 such pairs, one Fellegi-Sunter-style update estimates per-column agreement m_j; otherwise the rarity weights remain. Weighted GIVEN agreement is normalized with softmax over the top ten donors, whose answer vectors supply item evidence.

    weight_j = max(0, log(m_j/u_j) - log((1-m_j)/(1-u_j)))

This soft neighborhood can exploit ordinary similarity or near-duplicate structure; it does not establish household relationships or identities. An organizer ruling retained in the project allows matching within the supplied dataset without external identity linkage. We do not assert newly authenticated organizer correspondence or link to external records. [6]

**Concentration-specific calibration.** Self-excluded replay uses up to 6,000 complete visible queries. For each item, lambda is chosen from {0,0.1,...,0.9,0.95,0.98}, separately when maximum donor mass is below or at least 0.5. Each bucket requires 30 valid observations; insufficient support leaves lambda zero. The query is excluded as its own donor. The final update follows gate mixing and precedes descendants' decoding.

    final_i = (1-lambda_i) * base_i + lambda_i * evidence_i

No positive learned lambda means base-only prediction. No usable GIVEN signature supplies no evidence. GPU training exceptions can use CPU fallback; arbitrary whole-run failures and timeouts do not create a new TEST attempt. **E025 has no E041 learned section metric, 32-candidate reranking, metric-fit/selection/replay partition or section activation gate.** Its two-architecture choice, top-ten donors, replay cap and lambda grid are unchanged. [6]

<!-- pagebreak -->

## 3. Calibration limits, development evidence and phase-2 refit

Ladder selection, conditional agreement, architecture/epoch choice and network mixing use internal visible-row splits. Donor replay excludes self-matches, but base predictions are refitted on all visible rows, including replay labels. Self-exclusion therefore does not cross-fit calibration, and replay performance is not an unbiased generalization estimate. No E041 partitioning is implicitly credited to E025, and no repair of this optimism is claimed.

Algorithm choices and grids were developed through synthetic work, public instrument descriptions and repeated DEV feedback. Parameters are estimated at runtime, but the retained method was selected adaptively during development. Legal TRAIN+DEV final fitting does not make those DEV observations independent again. Fixed seeds do not prevent row-order, CPU/GPU or reduction-related numerical variation. [6]

Complete phase-2 visible counts grow to 16,373 UNICEF, 5,715 World Bank and 8,900 UNHCR respondents. Every fitted component is rebuilt from that frame: adding DEV can change marginals, asked-only heads, ladder order/shrinkage, network architecture/epochs/mixing, gate coefficients, agreement weights and replay lambdas. The larger visible bank may help or hurt; no linear runtime or gain forecast follows. Larger replay caps, ensembles, identifier signatures, tree blends and relation-specific evidence variants are not part of this predictor.

**Development counterevidence.** Six later hosted comparisons were flat at displayed resolution: evidence as network input (E027), parent-value gate decoding (E028), larger replay (E031b), relation-specific weights (E036), identifier signatures (E038) and a tree blend (E040). Simulation gains under injected assumptions did not establish transfer. E037 sentinel recalibration gained about 0.024 in-sample on a heavy-overlap simulation but lost about 0.004 under cross-fitting and was rejected. These observations neither prove zero possible improvement nor justify another same-policy attempt. [6]

E032-E034 aggregate UNHCR probes describe E025 only: approximate skill 0.79 from the base plus 0.10 from evidence, with remaining loss about 0.079 gated/0.031 ungated. Keeping sentinel mass while flattening asked answers left gated skill near 0.56. These are model-performance summaries, not private response statistics or an E041 decomposition. Rounded/noised same-phase Grand differences imply coarse practical UNHCR resolution, about 0.015-0.03, not three-decimal precision. E032 initially changed all instruments and used a second account, later retired and flagged as a likely Terms violation. No adjudication, waiver or independent replication is asserted. [6]

Separate Adult/SIPP studies address limited proxy channels. E053 and E055 oracle STOPs do not bound approximate UNHCR calibration; later E056-E059 supplied no deployed component. E059 STOP_SELECTION and A_half nonpromotion remain. Later E060/E062/E063 released ties leave effects unresolved; E061's adverse result applies to that complete pipeline. E064 local qualification supplies no actual hosted score. No result from these alternatives changes this draft's E025 identity or final-choice status. [6,7]

**Engineering scope.** Public synthetic phase-2 TEST-role cells were previously exposed development material, not newly independent real TEST evidence. The completed E025 provenance task below closes a concrete source/archive/data/scorer connection; it does not validate hidden humanitarian population structure, establish E025 superiority or remove selection/calibration uncertainty. No raw response values appear in this document.

<!-- pagebreak -->

## 4. New provenance, reproducibility and external-material disclosure

On 23 October a separately authorized S3 ran unchanged modular E025 once across all three instruments and the preserved archive once with the stock official scorer. All 442,425 ordered raw vectors were exactly equal; width, finite/nonnegative values and positive sums passed, and official phase 2 passed all three schemas. The pre-model E041 reuse gate checked exact input/frame/order/source/scorer/completion identities and recorded Python/six-package versions. E041 was not rerun. [7]

| Instrument / cells | E025 skill | E025 minus reused E041 |
|---|---:|---:|
| UNICEF / 41,676 | 0.490197770701 | 0 |
| World Bank / 92,112 | 0.462029504790 | 0 |
| UNHCR / 308,637 | 0.565173813942 | +0.000508448996 |

All absolute differences are at most 0.002 under the same truth/order/floor.001 engineering criterion. This is no TEST-ranking claim. Source/official whole-all3 walls were 429.930/450.277 seconds, each below a shared 900-second local cap, CPU2/GPU0. Maximum sampled tree RSS/private across them were 2.035/2.067 decimal GB; final samples counted, maximum gap 0.221341 seconds. No instantaneous or hosted peak guarantee follows. Source raw was frozen before dedicated truth evaluation; stock official truth sequencing remained unchanged and its predictor saw only masked frames. The identical ZIP/checker's previous PASS was reused. [7]

Older E025 official-minus-A012 UNICEF/WB drift (+0.000007983303/-0.000012753036) remains unexplained. A012 provenance was collected after fitting, with historical PyYAML/threadpoolctl/OS/native-library/affinity omissions. A018's assembly-only parity, aborted concurrent work and later guard repairs remain historical. The new modular/archive connection does not rewrite those records. Hidden-data runtime, GPU behavior and private hosted versions remain unverified. [6,7]

The exact predictor is submissions/2026-09-25-E025/main.py. document-pairing.json links its SHA256, inherited ZIP identity and new Markdown/PDF hashes; no ZIP was opened or rehashed here. Retained certificates list main.py and the full starter MIT notice only. Runtime uses hosted NumPy/pandas/PyTorch/scikit-learn. No external rows, pretrained weights, fitted artifacts, models.txt or network calls are bundled. Visible-row fitting/internal selection/refit consume the same saved public 3,600-second Final clock; the historical H100/eight-CPU/16-GB contract does not certify the current private environment. [1,6,7]

**External development disclosure.** Separate work used recoded/profile-constrained UCI Adult (Becker and Kohavi, 1996; CC BY 4.0), Census 2023 SIPP public-use observations and Prior Labs TabPFN V2 experiments. A040 used TabICLv2 for fake-data technical work. VAF/HOST document/header intake left empirical linkage/asked-state work on HOLD. None of those rows, weights, outputs or proxy-fitted artifacts enters E025/E041; their unchanged lineage predates later SIPP/TabICL/VAF work. Survey descriptions informed hypotheses, not fitted response priors. No access approval is treated as redistribution permission. [3-6]

Starter MIT and third-party notices remain intact; runtime software retains its own licenses. TabPFN's Prior Labs License 1.1 has extra attribution conditions and is not team MIT. Team-code rights holders and license scope remain undecided. The prior scoped MIT proposal is not effective; this draft grants no rights or whole-repository publication permission. Retained public dates are DEV through 13 November and Final 14-18 November 2026, with exact timestamps/timezone and latest Terms unconfirmed. Website winner-only method wording differs from September's every-TEST-entry clause. Final model, rights, current obligations, account/slot and upload need separate decisions. [2,6]

**References and evidence.** [1] [Pinned public kit f980ef5](https://github.com/SituatedEvals/public/tree/f980ef5059360fcf977ed7971af5c00ee5c1962f). [2] [Official site](https://simulacrabench.org/) and [Codabench](https://www.codabench.org/competitions/17822/), retained snapshots only. [3] [Adult, UCI](https://archive.ics.uci.edu/dataset/2/adult). [4] [Census 2023 SIPP](https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html). [5] [TabPFN license](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt). [6] A018 and A044 s3-prep methods, rules and license inventory. [7] A044 s3-e025-provenance closeout/comparison and S0 acceptance, 23 October 2026. No new web fetch; exact documentary sources are in evidence-map.md.
