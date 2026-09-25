# Calibrated survey completion with visible-row evidence

HSCC / SimulacraBench 2026 | E025 method for phase 2

## 1. Task and evidence

We predict categorical survey answers from each held-out respondent's GIVEN
block. Every PREDICT cell is hidden; EXCLUDE items are omitted. The three
instruments are UNICEF Faith & Immunisation, World Bank Skills Assessment,
and UNHCR ERPIS. We submit one self-contained predictor that learns separately
on each instrument's visible respondents, combining hierarchical count
smoothing, a shared neural network, approximate skip logic, and evidence from
similar visible rows.

The official score is skill = 1 + log_score / U, where log_score averages
log probabilities over scored cells and U averages log K over those cells;
K includes the gate sentinel when applicable. Grand is the unweighted mean
of the three instrument skills. Instruments therefore have equal weight
despite different item counts. The grader normalizes predictions and mixes
them with uniform probabilities to enforce a 0.001 floor. A confidently
wrong answer can cost about 6.9 nats. Probability calibration matters more
than modal accuracy.

The preserved fallback is E025: phase-1 Grand 0.63, with UNICEF 0.52, World Bank
0.49, and UNHCR 0.89. These are noised, rounded leaderboard readings, not
exact estimates. No phase-2 real-data score is available. Local results use
the public kit's synthetic data and official scorer [1]. Synthetic gains
establish implementation behavior; they do not establish real-data structure.
Household simulations test named mechanisms under injected assumptions.
Separate leaderboard comparisons assess transfer at limited resolution.

## 2. Schema handling and approximate gates

Answer vectors follow schema option order, with an extra final NA_GATED slot
for gated items. NaN marks a prediction target; refusals remain ordinary
answers. The predictor decodes items in schema order, propagating each
parent's belief, including any evidence update, to downstream children.
A visible parent has a one-hot belief. For gated item i:

    r_i = sum of parent probability over observed_if values
    hard_i = [r_i * conditional_i, 1 - r_i]
    base_i = a_i(x) * hard_i + (1 - a_i(x)) * full_i

Here conditional_i is trained on asked rows only; full_i includes the
sentinel. UNHCR's published schema reports approximate gates (agreement
median 0.83, range 0.29-0.98). Consequently, forcing the schema gate can be
wrong even when its parent is known. The agreement coefficient a_i(x)
softens this constraint using observed parent-child agreement.

The scalar rate is (k_i + 20 * m) / (n_i + 20), where m is the median
observed agreement across gated items. This is shrinkage toward the
instrument's agreement level, not necessarily toward one. For each child,
at most one GIVEN column with cardinality at most 12 is selected by
Bernoulli log likelihood on a 20% internal split. Its value-specific rates
shrink toward the scalar. If no column improves the split score, the scalar
remains. Exact gates recover hard coupling. This handles varying sentinel
coding without asserting that an approximate survey gate is deterministic.

<!-- pagebreak -->

## 3. Predictive stack

**Hierarchical backoff (E006).** Starting from a smoothed global marginal,
each level conditions on one additional GIVEN column. The previous level
supplies the prior:

    p_L(v | cell) = (n_L(v) + kappa_L * p_(L-1)(v)) / (n_L + kappa_L)

Column order, depth up to three, and kappa in {1, 3, 10, 30, 100} are
selected greedily by held-out log score on 20% of complete visible rows.
Candidate columns have at most 12 levels. Asked-only distributions use the
same ladder. Sparse cells borrow strength from broader cells; unseen cells
back off naturally.

**Shared-trunk network (E012/E025).** One-hot GIVEN inputs feed a
Linear-ReLU trunk and a softmax head for each PREDICT item. Gated items
also have asked-only heads, trained with masked cross-entropy. Loss pools
cells across the full and conditional heads. Training uses full-batch Adam
(learning rate 0.003, weight decay 0.0001), at most 500 epochs, and early
stopping with patience 30 on an inner split. An outer split selects between
two 64-unit layers without dropout and two 128-unit layers with dropout 0.1.
The selected epoch count is used to retrain on all complete visible rows.

