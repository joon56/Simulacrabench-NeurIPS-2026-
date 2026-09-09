# Experiment log

Daily record. Domain literature: [[domain]] · kit mechanics: [[starter-kit-notes]].

## 2026-08-30 — E007 parked on the numbers; E008 logistic blend adopted, submission #4

- **E007 (eRPIS prior blend) PARKED without implementation** — quantitative
  pre-check killed it: phase 1 exposes all 8,279 unhcr TRAIN rows, so
  country×wave cells hold n ≈ 1–2k real answers and a W-pseudo-count prior
  shifts the posterior by ≤ W/(n+W) of a difference that has no systematic
  sign (TRAIN and DEV are the same build). Expected Δ ≈ 0; rule 5 blocks
  the spend. The A003 CSV is repurposed as a standing sanity anchor
  (models should reproduce the published s3_11 country tables). Revive
  conditions recorded in the experiment file.
- **E008 (full-GIVEN logistic blend) implemented and adopted**: per
  PREDICT item, multinomial logistic on the one-hot full GIVEN block
  (7/30/72 columns vs the ladder's 3), mixed in probability space with
  the E006 ladder; one blend weight per instrument tuned on the internal
  20% holdout. Gate recursion + E003 softening unchanged. Runner: 3-inst
  mean 0.4783 → 0.4991 (**Δ +0.0208**, largest since E004; every schema
  up). Tuned w interior everywhere (0.6/0.9/0.8/0.6) with smooth concave
  curves — ladder and logistic are complements, not substitutes.
  max_iter probe: 1000 reproduces all skills to 4 decimals (cap
  immaterial, kept 200). Wall-clock ~182 s ≪ 900 s. Tests 27/27.
- **Smoke-check regression caught by check_submission_zip**: the kit's
  3-row smoke frame makes the tuning holdout empty → sklearn raised on a
  0-sample matrix. Guards added (empty split ⇒ w=0 ladder-only; w=0 skips
  all encoding/fits; gated items with zero asked rows fall back to
  ladder). Local harness never hits these paths — the zip checker is the
  only pre-submission probe that does; keep running it BEFORE spending
  the daily slot.
- **Submission #4 packaged** (`submissions/2026-08-30-E008/`, zip OK).
  LB expectations pre-registered in SCORES.md: Grand ≈ 0.57–0.59; the
  falsifiable claim is world_bank moving off 0.48 for the first time
  (psychometric GIVEN block = many weak predictors only the logistic
  sees); unhcr largest absolute gain; any instrument −0.02 ⇒ overconfident
  logits ⇒ C-grid / per-item w before next spend.

- **E008 submitted; result: Grand 0.58 — unicef 0.51 / wb 0.49 /
  unhcr 0.74** (E006: 0.50/0.48/0.66). Scorecard: Grand in the 0.57–0.59
  pre-registered band ✓; unhcr largest ✓ (+0.08, ~4–5× sandbox Δ — third
  straight submission where real GIVEN coupling beats the sandbox trait);
  unicef smallest ✓; no drops ⇒ no overconfidence ✓. One OPEN item: wb
  +0.01 is inside noise — the psychometric many-weak-predictors claim is
  neither confirmed nor falsified; resolve with a wb-targeted change
  before investing further in that story. Reading: unhcr headroom still
  live (0.74 with cheapest U and 155-parent cascade); next capacity step
  is E009 = more capacity where the logistic paid (per-item blend
  weights + C grid, then GIVEN interactions via boosted trees on the
  holdout), all locally verifiable before the next slot.

## 2026-09-02 — three nulls measured cheap; E012 shared-trunk net adopted, submission #6

- **A004 (wb structural pass) done**: corrected our own notes — wb GIVEN
  is 9 columns (21 of the non-PREDICT items are EXCLUDE), gates are
  near-exhausted (27/30 GIVEN-parented, 19 on the tracer `group` arms),
  so E008's "many weak predictors" story was mis-premised. 24 PREDICT
  items strict-parse numeric (spans K=15, counts K=12–13) → ordinal
  lever identified; sandbox provably cannot show it (random per-option
  loadings in make_sandbox).
- **E011 (ordinal kernel smoothing) REJECTED on its own sim channel**:
  clean sandbox ≡ E010 (off-by-default works), but sim v1 (+0.0003) and
  a deliberately favorable thin-cell sim v2 (+0.0000) measured the
  option-axis pooling headroom at ~0 — κ-ladder + logistic already
  exhaust it at n≈5k. Honest null, mirrors E007. Sim assertion kept as a
  strict xfail (the recorded null).
- **Seed-bagging probe killed before implementation**: E010 with holdout
  seeds 0/1/2 → 3-inst mean 0.4991/0.4988/0.4989 (spread 0.0003).
  Selection is stable; bagging would buy ~nothing at 2–3× runtime.
- **E012 (shared-trunk multi-head net) implemented and ADOPTED**: per
  instrument, one-hot GIVEN → 64-64 ReLU trunk → per-item softmax heads
  + masked asked-only conditional heads (torch, early stopping, fixed
  seed); replaces the 76–213 independent logistics; ladder blend w and
  E010 conditional agreement unchanged. Runner 3-inst 0.4991 → 0.5061
  (**Δ +0.0070**): wb +0.0102 (first wb movement anywhere), unhcr
  +0.0097, unicef +0.0012 — exactly the heads-count ordering
  pre-registered. The day's pattern in one line: per-item knobs, option
  smoothing, priors, bagging all ≈ 0 — the paying move was the
  model-CLASS change (nonlinearity + cross-item sharing).
- **Submission #6 packaged** (`submissions/2026-09-02-E012/`,
  script-assembled from verified src modules, parity exact, zip OK,
  score.py PASS 0.50/0.45/0.56, ~200 s ≪ 900 s). LB pre-registration:
  Grand 0.60–0.62; wb 0.49 → 0.50+ is the falsifiable core (sectioned
  multi-factor thesis); unicef ~flat; any −0.02 ⇒ net memorization ⇒
  lower w cap or revert to E010.

- **E012 submitted; result: Grand 0.60 — unicef 0.52 / wb 0.49 /
  unhcr 0.78** (E010: 0.51/0.49/0.77). Grand in band (bottom edge) ✓,
  unhcr +0.01 ✓, unicef +0.01 ✓ — but **wb flat, the falsifiable core
  FAILED**: fifth straight wb submission at 0.48–0.49; sandbox +0.0102
  did not transfer.
- **User leaderboard observation (same day, strategic)**: teams ranked
  ABOVE us have ~identical unicef and wb — the entire gap is unhcr.
  Combined with our own wb null series, conclusion upgraded: wb (9
  GIVEN cols) and unicef (7 GIVEN, deterministic gates) are near their
  INFORMATION CEILINGS for every serious team — they no longer rank
  anyone. The competition is decided on unhcr (70% of scored cells,
  cheapest U 1.2618, 72 GIVEN, 156 approximate gates, 2 waves).
  All future spend goes to unhcr until shown otherwise. Candidate
  unhcr edges the leaders may hold, in evidence order: (1) capacity —
  the established real>sandbox coupling amplification means our
  64-64 trunk is likely undersized for the real 72-column signal
  (locally near-invisible, real gain — the E008 pattern); (2) joint /
  consistent decoding of the three overlapping s3_11 branches
  (schema-documented overlap, unexploited); (3) cross-wave record
  linkage of the flattened panel (A001: real design is a panel) —
  legality UNCLEAR under the re-identification clause: forum question
  FIRST, never unilateral.

