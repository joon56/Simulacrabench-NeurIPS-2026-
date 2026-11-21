# S1 — A040 builder 보완본의 Modal H100 단일 측정

사용자가 아래 본문을 S1 실행 지시로 전달할 때 새 범위가 활성화된다.
S0의 작성이나 로컬 PASS 자체는 원격 실행 허가가 아니다.

```text
SimulacraBench / HSCC S1 — A040 고정 경로의 원격 기술 측정을 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1
이번 지시는 아래 새 bounded 원격 시도1회에 한정한다. S2 제작·업로드 아님.

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md를
순서대로 읽고 역할/개정/SHA256/읽기 근거·현재 HEAD/dirty/관련 jobs를 기록한다.
기존 변경·모든 실패/PASS·manifest/latch를 보존한다. 서브에이전트 실행 금지.

필수 입력(아래 경로는 docs/analysis/A040-outputs/ 기준):
- s0-builder-pass-review/decision.md
- local-preparation-repair2/{closeout,verification,source-manifest,cost-time-ledger},
  source.diff, placement.diff, boundary-design.md 및12개 production source.
  .md/.json 확장자는 실제 파일명대로 사용한다.
- modal-full-path1-resume4/{failure-analysis.md,termination-receipt.json,
  config-source-input-freeze.json,live-config.json,session-cost-time-ledger.json}
  이 live-config는 구조 참고만; deadline/latch/output/소스 해시 그대로 재사용 금지.
- modal-full-path1/allowlist.json, full-path-resume1/requirements.lock.txt,
  modal-local-integration1/phase-evidence.md와 미검증 목록.

고정 소스: docs/analysis/A040-outputs/local-preparation-repair2/
source-manifest SHA256:
c782c99e29cfceeaba132018d48f2be2a844e7f8b51ba8840157f9ebfa845765
controller_core SHA256:
fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb
linux_runner SHA256:
82facf9151daa8eadc55c438be99f4c0cf5e331978c18b3a59530ef2af5b680e
12source identity를 확인한다. 다른 파일이면 경위를 남기고 STOP; 되돌리지 않는다.
새 source 수리·다른 복사본·installer/pins 교체는 범위 밖이다.

새 설정/출력은 modal-full-path1-resume5/ 및 tmp/a040-modal-full-path1-resume5/.
충돌 시 미사용 suffix를 정해 entry에 고정한다. source 디렉터리에 결과를 쓰지
않는다. 새 고유 App/Sandbox 이름·absolute UTC deadlines·실행 intent/latch,
실제 이번 사용자 지시를 함께 기록한다. execution_authorized boolean만으로
권한을 주장하지 않는다. 옛 시도의 남은 시간/과학 allowance는 승계하지 않는다.

목적과 관측:
실제 builder 모듈 전달/설치, Linux 실행 경계와 고정 후보 all3 자원·출력 계약을
측정한다. 공개 checkpoint와 기존 fake3만 사용. ERPIS/VAF 효과 실험 아님.
이미 통과한 로컬 계약을 다시 검사하지 않는다. 각 gate가 통과하면 같은 S1에서
다음 단계로 진행; 첫 실제 준비/경계/과학 실패에는 종료·기록만 한다.

1. 진입/동결
기존 SDK1.6.0·정상 인증 재사용. local guard/check_local/isolate/run_check는
로컬 검증 도구이며 원격 worker로 쓰거나 함께 전송하지 않는다.
고정 live_launcher와12module을 사용한다. 새 config의 경로·extra_files·source
해시·시간/자원·권한 연결만 모델 없는 검사로 확인한다(누적60초 이내).
원격 요청 전에 확인된 config 오기는 이 한도 안에서 고칠 수 있지만 production
source 수정은 금지. 과거15/39/14 suite·최근6검사·tiny/schema fixture 반복 금지.
숨김 프로세스·UTF-8 로그·실제 PID/소유 process tree를 기록한다.

2. 계정/단일 이미지 준비
정상 SDK로 workspace joon56/main, 정상 billing metadata를 확인한다.
사용자 보고 credits30/spend0/usage30과 현재 독립 관측을 구분한다. 거절된
budget API 반복·한도/결제 변경·불필요한 재로그인/재설치 없음. 실제 인증 만료,
계정/현금 비용 모순 또는 현재 작업 권한 부재가 관측되면 해당 조건만 기록한다.
기존 base im-eWgRNij0VH6mzozlOzEyxy의 현재 status/result identity를 저장된
근거와 대조해 base로만 사용한다. 실패 image를 완성 이미지로 사용하지 않는다.
기존34pins 파일의 hash를 launcher 기대값과 새로 검증한다. 이 S1에서 필요한
허용 문서/소스 읽기이며 지난 local PASS가 pins bytes도 검증했다는 뜻은 아니다.

새 App/image recipe 요청 최대1회. include_source=True의 정확한
controller_core.py 바이트 전송을 사전 해시 확인 뒤 허용한다. SDK-managed
client mount는 프로젝트 파일과 구분해 기록한다. repo/root/HOME 자동 전송 금지.
installer600초/build900초, 기존 Python3.13.14/34pins 유지. 실제 image identity,
설치/lock·driver를 기록한다. 오류 후 재빌드/force build/다른 pins/다른 base 금지.

3. 허용 payload/단일 Sandbox
원격 전송은 기존 allowlist112개/145542095bytes 및12개 고정 production source만.
전송 직전에 정확한 allowlist의 fake3·공개 checkpoint·공개 소스 바이트 확인/
해시/전송을 허용한다. 변경·누락·추가 발견 시 STOP. 새 데이터 취득/재생성 금지.
코드 extra prefix: docs/analysis/A040-outputs/local-preparation-repair2/.
runner의 /work/tmp/a040-modal-local-integration1 출력 경로는 그대로이며 새
Sandbox 안에서 새 출력을 만든다. 옛 부분 출력이나 배열을 재사용하지 않는다.
112파일 밖 응답/Parquet/키/NPZ/cache/VAF/credentials는 접근·해시·전송 금지.

H100!1개, cpu(1,1)/two logical threads, RAM15258MiB=15999172608bytes,
swap0/gvisor/block_network/no secrets/no OIDC. Sandbox 최대1개/2400초.
고정 Linux boundary1회/60초, 모델 import 전에 수행한다. driver/정확한 pins/
CPU quota·affinity/cgroup·swap/native-network/allowlist/중복 방지 확인.
로컬 launcher affinity를 실제 worker 제한의 증거로 대체하지 않는다. 실제
모델 프로세스와 자원 경계를 기록한다. Linux private/RSS를 Windows commitment와
같다고 쓰지 않는다. 필요한 제한이 미확인 또는 실패하면 즉석 완화 없이 STOP.

4. 고정 reference와 candidate
앞선 gate 통과 후 reference1회/900초, 통과 시 candidate1회/900초.
각900초는 import/load/전처리/3기관 전부/검증/출력까지 포함한다.
같은 target reference로 비교; RTX/H100 bit equality를 새 기준으로 만들지 않는다.
원래 fake3, 모델/context/head/seed/alpha/guard/floor/refit 정책 불변.
213heads/189649vectors, controls/final E041/inactive/fallback parity,
shadow/S 동결/E guard/final/engineering alpha.25, state hash/checkpoint load/
call count 계약을 원래 runner대로 완료한다. 일부 head 성공으로 전체를 외삽 금지.
출력 key/count: unicef17856/world_bank39520/unhcr132273. Candidate extra2개는
hash/files에만 포함. 출력 회수 실패도 실패이며 candidate partial을 PASS로 쓰지 않는다.

시간/비용/중단
총active120분: 준비<=60분, GPU수명<=40분, export/cleanup/기록20분 확보.
단계 시작 시 그 전체 한도와 정리 시간이 남아 있어야 한다. deadline 연장 금지.
준비/controller10581.0943693초, 과학4process/1077.3504532초를 분리 승계.
소스에 남은 옛 history 값5504.7268216은 새 누적값이 아님; 새 session ledger가
현재 누적을 기록한다. worker/check/cleanup 중첩 시간을 두 번 더하지 않는다.

USD1 준비/USD5 누적은 모니터링 계획, cash0, 기존 계정 설정 불변.
과거 summary0/component0.00001152, management0.6502900821875501(여유.65 포함),
미게시/귀속 불확실성을 승계한다. 계획 여유를 실청구로 쓰거나 장부 초기화 금지.
정상 billing 및 자원시간 계획을 구분해 보수적으로 관리하되 중복 합산하지 않는다.
신규 단계 전 누적 관리값+다음 전체 단계 계획<USD4; USD4면 정리로 전환,
약USD1 종료 여유. 고정 비용 가정이 현재 근거와 맞지 않으면 기록 후 STOP;
예산/계정 상향·고정코드 변경으로 구제하지 않는다. 엄밀한 최종 청구액 보장이나
공급사 메일을 새 전제로 만들지 않으며, 게시 지연으로 현금0을 보장하지도 않는다.

첫 실제 준비/경계/과학 오류·timeout·identity/자원/비용 모순이면 STOP.
소스 수정·두 번째 build/Sandbox/scientific 호출·부분 상태 재개 금지.
예비 작업은 진단 회수·소유 자원 정리·closeout뿐. 계속 실행 권한 생성 금지.
정확히 기록한 이번 owned ID에 한해 cleanup-only SDK/CLI·종료 조회를 허용한다.
정리 한도60초, Sandbox terminal 및 App 명시STOPPED/task0를 확인한다.
stop ACK/client exit만으로 종료 판정 금지. parent 강제종료/ID유실/종료 미확인 시
UNCONFIRMED와 ID·남은 사용자 조치를 즉시 보고한다. 다른 자원은 종료하지 않는다.

산출물
entry/이번 권한·읽기 receipt, 새 config/source/input/전송 freeze,
실제 image/Linux lock/driver/boundary, reference/candidate 결과/events/resources/
출력 hash·회수 근거, 실패 시 partial·NOT_RUN 단계, 누적cost/time ledger,
termination receipt, 기존 파일 보존 확인, closeout와 s0-handoff.ko.md,
status/log 갱신. 준비 실패/측정 자원 실패/전체기술PASS를 구분해 S0로 반환한다.

금지·보존
E기록 생성, 모델/정책 변경, ZIP/checker/official scorer/E025-E041 release 비교,
업로드/commit/push/tree/S2/S3/TEST 선택은 범위 밖. 성공해도 S2 자동 이관 금지.
E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 과학STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039 HOLD 유지. UNHCR 회신은 이 작업의 조건 아님.
노출17999명/12339SSUID·집계·A022 역할, E059 소비 oracle1918/1124 및
selection2007/1130, 보호 audit2074/1177·calibration1866 유지.
A_half 비승격, A018 사용자 미확정, S3 중단, S2 후보 없음.
```
