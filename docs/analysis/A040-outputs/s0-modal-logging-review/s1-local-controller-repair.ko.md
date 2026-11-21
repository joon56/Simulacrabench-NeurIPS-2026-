# S1 — A040 로컬 UTF-8·종료 실행기 수리

```text
SimulacraBench / HSCC S1 — A040 로컬 실행기 수리 및 모델 없는 회귀 검증.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1; 기존 dirty 보존.

AGENTS → CLAUDE → status → log 최신3개 → workflow를 읽고 역할/범위를 보고한다.
docs/analysis/A040-outputs/s0-modal-logging-review/decision.md와
modal-full-path1-resume2/의 closeout.md, build-result.json, cost-policy.md,
cost-ledger.json, app-terminal.json, termination-receipt.json, verification.json,
entry.json, build_once.py, inspect_termination.py, artifact-manifest.json을 읽는다.
이 지시는 이 S1의 로컬 수리만 허용한다. 원격 재개/과학 실행 지시가 아니다.

목적:
cp949에서 U+2022 진행 로그가 실패한 경로와 cleanup 대기 문제를 로컬에서
검증 가능한 계약으로 고친다. 로그 오류는 확인됨; cleanup 경고의 내부 원인은
미확정이다. traceback/기존 SDK1.6.0 소스를 통해 원인을 좁히고 최소 수정한다.
계측 실패를 모델/H100/정책 실패로 해석하지 않는다.

허용 범위:
- 새 docs/analysis/A040-outputs/modal-controller-repair1/와 대응 tmp 아래에
  실행기 복사본·회귀·기록 작성. 원래 build_once/기록/manifest/latch는 보존한다.
- 기존 SDK1.6.0 설치 재사용. SDK 소스 읽기/로컬 import는 허용하지만 모든
  계정/네트워크 경로를 실행 전 차단 또는 가짜 transport로 치환한다.
  원래 모델/응답/checkpoint/112 staging 열람·해시·전송·역직렬화는 금지한다.
- python -X utf8 및 필요한 stdout/stderr·자식 환경·로그 파일 encoding을
  검토한다. 원래 cp949 실패를 모델 없는 작은 재현으로 확인한 뒤, 실제
  사용할 수정 launcher/출력 경로로 파이프와 파일 리다이렉션을 검증한다.
  U+2022/한글을 stdout/stderr에 출력하고 예외와 결과 기록이 끝까지 보존되는지
  확인한다. 문자 삭제/로그 숨김만으로 PASS하지 않는다.
- 수정 controller는 원격 호출을 가짜 transport로 대체하여 검증한다.
  일관된 async SDK 경로를 사용하고, cancellation gather/stop/query/전체
  cleanup의 대기를 유한하게 만든다. 필요하면 별도 프로세스 watchdog으로
  controller 수명까지 제한한다. 요청 재발행은 금지하고 owned ID만 처리한다.
- 검증 사례: 정상 완료, Unicode 로그 포함 예외, 취소가 즉시 끝나지 않는 task,
  stop timeout/실패, stop ACK 뒤 아직 running, terminal+task0 확인, 생성 응답
  유실/ID 미확정. stop ACK·클라이언트 종료만으로 remote stopped를 기록하지
  않는다. timeout 시 확인불가를 기록하고 실제 cleanup 대상 ID를 남긴다.
- cleanup 진입 전에 예외가 발생하는 경로도 검토한다. 중복 build/새 App을
  만들어 정리하려는 동작은 없어야 한다. 공개 async/private stub을 섞은 것이
  원인이라고 단정하지 말고 SDK 호출 일관성 근거를 남긴다.
- 최종 build recipe/34pins/모델/과학 정책은 바꾸지 않는다. launcher/출력/
  에러 기록·취소·종료 제어에 필요한 차이만 허용하고 diff로 설명한다.

예산과 실행:
사용자가 이 프롬프트를 전달한 시점부터 새 로컬 수리 작업<=30분.
로컬 회귀 subprocess 누적<=120초, 동시1. 모델 import/GPU/원격 비용 작업0.
재현용 예상 오류와 로컬 수리 후 필요한 회귀 반복은 이 한도 안에서 허용한다.
통과 후 같은 검증을 불필요하게 반복하지 않는다. 기존 모델 성공 suite나
Linux 전체 경계60초 예산을 이 로컬 회귀로 재실행/소진했다고 기록하지 않는다.
기존 active3312.1552137초와 새 로컬 수리 비용을 구분해 누적 기록한다.

금지:
실제 Modal 계정/RPC/빌드/이미지 조회·재사용/업로드/Sandbox/종료 요청,
재로그인/재설치/예산 API·설정 변경·공급사 문의, 보호 데이터/캐시 접근,
fit/predict/score/공식 release 검사/ZIP, commit/push/tree/S2/S3/TEST, 서브에이전트.
이미 stopped인 과거 App을 확인하려고 다시 원격 호출하지 않는다.

종료:
전체 로컬 계약 통과이면 LOCAL_CONTROLLER_CONTRACT_PASS로 S0 반환.
미완료/결함이면 정확한 실패 조건과 재현 증거를 기록하고 종료한다.
PASS여도 원격 종료 효과·이미지 성공·H100900초·실제 효과/release는 미검증이다.
수리 후 build retry를 자동 시작하지 않는다. 기존 base image는 metadata상
SUCCESS일 뿐이며 후속 별도 범위의 identity/status 확인 없이는 재사용하지 않는다.

산출물:
entry, 원인·미확정 분석, 수정 controller/launcher, source.diff와 원본/수정 해시,
가짜 transport 및 Unicode 회귀 결과(횟수/시간/네트워크 호출0 증거),
cleanup 상태 판독표, verification/closeout/s0-handoff, status/log 최소 갱신.
비용USD1/5는 계획·현금0인 변경 계약 유지; 과거 차단 사유를 부활시키지 않는다.
E041/E025·parked·모든 STOP/HOLD/노출·보호 audit/calibration·A_half 비승격,
A018 미확정/S3 중단/S2 후보 없음 유지.
```