- **Leaderboard intelligence (same day, decisive): teams above us show
  unhcr ≈ 0.92.** Arithmetic: skill 0.92 ⇒ (0.92−1)×1.2618 ≈ −0.101
  nats/cell ⇒ average 90% probability on the realized answer across all
  132k cells INCLUDING attitude items (we: −0.278 ⇒ 76%). GIVEN-only
  conditioning cannot plausibly reach that; the one mechanism that can
  is **cross-round panel linkage** (A001: real design is a panel,
  flattened; A002: both rounds inside one fieldwork window ⇒ same
  person's answers nearly identical across rounds; 72 GIVEN roster
  columns = a fingerprint). Classic DEV-probing overfitting is ruled
  out by the reusable-holdout arithmetic (ε=10 + 0.01 rounding + 1/day
  cannot yield +0.14 skill). Their phase-2 risks: (1) the
  re-identification/disqualification clause — legality of within-
  dataset record linkage is THE open question; (2) organizers may have
  built TEST from twin-less respondents (roles fixed at build) — the
  precise sense in which 0.92 could be "DEV overfitting"; (3) mandatory
  4-page method disclosure in phase 2.
- **Decisions**: (a) forum question on linkage legality FIRST (bundled
  with the GATE_CORRECTIONS.md question, still unposted); (b) prepare a
  conditional linkage module — runtime detection of duplicate roster
  signatures on visible real data, used only if found; harmless/inert
  on the sandbox (independent rows by construction) — but SUBMIT ONLY
  after an organizer ruling; (c) meanwhile continue the legitimate
  axis: E013 = unhcr-targeted capacity scale-up.

- **ORGANIZER RULING (email, Andy, same day)**: "Matching rows within
  the dataset — which does not extract identities outside of the
  enclave — is permitted." Cross-round linkage is LEGAL. Also disclosed:
  (1) "a few (<5) changes to gating in UNHCR that we still need to
  ship" — a kit/schema update is coming, re-audit on arrival (gate
  structure our E010 conditional-agreement layer depends on may move);
  (2) the dangling GATE_CORRECTIONS.md reference is removed for now;
  (3) prize-money announcement pending. Strategy consequence: E013 =
  cross-round respondent linkage (runtime-detected, stability-
  calibrated) is now the top-priority experiment; capacity scale-up
  moves to E014.

- **E013 (cross-round linkage) implemented and ADOPTED, submission #7
  packaged** (`submissions/2026-09-03-E013/`, upload tomorrow). Layer:
  round column from schema (2-valued wave/round GIVEN); FUZZY 1:1
  matching on the remaining GIVEN signature (≤2 mismatches, 90%
  relative floor, runner-up margin ≥2, claim resolution); per-item
  cross-round stability from visible-visible pairs (β-shrunk α=20)
  mixes the twin's answer into the E012 belief BEFORE the gate cascade;
  MIN_PAIRS=30 guard (added after the clean sandbox produced exactly 1
  spurious collision). Evidence: clean runner bit-identical to E012
  (isolated rerun; a contended run exposed torch CPU reduction
  nondeterminism worth ±0.0006 — noted); panel sim +0.2293 log
  (exact twins), +0.2003 (30% GIVEN-drift twins — fuzzy recall);
  zip OK, parity exact, suite 47 passed + 1 xfail. LB pre-registration
  in SCORES.md: unicef/wb structurally inert; unhcr 0.85–0.92 if the
  panel hypothesis holds; 0.80–0.84 ⇒ recall-bound (widen fuzz);
  flat ⇒ hypothesis wrong, re-open the 0.92 analysis; down ⇒ false
  matches (raise margins). Kit watch: "<5 gating changes" unshipped —
  full harness re-run required if an update lands before upload.

## 2026-09-03 — E013 result: flat; linkage hypothesis unresolved, cheap diagnostics queued

- **E013 submitted; result: Grand 0.60 — 0.52/0.49/0.78, identical to
  E012.** unicef/wb inert ✓ (as designed); **unhcr flat = the
  pre-registered flat arm**. Zero damage (guards worked) but zero gain:
  the fuzzy matcher armed nothing on real data. Two candidate causes,
  outside-indistinguishable: (a) rounds genuinely disjoint (organizers
  built the flattening that way) — then the 0.92 mechanism is NOT
  simple linkage, re-open that analysis; (b) real cross-round GIVEN
  drift > 2 of 71 columns (age-band shifts move paired roster columns;
  a different household respondent moves many), so MIN_PAIRS never
  armed. E013 experiment status updated: adopted → parked (no harm, no
  evidence of real-data function; revive on overlap confirmation).
