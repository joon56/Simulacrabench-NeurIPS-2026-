# A043 S1 — UNHCR conditional gradient 경로 계약

2026-10-11 KST. **CONTRACT_READY_FOR_S0_REVIEW.**
정적 소스·수식 설계 판정. 모델 구현·효과·release PASS·후속 실행 허가가 아니다.
이 계약은 독립 conditional head를 유지하면서 그 CE의 **trunk 직접 gradient만**
차단하는 한 개입 H를 정의한다. R은 현재 `supervised_retrieval.predict`다.
현재 E041 손실 지도, gradient 충돌, 회복 가능한 점수는 확보하지 않았다.
R의 source 경로를 추적한 것이며 E041 제출 snapshot/원격 bytes와의 실행 동일성을
이번에 인증한 것은 아니다. 그 source/release identity는 후속 별도 검증 조건이다.

## 1. 구현 경계와 같은 상태에서의 계약

UNHCR 판별과 UNICEF/WB delegation은 원래 E041 entry를 따른다.
UNHCR은 기존 `link_sharp.predict`의 `tune_fn` hook만 새 local tune 함수로 연결하고,
`layer_fn=supervised_retrieval.supervised_layer`, `configs=hh_cap.CONFIGS`,
`extra_fn=None` 및 원래 renderer를 유지한다. 다른 기관은 original R 직접 호출.
기존 production source/global 함수 교체·monkeypatch·별도 base 중복 fit은 하지 않는다.

`shared_trunk._train_on`은 `_Net`을 직접 참조하므로 새 factory만 선언해서는 연결되지 않는다.
후속 구현의 최소 배치는 새 local network와 `_train_on/_train/tune_and_train`의
원래 제어 흐름을 그대로 잇는 local 사본이다. E061의 tune hook 사용 방식은 참고하되
TiedNet/conditional map은 사용하지 않는다. import/이름 변경 외 제어 흐름 diff를
검사한다. 원래 source를 일반화하거나 optimizer/selector를 재설계할 필요는 없다.
이번 세션에서는 그 사본·모델 파일·E번호를 만들지 않았다.

GIVEN x, trunk parameter theta, full-head phi, conditional-head psi라 하자.
동일한 단 한 번의 trunk/dropout forward로 z=T_theta(x)를 만든다.

\[
f_j=W_j z+b_j,\qquad c_g=U_g\,\operatorname{sg}(z)+a_g,
\qquad \operatorname{sg}(z)=z,\quad D\operatorname{sg}=0.
\]

R은 c_g=U_g z+a_g다. H는 sg만 다르다. 생성자는 원래 `_Net`의 full_dims와
**원래 cond_dims 모두** 전달한다. trunk/full/cond 등록 순서, parameter 이름·수·shape,
초기화, seed0, dtype/device, optimizer parameter 순서와 state_dict를 보존한다.
conditional weights의 requires_grad를 끄거나 head forward 전체를 no_grad로 감싸면
계약 위반이다. trunk 재실행, in-place detach, full 경로 detach도 금지한다.

원래 두 config는 (64,2,0.0), (128,2,0.1). 둘 모두 이 한 경로 변경만 받는다.
Trunk를 한 번 실행하며 각 기존 dropout layer를 원래 순서·횟수대로 사용한다.
Full/cond는 같은 z 값을 소비한다.
sg는 random draw를 추가하지 않는다. 동일 state/input/train-mode/RNG에서 full·cond
logits, CE 값, denominator, forward 후 RNG 상태는 같아야 한다. Eval/no_grad에서도
같은 확률 함수족이다. 학습 이후 state·예측·epoch 수·최종 RNG 동일성은 주장하지 않는다.

## 2. CE, gradient, Adam과 희소 조건

I개 full head, G개 conditional head, n개 fit행. a_ig는 해당 답변이 schema의
ordinary value로 coding되어 conditional target>=0인 지시자다. 이는 training target
mask이며 parent gate의 논리값으로 대체하지 않는다. Sentinel은 full target에 남는다.

\[
L_F=\sum_{i,j}\mathrm{CE}(f_{ij},y_{ij}),\quad
L_C=\sum_{i,g}a_{ig}\mathrm{CE}(c_{ig},y_{ig}),\quad
N=nI+\sum_{i,g}a_{ig},\quad L=(L_F+L_C)/\max(N,1).
\]

