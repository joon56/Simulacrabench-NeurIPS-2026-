# A042 — E062 사후 판단과 round 조건부 donor 순위 계약

2026-10-09 KST. S0 문서 검토·전략·인계.
**E062 UNRESOLVED 수용; RECOMMEND_BOUNDED_S1_INFORMATION.**
주력은 UNHCR의 **query round 조건부 donor reranking** 한 가족에 대한
40분 정보·수식·생산 연결 계약 검토다. 구현·학습·새 E·S2 자격 판정이 아니다.
[다음 S1 프롬프트](A042-outputs/s1-handoff.ko.md).

## E062 종료 판단

사용자 제공 E062 ID969351와 등록 comparator E041 ID933094의 네 공개 문자열은
Grand .6433333333 / UNICEF .5200000000 / WB .4900000000 / UNHCR .9200000000으로
같다. Finished, Development/phase29772와 파일명은 기존 기록에 부합한다.
원래 WB/Grand tie arm UNRESOLVED를 유지한다. 공개상 새 best를 읽지 못했다는
뜻이며, best-update 이벤트는 미제공이다. 정확한 효과0·예측 동일·활성 여부·
전체 순서형 가설 반증이 아니다.

S1의 WB whole skill +.0002723772, 대상16 log score −.0007987550,
Not answered −.0044084735를 함께 보면 현재 E062 정책에 추가 자원을 쓸 근거는
강해지지 않았다. 같은 정책 재제출·seed/head/threshold 조정은 권고하지 않는다.
기술 release PASS는 그대로 보존하며 E041 incumbent/E025 fallback/E062 parked다.

[사후 원문/비교](E062-outputs/s2/post-result/result.ko.md)의 출처 한계를 수용한다.
E041 extract의 scorer metadata 부재, 원격 ZIP bytes 미확정, created_when이
플랫폼 생성 메타데이터라는 점은 그대로다. 현재 플랫폼 조회·ZIP 재해시 없음.
사후 검증에 명시된 문서29개 해시는 모두 일치했고, fragment에 바깥 괄호만
추가한 JSON의 필드도 일치했다. 과거 manifest를 현재 SCORES에 맞춰 바꾸지 않는다.

## 다음 우선순위 비교

| 선택지 | 근거 | 반대 근거·검증 한계 | 비용과 현재 판단 |
| --- | --- | --- | --- |
| **UNHCR round 조건부 donor 순위 계약** | E041의 고정 section metric에 구체적 표현 제한; wave는 공개 GIVEN; 공개 schema에 round별 기록 차이 존재 | base가 이미 wave 사용; 같은 K32 안에 유용한 대안이 없을 수 있음; 표본 분할·과적합·proxy selector 한계 | 원격/학습 없는40분 계약 검토만 주력 |
| WB 트리 또는 다른 입력 표현 | 공유 신경망과 다른 학습 편향 가능 | E039/E040 검증 결함은 A006이 이미 지적; E046/E051의 제한된 Adult oracle 낮음; WB에 좋은 보완성·회복 손실량 근거는 없음 | 불가능 판정 아님. 지금 새 구현으로 보내지 않음 |
| E062 head/비응답/seed 수정, A040 수리, VAF 의미 가정 | 기존 코드·자료가 존재함 | E062 새 효능 근거 없음; A040 원인·수리 근거 없음; A039 연결/결측 미해결을 가정으로 덮으면 평가 자체가 흔들림 | 현재 우선순위에서 제외, 기존 parked/HOLD 유지 |

선택 근거는 E041 검색 계열의 실제 긍정적 과거 관측, 현재 source에서 확인 가능한
개입 차이, 작은 계약 검토 비용이다. E041의 hosted 이득을 metric 하나의 인과효과로
확정하지 않는다. 이 비교는 검토한 경로 사이의 우선순위이며 전역 최선·우승확률
계산이 아니다. WB .49가 낮거나 UNHCR .92가 높다는 이유만으로 기회 크기를 정하지 않는다.

## 관측 사실과 새 가설

**사실:** src/models/supervised_retrieval.py의 metric_objective와
_replace_evidence는 section마다 하나의 w_s를 모든 query에 사용한다:
`score_s(q,d) = sum_j w_sj * 1[x_qj=x_dj]`.
후보는 original initial metric으로 고른32개이며, fit와 inference의 learned
metric은 그 후보 안의 posterior를 바꾼다. _sig_data_all은17 GIVEN 모두를 사용한다.
따라서 wave 일치 항도 이미 존재한다. E041 전체 모델이 round를 무시한다는 주장은 틀리다.