One network/ladder mixture weight w per instrument is selected on the outer
split from {0, 0.1, ..., 1}. Both full and conditional distributions use
w * network + (1 - w) * ladder. Shared nonlinear features pool signal across
items, while probability mixing limits reliance on unsupported sharpness.

**Visible-row evidence (E018/E022).** Every visible respondent is a
candidate, without a cross-round restriction. Matching uses only schema
GIVEN columns; E025 does not derive features from respondent identifiers.
Initial agreement weights are -log(u_j), where u_j is random agreement
computed from available GIVEN frequencies, including held-out GIVEN values.
No held-out PREDICT answer enters fitting or candidate evidence.

A first matching pass identifies provisional top candidates with posterior
mass at least 0.5. If at least 30 pairs exist, one Fellegi-Sunter-style update
estimates their per-column agreement m_j and sets weights to:

    weight_j = max(0, log(m_j/u_j) - log((1-m_j)/(1-u_j)))

Otherwise rarity weights remain. Weighted agreement scores are normalized
by softmax over the top ten candidates. Their answer vectors, averaged
with these weights, form evidence_i. This soft neighborhood can help through
near-duplicate structure or ordinary similarity; it does not identify the
social relationship between respondents.

For each item, replay on up to 6,000 visible query rows selects lambda from
{0, 0.1, ..., 0.9, 0.95, 0.98}, separately for diffuse and concentrated
posteriors (maximum mass at least 0.5). A bucket needs 30 valid observations.
The query itself is always excluded from candidates. The final belief is
(1 - lambda) * base_i + lambda * evidence_i, applied after the item's gate
mixture and before its children are decoded. Lambda = 0 disables evidence;
clean sandbox evaluations found negligible changes from this layer.

<!-- pagebreak -->

## 4. Calibration and limitations

Fitted parameters use only information visible in the evaluation frame.
Ladder selection, gate conditioning, architecture selection, and network
mixing use internal validation splits. Evidence replay excludes self-matches,
but its base predictions come from a model refitted on all visible rows:
the replay is not a fully cross-fitted estimate of generalization. We
therefore report held-out evaluations separately from replay optimization
and do not claim that every calibration stage is unbiased.

Algorithm choices and search grids were developed using synthetic tests,
public instrument descriptions, and phase-1 feedback. Their fitted values
are selected at run time. This distinguishes runtime estimation from the
development process: leaderboard feedback did influence which method was
retained. Fixed split and network seeds are zero; CPU/GPU execution and
floating-point reductions can cause small differences.

The evidence mechanism is consistent with repeated or household-related
responses, but the closed evaluation does not establish their prevalence
or identities. Similarity-based prediction is another possible explanation.
An organizer email recorded on September 2 permits matching rows within the
dataset without extracting identities outside the enclave. We use no
external record linkage. The method's aggregate gains must not be read as
reconstruction of individual records or evidence that survey respondents
can be replaced.

Six later real-data comparisons were flat at the displayed resolution:
evidence as network input (E027), parent-value gate decoding (E028), a larger
replay cap (E031b), relation-specific evidence weights (E036), identifier
signatures (E038), and a tree blend (E040). Some gained under injected
simulation assumptions. These null transfers prevent treating simulation
success as confirmation. Separately, sentinel recalibration (E037) gained
0.024 in-sample on its heavy-overlap simulation but lost about 0.004 under
cross-fitting, so it was rejected.

## 5. Phase-2 settings and compute

Phase 2 uses the unchanged E025 assembly at
`submissions/2026-09-09-E025/main.py`. TRAIN and DEV are visible, TEST is
scored. The two-architecture choice, top-ten candidate pool, replay cap of
6,000, and concentration-specific lambda grid remain unchanged. Larger
replay, ensembles, relation splits, identifier features, and trees are not
included. No phase-2 fitting occurs before the evaluation frame arrives.

Historical phase-2 hardening with the official scorer passed all three
schemas. These are synthetic scores on TEST-role cells, not final leaderboard
results:

