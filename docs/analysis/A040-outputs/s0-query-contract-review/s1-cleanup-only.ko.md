# S1 — 종료 조회 helper 검증과 기존 Sandbox 정리만

사용자가 이 프롬프트를 S1에 전달해 실행을 지시할 때 아래 범위만 활성화한다.
S0 작성 자체는 실행 허가가 아니다. 이전 조회 window와 resume5 허가는 소비됐다.

폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1
역할: S1 기술/기존 자원 정리. 전체30분, 종료 기록5분 확보.
목표: 검증된 조회 helper로 정확한 기존 Sandbox의 terminal 증거를 확보한다.

AGENTS → CLAUDE → status → log 최신3개 → workflow를 읽고 개정·역할·범위를 보고한다.
HEAD/dirty/관련 jobs를 확인하고 읽기 증거·workflow SHA256을 entry에 기록한다.
기존 변경·실패·latch·manifest를 보존한다.

읽을 자료:
- docs/analysis/A040-outputs/s0-query-contract-review/decision.md, verification.json
- docs/analysis/A040-outputs/sandbox-lifecycle-repair1/closeout.md,
  termination-billing-receipt.json, verification.json, cost-time-ledger.json,
  confirm_terminal.py, source-manifest.json
- tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages/의 관련 SDK1.6.0 소스
  modal/_grpc_client.py, modal/sandbox.py, modal_proto/api_pb2.pyi 등

실패 helper SHA256:
28019d3b2543e1f53d667b63af302b806e49b70e19bbe19aa25b2aaa735abd57.
기존 생산 manifest:
c782c99e29cfceeaba132018d48f2be2a844e7f8b51ba8840157f9ebfa845765.
허용 문서·helper·SDK 소스만 식별한다. payload112/원본 pins/모델은 재해시하지 않는다.

1. 종료 확인 전에도 가능한 로컬 helper 수리·검증

새 docs/analysis/A040-outputs/termination-query-repair1/에만 작업한다.
경로 충돌 시 새 경로를 사용한다. 원본 helper와 생산12모듈은 보존한다.
이번에는 종료 helper 준비를 terminal 확인의 선행 단계로 명시적으로 허용한다.
생산 controller/stream lifecycle 수리는 이번 범위에서 제외한다.

문제는 timeout=cap을 주면서 retry=None을 누락한 호출 계약이다.
한 호출만 고치지 말고 실제 사용되는 모든 SDK RPC 호출을 검증한다.
SDK UnaryUnaryWrapper.__call__의 원래 InvalidError/transport0을 로컬 재현한 뒤,
정정 인자가 실제 wrapper를 통과해 fake transport에 도달하는지 확인한다.
wrapper 자체를 대역으로 바꾸어 같은 오류를 가리지 않는다.
SDK 설치/패치·실제 인증·네트워크·모델 import는 로컬 단계에서 금지한다.
소유 asyncio IPC는 허용하되 외부 통신/정상 Client.from_env는 차단한다.

작은 고정 protobuf 응답으로 같은 helper 전체 분기를 확인한다:
- 정상 workspace/app/name/env, finished-inclusive 조회와 정확한 단일 ID
- 빈/중복/불일치/미지정·알 수 없는 상태에서 terminate0·terminal 미확정
- 이미 terminal이면 terminate0; running이면 정확한 ID에 terminate 최대1
- 실제 SDK의 Sandbox V1/V2 판별·wait/terminate 호출 및 인증 관리 계약
- timeout/cancel/예산 소진에서 추가 호출 차단·receipt 보존
- terminal 확인 뒤 billing 실패가 terminal 증거를 지우지 않음

