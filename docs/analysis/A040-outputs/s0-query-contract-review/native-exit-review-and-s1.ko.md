# A040 S0 — boundary2 관측 수용과 종료 crash 최소 재현

2026-10-06 KST. S0 문서·허용 소스 검토.
**LOCAL_PRODUCTION_LIFECYCLE_HOLD / REMOTE_MEASUREMENT_NOT_AUTHORIZED 유지.**
아래 S1 범위는 사용자가 담당 S1에 실행을 지시할 때만 활성화된다.

## 판단과 다음 작업

이전 두 경계의 전이 관측은 수용한다. 실제 SDK Image.build/function/mount/resolver와
정확한 controller_core.py 전달, 생성 image의 Sandbox 연결이 확인됐다.
builder 실패는 Sandbox0/과학 명령0/App 정리로 이어졌다.
실제 create 대기120.0091624초 후 취소·cleanup·metadata terminal 저장도 관측됐다.
감독자125.9060169초, 강제 종료 없음. 같은120초 대기를 반복할 이유는 없다.

다만 Python은 assertion 뒤 c0000005로 종료됐다. 소유 PID의 Windows 기록과
faulthandler GC 기록이 일치한다. python313.dll은 관측된 오류 위치이며 근본 원인 확정이 아니다.
child의 BOUNDARY_PASS/ASSERTIONS_PASS_EXIT_PENDING보다 감독자 exit code와 전체 verification을 우선한다.
새 소스13개는 manifest68d8ac3c와 일치한다. 원래 repair1/boundary2 HOLD는 그대로 보존한다.

**다음 주력은 짧은 model-free builder 실패 경로의 종료 crash 최소 재현·축소 한 개다.**
원인 근거가 나오면 같은 S1에서 해당 로컬 코드만 최소 수리한다.
원격 재시도, 전체 lifecycle 반복, 임의 패키지/인터프리터 교체는 다음 작업으로 선정하지 않는다.
지금 필요한 것은 추가 PASS 문구가 아니라 어떤 구성요소가 정상 종료를 깨뜨리는지의 구분이다.

| 가설 | 근거 | 반대 근거·한계 | 구분할 관측 |
| --- | --- | --- | --- |
| fixture/guard/계측과 객체 보관의 상호작용 | crash는 현재 로컬 검증 경로에서 관측; builder 대역·guard가 계속 존재 | 전역 profile/monitoring 제거와 일부 protobuf metadata화 뒤에도 재현 | A040 전체 실행기 없이 같은 guard/최소 대역만으로 재현되는지 |
| 새 managed loop와 SDK builder 객체의 종료 순서 | 실제 Image.build를 포함한 새 경로에서 반복; builder 실패만으로도 발생 | 명시적 GC/loop 종료는 해결 못함; loop 단독 원인 근거 없음 | 동일 loop의 단순 진입, image 정의/resolve/build 단계 중 최초 재현 경계 |
| 인터프리터 또는 native 의존성 결함 | 종료 GC의 access violation이며 Python 예외가 아님 | DLL 오류 위치만으로 특정 라이브러리나 버전 원인을 판정할 수 없음 | 최소 재현이 특정 dependency 객체/호출을 요구하는지 및 공식 근거 |

Sandbox/stream 없이 builder 실패에서도 재현되므로 그 부분만 고치는 안은 우선순위가 낮다.
프로파일 제거 후에도 발생했지만 audit/network guard와 transport 대역은 남아 있으므로
“검사 도구는 무관하다”도 아직 성립하지 않는다.
로컬 설치 metadata는 Python3.13.14, Modal1.6.0, synchronicity0.12.5,
protobuf6.33.6, grpclib0.4.9다. 버전 문자열은 호환성/원인 판정이 아니다.

여기까지 장부상 준비19167.1928679초(약5.32시간), 과학4process/1077.3504532초다.
매번 전체 실행기를 고치는 방식은 중단하고, 빠른 실패 경로를 줄이는 데 한정한다.
이 작업이 실패해도 식별 가능한 최소 재현이나 최초 실패 경계가 남아야 한다.
그것도 얻지 못하면 A040 추가 수리를 자동 반복하지 않는다. 정확한 미충족 입력 closeout이
유일한 예비 작업이다. 다른 연구 경로의 진행 권한은 별도로 판단한다.

## 같은 S1에 전달할 완성 프롬프트

이 채팅은 SimulacraBench / HSCC S1 기술 조사다.
C:\Users\USER\Desktop\SimulacraBench에서 아래 로컬 종료 crash 조사와
원인이 입증된 범위 내 최소 수리를 수행한다. 원격 실행·환경 교체는 포함하지 않는다.

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md와
이 문서를 실제 읽고 역할/개정/허용 범위를 보고한다. workflow r5를 적용한다.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
실제 HEAD·dirty·관련 jobs를 확인하고 기존 변경·HOLD·실패·latch를 보존한다.

