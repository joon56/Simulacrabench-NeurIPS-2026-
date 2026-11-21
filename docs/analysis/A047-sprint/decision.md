# A047 — Endgame sprint operating mode

2026-11-08 13:36 KST. User-authorized change of operating mode for the
remaining DEV days. Supersedes the per-step S0/S1/S2 handoff loop until the
Final package is frozen; earlier records, STOP/HOLDs and exposure stay intact.

## Actual user instructions (this conversation, 2026-11-08)

- "하루에 3개의 제출물을 낼 수 있어. 해당 사항 유의하고 스프린트 방식으로 가자."
- "코어는 8개이고, RAM이 16인지 32였는지 기억이 안 나." Measured: 31.9 GB RAM,
  16 logical CPUs, RTX 3070 8 GB; 16.4 GB free RAM at measurement time.
- "3번 실행하고" = execute the WB76 deployment route: no requirements.txt,
  vendored pure-Python einops (and tqdm as fallback), hosted psutil with a
  minimal shim only if the import fails.
- "4번은 작업한 결과물 모두 해당 로컬로 다 결과 첨부해서 신경쓰지 않아도 돼."
  = travel-device results are already in this checkout; no reconciliation task.

## Sprint rules

- Executor and single writer of this checkout: this Claude chat. Read-only
  subagents may run in parallel. Root does not kill other sessions' jobs.
- Candidate filter: a mechanism that could move one instrument by about +.01
  (readable on DEV), or that carries a real-data internal guard. No micro-variants.
- Safety line kept for every upload: ZIP checker OK; official score.py phase-1
  PASS on all three schemas; UNICEF/UNHCR raw vectors identical to E041 in the
  same environment when unchanged; measured runtime. Nothing goes into the Final
  package that has not run on the hosted platform once.
- Records: one short experiment file plus machine-written outputs; status/log get
  one entry per milestone. No per-step review documents.
- User keeps: uploads (3/day DEV), final TEST choice, license grant, commit/push.
- Calendar (tentative until the rules refresh returns): DEV candidates through
  Nov 12; Final package freeze Nov 13; Final upload early in the Final window.

## Later user decisions

- 2026-11-08: "라이선스는 BSD-3으로 가자." Team code released for the OpenReview `code_url`
  under BSD-3-Clause (copyright holder: the user, sole rights holder of team-original code
  per A044). Third-party notices (TabICL BSD-3, einops MIT, tqdm MPL-2.0/MIT, starter-kit
  MIT) stay with their files. Repository creation/upload remains a user action unless the
  user explicitly asks the assistant to push.
- 2026-11-08: user will upload three DEV submissions per day and paste the API results.

## Tracks

1. E065 WB76 TabICLv2 expert mixture — executed here.
2. UNHCR mechanism review — read-only subagent; returns at most two candidates.
3. Official rules/schedule refresh — read-only subagent (public web only).

E041 incumbent / E025 fallback; all parked/STOP/HOLD states, exposure ledgers
and protected roles are unchanged by this mode switch.
