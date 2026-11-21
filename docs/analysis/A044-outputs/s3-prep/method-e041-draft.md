# Calibrated survey completion with section-specific retrieval

HSCC / SimulacraBench2026 — E041 provisional method draft,23 October2026.
User final TEST choice remains open. Four-page content allocation below;
**not rendered, not a four-page PDF PASS, not a submission-ready attachment**.
Describes unchanged main.py SHA256
`22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.

## Page1 — task, evidence and approximate gates

We predict categorical PREDICT answers from each respondent's GIVEN block for
UNICEF Faith & Immunisation, World Bank Skills Assessment and UNHCR ERPIS.
Every hidden PREDICT cell is scored, including gated sentinels; EXCLUDE items
are omitted. Phase1 makes TRAIN complete and scores DEV. Phase2 makes TRAIN
and DEV complete and scores previously unseen TEST respondents. The current
official README says roles follow seeded row permutation: UNICEF stratified
by country, UNHCR balanced on survey round/country, WB plain random permutation.
Thus TEST is not a chronological or unseen-country holdout.[1]

The scorer averages log probabilities over scored cells and reports
skill=1+mean(logp)/U, where U is the mean log option-count over scored items,
including each gated sentinel. Grand equally averages the three instrument
skills. Each raw vector is normalized, then transformed to
p'_k=.001+(1−K*.001)p_k. We optimize log-score-based mixtures; confident errors
are costly. No private response-level data are available to the developers.

E041 is a provisional reference, not a user-confirmed TEST selection. Its
user-provided released API record ID933094 reports Grand.6433333333,
UNICEF.5200000000, WB.4900000000 and UNHCR.9200000000. The interface shows
Grand.64. These serialized decimals do not undo DEV noising and rounding or
establish precise underlying effects. The historical E025 reading was
.63/.52/.49/.89. This is a complete-pipeline comparison, not independent
replication or isolation of a learned-metric effect. No actual TEST score exists.

One self-contained predictor fits separately per instrument at runtime. E041
changes retrieval for UNHCR only; UNICEF and WB dispatch to E025. Vectors follow
schema option order, adding NA_GATED last when gated. NaN denotes a target;
refusal/non-response categories remain ordinary answers. Parents are decoded
before descendants; visible parents supply one-hot beliefs.

For gated item i, let r_i be parent mass on its observed-if values. The hard
distribution is [r_i times asked-conditional_i,1−r_i]. The final base mixes this
with an unrestricted full distribution using estimated agreement a_i(x).
Agreement shrinks (k_i+20m)/(n_i+20) toward median observed agreement m, not1.
At most one low-cardinality GIVEN column improves child-specific agreement on
an internal20% split; value-specific rates shrink toward the scalar fallback.
Published UNHCR agreement ranges.29–.98, median.83, so gates are approximate.

<!-- pagebreak -->

## Page2 — base model and donor evidence

Hierarchical backoff smooths each cell toward its parent distribution:
p_L=(n_L+kappa_L p_(L−1))/(N_L+kappa_L). A held-out20% visible split selects
GIVEN columns, depth up to3 and kappa in{1,3,10,30,100}. Candidate columns have
at most12 levels; unseen cells back off. Asked-only heads use the same ladder.

A shared Linear–ReLU trunk consumes one-hot GIVEN inputs, with separate softmax
full heads and asked-only heads for gated items. Full-batch Adam uses lr.003,
weight decay.0001, at most500epochs and inner-validation patience30. An outer
split chooses64x2/no-dropout or128x2/dropout.1. The selected epoch count is
refitted on all visible rows. One instrument-level network/ladder mixture
weight from{0,.1,…,1} is chosen on the outer split. No E061 tied heads, E062
ordinal head, E063 wave metric or E064 detached-gradient change enters E041.

E025 donor evidence uses all complete visible respondents as possible donors.
GIVEN matching weights begin with negative-log random agreement frequencies,
including held-out GIVEN covariates. At least30 high-posterior provisional
pairs are needed for a Fellegi–Sunter-style agreement weight update; otherwise
rarity weights remain. Softmax over the top10 donor candidates averages their
answer vectors. Respondent identifiers are not features and no external
identity linkage is used; similar donors do not prove household relationships.

Self-excluded replay over up to6000 visible queries chooses per-item lambda
from{0,.1,…,.9,.95,.98}, in separate buckets below/above maximum donor mass.5.
Each bucket needs30 observations; insufficient support defaults to lambda0.
The distribution (1−lambda)base+lambda evidence enters recursive decoding
after gate mixing. If no positive lambda is learned, only the base remains.

For UNHCR, E041 groups PREDICT items by section-name prefix. It reranks32
initial-metric candidates using nonnegative diagonal GIVEN equality weights
per section. Seed4101 partitions visible rows into metric-fit(up to1200),
selection(up to800), new-metric replay(up to800), and disjoint reference bank.
Metric-fit query labels learn weights and mixture share with floored log loss
and regularization toward initial weights; reference-bank labels provide donors.
Selection compares learned32-candidate evidence to initial top10 evidence.
A section activates only when mean log gain exceeds max(.003,2 estimated SE).
That heuristic is not a multiple-testing-adjusted population guarantee.

<!-- pagebreak -->

## Page3 — calibration, refit and development uncertainty

Active sections replace donor evidence and calibrate item/bucket lambdas on
their disjoint replay queries; inactive items retain legacy replay. Deployment
uses the full visible bank. Concentration buckets still use initial top10
posterior mass. Fewer than500 complete rows or no held-out rows invokes legacy
evidence; an unusable GIVEN signature supplies no evidence. The UNHCR dispatch
uses the exact schema key s3_11_intent_return_12m_lbl. Historical synthetic
phase2 activated7 of8 sections; hidden-data activity is unknown.

Query-role separation does not cross-fit the whole pipeline. Base distributions
are refitted on all visible rows, including replay labels; donor self-exclusion
does not remove that calibration optimism. Selection optimizes a marginal/
evidence proxy and mixture share that differ from deployed recursive base and
item lambdas. Repeated DEV observations also influenced development choices.
DEV becoming legal final training data does not restore independent validation.
No fitted state is frozen: adding DEV can change neural architecture/epochs,
ladder/gate choices, rarity/EM weights, role membership, sections and lambdas.

Published phase2 visible counts are16373/5715/8900. UNHCR reference rows grow
5479→6100 while caps1200/800/800 remain. This is same-population refitting under
the stated random split, but improvement is unmeasured. Internal row order and
numerical reductions can affect fitting. GPU training exceptions have a CPU
fallback; arbitrary failures or deadline exhaustion do not swap the whole model
to E025. E025 remains a separately stored pre-upload alternative only.

Counterevidence matters: E041 versus E025 was−.000486 synthetic UNHCR skill
and−.002026 on a household simulation. Adult audits+.000595/+.000427 had paired
intervals including0. Adult lacks UNHCR's approximate gate structure. A011
membership-associated replay contrasts did not establish recoverable gain.
E053 ungated Adult and E055 exact-gate SIPP oracle STOPs are scoped bounds,
not proofs of no headroom on UNHCR; no resulting calibrator enters E041.
E056–E059 SIPP studies also yield no deployed component; E059 STOP_SELECTION
and the prohibition on promoting A_half remain.

Later released E060/E062/E063 ties leave exact effects unresolved. E061's
released Grand−.0033333333/UNHCR−.01 is adverse for that complete pipeline.
E064's engineering PASS with synthetic−.0000843536 is neither efficacy nor
TEST qualification. E045/E047/E049/E052 likewise showed no readable new best.
These dependent development comparisons cannot supply precise causal effects
or a TEST win probability. E032–E034 component estimates belong to E025 only;
E041 has no corresponding loss decomposition. E032's initial reading used a
second account, later retired and recorded as a likely Terms violation. No
organizer adjudication or waiver is asserted; it is not independent replication.

<!-- pagebreak -->

## Page4 — engineering, reproducibility and external-material disclosure

Historical A012/A018 synthetic phase2 work produced exact442425-vector E041
source/assembly parity, valid outputs on all3schemas and absolute skill
differences versus E025 of0/0/−.000508448996, within.002. Final notice-preserving
ZIP official scoring totaled359.448694s; orchestration364.340160s. A shared
all3 process took336.554468s including imports, input/output, scoring and parity;
peak working set1.493GB/private commitment1.605GB on Windows CPU2. E025's
rehearsal332.782386s/private1.557GB has weaker historical official raw/scorer/
data provenance. These are neither H100/native image guarantees nor real TEST
measurements. A012 scored before some raw saves/provenance collection; A018
preserves an aborted concurrent run and later guard improvements separately.

October23 inspection confirmed unchanged dated ZIP/main/PDF identities and a
compatible public kit contract through commit f980ef5. It did not reopen raw
arrays/inputs, rerun models or verify the current runtime image. Old synthetic
results remain historical. Current complete parity is not claimed.

The predictor bundles no fitted artifact, external dataset, pretrained weight,
models.txt or network call. Both ZIPs contain main.py and the starter MIT notice
only. Runtime imports are NumPy/pandas/PyTorch/scikit-learn, plus SciPy and
threadpoolctl for E041. Hosted versions and native GPU timing are not independently
verified. Visible-row fitting/internal selection/refit is permitted by the
website and an October2 user-supplied organizer clarification, and consumes the
same3600s Final clock. No organizer email authentication is claimed here.

Separate development used recoded/profile-constrained UCI Adult observations
(Becker/Kohavi1996, CC BY4.0)[3], Census2023 SIPP public-use data[4], and Prior Labs
TabPFN V2 experiments[5]. A040 used TabICLv2 in separate fake-data technical work;
VAF/HOST work inspected documents and approved-file headers while empirical
linkage/missing-state use remained on HOLD. None of those rows, weights,
outputs or proxy-fitted artifacts enters E041/E025. The lineage of these
unchanged predictors predates the later SIPP/TabICL/VAF work. Access approval
does not authorize redistribution; no such external asset is redistributed here.

The starter kit is MIT; its complete notice is retained. Runtime components
retain their own licenses. TabPFN uses Prior Labs License1.1 with additional
attribution; it is not relicensed as team MIT. The team's original predictor
code license awaits owner choice; a scoped MIT text is only a proposal.
This draft grants no rights or whole-repository release permission.

Current public dates are Development through November13 and Final November14–18.
Exact platform timestamps/current Terms are unconfirmed. Website wording assigns
4-page method/source obligations to winners; September's retained Terms applied
the method to every TEST entry. This draft preserves that unresolved difference
and does not assert that the requirement disappeared. Final choice, current
agreement/slot confirmation and any upload remain separate user decisions.[2]

References: [1] [Official pinned kit](https://github.com/SituatedEvals/public/tree/f980ef5059360fcf977ed7971af5c00ee5c1962f).
[2] [Website](https://simulacrabench.org/) and [Codabench rules](https://www.codabench.org/competitions/17822/).
[3] [Adult](https://archive.ics.uci.edu/dataset/2/adult).
[4] [Census SIPP](https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html).
[5] [TabPFN license](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/LICENSE.txt).
Detailed provenance, license scope and limitations: companion S3-PREP-A044 records.