입력:
- docs/analysis/A040-outputs/production-lifecycle-boundary2/의 closeout.md,
  verification.json, stall-timing.json, regression-history.md, source-manifest.json,
  cost-time-ledger.json, owned-native-crash-evidence.json, source.diff, placement.diff.
- 같은 폴더의 builder-await6/image-success1/builder-failure1 관련 process/stderr/trace,
  check_boundary.py, boundary_transport.py, fixture_transport.py, local_guard.py,
  run_check.ps1 및 필요한 생산 소스. 이전 attempts는 비교에 필요한 소스만 읽는다.
- 기존 tmp/a040-modal-full-path1/sdk-venv/의 pyvenv.cfg, 관련 dist-info METADATA,
  설치 SDK/dependency 소스. import는 아래 차단 장치가 있는 새 로컬 검사에서만 허용한다.

현재 source-manifest SHA256:
68d8ac3c23b8ab0f74a41893bd122733e79e54fb6915ee293d921a9a30e1cb50.
새 산출물은 docs/analysis/A040-outputs/local-exit-diagnosis1/와 대응 tmp 경로에 둔다.
충돌 시 새 경로를 고른다. 원래 boundary2/repair1/설치 환경에 덮어쓰지 않는다.

확인할 질문:
같은 고정 환경에서 정상 종료를 깨뜨리는 최소 객체/호출/종료 상호작용은 무엇인가?
과거 full-path 결과를 재생하거나 모델 성능을 검증하는 작업이 아니다.

진행:
1. 기존 실패 trace/exit/source를 먼저 비교한다. 이미 효과 없었던 profile 해제,
   무조건 GC/loop close 반복을 다음 가설 없이 되풀이하지 않는다.
   새 process에는 작은 protocol 입력만 사용하며 실제 응답/모델은 넣지 않는다.
2. 짧은 builder_fail 경로를 출발점으로 축소한다. 현재 crash 재현의 기준 실행은
   허용하되 success 전체 경로와120초 stall을 기본 재현으로 사용하지 않는다.
   guard만 있는 진입, SDK import/관리 loop, image 정의/resolve/build 중 필요한
   대비만 택한다. 목록 전체를 의무 suite로 만들지 않는다.
3. 매 비교 전 가설·바꿀 한 가지·예상 구분 결과를 기록한다. A040 orchestration/
   observer/transport 객체 등을 덜어낼 때 실제 인증/RPC/모델/보호 파일 차단은 유지한다.
   guard 자체가 의심되면 동일 차단을 보장하는 최소 대역/진입에서 확인한다.
   “guard를 꺼서 실제 네트워크를 허용”하는 방법은 금지한다.
4. 정상 종료와 crash를 가르는 최소 재현·대조 및 소스 설명을 확보한다.
   일회성 정상 종료를 수리 완료로 보지 않는다. 필요한 재현/대조 재확인은 허용하지만
   목적 없는 조합 탐색은 하지 않는다. 변화가 원인 제거인지 검사 경로 생략인지 구분한다.
5. 원인이 fixture/guard 또는 허용된 orchestration Python 소스에서 입증되면
   새 복사본만 최소 수정하고 해당 짧은 경계를 실제 SDK로 다시 검증한다.
   일반 오류는 r5에 따라 같은 S1에서 수리한다. 오류마다 새 S0 인계를 만들지 않는다.
   native dependency/인터프리터 변경이 필요하다는 근거만 얻으면 임의 교체하지 말고
   최소 재현·현재 버전·정확한 변경 제안과 필요한 후속 검증을 남긴다.

허용 환경 변경:
- 새 조사 폴더/임시 출력, 검사 코드와 필요한 orchestration 복사본만 작성.
- 기존 동일 Python/SDK/dependency를 사용. faulthandler 등 기존 런타임의 문서화된
  진단 옵션은 단일 비교에 허용하고 옵션/해시/차이를 기록한다.
- 필요한 경우 원인과 직접 연결된 CPython/Modal/관련 dependency 공식 문서·이슈
  최대3개를 읽을 수 있다. 코드/로그/자료 업로드, 외부 문의 발송은 허용하지 않는다.
- 설치/업데이트/다운그레이드/다른 interpreter·backend 교체, SDK site-packages 패치,
  시스템 registry/전역 설정/계정 변경은 금지. 전체 프로세스 메모리 덤프도 범위 밖이다.