- Decisions: (1) ask Andy directly whether the two CATI rounds share
  respondents — zero-cost, resolves (a) instantly; (2) E014 designed =
  two-stage probabilistic linkage (loose blocking on a data-selected
  stable column subset → per-column entropy-weighted similarity →
  margin + absolute acceptance, column stability re-estimated from
  confident seed pairs), same inert-by-guard safety — flat again would
  falsify overlap conclusively; (3) kit watch unchanged ("<5 gating
  changes" still unshipped as of the E013 upload).

- **Parallel session (same day): E015 parked, E014 v2 adopted,
  submission #8 packaged.**
  - **E015 (trunk capacity grid)**: shared_trunk parameterized (default
    bit-identical to E012, verified); per-instrument selection over
    {64,128,256}×{2,3}+dropout. Runner Δ +0.0001 → parked per the
    pre-registered fallback; third confirmation that the 1-factor
    sandbox caps capacity gains; no leaderboard-loophole adoption.
  - **E014 v1 (hard Fellegi–Sunter) discarded by its own diagnostics**:
    the unhcr signature is ~16 GIVEN columns, not 72 (EXCLUDE counted —
    same error A004 caught on wb); seed-vs-random score gap 1.3 ⇒ hard
    matching unseparable under drift, and E013's real-data flat re-read
    as COLLISIONS (uniqueness margin rejected concentrated cells).
  - **E014 v2 (soft posterior evidence mixing) ADOPTED**: rarity-
    weighted (−log u_j) agreement scores = log-LR ⇒ softmax posterior
    over top-10 other-round candidates ⇒ posterior-mixed answers as
    evidence ⇒ per-item λ calibrated by replaying on visible rows. No
    uniqueness, no hard guards — collisions share mass, no signal ⇒
    λ→0. Discovered en route: vs a weak model the layer acts as k-NN
    conditioning (trait-similar neighbours) — kept, documented; vs the
    full net on clean sandbox it is redundant (unhcr −0.0002, in
    bound). Heavy-drift scored sim **+0.1556 log**; collision sim
    213/213 items stay armed. Suite 51+1 xfail; zip OK; score.py PASS
    0.50/0.45/0.56. The submission IS the overlap experiment: unhcr
    ≥+0.02 ⇒ overlap real (E013 died on collisions); flat ⇒ overlap
    dead, linkage abandoned, 0.92 question re-opens; +0.01 ambiguous
    (k-NN residual) — thresholds pre-registered in SCORES.md.

## 2026-09-10 (session 3) — E028 adopted and packaged as submission #16

- **E028 (parent-value-conditional gate decoding)**: v1 leaked ~0.5%
  sentinel mass on exact gates (shrink target = pooled rate); v2
  shrinks r_v toward the hard-gate prior — clean sandbox identical to
  E025. Branch-overlap sims: light (30% of round-2 No → Yes-branch)
  +0.0017; **heavy (70% of No+DK, both waves — inside the schema's
  documented 0.29–0.98 agreement range) +0.0121 log**. Adopted (E003
  route); parity exact, zip OK, score.py PASS 0.50/0.45/0.56.
  Queue: E027 (#15) first, then E028 (#16) — one change per reading.
  Readings: unhcr 0.90+ ⇒ real overlap heavy, condition A_v further;
  0.89 ⇒ E010 already had it; ≤0.88 ⇒ thin tables, revert.

## 2026-09-10 (session 2) — E027 packaged as submission #15; E028 (PVC gate decoding) built

- **E027 (concentrated-row evidence as net input, over E025)**: E024's
  harm removed by restricting the block to rows with max posterior
  ≥ 0.5 — household sim +0.0011, clean sandbox within ±0.002 (3-inst
  −0.0006), ~330 s local CPU (GPU absorbs training). Adopted as a
  pre-registered A/B on real cross-item household structure; parity
  exact, zip OK, score.py PASS. Readings: unhcr 0.90 ⇒ extend; 0.89 ⇒
  close the evidence-input idea; ≤0.88 ⇒ pin E025.
- **E028 (parent-value-conditional gate decoding) built**: the s3_11
  parent has three single-value branches (Yes 21 / No 40 / DK 11
  children); the hard/soft/agreement gate math is replaced by
  Σ_v b_parent[v]·[(1−r_v)·A_v + r_v·sentinel] with r_v, A_v estimated
  per parent value from visible rows (E010's selected column splits
  r_v; κ-smoothing). Exact gates reproduce the hard gate. Branch-overlap
  sim (round-2 No-respondents answering Yes-branch children from a
  skewed distribution) is the positive-evidence channel — running.

## 2026-09-10 — E026 result: flat at 0.63; capacity axis complete

- **E026 submitted; Grand 0.63, no update (≤ E025).** Pre-registered
  0.89 arm: 128×2 is the real optimum, wider/deeper trunks add nothing
  — the capacity axis is now fully characterized (E015 local null,
  E017 +0.01, E025 +0.01 stacked, E026 flat). Four trainings per
  instrument ran without timeout: the hosted GPU path is robust.
  E026 parked; **E025 stays best: 0.63 (0.52 / 0.49 / 0.89).**
- State of the search: matching layer saturated on its sim (E023),
  capacity complete (E026). Remaining levers, ranked: (1) E024-variant
  A/B — evidence block as net input restricted to rows with a
  concentrated posterior (removes E024's duplicate-free harm; tests
  cross-item household structure the sim cannot model); (2) joint
  decoding of the overlapping s3_11 branches (structural, needs its own
  sim); (3) phase-2 preparation (3600 s budget ⇒ lift CAL_QUERIES cap,
  DEV visible ⇒ larger pool; the layer self-calibrates).

## 2026-09-09 (session 2) — E026 (full capacity grid) packaged as submission #14

- **E026 = E025 with E017's full 4-config grid** restored (256×2+do,
  128×3+do added). Sandbox picks 128×2 again (blind to capacity):
  0.5006 / 0.4548 / 0.5629 — layer parity held. ~420 s local CPU; the
  hosted H100 absorbs training (E025 precedent); GPU-failure fallback =
  E025. Readings pre-registered: unhcr 0.90 ⇒ wider trunk real, push
  further; 0.89 ⇒ capacity complete at 128×2; ≤0.88 ⇒ pin E025.

## 2026-09-09 — E025 result: unhcr 0.89 (+0.01); capacity axis re-opened; GPU path confirmed

- **E025 submitted; result: Grand 0.63 — 0.52 / 0.49 / unhcr 0.89**
  (+0.01 over E022). The ≥0.89 pre-registered arm: E017's +0.01 was a
  real gain hidden in the ±0.01 band, and it stacks with the evidence
  layer. Grand 0.633 still rounds to 0.63 — the next unhcr +0.01 tips
  it to 0.64. Ran without timeout at ~300 s local CPU ⇒ **hosted H100
  training path confirmed alive**; the effective budget for
  CPU-side work stays ~130 s local, training is now nearly free.
- Score path: 0.43 → 0.53 → 0.55 → 0.58 → 0.60 → 0.63 (unhcr 0.78 →
  0.87 → 0.88 → 0.89). Two stacked +0.01 refinements in two days —
  the "3–4 more" estimate to 0.92 now reads 3 more.
- Next (E026): the rest of E017's grid — {256×2+do, 128×3+do} added
  to the selection — is the cheapest leaderboard-backed step (GPU
  absorbs the extra trainings); after that, phase-2 planning (DEV
  visible ⇒ household coverage rises for TEST rows; the layer
  self-calibrates, but the runtime budget doubles to 3600 s).

## 2026-09-08 (session 2) — E023/E024 null, E025 composition packaged as submission #13

- **E023 (replay-selected K + second EM iteration) REJECTED**: K-select
  +0.0000, EM2 −0.0001, both −0.0001 on the hard household sim. The
  matching layer is saturated at E022 on this sim family (weights
  converge in one pass; the posterior already ignores random
  neighbours). Same-wave weighting was dropped before running — `wave`
  is a signature column, so its weight is already learned.
- **E024 (evidence-input net as E022's base) PARKED**: household sim
  +0.0004 (no cross-item structure to learn there), but the clean
  sandbox is DOWN on all three instruments (3-inst −0.0011, wb −0.0016)
  — on duplicate-free data the evidence block is a noise feature —
  and runtime 216 s. Not worth a slot ahead of leaderboard-backed
  compositions; revive with the block restricted to concentrated rows.
- **E025 = E022 ∘ E017 capacity grid ADOPTED for submission #13**:
  re-reading E017's unhcr +0.01 by the standard E022 just validated
  (+0.01 = a real ~+0.009 skill gain), the two independent gains should
  stack. Clean runner: layer parity held (0.5006 / 0.4548 / 0.5629).
  Runtime 297 s local on CPU — above the observed hosted failure point;
  the worker's H100 (kit baseline uses the same `cuda if available`
  pattern) removes the ~140 s of training cost; timeout fallback
  pre-registered (pin configs). Readings in SCORES.md: unhcr ≥ 0.89 ⇒
  stack real; 0.88 ⇒ capacity closed for good; ≤ 0.87 ⇒ revert.

## 2026-09-08 — E022 result: unhcr 0.88 (+0.01), sim instrument validated quantitatively

- **E022 submitted; result: Grand 0.63 — 0.52 / 0.49 / unhcr 0.88**
  (+0.01, the pre-registered +0.01 arm; Grand stayed on the 0.63 side
  of rounding). The household sim's +0.0116 log (≈ +0.009 skill)
  transferred essentially exactly — after E018 (direction and rough
  size) and E019 (below resolution) this is the third consistent
  reading: the sim is now a QUANTITATIVE instrument for the evidence
  layer. Strategic reading: the tuning family stacks at ~+0.005–0.01
  skill per sim-verified refinement; unhcr 0.88 → 0.92 = 3–4 more.
  Grand gap to the ~10 teams above is 0.01–0.02 (unicef/wb equal for
  everyone), i.e. one or two stacked steps.
- Queue for E023 (all household-sim measurable): (1) TOP_K selected by
  replay (households have 1–3 co-respondents; K=10 dilutes with random
  neighbours); (2) second weight-estimation iteration on the purer
  pairs pass 1 produces; (3) same-wave candidate weighting (household
  composition drifts across rounds); (4) per-item λ split by
  household-level vs person-level items if (1)–(3) leave headroom.

## 2026-09-07 (session 2) — perf pass committed; E020 rejected; E021/E022 household matching, submission #12

- **Runtime pass committed** (`8066055`): ladder candidate scoring and
  evidence accumulation vectorized (outputs identical to 1e-15 / 4
  decimals), GPU training with CPU fallback; E018 240 → 146 s local;
  suite 57 passed + 1 xfail.
- **E020 (twin evidence as net input) REJECTED on sim**: the 40%-
  perturbed dup sim still credits E019 +0.0187 (real was flat) and E020
  scores −0.0211 vs E018. Re-diagnosis of the E018/E019/E020 trio: real
  matches are **household co-respondents** — roster columns shared,
  person-level GIVEN columns differ, answers correlate per item rather
  than copy.
- **Household sim built** (roster copied, person columns resampled,
  per-item copy rate ρ): the first instrument whose structure matches
  that diagnosis. **E021 (data-estimated signature weights, one
  Fellegi–Sunter iteration)**: learned weights roster 3.08 vs person
  1.39; +0.0100 log (ρ≤0.95), +0.0068 (ρ≤0.8). E019 on the same sims
  +0.0097 / +0.0053 — i.e. the real "flat" is what a +0.005–0.01
  gain looks like under 0.01 rounding + noise; the sims are not
  contradicted, the leaderboard just cannot resolve single refinements.
- **E022 = E021 ∘ E019 ADOPTED**: hard sim +0.0116 log (near-additive),
  clean sandbox in bound (unhcr +0.0001), 154 s local. **Submission #12
  packaged** (`submissions/2026-09-08-E022/`, parity exact, zip OK,
  score.py PASS 0.50/0.45/0.56). Readings: ≥+0.02 ⇒ family stackable;
  +0.01 ⇒ consistent, repeat; flat ⇒ close layer tuning for phase 1;
  down ⇒ raise PAIR_MASS/CONC_SPLIT.

## 2026-09-07 — E019: hosted timeout then flat; runtime pass in progress

- **E019 first upload: time limit exceeded.** Same zip re-uploaded the
  next day RAN → the failure was hosted worker-speed variance (E017 v1
  most likely the same). Timing model corrected: hosted/local ratio is
  not 1.94–2.6× but fluctuates past ~3.75× on bad days; new working
  ceiling **≤ ~130 s local**.
- **E019 result: Grand 0.63, no update** — ≤ E018, unhcr within noise of
  0.87. Flat arm: real twins noisier than the sim's 10%-perturbed
  copies; λ ceiling / concentration buckets bought nothing real. E019
  status → parked (harmless, no gain). Instrument lesson: the dup sim
  predicted E018's direction and roughly its size, but over-predicted
  E019 — re-calibrate the sim's perturbation before trusting it for
  further layer tuning.
- **Runtime pass (model-neutral) underway**: `hier_backoff._eval_candidate`
  vectorized (cells factorized once, [cells,K] count matrices, numpy
  scoring over all κ; ladder selections identical, history scores equal
  to 1e-15; unhcr selection 73 s → ~15 s with per-item code caching),
  `prob_link._evidence` vectorized (np.add.at accumulation), and
  `shared_trunk` training moved to the hosted H100 when available with
  CPU fallback on any GPU exception. E019 runner after the first two
  edits: identical scores, 240 s → 145 s. Parity of the GPU-path edit
  (CPU no-op) and full-suite run still pending before commit.

## 2026-09-06 (session 2) — E019 sharpened evidence layer adopted, submission #11

- **E019 implemented and ADOPTED**: two calibration refinements over
  E018 — λ grid extended to {…, 0.95, 0.98} (the 0.9 ceiling forced
  10% model mass onto every exact-twin cell), and per-item λ split into
  (diffuse, concentrated) buckets at max posterior weight ≥ 0.5, each
  replay-calibrated (exact twins want λ≈0.98, diffuse k-NN rows want
  it low; one λ was a compromise; the bucket is also the guard against
  the higher ceiling since false matches are diffuse). Evidence: clean
  runner identical to E018; on the within-round dup sim — now a
  LEADERBOARD-VALIDATED instrument (its ≥+0.02 arm fired at +0.09) —
  **E018 −0.4849 → E019 −0.4537, +0.0312 log** (6× the bar);
  concentrated-bucket λ exceeds 0.9 on twins, concentrated ≥ diffuse on
  average. ~240 s local. Suite additions 2/2.
- **Submission #11 packaged** (`submissions/2026-09-07-E019/`, parity
  exact, zip OK, score.py PASS 0.50/0.45/0.56). Pre-registered: unhcr
  ≥+0.02 expected (0.89–0.91, Grand ≈ 0.64); flat ⇒ real twins noisier
  than the sim's 10% perturbation; DOWN ⇒ λ=0.98 on false-but-
  concentrated matches ⇒ raise CONC_SPLIT to 0.8 / cap at 0.95.