동일 state에서, 원래 R의 trunk gradient는 (g_F+g_C)/N, H는 g_F/N이다.
phi gradient와 psi gradient는 각각 원래 full/conditional CE의 gradient 그대로다.
특히 psi는 z가 상수 입력이어도 학습된다. Full CE도 ordinary 답변을 학습하므로
conditional predictor가 무학습 표현만 받는 구조는 아니다. 다만 표현이 conditional
목표에 직접 맞춰지지 않는 손해는 가능하다.

N은 줄이지 않는다. H의 full gradient를 nI로 재정규화하거나 learning rate를
보상하지 않는다. Conditional CE/asked 수가 denominator에 미치는 영향도 남는다.
sg는 forward identity와 custom derivative를 가진 연산이다. H 역전파는 **동일한
수치 forward 손실을 ordinary finite difference한 gradient가 아니다**. 전체 CE
finite-difference 일치를 요구하면 의도한 차단을 오류로 판정하게 된다.

Adam은 기존 lr=.003, weight_decay=.0001, parameter groups/order와 기본값 그대로다.
현재 설치 파일 `torch/version.py`는 2.13.0+cpu라고 선언한다. import/동작 확인은 하지 않았다.
정적 optimizer 소스상 betas=(.9,.999), eps=1e-8, amsgrad=False,
decoupled_weight_decay=False; grad가 있는 parameter에는 g+.0001*parameter가
moment 계산에 들어간다. Trunk weight decay는 계속 작동한다. Adam의 비선형 상태
갱신 때문에 parameter 차이를 단순히 lr*g_C로 해석할 수 없다.
동일 첫 step에서 head gradient/state/update는 같아야 하지만 이후 z가 달라지면
head gradient·moment도 달라질 수 있다. Final refit은 원래대로 seed0 새 net/새 Adam이다.

`zero_grad()`의 현재 기본은 set_to_none=True. Asked mask가 전부 빈 head는
`_pooled_ce`에서 참조되지 않아 grad=None이며 Adam step/decay/state 생성이 생략된다.
원래와 동일하게 둔다. 0인 gradient tensor는 None과 다르므로 임의 zero loss를
더하지 않는다. K=1의 zero CE도 graph가 연결된 zero gradient일 수 있어 같은 의미로
합치지 않는다. 희소 범주를 삭제·재초기화·평활화하거나 full logits에 묶지 않는다.
Inner fit에 asked가 없고 final complete fit에는 있으면 final에서 원래대로 학습한다.
G=0이면 차단할 경로가 없다. 원래 작은 표본/empty 조건과 ladder fallback을 보존한다.
Empty inner validation을 임의 재분할하는 새 guard는 넣지 않는다. 원래 호출이 실패하면
실패 기록·종료이며 seed/표본 구제가 아니다.

## 3. 실제 학습·선택·refit·출력 소비

소스 위치는 현재 파일 기준이다. 함수 본문을 읽었고 import하지 않았다.

| 생산 경로 | 원래 동작과 H의 영향 |
| --- | --- |
| `supervised_retrieval.py:215`, `hh_cap.py:12`, `link_sharp.py:113` | UNHCR 전용 layer, config2, tune hook. Frame index reset 후 GIVEN ladder 선택. H는 neural tune만 바꿈. |
| `hier_backoff.py:33,46,174`, `logit_blend.py:36` | GIVEN/PREDICT layout; EXCLUDE 제외. 모든 layout 값이 non-null인 complete행만 fitting. GIVEN-only one-hot, schema category/unknown 처리 보존. Ladder는 seed0 20% holdout, 최대3depth·기존 kappa grid. |
| `shared_trunk.py:174` | Complete에서 seed0 Bernoulli .2 outer split. fit<10 또는 eval0이면 w0/netNone, neural0. Fit 안 seed1 .2 inner stop split. |
| `shared_trunk.py:119,211` | Config마다 fresh seed0 net/Adam 하나. Inner train full-batch; inner stop은 full+cond pooled CE, max500/patience30/improvement1e-5. Best state 복원. Outer full+cond CE로 config 선택, strict < 및 원래 tie 순서 유지. |
| `shared_trunk.py:225` | 선택 net의 **full** 확률과 fit_rows ladder를 outer에서 섞어 w=0:.1:1 선택. 원래 floor와 tie 순서 유지. 이때 net은 실제로 inner-train에서 학습한 checkpoint다. 주석의 'fit portion'을 별도 outer-fit 재학습으로 읽으면 안 됨. |
| `shared_trunk.py:250` | 선택 config/best epoch로 complete 전체에서 새 net·새 Adam final refit. W=0이어도 cells>0인 정상 경로는 이 refit을 수행함. Epoch/config/w 결과값은 고정하지 않음. |
| `link_sharp.py:130–193` | W>0이면 full/cond `_proba_maps`; 아니면 NN은 출력에서 빠지고 ladder. Complete 전체의 full/asked ladder 및 conditional gate-agreement 구성. Replay용 model_dists는 full NN/ladder mixture이고 gated recursive output이 아님. |
| `supervised_retrieval.py:146` | Visible B/F/S/L 분할 seed4101, metric/selector, replay lambda. Final net은 S/L도 이미 학습한 상태다. 새 독립 평가가 아님. |
| `link_sharp.py:195–248` | schema 순서 global recursion. 부모의 evidence 반영 belief를 자식이 사용. Full/cond head 둘 다 최종 출력에 실제 소비됨. |

