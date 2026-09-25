# A016 — Post-E055 research decision and S1 handoff
date-started: 2026-09-25
status: done
relates-to: A006 / A009 / A014 / E041 / E046 / E051 / E055

## Goal

Select one bounded next research task toward final TEST, without fitting or
packaging in S0. This is prioritization, not evidence of model improvement.

## Attempt log

### v1 — 2026-09-25: source and scoped-negative-evidence review

- Read CLAUDE, status, latest three log entries, workflow and session catalog
  in the required order. Inspected A006/A009/A014, E041/E045/E046/E048/E049/
  E051/E055, tree_blend.py and recursive_candidates.py. No model scores opened.
- Input HEAD: 7f712e136896b8b89a83d724a5d355d3c5c764fe,
  branch work/e050-submission. Existing unrelated changes: .gitignore,
  .claude/skills/paper-session/SKILL.md, .claude/settings.local.json and trip/.
  Preserve them; they are not part of this handoff.
- Get-Process showed no python/wsl process; node processes present. CIM command
  lines were inaccessible. This is limited process visibility, not a lock or
  proof no external work exists. S0 started no fit/job.
- E046 already addressed E040's fair-validation question on an Adult proxy;
  E051 already screened direct full-answer trees against actual E041. Merely
  fixing E040 again or renaming E051 would not be a distinct main task.

## Hypothesis comparison

| Hypothesis/task | Supporting evidence | Contrary evidence / risk | Valid test scope and action | Cost cap / priority |
| --- | --- | --- | --- | --- |
| Independent asked-answer prediction for gated leaves, retaining E041 sentinel mass | Prior tree studies targeted ungated/full distributions; a conditional tree can supply different GIVEN interactions within observed asked respondents. A014 supplies audited natural asked labels. | E041 already has conditional neural/ladder heads; factorization itself is not novel. E046/E051 tree gains were weak. Sparse asked rows increase variance; SIPP hospital content differs from refugee content. | Fixed conditional-tree library, finite constant-share oracle, separately selected weights and one group audit. Test complementary learned content, not gate repair or humanitarian transfer. | Main: one group view, <=1 E041 fit and six small tree fits; 2 CPU threads, no GPU, <=20 min cumulative fit wall, <=90 min research wall. Caps are limits, not runtime estimates. |
| Repair E041 replay calibration | A011 measured membership/objective mismatch; E041 retrieval was useful on DEV. | E053 and E055 finite-family gains were very small; E055 exercised both buckets and recursion. Mismatch is not a repair gain. | Different target-domain exploratory design could remain legitimate; no ready informative new channel/family currently justifies another calibration cycle. Preserve prior STOPs. | Lower priority; additional refits/renderer work with uncertain decision value. No work authorized here. |
| Repeat direct full-answer trees or enlarge PFN parents | Independent signal could exist; historical validation defects limit broad closure. | E046/E051 already stopped; E049 actual learned gains weak, hosted .64/no update. Blind size/guard sweeps repeat exposed decisions. | Need a distinct library and credible new information first. No automatic revival. | Medium/high fit and packaging cost; defer. |
| E054 loss probe | Qualified immutable package already exists. | A013 found limited useful readings; adverse ablation is not a score-seeking candidate. | Only a separately justified diagnostic could spend a slot. Keep parked. | Low preparation cost but one scarce/noisy DEV reading; not backup. |
| TEST decision and readiness gap review | E041 and E025 already have phase-2 qualification and method artifacts. Helps preserve an executable finalist if research stops. | No expected DEV gain; repeating completed checks adds little. | Compare frozen evidence, define selection/freeze criteria, identify only unverified engineering/disclosure gaps. No final selection or new package. | Backup: <=30 min read-only artifact review plus documentation, no fits. |

## Decision and domain check

Main: reserve E056 for **sentinel-preserving conditional content on gated
leaves**. A016 is this S0 analysis; no E056 experiment exists yet. Next S1
must register E056 before fitting and verify the reserved ID remains free.

Novelty is the independent asked-only predictor and final leaf-content
intervention, not conditional factorization. E051 trained complete answer
distributions including the sentinel; E055 changed existing evidence shares
inside recursion. Neither bounds this new fitted library. Their negative
evidence still reduces enthusiasm for another tree study.

[unchecked hypothesis] In humanitarian surveys, who was asked and what an
asked respondent says need not have identical demographic interactions. Test
only content without inventing exact refugee gates, household recurrence or
new demographic facts. On SIPP, observed non-sentinel labels define asked
training rows; no true parent/answer is an inference feature. A014's US health
domain, editing, sparse asked population and exact gates limit transfer.

At each leaf let p be the raw E041 vector, g its sentinel entry and M the sum
of its non-sentinel entries. Candidate q is a normalized conditional content
vector. Keep p'[g]=p[g]; set p'[answers]=(1-alpha)*p[answers]+alpha*M*q.
Alpha=0 returns the original vector directly. Raw total mass is preserved;
all parents and non-leaves stay exact E041. The official uniform-mixture floor
can indirectly change the final sentinel probability: measure and disclose it,
never claim post-floor sentinel equality without verification.

Use only the existing E055 12000-person sample and A014 SSUID-group roles.
Previously exposed oracle results are development evidence; do not describe
the sample as untouched. Leave person-view roles unused in this study.
Group selection/audit model scores were unopened at S0; audit is consumed once
if reached. The E055 calibration role stays masked/unscored throughout.

Prospective E056 feasibility screen: exact oracle over fixed per-leaf shares
{0,.25,.5}; require pooled seven-head delta skill >1e-10 to proceed to cheap
selection, otherwise STOP. This detects absence of a usable library at numeric
resolution; it is not a significance/adoption threshold, and not E055's gate
lowered after failure. The family has new fitted predictions. Learned audit,
uncertainty, intervention size and deployment cost determine further research;
no positive oracle alone earns a package. Full details in the S1 prompt.

Backup triggers only if the main is invalid, nonpositive, inconclusive or over
cap. Review existing TEST artifacts and write a decision matrix; do not refit
or rebuild completed A012/A013 work. No automatic third research task.

E041 remains DEV incumbent; E025 remains fallback. No winning-score forecast,
current slot availability, new hosted activation or final TEST choice asserted.
Potential gains and hosted readability remain unknown. No package recommended
now because no new candidate has efficacy evidence or release qualification.

## Reference identity and source check

- E041 main: submissions/2026-09-19-E041/main.py, SHA256
  22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
- E041 ZIP: submissions/2026-09-19-E041.zip, SHA256
  1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50.
- src/eval/recursive_candidates.py SHA256
  678ac72405d5c766c78318f79bd84747f6b0148ec3a9e8eb9243a810238c32a5.
- Official [HistGradientBoostingClassifier documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html)
  consulted 2026-09-25 for the public classifier API only. Reuse installed,
  recorded project version; no dependency upgrade or efficacy claim from docs.
- Date discrepancy remains in historical CLAUDE versus phase2 runbook. No
  deadline relies on either unverified date; S3 must verify current official dates.

## Artifacts and handoff

- [Copy-ready S1 prompt](../plans/2026-09-25-S1-conditional-content.ko.md).
- Updated status and log. Documentation only; no model, archive or score change.
- S1 is integration owner after S0 ends. Recheck HEAD/dirty files/processes.
  Next analysis ID A017; E056 reserved, not yet preregistered or executed.