## 2026-09-06 — E018 result: BREAKTHROUGH — Grand 0.63, unhcr 0.87

- **E018 submitted; result: Grand 0.63 — unicef 0.52 / wb 0.49 /
  unhcr 0.87** (+0.09 unhcr, largest jump of the campaign alongside
  E008). The ≥+0.02 pre-registered arm fired at 4.5× its bar:
  **within-round near-duplicates are real and abundant** — the axis
  E013/E014's cross-round-only pools were structurally blind to.
  unicef/wb flat = their λ self-calibrated to ~0 (no duplicate
  structure), the layer behaving exactly as designed. Rough inversion
  says a third to half of unhcr DEV rows have a usable visible twin —
  structural in the build, not accidental. **The leaders' 0.92 is now
  essentially explained: same axis, tighter tuning.** Gap to close:
  0.05.
- Known headroom for E019 (tighten the layer, locally verifiable on
  the dup sim + replay): (1) LAMBDA_GRID caps at 0.9 — a near-exact
  twin wants 0.95–0.98; (2) TOP_K=10 softmax posterior may dilute a
  dominant twin — tune K / posterior sharpness on the replay;
  (3) agreement weights are first-pass rarity (−log u_j) — an m_j
  iteration from high-λ matched pairs could sharpen matching;
  (4) evidence currently mixes at item level — a per-(item, posterior-
  concentration) λ could trust exact twins more than diffuse ones.

## 2026-09-05 (session 2) — EXCLUDE leak ruled out; E018 full-pool evidence adopted, submission #10

- **EXCLUDE answer-key hypothesis closed in 10 minutes, locally**: the
  kit's `generated_items()` provably never generates or ships EXCLUDE
  items ("never generated, never shown") — no leak path in the file.
- **E018 (full-pool visible-row evidence) implemented and ADOPTED
  (E003 route)**: E014's evidence layer generalized — candidates = ALL
  visible rows, self excluded (unit-tested), no round-column gate, so
  within-round near-duplicates (household co-respondents, re-dials,
  double entries) are finally in scope; per-item λ replay unchanged
  (its in-sample bias is conservative — errs toward λ low). Runtime
  guard: calibration replay capped at 6,000 queries; 250 s local =
  worst-case ~650 s hosted under the E017 bracket. Evidence: clean
  runner unhcr −0.0003 (in bound), others identical; within-round dup
  sim +0.0588 log scored, layer arms 159 items where E014's
  cross-round pools arm 40. Scope honesty pre-registered: the 0.92
  arithmetic needs ~71% twin coverage — this hunts a partial gain,
  not the gap.
- **Submission #10 packaged** (`submissions/2026-09-06-E018/`, parity
  exact, zip OK, score.py PASS 0.50/0.45/0.56). Readings in SCORES.md:
  any instrument ≥+0.02 ⇒ duplicates real, tighten; all flat ⇒ the
  ENTIRE row-matching family (E013/E014/E018) closes and the 0.92
  question narrows to joint branch decoding, calibration, or something
  unconceived; unicef/wb carry the layer for the first time — live
  readings now, not controls.

## 2026-09-06 — E017 v3 ran (after v1 hosted failure); capacity direction closed

- **E017 v1 FAILED on the platform** (first hosted failure; code
  unretrieved, timeout suspected — 465 s local vs the passing family's
  200–250 s). v2 ({64,256}) discarded on measurement (unhcr selector
  fell back to baseline — blind A/B); **v3** kept exactly the full
  grid's winners {64×2, 128×2+dropout}, reproducing v1's selections at
  340 s local. Lesson recorded: hosted wall-clock has never been
  observed — treat ~350 s local as the working ceiling until an
  organizer answer or a timing probe says otherwise.
- **E017 v3 result: Grand 0.60 — 0.52 / 0.49 / 0.79** (unhcr +0.01).
  Scored strictly against the pre-registration: unicef control clean,
  wb flat, unhcr inside the ±0.01 flat band, below the +0.02 evidence
  bar. **Capacity direction CLOSED** — the 0.92 gap is not
  architecture. Eliminated to date: priors, per-item tuning, ordinal
  smoothing, seed bagging, cross-round linkage (hard+soft), geography
  cells (locally), capacity (locally ×3 and now on the leaderboard).
- Carried-forward suspects, next session's queue: (1) **within-round
  duplicate rows** — E013/E014 candidate pools were strictly
  cross-round; same-round near-duplicates (household co-respondents,
  re-dials) straddling TRAIN/DEV would be an answer key our design
  never looked at; one-line pool extension, same self-calibrating λ
  safety; (2) joint decoding of the overlapping s3_11 branches;
  (3) per-item temperature calibration.

## 2026-09-05 — E013/E014 grand confirmed 0.60 each; linkage line CLOSED

