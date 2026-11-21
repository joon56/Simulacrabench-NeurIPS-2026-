# S1 제목: A040 — 출력 생산자·회수기 계약 보완

기존 S1에 아래 본문을 전달한다. 작성 자체는 실행 허가가 아니다.

```text
SimulacraBench / HSCC S1 로컬 기술 보완.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
이번 사용자 지시는 아래 출력 계약 보완만 허용한다. 원격 실행 권한 없음.

AGENTS → CLAUDE → status → log 최신3개 → workflow.md를 읽고 역할/개정/허용
범위/읽기 증거와 workflow 해시를 entry에 기록한다. HEAD/dirty/관련 jobs 확인.
기존 변경·실패·PASS·manifest/latch를 보존한다. 서브에이전트 실행 금지.

입력:
docs/analysis/A040-outputs/s0-modal-integration-review/decision.md
docs/analysis/A040-outputs/modal-local-integration1/의 closeout.md,
phase-evidence.md, verification.json, contract-manifest.json, source-manifest.json,
sandbox_stage.py, linux_runner.py, tests_integration.py, regression-history.md.
docs/analysis/A040-outputs/full-path-resume1/fixture-manifest.json 및
reference/result.json은 메타데이터만 읽는다. 그 경로의 실제 입력/출력 배열은 금지.

기준 source-manifest SHA256:
8377129e94e8457aebd64156d1599efd8bf7b4a49f2c1b99b2dc00104218451d
기준 sandbox_stage.py SHA256:
8e0cfd474416aa586af9f7ec936c20c7d4fbf0c1888d2d770cc10c4d038027d0

새 위치 docs/analysis/A040-outputs/modal-output-contract-repair1/ 및
tmp/a040-modal-output-contract-repair1/. 충돌 먼저 확인, 기존 폴더 덮어쓰기 금지.
새 복사본에서만 수정한다. 실행기 모듈 배치·manifest 갱신은 필요한 만큼만
허용하고 경로 변경을 diff로 구분한다. 기존 model/과학 runner 본문은 변경 금지.

문제:
생산 runner는 world_bank 키/파일을 만들지만 회수기는 wb를 요구한다.
현재 test 대역도 wb를 만들어 정상 경로가 거짓으로 호환돼 보였다.
또한 최종 gate는 기관별 개수 대신 총합만 확인한다.
기존39-case 통과와 LOCAL_ORCHESTRATION_CONTRACT_PASS는 역사로 보존한다.

할 일:
1. 기존 frozen fixture-manifest의 instrument/vectors와 runner의 쓰기·읽기
   경로, 과거 reference/result 메타데이터를 연결해 기대 계약을 고정한다.
   unicef17856, world_bank39520, unhcr132273; 합189649.
   candidate 추가 hash/file은 unhcr-engineering-alpha025와 unhcr-final-e041.
   추가 두 파일은 원래 output_counts 합에 중복 포함하지 않는다.
2. 현재 exporter에 생산자와 동일한 키를 가진 작은 protocol 결과를 넣어
   mismatch를 재현한다. 모델 import/실행 없이 실패 증거를 보존한다.
3. 새 exporter/test의 이름·경로·기관별 count 검증만 최소 보완한다.
   실제 runner를 wb로 바꿔 맞추거나 alias를 모두 무조건 허용하지 않는다.
   test 기대값을 consumer 상수만 복사해서 만들지 않는다. 기존 producer
   metadata/source에서 독립적으로 확인한 계약과 양쪽을 대조한다.
4. 모델 없는 변경 영향 회귀: 정상 reference/candidate 회수, world_bank
   filename/key 연결, wb 오기·누락/추가 키·총합은 같지만 기관별 개수 오류,
   hash/출력 누락 시 거절, reference 회수 실패 시 candidate0.
   실제 향후 exporter/orchestration 코드를 호출하고 외부 endpoint만 대역화.
   작은 bytes/hash와 실제와 같은 metadata envelope는 protocol fixture임을
   명시한다. 배열 []를189649개 예측 생성 증거로 주장하지 않는다.

한도:
로컬 active45분, focused regression 누적120초/최대3cycle. 범위 내 수정과
영향 경로 재검증 허용, 각 실패/수정/회차 보존. 무변경 성공 반복 금지.
기존39개 전체 suite/15개 suite/성공 과학 fixture 재실행 금지.
범위 밖 결함·새 의존성 필요·한도 소진이면 구체적 기록 후 종료한다.
예비 작업은 해당 closeout뿐; 추가 수리나 원격 재시도 자동 시작 금지.

허용: 문서·생산 소스·명시한 기존 result/manifest 메타데이터 읽기/해시,
설치 SDK/protobuf의 RPC 차단 import, 새 로컬 복사본/소형 protocol fixture,
등록된 회귀·소스 보존 확인·status/log 결과 추가.
금지: 인증/계정/RPC/설치/다운로드/빌드/전송/Sandbox/GPU/H100,
payload112·기존 fake3·checkpoint·실제 응답·키·Parquet/NPZ·cache/VAF 접근/해시,
model import·fit/predict/score·실제 Linux boundary/watchdog/science 실행,
과거 실제 출력 배열 열람, 새 E/ZIP/checker/release/upload/commit/push/tree/S2/S3.

종료 판정:
생산자·회수기 metadata/file 계약과 새 회귀가 일치하면
LOCAL_OUTPUT_CONTRACT_PASS / REMOTE_EXECUTION_NOT_AUTHORIZED로 S0 반환.
실패하면 정확한 반례·남은 조건을 기록한다. S0 검토 없이 다음 단계로 가지 않는다.
이 PASS는 실제 Linux/H100/900초/효과/release 인증이 아니다.

산출물: entry/receipt, producer-consumer-contract.md, 최소 source.diff,
새 source/contract manifest, 실패 재현·변경 영향 회귀 증거·시간,
보존 verification, exposure/cost-time ledger, closeout, s0-handoff.ko.md.
누적 준비/controller7553.1022106초와 과학4process/1077.3504532초는 분리 승계.
USD1/5 누적 계획·현금0 유지. 기존 billing0/component0.00001152USD는
재조회하지 않으며 미게시/귀속 미확정 유지. 이번 원격 비용 발생 작업0.
E041/E025, E057/E060/E061 parked, 모든 STOP/HOLD/E058/E059/A039,
17999/12339SSUID·집계·A022 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 보존. A_half 비승격/A018 미확정/S3 중단.
```
