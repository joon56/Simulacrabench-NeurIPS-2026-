# S1 제목: A040 — 원격 호출 전 실행기 전체 연결 보완

기존 S1에 아래 본문을 사용자 지시로 전달한다. 작성 자체는 실행 허가가 아니다.

```text
SimulacraBench / HSCC S1 — A040 로컬 기술 보완을 수행한다.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
이번 범위는 RPC 차단 로컬 구현·검증이다. 원격 재시도/H100 실행 범위가 아니다.

AGENTS → CLAUDE → status → log 최신3개 → workflow.md 순서로 읽고
현재 역할·개정·허용/금지·workflow 해시와 읽기 근거를 entry에 기록한다.
HEAD/dirty/관련 jobs 확인, 기존 변경 보존. 서브에이전트 실행 금지.

필수 입력:
docs/analysis/A040-outputs/s0-modal-protocol-review/decision.md
docs/analysis/A040-outputs/modal-full-path1-resume3/의 closeout.md,
failure-analysis.md, verification.json, result.json, termination-receipt.json,
live-controller-freeze.json, source.diff, live_binding.py, live_worker.py,
controller_core.py, live_launcher.py, preflight.py, operational-contract.md.
modal-controller-repair1의 계약·기존 회귀 결과는 기록으로 승계한다.
s0-modal-controller-review/s1-remote-resume.ko.md와 기존 platform/full-path
계약은 설계 입력이다. 그 문서의 원격 실행 지시를 이번에 활성화하지 않는다.

새 위치:
docs/analysis/A040-outputs/modal-local-integration1/
tmp/a040-modal-local-integration1/
번호/경로 충돌 먼저 확인하고 존재하면 덮어쓰지 않는다. 기존 resume3 파일,
실패/latch/manifest/SDK 설치·모델/제출물은 수정하지 않는다.
기준 live_worker SHA256:
bbc5fc6e2835f6bddf516a3eeade73b18c2546f826db990a5bddf806da1fc6dc
기준 live_binding SHA256:
ca1351a05eea38577632a918b286d5ee7e5c82d423928fd8c2ce1af67de206c8

목적·기존 작업과의 차이:
enum 한 줄 또는 클래스 signature만 검사하지 않는다. 다음 원격 시도에서
호출될 동일 실행기와 모든 로컬 모듈을 먼저 완성하고, 그 실행기의 응답 처리와
단계 연결을 RPC 차단 상태에서 검증한다. 새 모델·점수 실험이 아니다.

수행 범위:
1. 기존 설치 SDK1.6.0 소스/실제 protobuf 정의로 호출 계약을 확인한다.
   잘못된 모듈 상수와 GenericResult.GENERIC_STATUS_SUCCESS 차이를 로컬에서
   재현하고 새 복사본에서 최소 수정한다. 성공/실패/미지정 상태·빈 stream·
   identity 불일치와 실제 응답 필드 처리를 검증한다. 정의하지 않은 상수를
   fake SDK에 추가하거나 모든 응답을 성공으로 만드는 테스트 금지.
2. live preparation, image 완료, payload 확인/전송, Sandbox 설정, Linux
   watchdog/boundary, reference/candidate 순서, 결과 export, cleanup의 기존
   고정 흐름을 구현한다. 누락된 sandbox_stage와 Linux 이식도 이 로컬 범위에
   포함한다. 모델 코드는 읽기만, 변경/실행하지 않는다. 기존 정책을 호출하는
   orchestration/OS 계측 이식만 새 위치에 작성한다. 범용 플랫폼 재작성 금지.
3. 모든 호출 모듈 존재·import/호출 형태·enum/필드·시간/비용 gate를 먼저
   연결한다. 원격 build 뒤 코드 완성을 기다리는 continue 파일 흐름을 쓰지
   않는다. source manifest에 빠진 모듈/placeholder가 있으면 진입 거절한다.
   runtime image ID·현재 계정 수치·실제 payload parity처럼 원격/전송 시에만
   얻는 값은 UNVERIFIED로 둔다. 가짜 값으로 실제 gate를 통과 처리하지 않는다.
4. 실제 향후 실행할 orchestration을 대상으로 RPC/remote process/payload
   endpoint만 주입해 검증한다. SDK/protobuf는 설치된 실제 타입을 사용한다.
   과거 fake controller 복사본의 성공으로 새 live_worker를 대신하지 않는다.
   실제 자격증명 발견/Client.from_env/네트워크·RPC는 호출 경계에서 차단한다.
   socket monkeypatch만으로 native egress 차단이 증명됐다고 주장하지 않는다.
5. 새로 연결한 경로에 한해 모델 없는 통합 회귀를 수행한다: 정상 단일 경로,
   enum/응답 오류 시 create0, build 실패 시 science0, 준비/경계 미완료 시
   science0, reference 실패 시 candidate0, 중복/latch 거절, timeout·ID유실·
   cleanup 실패에서 거짓 PASS 없음. 실제 protobuf 메시지 및 spec에 맞춘
   제한된 fake를 사용한다. 기존15개 suite·성공 과학 fixture는 재실행하지
   않는다. 바뀐 orchestration의 cleanup 연결 검증은 새 회귀로 명시한다.

허용 입력/실행:
문서·공개 SDK/생산/기존 runner 소스·lock·manifest/allowlist 메타데이터 읽기·
해시, 새 로컬 integration 코드/일회용 소형 protocol fixture 작성, 설치된
SDK/protobuf import와 RPC 차단 회귀. fixture는 응답 데이터가 아닌 프로토콜
메시지·파일 전송용 무의미한 작은 바이트·가짜 process 결과로 제한한다.
112 payload/기존 fake3개/checkpoint/실제 응답/키/Parquet/NPZ/모델 cache/VAF는
열거나 재해시하지 않는다. 실제 scientific command는 recorder로 대체하고
fit/predict/score·model import·GPU·Linux 실제 boundary 실행은0이어야 한다.
설치/다운로드/로그인/계정 RPC/빌드/전송/Sandbox/유료자원 모두 금지한다.

원래 과학·자원 설계 보존:
fixed fake3개, E041/TabICL 정책·seed/context/heads/alpha/guard/floor/refit 불변.
미래 reference/candidate 각1회900초, H1001개2400초, CPU/RAM/native offline
한도는 기존 계약 그대로 코드에 연결한다. 이번에는 그 실행 허가가 없다.
원래 target 경계의 OS/native enforcement는 실제 환경에서 검증할 항목으로
남긴다. 로컬 mock PASS를 H100/900초/자원/과학/release PASS로 쓰지 않는다.

한도·종료:
새 로컬 active90분, focused regression 누적180초, 전체 회귀 cycle 최대3회.
최초 재현과 의도한 negative case는 등록된 검증이다. 이 한도 내에서 발견한
연결 결함 수정과 영향 경로 재검증은 허용하며 각 실패/수정/회차를 보존한다.
성공 뒤 무변경 반복 금지. 한도 소진·허용 범위 밖 의존성이 필요하면 중단한다.
금지된 접근이 발생하면 즉시 중단하고 접근 내역을 남긴다.
과거 첫 실제 오류 STOP과 실패 산출물은 불변. 이번 로컬 수정 범위는 과거
원격 재실행 권한이나 남은120분의 부활이 아니다.
누적 준비/controller active5504.7268216초, 과학4process/1077.3504532초 승계.
USD1/5 누적 계획·현금0 그대로; 이번 원격 비용 발생 작업은0.
기존 billing0/component0.00001152USD·미게시/귀속 미확정 보존, 새 조회 금지.

성공: 전체 호출 모듈 구현·고정 정책 보존·실제 타입 기반 로컬 회귀 통과,
외부 효과0, 보존/manifest 충족이면 LOCAL_ORCHESTRATION_CONTRACT_PASS로 S0 반환.
이는 원격 준비 완료/실제 Linux 실행 가능성 판정이 아니다.
실패/미완료: 정확한 interface/구현 누락·필요 입력·소유자·중단 근거를 기록해
S0 반환한다. 단순 enum 수정 PASS만으로 전체 완료 선언 금지.
예비 작업은 closeout뿐. 다음 원격 시도나 새로운 작은 수리 작업 자동 시작 금지.

산출물:
entry/read receipt, source.diff, source/contract manifest, 단계별 호출·증거표,
새 코드와 RPC 차단 회귀/오류/시간 기록, 보존 verification, exposure/cost/time
ledger, closeout, s0-handoff.ko.md. status/log에는 결과와 제한만 추가한다.
실제 SDK/source로 확인한 것·fake로 검증한 것·아직 미검증인 것을 구분한다.
새 E/ZIP/checker/official score/release/업로드/commit/push/tree/S2/S3 금지.
E041 incumbent/E025 fallback, E057/E060/E061 parked, E058 STOP/E059 STOP_SELECTION,
A039/모든 HOLD,17999/12339·A022 역할·집계 노출·E059 소비 oracle1918/1124와
selection2007/1130·보호 audit2074/1177/calibration1866 유지.
A_half 비승격/A018 사용자 미확정/S3 중단/S2 후보 없음.
```
