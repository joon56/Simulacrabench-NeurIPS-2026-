# A013 — E041 loss-probe resolution and method preparation
date-started: 2026-09-24
status: complete
relates-to: E041 / E054 / A012

## Goal

Determine what an E041 gated-item probe can identify before using a daily
submission, and finish a reviewable E041 four-page final-candidate method.

## Attempt log

### v1 — Fixed protocol and public-mechanism bounds

User approved the previous E054/method plan. Registrationa29fa9f precedes new
computation; implementationb57ec24 precedes output. No model fits or respondent
data in the resolution study. Analytic Laplace tail bounds use public epsilon,
floor, schema U and DEV respondent counts, never private random draws.

Public UNHCR constants:213PREDICT,156gated, U=1.261752202679108,
A=sum_gated(logK)/(213U)=.7391182798263595. Floor-derived minimum pooled losses
are .001700661446389479 gated and .000615250988946145 ungated. For baseline H
and probe P, L_G=A-H+P and L_C=1-A-P. These are losses relative to skill1,
not recoverable improvements or sentinel/asked-content causal components.

Simultaneous conditional noise envelopes use6draws (one fixed baseline and
probe) and93draws (at most30 prior3-instrument readings plus probe). UNHCR
tail bounds .004220649709356805 and .006636972550605420; rounding adds separate
uncertainty. No unconditional post-selection95% claim. Two Grand reporting
orders remain assumptions, not a verified description of the hosted code.

### v2 — Interval analysis and interpretation limit

Ten-variable linear programs retain common true controls and separate
baseline/probe noises. Baseline .64/.52/.49/.92 are noisy rounded observations.
The after-rounding model uses conservative outer intervals; passing arms need
a literal discrete reporting witness. Thus intervals need not be exact
discrete-model extrema and unresolved outer-feasible arms need not be attainable.
The enumeration includes all physically possible Grand values under these
assumptions. Negative true skill is allowed by the official probability floor.

| Probe Grand |93-draw before-rounding priority|93-draw after-rounding priority|Common reading|
|---|---|---|---|
|.38|Ungated|Ungated|Conditionally informative|
|.39|Ungated|Unresolved|Unresolved|
|.40-.42|Unresolved|Unresolved|Unresolved|
|.43|Gated|Unresolved|Unresolved|
|.44|Infeasible|Gated|Reporting models disagree|

Only.38 passes the archived implementation's93-draw existential criterion.
Its D=L_G-L_C bounds are [-.088235649658,-.078083464399] before rounding and
[-.088235649658,-.048083464399] in the after-rounding outer envelope. Both
are below-.015. Independent witnesses and closed-form extrema confirm this.
No arm passes both reporting orders under6draws: .38 is infeasible in its
before-rounding model. Enlarging uncertainty creates feasible tail arms even
while weakening precision. This is not evidence that more noise helps learning.

The prose registration's word "including93" did not explicitly specify a
conjunction across6/93 feasibility. The pre-result script explicitly used93
as its gate, supporting the implementation's interpretation. Report this
ambiguity; do not claim the result passes both noise envelopes. A strict
conjunction would STOP. No result-driven code or threshold change was made.

The .38 witness has almost all loss in ungated items and uses several noises
near their bounds. Feasibility supplies no probability, expected information
gain, or point score forecast. This probe therefore has limited decision value.
The prior suggestion that it would directly select gate repair versus content
repair was too strong: even exact item-group losses cannot identify that cause.

### v3 — Conditional exploratory package

Prepared E054 under the frozen implementation's packaging permission, with
the limitations above in its pre-run scorecard. Intervention/scorecard286ca28
precede package fitting. It preserves E041 base computation, then flattens only
final gated UNHCR outputs; nothing is propagated from the flattened vectors.
This is a deliberately lower-scoring measurement, not a model improvement.
No upload. Technical qualification PASS in its verification.json: official
skills .500648423071/.454717307363/.106532340789,338.472499s total. All189649
source/archive vectors exact;96876 gated UNHCR vectors uniform,92773 others
unchanged. Unmodified base is exact E041, delta0/0/-.000486144847 vsE025.
The intentional probe decrease matches the independent loss decomposition.

### v4 — E041 method candidate

E025 markdown/PDF preserved byte-for-byte in phase2-E025-preparation. E041
draft describes actual section retrieval, selection/replay mismatch, A011,
scoped E053 stop, A012 local engineering results and E025-only historical map.
Independent review restored A005's synthetic-only oracle and corrected the
E032 all-instrument versus E033/E034 UNHCR-only history. Four readable pages
rendered and visually inspected; six source/copy/backup hashes verified.
Adult and TabPFN developmental use disclosed; neither enters the E041 archive.
Current UCI/kit/weight license sources checked by implementer; Codabench HTML
and API were inaccessible to the tools for current terms. Clause7 attribution
therefore explicitly remains the repository's earlier API audit, not a new check.

### v5 — Observed-channel source scout

Official2023 SIPP documentation offers a candidate observed household/question-
universe channel. No microdata downloaded or model fitted. Repeated person-month
rows, copied household fields, recodes and imputation require an encoding and
leakage audit before any oracle or gain claim. See observed-channel-scout.md.

## Verification and findings

- Nine resolution tests PASS; four intervention tests PASS. No model fit in tests.
- Independent math review:21source/witness/closed-form checks PASS, extrema
  agree within5e-16. Separate pre-run package review found no blocker.
- Independent artifact review recomputes all3 scores, exact vectors and frames,
  hashes, target mask, decomposition and timing:758740checks PASS without fits. Its first
  run stopped on a UTF-8 BOM in method-validation.json after model checks;
  only the verifier's JSON reader changed to utf-8-sig before rerunning.
- [consistent] Uniform ablation maps model loss by schema item group.
- [unchecked] It does not reveal gate mechanism, recoverable gain or TEST ranking.
- [surprising] The formal informative arm appears only under the wider noise
  feasibility set. Preserve that limited result without presenting it as robust
  across sensitivities or likely worth a submission.

## Artifacts and next decision

docs/analysis/A013-outputs/; docs/analysis/E054-outputs/;
submissions/2026-09-24-E054/; docs/method-4p.md;
submissions/phase2-E041-preparation/method-4p-E041.pdf.

E041 remains incumbent and E025 fallback. A group-loss reading alone must not
trigger a recursive estimator. Further score-improvement work needs a named
model operation, a validation channel that naturally exercises it, and an
oracle bound appropriate to the coupled family. No additional Adult seeds,
assumed favorable simulator, blanket weight grid or automatic hosted upload.
