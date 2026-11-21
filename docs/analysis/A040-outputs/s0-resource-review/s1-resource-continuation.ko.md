# S1 — A040 동결 입력 재사용·자원 확보 후 전체 경로 검증

이 문서 작성은 실행 허가가 아니다. 사용자가 별도 S1에 아래 범위를 지시할 때만
적용한다. S0에서는 자원 확보 조치·코드 수정·모델 실행을 하지 않았다.

```text
SimulacraBench / HSCC S1 — A040 frozen full-path continuation.
폴더 C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS → CLAUDE → status → log 최신3개 → workflow.md 순서로 읽고 실제
개정·S1 technical 역할·허용 범위를 보고한다. HEAD/dirty/active jobs를 확인하고
기존 변경을 보존한다. 다른 세션/서브에이전트·commit/push·S2/S3는 금지한다.

필수 입력(아래 경로는 docs/analysis/A040-outputs/ 기준):
- s0-resource-review/decision.md 및 verification.json
- full-path-local-retry1/closeout.md, verification.json, resources.json,
  reference/resources.json, official-contract.md, registration.md,
  frozen-inputs/manifest.json, fixture-manifest.json, schema-manifest.json,
  model-free-result.json, dependency-identity.json, exposure-ledger.md
- 같은 폴더 runner.py, watchdog.py, schema_entry.py 및 연결된 소스
- s0-retry1-review/s1-full-path-handoff.ko.md
- s0-schema-failure-review/s1-schema-repair-handoff.ko.md
- s1/contract.md, cost-accounting.md, observation-plan.md

현재 상태:
schema 보완 PASS, 입력 생성/182개 사전 동결 완료. reference watchdog은
BLOCKED_RESOURCE/started:false; scientific latch/child0, candidate0이다.
과거 local failure/tiny PASS와 full-path preparation failure는 불변이다.
과학 누적2회/parent54.0961857초. 이번은 같은 검증의 새 invocation이며
새 실험·새 표본·이전 모델 실패의 구제가 아니다. 주최측 runtime 정책과
기존 설치·공개 checkpoint 취득 승인은 승계하며 다시 요구하지 않는다.

목적:
정확히 동결된 full-shape fake 입력으로 실제 E041 reference 및 통합 후보의
전체 경로·정확한 보존 조건·전체 비용을 확인한다. 효과 실험/제출물 제작 아님.
schema 연구·입력 재생성·성공한 tiny/all3 schema suite 반복은 하지 않는다.

진입 조건과 자원:
우선 모델 없는 읽기 전용 호스트 가용량 확인1회. 기존 watchdog과 같은
physical/commitment 측정 정의로 각각16000000000bytes 이상이어야 한다.
미충족이면 측정값·시각·started:false 기록 후 종료. polling/자동 재시도,
다른 앱 강제 종료·페이지파일/시스템 설정 변경·유료/원격 전환 금지.
사용자가 불필요한 작업을 저장·종료한 뒤에도 통과 여부는 실측으로 판단한다.
각 scientific 시작 직전 watchdog의 동일 자원 gate도 유지한다.

한도: task wall120분, reference900초 + candidate900초, 합1800초 이내,
각 최대1회·총2 scientific process. RTX3070 한개/CPU2/heavy1,
owned-tree RSS/private commitment 각각16000000000bytes 상한,
1초 watchdog 및 CUDA allocated/reserved 기록. 시작 가용량 조건과 실행 중
상한을 구분한다. 시간은 import/load/입력검증/all3/직렬화까지 포함한다.
기존 원본 E041 내부 fallback만 유지·비용 포함; 새 fallback 구제 금지.

새 경로(충돌부터 확인; 존재하면 덮어쓰거나 latch 초기화하지 말 것):
docs/analysis/A040-outputs/full-path-resume1/
tmp/a040-full-path-resume1/
원본 full-path-local-retry1/와 기존 tmp 경로의 모든 파일은 변경하지 않는다.

명시적인 입력 재사용 범위:
full-path-local-retry1/fixture-manifest.json에 열거되고 같은 frozen manifest에
동결된 tmp/a040-full-path-local-retry1/{unicef,world_bank,unhcr}.json 3개를
검증·읽기 전용 재사용한다. 동일 roles.json·schema/fixture metadata도 허용한다.
이 예외는 이번 고정 기술 검증에만 해당하며 노출을 새것으로 만들지 않는다.
나머지 옛 fake 입력/예측·실제 응답/키·Parquet/NPZ·기존 모델cache/VAF는
읽거나 해시하지 않는다. 승인된 tmp/a040-local-technical/venv 및 고정
TabICL source/acquisition checkpoint만 재사용. 설치·다운로드 없음.

허용 코드 변경은 새 위치로 복사한 runner/watchdog의 invocation 경로·출력
TEMP/HF_HOME·새 사전 deadline/manifest 연결뿐이다. fixture manifest의 입력
경로는 원래 동결된 3개 파일을 가리키도록 그대로 보존한다. runner는 그
manifest의 입력 path를 읽으므로 입력을 새로 만들 이유가 없다. 새 reference
결과와 candidate 결과는 모두 새 위치에 기록하고 서로 연결한다.
adapter/orchestration/observer/schema_entry/telemetry, 모델 설정·assertion·
seed/head/context/alpha/guard/floor/tolerance는 보존한다. 이 경계를 넘는
수정 필요 시 실행 전 S0 반환. 기존 코드나 과거 manifest를 덮어쓰지 않는다.

사전 동결:
원래182개 manifest의 경로를 먼저 분류한다. 위 허용 파일·공개 소스/metadata
외 응답/cache가 있다면 manifest에 있다는 이유로 읽지 말고 중단한다.
허용 원본 해시와34개 dependency identity를 확인하고 새 복사본·최소 diff·
새 deadline·입출력 경로를 기록한다. 구 manifest와 새 invocation manifest를
연결하고 이전 BLOCKED_RESOURCE 기록을 보존한다. 현재 설치 상태를 재설치로
맞추지 않는다. 변화가 있으면 경위를 기록하고 실행 전 S0로 반환한다.
원래 schema/tiny PASS를 재실행하지 말고 해당 코드·결과의 동일성을 확인한다.
새 경로·manifest·latch/deadline 연결만 모델 없는 정적 검사로 확인한다
(총60초 이내). runner import/모델 import·추가 tiny fit 금지.
code/input/환경/자원 조건·새 시간창이 고정된 뒤에만 scientific 시작.

실행 순서:
1. 새 reference watchdog1회: 실제 E041 all3, 정확히 같은 동결 입력.
2. REFERENCE_PASS/exit0일 때만 새 candidate watchdog1회.
   UNHCR F6279/S1000/E1000, final visible8279/query621와 전체213 heads 유지.
   full-context shadow/S 선택·E guard/최종 refit 및 원래 alpha{0,.25,.5} 유지.
   자연 정책과 engineering 강제alpha.25 출력을 분리한다. guard 거절은
   사전 설계된 정상 분기이며 효과 반증이 아니다. 전체 활성 경로는 기술적으로
   검증하되 자연 선택으로 둔갑시키지 않는다.
   UNICEF/WB controls와 inactive/fallback/final-R exact parity,
   총189649 vectors, 원래 순서/확률 유효성/입력·checkpoint 상태 불변,
   head별 context 격리 및 전체 fit/predict/load/refit 비용을 확인한다.

첫 예상 밖 오류·parity 불일치·한도 초과에서 중단. 수정 후 재실행/세 번째
scientific process/입력 재생성/축소/seed 탐색/사후 tolerance 변경 금지.
종료가 필요하면 자기 process tree만 처리한다. candidate 직전 자원 gate가
막히면 reference 성공만 보존하고 candidate를 기다리며 반복 시작하지 않는다.

판정/산출물:
- 전부 충족: LOCAL_FULL_PATH_PASS, S0로 반환. S2 자동 전환 아님.
- 시작 자원 미충족: BLOCKED_RESOURCE, started:false와 시각·가용량 기록.
- 모델/계약 오류: LOCAL_FULL_PATH_FAIL; OOM/상한: LOCAL_RESOURCE_LIMIT.
- 시간창 부족/불완료: INCOMPLETE. 정당한 예비 작업은 종료 기록뿐.
entry/registration, 최소 source.diff, 사전 manifest와 원본 연결, input reuse
명세, reference/candidate 결과·자원·검증·exposure ledger·closeout·S0 handoff를
새 위치에 남긴다. status/log 최소 갱신. 과거2회와 새 실행·준비 비용을 구분하고
메모리 peak는 합산하지 않는다. 미실행/부분 완료를 전체 PASS로 쓰지 않는다.

어떤 결과도 ERPIS 효과/H100/hosted900초/native egress/release/TEST 근거로
확대하지 않는다. 남은 S2의 source/assembly parity, ZIP checker, official
all3, E025기관별absolute.002/E041 비교, SCORES·업로드 bytes 검증은 실행 금지.
새 E기록/후보 정책 수정/ZIP/업로드/tree·기존 snapshot 변경/commit/push 금지.
E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
A039 HOLD 별개·A_half 비승격·A018 미확정·S3 중단·S2 후보 없음 유지.
17999명/12339SSUID·A022 원래 역할·집계 노출 및 E059 소비oracle1918/1124·
selection2007/1130, 보호audit2074/1177·calibration1866 보존.
```