**사실:** 현재 공개 unhcr.json의 wave는 GIVEN, 값은1/2다. 두 round는 같은
May–June2025 fieldwork에 속하고 host-country 질문지는 동일하다. 공개 설명은
5개 multiselect family59문항의 sentinel이 round2에만 나타나는 기록 차이도 명시한다.
이는 응답 행을 조사해 얻은 사실이 아니라 이미 공개된 schema 설명이다.
panel 연결·시간 경과·같은 가구 재조사를 새로 가정하지 않는다.
E036의 과거 panel 해석은 현재 작업의 전제로 사용하지 않는다.

**가설:** 같은 section 안에서도 query round에 따라 age/가구 구성/지리 등
GIVEN 일치의 유용성이 다르면, 공통 w_s 대신 공통값으로 축소되는 w_s,r(q)가
동일 K32 안에서 더 유용한 donor 순위를 만들 수 있다. 새 특징 신호가 아니라
기존 GIVEN을 사용하는 검색 함수족의 변경이다. 다른 context·pool 확장·새 expert·
lambda 세분화를 함께 넣지 않는다.

**수식상 구별:** 두 query의 round만 다르고, 각 query의 두 donor가 query와
같은 round라고 하자. 다른 두 GIVEN의 일치 벡터가 두 query 모두 A=(1,0),
B=(0,1)이고 나머지 일치 특징도 같으면, 고정 일치 가중치와 모든 일치-쌍
특징은 두 query에서 같은 donor 순서를 만든다. round1 가중치(2,1),
round2 가중치(1,2)는 순서를 뒤집을 수 있다. 이는 표현 차이의 손계산 예시이며
실제 데이터에 이런 경우가 있다는 증거·실행 fixture·효능 증거가 아니다.

## 과거 실험과 정확한 경계

- E036: same/cross-round **top donor 관계별 lambda**. 여기서는 query 자신의
  round에 따른 **donor 순위 metric**, 원래 lambda algorithm/minimum30 유지.
- E043/E045: metric 기반 pool 교체/확장. 여기서는 원래 K32 identity/order와
  original search를 유지하며 밖의 donor를 복구한다고 주장하지 않는다.
- E047/E049: 고정 donor/PFN의 최종 혼합 share 선택. 새 독립 expert를 넣거나
  최종 혼합 selector를 복제하지 않는다.
- E058/E059: e_j e_k라는 **일치 지시자의 쌍**. raw query round×e_j와
  구별된다. E058 active0 STOP과 E059 matched-additive 대비 선택 실패는 보존하며,
  더 복잡한 reranker가 이득을 보장하지 않는 반대 근거로 반영한다.
- E060: sentinel을 제외한 metric-fit loss. 여기서는 원래 all-cell 목적함수를
  임의 변경하지 않는다. E060 공개 동점을 이 경로의 긍정 근거로 쓰지 않는다.
- A021/A023/A024/A037: proxy와 최종 selector 비교 연구 HOLD 별개.
  새 reranker가 기존 proxy/replay 결함을 해결한 것으로 쓰지 않는다.
- E062: WB 출력 head 구조 변경. 본 과제는 UNHCR 검색 내부 계약 조사이며
  E062를 구제하거나 WB intervention을 연장하지 않는다.

E045/E047의 큰 permissive oracle과 작은 learned gain은 특히 강한 경고다:
표현 가능한 순위가 늘어나는 것과 GIVEN으로 유용한 순위를 학습하는 것은 다르다.
이 구별을 해결하지 않은 채 S1 구현·S2 제출로 바로 넘기지 않는다.

## S1이 해결할 한 판단과 종료 조건

질문: **단 하나의 wave 조건부·공통값 축소 reranker를 E041과 명확히 비교할
수 있는 고정 계약으로 만들 수 있는가?** 권한은 정보/수식/정적 소스 검토뿐이다.

필요한 계약:
1. 공통 metric과 두 round 보정의 한 parameterization, bounds/penalty/지원 부족
   fallback. E041 endpoint가 수식뿐 아니라 실제 상태·렌더링에서 무엇을 고정해야
   정확히 재현되는지 지정한다. 새 config/context/grid를 여러 개 만들지 않는다.
2. bank/metric-fit/selection/replay 및 future outer evaluation의 정보 접근 표.
   learned metric을 고르는 share와 실제 per-item lambda의 차이, 기존 selection
   재사용·refit 변화·in-sample replay를 명시한다. 동일 자료에서 재선택한 결과를
   독립 audit으로 쓰지 않는다. 현재 A022 역할을 가져와 채우지 않는다.
3. current E041 및 matched common-metric arm 중 어느 비교가 무엇을 답하는지,
   원래 .003/2SE selector·lambda minimum30/zero fallback 보존 가능성, 전체
   절차 개입 범위. 수용 불가능한 정책 변경이 필요하면 계약을 FAIL/HOLD로 닫는다.