gated item의 full blend mF, asked-only blend mC, 부모 belief에서 구한 asked 확률 t,
원래 조건부 agreement a이면 base=a*[t*mC,1-t]+(1-a)*mF다.
원래 concentration bucket lambda가 있으면 p=(1-lambda)*base+lambda*evidence.
그 p가 다음 자식의 parent belief다. 따라서 full·conditional·부모·비말단·ungated
출력까지 달라질 수 있다. Sentinel mass를 보존하는 E057 계약이 아니다.
NLL training, w proxy, lambda proxy, 최종 공식 score는 서로 같은 목적함수가 아니다.
기존 proxy/full-output 불일치와 in-sample replay를 해결했다고 주장하지 않는다.

**A043 S0의 영향 범위 구체화:** 동일 input/runtime에서 H는 `fit_sections`의
codes/labels/bank/F/S/initial/sizes/groups 어느 것도 바꾸지 않는다. 이 함수에는
model_dists 인자가 없다. `estimate_weights`는 GIVEN matches만 사용한다.
따라서 **fitted metric weights·section selector activity·donor identity/order·replay
자격·concentration bucket은 기대 불변**이다. 원래 ladder/conditional-agreement도 불변.
이를 과거 결과값으로 덮어쓰지 말고 양쪽 계산 결과를 검사한다. 불일치는 숨은 연결,
상태 오염 또는 수치환경 문제를 조사할 기술 신호다. S0 원문은 수정하지 않는다.

달라질 수 있는 것은 neural trajectory/config/epoch/w, replay p_model, item lambda,
lambda>0인 항목과 실제 evidence 사용 여부, 최종 parent/child 출력이다. Metric 활성과
lambda 활성은 별개다. Lambda 최소30/zero fallback, grid0:.1:.9,.95,.98 및 bucket.5,
K32 original-search와 legacyK10/first10-of-K32 proxy, .003·2SE section selector,
metric .001 penalty/maxiter50/ftol1e-7/0..12 bounds는 모두 그대로다.
Visible<500 또는 query0이면 원래 hh_sharp layer, codes없으면 evidence없음.
이는 retrieval fallback이며 H neural training을 자동 R로 되돌리는 새 정책은 아니다.

## 4. 정보 접근과 귀속

| 단계 | 허용될 정보와 원래 재사용 |
| --- | --- |
| 미래 model 입구 | TRAIN generated columns, query GIVEN과 행 순서 metadata만. Query의 **모든** PREDICT를 입구 전에 mask; EXCLUDE를 feature에서 제거. 원래 entry는 role name을 검사하지 않으므로 wrapper가 이 경계를 책임짐. |
| Inner train/stop/outer | Complete visible TRAIN 내 원래 seed/split. Labels는 targets/선택에만 사용. Full와 conditional gradient 경로만 다름. Query answer/asked truth를 feature나 dispatch에 사용하지 않음. |
| Final refit/ladder/agreement | Complete visible TRAIN 전체. Outer/inner-stop labels도 다시 사용하므로 독립 audit이라고 부르지 않음. |
| Retrieval | Query GIVEN도 factorization/rarity에 포함하는 기존 transductive 처리 유지. B/F/S/L은 metric 내부 역할일 뿐 base 학습 역할과 분리된 전역 holdout이 아님. S는 optimizer slice에서 제외되지만 F+S tensor materialization은 존재. |
| Replay | Selected section은 L, 비선택은 original cal, cal cap6000/seed0. Base는 replay행을 이미 학습했고 full proxy를 사용. Conditional CE 차단이 이 낙관 편향을 제거하지 않음. |
| 외부 공학 평가 | 향후 별도 허용된 synthetic TRAIN/DEV projection만. 같은 frame/order/schema/environment의 fresh R/H raw6개와 source hash 동결 후 별도 evaluator가 DEV truth를 요청. 실제 private DEV/TEST 답변은 계속 금지. |

