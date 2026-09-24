# Calibrated survey completion with section-specific retrieval

HSCC / SimulacraBench 2026 | E041 phase-2 method candidate

## 1. Task, score, and evidence

We predict categorical answers from each held-out respondent's GIVEN block.
Every PREDICT cell is hidden and scored; EXCLUDE items are omitted. The
instruments are UNICEF Faith & Immunisation, World Bank Skills Assessment,
and UNHCR ERPIS. One self-contained predictor learns separately from the
complete visible respondents of each instrument. E041 adds supervised
retrieval only for UNHCR; UNICEF and World Bank use the E025 stack unchanged.

The official score is skill = 1 + log_score / U, where log_score averages
log probabilities over scored cells and U averages log K over those cells;
K includes the gated sentinel. Grand equally averages the three instrument
skills. The grader normalizes each vector and mixes uniform mass to enforce
a 0.001 probability floor. We therefore select and mix distributions by
log score, where confident errors are costly.

E041 is the phase-1 DEV incumbent after a user-reported, rounded and noised
leaderboard reading: Grand 0.64, UNICEF 0.52, World Bank 0.49, UNHCR 0.92.
E025 previously read 0.63 / 0.52 / 0.49 / 0.89. This compares complete
pipelines, not an isolated effect of learned retrieval weights. No phase-2
real-data score exists. Synthetic sandboxes and public Adult experiments
test behavior and limited transfer channels, not confidential TEST gain.
E041 is locally qualified for phase 2; the final choice remains open.

## 2. Schema handling and approximate gates

Vectors follow schema option order, with a final NA_GATED slot for gated
items. NaN marks a target; refusal is an ordinary answer. Items decode in
schema order, and a parent's final belief enters its descendants. A visible
parent contributes a one-hot belief. For a gated item i:

    r_i = sum of parent belief over observed_if values
    hard_i = [r_i * conditional_i, 1 - r_i]
    base_i = a_i(x) * hard_i + (1 - a_i(x)) * full_i

The conditional distribution trains on asked rows; full_i includes the
sentinel. UNHCR's published gate agreement median is 0.83, range 0.29-0.98.
Thus a known parent need not imply an exact skip. The scalar agreement rate
is (k_i + 20 * m) / (n_i + 20), shrunk toward median observed agreement m,
not toward one. At most one low-cardinality GIVEN column is selected per
child by Bernoulli log likelihood on an internal 20% split. Its value-specific
rates shrink toward the scalar, which remains if no column helps.

<!-- pagebreak -->

## 3. Base distributions and visible-row evidence

**Hierarchical backoff (E006).** A smoothed global marginal anchors a ladder
that adds one GIVEN column at each level:

    p_L(v | cell) = (n_L(v) + kappa_L * p_(L-1)(v)) / (n_L + kappa_L)

Column order, depth up to three, and kappa in {1, 3, 10, 30, 100} are chosen
greedily by held-out log score on 20% of visible rows. Columns have at most
12 levels; unseen cells back off. Asked-only heads use the same ladder.

**Shared-trunk network (E012/E025).** One-hot GIVEN inputs feed a Linear-ReLU
trunk and softmax heads for PREDICT items, with separate asked-only heads
for gated items. Full-batch Adam uses learning rate 0.003, weight decay
0.0001, at most 500 epochs and patience 30 on an inner split. An outer split
selects two 64-unit layers without dropout or two 128-unit layers with
dropout 0.1. The selected epoch count retrains on all visible rows. One
per-instrument network/ladder mixture weight from {0, 0.1, ..., 1} is
selected on the outer split and applies to full and asked-only distributions.

**E025 evidence retained.** All visible respondents can be donor candidates.
Matching uses GIVEN values, never respondent identifiers or held-out answers.
Initial weights use negative log random agreement from GIVEN frequencies,
including held-out GIVEN values. Provisional high-posterior pairs can update
weights in a Fellegi-Sunter-style agreement calculation if at least 30 pairs
exist. Otherwise rarity weights remain. Softmax over the top ten candidates
averages their answer vectors into item evidence.

For each item, self-excluded replay on up to 6,000 visible queries chooses
lambda from {0, 0.1, ..., 0.9, 0.95, 0.98}, separately when maximum donor
mass is below or at least 0.5. Each bucket needs 30 observations. The final
belief is (1 - lambda) * base_i + lambda * evidence_i, applied after the
gate mixture and before decoding descendants. Lambda zero disables evidence.
Near-duplicate or ordinary similarity can help; this does not establish
household relationships.

## 4. E041 UNHCR section retrieval

UNHCR PREDICT items are grouped by section prefix in schema names. E041
learns nonnegative diagonal weights on GIVEN equality features, one metric
per section. It reranks a fixed 32-candidate donor set from the initial
E025 metric; softmax weights then form selected-section evidence. No external
data, pretrained model or respondent identifier enters this computation.
The other instruments dispatch directly to E025.

<!-- pagebreak -->

## 5. Retrieval fitting, selection, and limitations

Visible rows split with fixed seed 4101 into metric-fit (up to 1,200),
selection (up to 800), new-metric replay (up to 800), and reference rows.
These four groups are disjoint. Metric-fit query labels optimize section
weights and a mixture share by officially floored log loss, with a
squared-distance penalty to initial weights. Donors come only from the
reference bank. Selection labels compare the learned 32-candidate policy
with an initial-metric top-ten comparator. A section activates only when
mean log gain exceeds both 0.003 and twice its estimated standard error.
Selection labels never fit metric weights. Held-out PREDICT answers remain
absent throughout.

