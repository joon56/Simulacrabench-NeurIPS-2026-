# S0 전달 — A040 계측 오류, LOCAL_CONTRACT_FAIL

S0 결과 검토용. 실행 허가 아님.

AGENTS/CLAUDE/status/최신3개 log/workflow 순서로 읽고,
[closeout](closeout.md), [result](result.json), [resources](resources.json),
[verification](verification.json), [사전 동결](frozen-inputs/run-manifest.json) 확인.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1; dirty 변경 보존.

사용자 “승인해줘.” 후 격리 설치·취득과 RTX3070 단일 검증 수행.
기존 자동 승인 차단 해소. 주최측 runtime 정책도 해소 상태 유지.
설치/주최측 확인을 다시 요구하지 않는다. 새 실행은 별도 범위다.

판정 LOCAL_CONTRACT_FAIL. runner의 event(name, **values)와
tests의 event('many_class_head', name=name, ...) 인자 충돌.
첫 오류 후 중단. 수정·두 번째 scientific process 없음.
가설 반증·GPU 부족·TabICLv2 모델 결함으로 확대하지 않는다.

중단 전 K15 stock/adapter exact parity(diff0), A15/B11/A15와 fresh A
상태 격리, F-only/마스킹/early-E 차단, 가짜 baseline alpha0/fallback/floor,
선택 guard 산술 통과. 실제 E041 미실행.
전체213개 출력·모든 K>10 head·최종 가중치 해시·실제 fake-model S/E는 미완료.

실행1회. fit14/predict15/weight load2. child11.89초, parent13.26초.
샘플 RSS1.593GB/private commitment2.600GB. GPU allocated279.8MB,
reserved308.3MB. 한도 초과 관측 없음. 중단된 tiny fixture 비용일 뿐이다.
전체 context/refit/E041/all3/H100/900초 가능성은 미측정.

다음 판단: 계측 API 충돌만 수정하는 별도 S1 기술 재시도의 가치·범위 검토.
필요하면 모델 없는 logging fixture로 먼저 오류 차단, 새 bounded run
허가 후 고정 정책 그대로 미완료 검증 수행하도록 인계한다.
현재 실패 코드/manifest/latch 보존. 이번 세션 수정·재실행 없음.
seed/head/context/grid/tolerance 변경이나 유리한 결과 탐색 금지 유지.

S2 전달 불가. 남은 검증: 전체 local contract, 실제 E041/control parity,
full-shape shadow/selection/E/refit 비용, 전체 출력/offline 경계,
source/assembly parity, ZIP checker, official all3, SCORES 판독표·byte provenance.
이 목록은 실행·유료자원·ZIP 제작 권한이 아니다.

응답/키/보호 역할/기존 NPZ·모델 cache 접근 없음. 공개 checkpoint만 로드.
실제 노출17999명/12339SSUID 유지, 새 실제 응답 노출0.
E059 audit/calibration 보호. E041 incumbent/E025 fallback,
E057/E060/E061 parked, E058 STOP/E059 STOP_SELECTION,
A039 및 다른 HOLD, A_half 비승격 유지. A018 미확정/S3 중단.
ZIP/upload/commit/push 없음. S0로 반환하고 종료.

