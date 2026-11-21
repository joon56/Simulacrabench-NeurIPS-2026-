# A040 S0 — 종료 확인 수용과 다음 생산 실행기 작업

2026-10-05 KST. S0 문서/허용 소스 검토. workflow2026-10-05-r5.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, dirty89, 관련 로컬 python/pythonw/uv jobs0.
workflow SHA256 a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
진입 지침의 앞선 실제 읽기를 승계하고 최신 status/log3개와 지정 자료를 읽었다.
근거 도구38aa85/8d2337/e8a9db/0f7584/29b68c. 이 S0는 SDK/RPC/수리 실행을 하지 않았다.

## 판정

**TERMINAL_CONFIRMED 수용. 기존 Sandbox 종료 확인 작업은 완료.**
계정 joon56/main, App ap-XiMVzlJgrNrCiFpIN1kB4W, 지정 이름과
sb-svFnVI39hH3DpUIZ4Z9LXK가 일치한다. exact-ID SandboxWait가
GENERIC_STATUS_TERMINATED를 반환했다. 관측2026-10-05 21:46:48.981408 KST.
플랫폼 목록의 종료시각은18:50:47.436434 KST다. 관측시각과 구분한다.
이미 종료된 자원이므로 이번 종료 요청0. App STOPPED/task0는 별도 보조 근거다.

실제 child1회5.7395758초, local checks1.1279815초. 남은 cleanup 허용량은 닫혔다.
이번 성공으로 로그인/종료 조회를 새 과제로 반복할 필요가 없다.
Workspace meteredUSD0.01009897/billedUSD0 관측을 수용하되, 최종 A040 귀속
비용/과거 GPU 사용시간은 미확정이다. 청구0·GPU0 또는 다른 자원 부재로 확대하지 않는다.
종료 자료8개가 saved manifest와 일치하며, 현재 생산12개 소스도 기존 manifest와 일치한다.

## 다음 판단과 우선순위

**주력은 생산 실행기의 SDK lifecycle 로컬 수리·통합 검증1개다.**
목표는 이미 등록된 고정 모델 경로를 실제 SDK로 안전하게 시작하고 회수·종료할
준비가 되는지 확인하는 것. 승리 가능성이나 점수 향상 증거가 생긴 것은 아니다.
하지만 이전 이미지 설치는 완료됐고 종료 조회의 실제 작동 경로도 생겼으므로,
동일한 학습 정책의 H100 전체 실행 가능성 측정을 막던 결함을 좁혀 해결할 가치가 있다.

소스상 남은 문제:
- live_launcher는 독립 asyncio loop로 raw SDK를 실행한다. Sandbox hydrate는
  SDK-managed loop를 요구하는 stream 객체를 생성한다. 실제 create/stream 경계가
  이전 로컬 endpoint 대역으로 가려졌다.
- cleanup은 handle 복구 실패 시 같은 경로를 재사용하고 App 상태 확인을 반복한다.
  방금 실제 동작한 metadata-only exact-ID 종료 확인 경로를 재사용해야 한다.
- sandbox_stage는 create가 반환된 뒤에만 GPU 시간 계수를 시작한다. create 응답/
  hydrate 실패 사이의 가능한 자원과 비용을 누락한다. 요청 전 intent/예약을 기록해야 한다.

현재 소스로 다시 H100을 만드는 선택은 알려진 결함을 반복한다.
새 실행 프레임워크/모델로 바꾸는 선택은 범위·비용이 커진다.
따라서 기존 과학 본문을 보존하는 한정된 수리를 우선한다.
누적 준비14777.0797748초가 들었으므로 또 작은 오류마다 작업을 나누지 않는다.
같은 S1에서 아래 관련 경계를 묶어 완료하고, 상한 내 불가하면 정확한 결함을 남긴다.
정당한 예비 작업은 그 제한된 closeout뿐이다. 원격 재시도는 이 과제에 포함하지 않는다.

## 같은 S1에 전달할 작업 지시

사용자가 이 문서의 작업을 S1에 지시할 때 아래 범위만 활성화된다.
S0의 작성이나 종료 확인 결과 자체는 실행 허가가 아니다.

역할 S1 기술 검증. AGENTS/CLAUDE/status/log 최신3개/workflow r5를 읽고
역할·개정·범위/금지를 보고한다. HEAD·dirty·관련 jobs를 확인하고 기존 변경을 보존한다.

입력:
- 이 문서
- docs/analysis/A040-outputs/termination-query-run2/closeout.md,
  attempt-01/terminal-evidence.json, attempt-01/receipt.json,
  final-terminal-billing.json, verification.json, cost-time-ledger.json
- docs/analysis/A040-outputs/termination-query-repair1/confirm_terminal.py,
  regression-history.md, test_entry.py
- docs/analysis/A040-outputs/local-preparation-repair2/의 생산12모듈,
  source-manifest.json 및 필요한 기존 계약 기록
- 기존 설치 SDK1.6.0의 관련 소스. 재설치/취득 불필요.

생산 source-manifest SHA256:
c782c99e29cfceeaba132018d48f2be2a844e7f8b51ba8840157f9ebfa845765.
종료 조회 helper SHA256:
0e68a80ce1237aaa0f95d42777a24154b5cee110858e0bf0a692c17a2d75939a.
HEAD만으로 dirty 소스를 식별하지 않는다. 허용 소스/문서만 hash 확인한다.