- **User confirmed from the submissions panel: E013 and E014 both
  scored Grand 0.60** — identical to E012, no failures. Platform
  behavior also confirmed (Codabench organizer settings hide individual
  submission score detail; Force_Best-style leaderboard keeps E012's
  row). The "no update" mystery = tie at 0.60, not crashes.
- **Linkage line CLOSED, definitively**: two independent designs — hard
  1:1 fuzzy (E013) and soft posterior with self-calibrating λ (E014) —
  both inert on real data. Best remaining explanation of the whole
  arc: the organizers ROLE-ALIGNED panel twins when flattening (both
  rows of a person land in the same TRAIN/DEV/TEST bucket), which (a)
  makes cross-round matching harmless by construction, (b) explains why
  Andy permitted it so casually, and (c) means NOBODY's 0.92 comes from
  linkage. The overlap question to Andy remains worth sending as
  confirmation, not as a decision input.
- **0.92 question re-opened with linkage eliminated.** Ranked remaining
  hypotheses: (1) real-data capacity/conditioning gains the 1-factor
  sandbox provably cannot measure (E015 grid parked at +0.0001 local —
  a pre-registered leaderboard A/B is the only instrument); (2)
  unexploited unhcr specifics — note MAX_CARD=12 excludes
  governorate_col (K=46) and origin_governorate (K=16) from the LADDER
  (the net sees them one-hot, cell tables never did) — cheap, locally
  measurable; (3) sharper round-2 sentinel handling beyond E010.
  Next session: (2) first (local, free), then design the (1) A/B.

- **Same-day session: E016 rejected; E017 (capacity A/B) packaged as
  submission #9.**
  - Score-equality analysis for the user's question recorded: scenario
    (c) (unhcr down, others up) is structurally impossible — the
    linkage layers cannot touch unicef/wb; (b) bit-inert is the
    dominant read (guards/λ verified to degenerate); display noise
    (fresh Laplace per submission) is the fourth possibility — equal
    displays ⇒ (near-)identical outputs.
  - **E016 (ladder MAX_CARD 12→64) REJECTED at +0.0002** — but the
    watch point paid: the unhcr ladder DID swap country_asylum for
    governorate_col at depth 3; the mechanism works, the uniform-trait
    sandbox just can't value geography. Claim moved to the A/B pool.
  - **E017 = pre-registered leaderboard A/B of the E015 capacity grid**
    (the park verdict's named revive path; rule-4 audit in the file:
    verified-no-harm change spent as measurement on the one axis three
    local nulls prove the sandbox cannot see). Parity exact, zip OK,
    score.py PASS 0.50/0.46/0.56, ~465 s ≪ 900 s. Readings
    pre-registered: ≥+0.02 on unhcr/wb reopens capacity as main line;
    flat kills architecture spending for good; ≤−0.02 pins the default
    config; unicef is the control.

## 2026-09-04 — E014 result: no leaderboard update (≤ E012); linkage line provisionally closed

- **E014 submitted; leaderboard did not update — E012 (0.60,
  0.52/0.49/0.78) remains best.** Exact E014 triple pending from the
  Codabench My Submissions page (leaderboard only shows the best
  entry). Provisional reading per the pre-registered table: no update ⇒
  unhcr gain < +0.02 ⇒ the FLAT arm — with BOTH the hard 1:1 matcher
  (E013) and the soft posterior + self-calibrated λ layer (E014)
  finding nothing, the round-overlap hypothesis is effectively dead
  unless the exact triple or an organizer answer says otherwise.
- Consequences queued: (1) get the exact E014 triple (user, My
  Submissions); (2) the overlap question to Andy is now the cheapest
  decisive bit — if "no overlap", linkage is closed for good and the
  0.92 mechanism question re-opens with linkage eliminated; (3) next
  experiment direction if closed: the 0.92 gap must then come from
  modelling — E015's capacity grid as a pre-registered leaderboard A/B
  (sandbox provably cannot measure it), and/or unhcr-specific
  structures not yet exploited (round-2-only sentinel families beyond
  E010, joint decoding of the overlapping s3_11 branches).
- E014 status: adopted → parked pending the exact triple (no harm
  anywhere — the inert-by-calibration design held on real data too).

## 2026-09-01 — E009 rejected; E010 conditional agreement adopted, submission #5

- **E009 (per-item C+w blend) implemented and REJECTED**: per-PREDICT-item
  (C, w) grid on the internal holdout. Runner Δ +0.0013 < +0.005 (wb
  +0.0016, unhcr +0.0022, unicef flat). Pre-registered winner's-curse arm
  fired. Deeper lesson recorded in the experiment file: the sandbox
  generator is single-trait with uniform coupling, so the main-effects
  logistic is locally near-optimal — capacity-axis experiments (per-item
  tuning, boosted interactions) are locally capped BY CONSTRUCTION; the
  next locally-measurable lever must be structural. HGB probe: 0.5–3.6 s
  per unhcr item ⇒ per-item boosting would risk the 900 s budget anyway.
- **E010 (conditional gate-agreement softening) implemented and adopted
  (real-data motivated, E003 precedent)**: scalar ã_i → ã_i(v) conditioned
  on ONE data-selected GIVEN column per gated item (held-out Bernoulli LL
  vs scalar baseline; β-shrunk α=20 to the item scalar; degenerates to
  E008 when nothing wins). Evidence triple, all pre-registered: clean
  sandbox ≡ E008 to 4 decimals ✓; group-dependent violation sim (35%/2%
  by column value) **+0.0352 log over scalar** — and the sim's group
  column was the sandbox `wave` item, precisely the column the A002/E003
  domain analysis predicts real unhcr data will select for the 59
  round-2-only multi-select items ✓; uniform-violation sim +0.0000
  (shrinkage no-loss) ✓. Tests 35/35.
- **Submission #5 packaged** (`submissions/2026-09-01-E010/`, zip OK,
  parity exact, ~240 s ≪ 900 s). LB pre-registration: unicef/wb must stay
  flat (their gates are near-exact — any >0.02 move means something
  unintended engaged); unhcr is the entire bet (+0.01–0.03 if the
  wave-heterogeneity thesis holds; flat does NOT falsify — E008's
  logistic soft path may already absorb it; −0.02 ⇒ conditional layer
  overfit ⇒ raise its α or revert).

- **E010 submitted; result: Grand 0.59 — unicef 0.51 / wb 0.49 /
  unhcr 0.77** (E008: 0.51/0.49/0.74). Scorecard 4/4: unicef flat ✓,
  wb flat ✓, unhcr +0.03 at the top of the pre-registered band ✓, Grand
  in band ✓. The wave-heterogeneity thesis is REAL-DATA CONFIRMED — a
  change invisible on the clean sandbox (bit-identical to E008) moved
  the leaderboard on domain evidence alone; the E003-precedent adoption
  path is validated twice now. Strategic readout: unhcr at 0.77 has
  thinning headroom; the widest skill gaps are now wb (0.49, highest U
  2.0184) and unicef (0.51). Next-session queue: (1) wb structural pass
  — its 40 gates / 'Not answered'-heavy GIVEN columns / banded-score
  handling have had NO wb-specific experiment yet (every gain so far was
  generic); (2) unicef 10-country structure (Q01 gated on country,
  near-deterministic gating already handled — look at the 4 non-GIVEN
  gate parents); (3) revisit E009's per-item idea only after a real-data
  diagnostic justifies it.

## 2026-08-29 — E006 hierarchical backoff; submission #3 packaged

- **E006 (MRP-lite ladder) implemented and adopted**: greedy forward
  selection of ≤ 3 GIVEN columns, per-level κ, each level's prior = level
  above (p_L = (count + κ_L·p_{L-1})/(n + κ_L)); E003 softening and gate
  recursion unchanged. Runner: 3-inst mean 0.4682 → 0.4783 (Δ +0.0101).
  Depth 3 selected on all four schemas with shrinking gains and rising κ —
  the MRP empty-cell prediction measured (pre-registered watch point).
  Selection vectorized (groupby + κ batching + prefix caching): unhcr
  selection 75 s, total ~95 s.
