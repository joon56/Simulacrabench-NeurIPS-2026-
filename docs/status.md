# STATUS — read this first in a new session (kept current at every commit)

Updated: 2026-09-12 (session 2). Newest log entries are inserted ABOVE the previous
newest header inside docs/log.md (not appended at the end) — search the
latest date.

## Where we are

- Leaderboard best: **E025 — Grand 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.89)**,
  `submissions/2026-09-09-E025/`. 12 teams above: 0.65 ×2 (unhcr 0.92+wb 0.50;
  unhcr 0.93), 0.64 ×10 (unhcr 0.90–0.92). unhcr 0.90 alone → Grand 0.64 (joins
  the pack; rank inside it is noise). unicef/wb are at everyone's ceiling.
- Adopted stack (all in `src/models/`, assembled self-contained per submission by
  the script pattern in the E022+ sessions): hier_backoff ladder (E006) → E010
  conditional gate agreement → shared_trunk net (E012, GPU with CPU fallback) →
  dup_link/hh_sharp household evidence layer (E018/E022: full visible pool,
  Fellegi–Sunter weights, softmax posterior, replay-calibrated λ with
  concentration buckets) → hh_cap per-instrument config {64×2, 128×2+do} (E025).
- Instruments: clean sandbox runner (`src/eval/runner.py`, no household
  structure, blind to capacity; `phase=2` works as-is — E025 phase-2
  profile 0.4902/0.4620/0.5652, 254 s local CPU); **household sim** (`tests/test_hh_sharp.py::
  hh_inject_rho`, ρ∈[0.2,0.8]) — quantitatively validated against E018/E019/E022
  leaderboard readings; branch-overlap sim (`tests/test_pvc_gate.py`).
- Closed axes (do not re-spend): priors (E007), per-item tuning (E009), ordinal
  smoothing (E011), seed-bagging of selection, cross-round linkage (E013/E014),
  matching K / 2nd EM iteration (E023), capacity beyond 128×2 (E026),
  evidence-as-net-input (E020/E024/E027), parent-value gate decoding (E028),
  net seed ensemble / output temperature (E029: +0.0004, T=1 everywhere —
  ride-along candidate for a phase-2 stack only).

## Standing rules learned the hard way

- Hosted worker speed varies day to day; ~240 s local CPU has timed out. Net
  training runs on the worker's H100 (confirmed E025–E028), so CPU-side work
  should stay ≲ 150 s local; training count is free.
- Phase-1 leaderboard resolves only ≥ +0.02 unhcr per submission; sim-verified
  +0.005–0.01 refinements must be STACKED into one submission.
- Organizer rulings (email, Andy, 2026-09-02): within-dataset row matching is
  permitted; "<5 gating changes" to unhcr still unshipped — on any kit update,
  `git fetch` in external/starter-kit, re-run the full harness before submitting.
- Every submission: pre-register readings in SCORES.md, record the actual, commit
  with the experiment ID, push.

## Next session plan

1. Phase-2 household sim: extend `hh_inject_rho` so twins land in
   TRAIN/DEV/TEST and score with `phase=2`; measure the CAL_QUERIES cap
   lift (6,000 → all visible) there — the first phase-2-specific number.
2. Signature recall lever (new experiment, parent E025): partial
   agreement weight for adjacent levels of ordinal signature columns
   (age/household-size bands) in the Fellegi–Sunter score — the one
   matching-layer axis E023 did not cover; household sim is the channel,
   > +0.005 log ⇒ stack with the E029 ensemble into one submission.
3. `docs/method-4p.md` is drafted (adopted chain, both phase profiles);
   keep [P2] markers in sync as the final model settles.
4. Phase 2 (Nov 1–14, single submission, no retries): zero-failure
   hardening, final-model selection from the phase-2 runner only.
