# S1 · 기존 λ를 보존한 donor 상호작용 대조 연구

아래 블록은 사용자가 다음 S1에 전달할 실행 프롬프트다.
현재 S0에서는 실행하지 않았다. S1 인계 준비는 S2 후보 자격과 다르다.

```text
SimulacraBench / HSCC S1 연구를 시작한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 소스 HEAD: 1d223340d4e1fa3993b411dc5daafab9cb37d0cd
인계 문서: docs/analysis/A020-post-e058-design-review.md
인계 검증: docs/analysis/A020-outputs/verification.json

이 프롬프트는 아래에 한정한 새 연구의 구현·검증·실행을 허용한다.
E058 재실행, 기존 STOP 변경, 새 E041/base fit, 제출, S3 재개는 금지한다.
E041 incumbent, E025 fallback, E057 parked 유지.
A018 TEST 선택은 사용자 미확정이다.

1. 진입·목적
CLAUDE.md, docs/status.md, docs/log.md 최신 3개 순서로 읽고
docs/workflow.md를 적용한다. 다음도 읽는다:
- docs/analysis/A020-post-e058-design-review.md
- docs/analysis/E058-outputs/registration.md
- docs/analysis/E058-outputs/closeout.md
- docs/analysis/E058-outputs/exposure-ledger.md
- docs/analysis/E058-outputs/library.json, preflight.json
- docs/analysis/A019-sipp-model-exposure.md
- scripts/screen_e058.py
- src/models/supervised_retrieval.py
- src/models/link_sharp.py
- src/models/prob_link.py
- src/eval/retrieval_oracle.py, logloss.py, recursive_candidates.py

판단 문제: 기존 λ·부모·base를 고정할 때, 가산형 대조군보다 pair evidence가
유용하고 동시에 기존 E041보다 유용한가?
E058은 원래 활성 section 0개 때문에 beta fit을 못 했다.
이번에는 원래 활성 판정을 변경하지 않고, 별도 연구용 A/B 후보를 만든다.
두 후보의 독립적인 외부 검증이 필요하며 원래 비활성을 통과로 바꾸지 않는다.

HEAD/변경 파일/작업 소유권을 확인한다. A020 문서가 미커밋 상태일 수 있다.
관련 소스가 기준과 달라졌으면 차이를 기록하고 계산 전에 중단한다.
문서만 추가된 후속 커밋이면 차이와 실제 HEAD를 기록하고 진행 가능하다.
E059가 미사용인지 확인하고 단일 소유자가 예약한다. 충돌하면 임의 번호 변경
없이 중단한다. 새 docs/experiments/E059-leaf-donor-interactions.md에 이 명세를
사전등록한 뒤 구현한다. 캐시를 읽기 전 원본 등록 사본과 해시를 보존한다.
이번 범위에는 커밋·push를 포함하지 않는다. 로컬 기록과 해시로 인계한다.

2. 데이터·노출
전체 SIPP 원본은 기존 집계 노출이 있다. E055/E056의 모든 기존 역할을 보존한다.
학습은 원래 group fit 5922명만 사용한다. 그중 기존 metric-fit 1184명,
reference 3554명, inner selection 592명, replay 592명 역할을 그대로 둔다.
beta 목적함수는 metric-fit/reference만 사용한다. 저장된 일차 가중치는 이미
학습된 개발 산출물이다. inner selection/replay를 새로 점수화하지 않는다.
내부 행 분리는 새 SSUID 독립 검증이 아니다.

A019 고정 outer 역할 유지:
- oracle 1918명 /1124 SSUID
- selection 2007명 /1130 SSUID
- audit 2074명 /1177 SSUID
이들의 PREDICT 응답·점수는 미열람이지만 GIVEN 예측 질의에는 이미 사용됐다.
누적 모델 사용17999명/12339 SSUID와 원천 집계 노출을 기록한다.
E058 비활성·λ 기록을 본 뒤 정한 설계라는 사실도 기록한다.
새 seed, 표본, 역할 교환, 과거 calibration1866 재개방은 금지한다.

3. 허용 파일·자원
새 파일만 구현:
- scripts/screen_e059.py
- tests/test_e059_interactions.py
- docs/experiments/E059-leaf-donor-interactions.md
- docs/analysis/E059-outputs/ 아래 등록·검증·결과·closeout·exposure 기록
- ignored external/e059/ 아래 새 캐시·동결 출력·단계 marker
단일 소유자가 status/log/tree를 갱신한다. E번호 생성 후 tree 갱신은 허용한다.
src/, submissions/, E058/A019 산출물과 marker는 수정하지 않는다.
기존 사용자 변경 파일은 건드리지 않는다.

전체 작업 시작부터60분, 누적 beta 최적화120초, CPU2 threads,
프로세스 트리 합산8 GiB 상한. GPU·설치·유료 자원 금지.
새 base/E041 fit 0회, beta 최적화 최대1회, 재시작·재fit·자동 예비 실험 없음.
상한은 예측 시간이 아니다. import 포함 전체 시간과 최적화 시간, 합산 RSS와
commitment를 측정한다. 오류·상한 초과는 기록 후 종료한다.

4. 무학습 진입 검증
59 source hashes와 A020에 기록된5 artifact hashes를 재확인한다.
불일치/누락이면 STOP. 캐시를 새 fit으로 복구하지 않는다.
이 별도 연구에 한해 검증된 E058 first-stage.pkl, masked-frame.pkl,
library.npz 및 A019 fit/evaluation key 파일의 읽기를 허용한다.
다른 모델·응답·점수 캐시는 열지 않는다.
fit5922/전체query5999, 모든 query PREDICT=-1 또는 NaN, 순서·옵션·역할·SSUID
경계·원래 donor/fit 역할을 검증한다. labels/query 응답을 donor에 넣지 않는다.
원래 active=[]와 λ를 보존한다. weights/share의 유한성, 원래 learned weights,
원래 metric donor32와 캐시 R/library baseline 일치를 확인한다.

후보 적용 규칙은 원래 λ>0인 말단 항목/버킷이다.
기록상 EHREAS_BIR(.1,.1), EHREAS_OTH(0,.1), EHREAS_COR(0,.1)만 해당한다.
HOSPITALIZED의 λ=0, 세 항목에 자식 없음, 일곱 head 구조를 확인한다.
불일치하면 범위를 바꾸지 않고 STOP.

query donor32는 E058에 저장됐다고 가정하지 않는다. 저장된 signatures와
initial weights, visible5922 bank, 기존 candidate_indices(k=32)의 정확한
규칙으로 한번 계산하고 순서·해시를 A/B 공통으로 동결한다.
metric-fit donor32는 저장된 metric 호출의 앞1184행을 사용한다.
두 donor pool 모두 GIVEN만으로 정하며 labels는 원래 fit5922에서만 읽는다.

λ>0인 모든 query에서15 pair feature가 각각 donor 간 상수이면 모든 beta가
softmax를 바꾸지 못한다. 이를 확인할 경우 fit·응답 개방 없이 scoped STOP.
통과는 효과 증명이 아니다. 추가 rank/항목/seed 탐색으로 후보를 바꾸지 않는다.

5. 고정 후보·학습
R = 저장된 E058 generic E041 raw output. 재학습하지 않는다.
A = 고정 donor32에 원래 learned 일차 가중치만 적용한 evidence의 출력.
B = A의 score에 sum_{j<k} beta_jk e_j e_k만 추가한 evidence의 출력.
6개 GIVEN의 schema 순서대로15 pairs 모두 사용한다.
원래 일차 weights, metric retrieval share r, bank+.5 prior는 고정한다.
e_j는 query/donor GIVEN 정확 일치 indicator다.

beta=0 시작, bounds[-2,2], penalty .01*sum(beta^2), L-BFGS-B maxiter50,
ftol1e-7, 단일 시작점. scripts/screen_e058.py:objective와 같은 목적함수:
-mean_{1184 queries,7 heads} log[.001+(1-K*.001)*
 ((1-r)*prior_truth + r*sum_d softmax(score)_d*1[y_d=y_query])]
 +.01*sum(beta^2).
share/weights/penalty/head/grid는 재학습·탐색하지 않는다.
비유한 결과는 STOP. 유한한 maxiter 종료는 그대로 유지하고 공개한다.
원래 marginal 목적함수와 배포 λ의 불일치는 남으며 calibration 수리라고
주장하지 않는다. fit 내부 labels의 의존성을 외부 SSUID 독립성과 혼동하지 않는다.

부모와 기존 λ·bucket이 그대로인 말단 항목에 한해:
A = R + λ*(e_additive-e_legacy)
B = R + λ*(e_pair-e_legacy)
나머지는 R을 그대로 복사한다. lambda 및 concentration은 재계산하지 않는다.
stored active를 수정하거나 기존 production replacement를 강제 활성화하지 않는다.
cached_renderer/link_sharp.predict/supervised_layer를 새로 호출해 fit하지 않는다.
기존 cached_renderer의 memo closure는 세션 간 저장되지 않았다.

실제 평가 후보는 고정 공통 혼합비 .5:
A_half=R+.5*(A-R), B_half=R+.5*(B-R).
alpha 탐색은 없다. .5는 E058의 최대 shrinkage arm을 미리 택해 변경량을 제한한
것이며 최적이라고 가정하지 않는다. λ0 항목을 켜지 않는다.
비교는 B_half-R와 B_half-A_half 두 개다. A 단독 자동 승격은 없다.

6. 기술 검증과 동결
합성 소형 fixture만으로 먼저 다음을 확인한다:
-15 pair 순서, beta0 posterior, analytic/finite-difference gradient
-부모 고정 leaf 교체식과 직접 (1-λ)*G+λ*e 혼합식의 일치
-beta0=A, R 보존, λ0/부모/다른 head exact identity
-bucket/donor/일차weights/λ 불변, query label 오염 방지
-공식 normalize+floor, cluster SE, paired bootstrap와 단계 접근 순서
fit을 실행하는 통합 test는 만들지 않는다.
실제 캐시에서는 행/옵션 정렬·shape·유한값·비음수·합계>0을 확인한다.
음수를 clipping해서 통과시키지 않는다. beta0=A는 동일 연산 경로에서 exact,
대수적 복원 검사는 max_abs<=1e-12로 사전 고정한다.
불일치하면 새 fit/후보 변경 없이 technical STOP.

R,A_half,B_half와 원천·코드·등록·역할·출력 해시, 종료 상태, 시간·메모리를
모든 새 응답 접근 전에 동결한다. 새 단계 marker는 배타적으로 생성한다.
E058 markers와 출력은 건드리지 않는다. B_half=A_half exact이면 응답을
열지 않고 종료한다. 증명 가능한 출력 동일성은 응답으로 재확인하지 않는다.

7. 단계별 점수 접근과 판정
일곱 head 모두 pooled skill을 사용한다. K는 부모2, 자식각3:
U=(log(2)+6*log(3))/7.
raw vector를 정규화하고 .001+(1-K*.001)*p를 적용한 뒤 true-class log를 취한다.
개별 head/asked subset 결과를 보고 후보를 수정하지 않는다.
응답은 허용 단계의 정확한 SSUID/PNUM 필터를 Parquet scan에 적용한 후
필요 컬럼만 읽는다. 전체 응답을 메모리에 올린 뒤 필터하지 않는다.

oracle: 고정 R,A_half,B_half만 한번 점수화한다.
두 delta skill(B_half-R, B_half-A_half)가 모두>1e-10일 때만 계속한다.
아니면 STOP하고 selection/audit는 열지 않는다.
원하면 응답 개방 전에 각 비교의 mean_{query,head} max_class
log(p_B/p_comparator)/U를 계산할 수 있다. 어느 상계가<=1e-10이면 모든
label assignment에서 해당 gate가 불가능하므로 무응답 STOP한다.
이는 이미 학습·동결한 유한 출력의 feasibility screen이며 모든 beta나
UNHCR의 oracle 상계가 아니다. E058/E055의 STOP과 기준은 그대로 보존한다.

selection: 동일 세 출력만 한번 점수화한다. alpha는 선택하지 않는다.
각 비교의 person별7-head mean log difference d_i, N명, G SSUID,
n_g=그룹크기, S_g=sum_group(d_i), m=sum(d_i)/N에 대해:
SE=sqrt(G/(G-1)*sum_g(S_g-n_g*m)^2/N^2).
두 비교 모두 m>0 그리고 m>2*SE여야 audit 진행.
실패하면 R 유지·STOP, audit 미열람. 통과 정책과 비교군을 동결한다.

audit: R,A_half,B_half만 한번 점수화한다. 두 paired delta skill을 계산한다.
numpy.default_rng(5801), SSUID bootstrap2000회, 매회 G개 그룹 복원추출.
같은 draw를 두 비교에 사용하고, 그룹 delta 합/그룹 인원 합으로 사람가중
평균을 계산한다. 각 비교의 central97.5% interval은 linear quantile
[.0125,.9875]로 정한다. 두 하한이 모두>0일 때만 후속 UNHCR 연구 근거.
두 구간의 Bonferroni nominal simultaneous95%는 bootstrap 근사이며
학습 변동·기존 설계 적응·survey weights·domain shift를 포함하지 않는다.
둘 중 하나라도 실패/불확실이면 이 고정 연구를 STOP.
audit로 alpha/head/seed/가중치를 바꾸거나 추가 arm을 열지 않는다.

8. 종료·산출물
preflight/기술/자원/oracle/selection/audit 어디서든 STOP하면 원인과 범위를
기록하고 종료한다. 미열람 역할을 명시한다. 자동 예비 실험은 없다.
긍정적이어도 SIPP의 고정 weights·기존 λ·해당 donor/표본 조건부 결과다.
E041 전체 대비 비교와 beta 추가 비교를 구분한다. S2 후보·UNHCR 개선·TEST
채택으로 자동 승격하지 않는다. 이번 세션은 ZIP·method·공식 all3 실행 없음.

필수 산출물:
- 사전등록 원본과 실제 실행 코드 해시
- 의미적 preflight 및 fixture 검증 결과
- 3-arm 동결 manifest와 단계별 결과 또는 가장 이른 STOP certificate
- fit 횟수, 전체/fit 시간, 메모리, changed-vector 수
- closeout.md, exposure-ledger.md, S0용 다음 판단 인계
- status/log/tree 갱신, 변경 파일 목록, 실제 HEAD, 미커밋 상태
행 단위 자료는 ignored external/e059/에만 둔다.
E058 STOP, E041/E025, E057 parked, S3 중단, A018 사용자 미확정 유지.
```