Active sections replace their donor evidence and use disjoint replay rows
to select item/bucket lambdas; inactive items retain E025 replay. At
deployment learned weights operate on GIVEN agreement, while donor answers
come from complete visible respondents. Concentration buckets still use
the initial-metric top-ten posterior. Parent evidence feeds later gates.

The selector uses a marginal/evidence proxy rather than the full E025
stack. Its fitted mixture share differs from deployed item lambdas, and
tied donor order can differ. The replay base was refitted on all visible
rows: donor self-exclusion does not cross-fit base calibration. E041's
disjoint new-metric replay does not repair this. Local comparisons evaluate
the whole pipeline. CPU/GPU reductions can vary slightly.

UNHCR spans housing, work, protection and return intentions, so section
relevance is plausible but unproved. A September 2 organizer email permits
within-dataset matching. No outside linkage or identity inference is used.
Approximate gates and donor dependence remain sources of error.

**Development diagnostics.** On clean synthetic UNHCR, E041 versus E025
was -0.000486 skill; on an existing household simulation it was -0.002026.
UNICEF/WB clean predictions were exact E025 copies. Two observed UCI Adult
screens yielded learned-metric audit gains +0.000595 and +0.000427 skill
against their fixed comparator, with paired intervals including zero. Adult
has no UNHCR gate structure and was sampled with distinct-profile constraints.
The hosted E041 best update overrode local rejection for DEV selection; one
noised reading cannot isolate metric, bank, selector or replay effects.

A011 measured replay membership-associated log/cell contrasts +0.00450
clean, +0.00470 household, +0.01608 Adult. Included fits had 400 more rows;
these associations are not recoverable gains. Gate-base pressure shifted
oppositely in two UNHCR simulations. E053's ungated Adult absolute-weight
oracle stopped at mean-equivalent bounds +0.000523 and +0.000173, below
its +0.005 gate. It does not bound coupled UNHCR calibration, and no E053
calibrator enters E041.

<!-- pagebreak -->

## 6. Phase-2 engineering and historical diagnostic map

Phase 2 makes TRAIN and DEV visible and scores TEST. Frozen E041 source
and its original archive passed the official phase-2 scorer on all three
synthetic schemas. Every source/assembled raw vector matched exactly
(442,425 cells). Fresh paired E025 comparisons were:

| Instrument | E025 skill | E041 skill / delta |
|---|---:|---:|
| UNICEF | 0.490197771 | 0.490197771 / 0 |
| World Bank | 0.462029505 | 0.462029505 / 0 |
| UNHCR | 0.565173814 | 0.564665365 / -0.000508449 |

Absolute differences met the preregistered 0.002 per-instrument gate.
The original archive passed the ZIP checker. Inclusive local official
scoring totaled 367.177 seconds, below the shared 3,600-second phase-2
budget. Three local runs each used a separate process; neither hosted
speed nor 16 GB peak memory nor real TEST gain was measured. E041 is a
prepared candidate, not an automatically chosen final submission. E025
remains a separate fallback.

E032-E034 component probes describe **E025 only**: reported UNHCR skill
0.89 decomposed approximately into base 0.79 plus evidence 0.10.
Estimated remaining loss was 0.079 gated and 0.031 ungated; flattening
asked-answer probabilities while retaining sentinel mass left gated skill
near 0.56. These are aggregate model-performance probes, not private
response statistics. E041's 0.92 has no corresponding loss map.
The initial E032 probe changed all three instruments; E033/E034 changed
UNHCR only. Rounded, noised Grand readings give practical
UNHCR difference resolution about 0.015-0.03. The three-decimal components
are arithmetic summaries, not three-decimal measurement precision.
E032's initial per-instrument reading came from a second account, since
retired and flagged in the experiment record as a likely terms violation;
that reading is not independent replication.

The A005 synthetic GIVEN-only Bayes reference averaged 0.5085 across the
three instruments versus 0.5062 for the base (unrounded gap about 0.0024).
This limits what that public sandbox can validate, not confidential-data
performance or E041's possible TEST gain.

## 7. Reproducibility, external work, and disclosure

E041 is a self-contained main.py; fitting occurs when the evaluation frame
arrives. It bundles no fitted artifact, external dataset, pretrained weight,
models.txt, or network call. Archive hash, source/assembly parity, official
phase-2 scores and timing are in the preparation record. Internal splits
and phase-1 feedback influenced method selection; not all development
choices were prospectively fixed.

Development used public UCI Adult census data, licensed CC BY 4.0 [3],
to screen retrieval and calibration methods. Separate TabPFN V2 experiments
used Prior Labs' externally pretrained classifier weights [4], but E041
does not include TabPFN, its outputs or fitted artifacts at inference.
Neither Adult rows nor TabPFN weights are in the E041 archive. Public survey
descriptions informed hypotheses, not fitted response priors.

The competition agreement's Submissions clause 7, checked in the earlier
preparation audit [2], requires a four-page method for each Test entry and
research-reproduction-licensed source from top-three teams at award stage.
The public starter kit is MIT-licensed [1]; substantial copied portions
must retain its notice. A team release license remains to be selected
before award-stage delivery. This document grants no new license.

**References.** [1] SituatedEvals, public starter kit and MIT license:
https://github.com/SituatedEvals/public. [2] SimulacraBench agreement:
https://www.codabench.org/competitions/17822/.
[3] Becker and Kohavi, Adult (1996), UCI, CC BY 4.0:
https://archive.ics.uci.edu/dataset/2/adult.
[4] Prior Labs, TabPFN V2 classifier weight license:
https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt.