| Instrument | Exact skill | Scored cells |
|---|---|---|
| UNICEF | 0.4902 | 41,676 |
| World Bank | 0.4620 | 92,112 |
| UNHCR | 0.5652 | 308,637 |

Historical official scoring took 310.0 seconds across three processes; the
original CPU runner took 291 seconds. A018 freshly reproduced all 442,425
A012 frozen-main vectors in a single process across all instruments: 332.78
seconds including imports/data/scoring/parity, peak working set 1.47 GB and
peak commitment 1.56 GB, Windows CPU with two numerical threads. These
measurements fit the local 3,600-second/16 GB gates but do not certify hosted
H100 resources or hidden-data runtime. Historical official raw vectors were
not retained; tiny UNICEF/WB score drift from A012 remains unexplained.
Neural training uses CUDA when
available, with CPU fallback. TRAIN+DEV growth can change selected
architecture, epochs, gates and replay lambdas despite unchanged source.

<!-- pagebreak -->

## 6. Results and diagnostic map

E025 phase-1 synthetic skill was .501/.455/.563. Its user-reported hosted
reading was Grand .63, UNICEF .52, WB .49, UNHCR .89, rounded and noised.
Earlier E012 read .60/.52/.49/.78; E022 read .63/.52/.49/.88. These complete
pipeline observations do not identify precise, independent component effects.

**UNHCR component ablations (E032-E034).** Aggregate readings attribute
approximately .79 skill to the base plus .10 to evidence. Remaining loss
was .079 gated and .031 ungated. Retaining sentinel mass while flattening
asked answers left gated skill near .56. These are aggregate E025 performance
estimates, not hidden response statistics or an E041 decomposition.

UNHCR-only same-phase comparisons have delta_UNHCR = 3 * delta_Grand,
with practical resolution about .015-.03, not three-decimal precision.
E032 initially changed all instruments and used a second account, since
retired and flagged as a likely terms violation. That reading is not
independent replication. E033/E034 used the main account and changed UNHCR only.

**Synthetic oracle (A005).** A generator-based GIVEN-only Bayes reference
averaged .5085 versus .5062 for the base (unrounded gap .0024). This limits
that sandbox's usefulness, not confidential-data performance or headroom.

## 7. Reproducibility and disclosure

The archive contains a self-contained `main.py`; all learning happens at run
time. No external training data, pretrained weights, bundled fitted artifacts,
`models.txt`, or network API calls enter the predictor. Public survey material
informed development hypotheses, not fitted priors. Runtime uses the hosted
NumPy, pandas, PyTorch, and scikit-learn environment. Source modules, experiment
records, tests, and the official-score wrapper are retained in the repository.
Archive checks, source/assembly parity, and three-schema official scoring
precede release; the phase-2 preparation record holds exact commands and hashes.

Codabench's participation agreement [2], clause 7, requires a four-page method
with every Test submission and research-reproduction licensing of source code
for the top three at the award stage. It does not expressly require publication
of the entire development repository. The public starter kit is MIT-licensed;
its copyright notice must accompany redistributed substantial portions [1].
The agreement was rechecked 25 September 2026. The team's release license
must be selected before award-stage source delivery; A018 contains a scoped
MIT proposal. This document grants no new license.

Later development and final selection compared E025 with E041 and qualified
alternatives. UCI Adult (Becker and Kohavi, 1996; CC BY 4.0) and US Census
2023 SIPP public-use observations supported separate recoded proxy studies.
TabPFN V2 classifier weights from Prior Labs were used in separate experiments,
under their own license. No such rows, weights, outputs or proxy-fitted
artifacts enter E025. A018 preserves E025 as a separate failure fallback;
its final TEST performance remains unknown. TEST closes 14 November 2026
00:00 UTC; there is one submission per team and no assumed participant retry.

**References.** [1] SituatedEvals, public starter kit (MIT), revision ee427a9:
https://github.com/SituatedEvals/public. [2] SimulacraBench participation
agreement, Submissions clause 7: https://www.codabench.org/competitions/17822/.
[3] Adult: https://archive.ics.uci.edu/dataset/2/adult.
[4] Prior Labs: https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt.
[5] Census: https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html.
