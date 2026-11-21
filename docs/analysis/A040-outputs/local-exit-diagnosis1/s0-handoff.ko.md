# S0 전달 — A040 종료 crash 조사

판정 **LOCAL_EXIT_DIAGNOSIS_HOLD**. 수리 PASS/S2 후보 없음.

- builder 실패 crash 재현. A040 launcher/Context 없이도 재현.
- 같은 import/SDK loop 및 image 정의 대조는 exit0.
- coroutine 관측·출력 wrapper를 각각 제거해도 c0000005 유지.
- 첫 구분 경계는 실제 build/resolve. 정확한 객체/원인 및 upstream 결함 미확정.
- 5개 비교/6개 자식, 감독자27.3473137초, 각30초 이내, 강제 종료0/잔여PID0.
- C6 미실행: 시간 gate 차단. 전체 gross40분 초과를 명시적으로 기록.
  전체 자원 준수 PASS로 처리하지 말 것. deadline 변경/추가 검사 없음.
- 새 출력 wrapper 제거는 진단용이며 수리 후보가 아니다. 원본은 보존.
- 기존 image/120초 관측과 HOLD/실자원 종료 확인은 그대로 유지.
- 실제 원격/RPC/모델/보호 자료/환경 변경/commit/push/ZIP/S2/S3 없음.

검토: closeout.md, verification.json, regression-history.md,
C1..C6-registration.md, *-process.json/*-stderr.txt, source/placement.diff,
source-manifest.json/artifact-manifest.json, cost-time-ledger.json.

다음에 필요한 것은 build/resolve와 native 종료 사이의 구체적 인과 근거다.
C6는 미검증이며 자동 실행 권한 없음. 같은 전체 suite/120초/임의 환경 교체/
원격 재시도로 넘어가지 않는다. S0가 추가 조사 가치·범위 또는 보류를 판단한다.
E041/E025·parked·STOP/HOLD·노출·A018 미확정·S3 중단 모두 유지.