# S1 제목: A040 — 실제 Modal 연결과 단일 H100 전체 경로 검증

아래 본문을 기존 S1에 사용자 지시로 전달한다. 문서 작성·열람만으로 실행 허가가
발생하지 않는다. S0는 실행하지 않았다.

```text
SimulacraBench / HSCC S1 기술 검증을 진행한다.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
이번 사용자 전달은 아래 범위의 새 단일 시도를 지시한다. S0/S2 전환은 아니다.

AGENTS → CLAUDE → status → log 최신3개 → workflow.md 순서로 읽고,
실제 개정·역할·범위와 workflow 해시를 entry에 기록한다. HEAD/dirty/관련 jobs
확인, 기존 변경 보존. 다른 세션·서브에이전트 자동 실행 금지.

필수 입력:
- docs/analysis/A040-outputs/s0-modal-controller-review/decision.md
- docs/analysis/A040-outputs/modal-controller-repair1/의 closeout.md,
  verification.json, diagnosis-and-contract.md, controller.py, launcher.py,
  source-hashes.json, cleanup-state-table.md, sdk-contract-result.json,
  artifact-manifest.json. 성공 suite는 기록만 참고, 재실행하지 않는다.
- docs/analysis/A040-outputs/modal-full-path1-resume2/의 cost-policy.md,
  cost-ledger.json, build-result.json, app-terminal.json, termination-receipt.json.
- docs/analysis/A040-outputs/modal-full-path1/의 platform-contract.md 및 staging
  allowlist; full-path-resume1/frozen-inputs/manifest.json과 기존 과학 계약.
  위 경로들은 모두 docs/analysis/A040-outputs/ 아래다.
허용 문서/소스 identity부터 확인한다. 과거 manifest로 현재 파일을 되돌리지 않는다.

목적·차이:
LOCAL_CONTROLLER_CONTRACT_PASS는 fake transport 계약이다. 이번에는 실제
SDK1.6.0 async binding과 운영용 deadline을 연결하고, 성공 시 한 이미지 준비와
고정 reference/candidate의 H100 전체 경로까지 완료한다. 새 모델 가설이나
실제 효과 실험이 아니다. 단계별 조건 충족 시 같은 S1에서 계속하며 다시 S0
승인을 구하느라 중단하지 않는다. 첫 실제 준비/경계/과학 오류는 STOP.

새 산출물/코드 위치:
docs/analysis/A040-outputs/modal-full-path1-resume3/
tmp/a040-modal-full-path1-resume3/
먼저 충돌 확인. 존재하면 덮어쓰지 말고 새 고유 suffix를 entry에 고정한다.
repair1 및 과거 실패 코드/manifest/latch/로그/제출물은 수정하지 않는다.
controller 원본 SHA256 d830545f9ced6778d51f095fff68fd692e648496ba089ffb47d46db0fd1695de
launcher 원본 SHA256 cf9b61ab363c52a3bd26cacf08fae0b098bdfc8b7215c28ec6ca4e1d64acbda6

1. 실제 연결 준비 — 원격 자원 생성 전
SDK/인증 재사용. 만료/실제 모순이 없는 한 재설치·로그인·예산 API 재조회·
공급사 문의를 반복하지 않는다. 주최측 runtime fitting 정책 해소도 승계한다.
새 live worker에서 실제 내부 async SDK의 클래스/메서드/await 형태와 하나의
event loop/client 연결을 확인한다. fake_worker나 INJECTED_LOCAL_ONLY 표기를
실제 작업으로 사용하지 않는다. 0.12/0.35/3초 시험용 기본값을 운영에 쓰지 않는다.
SDK import는 허용하되, 새 바인딩의 모델 없는 로컬 preflight는 RPC를 차단하고
누적60초 이내로 한정한다. 기존15-case/tiny/schema/fixture suite 반복 금지.
현재 실제 SDK가 맞지 않으면 import/호출 형태만 이식한다. 과학 소스 변경 금지.

단계별 timeout, build/installer deadline, 유한 cancel grace, stop/query deadline,
상위 watchdog을 실행 전 동결한다. cleanup 최대60초와 부모 grace를 별도 확보하고
전체 deadline 안에 포함한다. 기존600초 installer 한도 유지. 자식/helper의
소유권과 종료 범위를 기록; 자기 worker 종료를 원격 종료로 취급하지 않는다.
prepare/create/construct/build 예외를 모두 보존. create intent와 확보된 ID를
즉시 내구 기록한다. ID 불명확 시 새 create/build를 반복하지 않는다.
해당 고유 이름/intent로 조회·정리만 가능. unrelated resource/app 종료 금지.
새 연결 부분의 예상 negative fixture는 과학 실행으로 세지 않는다. 실제 오류를
고친 뒤 두 번째 원격 준비나 과학 실행을 자동 수행하지 않는다.

2. 단일 이미지 준비 및 Linux 이식
preflight 통과 후 새 recipe build 요청 최대1회. force rebuild/재설치 시도 금지.
과거 base im-eWgRNij0VH6mzozlOzEyxy는 읽기 identity/status 확인 후 base로만
재사용 가능; 완성 dependency 이미지가 아니다. 불일치 시 조용히 대체하지 말고
중단한다. 기존 고정 Python/34 pins/공개 checkpoint 정책을 유지하며 Linux
wheel/driver/CUDA/image 식별값을 별도로 동결한다. 불가한 pin을 임의 교체하지 않는다.

공유한112-file allowlist의145542095bytes identity를 전송 직전에 대조한다.
이 단계에 한해 allowlist의 기존 fake3개·공개 checkpoint/소스 읽기·해시·전송을
허용한다. root/HOME/토큰/credentials/실제 응답/키/Parquet/NPZ/기존 model cache/VAF
업로드 금지. allowlist 밖 새 파일은 이번 controller/이식 코드·고정 lock/manifest
같은 필요한 비데이터 파일만 이름·해시·이유를 명시해 추가한다.

Windows watchdog/경로/메모리 계측의 Linux 이식만 허용. CPU·RAM·native network·
중복 방지 경계를 모델 import 전에 최대60초 새 model-free 검사로 확인한다.
CPU2 논리 실행과 기존 단일 physical-core 계약, thread/affinity를 구분한다.
memory15258MiB=15999172608bytes 및 swap 금지, native block_network, GPU1 계약을
증거로 확인한다. Linux cgroup/RSS/private와 Windows private commitment를 같다고
쓰지 않는다. SDK 인증정보는 network-blocked scientific child에 넣지 않는다.
image 완료/lock·이식 diff·입력·소스·경계/timeout/cost 계약 동결 후 과학 단계 진입.

3. 조건부 H100 단일 비교
H100!1개, CPU/RAM/스레드/네트워크 고정. GPU 자원 수명2400초 이내.
새 target reference1회 → 통과 시 candidate1회, 각각900초. import/load/전처리/
검증/출력까지 시간 포함. server retry/중복에 durable latch를 적용하고 replay 금지.
기존 fake3개를 그대로 사용하고 입력 재생성·부분 예측 이어붙이기 금지.
모델/context/heads/seed/alpha grid/guard/floor/선택·refit 정책 전부 유지한다.
동일 target reference 대비 controls/final E041 UNHCR/inactive/fallback parity,
213heads/189649vectors, shadow/S 선택→동결→E guard→조건부 final expert,
원래 engineering alpha.25 경로, checkpoint/state isolation·최종 hash를 검증한다.
engineering 강제 활성과 자연 선택 결과를 구분하고 기존 계약 이상 fit을 하지 않는다.
기존 RTX 출력과 다른 GPU의 byte equality를 새 통과 기준으로 추가하지 않는다.
첫 오류/900초/자원 초과 시 STOP; deadline 연장·정책 구제·두 번째 실행 금지.

비용·시간:
새 S1 active-work 상한120분: 준비 최대60분, 단일 GPU 수명 최대40분,
export/종료/closeout20분. entry에 새 UTC deadlines 고정. 단계가 늦으면 남은
시간으로 다음 전체 단계와 종료 여유를 확보할 수 있을 때만 진입한다.
이전 active4477.3871369초와 과학4process/1077.3504532초를 별도 승계한다.
기존 USD1 준비/USD5 전체는 누적 관리용 계획, 엄밀한 청구 상한 증명 요구 아님.
현금 권한0, 사용자 보고 credits30/spend0/usage30 승계. 계정 한도/결제 변경 금지.
로그인 성공을 새 잔액 인증으로 쓰지 않는다. 정상 billing summary 접근 범위만
관측하고 budget API PermissionDenied를 반복하거나 인증 미해소로 되돌리지 않는다.
이전 summary0/component0.00001152USD·최종 귀속 미확정을 보존한다. 이전 비용과
당시 미게시 비용을 누락하지 말고 과금 delta와 자원시간 추정을 중복 없이 기록한다.
공급사 자동 retry/전송/보관 미측정 항목은0으로 놓지 않는다.
각 단계 전 누적 관리값+다음 단계 계획<USD4 확인, USD4면 종료로 전환,
나머지 약USD1은 정리 여유. 가격 가정이 달라지면 계산을 갱신하고 계획 내에서만
계속한다. USD5를 넘는 사후 게시액은 숨기지 않는다. 현금0 보장이라고 주장하지 않는다.

종료·판독:
소유한 Sandbox가 있으면 명시 종료, App stop/상태/task 확인도 수행한다.
ACK/exit0/image SUCCESS는 종료 증거가 아니다. 명시 terminal+task0만 종료 확인.
cleanup 안에서 exact-ID read-only 제한 polling 가능; 원격 재시도와 구분한다.
watchdog 후에는 별도 bounded cleanup-only 경로로 알려진 자기 ID만 정리 가능.
ID유실/timeout/잔여 task는 UNCONFIRMED와 필요한 사용자 조치로 남긴다.
새 build/science 실행 허가로 사용하지 않는다. 기존 다른 자원/cache 삭제 금지.
PASS: 전체 named technical contract와 자원/종료 증거 충족 → S0 검토 반환.
FAIL/BLOCKED: 첫 오류·미충족 조건·비용·소유 ID/종료 상태를 기록 → S0 반환.
full PASS도 실제 ERPIS 개선/hosted900초/release PASS를 뜻하지 않는다.

산출물:
entry/읽기 receipt, source.diff와 동결 manifest, live-binding/preflight 증거,
image/lock/allowlist·전송 receipt, Linux boundary 결과, reference/candidate의
events/result/resources(미완료면 partial 명시), 누적 cost/time ledger,
termination-receipt, preservation verification, closeout와 s0-handoff.ko.md.
status/log에 이번 결과만 추가. 예비 작업은 오류/누락 조건 closeout뿐이다.

S2/source-assembly/ZIP checker/official score.py/E025 absolute.002 및 E041
release 비교/업로드는 후속 별도 범위다. 새 E기록·제출물·S2/S3·commit/push·
tree 수정 금지. E041 incumbent/E025 fallback, E057/E060/E061 parked,
E058 STOP/E059 STOP_SELECTION·모든 HOLD/A039 유지.17999명/12339SSUID,
A022 역할/집계 노출, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단.
```
