# A040 S0 — 생산 lifecycle 수리 수용과 남은 두 경계

2026-10-06 KST. S0 문서·허용 소스 검토. 아래 S1 지시는 사용자가 해당 S1에
전달하여 실행을 지시할 때만 활성화된다. 이 문서 작성은 원격 실행 허가가 아니다.

## 판단

**LOCAL_REPAIR_IMPLEMENTED 수용. LOCAL_PRODUCTION_LIFECYCLE_HOLD 유지.**
현재 13개 생산 소스가 manifest와 일치한다. SDK 관리 loop, 요청 전 intent·예약,
SDK 내부 종료까지 포함하는 중복 방지, metadata-only exact-ID 정리 및 terminal-first
증거 보존은 11개 명명된 사례와 소스가 뒷받침한다. 전체 경로 PASS로 확대하지 않는다.

남은 두 경계는 별도 모델 연구가 아니라 같은 실행기의 기술 검증이다.

| 경계 | 인정하는 증거 | 아직 없는 증거 | 다음 판단에 필요한 것 |
| --- | --- | --- | --- |
| create 대기 만료 | 즉시 TimeoutError/CancelledError 처리, 실제 SDK hydrate/stream 및 cleanup 사례 | 실제 생산 120초 대기가 끝나 cleanup으로 연결되는 관측 | 생산 120초·cancel grace를 유지한 로컬 stall 1개 |
| image와 Sandbox 연결 | resume5의 실제 builder 설치 완료, installer 바이트 보존, 현재 SDK Sandbox 경계 | 새 SDK 관리 loop에서 실제 Image.build가 완료되어 동일 image가 Sandbox에 전달되는 연결 | 완료-image 주입 없이 실제 SDK Image.build를 거치는 성공/실패 전이 |

120초 검사에 각 30초 상한을 적용한 이전 계약은 검증 목적과 충돌했다.
S0가 정한 시간 계약에도 책임이 있다. 이전 cycle3의 30.0874074초와 엄격한
자식 30초 이내 미입증은 그대로 남긴다. 소급 PASS나 실패 삭제로 해결하지 않는다.
새 시간 계약은 아래 한정된 검사에만 적용하며 원격·과학 한도를 늘리지 않는다.

과거 builder 성공과 현재 Sandbox 성공을 합쳐 새 연결 전체가 검증됐다고 할 수는 없다.
loop 진입점이 바뀌었고 현재 양성 fixture는 Endpoint._build/Image.build를 건너뛴다.
다만 기존 builder-source 검사나 installer를 다시 개발할 이유도 없다.
누락된 연결만 실제 SDK로 지나가고 외부 서비스 응답을 대체하면 된다.

**주력: 같은 S1에서 아래 두 경계만 보완.** 성공한 11개 suite 전체 반복은 제외한다.
현재 상태로 원격 재시도하면 시간 만료·image 연결의 미검증을 함께 떠안는다.
전면 재작성은 이미 작동하는 증거를 버리고 범위를 키운다. 즉시 경로를 포기하기에는
남은 질문이 구체적이며, 로컬 검사 몇 분으로 다음 H100 측정 판단을 바꿀 수 있다.
정당한 예비 작업은 한도 내 해결 불가 시 정확한 미충족 조건 closeout뿐이다.
이 작업도 TEST 개선 증거를 만들지는 않는다. 고정 후보의 실행 가능성 측정 전제다.

## 다음 S1에 전달할 완성 프롬프트

이 채팅은 SimulacraBench / HSCC S1 기술 검증이다.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
이 문서의 남은 두 로컬 경계 검증과 필요한 범위 내 수리를 실행한다.
현재 S0에서 실행하거나 다른 세션·서브에이전트를 자동 시작하지 않는다.

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신 3개,
docs/workflow.md를 읽고 실제 역할·개정·허용 범위를 보고한다.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1. 실제 HEAD·dirty·관련 jobs를
확인하며 기존 변경을 보존한다. workflow r5의 같은 세션 수리를 적용한다.

입력:
- 이 문서 전체.
- docs/analysis/A040-outputs/production-lifecycle-repair1/의 closeout.md,
  verification.json, source-manifest.json, regression-history.md,
  sdk-boundary-evidence.md, source.diff, placement.diff, cost-time-ledger.json.
- 같은 폴더의 생산 13모듈, tests_lifecycle.py, fixture_transport.py와 관련 local guard.
- 기존 SDK1.6.0 설치 소스. 이전 builder-source 및 resume5 기록은 필요한 문서만 참고.