Partial PREDICT가 남으면 renderer의 visible one-hot/parent belief가 답변을 소비할 수 있다.
`_complete_rows`만으로 query 격리가 된다고 주장하지 않는다. Asked-only mask는
fit/validation target 계산에만 쓰이며 추론은 모든 query에 GIVEN-only network 출력이다.
실제 hosted TRAIN 내부 선택 통계는 밖으로 score 등에 인코딩하지 않는다.

비교는 R 대 H 한 번, 기존 정책을 유지한 전체 절차 효과다. Conditional supervision
전체 제거, 직접 gradient의 순수 최종 인과효과, A021 D-P/D-R, 독립 audit이 아니다.
새 selector·결과 epoch/w/lambda 강제 고정·새 outer refit·head/seed/계수 grid는 없다.

## 5. 과거 작업과 결정 가치

| 작업 | 이번 질문과의 차이·반대 근거 |
| --- | --- |
| E012 및 E025 base | Shared nonlinear representation와 conditional modeling 자체는 기존 기전. E012 공동 학습의 과거 이득은 정보 제거가 해로울 수 있는 근거다. 그 모델군 교체는 이번 gradient 경로만 분리한 실험은 아니었다. |
| E061/A033 | 독립 conditional 모듈 제거·full logits tying·초기화 RNG 변화. H는 모듈/forward 자유도/초기화를 보존. E061 hosted adverse는 관련 경고이지 H의 관측 결과가 아님. |
| E060 | Metric-fit에서 sentinel을 제외한 loss 변경. H는 metric/all-cell target와 conditional CE 값을 유지. |
| E062 | WB ordinal probability family·학습 구조 변경. H는 UNHCR 동일 forward family의 gradient routing. E062 head 재튜닝 없음. |
| E063/A042 | Round-conditioned donor metric. H는 donor 학습과 selector를 원형 그대로 두며 그 결과도 기대 불변. 공개 tie는 미세한 H 효과를 판독할 근거가 아님. |
| A037/A023/A024 | Deployed-objective 비교와 평가 채널의 문제는 남음. H를 그 연구의 PASS나 대체 oracle로 부르지 않음. |

한정된 진행 가치는 (a) 차단·head 학습·초기 parity를 저렴한 직접 검사로 반박 가능하고,
(b) 추가 neural fit 없이 전체 정책 한 쌍으로 연결·비용·NO_OP를 확인하며,
(c) 후속 단일 hosted favorable/adverse/unresolved 관측에 따라 유지/park 결정을
달리할 수 있다는 점이다. 서로 다르다는 이유만으로 개선을 예상하지 않는다.
Full와 asked-only gradients가 실제 충돌한다면 유리할 수 있지만 미측정이다.
반대로 conditional 표현 학습과 부모/자식 content를 손상할 가능성이 분명하다.
같은 연구가 모든 미기록 과거 작업에 없었다고까지 증명하지 않는다.

## 6. 전체 호출·자원 계획 — 실측 아님

정상 all3는 세 기관 각각 config2 `_train` + final refit1. 따라서 pipeline3/neural9다.
기존 E063 등록에 고정된 UNHCR 8section과 현재 `_groups/fit_sections`의 section당
minimize1회 경로를 연결하면 metric8이다. 새 schema inventory/응답 검사는 하지 않았다.
Refit을 추가9회처럼 중복 계수하지 않는다.
Ladder 탐색·agreement·metric old-share grid·lambda grid·render는 neural fit이 아니지만
wall/memory에 포함한다. Neural max500은 각 호출 상한이지 예상 epoch/시간이 아니다.
각 기관 w0도 정상 final refit 비용을 지불한다.

