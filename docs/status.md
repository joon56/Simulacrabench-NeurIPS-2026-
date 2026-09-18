# STATUS — read this first in a new session (kept current at every commit)

Updated: 2026-09-21. Newest log entries are inserted ABOVE the previous
newest header inside docs/log.md (not appended at the end) — search the
latest date.

## Where we are

- Leaderboard best: **E025 — Grand 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.89)**,
  `submissions/2026-09-09-E025/`, unchanged since 2026-09-09. Field above us:
  a plateau at Grand 0.65 (unhcr 0.93) and 0.64 (unhcr 0.91–0.92), several
  teams each, with identical unicef/wb — unexplained by anything in our map.
- Adopted stack (all in `src/models/`, assembled self-contained per submission):
  hier_backoff ladder (E006) → E010 conditional gate agreement → shared_trunk
  net (E012, GPU with CPU fallback) → dup_link/hh_sharp household evidence
  layer (E018/E022: full visible pool, Fellegi–Sunter weights, softmax
  posterior, replay-calibrated λ with concentration buckets) → hh_cap
  per-instrument config {64×2, 128×2+do} (E025).
- **Phase-1 search is exhausted by our instruments** (see "What is closed").
  Phase-2 file = the E025 assembly, already hardened. Main line now:
  `docs/method-4p.md` and the phase-2 window (Nov 1–14).

## Real-data loss map (probe submissions E032–E034, unhcr)

- unhcr 0.89 = base model 0.79 + evidence layer +0.10.
- Per-cell skill: gated items 0.892, content items 0.885 (on unicef/wb, where
  gates are exact, gated cells are ~2× easier — on unhcr they are not).
- Sentinel knowledge alone leaves gated cells at 0.56 ⇒ most gated skill is
  content prediction on asked cells.
- Remaining loss 0.110 = 0.079 gated + 0.031 content.
- Arithmetic and tooling: `src/models/probes.py`, `tests/test_probes.py`.
  Probes read model-component contributions only, never a dataset statistic.

## What is closed (do not re-spend a session on these)

Local ceilings (measured, cannot clear the +0.005 bar even with oracle
settings): base model at the sandbox Bayes ceiling (A005, `src/eval/oracle.py`,
+0.0024); signature recall / ordinal adjacency (E030, +0.0025); evidence
transition tables (E035, +0.0032); sentinel recalibration (E037, negative
cross-fitted); λ/K matching refinements (E023); net variance (E029, +0.0004).

Flat real-data A/Bs (six consecutive, each locally no-regression and
sim-supported): E027 evidence-as-net-input, E028 parent-value gate decoding,
E031b replay cap lift, E036 relation-split λ, E038 identifier signature,
E040 tree blend. Also closed earlier: priors (E007), per-item tuning (E009),
ordinal smoothing (E011), cross-round linkage (E013/E014), capacity beyond
128×2 (E026).

## Standing rules learned the hard way

- Hosted worker speed varies day to day; ~240 s local CPU has timed out. Net
  training runs on the worker's H100 (confirmed E025–E028), so CPU-side work
  should stay ≲ 150 s local; training count is free.
- Phase-1 leaderboard shows **Grand only** unless the best improves. Every probe
  or A/B must therefore touch ONE instrument (unhcr, detected by public schema
  item names) so Δ_unhcr = 3·Δ_Grand; resolution ±0.015–0.03.
- A sim that injects an ASSUMED real-data structure is a directional channel,
  not evidence (E028, E036 both gained on their sims and read flat). Only a
  slot reads real data.
- "Calibration" gains must be cross-fitted before they count (E037: +0.024
  in-sample, −0.004 cross-fitted).
- Organizer rulings (email, Andy, 2026-09-02): within-dataset row matching is
  permitted; "<5 gating changes" to unhcr still unshipped — on any kit update,
  `git fetch` in external/starter-kit, re-run the full harness before submitting.
- Every submission: pre-register readings in SCORES.md, record the actual, commit
  with the experiment ID, push.
- A FAILED submission does not consume the 1/day slot (E031 → E031b same day).
  Second Codabench account exists (user-created, one reading of E032 from it) —
  flagged as a likely terms violation; do not use.

## Next session plan

1. **Phase-2 packaging is the main line.** The file is
   `submissions/2026-09-09-E025/main.py` (hardened: `score.py --phase 2`
   PASS ×3 = 0.4902 / 0.4620 / 0.5652, 291 s local CPU, worst case no-GPU
   ≈ 1,000–1,200 s ≪ 3,600 s, smoke frame OK, 8 clean hosted runs). In the
   window (Nov 1–14): re-zip from the snapshot, `check_submission_zip`,
   submit once, attach the method description.
2. **`docs/method-4p.md`**: trim to 4 rendered pages; license / disclosure
   check against the Codabench terms; keep §5 (phase-2 settings) and §6
   (probe map, oracle) in sync with docs/log.md.
3. **Phase-1 slots: hold.** Resubmit only if (a) the kit ships the pending
   gating changes — then `git fetch`, re-run runner + score.py, resubmit the
   E025 zip; or (b) a genuinely new hypothesis appears with a named mechanism
   AND a channel that is not an assumed-structure sim. Six flat A/Bs say the
   prior on any further refinement of this stack is low.
4. Weekly: kit update check, leaderboard intel (who moved, by how much).
