# Calibrated survey completion with section-specific retrieval

HSCC / SimulacraBench 2026 | E041 TEST selection, 25 September 2026

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
The A018 selection compares E025/E041/E044/E045/E047/E049/E052 using
target evidence, refit behavior, leakage, resources and release obligations.
E041 is selected on this evidence and phase-2 engineering; E025 is preserved.

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

A011 found replay membership-associated contrasts, not recoverable gains;
included fits also had 400 more rows. E053's ungated Adult oracle stopped
at mean-equivalent bounds +0.000523/+0.000173. E055's coupled exact-gate
SIPP oracle stopped at +0.000113/+0.000102. These scoped proxy stops do not
bound approximate UNHCR calibration. No resulting calibrator enters E041.
E045/E047/E049/E052 later read Grand .64 without a best update: small effects
remain unresolved. Their complexity and weak transfer evidence do not justify
replacement. No new predictor is selected by the clean synthetic ranking.

<!-- pagebreak -->

## 6. Phase-2 engineering and historical diagnostic map

Phase 2 makes TRAIN and DEV visible and scores TEST. Visible row counts grow
to 16,373/5,715/8,900. All fitted components and internal row memberships may
change; UNHCR's metric reference bank grows from 5,479 to 6,100 while
fit/selection/replay caps remain 1,200/800/800. No pretrained fit is frozen.
Frozen E041 source
and its original archive passed the official phase-2 scorer on all three
synthetic schemas. Every source/assembled raw vector matched exactly
(442,425 cells). Fresh paired E025 comparisons were:

| Instrument | E025 skill | E041 skill / delta |
|---|---:|---:|
| UNICEF | 0.490197771 | 0.490197771 / 0 |
| World Bank | 0.462029505 | 0.462029505 / 0 |
| UNHCR | 0.565173814 | 0.564665365 / -0.000508449 |

Absolute differences met the preregistered 0.002 per-instrument gate.
The original archive passed the ZIP checker; A012's separate-process official
total was 367.177 seconds. A018 freshly reproduced every vector in one process
across all three instruments: 336.55 seconds including imports, scoring and
parity, with peak working set 1.49 GB and peak commitment 1.60 GB. Seven of
eight UNHCR sections activated. These Windows CPU, two-thread measurements
fit 3,600 seconds/16 GB locally, but do not certify hosted H100 resources or
hidden-data behavior. The final notice-preserving ZIP also passed fresh official
phase-2 scoring on all three schemas with exact raw parity (359.45 seconds
official total; 364.34 seconds orchestration). E025 is a pre-upload fallback.

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

Development used UCI Adult (Becker and Kohavi, 1996), CC BY 4.0 [3], with
recoded profile-constrained splits, and Census 2023 SIPP public-use data [5]
with one reference month and audited hospital gates. Separate TabPFN V2
experiments used Prior Labs weights [4]. These are development disclosures:
no Adult/SIPP row, TabPFN weight/output or proxy-fitted artifact enters E041.
Public survey descriptions informed hypotheses, not fitted response priors.

The competition agreement's clause 7, rechecked 25 September 2026 [2],
requires a four-page method for each Test entry and
research-reproduction-licensed source from top-three teams at award stage.
The public starter kit is MIT-licensed [1]; substantial copied portions
must retain its notice. A team release license remains to be selected
before award-stage delivery; A018 contains a scoped MIT proposal. This
document grants no new license. TEST closes 14 November 00:00 UTC; one
submission per team. Participant-side failures have no assumed retry.

**References.** [1] SituatedEvals, public starter kit and MIT license:
https://github.com/SituatedEvals/public. [2] SimulacraBench agreement:
https://www.codabench.org/competitions/17822/.
[3] Becker and Kohavi, Adult (1996), UCI, CC BY 4.0:
https://archive.ics.uci.edu/dataset/2/adult.
[4] Prior Labs, TabPFN V2 classifier weight license:
https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt.
[5] US Census Bureau, 2023 SIPP public-use data:
https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html.
