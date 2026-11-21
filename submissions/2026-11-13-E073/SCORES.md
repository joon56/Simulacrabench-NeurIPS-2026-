# E073 hosted scorecard — preregistered 2026-11-12 (before any E073 upload)

Uploads (replace the never-uploaded E072w / E072h TabICL probes):

| Upload | Path | Content per instrument |
|---|---|---|
| E073n | submissions/2026-11-13-E073n.zip | UNICEF / WB / UNHCR = boosted trees with nearest-row answers alone (nmix100); E041 output unused |
| E073s | submissions/2026-11-13-E073s.zip | per instrument: best chain on S among xstack / xstackc / nstack(c) / gstack(c) over E041, no E test (applied only if it beats the shadow E041 on S) |
| E073b | submissions/2026-11-13-E073b.zip | UNICEF / WB / UNHCR = E041 with GIVEN-only trees mixed into its base (v = .5), E041 evidence layer and rendering unchanged |

Revised 2026-11-12 before any upload: the g-alone diagnostic (E073g) was replaced by E073b so
that every upload can beat E041; tree smoothing 2% -> 0.2%; neighbour ranking by
Fellegi-Sunter weights. E073g stays a reserve build (tmp/e073/).

Identities (2026-11-12, after local validation; ZIPs kept out of git via .git/info/exclude):
- E073n 103065729 bytes, SHA256 97291e63f96af177124733a42905378558dc7268e6a90b2500274183dcd80b9f
- E073s 103065742 bytes, SHA256 0a7791a97ac959f47b87455fa0556f2ae62ef07e5cc29d0d1bdae118399f5f9f
- E073b 103065725 bytes, SHA256 f6af3e608a9af07b3e627ed03b66c7c47ff538374353e47a6a43287567ef8073
Local (synthetic, kit aa03186 scorer, model venv, RTX 3070): ZIP checker OK x3; official phase 1
PASS on all three instruments for each; all vectors valid. Wall (three separate processes):
E073n 330 s, E073s 571 s, E073b 571 s. Synthetic log deltas vs E041 (engineering only; the
sandbox has no neighbour structure and its generator favours the network): E073n -.0147 /
-.0494 / -.0149 (UNICEF / WB / UNHCR); E073b -.0025 / -.0097 / -.0033; E073s 0 / 0 / +.0002
(nothing accepted on UNICEF/WB, gstackc on UNHCR). Plumbing: tree-base weight 0 reproduces
E041 exactly (17856 UNICEF vectors, hook applied once).
Upload window that satisfies either daily-reset convention (UTC or AoE): 2026-11-13 09:00
to 21:00 KST. The last three uploads: 2026-11-14 09:00 to 21:00 KST.

Same-scale E041 controls: UNICEF .3499339289 (old .52), WB .2335276584 (old .49), UNHCR
.8457264165 (old .92; E041 reads .91 = .8264422186 about two times in five, boundary noise).
New-scale values of old-scale bins — UNHCR: .94 = .8843, .93 = .8650, .92 = .8457, .91 = .8264,
.90 = .8071, .88 = .7686, .85 = .7107, .80 = .6143. WB: .51 = .2636, .50 = .2486, .49 = .2335,
.48 = .2185, .47 = .2035, .45 = .1734. UNICEF: .53 = .3635, .52 = .3499, .51 = .3364, .50 = .3228.

Arms (each instrument read separately; these are single noised/rounded readings):
- E073g / E073n at or above the E041 bin on an instrument: that expert alone matches the whole
  E041 stack there -> expect a gain from stacking; give the expert priority in the Final.
- One or two bins below E041: useful complementary model at best; keep guarded stacking.
- UNHCR at or below old .85, WB at or below .46, UNICEF at or below .50: the expert alone is
  far weaker than E041; tabular/neighbour trees do not explain the leaders' edge.
- E073s above the E041 bin: readable gain from S-selected stacking -> Final candidate after a
  phase-2 local PASS. Equal: unresolved. Below (beyond UNHCR boundary noise): S-only selection
  overfits; the Final keeps the E test.
- E073b above the E041 bin on an instrument: E041's base was a bottleneck there -> Final uses a
  guarded choice of the tree weight. Equal: unresolved. Below: trees are a weaker base there.
- Technical: Failed status / HSCC code (not counted; fix and re-upload).
No expectation is stated for the real data: the synthetic sandbox has no neighbour structure
and the trees alone score below E041 there (UNICEF -.015, WB -.045, UNHCR -.016 log).

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-12 22:0x KST user report: E073b Failed (timeout)

