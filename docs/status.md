# STATUS — read this first in a new session (kept current at every commit)

Updated: 2026-09-13 (session 2). Newest log entries are inserted ABOVE the previous
newest header inside docs/log.md (not appended at the end) — search the
latest date.

## Where we are

- Leaderboard best: **E025 — Grand 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.89)**,
  `submissions/2026-09-09-E025/`. **Submission #17 = E031** (E025 + replay cap
  lift + E029 ensemble; phase-2 ingredients read on real data, expected flat)
  packaged in `submissions/2026-09-13-E031/` — record the LB result in its
  SCORES.md. 12 teams above: 0.65 ×2 (unhcr 0.92+wb 0.50;
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

## Next session plan

1. Record E031's leaderboard result (SCORES.md + log); if unhcr ≥ 0.90,
   seed count / replay size become phase-2 knobs; if flat, both stay as
   no-risk phase-2 defaults.
2. Phase-2 hardening: run the E031 file under `phase=2` on all three
   sandboxes (runner + score.py --phase 2), check the 3600 s budget with
   CPU-only training as the worst case, smoke-frame guards.
3. Phase-1 slots only for a NEW structural hypothesis with a sim channel
   (E026–E031 refinements all ≤ +0.0013 locally). Candidate: evidence
   transition table (twin answer → learned per-item transition row instead
   of one-hot) — needs a structured-disagreement sim; probe the ceiling
   first (oracle table on the sim) before implementing the estimator.
4. `docs/method-4p.md`: fill [P2] once the final phase-2 model is fixed.
