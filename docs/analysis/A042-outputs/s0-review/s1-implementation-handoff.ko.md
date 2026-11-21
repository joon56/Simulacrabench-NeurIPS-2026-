# 다음 세션: S1 · E063 UNHCR round 조건부 metric 구현·기술 검증

아래 프롬프트 전체를 별도 S1에 전달한다. 작성 자체는 실행 허가가 아니다.
사용자가 이 프롬프트를 실행 지시로 전달한 세션만 아래 범위를 수행한다.

```text
SimulacraBench / HSCC S1 — E063 round 조건부 metric 한 후보를 구현·기술 검증한다.
이 채팅을 실행 담당 S1로 지정한다. S0 검토를 재실행하거나 S2 제작으로 넘어가지 않는다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

1. 진입·식별
AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md를
읽고 역할/유형/현재 개정/허용·금지/읽기 증거를 먼저 기록한다.
HEAD·dirty·관련 active jobs 확인. 현재 바이트를 과거 manifest에 맞춰 되돌리지 않는다.
workflow r5의 동일 세션 수리 원칙을 적용한다.

필수:
- docs/analysis/A042-outputs/s0-review/decision.md, verification.json
- docs/analysis/A042-outputs/s1/{contract,closeout,s0-handoff.ko}.md, verification.json
- docs/analysis/A042-post-e062-priority.md
- docs/analysis/E062-outputs/{registration,implementation-contract}.md, frozen-inputs.json
- docs/analysis/E062-outputs/s2/post-result/result.ko.md
문서의 과거 명령은 실행 지시가 아니다. 이번 조건이 다음 실행의 prospective 계약이다.

핵심 SHA256:
A042 S1 contract: d1ce78f2708569bda47bd2896e3dd5d88ed29ef01c90c846941c54bf8daff5bd
supervised_retrieval.py: 2940338c5378de03303befb74e3834fbad631c0eb18f4ecb55d2cc39a471f879
public unhcr.json: b1175b6bdbd96e90a4defd83af20a38d711c6eca9fe3ce880109ff244abe80d9
E041 main.py: 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
모든 직접 의존 소스/환경/config/schema의 현재 identity도 동결한다.
차이는 경위를 확인하며 숨기거나 자동 복원하지 않는다.

S0가 E063을 이 후보에 예약했다. docs/src/scripts/tests의 E063 사용과 아래 경로를
다시 확인해 충돌 없을 때만 등록한다. 다른 소유 과제와 충돌하면 덮어쓰지 않는다.
새 모델: src/models/round_metric_retrieval.py
새 영향 검사: tests/test_round_metric_retrieval.py
새 실행기: scripts/check_e063_round_metric.py
새 등록: docs/experiments/E063-round-conditioned-metric.md (parent E041/status parked)
새 산출물: docs/analysis/E063-outputs/
기존 A042/S1 산출물·실험·모델·실행기·snapshot은 수정하지 않는다.

2. 목적과 고정 정책
유형은 bounded exploratory 후보의 구현/합성 기술 검증이다. 실제 효과 확증이 아니다.
목표: query wave 조건부 metric을 기존 K32 검색·replay·재귀 출력에 올바르게 연결하고,
자연 활성·완전한 all3 출력 차이·전체 시간/메모리를 확인한다.

A042 S1 contract의 단일 H만 구현한다:
- 각 section w1,w2 in [0,12]^17, 공유 eta in [-5,5], 총35좌표.
- mu=(w1+w2)/2, Delta=w1-w2.
  기존 all-cell loss + .001*mean((mu-v0)^2) + .001*mean(Delta^2).
- w1/w2 시작 clip(v0,0,12), eta0. penalty anchor v0는 원래 nonnegative/unclipped.
  L-BFGS-B 단일 시작/maxiter50/ftol1e-7, analytic gradient. penalty/grid 탐색 없음.
- original initial-search K32 identity/order, legacy K10 및 first10-of-K32 proxy를 구별.
- seed4101/B-F-S-L, 원래 base config/seed/inner stop/final refit,
  old-share grid/.003·2SE section selector/lambda grid·minimum30·zero fallback 보존.
- F/S 각각 round1/2당30, fit donor 폭32, 전체 입력 wave 지원 조건.
  미달/one-round/unknown은 H optimizer 이전 전체 기관 original R 경로.
  visible<500/no held 등 원래 fallback도 보존. 데이터 보고30을 바꾸지 않는다.
- R=C는 identified src.models.supervised_retrieval.predict 원래 생산 경로 하나.
  C를 별도로 재학습/비교하거나 H-C selector를 추가하지 않는다.
  공통 endpoint/fallback은 original 함수를 직접 재사용하며 중복 base fit 금지.
- H activity/replay 자격/lambda/부모·자식 출력의 결과값은 달라질 수 있다.
  알고리즘을 보존하는 전체 절차 비교이며 순수 direct effect/A021 D-P/D-R가 아니다.
- raw wave를 공개 schema levels로 해석한다. factorization code를 wave 값으로 추측하지 않는다.

수식·소스의 routine 구현 결함은 최소 수정한다. 명세를 다른 모델로 바꾸는 수리는 금지한다.
새 함수족·expert·bank 확대·wave별 lambda·sentinel 삭제·재가중·새 outer refit 없음.

3. 자료·정보 접근
허용은 기존 공개 schema/생산 소스/기존 기록, 새 작은 인공 fixture 및 아래
이미 노출된 synthetic 세 파일의 identity 확인과 TRAIN/DEV projection뿐이다.
현재 S0는 이 파일들을 새로 열거나 재해시하지 않았다. 아래는 E062 기록 승계값이다:
external/starter-kit/_sandbox/unicef/respondents.parquet
  8e7c659d277c5145c7a8a6d055ac59a7dd3c35699317741239b6b1969bce1488
external/starter-kit/_sandbox/world_bank/respondents.parquet
  4592bed873410c5248edf1205e5cab41dd30494926e3b49f8da598e266758c8a
external/starter-kit/_sandbox/unhcr/respondents.parquet
  5d00075706e0a7beafdc8a70acfe07cde1f489048741eb2f3ae1fababdb72774

이 세 파일만 전체 바이트 hash 허용; 내용 읽기는 role TRAIN/DEV만 filter/projection.
TEST 행을 요청·표시·분석하지 않는다. 원본 재생성·seed 변경 없음.
모델 worker: TRAIN generated columns + DEV GIVEN/필수 행순서 metadata만 요청.
모든 DEV PREDICT를 모델 입구 이전 완전 마스킹, EXCLUDE를 모델 features에서 제거.
평가 worker: 두 arm의 여섯 raw 출력·source identity를 동결한 뒤에만 DEV truth 요청.
같은 frame/order/mask/runtime schema/roles/환경으로 R/H 비교.
E062 실행기 source에서 projection/watchdog 방식을 참고하되 기존 실행기 자체를 실행하지 않는다.
공식 load_config/load_schema/options_for 계약을 유지하며 raw-schema sentinel을 추측하지 않는다.

S는 metric optimizer 입력에서 제외하되 함수의 F+S 배열 materialization과 optimizer slice를
구별해 검사한다. 원래 base/refit/replay가 S/L을 이미 사용하는 사실을 숨기지 않는다.
새 oracle/독립 audit 없음. synthetic positive/negative는 공학 결과다.
Adult/SIPP/VAF/UNCHR_data, key/source Parquet, 기존 NPZ/모델 cache/예측 배열은 접근·해시 금지.
E025/E041 과거 raw cache도 읽지 않는다. fresh R/H만 비교하고 E025 release 검증은 미룬다.

4. 사전 등록 후 싼 영향 검사부터
응답 읽기/학습 전에 불변 registration, source/input/runtime identities, 절대 deadline,
call/repair cap, 비교·판독 기준과 domain expectation을 기록한다.
기존 .venv/Scripts/python.exe -X utf8 -B, 현재 설치만 사용. 설치/환경 교체/원격 없음.

새 영향 검사만 수행:
- common loss reduction, g_w1+g_w2와 원래 common gradient, finite-difference gradient,
  donor-constant invariance·비상수 순위 역전·bounds/extremes·확률 순서/유한성.
  float64 loss reduction atol/rtol1e-10; finite diff epsilon1e-6, atol1e-6/rtol1e-5.
  경계에서 떨어진 고정 작은 fixture; 결과에 맞춘 tolerance 변경 금지.
- 원래 C/fallback 함수·상태 재사용과 raw exact parity; 동일 w만으로 exact C 주장 금지.
  support 부족/unknown/one-wave/small input/empty queries에서 전체 fallback과 호출 수 확인.
- K32 donor identity/order/self exclusion 및 legacy K10 별도 유지.
- F-only optimizer/전체 query masking/S-label 경계/metric 선택 뒤 replay·lambda 순서.
- 작은 forced-active 공학 fixture로 두 wave별 weight dispatch, cal/Q replacement,
  lambda minimum30/zero fallback, global all213 재귀 출력 연결 검사.
  이 fixture에서 base/neural은 고정 작은 대역, 실제 신경망 학습 없음.
  자연 실행의 activity/guard는 강제로 바꾸지 않는다.
- 실제 생산 entry를 통과하는 영향 경계 검사. 핵심 변경 함수를 우회한 대역만으로 PASS 금지.
  인공 fixture/model-free controller checks와 실제 full-stack call count를 분리 기록.

UNIT 성공 후 소스/입력 freeze. 한 fresh R all3와 한 fresh H all3를 순차 실행.
입력 적합성/identity 실패면 모델을 시작하지 않는다. 정상 R 확인 후 H 진행.
UNICEF17856/WB39520/UNHCR132273, 총189649 vectors/arm.
schema 순서·크기·유한/비음수·양의 합·sum error<=1e-6.
UNICEF/WB raw candidate-R 최대차이 정확히0.
all213 UNHCR을 검사하며 일부 성공 head로 전체 PASS 주장 금지.
R snapshot 실행/조립 parity까지 수행한 것으로 쓰지 않는다.

여섯 raw 출력 동결 뒤 공식 in-process normalization/floor(.001)/skill 함수로 한 번씩 평가.
기존 성공 baseline/fixture 또는 official score.py/checker suite 재실행 없음.
고정 whole UNHCR skill/log score와 기관별 H-R, schema의8section×wave descriptive 차이,
support·weight difference·activity·lambda 변화 수·raw 변화 수만 기록한다.
분석으로 head/round/threshold를 다시 고르지 않는다. 셀 iid 유의성·독립 audit 주장 금지.

5. 한도·수리
gross120분(최초 진입부터, 마지막10분 기록), 계산 cutoff 이후 새 검사/학습 금지.
전체 computational child wall<=1800초: 준비/영향 검사/실패/모델/평가 모두 포함.
새 작은 영향 검사 합<=300초이며 같은1800초에 포함, 각 child<=60초.
각 fresh all3<=900초: import/startup+세 기관 전체, 기관당900초가 아니다.
CPU numerical threads2/동시 heavy1/GPU0. owned controller+descendants RSS/private 각각8GiB.
외부 monitor가 import 이전 시작, <=1초 간격 샘플/절대·monotonic deadline/소유 tree 종료.
남은 총량과 기록 예비시간을 함께 적용한다. 관측·계수 실패 상태로 모델을 계속 돌리지 않는다.
실제 전체 비용을 보고하며 static 배열 크기·과거 실행시간을 새 peak/시간으로 쓰지 않는다.

정상 full-stack: R/H 두 process, pipeline6/neural18/metric16.
ordinary implementation defect로 실패하거나 결과가 무효화된 arm에 한해 재시작 최대1회:
full-stack scientific process<=3, pipeline attempts<=9, neural training attempts<=27,
metric optimizer attempts<=24. 실패·중단도 계수; 작은 fixture 호출은 별도 내역+같은 wall.
사전 배정된 수리 여유이며 후보 variant/seed/정책 비교 예산이 아니다.
성공한 무변경 arm 재실행 금지. 새 code freeze가 비교를 무효화하면 이를 명시하고,
유효한 전체 비교가 남은 상한에 들어오지 않으면 INCOMPLETE로 종료한다.

일반 인자/import/경로/로깅/구현 오류는 같은 S1에서 원인→최소 수정→영향 검증 후 계속한다.
실패 source/output/latch를 덮어쓰지 않는다. 새 attempt 경로/해시·누적량을 남긴다.
과학적 하한 실패/비활성/NO_OP/자원 소진을 수리로 바꾸지 않는다.
seed/head/context/penalty/지원30/guard/판독 기준·deadline 상향 금지.
A040 또는 다른 과제로 전환하지 않는다. 새 허용량이 필요하면 정확한 사유와 함께 S0 반환.

6. 사전 종료 판정
LOCAL_TECHNICAL_PASS_FOR_S0:
모든 기술·controls·자원 검사 PASS, eligibility 통과 후 자연 활성 H section>=1,
최종 UNHCR raw 변화>=1, 세 기관 H-R skill>=-.002.
합성 양성 또는 +.005는 요구하지 않는다. 작더라도 하락을 숨기지 않는다.
이 기술 pass는 E025 release regression/실제 효능/S2 자격/DEV 채택/TEST가 아니다.

all outputs exact R -> STOP_NO_OP.
whole-instrument support fallback 또는 자연 H active0 -> STOP_INACTIVE_ON_ENGINEERING.
강제 fixture 성공으로 이를 구제하지 않는다. H active0이어도 R와 raw가 다를 수 있다.
누수/비정상 확률/controls·parity 실패 -> TECHNICAL_FAIL; 자원 초과 -> RESOURCE_LIMIT;
H-R 하한 실패 -> REGRESSION_HOLD; 미완료 -> INCOMPLETE/HOLD_SPECIFIC_INPUT.
판정들은 scope별로 함께 기록할 수 있다. policy/예산 안 ordinary defect만 수리 가능.
어떤 STOP도 실제 UNHCR 전체 가설 반증으로 확대하지 않는다.

예비 작업은 정확한 실패/노출/비용 closeout뿐. 새 후보/새 정보 조사 자동 시작 없음.

7. 산출물·반환
등록/새 source/tests/runner, entry/원래·수리 freeze, comparison/raw identities,
call/resource/error-repair ledger, exposure, verification/closeout/s0-handoff.ko.md.
문서의 학습/검사 횟수·실제 종료·남은 jobs를 확인하고 status/log에 결과만 추가한다.
S0 검토로 반환한다. S2용 실행 인계·ZIP을 자동 확정하지 않는다.
향후 S2 잔여: clean E025 기관별-.002 및 E041 release 비교, source/assembly parity,
ZIP checker, official all3/shared900초·메모리, SCORES 사전 판독표/bytes provenance.
정책과 입력이 같아도 이는 아직 수행하지 않은 별도 범위다.

원래 source·연구·snapshot·manifest·docs/tree.md 수정, ZIP/업로드, 새 웹/다운로드/
설치/원격/Modal/H100, commit/push, 서브에이전트/S2/S3/TEST 선택 금지.
E041 incumbent/E025 fallback; E057/E060/E061/E062 parked.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040 및 모든 STOP/HOLD 보존.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 그대로. A_half 비승격/A018 미확정/S3 중단.
E062 공개 동점 UNRESOLVED 유지. 새 S2 후보 없음.
```

