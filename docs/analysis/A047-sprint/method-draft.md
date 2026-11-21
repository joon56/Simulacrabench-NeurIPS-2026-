# Survey completion with a retrieval-calibrated base and runtime-validated additions

**DRAFT (2026-11-10) — final configuration and numbers to be filled after DEV closes**

Team Odyssey (Minjoon Yoo, Yonsei University) | HSCC / SimulacraBench 2026

## 1. Task and metric

We predict every held-out PREDICT cell of three instruments (UNICEF Faith & Immunisation,
World Bank Skills Assessment, UNHCR ERPIS) from the respondent's GIVEN block. Visible
respondents arrive complete; gated items carry an extra final option, the schema's gate
sentinel, for "never asked". The grader renormalizes each vector and mixes in a flat floor
f = 0.001, scores the mean log probability of the realized answers per instrument, and
reports skill relative to the crowd-marginal reference; the Grand score is the flat mean of
the three instrument skills. A confidently wrong cell costs log f, so every component below
is judged on calibrated log loss rather than accuracy.

## 2. Base predictor (E041)

**Hierarchical backoff.** A smoothed marginal anchors a ladder of GIVEN-cell tables; column
order, depth (up to three) and shrinkage are chosen on an internal 20% split.

**Shared neural trunk.** One-hot GIVEN features feed a two-layer trunk with one softmax head
per PREDICT item (sentinel included) and an asked-only head per gated item. Architecture,
epoch count and a network/ladder mixture weight are selected on internal splits; the network
is refitted on all complete visible rows.

**Approximate gates.** Gate-implied distributions are mixed with unrestricted heads using
shrunken gate-agreement weights (optionally conditioned on one GIVEN column), so a gate that
the data contradict is not enforced as deterministic. UNHCR's schema reports gate agreement
with median 0.83.

**Donor evidence and supervised retrieval.** Complete visible respondents serve as donors;
a Fellegi-Sunter-style agreement weighting over GIVEN columns ranks candidates, and a
self-excluded replay chooses item-specific evidence weights. For UNHCR, section-specific
metrics learned on disjoint fit/selection/replay partitions rerank 32 candidates; a section
activates only when it beats the legacy evidence on held-out selection rows.

## 3. Runtime-validated additions (final submission)

All additions are decided inside the run, on the delivered visible rows only.

**Seed averaging.** The final base is the cell-wise mean of E041 runs with different network
seeds (k = [fill]). By Jensen's inequality the log score of an average of probability vectors
is at least the average log score of its members, and the grader's floor is affine, so seed
averaging cannot lower the expected log score of a single run.

**Pretrained in-context tabular expert.** Per PREDICT item, a TabICLv2 classifier (bundled
public checkpoint, fixed settings, no gradient updates) is fitted on the GIVEN features of the
visible rows, predicting the full option set including the sentinel. Candidate transforms of
the base: a global linear pool with weight alpha; an uncertainty-scaled pool, where alpha is
multiplied per cell by (1 - max p)/(1 - 1/K) so that confident (e.g. donor-linked) cells stay
close to E041; and per-item weights chosen from {0, .25, .5, .75, 1}.

**Documented gate corrections.** (i) UNHCR return branches: the schema states that branches
s7a/s7b follow s3_12 more closely than their declared parent s3_11; when the visible rows
confirm this (per branch and survey round, smoothed skip rates, log-likelihood margin), the
sentinel mass is re-estimated from E041's predicted s3_12 distribution. (ii) UNHCR
multi-select families coded "0" for skipped respondents in round 1: sentinel mass moves to "0"
where the visible rows of that round contain no sentinel. (iii) World Bank tracer items: the
declared gate (randomisation arm) over-states who was followed up; on gates the visible rows
contradict (agreement < 0.95), the sentinel probability comes from the expert.

**Internal validation rule.** A fixed permutation splits complete visible rows into S (1000),
E (1000) and F (rest). A shadow E041 and the expert are fitted on F only. Each candidate chain
is scored on S (pooled floored log score; per-item weights use a two-fold out-of-fold score
inside S to remove selection optimism). The best chains are tested on E in order; a chain is
applied only if the one-sided lower bound mean(d) - 1.645 sd(d)/sqrt(1000) of the
per-respondent log-score difference is positive. Otherwise the instrument keeps the seed-
averaged base. Accepted chains are refitted on all visible rows. [fill: chains per instrument]

## 4. Development evidence and limitations

[fill: DEV readings table — E041 and final-structure uploads; local synthetic phase-2 deltas]

Development-phase scores are noised and rounded before conversion, so effects below one
display step are unreadable; repeated uploads of identical E041 code read old-scale UNHCR
0.92 and occasionally 0.91, consistent with a value near a rounding boundary. For this
reason the final package relies on the internal S/E comparison on real visible rows rather
than on single development readings. The internal check is a one-sided approximate bound over
respondents, not an independent audit; S selection among a few chains is included in what E
must confirm; the shadow base is single-seed while the deployed base is seed-averaged.
Local synthetic data (organizer sandbox) were used for engineering checks only.

## 5. Reproducibility and disclosure

Code: [fill code_url], BSD-3-Clause (team code). Third-party components retain their
licenses: TabICL 2.2.0 source (BSD-3, commit 0dbff3e), TabICLv2 classifier checkpoint
(Hugging Face jingang/TabICL, revision 4dcd344e, bsd-3-clause), einops 0.8.1 (MIT), tqdm
4.67.1 (MPL-2.0/MIT), starter-kit material (MIT). No requirements.txt; the checkpoint is
bundled and loaded at import; no network access at runtime. No external response data or
fitted priors enter the predictor. Runtime on the Final budget: [fill] (local phase-2
rehearsal on synthetic data: ~2,240 s for the maximal configuration on one RTX 3070).