| 미래 단계 | all3 process | pipeline | neural `_train` | metric minimize |
| --- | ---: | ---: | ---: | ---: |
| S1 fresh R + fresh H | 2 | 6 | 18 | 16 |
| S2 clean E025, 일치 cache 없을 때 | 1 | 3 | 9 | 0 |
| S2 H 조립·추출본 parity 전체 실행 | 1 | 3 | 9 | 8 |
| S2 H official all3 별도 전체 실행 | 1 | 3 | 9 | 8 |
| S1+S2 정상 합, fresh E025 포함 | 5 | 15 | 45 | 32 |

E025는 `hh_cap.predict`의 config2와 hh_sharp라 SciPy section metric0.
인증된 동등 E025 cache 재사용이 별도로 허용되고 source/snapshot/data/roles/split/
mask/runtime/환경 identity가 맞으면 위 합에서 process1/pipeline3/neural9만 뺀다.
과거 E025 raw/cache를 지금 열거나 정당화하지 않았다. S1의 fresh R/H 결과 재사용도
동일 identity와 명시된 후속 권한이 필요하다. 안 맞으면 조용히 추가 fit하지 않고 HOLD.
S1 source 결과와 S2 extracted 결과를 직접 대조해 source/assembly parity를 검증한다.
조립본과 추출본의 source bytes 동일성은 별도 정적으로 확인한다. Checker의 실제 추가
invocation은 따로 계수하며 위 정상 5process가 모든 실패 비용까지 포함한 보장은 아니다.

Fallback 계수: small neural split은0, outer cells0은 config2 후 refit0일 수 있다.
UNHCR visible<500/query0은 section metric0. `_train`은 CUDA exception 때 CPU `_train_on`
재시도하는 기존 경로가 있으므로 logical9와 backend attempt는 다를 수 있다.
후속 로컬은 CPU2/GPU0를 고정해 CUDA fallback을 실행하지 않는다. 실패·시작된 호출도
ledger에 계수한다. 성공 arm 재실행 금지. Ordinary defect로 무효인 arm만 최대1회
재시작 제안을 S0가 별도 판단하며, S1 절대3process/9pipeline/27neural/24metric과
아래 시간 한도를 함께 만족해야 한다. 후보/seed/정책 비교 여유가 아니다.

후속 S1 제안 상한: gross120분/기록10분, 모든 computational child 합1800초,
새 작은 영향검사 합300초(같은1800에 포함), 각 작은 child60초,
fresh all3 각900초(시작/import/세 기관 전부). CPU numerical threads2, heavy1,
GPU0, owned controller+descendants RSS/private 각각8GiB. 외부 감시가 import 전에 시작,
1초 이하 sampling, absolute와 monotonic deadline, 자기 tree만 종료.
남은 총량·기록 예비시간 중 더 작은 제한 적용. 두 arm이 각각900초를 모두 쓰면
검사 여유는 없으므로 이 상한이 완료를 보장하지 않는다. 부족하면 INCOMPLETE.

후속 S2 정상 추가 작업은 fresh E025/assembly/official 각 shared900초까지,
검사·평가·준비 포함 계산합3600초를 제안한다. 재사용 R이 무효면 그 범위에서
몰래 baseline을 더 돌리지 않는다. Exact S2 scope/실패 attempt cap은 별도 사용자
권한으로 동결해야 한다. 현재 S2 실행·ZIP 허가가 아니다. 로컬+release 정상
계산허용 제안은 1800+3600초이며 실사용·예상 비용으로 보고하지 않는다.

메모리 계획: parameter 수 P와 head logits 크기는 R/H 동일. Float32 parameter·grad와
Adam 1/2차 moment가 대략 4P씩 필요하나 best_state/candidate/final net 동시 생존,
dense GIVEN tensor, full/cond logits, NumPy/Pandas/allocator·process memory도 포함해야 한다.
sg는 storage 공유이며 conditional head forward/backward를 없애지 않아 peak 절감 보장 없음.
`_topk_excl`의 chunk256×visible×GIVEN 비교/가중 임시 배열과 argsort,
`candidate_indices`의 chunk128×bank float64 score, fit/selection K32 features,
section label-match 임시 배열, 전체 probability matrices/output 직렬화도 측정한다.
Section match 생성은 전체 donor labels 인덱싱 중간값도 만들므로 최종 tensor 크기만
peak로 쓰지 않는다. 세 기관 총 import/선택/refit/replay/render/출력/eval 시간을 계수한다.
현재 runtime/peak는 **미측정**. E063의 과거 R331.947906/H327.633190 및 공식701.7초는
기존 문서상 참고만이며 H의 배속·900초 보장 근거가 아니다. 새 환경·클라우드 필요 없음은
설계 판단이며, 현재 환경에서 실제 import/완주 가능성은 후속 기술검증 대상이다.

