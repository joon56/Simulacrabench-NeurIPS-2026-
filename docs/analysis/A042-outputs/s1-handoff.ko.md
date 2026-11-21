# 다음 S1 — A042 UNHCR round 조건부 donor 순위 계약 조사

세션 제목: **S1 | A042 round 조건부 검색 metric 계약 — 정보 조사**

아래 전체를 별도 S1에 전달한다. 현재 S0의 문서 작성은 실행 허가가 아니다.
사용자가 해당 S1에 이 범위의 수행을 지시할 때만 정보 조사를 시작한다.

```text
SimulacraBench / HSCC S1 — A042 정보·설계 조사만 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md,
docs/analysis/A042-post-e062-priority.md 순서로 실제 읽고 receipt를 남긴다.
현재 HEAD·dirty files·named local jobs를 확인한다. 기존 변경·실험/실패/manifest를
보존한다. workflow r5의 범위 내 오류는 같은 세션에서 고치되 총시간을 초기화하지 않는다.

역할/유형: S1 정보 조사. 모델 구현·실증·S2 제작을 허용하는 프롬프트가 아니다.
한 질문: 공개 GIVEN wave=1/2에 따라 기존 K32 donor 안의 가중치가 달라지는
단 하나의 축소 metric 계약이 과거 기법과 구별되고 비교·실행 가능한가?

필수 입력:
- docs/analysis/A042-post-e062-priority.md 및 A042-outputs/verification.json
- docs/analysis/E062-outputs/s2/post-result/{result.ko.md,comparison.json,verification.json}
- docs/experiments/E036-wave-lam.md, E041-supervised-retrieval.md,
  E043-section-candidate-search.md, E045-union-retrieval.md,
  E047-adaptive-final-evidence.md, E058-donor-pair-interactions.md,
  E059-leaf-donor-interactions.md, E060-content-target-retrieval.md
- docs/analysis/A006-dev-validation-audit.md,
  A021-selector-comparison-contract.md, A023-candidate-boundary-contract.md,
  A024-channel-precision-review.md, A037-winning-priority-review.md
- src/models/supervised_retrieval.py, dup_link.py, hh_cap.py, link_sharp.py,
  prob_link.py, shared_trunk.py, hh_link.py, hh_sharp.py;
  src/eval/retrieval_oracle.py; external/starter-kit/data/unhcr.json
- 직접 연결된 local source는 파일명과 읽는 목적을 기록한 뒤 정적으로 읽는다.
  코드 실행·import는 하지 않는다.
Source identity:
  supervised_retrieval.py SHA256
  2940338c5378de03303befb74e3834fbad631c0eb18f4ecb55d2cc39a471f879
  public unhcr.json SHA256
  b1175b6bdbd96e90a4defd83af20a38d711c6eca9fe3ce880109ff244abe80d9
  E041 main.py snapshot recorded SHA256
  22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
기록과 현재 허용 source 해시가 다르면 경위를 확인하며 과거 바이트로 되돌리지 않는다.

고정된 목적/차이:
E041 metric은 section마다 고정 w를 query/donor의 GIVEN exact-match vector에
곱한다. 새 검토는 query 자신의 wave 값으로 w가 달라지는 함수족이다.
E036의 same/cross top-donor lambda, E047 최종 혼합, E058/E059 match×match와
수식상 차이를 확인한다. E041 base와 기존 wave-match가 이미 갖는 정보도 반영한다.
E062 head를 다시 조정하지 않으며 A040/VAF 연구를 재개하지 않는다.

최소 범위:
- context는 wave 하나, 기존 K32 donor 검색/identity/order 유지.
- UNHCR만 향후 개입 대상으로 검토, UNICEF/WB exact E041 controls.
- shared common metric으로 축소되는 두 round 가중치 한 계약만 정한다.
  source에 있는 원래0..12 bounds 등과의 호환성, penalty/지원 부족 fallback,
  식별성 및 exact E041 endpoint를 명시한다.
- 다른 context/seed/head/K/threshold/grid 탐색, 새 expert, lambda 분할,
  sentinel 제외 loss, selector 목적함수 교체를 동시에 제안하지 않는다.
- .003/2SE selector, lambda minimum30 및 zero fallback 등 기존 정책 보존을
  기준으로 검토한다. 변경 없이는 정당한 비교가 안 되면 그 이유로 HOLD/기각한다.
  개선하려고 보호 역할·기준을 바꾸지 않는다.
- replay/selection/활성/최종 lambda 값이 새 metric의 영향으로 달라질 수 있는
  범위는 숨기지 않는다. 기존 proxy/full-output 불일치를 해결했다고 주장하지 않는다.

산출해야 할 계약:
1. 한 parameterization과 원래 함수족과의 차이/동치 손계산.
   donor-constant 항이 softmax에서 사라지는 경우, wave feature가 이미 있는 경우,
   한 round만 있거나 unknown/지원 부족일 때의 fallback을 포함한다.
2. bank/fit/selection/replay/final query의 정보 접근·상태 흐름.
   common arm과 candidate를 선택하는 자료 재사용, E041 refit/기존 in-sample
   replay, query PREDICT 마스킹, selector 비교 분포를 정확히 구분한다.
3. E041와 matched common arm 각각의 비교가 답하는 질문, 기존 bias/overfit
   한계. 독립 audit·D-P/D-R 연구 PASS라는 이름을 붙이지 않는다.
4. 실제 source call graph로 추가 metric/full-stack/neural/refit 횟수와
   peak tensor/후보 메모리, 전체 all3 자원 측정 계획. 실제 시간은 미측정.
   새 환경/클라우드·모델 취득 없는 최소 future 범위인지 판단한다.
5. future 기술검증 항목·정책 동결·관측 채널·진행/중단 기준.
   이 문서만으로 future 구현/과학 실행을 시작하지 않는다.

채널/oracle:
현재 문서·공개 schema·생산 source·기존 집계만. 새 응답/예측 없음.
S0의 손계산은 표현력 예시이며 실제 유용한 보완성 근거가 아니다.
새 frozen library와 적절한 labels가 없어 현재 유효한 수치 oracle 없음.
Adult의 과거 donor oracle을 재사용해 이 정책의 gain으로 쓰지 않는다.
synthetic은 노출된 공학 자료, round 기제를 주입한 sim도 실증 증거 아님.
향후 허용 채널이 필요한 경우 구체적인 입력·소유자·범위를 써서 반환한다.

시간: 진입부터 gross40분, 마지막10분은 기록. CPU2 이하/학습·모델0/
원격비용0. 자료 재검색 없이 기존 문서·source 정적 읽기만 한다.
생산 코드·검사 도구·fixture 작성/실행0. 불필요한 새 계획 프로젝트를 만들지 않는다.

허용: 지정 문서/공개 schema/source와 그 문서·source 해시 읽기, 수식 유도,
A042-outputs/s1/ 새 문서 작성, status/log의 이번 조사 결과 추가.
금지: 실제 GIVEN/PREDICT/키/Parquet/NPZ/cache/VAF 접근·해시·역직렬화,
fit/optimizer/predict/score·모델 import·fixture/test, 데이터 취득·새 웹 조사,
설치/다운로드/연락/로그인/Modal/원격, 모델·E기록·ZIP·tree 변경,
commit/push·서브에이전트·S2/S3 실행·TEST 선택.
기존 E041/main과 모든 연구 파일은 읽기 전용이다.

종료:
- CONTRACT_READY_FOR_S0_REVIEW: 하나의 모순 없는 비교/정보/비용 계약 완성.
  효과·local model/release PASS나 후속 실행 권한을 뜻하지 않는다.
- REJECT_DUPLICATE_OR_UNINFORMATIVE: 중복/상수 항/판독 가치 없음/범위 내 비교 불가.
- HOLD_SPECIFIC_INPUT: 정확한 누락 입력·소유자·확보경로·재개 조건.
예비 작업은 기각/HOLD closeout뿐. 다른 모델·context로 교체하지 않는다.

산출물 A042-outputs/s1/:
contract.md (차이·수식·정보/선택 흐름·비용·future 검사·판독 조건 통합),
closeout.md, s0-handoff.ko.md, verification.json (읽기/소스해시/허용 접근/
기존 기록 보존/시간). 필요 없는 중복 문서를 늘리지 않는다.

E062 ID969351 공개 tie UNRESOLVED; E041 incumbent/E025 fallback,
E057/E060/E061/E062 parked. E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD, A039/A040와 모든 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할·E059 소비oracle1918/1124 및
selection2007/1130, 보호audit2074/1177·calibration1866 보존.
A_half 비승격, A018 사용자 미확정, S3 중단, S2 새 후보 없음.
```