E073b (tree base on all three instruments, 5-fold out-of-fold trees) exceeded the 900 s
hosted budget; no score. Failed uploads do not count toward the daily limit. Cause: CPU-bound
tree fitting (289 s locally of the 571 s total) runs about 2-2.6x slower on the hosted worker
(E017/E019 notes); the runtime estimate wrongly assumed hosted ~ local from GPU-heavy uploads.
Accepted uploads after 21:00 KST while three were already made at 08:52 UTC the same UTC day:
the daily counter is not UTC-midnight based (consistent with the AoE day boundary 12:00 UTC).

Replacement E073b2 (registered before upload): tree base v = .5 on UNHCR only, 2-fold
out-of-fold trees, OpenMP capped at 8 threads; UNICEF/WB = E041 exactly (local: 0 changed
vectors). Local wall 334 s (UNHCR trees 74 s); hosted estimate 560-690 s for a 2.3-4x tree
slowdown. submissions/2026-11-13-E073b2.zip, 103065845 bytes (SHA256 on the last line). Arms as
E073b, UNHCR only.
3e8297e4a19a74b191f70564baba8c7937c70cdcb23d55362408440ab9e579c2

### 2026-11-12 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1049629 | 2026-11-13-E073n.zip | 2026-11-12T12:27:32.381171Z | Finished / Dev 29772 | second account (identifiers withheld) | 0.4604439645 | 0.3363908858 | 0.2184987890 | 0.8264422186 |
| 1049646 | 2026-11-13-E073s.zip | 2026-11-12T12:28:11.783720Z | Finished / Dev 29772 | second account (identifiers withheld) | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

