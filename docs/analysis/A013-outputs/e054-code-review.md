# E054 pre-execution code review

Reviewed scripts/analyze_e054_resolution.py and tests/test_e054_resolution.py
on 2026-09-24 before schema-only execution. No tests rerun, fits, respondent
access, or production edits by this reviewer.

## Findings

1. **No material LP sign/coupling defect found.** Variables are four true
   skills C1/C2/H/P and six independent-coordinate noised readings. Both
   baseline and probe controls couple to the same true C1/C2. Each instrument
   uses its own public tail radius. Baseline individual displays and Grand
   constraints remain joint. Gated-loss constraint, ungated-loss-derived P
   bounds, floor-limited instrument bounds, and all three objectives agree
   with independently derived identities. Negative true skill is allowed.

2. **Conservative reporting-order relaxation must be disclosed.** The
   after-order LP permits mean unrounded probe skill within one display step
   of probe Grand. This contains the exact discrete reporting model. Its
   extrema are conservative outer bounds, not exact extrema of that model;
   unresolved outer-feasible arms need not be literally feasible. Requiring
   a literal feasible witness for a passing after-order arm prevents a
   vacuous PASS from an empty exact set. Any priority valid throughout the
   larger set holds in the exact subset. This may lose valid informative
   arms (false STOP), never justify a stronger priority. The preregistration's
   request to enumerate feasible allocations and LP minima/maxima should be
   reconciled explicitly with this implementation deviation before reporting.

3. **Specify schema encoding explicitly.** run() uses Path.read_text()
   without encoding for schemas. On Windows its default can fail on Unicode
   UNHCR metadata; use encoding='utf-8'. This is a reproducibility fix, not a
   statistical change. Root notified before execution.

4. **Witness verification can be stronger.** Current literal check verifies
   only probe instrument/Grand rounding, while baseline display bins are
   closed LP bounds. Prefer checking all baseline literal displays too and
   retaining baseline noised values in the witness. Ties have probability
   zero under continuous Laplace draws, so closed intervals are conservative
   for extrema, but claiming a literal witness merits checking both paths.
   HiGHS feasibility tolerance exceeds the 1e-10 bin inset; checking returned
   solution residuals avoids relying on that inset alone. No current false
   priority finding established; output review should inspect actual margins.

5. **Enumeration covers current schema.** Independently using the 93-draw
   constants, baseline H interval and group floor gives
   P in [.1709454090694246, .2602664691846944]. Adding loose control/noise and
   after-rounding bounds puts all displayed Grand values within
   [.3733079691234773, .4437626569612290]. Thus [-1,1] enumeration contains
   every relevant current reading. This conclusion is specific to the
   fixed baseline/schema, not a general property of negative-skill models.

## Test coverage and decision interpretation

Existing nine tests exercise identities, floor limits, union bound, exact
zero-error inversion, monotonic uncertainty, infeasibility, literal probe
rounding, inconsistent baseline Grand, and strict priority margin. Root's
reported pass was not rerun here. More valuable than duplicate tests would be
independent post-output checks of each passing witness, all LP residuals,
reported priority extrema, and same-arm robustness across reporting orders.

The 93-draw set contains the six-draw set, so its robust priority holds on
any nonempty six-draw subset. This does not ensure six-draw feasibility:
an arm can exist only in the larger envelope. Unknown
hosted aggregation, baseline selection count, and exact repeated control
predictions remain assumptions. Formal existential PASS is neither expected
information gain nor a recommendation that this slot is likely worthwhile.
It never chooses sentinel/gate repair over content-answer repair.

## Independent output review

Reviewed archived e054-resolution.json after execution. Root fixed explicit
UTF-8 reads and baseline literal-rounding checks before freezing b57ec24.
No model fit or project Python import was used in this review. Independent
PowerShell arithmetic checked eight source hashes, nine witness noise/display
conditions, and four closed-form extrema against the output: 21 recorded
checks passed. Group floor checks also passed.

Only .38 passes the implemented 93-draw rule. Its D intervals are:

- Before rounding: [-.08823564965782646, -.07808346439868942].
- After rounding outer envelope: [-.08823564965782646, -.04808346439868942].

These extrema were independently derived without invoking the LP. Let
Hlo=.915-tH, C1lo=.515-t1, C2lo=.485-t2. The common lower bound is
2*Gmin-1+Hlo. For reporting-error e=.005 before or .01 after, the upper
P is 3*(.38+e)-C1lo-C2lo+(t1+t2+tH), and upper D is
2*A-Hlo+2*Pmax-1. Each agrees with the saved LP result within 5e-16.
The strict .015 threshold has ample numerical margin.

The after-order witness has L_G=.00239022492757082 and
L_C=.08924574762303458. Baseline noised values round to .52/.49/.92;
probe noised values round to .51/.48/.16, whose mean rounds to .38.
All six errors respect their declared bounds. This same true allocation
also supports a before-order witness: set probe control noises to -t1/-t2
and retain its probe UNHCR noised value .164999. The noised probe mean is
approximately .3835388236172043, which rounds to .38, while the baseline
noised mean is .6383343333333334, which rounds to .64. Thus both reporting
orders have actual witnesses, not merely an outer-set artifact.

The archived witness uses baseline noises at their upper tail bounds and
the UNHCR probe noise at its lower bound. It demonstrates feasibility only,
not typical behavior or probability. Gated-item residual loss is nearly its
score-floor minimum and ungated loss contains nearly all remaining loss.

### Registration interpretation requiring explicit disclosure

Under six draws, .38 is infeasible before averaging and has no literal
after-order witness. No arm passes both reporting orders in that scenario.
Therefore do not report robustness across both six- and 93-draw envelopes.

The prose preregistration says "including the93-draw sensitivity" without
explicitly naming 93 as primary or requiring a conjunction of feasibility
across both draw counts. The frozen pre-run implementation explicitly uses
the 93-draw decision. That supports a defensible 93-primary interpretation,
but the prose alone is ambiguous. A transparent verdict is: "PASS under
the archived implementation's 93-draw rule; no arm passes the six-draw
rule under both reporting orders." Selecting 93 after seeing this output
would be unjustified; the pre-run script history is the relevant evidence
that this was not a post-result decision change.

If the intended prose criterion instead required a passing arm in BOTH
draw envelopes, this result is STOP. The correct mathematical observation
is that enlarging uncertainty can create feasible arms while weakening
precision within existing arms; an existential feasibility gate is not
monotone in the direction users usually expect from sensitivity analysis.
Packaging permission under the frozen 93-only implementation does not
remove that practical limitation or establish expected usefulness.
