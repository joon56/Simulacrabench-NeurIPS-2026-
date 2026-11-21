# S1 제목: A040 — 보완된 고정 실행기의 Modal H100 단일 측정

아래 본문을 기존 S1에 사용자 지시로 전달한다. S0의 문서 작성 자체는 실행이 아니다.

```text
SimulacraBench / HSCC S1 기술 측정.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
이번 사용자 전달은 아래 새 bounded 원격 시도1회를 지시한다.
S0/S2/제출 작업으로 전환하지 않는다. 서브에이전트 실행 금지.

AGENTS → CLAUDE → status → log 최신3개 → workflow.md를 읽고 역할/개정/범위,
읽기 근거·workflow 해시·HEAD/dirty/관련 jobs를 entry에 기록한다.
기존 사용자 변경·실패/PASS·manifest/latch/STOP/HOLD 보존.

입력:
docs/analysis/A040-outputs/s0-modal-output-review/decision.md
docs/analysis/A040-outputs/modal-output-contract-repair1/의 closeout.md,
producer-consumer-contract.md, verification.json, source/placement.diff,
source-manifest.json, contract-manifest.json, cost-time-ledger.json 및12개 source.
modal-local-integration1의 phase-evidence.md/계약·미검증 목록도 승계한다.
modal-full-path1/allowlist.json, full-path-resume1/requirements.lock.txt,
modal-full-path1-resume2/termination-receipt.json 및 누적 cost ledger를 읽는다.
모두 docs/analysis/A040-outputs/ 아래다. 과거 실행 프롬프트를 재사용하지 않는다.

고정 실행 소스 폴더: docs/analysis/A040-outputs/modal-output-contract-repair1/
source-manifest SHA256:
0060ed98fc7e3c9ecc5625bd24f5c276971b026817dbb06c92fc2744dec83815
linux_runner SHA256:
82facf9151daa8eadc55c438be99f4c0cf5e331978c18b3a59530ef2af5b680e
manifest와12개 소스 identity 확인. 변경 발견 시 경위를 기록하고 중단한다.
소스 수정·다른 복사본으로 대체·이전 snapshot 되돌리기 금지.

새 설정/산출물:
docs/analysis/A040-outputs/modal-full-path1-resume4/
tmp/a040-modal-full-path1-resume4/
충돌 먼저 확인, 존재하면 새 고유 suffix를 entry에 고정한다. 코드 위치와
config/output/launcher 디렉터리를 구분한다. 기존 코드 폴더에 결과 덮어쓰기 금지.
새 고유 App/Sandbox 이름, 새 absolute UTC deadlines, LIVE plan과 이번 사용자
지시를 연결한다. boolean execution_authorized 자체가 사용자 권한을 대체하지 않는다.

목적:
로컬 연결/출력 계약의 PASS를 실제 image/Linux/H100 경로로 측정한다.
정책·입력·평가 범위를 고정한 기술 검증이다. 실제 ERPIS 효과 검증이 아니다.
같은 로컬 suite를 반복하지 말고, gate가 통과하면 같은 S1에서 다음 단계로 간다.

단계1 — 원격 요청 전 설정 동결:
기존 SDK1.6.0·인증 재사용. 성공39/15/14 suite·tiny/schema fixture 재실행 금지.
새 config의 경로/allowlist/source/시간·자원 한도 정적 검증만 수행한다.
필요한 모델 없는 config 검증 누적60초 이내; 모델 import/RPC 없이 실시한다.
새 실행 모듈·미완성 코드·policy 변경이 필요하면 중단한다. 새 수리 범위 아님.
live_launcher.py와 그12개 고정 모듈을 그대로 사용한다. launcher는 숨겨진
프로세스로 시작하고 UTF-8 stdout/stderr·PID·실행 intent를 남긴다.

단계2 — 단일 준비:
정상 SDK로 workspace joon56/main 및 정상 billing metadata를 확인한다.
기존 사용자 보고 credits30/spend0/usage30과 독립 관측을 구분한다.
예산 API PermissionDenied를 반복하지 않고, 실제 인증 만료가 없으면 로그인/
재설치 요청도 반복하지 않는다. 계정/결제/usage/spend 설정 변경 금지.
관측된 현금청구·계정 불일치 등 실제 모순이 있으면 중단한다.

기존 base im-eWgRNij0VH6mzozlOzEyxy는 저장된 result identity와 현 상태를
읽기 확인한 뒤 base로만 재사용한다. 과거 SUCCESS를 현재 확인으로 대신하거나
완성 dependency image로 취급하지 않는다. identity 불일치 시 대체 base 탐색 금지.
새 App/image recipe build 요청 최대1회; installer600초/image build900초 한도.
기존 Python3.13.14/34 pins 유지. 실제 Linux lock/image/driver 식별 기록.
force build·오류 후 재빌드·pin 교체·자동 추가 설치 시도 금지.

원격 전송은 기존 allowlist112개/145542095bytes와 명시한12개 고정 코드만.
이 단계에 한해 allowlist의 기존 fake3·공개 checkpoint·공개 소스 바이트 확인/
해시/전송을 허용한다. 전송 직전 재대조, 신규 원격 target contract도 고정한다.
소스 extra prefix는 docs/analysis/A040-outputs/modal-output-contract-repair1/.
원래 output temp는 /work/tmp/a040-modal-local-integration1 그대로 둔다.
새 Sandbox이므로 옛 실제 출력 재사용은 없다. root/HOME/credentials/실제 응답/
키/Parquet/NPZ/기존model cache/VAF/옛 예측 배열 읽기·해시·전송 금지.
전송·기본 검증이 끝나기 전 과학 실행으로 진행하지 않는다.

단계3 — 실제 경계 및 고정 비교:
H100!1개, cpu(1,1) physical/two logical threads, RAM15258MiB=15999172608bytes,
swap0/native block_network/gVisor/no secrets/no OIDC. 새 Sandbox1개2400초 이내.
CPU quota·affinity·Linux cgroup/RSS/private를 기록하고 Windows commitment와
같다고 쓰지 않는다. 모델 import 전 고정 Linux boundary1회/60초.
native probe·자원·pin·payload·중복 방지 gate 미충족/관측 불가면 STOP.
한도나 probe를 현 환경에 맞춰 즉석 완화하지 않는다.

경계 통과 후 새 target reference1회900초, 통과 시 candidate1회900초.
각900초는 import/load/전처리/all3/검증/출력 포함. 기준도 새 target에서 측정.
기존 가짜 입력3개, 모델/context/head/seed/alpha/guard/floor/refit 정책 불변.
전체213heads/189649vectors, controls/final E041/inactive/fallback parity,
shadow/S→freeze→E guard→원래 final/engineering alpha.25 경로·state hash,
원래 call counts 및 checkpoint load 계약을 그대로 검증한다.
출력 key/count는 unicef17856/world_bank39520/unhcr132273.
candidate extra2개는 hashes/files에만 포함. 같은 target reference와 비교하며
RTX와 H100의 bit equality를 새 조건으로 만들지 않는다.
성공해도 S2/release/실제 효과로 자동 승격하지 않는다.

시간·비용:
새 전체 active120분, 준비<=60분, GPU수명<=40분, export/cleanup/closeout20분 확보.
시작 시 새 deadlines 고정, 각 단계에 필요한 전체 남은 시간 없으면 진입하지
않는다. 예전 남은 시간·latch·부분 상태는 재사용하지 않는다.
준비/controller 누적8319.0316208초와 과학4process/1077.3504532초 분리 승계.
고정 코드의 옛 historical_active_seconds 필드는 과거 값이다. 이번 session
ledger에 현재 누적값을 명시하고 옛 필드를 새 누적값으로 보고하지 않는다.

USD1 준비/USD5 총액은 이전 시도 포함 모니터링 계획, 현금 권한0.
엄밀한 최종 청구 상한 증명/공급사 문의로 되돌리지 않는다. 이전 summary0/
component0.00001152USD와 미게시 비용·귀속 미확정 승계, 장부 초기화 금지.
현재 정상 billing과 자원시간 추정 중 보수적인 관리값을 사용하되 중복 합산
금지. 신규 단계 전 누적 관리값+다음 전체 단계 계획<USD4, USD4면 정리 전환,
약USD1 종료 여유. 가격 가정이 달라졌다면 공식 근거로 계획만 갱신하고 기존
예산 내에서만 진행한다. 실제 비용·계획 여유분·불확실 항목을 구분한다.
사후 게시액 초과 가능성을0으로 숨기지 않고 현금0 보장을 주장하지 않는다.

중단·종료:
첫 실제 준비/경계/과학 오류·timeout·identity/자원/비용 모순이면 STOP.
소스 수정·두 번째 build/과학 호출·deadline 연장·부분 예측 이어붙이기 금지.
백업은 진단 export·소유 자원 정리·closeout뿐. 새 과학 allowance 생성 금지.
Sandbox 종료와 App 명시STOPPED/task0 및 Sandbox terminal을 확인한다.
stop ACK/exit0/client 종료만으로 원격 종료를 주장하지 않는다.
상위 watchdog 강제종료 시 정확히 기록된 owned ID/고유 intent에 한해
bounded cleanup-only SDK/CLI 종료·읽기 조회를 허용한다. 전체60초 정리 시도와
별도 결과를 기록; 재시작/create/build 금지. 미확인 상태면 UNCONFIRMED로 남기고
즉시 ID·남은 조치를 사용자에게 알린다. 타인/다른 작업 자원 종료 금지.

산출물:
entry/권한·읽기 receipt, config/소스/입력/전송 freeze, image·Linux lock/자원
identity, boundary 결과, reference/candidate 결과/events/resources/출력 hashes,
실패 시 partial와 미실행 단계, 누적 cost/time ledger, termination receipt,
preservation verification, closeout, s0-handoff.ko.md 및 status/log 갱신.
H100 전체 기술 PASS/측정된 자원 실패/플랫폼 준비 실패를 구분한다.
S0 검토로 반환한다. ZIP/checker/official scorer/E025-E041 release 비교,
업로드/새E/commit/push/tree/S2/S3/TEST는 이번 범위 밖이다.
E041 incumbent/E025 fallback, E057/E060/E061 parked, 과학STOP/HOLD/E058/E059/A039,
17999/12339·집계·A022 역할·E059 소비oracle1918/1124·selection2007/1130와 보호
audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단/S2 없음.
```
