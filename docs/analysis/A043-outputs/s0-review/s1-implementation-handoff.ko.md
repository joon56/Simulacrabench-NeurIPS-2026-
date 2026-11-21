# 다음 S1 — E064 조건부 gradient 차단 구현·합성 기술 검증

S0 권고문. 작성 자체는 실행 허가가 아니다. 사용자가 별도 S1에 아래 본문을
실행 지시로 전달할 때만 적용한다. 이전 A043 정보 조사 인계 대신 이 문서를 사용한다.

```text
SimulacraBench / HSCC — 이 별도 S1에서 A043 고정 계약의 구현·합성 기술 검증을 실행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

1. 진입·기준
AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md를
실제로 읽고 현재 개정·S1 bounded exploratory technical scope·허용 범위를 보고한다.
HEAD/branch/dirty/named jobs를 확인하고 사용자 변경을 보존한다. r5 일반 오류 수리는
같은 세션에서 처리한다. 이 채팅을 지정한 사용자 지시를 entry에 기록한다.

필수 입력:
- docs/analysis/A043-outputs/s0-review/{decision.md,entry.json,verification.json}
- docs/analysis/A043-outputs/s1/{contract.md,closeout.md,verification.json,s0-handoff.ko.md}
- docs/analysis/A043-post-e063-priority.md
- docs/analysis/E063-outputs/freeze-01.json (문서로만 읽고 아래 허용 목록만 취함)
- docs/analysis/E063-outputs/{implementation-contract.md,verification.json}
- docs/experiments/E012-shared-trunk.md, E061-tied-content-heads.md,
  E063-round-conditioned-metric.md와 E063 사후 result.ko.md
- src/models/shared_trunk.py, supervised_retrieval.py, link_sharp.py, hh_cap.py,
  tied_content_heads.py 및 직접 필요한 기존 import source
- scripts/check_e063_round_metric.py, tests/test_round_metric_retrieval.py는
  harness 구조 참고용 텍스트만. 기존 성공 suite/arm을 실행하지 않는다.

A043 S1 contract SHA256:
f4ec8f24d394cd94d4baf1a58fe40fe9c6bf3ddc5a6d12865bbe9c2b9d41563e
원래 shared_trunk SHA256:
df648763c8e0ba5532ebf9e437af95cd10d8527112c1338b8b5db9ad6a212e1f
R supervised_retrieval SHA256:
2940338c5378de03303befb74e3834fbad631c0eb18f4ecb55d2cc39a471f879
기타 source는 S0 entry/current source identity로 확인한다. 차이는 경위를 기록하며
과거 manifest에 맞춰 되돌리지 않는다. S1 설치 Torch version/optimizer 텍스트 근거를
실제 import·동작 검증으로 확대하지 않는다. 현재 기존 .venv만 사용, 새 설치 없음.

2. 목적·등록
독립 asked-only head를 계속 학습시키되 conditional CE의 trunk 직접 gradient만
차단하는 고정 H 하나를 구현한다. 기존 E061 tying/모듈 제거, E063 round metric과
다른 경로다. 실제 gradient 충돌·이득은 미확정이며 E012/E061 반대 근거를 유지한다.
E064와 conditional_gradient 파일명 충돌을 먼저 재확인한다. 비어 있으면 새
docs/experiments/E064-conditional-gradient.md와 불변 registration을 실행 전에 작성한다.
이미 사용 중이면 덮어쓰거나 임의로 번호를 바꾸지 말고 충돌 내용을 S0에 반환한다.

허용 새 파일:
src/models/conditional_gradient.py
tests/test_conditional_gradient.py
scripts/check_e064_conditional_gradient.py
docs/analysis/E064-outputs/** 및 위 실험 기록, status/log 결과 추가.
필요한 harness/helper는 새 E064 경로 안에 한정한다. 원래 모델·실험·snapshot·tree는 보존.

3. 고정 개입
A043 contract 1~4절 그대로. 원래 _Net constructor/파라미터 순서/seed0/RNG/단일
trunk forward/dropout/full·conditional logits/CE/N을 유지하고 cond 입력 z만 detach한다.
Cond head requires_grad 유지, full 경로 detach/no_grad·head freeze·trunk 재실행 금지.
UNHCR tune_fn local 사본만 연결하고 UNICEF/WB는 원래 R 직접 호출한다.
원래 _train_on/_train/tune 제어 흐름을 연결하며 source global monkeypatch는 금지한다.
Config2, Adam/split/early-stop/outer config/w/final refit, ladder/metric/renderer,
lambda minimum30/zero fallback을 유지한다. Epoch/config/w/lambda 산출값은 달라질 수 있다.
추가 refit/selector/seed/head/context/loss 계수/threshold/tolerance 탐색은 없다.

Metric weights·section activity·donor/replay 자격·concentration·ladder/agreement는
동일 input/runtime에서 기대 불변이다. Lambda와 최종 출력은 다를 수 있다.
양쪽 실제 계산값을 검증하고 과거 값으로 덮어쓰지 않는다. Lambda가 비어 held-query
evidence를 생략한 arm은 생략으로 기록한다. 대응 경로 미실행을 donor 변동으로 부르거나
진단을 위해 추가 전체 예측을 하지 않는다. Metric activity와 lambda activity를 구분한다.

4. 허용 입력·정보 경계
작은 고정 인공 tensor/row는 새 영향검사에만 허용한다. 과학 입력은 기존 세 synthetic
external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet만 허용한다.
현재 bytes를 읽기 직전 확인할 기록상 SHA256은 순서대로:
unicef 8e7c659d277c5145c7a8a6d055ac59a7dd3c35699317741239b6b1969bce1488
world_bank 4592bed873410c5248edf1205e5cab41dd30494926e3b49f8da598e266758c8a
unhcr 5d00075706e0a7beafdc8a70acfe07cde1f489048741eb2f3ae1fababdb72774
이 값은 S0의 새 데이터 재해시 결과가 아니다. 불일치하면 재생성/대체하지 않고 HOLD.
공식 공개 schema/config와 sample_rows/normalization/floor/skill source를 사용한다.

Parquet은 TRAIN/DEV role filter와 필요한 columns로 읽고 TEST 행은 materialize하지 않는다.
Model worker에 TRAIN 답변과 DEV GIVEN만 전달한다. DEV의 모든 PREDICT를 model entry
전에 mask하고 EXCLUDE feature를 차단한다. 각 worker는 DEV truth를 요청하지 못한다.
DEV truth는 fresh R/H 여섯 raw 파일·source/input identity가 동결된 뒤 별도 evaluator만
요청한다. 공식 함수로 각 raw를 한 번 평가하고 같은 truth/order/floor.001을 적용한다.
새 E064가 생성한 raw/cache만 자신의 검증에 읽을 수 있다. 이전 raw/NPZ/모델 cache,
실제 Adult/SIPP/VAF/UNCHR_data·원천키·보호 audit/calibration은 읽거나 재해시하지 않는다.
기존 세 synthetic의 재생성·대체, seed 변경·TEST 평가·외부 취득 없음.
위 작은 고정 인공 입력은 영향검사에만 쓰며 새 full-size 합성 데이터셋을 만들지 않는다.

5. 새 영향검사와 전체 경로
본 실험 전 등록·새 코드/입력/환경/검사/판정/한도 freeze를 완성한다.
고정 fixture와 tolerance를 미리 정하고 A043 contract 7절의 영향검사만 실행한다:
- 두 config 초기 parameter/state/order/RNG, train/eval/dropout의 forward·CE/N parity.
- Float64 nondegenerate asked fixture에서 분기별 gradient atol/rtol1e-10.
  H trunk=L_F/N, R trunk=(L_F+L_C)/N; 초기 full/cond head gradient 동일.
  전체 CE ordinary finite difference를 stop-gradient의 기준으로 쓰지 않는다.
- 독립 cond head nonzero gradient와 Adam 1step 갱신, None/zero·empty asked·K1 구분.
  H conditional-to-trunk zero는 의도한 계약이며 NO_OP 실패 기준이 아니다.
- 실제 factory/tune hook의 config2/final refit 연결, masking/정보 경계, 원래 fallback.
  Mock이 핵심 변경 경로를 생략한 결과를 production 검증으로 쓰지 않는다.

영향검사 통과 후 fresh R all3 1회, fresh H all3 1회 순차 실행한다.
기존 성공 R/H 재실행이 아니라 새 H와 같은 입력/환경의 이번 비교기다.
UNICEF17856/WB39520/UNHCR132273, 총189649 vectors/arm의 shape/order/finite/
nonnegative/positive sum·최대 sum 오차1e-6을 확인한다. UNICEF/WB raw exact0.
UNHCR 전체 raw 차이·metric 불변 경계·w/NN 사용·lambda/최종 부모·자식 출력 및 비용을 기록한다.
새 subgroup/gradient-conflict 진단·head별 성능 탐색·결과 기반 fixture 추가는 하지 않는다.
R source를 clean 제출 snapshot과 새로 실행 parity 인증했다고 부르지 않는다.

6. 자원·수리
Gross120분, 마지막10분 기록 포함. Computational child 합1800초; 새 작은 검사 합300초
(1800 안에 포함), 작은 child 각60초. 각 all3 import/세 기관/출력 포함 shared900초.
CPU numerical threads2/GPU0/heavy1; owned process tree RSS/private 각각8GiB.
Import 전 외부 watchdog, absolute+monotonic deadline, <=1초 sampling과 최대 gap 기록,
자기 process tree만 종료. 남은 총량/기록 예비시간으로 더 짧은 deadline을 적용한다.
자식 아래 중첩 process 시간을 다시 더하지 말고 wall/호출/실패·검사 비용을 구분한다.
정상 full-path6pipeline/18neural/16metric, refit 포함. 작은 gradient/optimizer 검사 별도 계수.

일반 구현 오류는 같은 세션에서 최소 수리·영향 경계만 재검증하고 계속한다.
무효 scientific arm의 재시작은 전체 최대1회, 정상2회 포함 절대3all3/9pipeline/
27neural/24metric 및 위 시간 한도 이내다. 실패 산출물/latch/source freeze를 보존하고
수정 근거·새 freeze를 남긴다. 성공 arm은 반복하지 않는다. NO_OP/하한 실패/w 선택 등
유효한 결과, 자원 한도 초과, 데이터/정책 위반을 수리 예비로 구제하지 않는다.
부분 예측 이어붙이기·동결 결과 삭제·한도 초기화·CUDA fallback/원격 전환 없음.

7. 판정·종료
LOCAL_TECHNICAL_PASS_FOR_S0: 모든 영향/정보/초기/control/기대 불변/확률/자원 조건 통과,
UNHCR raw>=1변화, 기관별 H-R skill>=−.002. 합성 개선이나 +.005는 필수 조건이 아니다.
실제 효능·독립 audit·DEV 채택·S2 qualification은 아니다.
전체 exact R이면 STOP_NO_OP. 하한 실패 REGRESSION_HOLD, 연결/정보/유효성 실패
TECHNICAL_FAIL, 자원 초과 RESOURCE_LIMIT, 미완료 INCOMPLETE로 구분한다.
유효 결과를 보고 seed/head/tolerance/정책을 바꾸지 않는다.
예비 작업은 실패·소비 예산·정확한 재개 입력의 closeout뿐이다.

산출물: 새 실험 등록/불변 registration, implementation-contract, freeze/manifest,
새 검사와 실패·수리 기록, R/H raw/비교·자원·호출 장부, exposure-ledger,
verification, closeout, s0-handoff.ko.md. Status/log 결과만 추가. S0 검토로 반환한다.
S2 인계문/ZIP 제작을 자동 시작하지 않는다. S2에는 clean E025 기관별−.002/E041 비교,
source/assembly/extracted parity·ZIP checker·official all3/shared900초·메모리·bytes·
사전 SCORES가 남는다. 정상 전체15/45/32와 S2 추가3600초는 후속 설계일 뿐 권한 아님.

관측 한계: no fresh oracle/current E041 loss map. 기존 base/refit의 S/L 재사용,
in-sample full-proxy replay 유지. Synthetic은 노출된 공학 채널이다. 향후 hosted arm은
A043 contract8절처럼 공개 favorable/adverse/unresolved/technical/HOLD로 기록하며,
score precision과 실제 효과를 혼동하지 않는다. 반대 방향·controls 변화는 mixed/HOLD,
필수 필드/출처 부족도 HOLD. 자동 승격·동일 정책 반복 제출 없음.

금지: 기존 모델/기록/제출 snapshot/tree 수정, generic 성공 suite 반복, 추가 후보,
보호 데이터/기존 cache/TEST, 설치·웹·원격·GPU·플랫폼·ZIP·업로드·commit/push·
서브에이전트·S3/TEST 선택. E041 incumbent/E025 fallback, E057/E060/E061/E062/E063
parked/E062·E063 UNRESOLVED, E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/
A039/A040/all STOP/HOLD 유지.17999/12339·집계·A022 원래 역할, E059 소비1918/1124·
2007/1130와 보호2074/1177·calibration1866, A_half 비승격/A018 미확정/S3 중단 보존.
```