4. 실제 caller graph에서 추가 metric fit·full-stack/neural/refit 횟수, tensor/
   후보 메모리와 all3 비용 계획. 원격·새 의존성 없이 가능한 최소 범위.
   실행시간은 미측정이라고 쓴다. 17개 GIVEN의 단순2 metric+공통 share라면
   좌표35개(원래18개)라는 산술은 대조용이며 허용 구현/실측 비용이 아니다.
5. 별도 미래 기술 검증의 영향 경계와 종료 기준. 현재 S1은 구현·검사를 실행하지 않는다.

**CONTRACT_READY_FOR_S0_REVIEW:** 위 항목이 모순 없이 하나로 고정되고 과거 연구와
차이·채널 한계·총비용을 명시한 경우. 효과 PASS나 모델 실행 권한이 아님.
**REJECT_DUPLICATE_OR_UNINFORMATIVE:** 기존 알고리즘과 동치, 변경이 donor-constant,
새로운 판독이 없음, 또는 범위에 맞는 비교를 설계할 수 없는 경우.
**HOLD_SPECIFIC_INPUT:** 필요한 단일 문서·계약·권한을 소유자/확보 경로와 특정.
예비 작업은 그 기각/HOLD closeout뿐이다. 같은 자료로 후속 검토를 자동 반복하지 않는다.

## 관측 채널·oracle·우선순위를 바꿀 입력

지금 허용된 채널은 기존 문서/공개 schema/허용 source/기존 결과 집계다.
수치 oracle을 계산하지 않는다. 새 frozen predictor library와 독립 허용 labels가
없고, Adult에는 이 CATI round 기록 기제가 없으며 SIPP 보호 역할을 사용할 수 없다.
원래 synthetic은 공학 채널이며 임의 round 차이 주입은 가설을 전제한 방향 검사다.
E041/E043/E045의 과거 oracle 값을 이 새로운 정책의 oracle로 옮기지 않는다.
동일 donor simplex oracle은 포함관계가 입증돼도 해당 자료/후보에만 한정되며
context-conditioned policy의 learnability·실제 ERPIS 효과를 말하지 못한다.

우선순위를 바꿀 근거는 명확하다:
- S1이 표현 차이를 소거하거나 정확한 비교/지원 부족 fallback/비용 계약을 못 만들면
  이 경로의 구현을 권고하지 않는다. 문제를 푸는 특정 새 source/설계 근거가 재개 조건.
- 계약이 성립하면 **그때** 별도 bounded exploratory 구현/기술 범위를 S0가 판단한다.
  실제 donor 가중치 변화만으로 개선을 인정하지 않고, fixed UNICEF/WB controls와
  전체213 출력·E025/E041 release 비교·전체 all3 자원이 필요하다.
- 새로운 공식 VAF export/linkage/missingness 명세가 생기면 A039/A037 채널 우선순위를
  재검토할 수 있다. 현재 문의 무응답을 응답 의미의 확정으로 대체하지 않는다.
- A040 build/resolve 종료 crash의 구체적 원인·검증 가능한 수정 근거가 생기면
  인프라 경로 재검토 가능. 기존 조사·성공 suite/120초 대기를 자동 반복하지 않는다.
- 향후 실제 hosted 결과가 있어야 실제 전체 후보의 판독이 가능하다. favorable/
  unresolved/adverse/technical/출처보류 arm을 사전에 정하고 한 정책 반복을 금지한다.
  구현 전 현재 단계에서 기대 Grand나 보편적 +.005 문턱을 부여하지 않는다.

## 읽기·보존

AGENTS/CLAUDE/status 현재항목/log 최신3개/workflow와 E062 사후 인계를 순서대로 읽음.
workflow2026-10-05-r5 SHA256
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
S2 자체 read receipt는 session-reported. S0 실제 tool reads·source 해시·쓰기 범위는
[A042 verification](A042-outputs/verification.json)에 기록함. 새 A042 충돌 없음 확인.

기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, branch work/e050-submission.
진입 dirty102/조회한 Python/pythonw/uv jobs0. 원격 작업 부재 인증 아님.
karpathy-guidelines로 source 관측/가정을 구분했고 brainstorming으로 경로를 비교함.
사용자의 S0 기록 범위가 skill의 commit/구현 전환 기본값보다 우선함.
완료 확인은 새 문서·링크·해시 보존 검사만 수행함.

E041 incumbent/E025 fallback, E057/E060/E061/E062 parked.
E058 STOP/E059 STOP_SELECTION, A023/A024 empirical HOLD, A039/A040 및 모든 STOP/HOLD.
17999명/12339SSUID·집계·A022 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격, A018 사용자 미확정/S3 중단.
S2 새 후보 없음. 모델·데이터·cache·검증 재실행·ZIP·플랫폼·commit/push·서브에이전트0.

