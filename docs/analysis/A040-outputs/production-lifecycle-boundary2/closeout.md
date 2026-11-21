# A040 S1 — 남은 두 lifecycle 경계

2026-10-06 KST. **LOCAL_PRODUCTION_LIFECYCLE_HOLD /
REMOTE_MEASUREMENT_NOT_AUTHORIZED.** 명명된 전이는 관측했지만 정상 프로세스 종료는 실패했다.

사용자가 이 S1에 전달한 완성 인계문 범위를 수행했다. AGENTS/CLAUDE/status/log 최신3개/
workflow2026-10-05-r5를 재읽었으며 receipt·SHA·도구 근거는 [entry.json](entry.json)에 있다.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, repair1 source-manifest9bed4451 확인 후
새 boundary2 경로를 사용했다. 원래 HOLD·실패·latch·manifest는 수정하지 않았다.

## 확인된 사실

1. **실제 Image.build 연결:** Endpoint 기본 `_build`, SDK Image/function/mount/resolver를
   그대로 사용했다. SDK가 읽고 전송 요청한 프로젝트 파일은 `/root/controller_core.py`
   하나,1760bytes, SHA256 `fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb`였다.
   SDK client mount는 별도 이름 조회 응답이다. builder의 module/function은
   `controller_core.install_pins`, 완료 image ID는 `im-dddddddddddddddddddddd`.
   같은 ID가 실제 SDK SandboxCreate 요청에 들어갔다. protocol 출력 회수와 exact terminal도 관측했다.
   완료 image를 직접 hydrate하는 함수는 주입하지 않았다. installer 본문은 실행하지 않았다.
2. **builder 실패 전이:** 실제 SDK의 ImageBuildError가 생산 실행기에 전달됐다.
   Sandbox create0·과학 명령0·App 정리·STOP_FIRST_ERROR가 관측됐다.
3. **실제120초 만료:** create 시작15:57:26.320799Z, 취소 관측15:59:26.327151Z.
   perf_counter 차이는 **120.00916240000515초**다. 생산 timeout120/cancel_grace2/cleanup60을
   유지했고 즉시 예외·가짜 clock을 사용하지 않았다. 생산 TimeoutError 후 cleanup 진입,
   exact-ID terminal 저장으로 연결됐다. create1/terminate1, boundary/reference/candidate0.
   작은 fixture의 exact ID는 `sb-aaaaaaaaaaaaaaaaaaaaaa`이며 실제 서비스 자원 ID가 아니다.

시간축·PID·관측과 종료는 [stall-timing.json](stall-timing.json)에 분리했다.
실제 Python48852는125.8273074초 뒤 종료, launcher54420은125.8868132초,
감독자 전체125.9060169초였다.210초 한도 안이며 강제 종료하지 않았다.
당시 생성·취소·terminal 파일과 callback/trace는 [protocol-evidence](protocol-evidence/) 및
`attempts/real-stall1/`에 있다. 초 단위 시계 차이는 각 시계가 측정하는 구간의 차이이며
UTC timestamp 차이를 perf_counter 값과 동일하다고 만들지 않았다.

## 전체 PASS가 아닌 이유

위 assertion이 완료된 뒤 Python 프로세스가 **c0000005 / access violation**로 종료됐다.
Windows의 해당 소유 PID 오류 기록은 `python313.dll`을 지목하고,
faulthandler 일부 기록은 최종 Garbage-collecting 구간을 보인다.
프로파일 해제, 특정 코드 monitoring, 명시적 GC/SDK loop 종료, protobuf 증거의 단순 metadata화로
해결되지 않았다. 전역 계측을 제거한 coroutine-await-chain 관측에서도 재현됐다.
정확한 원인은 미확정이다. 프로파일·SDK·protobuf·특정 모델의 결함으로 확정하지 않는다.

초기 child 산출물의 `BOUNDARY_PASS`는 assertion 직후 기록된 값이다.
**비정상 종료한 어느 child도 최종 PASS가 아니다.** 후반 기록은
`ASSERTIONS_PASS_EXIT_PENDING`으로 분리했고 감독자 판정을 추가했다.
원래 기록을 지우거나 소급 수정하지 않았다. [verification.json](verification.json)이 전체 판정이다.

실행 중 source 변경·SDK patch·assertion 제거·의존성/인터프리터 교체·`os._exit(0)` 우회는 하지 않았다.
입증된 일반 오류인 Windows affinity HANDLE 형식은 같은 세션에서 수정했다.
native 원인까지 입증할 경로가 이번 허용 입력·변경 범위 안에서 확보되지 않아 더 같은 진단을
반복하지 않았다. 전이 관측을 깨끗한 프로세스 종료로 대체하지 않고 S0에 반환한다.

## 보존·비용·한계

생산13개 중10개 복사본은 바이트 동일하다. contract/launcher는 새 위치만 바뀌었다.
live_worker에는 cleanup 진입과 terminal 파일 저장 후 event 두 개만 추가했다.
installer/pins·과학 runner·모델/seed/head/context/선택·guard/refit·900초 정책은 보존했다.
[source.diff](source.diff), [placement.diff](placement.diff), [preservation.json](preservation.json),
[source-manifest.json](source-manifest.json)을 참조한다.

새 검사11회 감독자 wall 합계 **184.9543889초 /420초**. 중첩 Python 시간은 더하지 않았다.
모든 short/stall 감독자 cap 안에서 회수됐다. 초기 venv launcher의 CPU affinity 설정만으로
redirect된 Python의 정확한 affinity를 별도 입증하지 못했다. 후반 검사는 SDK import 전에
실제 Python에 CPU2를 설정했고, stall은 실제 PID/affinity/종료를 감독자에서도 포착했다.
잔여 관련 로컬 python/pythonw/uv jobs0. 전체 wall과 누적 준비는 [장부](cost-time-ledger.json) 참조.

준비17197.7879076초에 이번 active wall만 가산. 과학4process/1077.3504532초 불변.
실제 인증/RPC/billing 조회/build/전송/App·Sandbox 생성/GPU/model/설치/유료 행동0.
과거 workspace meteredUSD0.01009897/billed0·USD1/5 계획·cash0·2400초 예약USD2.965933453125 유지.
최종 A040 귀속 비용·실제 GPU 시간 미확정. 서비스 과금이나 다른 자원 부재를 재조회하지 않았다.

작은 protocol bytes/count metadata는 실제189649개 예측·Linux/GPU/native 메모리/offline/watchdog
동작의 증거가 아니다. 현재 image/account/payload identity, H100900초, 효과·release/S2는 미검증.
기존 실자원 `sb-svFnVI39hH3DpUIZ4Z9LXK` 종료 확인은 완료 상태로 유지하고 조회0.
기존 성공11 suite·builder-source suite·과학 fixture는 반복하지 않았다.
모든 기존 STOP/HOLD·평가 노출·E041/E025·parked·A018 미확정/S3 중단을 유지했다.
ZIP/업로드/commit/push/tree/서브에이전트/S2/S3 실행0.

다음 판단은 [S0 인계문](s0-handoff.ko.md)에 한정한다.