Old-scale bins: E073n UNICEF .51 / WB .48 / UNHCR .91 (each one bin below E041's .52 / .49 /
.92; E041's UNHCR itself reads .91 about two times in five). E073s equals E041 on all four.
Arms: E073n "one bin below E041: useful complementary model" on every instrument — an untuned
single neighbour-tree model alone is within about .01 old-scale skill of the whole E041 stack.
E073s **Unresolved** (S-selected per-head stack gained less than one bin).

**Account discrepancy (recorded as supplied):** these two records show the owner and team of a second account (identifiers
withheld), while all earlier sprint uploads show owner `minjoonyoo`, team "Odyssey".
E073s is `on_leaderboard: true` (leaderboard 19827) under that owner. The rules allow three
Development submissions per team per day and one successful Final submission per team; this
project's records treat the earlier second-account use (E032) as a likely Terms violation and
state "use one authorized account". Legitimacy of this account for this team is unverified and
was raised with the user on 2026-11-12. The earlier inference that the daily counter resets at
21:00 KST is withdrawn: it assumed the same account had uploaded.

### 2026-11-12 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1049751 | 2026-11-13-E073b2.zip | 2026-11-12T13:49:30.035771Z | Finished / Dev 29772 | second account (identifiers withheld) | 0.4699679353 | 0.3499339289 | 0.2335276584 | 0.8264422186 |

UNHCR old-scale .91 with unchanged UNICEF/WB (as built: UNHCR only). Arm: **below E041's bin**,
but E041 itself reads .91 about two times in five, so the single reading is weak. It does make
a gain of +.002 or more unlikely (such a model would read .91 with probability about .03 under
the Laplace scale ~.00088): mixing GIVEN-only trees into E041's base at v = .5 gives no
meaningful UNHCR gain. The tree-base route is dropped from the Final (it also costs the most
hosted CPU time). Same account discrepancy as above: uploaded at 22:49 KST from the same second account;
the user was advised against further use of that account (2026-11-12).

## Second set: calibration and pooled stacks — preregistered 2026-11-13 before any upload of them

Main-account uploads only (owner `minjoonyoo`, team "Odyssey"); the assistant prepares no
package or plan for any other account.

| Upload | Path | Content per instrument |
|---|---|---|
| E073c | submissions/2026-11-13-E073c.zip | all three: guard over `cal, tpool, tpoolh, tpoolh+cal` (no expert) |
| E073x | submissions/2026-11-13-E073x.zip | UNHCR: guard over `xlpool, xlpoolh, xlpool+cal, xlpoolh+cal, tpoolh, cal` with experts n and m; UNICEF / WB = E041 |
| E073pc (reserve) | submissions/2026-11-13-E073pc.zip | UNHCR / WB: guard over `cal, tpoolh, tpoolh+cal, nlpool+cal, nlpoolh, nlpoolh+cal`; UNICEF = E041 |

Identities (2026-11-13, after the final local validation of the patch-10 source):
- E073c 103068848 bytes, SHA256 ff3c04332e43134fcf717ef8a110ca3bede26aada88fbdd132911d8f8ab1569b
- E073x 103068820 bytes, SHA256 d5bc1585c678bbad26c928daa1855fbe270fc3b2fb6e24c0e835d4757d77871f
- E073pc 103068852 bytes, SHA256 1d7efa5a1b7bbd5ec237543d9f4dee526b3af6d1d4c36b2fb081bd6a4da6e3ec
Local (synthetic, kit aa03186, model venv, RTX 3070): ZIP checker OK x3; official phase 1 PASS
on all three instruments for each; all vectors valid; wall c 524 s, pc 489 s, x 474 s (UNHCR x:
shadow n 33 s + m 36 s). Every guard rejected every chain on the synthetic data (e.g. UNHCR x
E lower bound -.0001), so all outputs equal E041 there; the sandbox has no neighbour structure,
this is plumbing and runtime evidence only. Fitted chains are ranked by two-fold out-of-fold
S scores and refitted on S+E after acceptance (patch 10). E073p (pool applied without a guard)
moved to tmp/e073/reserve/, not for upload.

Arms (each instrument read separately; E041 bins UNICEF .3499 / WB .2335 / UNHCR .8457, and
UNHCR .8264 is E041's own boundary reading about two times in five):
- E073c above the E041 bin on an instrument: output sharpening/calibration gives a readable
  gain there -> Final keeps the guarded calibration first. Equal (or UNHCR .8264): unresolved.
  UNHCR <= .8071, WB <= .2185 or UNICEF <= .3364: adverse (accepted internally, worse on the
  all-visible run) -> calibration dropped from the Final.
- E073x UNHCR >= .8650: readable gain from pooling E041 with the neighbour trees -> Final uses
  the guarded pools. .8457 / .8264: unresolved. <= .8071: adverse -> pools dropped.
- Failed status / HSCC code: not counted; fix and re-upload.
No numeric expectation is stated: no real-data evidence exists for these chains.
Upload window valid under either daily-reset convention (UTC or AoE day): 2026-11-13 09:00 to
21:00 KST; the last three: 2026-11-14 09:00 to 21:00 KST.

## Actual results of the second set

(append below; keep the arms above unchanged)

### 2026-11-13 revision before any upload of the second set: E073x replaced by E073xm

Runtime review: if the guard accepts a two-expert pool, E073x refits experts n and m on all
visible rows (about 90 s locally) on top of 69 s of shadow tree fitting; with hosted CPU tree
fitting 1.9-2.7x slower (bracket from E073b timeout / E073s finish) the run could reach
810-935 s, i.e. a timeout exactly when the candidate works. E073xm uses the single expert m
(n's features plus the soft votes of the ten nearest rows): UNHCR guard over
`mlpool, mlpoolh, mlpool+cal, mlpoolh+cal, tpoolh, cal`, UNICEF / WB = E041, and
BUDGET_SECONDS = 880 as a backstop (final expert fit skipped beyond 748 s, output then E041).
Hosted estimate 645-715 s when accepted. E073x and E073pc moved to tmp/e073/reserve/ (not for
upload). Arms: those of E073x above, unchanged.
- E073xm 103068841 bytes, SHA256 a49b22e4fcf7144bd0e22965cd9a4cbc737f42a685c301dd24bcce575e2a752c
Local (clean synthetic, official phase 1): PASS on all three, UNHCR 356.4 s / WB 66.2 s /
UNICEF 29.2 s (452 s); shadow m 40 s; mlpool out-of-fold S gain +.00014, E lower bound
-.00006 -> rejected; vectors equal E041 on all three (0 changed). The scorer's printed phase-1
value is noised (WB printed .2776 or .2907 for identical vectors); comparisons use exact logs.
ZIP checker OK. Acceptance path exercised on the two-fidelity duplicate simulation
(tmp/e074_make_sim2.py; synthetic, mechanism only): out-of-fold S gains mlpool +.0270,
mlpool+cal +.0274 log; E lower bound +.0227 -> `mlpool+cal` accepted (exponents E041 .28,
m .68), expert m refitted on all visible rows (42 s), official log -.388611 -> -.353962
(+.0488 old-scale skill; E074t on the same table +.0100), 536 s local. On that synthetic
structure the neighbour trees dominate E041; on real data E073n alone read one bin below E041,
so the real structure differs from this simulation and no transfer is claimed.

### 2026-11-13 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1050766 | 2026-11-13-E073c.zip | 2026-11-13T09:14:54.143556Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1050762 | 2026-11-13-E073xm.zip | 2026-11-13T09:14:18.549164Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

Both equal E041 on all four values (old-scale .52 / .49 / .92). Arms: E073c **Unresolved**
(calibration / temperature rejected internally or accepted with a sub-bin gain); E073xm
**Unresolved** (same for the m-pool). Both finished inside 900 s (no hosted runtime supplied).
Three uploads were accepted on the UTC day 11-13 at 09:13-09:14 UTC from the main account.
