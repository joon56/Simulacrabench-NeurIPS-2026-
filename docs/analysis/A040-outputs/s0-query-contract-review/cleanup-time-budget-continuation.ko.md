# A040 — 종료 조회 시간 계약 보완과 S1 계속 작업

2026-10-05 KST. S0 문서 검토. workflow2026-10-05-r5.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1.
workflow SHA256 a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.

## S0 판단

S1의 STOP_TERMINATION_UNCONFIRMED /
REMOTE_WINDOW_EXHAUSTED_BEFORE_QUERY를 수용한다. S1은 r5에 따라 같은 세션에서
오류를 고쳤으며, 정해진 절대 deadline을 임의로 늘리지 않았다.

첫 helper는2026-10-05T12:14:19.5405169Z 시작,0.756681초 뒤 인증 전에 실패했다.
수정 후 실제 SDK synchronizer 진입 검사는 통과했다. 그러나 기존
12:16:19.5405169Z 종료 창의30초 예비시간만 남아 두 번째 실행은 시작되지 않았다.
새 인증/조회/종료/billing0은 기록·source 흐름에 따른 판단이며 패킷 캡처 주장은 아니다.
로컬 검사3.1790341초. 앞19개 case는 trace 순서에 따른 추론이며 개별 PASS19개가 아니다.
수정 helper/지정 기록의 허용 해시는 source-manifest와 일치한다.

기존120초는 로컬 수리 중에도 계속 흘렀다. 이는 실제 조회량을 제한하려던 목적과
맞지 않는 S0 시간 설계였다. 과거 창 소진 기록은 보존한다. 다음 작업에는 새
한정된 허용량을 명시하며, 실제 helper 실행 시간을 누적으로 계수한다.
로컬 준비/수리는 전체 세션 시간에 포함하고 그 사이에 원격 시간을 소진시키지 않는다.
이 방식은 이번 기존 자원 정리 전용이다. GPU/과학 실행의 연속 deadline을 바꾸지 않는다.

수정 helper를 재사용해 종료 조회를 수행할 가치가 있다. 새 연구 가설·대규모
controller 수리·성공 suite 반복을 제안하지 않는다. 종료/최종 비용은 여전히 미확정.
다음 프롬프트를 사용자가 같은 S1에 전달해 실행을 지시할 때만 새 범위가 활성화된다.

## 같은 S1에 전달할 실행 지시

기존 종료 확인 작업을 계속한다. AGENTS/CLAUDE/status/log 최신3개/workflow r5와
이 문서를 읽고 실제 개정·역할·허용 범위를 보고한다. HEAD/dirty/관련 jobs를
확인하고 기존 변경·실패·과거 window/manifest를 보존한다.

입력은 docs/analysis/A040-outputs/termination-query-repair1/의 closeout.md,
regression-history.md, closeout-terminal-status.json, verification.json,
source-manifest.json, cost-time-ledger.json, confirm_terminal.py, entry-repair.diff다.
수정 helper SHA256:
0e68a80ce1237aaa0f95d42777a24154b5cee110858e0bf0a692c17a2d75939a.
기존 SDK1.6.0·인증·로컬 통과 기록을 재사용한다. 재설치/재로그인/성공 suite 반복 금지.

목표는 다음 기존 자원의 정확한 ID·terminal·관측 시각을 확보하고, 살아 있으면
그 자원만 종료하는 것이다:
workspace joon56 / environment main
App ap-XiMVzlJgrNrCiFpIN1kB4W
App name a040-resume5-20261005-094405
Sandbox name a040-resume5-20261005-094405-gpu

이번 새 범위의 한도:
- 전체30분, 종료 기록5분 확보. 필요한 새 영향 검사만 합180초/각30초, CPU2/GPU0.
- 모든 실제 helper 자식 실행 시간의 합120초. 시작/초기화/인증/응답 대기/
  취소/종료 확인까지 자식이 살아 있는 시간을 포함한다. 여러 process에 나누더라도
  이미 사용한 시간을 차감한다. 프로세스 밖의 로컬 수리는 전체30분에 포함한다.
- RPC마다15초 이하. 누적 원격120초 중 마지막30초는 읽기 확인/receipt에 확보한다.
  잔여량이30초 이하이면 새 탐색/종료 요청 금지. 확보된 정확한 ID의 terminal
  확인 등 필요한 읽기만 잔여량 안에서 수행한다.