- **Submission #3 packaged** (`submissions/2026-08-29-E006/`, zip OK,
  score.py PASS 0.48/0.42/0.54, 23/23 tests). LB expectations
  pre-registered in SCORES.md (modest gain; unicef largest; flat result
  not falsifying at ±0.01–0.02 noise; >0.02 drop ⇒ greedy instability
  diagnostic).
- Next in queue: eRPIS published-marginal priors as bundled CSV (A001
  transcriptions), T1 temperature scaling as calibration guard, A001 v3
  (unicef exact source study with the named 10-country list).
- **A003 done (same day): eRPIS Sep-2025 tables → `data/priors/erpis_2025.csv`**
  (49 rows, basis-tagged verbatim/derived/mapped-medium, mapped onto real
  item names; intention chain s3_11→s3_12→s3_13 matches published
  conditionals 1:1 including gate directions). Flash Jan-2025 excluded
  (wrong time point per A002 finding 1). Feeds E007.
- **E006 submitted; result: Grand 0.55 — unicef 0.50 / wb 0.48 /
  unhcr 0.66** (E005: 0.49/0.48/0.63). Pre-registration scorecard:
  across-board gain ✓, no >0.02 drops ✓, wb flat (explicitly allowed).
  One miss: unhcr gained most (+0.03, above noise), not unicef —
  consistent with country_asylum/wave entering the real-data ladder
  (the A001/A002 domain prediction); sandbox magnitude ordering again
  didn't transfer. unhcr remains the paying vein → E007 (eRPIS prior
  blend) is the right next spend.

## 2026-08-28 — E003/E004/E005 implemented; submission #2 packaged

- **E004 (stratum backoff) implemented and adopted**: data-driven stratum
  selection (GIVEN card ≤ 12; best single by 20%-holdout log score, then
  best pair; κ ∈ {1,3,10,30,100} joint) — deviation from the T3
  smallest-cardinality rule, justified by A002 finding 5 (wb country only
  38.8% recorded). Runner: mean 0.3412 → 0.4595, **unhcr moved for the
  first time** (0.4297 → 0.5347) — gate cascade over 155 PREDICT parents
  confirmed as the multiplier E001/E002 predicted. 3-inst Δ +0.1202.
- **E003 (soft gating) implemented and adopted (real-data motivated)**:
  ã_i beta-binomial-shrunk gate agreement (α=20 fixed — untunable locally),
  pred = ã·hard + (1−ã)·marginal. Clean sandbox bit-identical to E002
  (pre-registered: sandbox gates exact). Violation sim (17% flipped):
  unhcr +0.0289 log over hard; on stratum tables +0.0422 log — insurance
  grows exactly when E004 activates the cascade.
- **E005 = E003∘E004 composed, adopted, packaged as submission #2**
  (`submissions/2026-08-28-E005/`, self-contained main.py, zip OK,
  score.py PASS ×3, ~101 s total, 19/19 tests). Clean sandbox ≡ E004.
  LB expectations pre-registered in SCORES.md (unhcr largest gain; unhcr
  below 0.41 ⇒ softening insufficient → raise α / cap ã on the 59
  round-2-only multi-select items).
- Process note: Domain check sections pre-registered in E003/E004 BEFORE
  implementation (first full use of rule 7 + A-series flow: A001 → A002 →
  experiment design).
- **Submitted; result: Grand Prize 0.53 — unicef 0.49 / wb 0.48 /
  unhcr 0.63** (E002 was 0.43 — 0.45/0.43/0.41). All three pre-registered
  expectations hit: every instrument up, unhcr largest (+0.22, the
  country×wave + cascade fingerprint), no softening-failure signal.
  unhcr's real gain (+0.22) doubles the sandbox prediction (+0.105):
  real GIVEN-answer coupling is stronger than the sandbox trait — supports
  investing next in richer conditioning (hierarchical backoff T4) and the
  eRPIS published-marginal priors (A001) rather than exotic models.

## 2026-08-27 — first submission packaged (E002)

- **Submission #1 packaged: `submissions/2026-08-27-E002/`** (exact copy of
  `src/models/gated_marginal.py` as `main.py`, no requirements.txt). Zip passes
  `check_submission_zip.py`; official `score.py` PASS on all three real schemas
  (unicef 0.3200 / wb 0.2900 / unhcr 0.4300 noised, ~15 s total ≪ 900 s).
  Runner exact skills reproduce the 08-19 numbers bit-for-bit (mean 0.3412 incl
  sample, 0.3479 excl) — no drift since the kit update.
- Purpose: pipeline validation + first REAL-data baseline; sandbox skills are
  not LB predictions (see SCORES.md for qualitative expectations). Reported LB
  triple becomes the reference for all future local-vs-LB gap tracking.
- Submission cadence decided: submit only changes that clear +0.005 locally;
  E004 (stratum backoff) next but **never alone** — must ship together with
  E003 soft gating, since predictable unhcr parents + hard coupling + approximate
  gates (agreement 0.29–0.98) = invisible-on-sandbox log(1e-3) risk.
- Still open: GATE_CORRECTIONS.md forum question not yet posted.
- **Process discipline upgrades (user-driven, same day):** rule 7 added to
  CLAUDE.md — every empirical conclusion validated against BACKGROUND domain
  (vs technical domain); domain surprise raises the evidence bar (artifact
  check + replication) but never auto-rejects — survivors are adopted and
  logged as potential discoveries. Experiment TEMPLATE gains a pre-registered
  "Domain check" section. New A-series (`docs/analysis/A0XX`) records every
  analysis attempt/method/version append-only, dead ends included, so the
  full process is reconstructible for the method description and talks.
- **A001 (background domain packet) v1 done** — delegated primary-source
  research, findings in `docs/analysis/A001-sources/findings.md`. Headlines:
  unhcr = real eRPIS (wave 1 = exactly 6,316 CATI, May–Jul 2025; real design
  is a PANEL, competition flattens to cross-sections); **the Assad-fall
  return-intention discontinuity (1.7%→27%) predates the competition window —
  between-round movement is a decay (Jordan 40%→22%), not a jump** — a wrong
  jump-prior averted purely by domain check; per-country marginals for the
  gated Q1→Q2→Q3 chain transcribed from PDFs (no microdata exists); unicef ≈
  WGM 2018 item content (free CC-BY microdata = best machine-readable prior;
  importance>effectiveness>safety ordering universal); world_bank = STEP-shaped
  composite, digit-span/Corsi from impact-evaluation batteries (Laajaj &
  Macours), country triple unverifiable. 15 pre-registrable expectations
  catalogued → A002 EDA lens + E004 Domain check.
- **A002 (schema EDA) v1–v3 done** — `docs/analysis/A002-schema-eda.md`,
  report in `A002-outputs/`. Headlines: (1) **both unhcr rounds sit inside
  the single May–June 2025 eRPIS wave-1 window** (round 2 ≠ Oct–Nov wave 2)
  → A001's between-round-decay expectation WITHDRAWN, replaced with
  "rounds near-identical; eRPIS Sept-2025 tables are direct priors for
  both"; (2) s3_11 = eRPIS Q1 verbatim, ungated root with 73 direct
  children, 155/156 unhcr gate parents PREDICT → E004's target is
  literally "predict s3_11 per country×wave"; (3) unicef gating nearly
  deterministic (6/8 GIVEN parents) — explains its LB lead; COVID-era
  faith survey, 10 countries named, WGM demoted to wording ancestor;
  (4) wb country recorded for only 38.8% → stratum = employmentStatus /
  RCT arm / hadJob, NOT country; full psychometric battery as banded
  scores, EXCLUDE = raw duplicates (leak prevention); (5) sandbox gates
  verified EXACT (0 violations / 2.57M pairs) — unhcr approximate-gate
  risk invisible locally, E003 violation sim is the only probe;
  (6) U: unicef 1.5620 / wb 2.0184 / unhcr 1.2618 — unhcr cheapest-U +
  132k cells + 144 binaries = calibration leverage concentrated there.
