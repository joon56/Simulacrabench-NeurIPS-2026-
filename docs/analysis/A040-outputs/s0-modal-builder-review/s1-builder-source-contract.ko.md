# A040 S1 — builder 모듈 전달 보완과 로컬 검증

이 문서는 S0의 다음 작업 제안이다. 작성만으로 실행되지 않는다.
사용자가 이 범위를 S1에 전달해 작업을 지시할 때 로컬 범위만 활성화된다.
원격 build/H100 실행 권한은 포함하지 않는다.

```text
SimulacraBench / HSCC S1 — A040 builder source 전달 기술 보완.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개,
docs/workflow.md 순서로 실제 읽는다. 역할 S1/기술 검증, 실제 workflow 개정·
SHA256·읽은 경로·허용 범위를 기록한다. 현재 HEAD/dirty/로컬 active jobs 확인.
기존 변경을 되돌리지 않는다. 이번은 로컬 구현·검증만, 원격 실행 아님.

필수 입력:
- docs/analysis/A040-outputs/s0-modal-builder-review/decision.md
- docs/analysis/A040-outputs/modal-full-path1-resume4/의 closeout.md,
  failure-analysis.md, builder-stdout.txt, builder-stderr.txt,
  config-source-input-freeze.json, termination-receipt.json,
  session-cost-time-ledger.json, verification.json
- docs/analysis/A040-outputs/modal-output-contract-repair1/의
  source-manifest.json, sdk_endpoint.py, controller_core.py, live_binding.py,
  contract.py, live_launcher.py 및 전달 경로에 필요한 허용 생산 소스
- tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages/modal/의
  _image.py, _functions.py, _utils/function_utils.py, 필요한 mount 구현.

원래12source manifest SHA256:
0060ed98fc7e3c9ecc5625bd24f5c276971b026817dbb06c92fc2744dec83815
controller_core.py SHA256:
fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb
sdk_endpoint.py SHA256:
94606de56ba23e65e3dcacc57009cb0e60b5506648a2b276cb3165696af4251f
현재 문서 차이는 확인하되 과거 hash에 맞추려고 되돌리지 않는다.

목적과 기존 작업과의 차이:
resume4는 builder가 controller_core를 import하지 못해 설치 본문 전에 실패했다.
include_source=False는 실제 SDK의 defining-module mount를 제거한다.
이전 회귀의 image-build endpoint 대역은 이 경계를 실행하지 않았다.
이번 성공 조건은 실제 SDK가 구성한 builder 함수·mount 목록과 그 정확한
모듈 바이트의 격리 import가 일치함을 확인하는 것이다. flag 검사나 fake
build 성공만으로 PASS하지 않는다. 모델 성능·실제 Linux 실행 검증 아님.

허용 구현:
1. 새 docs/analysis/A040-outputs/modal-builder-source-repair1 경로를 쓰되
   충돌 시 새 미사용 경로를 정한다. 기존 실패/source/latch/manifest는 보존.
   기존12개 생산 모듈 복사와 필요한 로컬 회귀·기록만 작성한다.
2. sdk_endpoint의 installer source 전달만 최소 수정한다. 우선 후보는
   include_source=True. 실제 FunctionSourceInfo가 FILE임을 확인하고,
   SDK client 기본 mount와 별도로 프로젝트 전달 파일이 controller_core.py
   단1개인지, 원격 경로·module_name·function_name이 맞는지 확인해야 한다.
   PACKAGE 분류나 예상 밖 파일 포함이면 자동 허용하지 말고 중단한다.
   repo 전체/상위폴더 자동 mount, 숨은 데이터·설정 전달을 금지한다.
3. controller_core 및 install_pins 본문,34 pins, 모델/runner/출력/선택정책/
   자원/cleanup 계약은 그대로 둔다. 새 경로에 필요한 prefix 변경만 별도
   placement diff로 구분한다. 새로운 추상화나 installer 재작성은 하지 않는다.

허용 검증과 실행 경계:
- 기존 SDK1.6.0 재사용. 설치/취득/로그인/계정 조회 없음.
- RPC를 차단한 로컬 SDK import·builder 정의/의존성 구성·mount 파일 목록
  추출만 허용한다. 생성/전송/build를 호출하지 않는다. 인증정보를 읽거나
  출력하지 않는다. 구성 과정에서 RPC가 필요하면 진행하지 않는다.
- 실제 SDK 구성 경로를 검사한다. 외부 RPC를 막는 대역은 가능하나
  검증 대상 source-discovery/mount/function 처리 자체를 대역화하지 않는다.
- SDK가 고른 정확한 controller_core.py 바이트만 임시 격리 폴더에 배치.
  원본 폴더를 sys.path/CWD로 보완하지 않은 새 프로세스에서 해당 module과
  install_pins의 import/식별을 확인한다. top-level 전이 import도 확인한다.
  pip/subprocess 설치 명령과 install_pins 본문은 실행 금지.
- 원래 include_source=False의 목록 누락, 파일 없는 격리 import 실패,
  수정 후 정확한 단일 파일 import 성공을 구분한다. 임의 파일·경로·hash
  불일치 및 예상 밖 source 포함을 PASS로 처리하지 않는다.
- 실패 재현은 기대된 음성 검사로 기록. 예상 밖 실패는 보존하고 같은
  로컬 범위 안에서만 수정 가능. 최대2cycle/검사 누적120초/전체45분.
  과거39/15/14 suite, 과학 fixture, 성공 검사 묶음은 반복하지 않는다.
  필요한 subprocess는 시간 제한 및 Windows 숨김 실행을 사용한다.

종료 조건:
- 실제 SDK source 전달 목록·module/function identity·격리 import·최소 diff가
  모두 맞으면 LOCAL_BUILDER_SOURCE_CONTRACT_PASS. 실제 원격 import/build,
  Linux image/H100/900초/효과/release PASS로 확대하지 않는다.
- 불일치·미구현·범위/시간 초과면 정확한 누락 조건을 남기고 STOP.
  대체 배포 구조/다른 pins/원격 시도/새 수리 작업으로 자동 전환하지 않는다.
- 주력 1개. 예비는 실패 보존·closeout뿐. 어느 결과든 S0로 반환한다.

산출물:
closeout.md, verification.json, source.diff/placement.diff, 새 source manifest,
SDK builder 함수·mount 목록과 import 근거, 로컬 회귀 결과·시간,
기존 기록 보존 확인, exposure 및 cost-time 기록, s0-handoff.ko.md.
간결하게 작성하며 동일 내용을 여러 문서에 반복하지 않아도 된다.
status/log에는 결과와 S0 반환만 추가. tree와 기존 연구 파일은 보존한다.

비용·역사:
S1 준비/controller 누적9080.7295157초, 과학4process/1077.3504532초를 분리 승계.
이번 로컬 시간만 추가하고 과거 worker/cleanup을 중복 합산하지 않는다.
USD1/5는 누적 계획, cash0; account/billing 재조회 없음. 기존 summary0,
component0.00001152와 미게시/귀속 불확실성 유지. 관리값0.6502900821875501은
0.65 여유분 포함, 실청구 아님. 엄밀한 과금 보장/재로그인/공급사 문의를
이번 수리의 새 전제로 만들지 않는다. 원격 reference/candidate 실행0 유지.

금지:
실제/가짜 응답·112 payload·checkpoint·Parquet·NPZ·키·기존 cache/VAF 접근이나
재해시, 모델 import/fit/predict/score, 설치 본문, RPC/원격 전송/build/Sandbox/
GPU, 기존 App 재조회/종료, ZIP/S2/S3/TEST 선택, commit/push, subagent 실행.
기존 종료 기록 STOPPED/task0 보존. 새 원격 자원은 만들지 않는다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039 별도 HOLD를 유지한다.
17999명/12339SSUID·집계 노출·A022 역할·E059 소비 oracle1918/1124,
selection2007/1130, 보호 audit2074/1177·calibration1866 유지.
A_half 비승격, A018 사용자 미확정, S3 중단, S2 후보 없음.
다음 원격 시도는 새 source를 검토한 별도 범위가 필요하다.
```