범위는 생산 orchestration의 loop/handle/stream/상태 복구/종료/시간·비용 기록이다.
새 production-lifecycle-repair1 폴더의 복사본에 작업하고 충돌 시 새 경로를 고른다.
필요한 orchestration 모듈의 최소 수정은 같은 세션에서 자율 수행한다.
파일이 여러 개에 걸친다는 이유만으로 다시 승인/인계를 만들지 않는다.
과학 runner·모델/seed/head/context/선택·guard/refit·900초 정책과 installer/pins는 보존한다.
경로 배치는 의미 변경과 구분하고, 설치 SDK를 패치하거나 assertion을 제거하지 않는다.

1. 생산 진입점을 일관된 SDK 관리 loop에 연결한다. plain async wrapper 등
   검증된 방식과 실제 설치 소스를 사용한다. 외부 RPC/인증만 대역화하고 실제 SDK
   create/recover의 handle hydration, StreamReader/Writer, filesystem/exec 반환 객체,
   launcher dispatch를 우회하지 않는다. 과학 명령은 기록만 하며 실행하지 않는다.
2. create intent/고유 이름/가능한2400초 자원 예약을 요청 전에 저장한다.
   handle 반환 전 실패도 자원0/비용0으로 기록하지 않는다. 계획 예약·관측 청구·
   실제 GPU 사용시간을 구분하며 기존 장부를 초기화하지 않는다.
3. handle이 없어도 metadata-only 경로로 정확한 ID/상태를 복구할 수 있게 한다.
   인증/timeout/retry/V1/V2 처리에는 방금 검증한 조회 경로를 재사용한다.
   결과가 불명확한 create를 중복 실행하지 않는다. exact-ID terminal을 먼저 보존하고,
   billing 실패나 App 상태 반복으로 그 증거를 잃지 않는다.
4. 같은 생산 진입/실행기를 실제 SDK와 연결한 새 영향 검사로 확인한다.
   정상 경로, create 응답 후 hydrate 실패, ID유실/복구 불가, timeout/cancel,
   stream 소비, reference 실패 시 candidate0, 중복 생성/종료 차단,
   terminal 확인 전 PASS 금지, billing 실패 시 terminal 보존을 포함한다.
   SDK 객체/stream 자체를 fake로 치환한 검사를 이 경계의 PASS로 쓰지 않는다.
   파일/프로세스 응답은 작은 고정 대역 bytes/metadata만 쓴다.
   placeholder []나 개수 metadata를 실제 예측189649개로 보고하지 않는다.
5. 실제 production CLI의 선택한 진입 경로도 인증/RPC를 차단한 채 확인한다.
   내부 함수만 검사하고 바깥 launcher/loop/import 경계를 미검증으로 남기지 않는다.
   새 fixture의 실제 대역 위치와 미검증 항목을 기록한다.

전체60분, 기록10분 확보. 새 영향 검사 합180초/각30초, CPU2/GPU0.
r5에 따라 오류는 이 상한 안에서 수정·검증하고 계속한다. 이전 성공15/39/14/6 suite,
tiny scientific fixture, 종료 조회는 반복하지 않는다. 실패 cycle과 변경 영향만 남긴다.
서로 다른 결함이 계속 드러나 상한 내 연결을 입증할 근거가 없으면 범위를 늘리지 않고
정확한 구조적 문제/수리 잔여를 closeout한다. 임시 증상 수정을 새 원격 시도로 시험하지 않는다.

산출물: 실제 읽기/entry·원인/최소 diff·변경/불변 소스 manifest·같은 실행기의
영향 회귀·시간/비용/노출 장부·verification·closeout·S0 인계·status/log.
완료 판정은 LOCAL_PRODUCTION_LIFECYCLE_PASS / REMOTE_MEASUREMENT_NOT_AUTHORIZED
또는 구체적인 미충족 조건이다. 실제 Linux/native 경계·H100900초·모델 효과·release는
여전히 다음 별도 실행에서 확인할 사항이다. 로컬 PASS 뒤 임의 원격 실행하지 않는다.

실제 인증/RPC/billing 재조회, 새 App/Image/Sandbox/build/H100, 원격 전송,
payload112/응답/키/Parquet/NPZ/checkpoint/cache/VAF 접근·재해시,
모델 import/fit/predict/score, ZIP/제출, commit/push/tree 수정, 서브에이전트·S2/S3 금지.
공개 SDK import와 새 가짜 transport/작은 고정 파일 검사는 위 로컬 범위에서만 허용한다.

과학4process/1077.3504532초와 준비14777.0797748초 승계; 겹친 시간은 한 번만 계산한다.
E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD/E058/E059/A039,
노출17999/12339·집계/A022 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단/S2 없음.
과거 종료 미확인 기록은 역사로 보존하며 현재 해소 상태와 구분한다.

S0 문서 검증: 종료 근거8개/생산 소스12개/workflow/tree 해시 불변.
status/log의 이번 추가를 제거하면 직전 UTF8 BOM/CRLF 바이트 해시가 복원된다.
새 문서 경로 확인 완료. 위 판단 검토를 위한 실행/과학 테스트는 수행하지 않았다.

