# A041 S1 — 전체 비용 계약

문서/소스 판독만 수행. 새 candidate의 import/fit/predict/score 시간, 메모리, CPU2 완료 가능성 **미측정**. 아래 숫자는 코드의 호출 구조 또는 명시한 과거 기록이며 이번 실측값이 아니다.

## 소스에서 확인한 계수

기준 `submissions/2026-09-19-E041/main.py`. 주요 위치: select_ladder179, _train429/_train_on445, tune_and_train500, predict745, hh_sharp_layer882, CONFIGS945, fit_sections1026, supervised_layer1092, 최종 dispatch1153. A041은 WB head만 바꾸며 dispatch/기존 선택 규칙 유지 제안.

| 단계 | 정상 instrument 한 번 | all3 한 번 | candidate/E041/E025 각 all3 한 번 |
| --- | ---: | ---: | ---: |
| 최상위 predict pipeline | 1 | 3 | 9 |
| config neural fit | 2 | 6 | 18 |
| 최종 visible-data neural refit | 1 | 3 | 9 |
| 총 logical neural training call | 3 | 9 | 27 |
| config 선택 | 2개 outer pooled CE 비교 | 3번 선택 | 9번 선택 |
| w 선택 | 11개 값 | 33개 값 | 99개 값 |
| ladder 구조 선택 | 1회 | 3회 | 9회 |
| final ladder full/conditional 구축 | I+G개 | 각 기관 합 | 모델별 합 |

2개의 legacy config는 새 ordinal 후보 grid가 아니다. 각 config의 best state를 outer eval에 사용하며 outer fit 재학습을 추가하지 않는다. 최종 refit만 별도로1회다. 정상 최댓값은 instrument당 학습 epoch 합1500(두 config≤500씩, 선택epoch refit≤500), all3≤4500, 세 절차 비교≤13500. 이는 학습 update 수의 상한이며 시간 환산이 아니다. config마다 매 epoch inner validation forward가 있고 outer 평가2회, 선택 net의 w용 forward1회, 최종 all-row forward는 w>0일 때1회다. refit에는 validation forward가 없다.

작은 표본 fallback은 fit<10/outer eval=0이면 neural0. 정상 w=0이어도 refit1은 이미 소비하며 마지막 all-row neural forward만 생략한다. 후보 안에서 E041을 별도 fit하여 비교하거나 최종 실패 뒤 baseline을 다시 fit하는 경로를 추가하지 않는다. 전체 E041/E025 비교는 위 표의 독립 실행으로 계수한다.

`_train`은 CUDA 오류 때 CPU로 재시도할 수 있다. logical call과 실제 `_train_on` attempt를 따로 기록해야 한다. 미래 CPU2/GPU0 검증에서는 CUDA 분기를 사용하지 않는다. hosted에서 해당 기존 fallback이 발생하면 실패 attempt 시간까지 같은 shared900초에 포함하며 정상9회라는 수로 비용을 숨기지 않는다. 최대 한 번의 CPU 재시도가 있는 각 logical call도 예산 밖 추가 시도가 아니다.

### 비신경망 선택/렌더링도 포함

- Ladder: eligible GIVEN 개수 M, 최대 depth3, κ5개. 세 단계 모두 진행할 때 비교 가설 수 상한은 `5 * sum(M-d, d=0..min(3,M)-1)` + depth0 기준이다. `_eval_candidate`는 한 column의 κ 후보들을 함께 처리하므로 이 수를 neural fit 횟수로 부르지 않는다. 단계별 기존 ladder 구축, counts/code cache, EVAL_CAP3000도 비용이다. 개선 없으면 일찍 끝난다.
- Gate agreement: 각 gated item의 scalar 및 eligible GIVEN별 비교, 선택 table의 전체 visible 재구축. 대상16은 ungated이나 다른 WB 출력/타기관의 기존 경로는 계속 실행한다. 일부 global scalar는 visible 전체를 사용한다. 내부 비교를 전체 독립 validation으로 해석하지 않는다.
- Household: CAL_QUERIES≤6000/seed0, 첫 rarity donor 탐색1회, weight 추정1회, 보정된 replay 탐색1회. λ 활성일 때 held-query 탐색1회 추가. 각 탐색은 여러 chunk와 item별 evidence 계산을 포함한다. TOP_K10, minimum pairs30, concentration bucket .5 유지.
- λ: evidence가 있는 item의 두 bucket, 각 support≥30일 때 zero baseline+11개 후보 값. WB76이면 최대152 bucket 결정/1824개 log-mean 평가 값(그중 zero 이후1672개)이다. 실제 support/활성 수는 응답을 읽지 않고 알 수 없다. 후보 추가 grid가 아닌 기존 경로다.
- Metric optimizer: 최종 E041 dispatch상 **WB0/UNICEF0**. UNHCR에서 visible≥500 등의 조건이 맞으면 section group당 L-BFGS-B1회, maxiter50. 그룹별 기존 donor-share6값 선택과 별도 select-row 비교도 있다. E025는 supervised metric0. 따라서 세 모델 all3 비교의 optimizer 수는 최대 `2 * G_UNHCR`인 정상 구조다. 기존 E061 기록은16회였으나 이 조사에서 실제 branch/iteration을 실행·재계수하지 않았다. 부족 표본 등 fallback이면 감소한다. 최적화 iteration 수를 function/gradient evaluation 수로 바꾸어 적지 않는다.
- Raw render: 모든 행의 full/conditional ladder, neural 확률, gate recursion 및 donor blend, blank-cell schema 순서 flatten. 학습 대상16개뿐 아니라 WB76/세 instrument 전체가 비용 범위다. 검증·공식 floor/score·해시·출력 기록·worker 종료도 전체 검증 비용에 포함한다.

