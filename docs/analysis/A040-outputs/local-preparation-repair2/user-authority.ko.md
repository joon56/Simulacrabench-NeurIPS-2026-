# S1 — A040 로컬 준비 경계 재설계와 builder source 검증

사용자가 이 프롬프트를 S1에 전달하면 아래 로컬 작업을 수행한다.
이 S0에서 작성했다는 이유로 실행하거나 원격 실행 권한을 만들지 않는다.

```text
SimulacraBench / HSCC S1 — A040 로컬 준비 작업을 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1
이번은 기술 검증. UNHCR 답변 없이 진행하며 VAF 응답은 사용하지 않는다.

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md를
순서대로 읽고 실제 역할/개정/SHA256/읽기 근거/범위를 기록한다.
HEAD·dirty·로컬 active jobs 확인. 기존 변경·실패·latch·manifest를 보존한다.

입력:
- docs/analysis/A040-outputs/s0-no-reply-plan/decision.md
- docs/analysis/A040-outputs/modal-builder-source-repair1/의 closeout.md,
  verification.json, check_builder_source.py, run_local.ps1, baseline-result.json,
  cycle2-baseline-stderr.txt, source-manifest.json, cost-time-ledger.json
- docs/analysis/A040-outputs/modal-full-path1-resume4/의 failure-analysis.md,
  builder-stdout.txt, termination-receipt.json, config-source-input-freeze.json
- 기존 SDK: tmp/a040-modal-full-path1/sdk-venv
  modal/_image.py, _functions.py, _utils/function_utils.py, _utils/async_utils.py,
  synchronicity/synchronizer.py 및 async_utils.py, 필요한 stdlib/SDK source.

미검증 복사본 manifest SHA256:
33adec1d4cb7559e77b5891ec9975cb33ec4bbdba04c67bd84116639f162182a
controller_core.py SHA256:
fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb
현재12개 production source는 원본과 동일하다. repaired candidate로 부르지 않는다.

목적:
실제 SDK가 installer defining module을 builder에 전달하는 구성인지 검증한다.
Windows asyncio IPC를 전면 차단했던 검사 도구를 먼저 바로잡는다. SDK는
Windows loop policy를 바꾸며 synchronicity 스레드에서도 루프를 만들 수 있다.
첫 루프만 예외 처리하거나 같은 실패 스크립트를 다시 실행하지 않는다.

새 허용 범위와 종료 예산:
- 새 docs/analysis/A040-outputs/local-preparation-repair2 및 대응 tmp 폴더.
  경로 충돌 시 미사용 경로를 선택. 기존 폴더/스크립트/latch 수정 금지.
- 총60분 wall, 마지막10분은 종료 기록. 새 검사 프로세스 wall 합계180초,
  각30초 이하, CPU 최대2/GPU0. 모든 실패·시간·프로세스를 기록한다.
- 범위 안의 launcher/검사 도구 오류는 원인을 확인한 뒤 같은 S1에서 수정하고
  영향 검사만 반복할 수 있다. 사소한 준비 오류마다 S0로 돌아가지 않는다.
  기존2회 기록은 소비 상태 유지. 이번은 새 설계에 대한 별도 예산이며
  과학 실행 allowance를 소비하거나 늘리지 않는다. SDK 재설치/취득 없음.
- Python 경로·기반 interpreter 접근은 모델 없는 짧은 진입 확인으로 먼저
  점검한다. 실제 access denial 시 정상 도구 승인 경로만 사용한다. 대체 계정,
  ACL 변경이나 자동 승인 거절 우회 금지. 환경 확인도 총시간에 포함한다.

수행:
1. 필요한12개 production source를 새 위치에 복사하고 identity를 확인한다.
   기존 검사 소스는 참고하되 새 경계 설계를 짧게 기록한 후 실행한다.
   credential 환경값은 출력하지 않고 제거, 빈 별도 Modal config 경로 사용.
   실제 사용자 config/토큰 파일 접근을 막는다.
2. 표준 라이브러리 이벤트 루프가 만드는 자기 socketpair의 로컬 IPC만 허용.
   생성 경로·프로세스 소유·수명을 확인 가능한 좁은 허용으로 구현한다.
   모든 loopback 통신을 풀거나 SDK 작업 뒤에 차단을 설치하지 않는다.
   동기/비동기 SDK 경로에서 필요한 추가 스레드 루프도 검증한다.
3. 실제 client 취득/인증·transport RPC·remote image resolution/build,
   external connect/DNS, installer/pip/예상 밖 subprocess는 별도로 차단한다.
   음성 검사는 dummy 인자로 차단 지점까지만 호출하며 실제 네트워크·실제
   토큰·실제 설치를 시도하지 않는다. SDK source 탐색/FunctionSourceInfo/
   mount 구성 자체는 대역으로 바꾸지 않는다. native/OS egress 증명은 아님.
4. 위 경계 확인 후 실제 SDK가 구성한 builder 함수와 spec/dependency mount
   목록을 얻는다. include_source=False의 project source 누락과 빈 격리
   디렉터리의 module import 실패를 재현한다. loader를 호출해 원격 resolve나
   전송으로 넘어가지 않는다. SDK 기본 client mount와 프로젝트 파일 분리.
5. 새 sdk_endpoint의 defining-source 전달만 최소 수정한다. 우선 후보는
   include_source=True. 실제 FILE 분류와 controller_core.py 하나만 선택됨,
   /root/controller_core.py 및 module/function identity가 일치함을 확인한다.
   PACKAGE/추가 프로젝트 파일/암묵적 루트 mount는 허용하지 않는다.
6. 정확한 선택 바이트만 staging해 새 격리 프로세스에서 import한다.
   원본 디렉터리를 CWD/sys.path로 보완하지 않는다. installer 본문은 실행하지
   않고 함수 식별/파일 hash/전이 import를 확인한다. 누락·추가·잘못된 경로·
   hash는 거절해야 한다. 원래 문제를 가리는 가짜 build PASS는 사용하지 않는다.

변경 제한:
production 의미 변경은 source 전달 flag뿐. 새 prefix 연결은 placement diff로
분리한다. controller_core/installer 본문,34 pins, linux_runner, 모델·정책·
출력·선택/guard·deadline/remote lifecycle은 보존한다. 실제 SDK 사용 형태의
검사 도구 오류는 이 범위에서 고칠 수 있으나 SDK 설치 파일을 수정하지 않는다.
과거15/39/14 suite 전체나 과학 fixture를 재실행하지 않는다. 신규 검사가
통과하면 불필요한 확대·반복을 중단한다. 새 배포 프레임워크를 만들지 않는다.
subprocess는 숨김 창·timeout·자기 process tree 종료·잔여 확인을 사용한다.

즉시 중단:
예상 밖 실제 인증/서비스 요청/installer/모델 실행/보호 자료 접근 시도,
프로젝트 파일의 범위 밖 포함, 범위 밖 production 수정 필요, 예산 소진.
의도한 음성 검사가 금지 동작 전에 정상 차단되는 것은 성공 관측이다.
문제가 있는 guard를 제거하고 PASS시키거나 한도를 늘리지 않는다.

성공 조건:
로컬 IPC 경로 정상, 인증/RPC/설치/외부연결 음성 검사 차단,
실제 SDK 단일 파일 전달 구성 및 원본 누락 재현, 정확한 격리 import,
고정 science/pins/source 보존. 모두 확인되면
LOCAL_BUILDER_SOURCE_CONTRACT_PASS / REMOTE_NOT_AUTHORIZED.
일부만 확인되면 구체적 미완료 조건을 기록하고 STOP. 실제 Linux/build/H100/
900초/ERPIS 효과/S2 release PASS로 확대하지 않는다. 어느 결과든 S0로 반환.

산출물:
closeout.md, 짧은 경계 설계와 검증 결과, diff/placement diff, 새 source manifest,
실제 SDK builder/mount 식별·격리 import 근거, 전후 보존·노출·시간 기록,
s0-handoff.ko.md. 간결하게 묶어도 된다. status/log만 현재 결과 추가.
다음 원격 scope의 검토에 필요한 source identity는 제공하되 실행하지 않는다.

절대 범위 밖:
112 payload·checkpoint·실제/기존 fake 응답·Parquet·NPZ·키·cache·VAF 열람/재해시,
모델 import/fit/predict/score, 웹/다운로드/설치/계정/청구 조회, 원격 build/전송/
Sandbox/H100, 기존 App 재조회/종료, ZIP/제출/S2/S3/TEST 선택, commit/push,
docs/tree.md·기존 연구 파일 수정, 서브에이전트 실행.

누적 준비9685.2829087초와 과학4process/1077.3504532초를 분리 승계.
이번 준비 시간만 더하고 검사 시간을 중복 합산하지 않는다. 원격비용 신규0인
범위이며 과거 billing0/component0.00001152와 미게시/귀속 불확실성은 유지.
USD1/5는 기존 계획, cash0. 계정 한도·주최측 정책을 다시 문제 삼지 않는다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039 HOLD 유지. VAF 의미를 추정해 대체하지 않는다.
17999명/12339SSUID·집계·A022 역할·E059 소비 oracle1918/1124 및 selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격, A018 미확정,
S3 중단, S2 후보 없음. UNHCR 답변·추가 결제 없이 끝낼 수 있는 로컬 작업만 한다.
```
