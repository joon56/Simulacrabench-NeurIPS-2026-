# E065 — WB76 TabICLv2 expert mixture
parent: E041
status: parked
date: 2026-11-08

## Registration (before any run)

Sprint execution of the A045 WB76 contract under [A047](../analysis/A047-sprint/decision.md).
Mechanism: mix the final E041 World Bank distributions with a pretrained
in-context tabular classifier (TabICL 2.2.0 source 0dbff3e, checkpoint
tabicl-classifier-v2-20260212, SHA256 bdc7dbd5...b4ed0) fitted per PREDICT head on
the 9 GIVEN features. UNICEF and UNHCR call a byte-identical copy of the E041
predictor (`e041_core.py` = submissions/2026-09-19-E041/main.py, SHA256 22c91180...3073).
Frozen expert settings are the A045 contract's (n_estimators 8, temperature .9, seed 42, ...).

Variants (one DEV upload each; 3 uploads/day):
- `a25` / `a50`: fixed alpha .25 / .5 on all 76 WB heads; expert context = all
  complete visible WB rows, queries = held-out rows. Direct real-data reading.
- `guard`: A045 guarded procedure — PCG64(4501) split S1000/E1000/F rest, shadow
  E041 and expert on F, alpha in {0,.25,.5} chosen on S, accept only if the E lower
  bound mean(d)-1.645*sd(d)/sqrt(1000) > 0, then all-visible refit.

Deployment: no requirements.txt. Vendored TabICL + einops 0.8.1 first on
sys.path; tqdm 4.67.1 appended as fallback; psutil shim (virtual_memory total/
available from /proc/meminfo) installed only if `import psutil` fails.
Strict DEV builds raise on any expert failure so a fallback cannot hide as a tie.

Local gates before upload: ZIP checker OK; official score.py phase 1 PASS on all
three schemas through the model interpreter; UNICEF/UNHCR raw vectors identical
to E041 run in the same environment; all-instrument runtime measured (< 900 s).
Synthetic WB skill is engineering evidence only.

Hosted reading arms versus E041 ID933094 (.6433/.52/.49/.92):
- Favorable: WB >= .50 and Grand > .6433 with UNICEF .52 / UNHCR .92 unchanged.
- Unresolved: WB .49 and Grand .6433.
- Adverse: WB <= .48 or Grand < .6433 with unchanged controls.
- Mixed: a control value changes; record signs, no attribution to WB alone.
- Technical: Failed status / HSCC code; no effect conclusion.
A favorable fixed-alpha reading makes E065 a Final candidate only after a phase-2
local PASS (3600 s) of the exact package. No automatic TEST selection.

## Results

**Local engineering, 2026-11-08 (synthetic sandbox, official score.py ee427a9, model venv
torch 2.8.0+cu126 on RTX 3070; not efficacy evidence).** ZIP checker OK (a25, a50).
UNICEF 17856 and UNHCR 132273 E065a25 vectors identical to E041 run in the same
environment (changed 0). World Bank exact skill: E041 .454929; a25 .455868 (+.000939);
a50 .456342 (+.001413); guard selected alpha .5 on S (pooled log -1.09621/-1.09470/
-1.09432 for 0/.25/.5), E lower bound +.00130, accepted, output equal to a50.
Wall per instrument (separate processes incl. import): UNICEF 29 s, UNHCR 164 s,
WB a25 172 s / a50 141 s / guard 243 s (E041 55 s, shadow E041 36 s, shadow expert 62 s,
final expert 81 s). All-three estimate well under 900 s. psutil real module used locally.

**Hosted, 2026-11-08.** IDs 1041540 (a25) and 1041542 (a50): Grand .4763960013 / UNICEF
.3499339289 / WB .2335276584 / UNHCR .8457264165; same-scale control E066 ID 1041566 has
the identical WB string. **Arm: Unresolved** for both alphas. Status stays parked; the
guarded procedure remains a Final candidate on its internal real-data check, not on a
DEV reading.
