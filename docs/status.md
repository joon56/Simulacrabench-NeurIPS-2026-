# STATUS — read this first in a new session (kept current at every commit)

Updated: 2026-09-20 E044 result recorded; E041 result reported on 2026-09-19, continuing the supplied
2026-09-21 handoff; see `docs/phase2-preparation.md` for date provenance. Newest work is
inserted at the TOP of docs/log.md; historical dated entries are newest-first.

## Where we are

- Leaderboard best: **E041 — Grand 0.64 (unicef 0.52 / wb 0.49 / unhcr 0.92)**,
  user-reported on 2026-09-19; `submissions/2026-09-19-E041.zip` and matching
  snapshot directory. Previous E025: .63 / .52 / .49 / .89. Displayed gains:
  Grand +.01, UNHCR +.03, controls unchanged. Field above us:
  latest user-provided screenshot shows three leading rows at
  **0.52 / 0.50 / 0.93 (Grand 0.65)** and three more at
  0.52 / 0.49 / 0.93. Displayed gap to that snapshot: WB +0.01, UNHCR +0.01.
  Screenshot date/team identities are not visible; no new leaderboard fetch.
- Adopted stack (all in `src/models/`, assembled self-contained per submission):
  hier_backoff ladder (E006) → E010 conditional gate agreement → shared_trunk
  net (E012, GPU with CPU fallback) → dup_link/hh_sharp household evidence
  layer (E018/E022: full visible pool, Fellegi–Sunter weights, softmax
  posterior, replay-calibrated λ with concentration buckets) → hh_cap
  per-instrument config {64×2, 128×2+do} (E025), then supervised section
  retrieval on UNHCR only (E041, `supervised_retrieval.py`).
- **User priority: improve DEV rank.** A006 reopens validation auditing:
  E040 compares an out-of-sample tree with an in-sample refitted net, and
  tuning/deployment mixture formulas differ. Historical flat scores remain;
  the claim that all real-data base-model headroom is exhausted is withdrawn.
  E041 is now DEV incumbent; the specific E040 audit repairs remain untested.
  Phase-2 fallback is prepared. `docs/method-4p.md` renders to four verified
  pages in `output/pdf/method-4p.pdf`; runbook: `docs/phase2-preparation.md`.
- **E041 adopted as DEV best after a positive hosted reading.** Section-specific
  diagonal retrieval: clean UNHCR -.000486 skill, existing household sim
  -.002026. Observed Adult audit gains +.000595 / +.000427 are inconclusive.
  `submissions/2026-09-19-E041.zip` passes checker, official phase-1 x3 and exact source
  parity (320.6 s CPU total). User-reported hosted .64/.52/.49/.92 selects the
  preregistered .64 positive arm. Local rejection remains historical evidence;
  the new decision follows the hosted best update, not revised local scores.
  E042 final-evidence blend stopped at its oracle: +.004570 log < .005.
  One result does not identify the causal component or exact unnoised gain.
  A008's independent pretrained base remains
  unimplemented; the broader retrieval family is not universally ruled out.
- **WB is a secondary research target, not a demonstrated ceiling at .49.**
  Screen the independent tabular base on WB locally as well. With controls
  .52/.50, H .95 gives mean .6567 (about Grand .66); with WB .49 it needs
  H .96. These are arithmetic scenarios, not forecasts or guaranteed ranks.
  Keep initial hosted tests UNHCR-only under the standing attribution rule.
- **E044 reported Grand .63, no best update; rejected for adoption.**
  Individual instrument scores are unavailable. The preregistered .63 adverse
  arm supports retaining learned weight use, conditional on E041 activation
  and downstream recalibration; no exact hidden UNHCR score is inferred.
  `submissions/2026-09-20-E044.zip` replaces learned weights only in active
  section evidence, retaining E041's learned activation/K32/replay procedure.
  Clean UNHCR delta -.000168 vs E041 / -.000654 vs E025; controls exact;
  household sim +.003090. Checker, official x3 and exact source parity PASS,
  371.022 s local total. E043 candidate-search oracle stopped first: marginal
  mean equivalents +.000963 / -.000392 on observed Adult seeds 41 / 42.
  Neither local model adoption nor a .65 forecast is claimed. E041 stays best.

## Historical E025 loss map (probe submissions E032–E034, unhcr)

These measurements describe E025, not E041. E041's .92 has not been decomposed;
do not automatically relabel the old evidence contribution as .13.

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
  should stay ≲ 150 s local as a historical heuristic. Training is not free:
  profile import, fitting and all instruments against the shared time budget.
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

1. **Retain E041 learned weights after E044's adverse reading.** User reported
   Grand .63 without best update; individual scores are unavailable. Apply the
   preregistered .63 arm: reject E044 for adoption, prioritize honest metric/
   selector validation, and avoid a blind daily removal/weight grid. The
   displayed -.01 Grand gives only an approximate -.03 UNHCR effect translation,
   not a measured instrument delta or hidden score. The experiment is conditional
   on E041's learned activation and includes downstream recalibration. E043's
   new-pool replacement failed its observed-data oracle gate; the larger union
   family was diagnostic only and requires a distinct preregistered experiment.
   **Freeze E041 as the DEV comparison baseline.** The user reported
   .64/.52/.49/.92; preserve the exact ZIP and interpret this as the registered
   positive arm. Next experiments need a named incremental mechanism, a scoped
   oracle and honest selection/evaluation; no blind daily weight grid. Positive
   transfer justifies further study but does not isolate weights, donor bank,
   selector or replay. The old E025 loss map cannot decompose E041.
   Read A008 v5 and E041/E042 results before more work. The observed Adult
   screen's domain/profile limits and negative household sim did not predict
   the hosted gain. An independent pretrained base remains a possible separate
   family, subject to feasibility and oracle screening. Preserve A007 checks.
   Its provisional experiment names were superseded: actual E041 is retrieval,
   actual E042 is the final-evidence blend oracle. New work needs a new ID.
   UNHCR-only initial hosted test, separate selection/evaluation, no automatic
   daily upload. E025 remains the fallback; E041 is the new DEV incumbent.
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
3. **E025 phase-2 method complete; E041 coverage pending.** Four rendered pages, corrected
   agreement prior and replay limitations, six flat A/Bs, probe precision and
   oracle. Codabench terms §7 checked: method required for every Test entry;
   top three provide research-reproduction-licensed source at award stage.
   Choose our release license before that delivery; no new license applied.
   This document/PDF still describes the E025 fallback, not E041. Validate
   E041 on phase 2 and update/render its method before changing that package.
4. **Separate adoption from exploration; retain technical verification.**
   The user's latest direction permits a technically validated, preregistered
   exploratory candidate without a positive local adoption result. This
   supersedes the earlier blanket hold; it does not permit arbitrary changes,
   fabricated gain claims or skipping the three submission checks. Other
   opportunities: (a) the kit ships pending
   gating changes — then `git fetch`, re-run runner + score.py, resubmit the
   E025 zip; or (b) a genuinely new hypothesis appears with a named mechanism
   AND a channel that is not an assumed-structure sim. Six flat A/Bs say the
   prior on blind refinements is low. A006 supplies a concrete independent
   correctness channel for auditing failed selection, not proof of score gain.
5. Weekly: kit update check, leaderboard intel (who moved, by how much).
   Continuation fetch: HEAD = origin/main = ee427a9; no gating update.
   Public leaderboard snapshot: six entries at unhcr 0.93 / Grand 0.65
   (two share a team name); unicef 0.52, wb 0.49–0.50. No new mechanism.