- **Submitted; result same day: Grand Prize 0.43 — unicef 0.45 / wb 0.43 /
  unhcr 0.41.** Pipeline validated end-to-end on the hosted stack. Readings:
  (1) unhcr 0.41 is the real-data crowd-marginal skill itself (E002 ≡ marginal
  there) — largest instrument sits fully unconditioned, biggest headroom;
  (2) real-data skills ≫ sandbox skills (real marginals much sharper than
  invented ones) — sandbox-vs-LB comparisons are meaningless, gap tracking is
  LB-vs-LB from here; (3) all numbers ±0.01–0.02 (Laplace ε=10, rounded).

## 2026-08-21 — trip pack (4 days away)

- Built `trip/` pack for a 4-day trip: `trip/README.ko.md` (day plan: AM paper via `/paper-session`, PM implementation), `trip/tasks/T1–T4` (temperature scaling, E003 soft gating, E004 stratum backoff, hierarchical backoff / first-submission prep), skeleton experiment files E003/E004 (status parked, hypotheses fixed), open-access PDFs under `trip/papers/` (gitignored, zip only). Zip includes the working copy with `.git` and `external/starter-kit/` (+ sandboxes) so the runner works offline after `pip install -r requirements.txt`.
- Nothing measured today; expectations written into E003/E004 Decision sections before any code exists.

## 2026-08-19 — Codabench live, registered; kit update audit

- **Codabench competition 17822 is live; user registered (auto-approve).** Leaderboard columns: Grand Prize + per-instrument skills. Phase config: Dev to Oct 31 / 1 per day, Test Nov 1–14 / 1 total. Site says launch Aug 18, dev ends Oct 30 → treat Oct 30 as deadline. New site item: "Roots of the Data Prize" (teams based in the 14 data-collection countries).
- **Kit: 8 new commits pulled.** The big ones:
  - **Submission cap removed** — `max_submissions_per_participant: 20` deleted from config.yml; 1/day is the only limit (~70+ possible submissions). Discipline unchanged: local harness decides, leaderboard validates.
  - **`FINAL` → `TEST` rename; split now exact counts** (`n_train/n_dev/n_test`), roles assigned deterministically, **`data_fraction` removed** — phase 1 shows ALL TRAIN rows. Exact phase-1 scored cells: unicef 17,856 / wb 39,520 / unhcr 132,273. `sample_rows` signature changed again → runner.py updated, sandboxes regenerated, 11 tests pass.
  - **Real instrument metadata published in schema descriptions**: unicef v1.1 = Faith & Immunisation, 10 named countries, Q01 gated on country; unhcr v1.3 = Syrian refugees in Egypt/Iraq/Jordan/Lebanon, 2 CATI rounds (6,316+4,033) as independent cross-sections; wb = youth job-seekers, 3 countries. Gated counts: unicef 8, wb 19→40, unhcr 143→156.
  - **unhcr gates are approximate on real data** (agreement median 0.83, range 0.29–0.98; s3_11 branches overlap; 59 multi-select items sentinel-marked in round 2 only; `GATE_CORRECTIONS.md` referenced but missing from kit → forum question). Hard gate coupling unsafe on unhcr; sandbox can't show it. E002 caveat recorded; softened gating is the successor experiment.
- **Re-measured on updated kit** (seed 0, exact): marginal mean 0.2877; gated_marginal 0.3412 (Δ +0.0535; unicef +0.161, wb +0.052, unhcr +0.001). E001/E002 files updated.
- Minor: Codabench API reports docker python:3.12-slim vs kit 3.13-slim — flagged in notes, likely stale platform field.
- Next: E003 = soft/agreement-weighted gate coupling design (needs a way to estimate per-item gate agreement from visible rows); first leaderboard submission once E002 zip passes check_submission_zip + all three schemas.
- **Domain-study update (same day, later):** [[domain]] §9 added for the substantive (not just factual) shifts: (1) gates as estimated structure — empirical-Bayes agreement weighting as the E003 design note; (2) **UNHCR instrument identified as Enhanced RPIS** — the published RPIS series (rounds since 2017, 9th 2024, flash Feb 2025, ERPIS report Sept 2025 with matching fieldwork window) gives partner-published aggregate marginals for near-identical items = strongest offline prior for the largest instrument; must be disclosed as external data (FAQ 8); (3) `wave` is GIVEN → round-confounded sentinel rates are directly conditionable; (4) cap removal recalibrates the reusable-holdout budget note (~70 queries, noise floor binds). UNICEF exact source study and World Bank countries still to identify. Reading order extended (items 16–17).
- **Full repo re-audit against the 08-19 kit as standard (same day, later):** verified gate format uniform across all four schemas ({parent, observed_if}, single string parent, parents always precede children — gated_marginal structurally compatible); kit `score()` metric unchanged (skill formula identical; new `item_normalized`/`brier` outputs are diagnostics only); baselines and runtime section untouched by the kit update; `check_submission_zip` smoke schema moved to count-splits (no contract change). Fixed stale internals on our side: submissions/README (20-cap), E001 (08-19 numbers row), logloss.py verification note, domain.md (61k×150 briefing-era scale, "Rule 9/declared before phase 2" → models.txt/FAQ disclosure), method-4p.md ("Rule 7" numbering, hard-gate wording → softened-gate wording, unverified license claim → verify-against-terms). Official grader re-cross-checked on the updated kit: sample `PASS 0.3200` vs harness exact 0.3210 (noise-consistent). 11 tests pass. SIMULACRABENCH.md left as-is (historical briefing, marked outdated).

## 2026-08-17 — public launch, kit migration

- **Competition launched.** Old URLs dead (situatedevals.org/simulacrabench, `SituatedEvals/notebooks` both 404). New: site **simulacrabench.org**, kit repo **SituatedEvals/public**, leaderboard **codabench.org/competitions/17822**, contact **team@simulacrabench.org**. Cloned the new kit to `external/starter-kit/`; draft archived at `external/starter-kit-notebooks-archived/`.
- **Full diff draft → launch kit.** Structural change: no more `train/test.parquet` — one `respondents.parquet` with `role` ∈ TRAIN/DEV/FINAL assigned at build; phase 1 scores DEV, phase 2 scores FINAL with DEV turned visible; FINAL rows not shipped in phase 1. `load_frames`/`sample_rows` signatures changed accordingly.
- **Fact corrections vs our notes (CLAUDE.md + starter-kit-notes updated):**
  - Wall-clock budget is for the **whole run, all three instruments together** (900 s / 3600 s) — not per instrument.
  - Runtime: +8 CPUs, Python 3.13, `requirements.txt` now optional (large pre-install list incl. torch, transformers, and organizer lib `torch_measure`); HF models via `models.txt` fetched at image build.
  - Schemas: world_bank now 106 items/76 scored (was 82/73, cognitive items re-classed, numeric options now strings); unhcr 285/213/143 gated; sample rebuilt (12,000 rows, 11 items). Splits now train/dev/final fractions.
  - Submission cap 20 confirmed; phase 1 ends **Oct 30** (site); zip ≤ 1 GB; failures return sanitized `HSCC-*` codes only.
  - Sandbox `trait_scale` 0.6 → **2.0**: conditional models are now testable locally. All draft-era reference scores obsolete.