## 7. 후속 최소 영향검사 설계 — 이번 실행0

모든 입력/소스/환경/seed/정책/한도를 응답 접근 전 등록한다. 숨은 실제 DEV/TEST 금지.
모든 검사는 원래/후보 production entry와 실제 local factory 연결까지 관측해야 한다.

| 검사 | 고정 성공 조건·실패 해석 |
| --- | --- |
| 초기 parity | 두 config 각각 state_dict keys/순서/값, parameters, RNG, forward full/cond, pooled CE/N 동일. Dropout train/eval 모드와 restore RNG 확인. 같은 초기값을 사후 load해 생성자의 다른 RNG 소비를 숨기지 않음. |
| Gradient 경로 | 고정 nondegenerate asked fixture에서 H trunk는 L_F/N만의 gradient, R은 (L_F+L_C)/N. Full/cond head gradient는 동일 state에서 R과 일치. Float64 비교 atol/rtol1e-10 제안, 고정 자료·tolerance. Whole-loss finite difference 사용 금지. |
| Conditional 학습/Adam | Asked 있는 독립 head의 nonzero gradient·1step parameter/moment 갱신, trunk 직접 conditional contribution 차단. 초기 head Adam state는 R과 일치, trunk는 차이 허용. Empty asked의 None/skip와 K1 zero 경우를 분리. No-grad 실수·head freeze면 실패. |
| Hook/selection/refit | Config2와 final refit 모두 새 factory 사용, 원래 순서/seed/pooled stop/w algorithm. R 또는 controls로 새 factory가 새면 실패. Epoch/config/w 산출값의 동일성 강제 없음. |
| Mask/정보 | Query PREDICT 입구 전 전체 mask, EXCLUDE feature 부재, asked mask training target만. S-label이 metric objective slice에 유입되지 않음과 base/refit의 기존 S/L 재사용을 별개로 기록. 평가 truth는 raw freeze 뒤. |
| Retrieval/fallback | R/H donor/metric/activity/ladder/agreement 기대 동일; lambda는 차이 허용. Minimum30/zero fallback, small/no-query/G0/empty asked 등 원래 결과·호출 보존. Metric active0을 H 중단 사유로 새로 쓰지 않음. |
| 전체 출력·비용 | Fresh R/H all3 순차. UNICEF/WB raw exact0. UNHCR all213/schema order/shape/finite/nonnegative/positive sum/max sum error1e-6. 기존 synthetic counts17856/39520/132273, 총189649 vectors/arm은 미래 identity 확인 후만 적용. Raw6개 동결 뒤 공식 normalization/floor.001/skill 각1회. |

기술 판독 제안: 위 경계·controls·비용 통과, UNHCR raw변화>=1, 각 기관 skill H-R>=-.002이면
LOCAL_TECHNICAL_PASS_FOR_S0. 양성 이득/+.005 요구 없음, 작은 하락도 기록.
전부exact R이면 STOP_NO_OP. R/H 각 최종 w와 NN 사용 여부도 기록한다.
양쪽 NN 비사용·동일 출력은 강제 fixture 성공으로 구제하지 않는다. H의 conditional
trunk gradient가 0인 것은 의도한 계약이며 비활성 실패가 아니다. 학습 변화로 H가
w=0을 선택하고 R와 출력이 달라지는 경우도 전체 절차 비교에 포함하고 숨기지 않는다.
Metric active0만으로 stop하지 않는다. 누수/비정상 확률/초기 parity·control 실패는
TECHNICAL_FAIL, 하한 실패 REGRESSION_HOLD, 자원 초과 RESOURCE_LIMIT,
미완료 INCOMPLETE. 실제 UNHCR 가설 전체 반증으로 확대하지 않는다.
일반 구현 오류만 r5의 같은 세션 최소 수리·관련 재검증 대상, 과학적 NO_OP/하한/비활성은 아님.

