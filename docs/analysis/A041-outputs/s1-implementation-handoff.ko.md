# 다음 세션 제목

S1 — WB16 순서 조건부 head 구현·합성 기술 검증

아래 블록을 별도 S1에 그대로 전달한다. 사용자의 전달이 실행 지시이며, 이 파일 작성/S0 권고만으로 실행하지 않는다. 이전 A041 정보 조사 프롬프트를 반복하지 않는다.

```text
SimulacraBench / HSCC 별도 S1을 시작한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

이번 S1에서 변경 기관을 World Bank로 명시적으로 지정한다. A041의 고정
WB16 순서 조건부 head 후보 하나를 구현하고, 아래 기존 합성 TRAIN/DEV의
기술·회귀·비용 비교를 실행한다. UNICEF/UNHCR는 E041 그대로 통제한다.
이는 이 별도 S1의 bounded exploratory 구현/기술 검증 지시다. 독립 실증,
실제 WB 효과 확인, S2/제출/TEST 실행 지시가 아니다.

1. 진입·동결

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md를 실제 읽고 역할·유형·개정·허용 범위를 보고한다.
workflow r5 SHA256:
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23
더 최신 개정이 있으면 현재 사용자 범위를 보존하면서 차이를 기록한다.
HEAD/dirty/local active jobs를 확인하고 기존 변경을 보존한다. 다른 작업을
임의 종료하지 않는다. 과거 manifest에 맞춰 현재 파일을 되돌리지 않는다.

읽을 자료:
- docs/analysis/A041-outputs/s0-review.md, s0-review-verification.json
- docs/analysis/A041-outputs/s1/{contract,cost-accounting,closeout,
  source-register,exposure-ledger}.md, verification.json
- docs/analysis/A041-wb-ordinal-head-review.md 및 inputs.json
  (inputs.json은 docs/analysis/A041-outputs/ 아래)
- docs/experiments/E011-ordinal-smooth.md
- docs/analysis/E061-outputs/frozen-inputs.json: 허용 synthetic/source identity
- 필요 source: E041/E025 snapshot main.py, 관련 src/models, 공식 score.py,
  scripts/check_e061_tied_heads.py의 mask/비교/계측 경로. 원본 수정 및 기존
  검사 스크립트 재실행 금지. 아래 명시한 baseline import/predict는 허용한다.

주요 고정 identity:
- A041 s1/contract.md:
  c65c4eb4eb75a1a15fda8416c5c7988f6ef47464460ac9b195201675cac20ca8
- submissions/2026-09-19-E041/main.py:
  22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
- submissions/2026-09-09-E025/main.py:
  00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9
- external/starter-kit/data/world_bank.json:
  6b3760742c6e864eb8d0bb2f9ec523a19a486b73282d79432dbcca16e3664125
모두 허용 파일만 비교한다. manifest 전체를 무조건 재해시하지 않는다.

E062 번호 충돌부터 확인한다. 비어 있으면 E062-wb-ordinal-heads로 등록;
충돌이면 다음 미사용 번호와 새 출력 경로를 고정한다. 기존 E/A 기록 덮어쓰기
금지. 구현/점수 전에 registration에 대상·정책·관측 채널·노출·판독·비용을
기록하고, 전체 실행 전에 source/input/split identity와 deadline을 동결한다.
소스 완성 전 초기 등록과 실제 실행 freeze를 구분한다.

2. 목적·기존 작업과 차이

질문: WB16의 affine conditional-logit 학습 편향을 넣은 전체 절차가
통제 기관을 유지하고 전체 출력/회귀/로컬 비용 계약을 충족하는가?
기전은 순서 조건부 함수족이다. E011 post-hoc Gaussian kernel이나
E030 GIVEN 거리, E061 UNHCR tying을 재실행하지 않는다.
nominal softmax도 정상 분포다. 순서 정합성만으로 개선을 주장하지 않는다.
비응답 분리·초기화·공유 trunk·config/w/λ 선택 결과가 함께 변하므로
순서만의 단독 인과효과라고 부르지 않는다. E011 null/기존 STOP 유지.

3. 후보 하나 — A041 contract를 변경 없이 구현

대상은 ungated WB16 전부, 아래 sc_nstd_ 접미사:
extra, agree, consc, stability, open, gm, pp, s_aware, s_manage,
soc_aware, realistic, invest, artistic, social, enterp, convent.
범주 순서는 <2.5, 2.5-3.0, 3.0-3.5, 3.5-4.0, 4.0-4.5,
4.5-5.0, Not answered. 정확한 이름/순서/ungated/대상 수를 확인한다.
불일치하면 head를 임의 제외하거나 sentinel을 추측하지 않는다.

기존 shared GIVEN trunk z에서 m=sigmoid(g), r_k=sigmoid(t_k), k=1..5.
S0=1, Sk=product(r_1..r_k), S6=0; q_j=S(j-1)-Sj.
p_j=(1-m)q_j, p_NotAnswered=m. 안정적 logsigmoid 누적으로 일곱 logp를
구성한다. 자세한 수식/인터페이스는 contract 준수. 최종 floor/temperature/
clamp/추가 prior/역순/head별 fallback/aux loss를 추가하지 않는다.
Not answered는 정상 범주이며 gate sentinel이나 순서 끝값이 아니다.
범주 NLL은 셀당 -log p_y 한 번. 기존 pooled denominator 유지;
risk-set 크기로 개별 BCE를 나누는 CORN 원전 loss로 교체하지 않는다.

원래 nominal net 전체를 먼저 생성하고 대상 Linear 행0..4를 t1..t5,
행6을 g로 복사하며 행5는 버린다. 추가 난수 소비 없이 비대상 parameter/
trunk/RNG를 보존한다. 초기확률 비대칭은 등록된 개입 일부다. 빈 risk set의
통계적 식별은 보장되지 않으며, 관측 뒤 bias 보정/빈도 초기화를 추가하지 않는다.

기존 configs(64,2,0.0)/(128,2,0.1), 순서, seed, optimizer, patience,
inner-stop, outer config+w, 동점 규칙, final refit, ladder/gate/donor/λ 유지.
outer fit 중간 재학습을 추가하지 않는다. w=0도 원래 final refit을 수행한다.
선택값은 후보에서 재계산하며 E041의 선택값을 강제하지 않는다. λ minimum30/
zero fallback 유지. WB 나머지60개는 trunk 등을 통해 변할 수 있고 전부 평가한다.

4. 허용 변경·데이터

새 src/models/wb_ordinal_heads.py 및 해당 후보의 새 tests/check script,
새 E기록/outputs와 status/log만 작성한다. 필요 최소 wrapper/새 candidate
복사본으로 연결하되 원래 production modules/E041/E025 snapshot은 수정하지 않는다.
기존 Python/Torch 환경만 사용. 새 설치/취득/환경/클라우드/Modal/GPU 없음.

이번 S1에 한해 다음 세 노출된 synthetic 파일의 identity 검증과
TRAIN/DEV 역할 읽기·학습·예측·engineering 채점을 허용한다:
external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet.
기존 E061 frozen-inputs.json의 각각 SHA256:
unicef: 8e7c659d277c5145c7a8a6d055ac59a7dd3c35699317741239b6b1969bce1488
world_bank: 4592bed873410c5248edf1205e5cab41dd30494926e3b49f8da598e266758c8a
unhcr: 5d00075706e0a7beafdc8a70acfe07cde1f489048741eb2f3ae1fababdb72774
위 값은 S0가 새로 검증한 해시가 아니다. 불일치면 새 입력을 즉석 대체하지 않는다.
Parquet reader에 TRAIN/DEV 필터 적용; synthetic TEST 역할 접근/분석 금지.
원래 config/load_schema/options_for를 사용해 세 runtime schema를 정규화한다.

GIVEN-only feature, EXCLUDE와 query 전체 PREDICT block을 모델 진입 전에
차단한다. DEV truth는 평가기만 보유. 내부 train/stop/outer/refit 역할 및
lambda replay 재사용을 기록한다. 내부 선택·synthetic은 독립 실증이 아니다.
실제 보호 응답/키/옛 prediction·model cache/Adult/SIPP/VAF 접근·재해시 금지.
fresh WB oracle은 없음. 수치 oracle이나 예상 Grand를 만들어 진입 조건으로
삼지 않는다. 합성 주입 예제는 구현 검증 범위로만 해석한다.

5. 검증 순서·판독 — 결과를 보기 전에 등록

(a) 새 영향 검증을 먼저 한다. 수식·7범주 순서/정규화·극단 logits·미관측
범주/빈 risk set·Not answered gradient·exact NLL/pooled count·전체 query mask·
두 config의 비대상 초기 parameter/RNG·inactive/fallback을 확인한다.
수식/gradient 검증은 작은 tensor/backward까지, 추가 optimizer fit은 하지 않는다.
float64 확률/NLL 동등성 atol/rtol1e-10, float32 1e-6/1e-5를 사전 고정한다.
원래 비대상 초기 parameter/RNG는 exact equality. 유한 logits ±1000에서도
logp/gradient finite 검사; raw underflow0은 공식 floor와 별도로 기록한다.
관측 뒤 tolerance 확대 금지. 원래 성공 suite 전체를 반복하지 않는다.

(b) 모두 통과하면 source/input/split freeze 후 clean E025, clean E041,
고정 candidate의 all3 각1회. 각 model/instrument 과학 호출1회 계획.
cache 없이 fresh process로 생성하고 아홉 raw output을 모두 동결한 뒤 채점한다.
UNICEF17856/WB39520/UNHCR132273, 합189649 vectors의 순서/shape/finite/
비음수/양의 합을 검증한다. UNICEF/UNHCR candidate-E041 raw max차이0 필수.
WB 최종 output의 실제 변화 수/max차이를 기록한다. 전부 exact 동일면
NO_OP/판독 가치 미확인으로 반환하며 w/λ/활성 문항을 강제로 바꾸지 않는다.

(c) 공식 score source의 normalize/floor(.001)/score 함수로 in-process
engineering 비교한다. 모델이 floor를 미리 적용하지 않는다. 공식 CLI/all3
release·ZIP 검증과 구분한다. WB 전체 skill/log score가 주 판독이다.
16/나머지60/Not answered 진단은 설명용; head 선택이나 정책 수정에 사용하지 않는다.
각 기관 candidate-E025 ≥ -.002 및 candidate-E041 ≥ -.002를 요구한다.
절대 skill 차이 기준이다. 보편적 +.005나 합성 양성 필수 조건은 추가하지 않는다.

기술·parity·자원·회귀 통과와 WB 변화가 있으면 EXPLORATORY_SOURCE_QUALIFIED,
S0 재검토로 반환한다. 기술 결함은 TECHNICAL_FAIL, 한도는 RESOURCE_LIMIT,
회귀 미달은 REGRESSION_HOLD, 불완전 검증은 INCOMPLETE로 사실에 맞게 분리한다.
합성 상승은 실제 WB/TEST 개선 증거가 아니며 작은 손실도 숨기지 않는다.
평가 셀 수를 독립 표본 수로 사용하거나 유의성/검정력을 주장하지 않는다.

6. 총비용·오류 처리

진입부터 gross120분, 마지막10분은 종료 기록. deadline 갱신/대기 임의 공제 금지.
CPU numerical threads2/GPU0/heavy worker1. owned controller+child tree의
RSS 및 private commitment 각각8GiB, .1초 관측. 부모 monotonic watchdog과
실제 계측이 준비돼야 과학 실행한다. 기존 계측을 최소 재사용하고 새 인프라 금지.
candidate all3는 startup/import부터 세 predict 전체≤900초.
집중 검증+세 절차 비교의 실제 computational child wall 합≤1800초.
pipeline attempt≤9/neural training attempt≤27, 실패도 소비한다.
내부 metric/ladder/선택/refit/렌더링/검증 시간을 누락하지 않는다.
겹치는 parent/child/stage 시간을 더하지 않고 wall과 cumulative worker를 구분한다.

첫 과학 오류나 한도 초과는 해당 owned worker tree를 중단하고 기록한다.
workflow r5에 따라 계약 안의 일반 구현 오류는 이 S1에서 수리·영향 검증한다.
오류마다 S0에 새 프롬프트를 요청하지 않는다. 단, 총 deadline/횟수/데이터/
과학 정책은 고정이고 성공 검사는 무변경 반복하지 않는다. fit allowance가
소진되면 수리됐다는 이유로 재학습을 추가하지 않는다. 점수로 model/seed/
head/context/threshold/grid를 바꾸는 구제는 금지한다.

7. 종료 산출물·다음 담당

새 E 등록/후보 source/영향 테스트와 함께 entry/read receipt, registration,
frozen-input/source manifest, 비교 결과와 raw output identity, 실행·자원 장부,
오류/수리 이력, exposure-ledger, verification, closeout, s0-handoff.ko.md 작성.
누락이면 필요한 입력·남은 검증·재개 범위를 특정한다. status/log에 결과 추가.
S0 결과 검토 전 S2로 넘기지 않는다. S2의 source/assembly parity, ZIP checker,
official all3, clean E025/E041 release 비교, SCORES 판독표는 이후 별도 범위다.
이 S1은 ZIP·제출 snapshot·tree·upload·commit/push·S2/S3/서브에이전트 실행 금지.

E041 incumbent/E025 fallback, E057/E060/E061 parked 유지. E058 STOP/
E059 STOP_SELECTION, A039/A040 및 모든 STOP/HOLD 보존.17999명/12339SSUID·
집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격, A018 사용자 미확정,
S3 중단, 현재 S2 후보 없음. 이번 구현 후보도 자동 incumbent/TEST 채택하지 않는다.
```
