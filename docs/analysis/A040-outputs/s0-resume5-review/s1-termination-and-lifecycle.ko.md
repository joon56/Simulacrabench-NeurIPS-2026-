# 다음 S1 — 기존 Sandbox 종료 확인과 실제 SDK lifecycle 로컬 수리

이 프롬프트를 사용자가 S1에 전달해 작업을 지시할 때 아래 범위만 활성화한다.
S0 작성 자체는 실행 허가가 아니다. 이전 resume5 허가는 소비됐으며 되살리지 않는다.

작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1
역할: S1 기술 작업. S0 판단이나 S2 제작을 대신하지 않는다.

## 시작·근거

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md를 실제 읽고 개정·역할·허용/금지 범위를 보고한다.
HEAD·dirty files·관련 active jobs를 확인하며 기존 변경을 보존한다.
워크플로 읽기 증거와 SHA256을 entry.json에 기록한다.

다음을 읽는다:
- docs/analysis/A040-outputs/s0-resume5-review/{decision.md,verification.json}
- docs/analysis/A040-outputs/modal-full-path1-resume5/closeout.md,
  verification.json, failure-analysis.md, run/termination-receipt.json,
  run/result.json, session-cost-time-ledger.json, builder-evidence.json
- docs/analysis/A040-outputs/local-preparation-repair2/source-manifest.json,
  live_binding.py, sdk_endpoint.py, live_worker.py, live_launcher.py
- 기존 설치 SDK1.6.0의 관련 sandbox/io_streams/클라이언트 소스

원본 source-manifest SHA256:
c782c99e29cfceeaba132018d48f2be2a844e7f8b51ba8840157f9ebfa845765.
HEAD만으로 dirty 소스를 식별하지 않는다. 허용 문서·소스 해시만 확인한다.
과거 manifest에 맞춰 파일을 되돌리지 않는다. payload112/pins 원본은 재해시하지 않는다.

## 목적·기존 작업과의 차이

resume5는 builder 완료 뒤 실제 StreamReader loop assertion에서 실패했다.
과거 로컬 대역 검사는 실제 SDK handle/stream 생성을 통과하지 않았다.
이번에는 먼저 그 시도의 종료 증거를 확보하고, 종료가 확인되면 실제 SDK
hydrate/stream/cancel/recover 경로를 외부 RPC 대역과 연결해 로컬 검증한다.
새 모델 가설·H100 성능·실제 효과를 검증하는 작업이 아니다.

## 1단계 — 기존 자원 조회·필요한 종료만

대상은 workspace joon56 / environment main의 아래 기존 자원이다:
- App: ap-XiMVzlJgrNrCiFpIN1kB4W
- App name: a040-resume5-20261005-094405
- Sandbox name: a040-resume5-20261005-094405-gpu
- Sandbox ID: 미확인
- App STOPPED/task0는 과거 관측; Sandbox terminal UNCONFIRMED.
- 사용자도 종료를 확인하지 못했다. 새 계정 권한·slot 확인으로 확대하지 않는다.

SDK/인증 재사용. 재설치·재로그인·결제/예산 설정 변경·문의 발송 금지.
정상 인증 경로가 내부적으로 프로필을 사용하는 것은 허용하되, 인증 파일을
수동 열람하거나 토큰/비밀값을 출력·저장하지 않는다.

원격 작업 총120초, 각 호출 최대15초. 마지막30초는 종료 증거/장부 기록에
배정한다. 새 deadline과 호출 내역을 사전 기록하고 초과 시 중단한다.
허용은 대상 identity/status 조회, 필요한 단일 종료 요청, terminal 확인,
정상 workspace billing 요약 조회뿐이다. 새 App/Image/Sandbox/build 요청,
원격 명령·파일 읽기·전송·설치는0이어야 한다.

실패했던 독립 raw asyncio loop의 handle 복구를 그대로 재실행하지 않는다.
설치 SDK 소스로 실제 호출 형태를 확인한 뒤, 일관된 정상 public sync 경로
또는 SDK 관리 loop를 사용한다. 필요하면 StreamReader를 만들지 않는 metadata
RPC로 정확한 ID·finished result를 조회한다. SandboxGetFromName/SandboxList/
SandboxWait/SandboxTerminate 등 실제 protobuf 필드·결과 상수를 소스로 확인한다.
list의 기본 running-only와 finished 포함 조회를 구분한다. 임의 CLI 명령 금지.

이름·app/workspace/environment가 맞는 자원만 종료한다. 살아 있으면 해당
Sandbox만 종료 요청1회 후 명시적 terminal result를 확인한다. 다른 작업·App
일괄 종료 금지. 이미 확인된 과거 App을 불필요하게 반복 stop하지 않는다.
ACK·App task0·NotFound·active-list 누락·timeout 경과만으로 terminal을 만들지 않는다.
과거 finished 결과나 정확한 자원의 공식 화면 증거가 없으면 UNCONFIRMED다.

