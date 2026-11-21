# E069 — World Bank sentinel from a direct classifier where the gate is approximate
parent: E065
status: parked
date: 2026-11-08

## Registration (before any hosted run)

World Bank schema description: "feedback-arm randomisation in a 1229-person subsample and
a 6-month tracer follow-up in 471 of those." The schema gates 19 tracer items on the GIVEN
`group` in {yes1..yes4} (the 1229 randomised) and 2 more on tr_job_full = Yes, so the gate
calls ~62% of randomised respondents "asked" although only 471 were followed up. E041 mixes a
hard path (sentinel ~0 for group = yes) with a soft direct path, weighted by gate agreement,
which plausibly under-predicts the sentinel for randomised respondents. Leaderboard context
(user screenshot 2026-11-08): 36 of the 50 entries above us show WB .25 (old .50) versus our
.23 (old .49).

Rule: for each gated PREDICT head whose schema gate agrees with the visible rows' sentinel
pattern less than 95% of the time, replace E041's sentinel mass by a TabICLv2 per-head
classifier's sentinel probability (fit on all visible rows, GIVEN features, frozen E065
settings); content mass keeps E041's proportions. Exact gates (agreement >= .95) and all
ungated heads stay E041. UNICEF/UNHCR exact E041. Build: E067 source with PLAN
{"world_bank": {"alpha": 0, "sentinel": true}}; tmp/e067/2026-11-09-E067ws.zip, SHA256
1201bd48c415c34c20f4637947f9ea97d52be5bf302a87243788fc01898b25e5. Synthetic sandbox gates
are exact, so locally nothing is flagged unless the threshold is overridden for a plumbing
test (env E069_AGREE_MAX, never set on the platform).

Hosted arms (WB versus the day-1 E041-code WB .2335276584; UNICEF/UNHCR must equal
.3499339289/.8457264165): Favorable WB higher (likely .2486 = old .50); Unresolved equal;
Adverse lower; Technical Failed.

## Results

**Local engineering, 2026-11-08.** ZIP checker OK; official scorer PASS on all three;
outputs identical to E041 (0 heads flagged on exact-gate synthetic data). Forced plumbing run
(E069_AGREE_MAX=1.01, all 30 gated WB heads): PASS, 15600 vectors changed, all valid, synthetic
log -1.100061 versus E041 -1.100151; sentinel expert 34 s, WB wall 99 s.