- os._exit(0), crash exit code 무시, GC/필수 종료 단계 제거로 성공 처리하지 않는다.
  종료 위치를 바꾸는 실험이 원인 축소에 쓰였다면 진단으로만 표기하고 생산 수리로 승격하지 않는다.

시간·자원:
전체40분, 마지막10분 기록. 새 검사 감독자 wall 합240초, 각30초.
소유 프로세스20초에서 정리 시작, 나머지10초 회수/기록. CPU2/GPU0.
실제 Python 자식과 venv launcher를 구분하고 시작 전 CPU 제한 및 잔여 프로세스를 확인한다.
매 실행 전 필요한 최악 시간·잔여 합계·기록 시간을 확인한다.
최대6개의 명명된 원인 비교 안에서 적응적으로 진행한다. 단순 경로/import/시험 도구 오류는
같은 비교 안에서 고치되 모든 실행 시간·실패를 누적한다. 한도/허용량은 초기화하지 않는다.
같은 비교가 새 정보를 만들지 못하면 다음으로 옮기거나 종료한다.

실제 Modal 인증/RPC/billing/옛 자원 조회·App/image/Sandbox 생성·전송/H1000.
기존112payload/checkpoint·응답/키/Parquet/NPZ/모델cache/VAF 접근·해시 금지.
fit/predict/score·설치·과학 fixture·120초 재대기·성공11-case suite 반복 금지.
새 모델/seed/head/context/선택/guard/refit/900초 과학 정책 변경 금지.
ZIP/제출·S2/S3·tree·E기록·commit/push·다른 세션/서브에이전트 자동 실행 금지.

종료·산출물:
- 진단 성공: 최소 재현과 대조, 변경한 변인, 실제 부모/자식 exit code·GC/error 기록,
  해당 원인에 대한 근거/미확정을 제출한다. 이는 LOCAL_EXIT_CAUSE_ISOLATED 수준이며
  전체 lifecycle/원격/H100 PASS가 아니다.
- 근거 있는 로컬 수리까지 완료하면 LOCAL_EXIT_REPAIR_VERIFIED로 구분한다.
  최종 exit0·강제 종료 없음·예상 실패 전이 유지·금지 동작0·잔여 PID0을 확인한다.
  이미 관측한 image/timeout 증거 중 무엇이 그대로 유효한지, 수정으로 무효화되어
  후속 검증이 필요한 경계가 무엇인지 적는다. 부족한 검증을 PASS로 메우지 않는다.
- 원인 미확정이면 정확한 최소 재현/최초 실패 경계 또는 확보 못한 입력을 적어 HOLD.
  이번 범위에서 신뢰할 축소 근거가 없으면 또 전체 suite/환경교체/원격 시도를 제안하지 않는다.
- 최소 reproducer/대조 소스, source manifest/diff, 실행별 감독자 receipt,
  regression-history, verification, cost-time-ledger, exposure-ledger,
  closeout, s0-handoff.ko.md 및 status/log 갱신. 생성 자체가 다음 실행 허가는 아니다.

준비19167.1928679초에 이번 active wall만 중복 없이 가산한다.
과학4process/1077.3504532초 불변. 과거 workspace meteredUSD0.01009897/billed0,
최종 A040 귀속/GPU시간 미확정, USD1/5 계획·cash0·2400초 예약은 승계한다.
실Sandbox sb-svFnVI39hH3DpUIZ4Z9LXK 종료 확인은 완료 상태이며 재조회하지 않는다.
E041 incumbent/E025 fallback, parked E057/E060/E061, E058 STOP/E059 STOP_SELECTION,
A039 및 모든 STOP/HOLD,17999명/12339SSUID·집계/A022 원래 역할,
소비 oracle1918/1124·selection2007/1130와 보호 audit2074/1177·calibration1866,
A_half 비승격·A018 미확정·S3 중단·S2 없음 유지.

## S0 접근·읽기 기록

S0는 필수 진입 순서와 최신3개 log, 명명된 boundary2 산출물, 실패 stderr/소유PID Windows
기록, 생산 diff 및 검사/대역/guard/감독자 소스, 기존 SDK image/synchronizer 소스와
pyvenv.cfg/4개 dependency METADATA를 읽었다. SDK import/검사/RPC/웹 조회는 수행하지 않았다.
karpathy-guidelines와 systematic-debugging 원칙으로 근거와 원인 추정을 분리했다.
workflow2026-10-05-r5 SHA256:
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
HEAD a43f4379, branch work/e050-submission, dirty89, 이름 기준 Python/pythonw/uv jobs0.
S1 entry의 읽기 증거는 S1 보고로 분류하며 다른 채팅의 준수까지 보증하지 않는다.
전후 해시·공유 기록의 기존 본문 보존은 [검증](native-exit-review-verification.json)에 기록한다.

