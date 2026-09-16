# STATUS — read this first in a new session (kept current at every commit)

Updated: 2026-09-19. Newest log entries are inserted ABOVE the previous
newest header inside docs/log.md (not appended at the end) — search the
latest date.

## Where we are

- Leaderboard best: **E025 — Grand 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.89)**,
  `submissions/2026-09-09-E025/`. #17 E031 (cap lift + ensemble) FAILED without
  an HSCC code; #18 E031b (cap lift only) flat at 0.63 — cap lift null on real
  data, ensemble unread. E025 stays the model of record.
- Adopted stack (all in `src/models/`, assembled self-contained per submission by
  the script pattern in the E022+ sessions): hier_backoff ladder (E006) → E010
  conditional gate agreement → shared_trunk net (E012, GPU with CPU fallback) →
  dup_link/hh_sharp household evidence layer (E018/E022: full visible pool,
  Fellegi–Sunter weights, softmax posterior, replay-calibrated λ with
  concentration buckets) → hh_cap per-instrument config {64×2, 128×2+do} (E025).
- Instruments: clean sandbox runner (`src/eval/runner.py`, no household
  structure, blind to capacity; `phase=2` works as-is — E025 phase-2
  profile 0.4902/0.4620/0.5652, 254 s local CPU); **sandbox oracle**
  (`src/eval/oracle.py`, A005): Bayes ceiling for GIVEN-only models is
  +0.0024 above E025's base — base-model changes cannot be validated
  locally; only the evidence layer has local headroom (household sim); **household sim** (`tests/test_hh_sharp.py::
  hh_inject_rho`, ρ∈[0.2,0.8]) — quantitatively validated against E018/E019/E022
  leaderboard readings; branch-overlap sim (`tests/test_pvc_gate.py`).
- Closed axes (do not re-spend): priors (E007), per-item tuning (E009), ordinal
  smoothing (E011), seed-bagging of selection, cross-round linkage (E013/E014),
  matching K / 2nd EM iteration (E023), capacity beyond 128×2 (E026),
  evidence-as-net-input (E020/E024/E027), parent-value gate decoding (E028),
  net seed ensemble / output temperature (E029: +0.0004, T=1 everywhere —
  ride-along candidate for a phase-2 stack only), ordinal near-agreement in
  the signature (E030: drift sim +0.0013, ceiling +0.0025 — matching recall
  closed).

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
- A FAILED submission does not consume the 1/day slot (E031 → E031b same day).
  Codabench's ? button normally carries the HSCC block; E031 showed none —
  memory ruled out locally (peak RSS 2.4 GB), cause undetermined.

## Next session plan

1. **Record E038's reading** (`submissions/2026-09-19-E038/SCORES.md`):
   ≥ 0.64 ⇒ identifier structure real — retune MIN_AGREE / BLOCKS, add
   the E029 ensemble ride-along, write the disclosure paragraph; 0.63 ⇒
   park; ≤ 0.62 ⇒ raise MIN_AGREE, drop block columns, retest.
2. Dev-rank programme (user decision 2026-09-18: keep working the rank):
   real-data A/Bs one per slot, each with exact local no-regression and a
   directional sim. Queue after E038: (a) base-model tree blend (sklearn
   HistGradientBoosting per item on unhcr, probability blend with the
   net, w on the holdout; LB-only per A005; CPU-side ≲ 150 s local);
   (b) evidence top-K / posterior temperature retune conditional on E038
   arming (only if E038 reads ≥ 0.64).
3. Phase-2 submission = E025 assembly unless a phase-1 A/B lifts the
   best; then the lifted file after the same hardening (score.py
   --phase 2, worst-case CPU-only timing, smoke frame).
4. Weekly kit / leaderboard check; method-4p trimming.
