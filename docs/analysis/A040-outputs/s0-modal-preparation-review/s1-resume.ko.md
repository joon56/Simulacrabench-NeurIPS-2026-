# S1 — A040 Modal 준비 재개, 조건 충족 시 원래 단일 검증

```text
기존 A040 Modal S1을 재개한다. 작업 폴더:
C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.

AGENTS → CLAUDE → status → log 최신3개 → workflow를 읽고 역할/범위를 보고한다.
docs/analysis/A040-outputs/s0-modal-preparation-review/decision.md 및
modal-full-path1/{closeout.md,verification.json,platform-contract.md,cost-ledger.json,
entry.json,allowlist.json,source-input-image-manifest.json,termination-receipt.json},
s0-modal-plan/s1-modal-full-path.ko.md를 읽는다. 기존 미커밋 변경 보존.

이 지시는 이 S1에서 기존 준비를 이어갈 권한이다. S0/S2 전환이 아니다.
원래 인계의 과학 정책·입력 경계·검증 항목·비용 상한은 그대로 적용한다.
SDK1.6.0과112파일 staging을 재사용한다. 재설치/입력 재생성/기존 성공 suite
재실행 금지. 전송 전 허용 목록의 현재 identity 확인은 필요 범위에서 수행한다.
modal-full-path1의 종료 기록/manifest/latch는 덮어쓰지 않는다.
새 docs/analysis/A040-outputs/modal-full-path1-resume1/와 대응 tmp 경로를 사용한다.

남은 작업은 둘이다.
1. 정상 사용자 인증과 계정 확인.
   사용자가 아직 로그인하지 않았다면 아래 명령을 PowerShell에서 실행하고
   브라우저에서 joon56 연결을 승인하도록 안내한다. 토큰은 요구하지 않는다.
   & 'C:\Users\USER\Desktop\SimulacraBench\tmp\a040-modal-full-path1\sdk-venv\Scripts\python.exe' -m modal setup
   완료 보고가 없다고 이미 된 것으로 취급하지 않는다. 정상 CLI로 확인하며
   기존 계정/크레딧/spend0/usage30 증거를 최소 출력으로 읽는다. 인증 실패,
   다른 workspace, 비용 조건 불일치면 원격 작업을 하지 않는다.
2. 전체 이미지 준비/build/전송/취소 비용을USD1 안에서 통제하는 절차 완성.
   이는 에이전트 담당이다. 로그인 대기 중에도 허용 SDK 소스/공식 문서로
   진행 가능하다. 이미 확인한 Sandbox cap 조사를 반복하지 말고 미해결인
   builder/pull/layers/retry/cancel/cleanup 범위에 집중한다.
   준비40분 중 이 미해결 설계에 최대20분. 해결되면 남은 시간으로 구현한다.
   가격·자원 상한·전체 작업 시간·취소 후 잔여 비용·여유분을 연결한 계산과
   제어 절차를 원격 요청 전에 기록한다. 한 단계 timeout이나 빠를 것이라는
   기대를 전체 비용 보장으로 쓰지 않는다. 예산/계정 한도 상향은 금지한다.

이번 재개는 준비<=40분/전체<=100분. 이전1169.2559841초를 누적 기록한다.
활성화 시 새 절대 deadline을 기록하고 과거 deadline을 수정하지 않는다.
세션 사이 대기와 실제 작업 시간을 구분한다. 비용은 과거 시도와 합쳐USD5
credits/USD0 cash, 준비USD1/종료·기타USD1 여유. 비용 ledger를 초기화하지 않는다.
과학 실행 여전히 reference1회/candidate1회 각900초, H100!1개<=2400초,
새 모델 없는 경계검증 총60초. 전 회차는 과학/경계/원격 모두0회였음.

로그인과 비용 통제가 확보되면 같은 S1에서 원래 허용된 Linux 이식·이미지/
source/input freeze·CPU/memory/offline/중복실행 경계 검증을 마무리한다.
전제 통과 뒤에만 원래 고정 reference/candidate 각1회를 실행한다.
이때 추가 S0 확인을 반복 요구하지 않는다. 원래900초/첫 오류 STOP·종료/
회수 규칙을 지킨다. 성공/실패 모두 정확한 remote ID와 종료·청구 증거 남긴다.
제어를 확보하지 못하면 BUILD_BUDGET_CONTROL_UNRESOLVED 등 정확한 부족
조건을 기록하고 반환한다. 로그인 대기는 AUTH_PENDING으로 별도 기록한다.
어느 경우에도 새 run, GPU 변경, 예산 상향, seed/context/head/guard 구제 금지.

산출물은 새 재개 entry, build-control 결정/근거, 갱신 cost-ledger, 원래 인계의
실제 완료 산출물, verification/closeout/s0-handoff와 status/log 최소 추가.
실행하지 못한 결과 파일을 PASS처럼 만들지 않는다. 모든 STOP/HOLD·노출·
보호 경계·E041/E025·parked 상태 유지. S2/ZIP/업로드/commit/push/tree/S3/TEST
선택 금지. 성공해도 S0 검토로 반환한다.
```