S2 잔여: clean E025 각 기관 absolute .002 이내 regression 및 E041 release 비교,
source/assembly/extracted parity, ZIP checker, official all3 shared900초·메모리,
bytes provenance와 사전 SCORES 판독표. 현재 어느 항목도 새로 실행하지 않았다.

## 8. 관측 채널과 사전 hosted 판독

현재 유효한 수치 oracle 없음. 새 학습 trajectory의 frozen library도 허용된 새 독립
labels도 없다. E049 혼합 oracle/E025 과거 분해는 현재 E041 조건부 gradient의 headroom이
아니다. Gradient cosine도 final score oracle이 아니다. 노출된 synthetic은 연결·마스킹·
실행비용 채널이며 개선/손실 어느 쪽도 실제 ERPIS 효과의 상한·하한이 아니다.
충돌/ordinal/round 가정을 주입한 예제를 만들더라도 실증 증거가 되지 않는다.

후속 제출은 별도 S0/S2/사용자 권한이 있을 때 단일 고정 정책만. 아래 판독을 제출 전에
SCORES에 동결하며, ID/Finished/Development phase/filename/score keys/precision와
출처·scorer metadata·로컬/원격 bytes 확인 범위를 구분한다. 현재 E041 ID933094 공개
Grand.6433333333/UNICEF.52/WB.49/UNHCR.92는 노이즈·반올림 후 값이다.

| 미래 관측 | 판정과 다음 행동 |
| --- | --- |
| UNHCR·Grand 모두 공개 개선, controls 공개 동일, 출처 모순 없음 | FAVORABLE noisy whole-policy evidence. S0가 연구/DEV 보존 우선순위 검토. Direct gradient 효과 확증·TEST 자동 채택 아님. Best-update 사건은 별도 실제 근거가 있을 때만 기록. |
| UNHCR·Grand 공개 하락, controls 공개 동일 | ADVERSE for this fixed policy. E041 유지/H parked; seed/head/계수 구제·같은 정책 재제출 없음. 모든 gradient 분리의 불가능으로 확대하지 않음. |
| 네 공개 값 모두 동일 | UNRESOLVED. 읽을 수 있는 개선 없음, H parked/동일 정책 우선순위 낮춤. 정확한 효과0·예측 동일·hidden head 활성 추론 금지. |
| Mixed target/Grand 방향, controls 변화 또는 출처/phase 모순 | HOLD_ATTRIBUTION/COMPARABILITY. 제공된 정확한 기록·정상 score 상세의 부족 항목만 S0에 요청. 추가 응답 진단/튜닝/반복 제출 없음. |
| Runtime/format/contract 실패 | TECHNICAL failure. 효과 방향 판정 없음. 정확한 실패 경계를 S0로 반환. |
| 필요한 기관값/ID/status 미제공 | HOLD_SPECIFIC_INPUT. 사용자 소유 정상 결과/API 기록의 해당 필드가 재개 입력. 누락을 adverse/tie로 대체하지 않음. |

공개 문자열의 긴 소수 표시로 hidden 정밀도를 복원하지 않는다. E063 공개 tie와 같은
값의 반복은 미세 효과 구별 근거가 아니다. 이 한정된 판독 이상의 precision/power나
실제 target efficacy를 요구한다면 현재 채널로 충족할 수 없어 별도 채널 권한이 필요하다.

## 9. 반환·보존

이 계약의 미해결 실행 조건은 새 source/환경/입력 freeze와 실제 영향검사·전체비용,
clean E025/S2 release, 장래 hosted 결과다. 계약 자체의 경로·학습 가능성·정적 호출 수는
명시할 수 있으므로 현재 일반적 효과 미확정을 이유로 반복 HOLD 조사하지 않는다.
S0가 **별도 제한된 구현/공학 검증을 지시할 가치가 있는지** 판단한다. 자동 전환 없음.

현재 읽기/해시/비용/노출/보존 근거는 [verification.json](verification.json),
요약은 [closeout](closeout.md), [S0 인계](s0-handoff.ko.md).
E041/E025, parked E057/E060/E061/E062/E063 및 E063 UNRESOLVED 유지.
E058 STOP/E059 STOP_SELECTION, A023/A024 empirical HOLD/A039/A040/all STOP/HOLD;
17999명/12339SSUID·집계·A022 원래 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단/S2 후보 없음.