## 이 후보의 연산 변화와 미측정 항목

Target head당 linear output7개가 조건부5+비응답1로 바뀐다. trunk width H에서 16(H+1) parameter 감소지만, log-sigmoid/prefix sum/일곱 log-probability 조립과 기존 softmax/NLL가 필요하다. epoch 수·config/w 선택도 바뀔 수 있다. parameter 감소만으로 빨라진다고 주장하지 않는다. 추가 fit/ordinal optimizer/library는 설계상0이다.

메모리는 GIVEN dense tensor, fit/stop/eval/refit 복사, full/conditional target 및 logits, Adam state/best-state clone, 동시 참조되는 config network, ladder/donor 배열, 전체 raw output을 포함한다. 순차 all3라도 해제 시점/캐시가 미확정이면 peak가 한 instrument와 같다고 보장할 수 없다. 이론상 작은 head 변화는 전체 top-k/chunk 배열 비용을 제거하지 않는다.

기존 Torch의 Linear/logsigmoid/cumsum/logsumexp 및 NumPy로 표현 가능하다. 이 판단은 API/수학 설계이며 현재 환경 import 확인이 아니다. 기존 환경으로 실제 실행 불가가 드러나면 원인을 기록한다. 새 환경/클라우드 구축을 예비 작업으로 삼지 않는다.

## 과거 E061 참고 — 전용 금지

`docs/experiments/E061-tied-content-heads.md`의 기존 기록:
candidate all3 340.093s, scientific worker1083.500s, 누적 test/fit/evaluation worker1098.523s, full-stack9/neural27/metric16. CPU2/GPU0, conservative owned-tree RSS1.991GiB/private commitment1.514GiB.
이 조사에서는 해당 모델·cache·응답·출력을 열지 않았다. 다른 개입/데이터의 기록이므로 A041 실행시간/메모리/900초 PASS 예측치로 사용하지 않는다.

## 후속 S1에 제안하는 한도 — 현재 실행 권한 아님

E061의 비교 예산 구조를 유지하는 한 가지 안: 전체 세션120분, 마지막10분 closeout; CPU numerical threads2, GPU0, heavy worker1. candidate all3 worker startup/import+세 기관 전체≤900s. candidate/E041/E025 비교와 새 집중 검증을 합친 실제 computational child wall≤1800s. full-stack≤9/neural training attempt≤27를 합산하고, 실패도 차감한다. 과학 실행은 각 model/instrument1회 계획이며 성공 무변경 반복 없음. 구현 오류 수리는 workflow r5 범위에서만, 남은 합산 budget/attempt 안에서 판단한다. 한도를 넘길 추가 실험은 자동 시작하지 않는다.

자기 controller+자식 tree의 RSS 및 private commitment 각각≤8GiB, Windows 관측 주기.1초를 제안한다. 사전 monitor가 실제 계수를 못 하면 시작하지 않는다. 두 메모리 지표를 혼동하지 않고 per-process peak 합산의 보수성을 적는다. 초과/첫 과학 오류 시 자기 worker tree만 종료하고 원인/부분결과 보존. 부모 monotonic clock과 절대 세션/candidate deadline을 같이 둔다. 수정 중 한도 초기화 금지. 이 숫자는 **미래 등록에 제안한 한도**, 완료 보장이 아니다.

계측 위치: worker import 시작 → 각 predict 입출구 → ladder 선택 → 각 `_train`/`_train_on` 시작/끝/epoch 및 early-stop → outer config/w 결정 → final refit → gate/donor/λ/metric 단계 → full render → 전체 검증/score → 종료. 시간이 겹치는 상위/하위 span은 합산하지 않는다. 실제 branch/iteration/rows/input-source-split identity, fallback 및 skipped 단계도 별도 기록한다. 이번에 계측 코드는 작성하지 않았다.

S2는 별도 source/assembly parity, ZIP checker, official all3 **import부터 세 기관을 합친900초**, hosted memory contract(현재 저장 문서16GB), clean E025 대비 기관별 absolute .002 및 E041 비교/SCORES 판독이 남는다. 로컬8GiB/CPU2 통과가 hosted 환경·release 통과를 대체하지 않는다. 보장되지 않은 H100 배속/비용을 적지 않는다.
