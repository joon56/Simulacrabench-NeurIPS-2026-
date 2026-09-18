# A008 - Winning objective: new model hypotheses
date-started: 2026-09-18
status: done
relates-to: A007 / E018 / E023 / E025 / E027 / E030 / E035

## Objective and status

The user prioritizes winning, permits replacing the incumbent method, and
asks how to reach beyond Grand .65. This is a researched proposal, not an
implemented design or a measured forecast. A007's validation findings remain
useful infrastructure; repairing the incumbent is no longer the main research
objective. No E-series ID is assigned to these hypotheses yet.

With controls held at their displayed .52/.49, H=.94 gives mean .6500;
H=.95 gives .6533; H=.96 gives .6567. Rounded Grand .65 alone does not ensure
first place. These are arithmetic targets, not predictions; the displayed
scores have noise and the leaderboard can move. H=.89 to .94 requires .05
skill, about 45% of the remaining .11 loss. For U_H about 1.2618 this is
.0631 mean log probability per cell. Component gains cannot be added without
measuring their interaction.

## Main hypothesis: learn which reference respondents help each question

### Evidence and loss-map fit

E034 puts the E025 base near .79 and the incremental evidence contribution
near .10. Source inspection confirms one learned GIVEN-agreement weight
vector and one candidate posterior are reused across all PREDICT items;
only the final lambda varies by item and concentration bucket. Matching
weights are estimated from provisional feature matches, not optimized for
held-out answer prediction.

Hypothesis: useful neighbours depend on the response domain, and GIVEN
interactions carry information that the global exact-agreement kernel misses.
Age/education may matter differently from household composition or geography
for different questions. These are motivations to test, not established facts
about this file. No household recurrence or duplicate prevalence is assumed.
The method targets conditional prediction using the same available data.

### Proposed method

A compact, supervised retrieval model learns query/reference embeddings from
GIVEN only. Small section-specific projections share statistical strength
across related items while allowing different neighbour weights. Reference
answers are probability values; the query's answers are training targets only.
Optimize the pooled final log score, including NA_GATED as an ordinary output
category. A base-prediction option lets the model abstain from borrowing a
reference answer when none is useful; a peaked relative neighbour score alone
does not establish reliability. Gates can inform the base but cannot impose
exact routing constraints on the approximate real UNHCR gates.

This is a new predictor family. E023 changed K and repeated unsupervised
weight estimation. E030 changed ordinal adjacency credit. E027 fed an
already fixed retrieval aggregate to a network. None trained section-specific
retrieval by the answer-prediction objective. E035's transition oracle on an
injected structure does not bound a different learned neighbour distribution.

TabR supplies primary-source precedent for learning tabular prediction with
retrieved training features and labels, not proof of an HSCC gain:
https://proceedings.iclr.cc/paper_files/paper/2024/hash/4ef594af0d9a519db8fb292452c461fa-Abstract-Conference.html
https://github.com/yandex-research/tabular-dl-tabr

### Ceiling channel before an estimator

On observed, non-injected survey rows, mask the complete PREDICT block on
query respondents and freeze the candidate bank and base predictions. An
optimistic oracle optimizes reference-mixture weights shared across a whole
question section, not an independent correct donor for every cell. Define
the admissible candidate family first; report the oracle only as a bound for
that family and those rows. A large oracle gain is necessary, not evidence
that GIVEN can learn it. Then require gains on separate evaluation rows with
the query labels absent from all fitting, reference banks and early stopping.
Split by respondent, not by individual cells; training/reference inclusion
must also be controlled while learning the supervised retrieval embeddings.

The local sandbox remains a correctness/no-regression channel. It cannot
establish the real-data ceiling. A public real survey is a possible independent
screening channel: UNHCR's Jordan VAF catalog describes household demographics
and multiple vulnerability domains. It is a different survey, so even success
there is external validation, not an HSCC estimate. Catalog located, but the
microdata access endpoint returned an error/403 in this review; no data was
downloaded and access conditions have not been verified:
https://microdata.unhcr.org/index.php/catalog/1030/study-description

Inside the competition container, visible TRAIN supports real, fully masked
respondent validation and ordinary model selection. Those diagnostics cannot
be read outside the enclave; a submission is still needed for the external
DEV transfer reading. Do not describe this as a pre-submission observation.
If no non-injected screening channel can be made operational, the proposed
method remains unqualified under the standing submission rules.

### Practical limits

Use shared embeddings and bounded candidate batches, not 213 independent
retrieval networks. Profile actual fit, calibration and prediction against
the shared 900-second budget before packaging. No runtime or gain is measured
yet. Exact query exclusion is insufficient if validation labels enter other
training queries' reference banks: validation must exclude all such paths.

## Independent challenger: a tabular foundation model for the base

Hypothesis: E025's small shared network misses GIVEN interactions which a
pretrained tabular predictor can model. UNHCR has 8,279 visible TRAIN rows and
17 GIVEN columns. TabPFNv2's published evaluation regime includes datasets
up to 10,000 rows and 500 features, making it a concrete candidate, not proof
of performance here:
https://www.nature.com/articles/s41586-024-08328-6

Begin with schema-selected gate parents and a bounded set of content heads;
score all final descendants rather than the parent head alone. The return-
intention parent has 73 direct children. This targets the .79 base and can
affect the .079 gated residual, which also contains asked-answer errors.
Do not claim that the gated residual is all recoverable by better parents.
Compare fully out-of-sample probabilities, then measure overlap/complementarity
with the incumbent and the retrieval candidate before any composition.

The oracle for a frozen candidate library bounds only its mixture-selection
headroom. It cannot predict how good an unrun foundation model will be;
the pretrained forward pass must first be measured. This differs from building
a new fitted estimator before testing its oracle ceiling.

Official documentation supports offline weights and distinguishes code and
weight licenses. Newer default releases have separate non-commercial weight
terms and access flows; v2 has a different attribution-based license. Pin the
chosen version and verify its exact weights, terms, compatibility and runtime.
Do not assume a default pip install is reproducible. Competition data stays
inside the runner; no hosted inference API is part of this proposal:
https://github.com/PriorLabs/TabPFN

## Work order and decisions

1. Prioritize the supervised retrieval hypothesis; define the constrained
   oracle, secure a lawful non-injected screening dataset, and test whether
   meaningful headroom exists before building its estimator.
2. Screen the independent pretrained base on a small, schema-defined head set
   for feasibility and held-out complementarity. Neither target head choice
   nor reported gain may use hidden DEV labels.
3. Compare learned models on separate respondent splits with final-output
   scoring. Preserve the adoption bar and all A007 packaging checks. Keep
   initial hosted interventions UNHCR-only for attribution.
4. Spend one eligible slot on a qualified candidate; compose only after
   measured evidence. Maintain E025 as a fallback, not a mandatory architecture.

No honest per-method score forecast is available today. .94-.96 UNHCR is a
research target needed to move beyond the recorded leading .93, not a claim
that either proposal will achieve it. Flat or worse remains plausible.
The next deliverable is a go/no-go measurement, not another synthetic story
chosen to make a preferred architecture look successful.
