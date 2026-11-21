# A042 S1 closeout

2026-10-09 KST. **CONTRACT_READY_FOR_S0_REVIEW**.
Completed the authorized static information/design task. No technical model,
empirical, release or TEST PASS. [Contract](contract.md), [receipt/verification](verification.json),
[S0 handoff](s0-handoff.ko.md).

Facts: current E041 uses17 GIVEN matches and one weight vector per section.
Public UNHCR wave1/2 is already used by the model; eight groups cover213
PREDICT items. K32 search and deployed legacy K10 have different tie/order
semantics. Section proxy selection differs from lambda replay and recursive
deployment, and final base replay remains in-sample.

Design conclusion: one pair of bounded round weights with a fixed common/difference
penalty can reverse rankings unavailable to a common match metric. Common arm C
is deliberately original R/E041, not a new altered-role selector. Keep .003/2SE,
lambda minimum30/zero fallback, all-cell fit and original base/refit policy.
Fix support fallback before scores; no second H-versus-C selector. Exact endpoint
requires original fitting/selection/replay/render state, not merely equal weights.

Cost: normal all3 remains3 pipelines/9 neural calls/8 metric fits; metric dimension
18→35. Fresh R/H comparison would be6/18/16. No extra metric or whole-stack refit.
Complete time, memory, activation and efficacy remain unmeasured; static tensor
sizes are not process RSS. Existing CPU dependencies suffice at the design level,
not a tested environment/runtime qualification.

Limits: mathematical witness is not a real donor library or oracle. No response,
prediction, model, cache or protected-role access. No implementation, import,
fixture/test, fit/score, web/remote, E/ZIP, commit/push or subagent work. E062's
public tie remains unresolved; previous research STOP/HOLDs and all exposures
remain unchanged. Existing files were read-only except additive status/log.

Next: S0 reviews this one contract and decides whether to authorize a bounded
technical implementation. Independent observed effect evidence lacks an
authorized suitable channel; its exact requirements are in contract section6.
No automatic S2 or another research branch. Entry/end, allowed hashes, shared
document restoration and preservation scope are recorded in verification.