- 전체 작업에서 정확한 Sandbox 종료 요청 최대1회. 새 자원/build/GPU/과학 실행0.
  과거 소진 창을 삭제/갱신하지 않고 이번 새 허용량과 역사적 사용량을 따로 기록한다.

로컬 준비·허용 소스 identity 확인을 마친 뒤 실제 helper를 시작하기 직전에만
그 호출의 남은 deadline을 만든다. 같은 세션의 수리 시간 동안 고정된 원격
wall-clock 창을 계속 흘려보내는 방식은 이번 범위에서 사용하지 않는다.
이 변경을 공짜 시간이나 무제한 재시도로 해석하지 않는다. 전체30분과 누적120초,
각 호출15초를 모두 지킨다.

새 termination-query-run2 출력 경로에 보존용 원본과 시도별 기록을 구분한다.
수정 helper의 조회/identity/version/terminal 판독 본문은 우선 그대로 재사용한다.
부모 실행기의 잔여 시간/출력 경로/누적 장부 연결만 최소 구현한다. 각 시도 직전
허용 소스 hash와 잔여량을 기록하고 실제 자식 wall을 차감한다.
이미 성공한 wrapper/protobuf/SDK 진입 검사를 통째로 반복하지 않는다.
새 시간 계수 연결이 필요하면 예산 차감·소진·중복 종료 차단에 대한 영향 검사만 한다.

r5대로 일반 구현 오류는 같은 세션에서 수정·관련 검증 후 계속한다.
단, 재진입 전 이전 receipt/실패 단계를 확인한다. 종료 요청이 기록됐거나
발송 여부가 불명확하면 전체 helper를 재실행해 종료를 중복시키지 않는다.
그때는 정확한 기존 ID에 대한 읽기 확인만 허용한다. 인증/권한 모순·대상 불명확·
한도 소진은 숨기지 않고 중단한다. 어떤 경우에도 새 자원을 만들지 않는다.
잔여 자식이 없고 외부 동작이 진행 중이지 않을 때만 로컬 수리 구간으로 전환한다.

명시적인 exact-ID terminal 결과를 먼저 저장한다. billing은 남은 범위에서
정상 요약 조회만 한다. 집계/게시 지연/귀속 미확정과 실제 terminal을 구분한다.
App STOPPED/task0, ACK, NotFound, active-list 부재, 시간 경과는 종료 증거가 아니다.
종료가 확인돼도 생산 controller/H100 작업으로 넘어가지 않고 S0에 결과를 반환한다.

산출물은 이번 작업 폴더의 entry·소스/diff·시도별 사용량/receipt·최종 terminal/
billing·closeout·S0 인계와 status/log 갱신이다. 작은 오류마다 새 인계문을 만들지 않는다.
해결 불가하면 실제 누적 사용량과 정확히 남은 증거/공식 상세 화면 항목만 적는다.
재개 비용/시간 장부 기준: 준비13951.7380878초, 과학4process/1077.3504532초.
겹친 시간은 중복 합산하지 않는다. 기존 USD1/5 계획/cash0, 집계0.00178978USD와
2400초 예약2.965933453125USD, 게시/귀속 미확정은 유지하며 실제 청구로 바꾸지 않는다.

금지: 모델/응답/키/Parquet/NPZ/cache/checkpoint/VAF/payload 접근·재해시,
fit/predict/score, 새 paid resource/build/H100, 생산 controller 수리,
ZIP/업로드, commit/push/tree 수정, 서브에이전트·S2/S3/TEST 선택.
E041/E025·parked E057/E060/E061·모든 STOP/HOLD/E058/E059/A039,
17999/12339·집계/A022 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 미확정/S3 중단 유지.

## 이번 S0 접근·보존

현재 지침 읽기 승계 후 최신 status/log3개, 필수 종료 자료와 helper/entry source를
읽었다. 도구 근거 acd076/4bf1cc/aca1f9/be963f/270bfb/b9fb73.
HEAD 불변, dirty89, 이름으로 확인한 python/pythonw/uv 로컬 jobs0.
원격 부재를 확인한 것은 아니다. 이 S0는 문서만 작성했고 실제 SDK import/RPC/
수리/검사/모델/데이터/ZIP/commit/push0. 기존 실패 원본·workflow r5는 보존한다.

문서 검증: 지정 원본9개와 workflow/tree 해시 불변. status/log의 이번 추가를
제거하면 직전 UTF8 BOM/CRLF 바이트 해시가 복원됨. 새 문서 경로 확인 완료.
기존 source-manifest의 자기 해시 제외8개 항목 일치; payload나 모델은 미접근.

