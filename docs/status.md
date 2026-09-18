# STATUS — read this first in a new session (kept current at every commit)

Updated: continuation of the 2026-09-21 handoff. The audit environment reports
2026-09-18; see `docs/phase2-preparation.md` for provenance. Newest work is
inserted at the TOP of docs/log.md; historical dated entries are newest-first.

## Where we are

- Leaderboard best: **E025 — Grand 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.89)**,
  `submissions/2026-09-09-E025/`, unchanged since 2026-09-09. Field above us:
  latest user-provided screenshot shows three leading rows at
  **0.52 / 0.50 / 0.93 (Grand 0.65)** and three more at
  0.52 / 0.49 / 0.93. Displayed gap: WB +0.01, UNHCR +0.04.
  Screenshot date/team identities are not visible; no new submission by us.
- Adopted stack (all in `src/models/`, assembled self-contained per submission):
  hier_backoff ladder (E006) → E010 conditional gate agreement → shared_trunk
  net (E012, GPU with CPU fallback) → dup_link/hh_sharp household evidence
  layer (E018/E022: full visible pool, Fellegi–Sunter weights, softmax
  posterior, replay-calibrated λ with concentration buckets) → hh_cap
  per-instrument config {64×2, 128×2+do} (E025).
- **User priority: improve DEV rank.** A006 reopens validation auditing:
  E040 compares an out-of-sample tree with an in-sample refitted net, and
  tuning/deployment mixture formulas differ. Historical flat scores remain;
  the claim that all real-data base-model headroom is exhausted is withdrawn.
  E025 stays incumbent; no improvement from these findings is measured yet.
  Phase-2 fallback is prepared. `docs/method-4p.md` renders to four verified
  pages in `output/pdf/method-4p.pdf`; runbook: `docs/phase2-preparation.md`.
- **Latest objective: win, with new methods allowed.** A008 proposes supervised
  section-specific retrieval as the main research hypothesis and an independent
  pretrained tabular base as a challenger. Neither is implemented or scored.
  Grand .65 is not a guarantee of first place; H .94-.96 is a target scenario,
  not a forecast. A007's repairs remain validation infrastructure.
- **WB is a secondary research target, not a demonstrated ceiling at .49.**
  Screen the independent tabular base on WB locally as well. With controls
  .52/.50, H .95 gives mean .6567 (about Grand .66); with WB .49 it needs
  H .96. These are arithmetic scenarios, not forecasts or guaranteed ranks.
  Keep initial hosted tests UNHCR-only under the standing attribution rule.

## Real-data loss map (probe submissions E032–E034, unhcr)

- unhcr 0.89 = base model 0.79 + evidence layer +0.10.
- Per-cell skill: gated items 0.892, content items 0.885 (on unicef/wb, where
  gates are exact, gated cells are ~2× easier — on unhcr they are not).
- Sentinel knowledge alone leaves gated cells at 0.56 ⇒ most gated skill is
  content prediction on asked cells.
- Remaining loss 0.110 = 0.079 gated + 0.031 content.
- Arithmetic and tooling: `src/models/probes.py`, `tests/test_probes.py`.
  Probes read model-component contributions only, never a dataset statistic.

## What has tested null (respect the scope; see A006)

Local results (not universal real-data ceilings): base model at the
sandbox Bayes ceiling (A005, `src/eval/oracle.py`,
+0.0024); signature recall / ordinal adjacency (E030, +0.0025); evidence
transition tables (E035, +0.0032); sentinel recalibration (E037, negative
cross-fitted); λ/K matching refinements (E023); net variance (E029, +0.0004).

Flat real-data A/Bs (six recorded; limited resolution and scope):
E027 evidence-as-net-input, E028 parent-value gate decoding,
E031b replay cap lift, E036 relation-split λ, E038 identifier signature,
E040 tree blend. Also closed earlier: priors (E007), per-item tuning (E009),
ordinal smoothing (E011), cross-round linkage (E013/E014), capacity beyond
128×2 (E026).

A006/A007: E040 has validation defects and fits trees for 57 ungated heads,
whose beliefs can propagate to 155 gated descendants. E023
tested K/weight iterations, not out-of-sample evidence calibration. E037's
cross-fitted isotonic null is not a bound on every calibrator. Do not repeat
unchanged experiments; first repair the evidence behind their interpretation.

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

1. **Winning-strategy research is the main line.** Follow
   `docs/analysis/A008-winning-strategy-hypotheses.md`: establish a non-injected
   screening channel and scoped retrieval oracle before building a supervised
   matcher; independently screen a pretrained tabular base within runtime.
   No new score claim or ready submission. Preserve validation requirements in
   `docs/analysis/A007-submission-history-and-dev-plan.md` (all 24 submission
   scorecards and full log reviewed). Its E041/E042 IDs remain provisional and
   unimplemented; register actual experiments only when execution begins.
   Separate selection/evaluation, all packaging checks, UNHCR only, no
   automatic daily upload. E025 remains the measured fallback.
2. **Keep the phase-2 fallback ready.** The file is
   `submissions/2026-09-09-E025/main.py` (hardened: `score.py --phase 2`
   PASS ×3 = 0.4902 / 0.4620 / 0.5652, 291 s local CPU, worst case no-GPU
   ≈ 1,000–1,200 s ≪ 3,600 s, smoke frame OK, 8 clean hosted runs). In the
   window: re-zip from the snapshot, repeat the three required checks,
   submit once, attach the method. API dates: Nov 1 00:00 UTC through
   **Nov 14 00:00 UTC (09:00 KST)**; plan upload by Nov 13. Preparation
   readings: `submissions/phase2-E025-preparation/SCORES.md`. Fresh local
   rehearsal: ZIP OK, official phase-2 PASS x3 (same scores, 310.0 s),
   src parity exact x3 (268.1 s); hashes/results in adjacent `verification.json`.
3. **Method complete; keep it synchronized.** Four rendered pages, corrected
   agreement prior and replay limitations, six flat A/Bs, probe precision and
   oracle. Codabench terms §7 checked: method required for every Test entry;
   top three provide research-reproduction-licensed source at award stage.
   Choose our release license before that delivery; no new license applied.
4. **No unverified phase-1 submission.** Resume only if (a) the kit ships pending
   gating changes — then `git fetch`, re-run runner + score.py, resubmit the
   E025 zip; or (b) a genuinely new hypothesis appears with a named mechanism
   AND a channel that is not an assumed-structure sim. Six flat A/Bs say the
   prior on blind refinements is low. A006 supplies a concrete independent
   correctness channel for auditing failed selection, not proof of score gain.
5. Weekly: kit update check, leaderboard intel (who moved, by how much).
   Continuation fetch: HEAD = origin/main = ee427a9; no gating update.
   Public leaderboard snapshot: six entries at unhcr 0.93 / Grand 0.65
   (two share a team name); unicef 0.52, wb 0.49–0.50. No new mechanism.