V1이라고 추측하지 않는다. V2가 필요하면 정상 SDK 인증 관리 경로를 사용하고
토큰은 출력/저장하지 않는다. 로컬 대역은 가짜 토큰만 사용한다.
상태는 설치 protobuf의 명명된 enum으로 판독하고 미지정/새 값은 보류한다.
오류는 type/stage와 비밀값을 제거한 message를 기록한다.
helper 성공 종료와 실제 terminal PASS를 분리한다.
최소 수정만 수행하며 소규모 경계 검사 wall 합180초/각30초, CPU2/GPU0.
이 한도 안에서 새 로컬 결함을 수정할 수 있다. 실패 cycle/diff를 보존한다.
기존 성공 fixture/15/39/14/6 suite는 반복하지 않는다.

2. 로컬 계약 PASS 뒤 같은 S1에서 기존 자원 확인

별도 S0 왕복 없이 다음 단계를 수행하도록 이 범위에서 허용한다.
수정 helper hash·허용 RPC·새120초 window와 deadline을 먼저 동결한다.
정상 인증/SDK 재사용. 재설치·재로그인·계정/usage/spend 변경·문의 발송 금지.
원격 window1회, 호출마다 최대15초, 마지막30초는 terminal/receipt에 배정한다.
billing은 terminal 증거 저장 후 남은 범위에서만 확인한다.

대상:
workspace joon56 / environment main
App ap-XiMVzlJgrNrCiFpIN1kB4W
App name a040-resume5-20261005-094405
Sandbox name a040-resume5-20261005-094405-gpu
Sandbox ID 미확인. App STOPPED/task0는 과거 관측뿐이다.

허용: 정상 인증, 정확한 기존 자원 identity/status/finished 결과 조회,
살아 있을 때 그 Sandbox만 종료 요청 최대1회, terminal 확인, billing 요약.
목록은 가능한 app/environment로 제한한다. 정확한 소유 자원 확인 전 종료 금지.
새 App/Image/Sandbox/build/exec/files/전송은0. 다른 계정 작업 종료 금지.
raw StreamReader handle 생성은 피하고 검증한 metadata 경로를 사용한다.
SDK 정상 내부 인증을 외부 수동 토큰 열람으로 대체하지 않는다.

명시적 대상 terminal result 또는 정확한 공식 상세 화면 증거가 있어야 완료다.
App STOPPED/task0, ACK, active-list 부재, NotFound, 시간 경과는 대체 증거가 아니다.
SDK/service의 예상 밖 첫 오류나 window 만료 시 추가 수리/새 window 없이 종료한다.
미확인 상태면 exact ID/상태/시각 중 빠진 항목과 필요한 공식 화면만 명시한다.
정확한 자원을 찾았더라도 낯선 버전/불명확한 권한이면 추측해 종료하지 않는다.

3. 종료·산출물

terminal 확인 여부를 최우선으로 기록하고 과학/생산 수리로 진행하지 않는다.
산출물: entry, helper/diff/hash, wrapper·protobuf 영향 회귀, terminal/billing receipt,
비용·시간/노출 장부, verification, closeout, s0-handoff.ko.md, status/log.
최종 판정은 TERMINAL_CONFIRMED 또는 구체적인 미확인 원인이다.
local PASS만으로 원격 terminal을 선언하지 않는다. 화면 증거도 출처를 구분한다.

누적 준비12587.4312918초·과학4process/1077.3504532초를 승계하고 겹친 시간을
더하지 않는다. 기존 billing0.00178978USD 집계, 2400초 예약2.965933453125USD,
게시/귀속 미확정, USD1/5 계획·cash0 유지. 예약은 실제 청구가 아니다.

금지: 새 유료 자원·H100/모델 실행, controller 생산 수리, payload/응답/키/
Parquet/NPZ/checkpoint/cache/VAF 접근·재해시, fit/predict/score, ZIP/업로드,
새 E, commit/push/tree 수정, 서브에이전트·S2/S3/TEST 선택.
E041/E025, parked E057/E060/E061, 모든 STOP/HOLD/E058/E059/A039,
노출17999/12339·집계/A022역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 미확정/S3 중단/S2 없음 유지.