UTC/KST 확인 시각·출처·ID·종료 요청·terminal·billing을 별도 receipt에 기록한다.
비용 workspace 집계/게시 지연/귀속 미확정은 그대로 남긴다. GPU timer 미시작을
사용0으로 쓰지 않는다. 과거2400초 예약은 계획이며 실제 청구로 바꾸지 않는다.

terminal을 확인하지 못하면 여기서 STOP. 필요 화면/정확한 자원/사용자 조치만
명시하고 S0로 반환한다. 추가 원격 호출·2단계 수리·새 실행은 하지 않는다.
terminal이 확인되면 final billing의 게시/귀속 미확정만으로 자원0 로컬 수리를
막지는 않는다. 그 불확실성은 유지하며 새 유료 실행을 허가하지 않는다.

## 2단계 — terminal 확인 시에만 로컬 수리

전체 세션60분 이내, 종료 기록10분 확보. 집중 검사 wall 합180초,
각 process30초, CPU2/GPU0. RPC/auth/install/model/GPU 경로는 차단한다.
Windows 소유 loop/socketpair IPC는 허용하며 외부 네트워크와 구분한다.
회귀의 fake endpoint 호출은 실제 원격 RPC와 별도 계수한다.

새 docs/analysis/A040-outputs/sandbox-lifecycle-repair1/에 복사본을 만든다.
충돌 시 새 경로를 고르고 원본·기존 실패/latch/manifest를 보존한다.
수리 범위: 실제 SDK loop binding, create/recover/stream 연결, 중복 방지,
bounded cleanup/terminal 처리, 생성 전 비용 예약/시간 계수와 필요한 placement.
installer/controller_core와 linux_runner/과학 본문·34pins·모델·seed·context·head·
alpha·guard/refit·timeout 정책은 변경하지 않는다. 설치 SDK 패치/assertion 제거 금지.

외부 protobuf endpoint만 대역화한다. SDK hydrate/StreamReader/StreamWriter 자체를
가짜로 바꾸지 않는다. 실제 설치 SDK로 원래 loop 오류를 먼저 재현하고,
같은 생산 실행기로 수정 경계를 확인한다:
- create 응답→ID/handle→stdout/stderr reader·stdin writer 경로
- create 응답 후 hydrate 실패/ID 미보존 시 exact-name metadata recovery
- 미지정/실패/불일치 결과, 취소·timeout·terminal 미확인
- create intent/가능 비용 예약을 요청 전에 기록; 실패해도 자원0으로 세지 않음
- 불확실한 create 결과에서 중복 생성0, science0, 자동 재시도0
- Sandbox terminal과 App STOPPED/task0를 분리; cleanup 소진 전 증거 저장

수리·새 영향 검사의 수정은 같은 로컬 시간 범위에서 허용한다. 실패 cycle과
diff를 모두 보존한다. 기존 성공15/39/14/6 suite·tiny scientific fixture 재실행 금지.
최소 변경으로 해당 실제 SDK 경계를 입증할 수 없으면 범위를 늘리지 않고 종료한다.
새 manifest에는 정확한 생산 소스와 대역 범위·남은 실제 원격 미검증을 구분한다.

## 종료 조건·산출물

종료 조건: 시간/검사 한도, terminal 미확인, 실제 금지 동작 발생, 또는 명명된
로컬 계약 증거 확보. 로컬 PASS여도 원격 빌드/과학/S2로 자동 전환하지 않는다.
완료 판정은 LOCAL_SANDBOX_LIFECYCLE_CONTRACT_PASS /
REMOTE_MEASUREMENT_NOT_AUTHORIZED 또는 정확한 미충족 조건이다.

산출물: entry/read receipt, 종료·billing receipt, 원인/계약, 원본 재현·영향 회귀,
source/placement diff와 manifest, 비용/시간/노출 장부, verification, closeout,
s0-handoff.ko.md, status/log 갱신. 배열 대신 최소 metadata만 기록한다.
누적 준비11874.4328804초와 과학4process/1077.3504532초 승계. 겹친 시간을 더하지 않는다.
USD1/5는 누적 계획·cash0, 기존 비용/예약/미게시 귀속 불확실성을 초기화하지 않는다.

금지: 새 자원/build/H100·원격 과학 명령, 기존 partial 상태 재개,
응답/키/Parquet/NPZ/cache/VAF·payload112 접근/재해시/전송, checkpoint import/load,
fit/predict/score, 새 E/후보, ZIP/checker/all3/업로드, 유료 설정 변경·연락,
commit/push/tree 수정, 서브에이전트·S2/S3·TEST 선택.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD와
E058 STOP/E059 STOP_SELECTION/A039 HOLD 유지. 노출17999명/12339SSUID·집계,
A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130 및 보호
audit2074/1177·calibration1866 유지. A_half 비승격, A018 미확정/S3 중단/S2 후보 없음.