- New kit pieces: `FAQ.md`, `tools/check_submission_zip.py` (mirrors hosted ingestion), baselines `bundled_artifact` (bundled-CSV prior) and `external_model` (LLM prior + gate recursion + Dirichlet backoff; organizers warn it cannot beat marginal on the sandbox by construction), 6-language tutorials.
- **Harness re-verified on launch kit** (`runner.py` updated to the role API; 11 tests pass). Exact skills, seed 0, phase 1: marginal 0.3198/0.1486/0.2469/0.2988 (mean 0.2535); gated_marginal 0.3198/0.3267/0.2568/0.2988 (mean **0.3005**). Official `score.py` on sample: `PASS 0.3200 (27 s)` — matches. Gate-gain pattern shifted with the new sandbox: unicef +0.178, world_bank +0.010, sample/unhcr ±0 (parents PREDICT → falls back to marginal, consistent with the 08-12 structural conclusion).
- Next: register on Codabench (user action — site may go live with the Aug 17 UTC day), then first leaderboard submission = gated_marginal as pipeline validation candidate; start GIVEN-conditioning to unlock unhcr's 143 gates.
- **Workflow decided (same day, later):** experiment-tree recording adopted — one file per experiment in `docs/experiments/` with `parent:`/`status:` headers forming the tree, IDs in commit messages, fixed +0.005 adoption threshold, `scripts/render_tree.py` → `docs/tree.md` (mermaid). E001 (kit marginal, root) and E002 (gated marginal, +0.047, adopted) written retroactively. Daily push to private GitHub repo (`joon56/Simulacrabench-NeurIPS-2026-`).
- **Cleanup + domain refresh (same day, later):** deleted the archived pre-launch clone (`external/starter-kit-notebooks-archived/` — differences fully recorded in starter-kit-notes and this log). Added [[domain]] §8, the areas the launch kit made load-bearing: (1) prediction-powered inference — tutorial part 2 builds the PPI estimator explicitly, GIVEN block reframed as sampling-frame variables; (2) reusable-holdout/Ladder theory for the noised fixed-DEV leaderboard → submission-spending policy; (3) cognitive-test norm priors (Woods 2011 digit span, Kessels 2000 Corsi) for world_bank's re-classed raw-span items — real-world priors the sandbox cannot measure; (4) the `external_model` LLM-prior + Dirichlet-backoff recipe as the sanctioned LLM pattern (base measure worth ALPHA pseudo-respondents, not persona simulation); (5) `torch_measure` = Stanford AIMS PyTorch IRT lib (Rasch/2PL/3PL, GPU) pre-installed in the image — public docs suggest binary-only, verify polytomous support before designing around it.

## 2026-08-12

- **Experiment runner** (`src/eval/runner.py`): scores any `predict(frame, schema)` in-process with the kit's own modules — exact un-noised skill + wall-clock, all four schemas. Kit marginal baseline reproduces the noised scores exactly (0.1902/0.2468/0.3208).
- **Metric noise baseline** (10 phase-sampling seeds, crowd marginal): per-instrument skill std 0.002–0.004; 3-instrument-mean std **0.0016**. Decision rule: an improvement is real only if > +0.005 on the 3-instrument mean (~3σ). `sample` is ±0.06 (144 cells) — debugging only, never for judging.
- **Gate-aware marginal** (`src/models/gated_marginal.py`): per respondent, P(child=NA_GATED) = 1 − P(parent ∈ observed_if) using the respondent's own parent belief (one-hot if visible, predicted otherwise); substantive mass = P(asked) × asked-only conditional. Chain closure automatic (NA never in observed_if).
- Results vs plain marginal (seed 0, phase 1, exact skill):

  | Schema | marginal | gated | Δ | why |
  |---|---|---|---|---|
  | unicef | 0.1902 | 0.3653 | **+0.1751** | 5/7 gates have GIVEN parents → deterministic for test rows |
  | world_bank | 0.2468 | 0.2516 | +0.0048 (~3σ, borderline) | only 6/19 gates on GIVEN parents |
  | unhcr | 0.3208 | 0.3208 | +0.0000 | all 143 gates on PREDICT parents → parent belief falls back to crowd → algebraically identical to marginal |
  | 3-inst mean | 0.2526 | 0.3126 | **+0.0600** | |

- **Structural conclusion:** gate coupling is a *multiplier on parent predictability*. unhcr's 143 gates yield nothing until a model predicts parents respondent-specifically — which is exactly what GIVEN-conditioning (MRP-lite) and latent-factor models add. Their value estimates should include the unlocked gate cascade, not just their direct item gains.
- Caveat: sandbox gains transfer qualitatively (the gate mechanism is identical on real data), magnitudes don't (invented marginals; unicef's +0.175 depends on how often invented parents fall outside observed_if).

## 2026-08-11 (later)

- **Launch postponed to Aug 17** (website commit 2026-08-11 04:12 UTC, "Update launch date to August 17, 2026"; timeline heading changed "Eight months" → "Four months"). Registration opens with launch — no registration or leaderboard submission possible until then.
- Starter kit repo still public and unchanged (last push 8/10) — our clone is a pre-launch draft. All facts derived from it (skill metric, floor, 900/3600 s, submission caps, schemas) must be re-verified against the kit on Aug 17.
- Draft inconsistencies visible in kit commit history: rules v0.8 "92 submissions" vs config.yml cap 20; contact address mismatch; tutorial commit still uses "Track B" wording the README dropped.
- Tutorial commit (8/5) leaks a useful signal: in the kit's own experiments, **skip-logic handling was the single largest gain (M1 0.98 → M2 0.76 log score), more than any modelling step** — confirms the strategy priority; and naive Bayes underperforms because one latent trait per respondent makes answers conditionally dependent (double-counting evidence).

## 2026-08-11

- **Competition launched.** Starter kit found: <https://github.com/SituatedEvals/notebooks>, cloned at `external/starter-kit/` (gitignored). Official name: Humanitarian Survey Completion Competition (HSCC). Leaderboard/rules/registration on Codabench (org 4076).
- Pipeline verified end-to-end on all four schemas with the official grader (`score.py`, marginal_counts baseline, phase 1, noised skill scores): sample PASS 0.45, unicef PASS 0.19, world_bank PASS 0.25, unhcr PASS 0.32. Run times ~25 s each, far under the 900 s limit.
- Major corrections vs the original briefing (CLAUDE.md updated accordingly):
  - No Track A/B. Single task: held-out respondents, `GIVEN` visible, all `PREDICT` cells scored.
  - Leaderboard metric is **skill** = 1 + log_score/U (0 = uniform, 1 = perfect), plain mean over three instruments; log score pooled over cells.
  - Grader floors vectors by mixing with flat vector, floor 1e-3 — no self-flooring needed.
  - Compute: 1× **H100**, 16 GB RAM; **900 s/instrument (phase 1)**, 3600 s (phase 2) — not A100 10/100 min.
  - Phase-1 scores noised (Laplace ε=10, rounded 0.01); **max 20 submissions total** per participant on top of 1/day.
  - Gated items: extra final option slot for sentinel `NA_GATED`; predicting who gets skipped scores like any answer.
- Local harness updated to mirror official metric exactly (`floor_mix`, `uniform_reference`, `skill` in `src/eval/logloss.py`); pooling-over-cells assumption confirmed against `score.py`. 10 tests pass.
- Next: register (Google Form + Codabench, user action), first leaderboard submission with marginal baseline to validate the official pipeline, then start on structure-aware models (respondent-trait / low-rank on GIVEN block).

## 2026-08-09

- Repo scaffolded per SIMULACRABENCH.md §8, git initialized, CLAUDE.md added.
- Official site checked (situatedevals.org/simulacrabench + GitHub org `SituatedEvals`): starter kit NOT published yet — launch is 2026-08-10. Only `website` repo exists; page source has no kit links. **TODO tomorrow: register (Google Form), clone starter kit, verify submission pipeline end-to-end on official synthetic sandbox, replace provisional sandbox.**
- Built local log-loss harness (`src/eval/`): mean log-loss pooled over masked cells (assumption — verify pooling vs per-item averaging against official kit), Track A (MCAR cell mask) and Track B (respondent holdout, demographics visible) splitters, provisional synthetic sandbox with all announced item types incl. skip-logic "not shown" level, per-item marginal baseline. 8 tests pass.
- Baseline numbers on provisional synthetic sandbox (n=5000, seed=42, 20% mask):

  | Model | Track A | Track B |
  |---|---|---|
  | uniform | 1.1206 | 1.1537 |
  | marginal (Laplace α=1) | 1.0856 | 1.0987 |
