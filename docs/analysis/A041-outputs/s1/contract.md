# A041 S1 — WB 순서형 head 적용 계약

2026-10-07. **DESIGN_READY_FOR_S0_REVIEW**. 정보 조사/설계만 완료.
후속 구현·기관 변경·학습·S2 자격·효과 승인이 아니다. 실제 모델/자료 실행 0.
입력/읽기 영수증은 [entry.json](entry.json), 근거는 [source-register.md](source-register.md).

## 1. 한 후보와 반증 가능성

추천: **CORN식 여섯 범주 조건부 확률 + 별도 Not answered 확률**. 기존 WB shared trunk에 연결하고 원래 일곱 범주 NLL로 학습한다. CORAL 비교 arm, 역순 arm, 새 seed, head 부분선택, 새 hyperparameter grid는 만들지 않는다. CORN 원 논문을 그대로 재현한다는 이름도 쓰지 않는다. 비응답 분리와 pooled 분모 유지가 이 적용안의 명시적 차이다.

원전 비교: CORAL은 공통 logit 방향과 threshold별 bias, 전체 threshold BCE를 사용한다. 최적 bias의 순서 정리는 유한 early stopping 결과의 증명이 아니다. CORN은 조건부 risk set에서 별도 logit을 학습하고 확률의 곱으로 누적확률 순서를 보장한다. 여기서는 공통 기울기 제약을 더하지 않고 범주 NLL과 직접 연결할 수 있는 후자를 택한다. 원 논문의 MAE/RMSE 결과는 HSCC log score 이득 근거가 아니다. [CORAL](https://arxiv.org/html/1901.07884v7), [CORN](https://arxiv.org/html/2111.08851v5).

비교를 수식으로 적으면 CORAL의 substantive survival은 a_k=σ(g+b_k), loss는 Σ_k λ_k BCE(a_k,1[Y>k]) (λ_k>0)다. b_1≥…≥b_5라면 (1-a_1,a_1-a_2,…,a_4-a_5,a_5)로 범주 확률을 복원할 수 있다. 이 차분 분포의 categorical NLL은 threshold BCE 합과 다르다. 실제 유한 학습에서 bias 순서를 보장하려면 별도 제약 검증이 필요하다. 이번에는 그 후보/제약을 구현하지 않는다.

**자체 설계 추론:** 작은 고정 trunk 위에서 각 순서 경계의 조건부 log-odds를 affine 함수로 제한하면, 범주별 nominal logit과 다른 함수족/gradient를 얻는다. WB 공개 구간 라벨은 이 순서를 고정할 근거다. 제한된 표본에서 이 편향이 확률 추정을 도울 수 있으나 상위 risk set의 희소성·곱의 오차 누적 때문에 악화할 수도 있다. 실제 빈도나 효과 크기는 모른다.

모든 정상 categorical 분포는 이미 단조 누적확률을 갖는다. 따라서 E041 softmax가 확률적으로 모순돼 이를 고친다는 주장은 틀리다. 자유로운 조건부 확률은 한 x에서 모든 여섯 범주 분포를 나타낼 수 있다. 검증 대상은 **순서를 사용한 제한된 logit 함수족의 학습 편향**이다. 별도 비응답 factor도 개입 일부이므로 결과를 순서 효과 하나로 인과 분해하지 않는다.

E011은 다른 문항 검출 규칙과 사후 kernel, E030은 GIVEN 검색 서명, E017/E026은 용량, E029는 seed/온도, E061은 UNHCR full/conditional 공유다. 공유 표현 자체는 E041에 이미 있다. 기존 null/STOP/parked를 해제하지 않는다. 향후 적법한 고정 비교에서 전체 WB log score가 하락하면 이 절차의 실용 가설에 반대 근거다. ordinal MAE 개선만 관측되면 가설 지지가 아니다. 노출 synthetic의 양성/음성은 실제 WB 효과의 증명/불가능 판정이 아니다.

## 2. 대상·출력 계약

대상은 S0 [inputs.json](../inputs.json)에 고정된 16개 그대로다. 새 inventory/빈도 선별을 수행하지 않았다.

`sc_nstd_extra`, `sc_nstd_agree`, `sc_nstd_consc`, `sc_nstd_stability`,
`sc_nstd_open`, `sc_nstd_gm`, `sc_nstd_pp`, `sc_nstd_s_aware`,
`sc_nstd_s_manage`, `sc_nstd_soc_aware`, `sc_nstd_realistic`, `sc_nstd_invest`,
`sc_nstd_artistic`, `sc_nstd_social`, `sc_nstd_enterp`, `sc_nstd_convent`.

공개 schema identity: `6b3760742c6e864eb8d0bb2f9ec523a19a486b73282d79432dbcca16e3664125`.
16개 모두 PREDICT, gate=null. 순서 고정:
`<2.5`, `2.5-3.0`, `3.0-3.5`, `3.5-4.0`, `4.0-4.5`, `4.5-5.0`, `Not answered`.
마지막 범주는 낮거나 높은 점수도 gate sentinel도 아니다. 명시적 답변 범주이며 null과 구분한다. schema 불일치는 기술 중단 사유다. 맞는 일부 head만 남기는 구제 금지.

이하 수식은 A041 적용안의 자체 유도다. z는 기존 GIVEN-only trunk 출력, M은 Not answered다.

\[
m(x)=\sigma(u^Tz+c),\qquad
r_k(x)=\sigma(a_k^Tz+b_k),\quad k=1,\ldots,5.
\]

r_k의 의미는 \(P(Y>k\mid Y\ne M,Y\ge k,x)\). r_1은 substantive 응답 내 첫 조건부 확률이다.

\[
S_0=1,\quad S_k=\prod_{l=1}^k r_l\ (1\le k\le5),\quad S_6=0;
\quad q_j=S_{j-1}-S_j.
\]

\[
p_j=(1-m)q_j\quad(1\le j\le6),\qquad p_M=m.
\]

0≤r_k,m≤1이므로 S는 내림차순, q/p는 비음수, 망원합으로 Σq=1 및 Σp=1. q 자체의 단조성/단봉성은 요구하지 않는다. 거리·구간 중점·원점수·결측 원인·MAR 가정 없음. m=1이면 전 질량이 M, m=0이면 substantive 분포. r_k=0이면 그 이후 질량0, 모든 r_k=1이면 여섯째 범주 질량1. 이 극한은 정상 분포다.

유한 logit에서는 log-sigmoid로 계산:

\[
\log p_M=\log\sigma(g),\quad
\log p_j=\log\sigma(-g)+\sum_{l<j}\log\sigma(t_l)+\log\sigma(-t_j)\ (j\le5),
\]
\[
\log p_6=\log\sigma(-g)+\sum_{l=1}^{5}\log\sigma(t_l).
\]

g=uᵀz+c, t_k=a_kᵀz+b_k. 작은 확률을 뺄셈으로 복원하지 않는다. 후속 구현은 이 일곱 log-probability를 기존 full-head logits 인터페이스에 넘기는 방식 하나로 고정한다. 기존 cross_entropy/softmax의 logsumexp 정규화는 수학적으로 동일한 분포이며 수치 보정만 수행한다. 새 clamp/floor/label smoothing/temperature 없음. 비유한 값은 기술 실패다.

희소 범주도 schema 자리와 일곱 출력 유지. 관측 없는 risk set에는 data gradient가 없고 기존 초기화/weight decay만 남는다. 이는 식별된 확률이 아니다. substantive 관측이 전혀 없으면 m만 지도되며 q는 식별 불가다. 임의 최소 표본 기준·새 prior·head별 교체·평활화로 구제하지 않는다. 기존 전체 neural 작은 표본 fallback(fit<10 또는 outer eval=0: w=0, net=None)은 보존한다. 기존 ladder의 0.5 pseudocount와 λ의 minimum30/zero fallback도 그대로다.

## 3. 범주 NLL, pooled loss, 최종 점수

BCE(a,b)는 Bernoulli NLL이다. 한 cell의 손실은 다음과 같다.

\[
\ell(M)=\mathrm{BCE}(m,1),\quad
\ell(j)=\mathrm{BCE}(m,0)+\sum_{k=1}^{5}1[j\ge k]\mathrm{BCE}(r_k,1[j>k]).
\]

j≤5일 때 j보다 작은 k는 log r_k, j는 log(1-r_j); j=6이면 다섯 log r_k. 따라서 정확히 \(\ell(Y)=-\log p_Y\). 이를 **한 cell**로 계수한다. 원 논문의 risk-set 총크기 분모를 multihead pooled loss에 이식하지 않는다. 그러면 head별 상대 가중치와 regularization 비율까지 달라진다. 기존 분모 유지:

\[
D=N\,I+\sum_{h\in\text{gated heads}}n_{h,\mathrm{asked}}.
\]

I는 해당 instrument의 모든 full PREDICT head 수다. 변경16개도 기존과 같이 N회씩 센다. 나머지 full nominal CE와 asked conditional auxiliary CE는 그대로다. Not answered도 유효 full cell이며 conditional risk set에만 포함되지 않는다. auxiliary head는 추가하지 않는다.

공식 채점은 모든 혼합·재귀 렌더링 뒤 raw vector v를 정규화한 \(p^*=v/\sum v\)에 적용한다.

\[
\widetilde p_c=\epsilon+(1-K\epsilon)p^*_c,\quad\epsilon=.001;
\quad L=\frac1{N_{\rm cells}}\sum\log\widetilde p_{Y};
\quad \mathrm{skill}=1+L/U,
\]

U는 schema의 PREDICT별 log K 평균, Grand는 세 기관 skill 평균. 7-class 대상의 계수는 .993이다. 반환 raw 확률에 미리 floor를 넣지 않는다. 공식 평가 단계에서 한 번 적용한다. 기존 w 선택의 임시 평가 floor는 유지되며 그 값을 출력에 다시 넣지 않는다.

neural NLL은 final floored mixture score와 같지 않다. 혼합 없는 경우조차, t=-log p_Y라 놓으면 floored NLL의 t 미분은 \((1-K\epsilon)p_Y/[\epsilon+(1-K\epsilon)p_Y]\)다. 작은 p에서는 raw NLL과 gradient가 다르다. donor/ladder 혼합과 gated auxiliary loss까지 있으므로 NLL/threshold BCE/MAE 개선을 최종 점수 개선으로 대체할 수 없다. floor-aware loss로 바꾸는 추가 개입은 제안하지 않는다.

기존 λ 선택도 true-class probability clamp와 평균 log를 쓰며 전체 최종 분포의 공식 floor와 완전히 같은 목적함수는 아니다. 이를 이번 후보에서 수리하지 않는다. 최종 판독은 공식 범주 log score/skill이다.

## 4. E041 경로와 고정할 학습 절차

기준 snapshot SHA256 `22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.
실제 마지막 dispatch는 UNHCR marker가 없으면 E025 경로다. 따라서 **WB의 E041은 E025 경로와 동일**하며 WB metric optimizer 추가0. UNICEF/UNHCR는 원래 E041 dispatch와 바이트 동등 출력이 통제다. WB 전용 모듈의 전역 patch가 다른 기관을 오염시키면 실패다.

고정 규칙: configs 순서 `(64,2,0.0)`, `(128,2,0.1)`; torch seed0; Adam lr.003, weight_decay.0001; max_epochs500, patience30, 개선1e-5. outer split seed0/Bernoulli.2, outer fit 안 inner split seed1/Bernoulli.2. 정확한 행 수는 실제 visible TRAIN 없이는 모른다. 기대 비중은 inner train64%/inner stop16%/outer selection20%이며 정확한 고정 크기라는 뜻이 아니다.

기존 split은 행 단위이며 희소범주 stratification이나 household 독립성을 보장하지 않는다. 이를 새 group split으로 바꾸지 않는다. 내부 선택의 불확실성/과적합 가능성으로 기록한다.

각 config는 inner train에서만 gradient를 받고 inner stop에서 epoch/state를 고른다. outer selection pooled CE의 엄격한 `<`로 config를 고르므로 동률은 먼저 나온 config다. **outer fit 전체로 중간 refit하지 않는다.** 이 선택 net의 outer 예측으로 w∈{0,.1,…,1}를 고른다. ladder는 outer fit에서 만들며 동률 w는 기존 순서의 첫 값이다. 선택한 config/epoch/w를 동결한 뒤 모든 complete visible TRAIN으로 새 seed0 net을 한 번 refit한다. 최종 epoch=max(best_epoch,1), validation 없음. 정상 경로는 w=0이어도 이 refit을 수행한다.

후속 초기화 설계: 원래 nominal network 전체를 seed0으로 먼저 구성한 뒤, 대상 head의 기존 7개 linear 행 중 0..4를 r_1..r_5, 행6을 m의 초기 parameter로 복사하고 행5를 버린다. 새 난수를 소비하지 않는 parameter 복사로 trunk/비대상 head 초기값과 이후 RNG 상태를 보존한다. 이것은 target 확률 초기 parity를 뜻하지 않는다. 별도 bias 보정/빈도 초기화는 하지 않는다. 원래와 다른 초기확률 역시 이 한 parameterization의 일부다. 아직 구현/검증되지 않았다.

초기 확률의 순서 비대칭도 숨기지 않는다. 모든 logit이0인 수학적 예에서는 m=.5, q=(1/2,1/4,1/8,1/16,1/32,1/32)다. 실제 seed0 초기 출력이 이 값이라는 관측은 아니다. 이 차이와 finite-epoch 최적화가 결과에 영향을 줄 수 있다. 사후 초기값/순서 구제는 하지 않는다.

기존 ladder depth≤3/kappa{1,3,10,30,100}, gate agreement, household donor, bucket/λ 순서·minimum30·zero fallback·재귀 렌더링을 유지한다. 선택 **규칙**을 보존하며 후보별 선택값을 다시 산출한다. head 변화 때문에 config/epoch/w/λ와 WB의 나머지60개 출력도 달라질 수 있다. 비교는 전체 절차 효과다. 기존 E041 선택값을 억지로 고정하거나 성적이 좋은16개만 보고 판단하지 않는다.

## 5. 정보 역할과 관측 채널

추론 feature는 GIVEN-only. EXCLUDE 및 모든 query PREDICT 응답은 feature/검색 서명으로 금지. 미래 외부 평가/hosted query의 **전체 PREDICT block**을 모델 진입 전에 마스킹한다. 일부 target만 숨기고 같은 query의 다른 PREDICT를 남기지 않는다. schema의 알려진 범주 사전 사용과 전체 행 GIVEN 기반 rarity는 기존 동작이며 답변 접근과 구분한다.

| 역할 | 미래 허용 정보/행위 | 해석 |
| --- | --- | --- |
| Inner train | 해당 행 GIVEN와 target만 optimizer에 전달 | 다른 역할 target은 optimizer 입력에서 격리 |
| Inner stop | 해당 행 GIVEN forward, target은 epoch/state 판단만 | training gradient 없음; 독립 최종 평가 아님 |
| Outer selection | 해당 행 GIVEN forward, target은 config/w 선택만 | config와 w가 같은 역할 재사용; 독립 audit 아님 |
| Final refit | 동결 config/epoch로 complete visible TRAIN 전체 | 이전 내부 선택 행도 사용; query target 금지 |
| Legacy λ replay | 기존 규칙대로 visible TRAIN target 재사용, donor 자기 행 제외 | model은 이미 그 행을 fit했음. self exclusion만으로 독립성 없음 |
| 외부 query/evaluation | 전체 PREDICT 마스킹, GIVEN만 모델에 전달 | truth는 별도 평가기에만 존재; 이 조사에서는 접근0 |

이 표는 실제 역할 재배정/접근 허가가 아니다. 기존 파이프라인 내부 selection은 neural 부분만 분리된 절차다. ladder 등 다른 내부 선택과 refit/λ까지 통틀어 독립 검증이라고 부르지 않는다. 전체 파이프라인을 검증할 외부 held-out 자료가 필요하다면 모든 구성요소에서 해당 행 전체 PREDICT를 먼저 제거해야 한다. 이번 설계에 추가 split/fit/audit를 몰래 삽입하지 않는다.

현재 fresh oracle 없음. 공개 schema는 확률 구조만, 원 논문은 다른 과제의 방법만 알려준다. 과거 synthetic DEV/TEST는 노출된 engineering 자료다. 순서 가정을 주입한 예제는 그 가정하의 계산만 확인한다. 적법한 독립 WB 답변과 고정 후보 예측이 없으므로 유용한 목표 효과/상한 oracle을 만들 수 없다. 기존 Adult/SIPP 역할·미열람 calibration·보호 audit를 새 WB holdout으로 바꾸지 않는다. VAF 의미/채널 HOLD도 별개다.

미래 실제 TRAIN 선택은 허가된 hosted 실행 내부에서만 수행한다. 내부 상세통계·target·split 결과를 점수/확률의 추가 인코딩으로 반출하지 않는다. hosted DEV 공개 점수는 허가된 S2 이후 가능한 별도 채널이며 노이즈/반올림 전 원점수가 아니다. 지금 S2나 제출 횟수를 허가하지 않는다.

## 6. 후속 실험 설계안 — 아직 비활성

S0 검토와 사용자의 **prospective WB 기관 변경 지시**, 별도 S1 사전 등록이 선행 조건이다. 이 문서에는 실행 명령/E번호가 없다. 원리상 기존 Torch/NumPy 연산으로 구현 가능하며 새 환경/클라우드/체크포인트가 필요하다는 근거는 없다. 환경 정상 작동과 실제 비용은 미검증이다.

첫 단계는 학습 없는 수식/인터페이스 집중 검증: 일곱 확률의 비음수·합1·schema 순서, log-NLL 일치, m/r 극단값, 빈 risk set/미관측 범주, 전체 query mask, 비대상 초기 parameter/RNG 보존, inactive neural 경로다. parameter/RNG 확인에는 향후 network 생성이 필요하며 모델 import 없는 검증이라고 부르지 않는다. 이는 미래 계획이며 이번 실행0. 다음 단계도 기존 노출 engineering 입력을 사용할 별도 권한/identity를 등록한 뒤에만 수행한다. target16뿐 아니라 WB76 및 all3 모든 출력·raw control parity를 확인한다. 학습 전 schema/확률 결함이면 fit0으로 중단한다.

한 고정 candidate/E041/E025의 all3 각1회 비교를 제안한다. 캐시 재사용 없이 비용을 직접 계수하는 최소 설계다. 후보 코드/입력/분할/대상/기준을 점수 전 동결하고 예측을 보존한다. 같은 자료를 보며 head/seed/width/grid/threshold를 바꾸거나 성공 시 같은 검사를 반복하지 않는다. 후속 cap 제안은 [cost-accounting.md](cost-accounting.md); 현 세션에서 활성화되지 않는다.

| 사전 관측 | 판독/행동 |
| --- | --- |
| 확률·mask·schema·UNICEF/UNHCR exact raw parity 결함 또는 자원 초과 | 기술 실패, 산출물 보존. 허가 범위 내 구현 수리는 가능하나 합산 예산/시도 수 유지; 과학 정책 구제 금지 |
| Engineering WB 이득, 통제/전체 비용 통과 | 기술 후보 검토 자료. 실제 WB 효과 미확정; synthetic 양성으로 채택 금지 |
| Engineering WB 중립/비활성 | 효과 미확정. 활성 경로 기술 증거가 없으면 검증 누락 표시; 실제 불가능으로 확대 금지 |
| Engineering WB 저하 | 해당 generator상의 반대 근거. 정한 회귀 기준 미달이면 release 준비 보류; seed/head 구조 구제 없음 |
| 향후 허가된 hosted에서 WB 상승, 고정 타기관 동일 | 전체 절차의 탐색적 지지. 단일 점수로 순서의 단독 인과효과/통계적 유의성 주장 금지 |
| hosted WB 동점/하락 또는 타기관 변화 | 노이즈·반올림 동점은 효과 미해결; 하락은 절차의 반대 근거, 타기관 변화는 귀속/동일성 확인 필요 |

유니버설 +.005 이득 조건을 만들지 않는다. 공식 log score/skill의 WB 전체 차이를 주 판독으로 두고 16/나머지60/Not answered 분해는 적법한 engineering 자료에서 설명용으로만 쓴다. head별 승자 선택·ordinal MAE gate·추가 proxy guard 금지. 셀들이 같은 응답자에 종속하므로 셀을 독립 표본처럼 다루지 않는다. 현재 독립 표본/분산 정보가 없어 검정력이나 유의성 보장을 쓰지 않는다.

S2 잔여: clean E025 대비 기관별 skill 절대 .002 비열등 범위(상대0.2% 아님), E041 비교, exact source/assembly parity, ZIP checker, 공식 all3 shared900s/메모리, SCORES 판독. E061의 기존 engineering 기준인 E041 대비 -.002도 후속 사전 등록에 그대로 제안한다. 둘 다 실제 효과/최종 채택 기준과 분리한다. source/assembly/ZIP/official checker를 이번에 수행한 것으로 기록하지 않는다.

## 7. 범위별 판정

확률·학습·선택·귀속·비용 설계: **DESIGN_READY_FOR_S0_REVIEW**.
실제 구현/수치 검증/CPU2 완료시간·메모리: **NOT_RUN / UNMEASURED**.
실제 WB 효과: **UNRESOLVED**, fresh oracle 없음.
기관 변경 실행·E등록·S2/release: **NOT_AUTHORIZED**.
모든 incumbent/parked/STOP/HOLD/노출 경계 유지. 다음 담당 S0; 자동 실행 없음.