기준 source-manifest SHA256:
9bed44512e531215e68c4cc0a2dfd5ea99670a44f4125166eb62999684e624f3.
HEAD만으로 미커밋 소스를 식별하지 않는다. 허용 문서·소스만 해시 확인한다.

목적은 (1) 실제 120초 만료가 중복 생성 없이 정리로 연결되는지,
(2) 같은 SDK 관리 loop에서 실제 Image.build와 Sandbox 경계가 연결되는지 확인하는 것이다.
기존 11개 사례, 과거 builder-source 검증, 실제 종료 확인을 반복하는 작업이 아니다.

작업 위치:
docs/analysis/A040-outputs/production-lifecycle-boundary2/
및 대응 tmp/a040-production-lifecycle-boundary2/를 사용한다.
번호/경로 충돌 시 미사용 경로를 고르고 기록한다. 기존 repair1의 소스·실패·
manifest·latch·검사 산출물은 보존한다. 재사용 소스와 변경 소스를 해시/diff로 구분한다.

허용된 새 영향 검사:
1. 실제 Image.build 성공 연결. Endpoint의 기본 image_builder를 사용한다.
   SDK Image/function/mount/resolver 및 Sandbox hydrate/stream 객체는 유지한다.
   원격 서비스·인증·전송 응답만 작은 protocol 대역으로 제공한다.
   실제 SDK가 요청할 builder source가 controller_core.install_pins와 필요한 허용
   소스에 일치하는지 확인한다. installer 실행·패키지 설치·모델 실행은 하지 않는다.
   생성된 image identity가 Sandbox 생성 요청까지 전달되고, 기존 작은 protocol
   출력 회수·terminal 저장까지 연결되는지 trace로 확인한다.
   완료 image를 직접 hydrate하는 fixture, Image.build 대체 함수로 통과시키지 않는다.
2. 같은 연결의 builder 실패 응답. SDK가 오류를 생산 실행기로 전달하고
   Sandbox create0·과학 명령0이며 허용된 App 정리/실패 기록으로 끝나는지 확인한다.
   필요한 실패 전이만 검사하며 builder의 모든 서비스 상태를 새로 모사하지 않는다.
3. 실제 create-stall 만료. 생산 sandbox_create 120초와 cancel_grace 2초를 유지한다.
   fixture가 즉시 예외를 던지거나 가짜 clock으로 만료를 대신하지 않는다.
   시작·취소 관측·cleanup 진입·exact-ID terminal 저장·프로세스 종료의 시각/경과를
   분리 기록한다. 성공 조건은 명명된 생산 timeout 이후 metadata 정리와 증거 저장,
   중복 create/terminate 없음, boundary/reference/candidate 호출0이다.
   짧은 취소 예외 검사나 감독자 강제 종료만으로 이 사례를 PASS 처리하지 않는다.
   원래 30초 제한의 tests_lifecycle.py를 그대로 실행하지 말고 새 한정 진입을 작성한다.

작은 새 payload bytes/metadata, 입력 Context/명시적 LOCAL_PROTOCOL_FIXTURE 주입은 허용한다.
실제 112 payload나 과학 입력을 재검사하는 작업이 아니다. 대역 위치를 명시하며
protocol 개수·배열 흉내를 실제 예측·Linux/GPU 동작 근거로 기록하지 않는다.
가능하면 생산 13개 의미를 그대로 사용한다. 관련 orchestration/fixture의 실제
결함이 드러나면 최소 수정·영향 검증 후 같은 S1에서 계속한다. 결함과 무관한
모델·installer 본문·pins·과학 runner·seed/head/context/선택·guard/refit·900초는 보존한다.
설치 SDK 패치, assertions 제거, 성공 기대값 완화, 새로운 실행 프레임워크는 제외한다.

시간·자원 계약:
- 전체 45분, 마지막 10분 기록·정리 확보. CPU2/GPU0, 실제 외부 RPC·비용 작업0.
- 새 검사 감독자 wall 합계 420초. 부모가 포함한 자식 시간을 다시 더하지 않는다.
- 일반 짧은 검사는 회수 포함 60초. 50초에 소유 프로세스 종료 절차를 시작하고
  나머지 10초는 회수·기록에 쓴다.
- 120초 stall 검사는 별도 회수 포함 210초. 실제 120초 대기 + cancel grace2초 +
  기존 cleanup 최대60초 + 시작/회수 여유를 포함한다. 200초에 소유 프로세스 종료
  절차를 시작하고 나머지10초를 회수에 쓴다. 실제 wall/잔여 PID를 기록한다.
  감독자 시간은 자식의 정확한 종료 시각과 구분하며, 한도 준수 미입증을 숨기지 않는다.
- 모든 재검사는 남은 합계 안에서만 한다. 성공한 사례는 관련 생산 변경이나
  새 결함으로 기존 증거가 무효화된 경우만 다시 검사하고 이유를 기록한다.
- 매 실행 전 잔여 합계와 closeout 시간을 확인한다. 실행에 필요한 최악 시간을
  수용할 수 없으면 시작하지 않는다. 수정했다고 타이머/한도를 초기화하지 않는다.
- 오류마다 S0 인계하지 않는다. 범위 내 오류는 r5에 따라 보존·수리·영향 검증한다.
  한도 소진·범위 확대 필요·해결 근거 없음이면 정확한 closeout으로 끝낸다.
  예기치 않은 실제 외부 동작 시 신규 동작을 차단하고 사실/가능한 부작용을 보고한다.

인증/RPC 차단은 SDK 진입 전에 설치한다. Windows 소유 loop IPC만 허용하며,
실제 SDK import는 기존 격리 환경에서만 한다. 설치/취득/로그인/계정·billing 조회,
옛 App/Sandbox 재조회·원격 build/전송/생성/H100 실행은 모두 금지한다.
기존 112파일·checkpoint·응답/키/Parquet/NPZ/모델cache/VAF 접근·해시 금지.
fit/predict/score·과학 fixture·성공 suite 무변경 반복·ZIP·S2/S3·tree·E기록·
commit/push·서브에이전트 실행도 금지한다.

종료 조건·산출물:
- 두 경계의 명명된 성공/실패 전이가 실제 SDK trace와 결과로 확인되면
  LOCAL_PRODUCTION_LIFECYCLE_PASS / REMOTE_MEASUREMENT_NOT_AUTHORIZED로 S0에 반환.
  원래 repair1 HOLD를 수정하지 않고 새 증거가 어느 누락을 해소했는지 연결한다.
- 실패/시간 부족이면 해당 경계와 마지막 확인 사실만 기재한 HOLD closeout.
  미완료를 성공으로 바꾸거나 원격 시도로 대신 확인하지 않는다.
- 새 source-manifest·diff/보존 확인, fixture/transport 범위, 실행별 시각·wall·PID·
  종료 증거, 회귀 이력, verification, cost-time-ledger, exposure-ledger,
  closeout 및 s0-handoff.ko.md를 남기고 status/log를 갱신한다.
- 실제 Linux/native 제한·image/현재 계정/payload identity·H100 전체900초·
  실제 효과·release/S2는 계속 미검증이다. 성공해도 원격 실행으로 전환하지 않는다.

장부·상태:
S1까지의 준비17197.7879076초, 과학4process/1077.3504532초를 승계한다.
이번 active wall만 중복 없이 가산한다. 과학·GPU·원격 비용 작업은 새로0이다.
원격 과거 aggregate meteredUSD0.01009897/billed0, 최종 A040 귀속/GPU시간 미확정,
USD1/5 계획·cash0·2400초 예약USD2.965933453125를 유지한다. 계획은 실청구가 아니다.
sb-svFnVI39hH3DpUIZ4Z9LXK 종료 확인은 완료 상태이며 반복 조회하지 않는다.
E041 incumbent/E025 fallback, parked E057/E060/E061, E058 STOP/E059 STOP_SELECTION,
A039 및 모든 STOP/HOLD,17999명/12339SSUID·집계/A022 원래 역할,
E059 소비 oracle1918/1124·selection2007/1130와 보호 audit2074/1177·calibration1866,
A_half 비승격·A018 사용자 미확정·S3 중단·S2 없음 유지.

## S0 읽기·보존 기록

필수 진입 순서의 실제 읽기는 이번 연속 검토의 도구676f0b,
현재 상태 확인297eb5를 승계한다. 명명된 자료 UTF-8 재읽기8d28ac,
소스·검사 대역·entry/preservation 읽기 및 현재13파일 해시 대조를 추가했다.
S1 entry.json의 read_evidence는 S1이 보고한 증거이며 다른 채팅의 로드를 보증하지 않는다.
workflow2026-10-05-r5 SHA256:
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
S0는 SDK import·검사·원격 호출·실험 실행 없이 문서/소스/허용 해시만 읽었다.
S0 기록은 이 문서와 검증 JSON, status/log 추가뿐이다. 원래 HOLD/소스/manifest/tree를
변경하지 않는다. [문서 검증](lifecycle-boundary-review-verification.json)에 전후 해시와
접근 범위를 남긴다.

