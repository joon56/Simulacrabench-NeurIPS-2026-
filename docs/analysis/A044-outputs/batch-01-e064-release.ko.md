# B01 — E064 고정 후보의 남은 S2 release

상태: **PROPOSED / USER_EXECUTION_INSTRUCTION_REQUIRED**. 작성은 실행이 아니다.
Executor: S0와 별도 채팅 **EXEC-B01-E064**. 후보1, 추가 S1/새 E번호0.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1. Dirty source는 아래 hash로 식별한다.

## 진입과 전환 권한

사용자가 이 별도 채팅에 이 배치를 실행하라고 지시한 근거를 기록한다.
AGENTS → CLAUDE → status → log 최신3개 → workflow r6 → 이 문서 순서로 읽는다.
현재 HEAD/dirty/named jobs와 이전 writer 해제를 확인한다. 별도 S3의
docs/analysis/A044-outputs/s3-prep/closeout.md 및 kit-compatibility.md를 읽고
쓰기 담당을 인수한다. 없으면 조사를 자동 복제하지 말고 준비 미완료를 보고한다.

A043 구현은 E064 S1으로 이미 완료됐다. 다음 세 조건 충족 후 **남은 S2부터**
같은 실행 세션에서 조립·검증·ZIP 준비까지 진행한다. 다시 S0 승인을 묻지 않는다.

1. E064 완료 verdict와 고정 source identity가 일치한다.
2. S3가 확인한 현재 kit의 shape/order/masking/runtime-schema/floor/score 계약이
   고정 경로와 호환된다. 날짜·설명·새 sandbox 생성 기본값 변경만으로 S1을 다시
   돌리지 않는다. 실제 의미 변화나 비교 불능은 영향 범위를 특정해 S0로 반환한다.
3. 아래 허용 입력의 identity/환경/완료 provenance와 새 자원 상한을 확인한다.

S1 성공10검사·fresh R/H source all3는 재실행하지 않는다. 새 가설·후보를 추가하지 않는다.
이 조건부 S2 권한은 사용자의 배치 실행 지시에서 오며 파일 존재나 S0의 작성에서 오지 않는다.

## 목적과 반대 근거

Conditional CE의 trunk 직접 gradient를 차단하는 고정 H의 배포 일치성과 release
기준을 확인한다. S1 합성 UNHCR delta −.00008435360179303028은 개선이 아니다.
132225 vectors/lambda12쌍 변화, controls exact, metric/activity/donor/replay 불변을
함께 보존한다. 실제 이득·유의성·독립 audit·TEST 자격은 미확인이다.
새 seed/head/계수/stop/config/refit/선택 기준·expert/ensemble·기관 변경 금지.

## 허용 입력과 식별값

문서/정적 source:
- docs/analysis/E064-outputs/의 closeout/verification/freeze/entry/registration,
  exposure/reproduction/regression-history 및 attempts의 JSON·로그·실행 source.
- docs/experiments/E064-conditional-gradient.md, A043 S1 contract/S0 decision.
- src/models/conditional_gradient.py 및 freeze-01에 열거된 직접 의존 source.
  원본 모델/tests/runner는 읽기 전용이며 조립 복사본만 새 출력에 작성한다.
- E062/E063 완료 release 문서·freeze·환경·baseline provenance와 공식 checker/evaluator.
  S3가 확인한 공개 source만 사용하며 기존 kit checkout을 pull/reset/수정하지 않는다.
- submissions/2026-09-09-E025/main.py, submissions/2026-09-19-E041/main.py 및
  인접 요구사항/공개/점수 문서. 기존 snapshot은 수정하지 않는다.

허용 numerical 입력은 다음 **기존 synthetic3개와 NPZ12개만**이다.
- external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet.
  전체 파일 identity 확인은 허용하되 projection은 TRAIN/DEV만, TEST 행 요청 금지.
- docs/analysis/E064-outputs/attempts/R-01/vectors-{unicef,world_bank,unhcr}.npz 3개.
- docs/analysis/E064-outputs/attempts/H-01/vectors-{unicef,world_bank,unhcr}.npz 3개.
- docs/analysis/E062-outputs/vectors-E025-{unicef,world_bank,unhcr}.npz 3개.
- docs/analysis/E062-outputs/vectors-E041-{unicef,world_bank,unhcr}.npz 3개.

각 NPZ hash는 E064 attempts/score-01/frozen-predictions.json 및 E062
frozen-predictions.json을 따른다. E064 freeze-01.json/E062 frozen-inputs.json의
환경·입력·source·실행 완료를 대조하고 읽기 전에 exact allowlist를 새 freeze에 적는다.
Manifest에 있다는 이유로 다른 cache/NPZ/Parquet/VAF/원자료/키를 읽지 않는다.

| 항목 | SHA256 |
|---|---|
| E064 freeze-01.json | 5e8bd2eb84b73957e10f4ca21de858c8a5743290527364c45b09beeafb42245e |
| E064 verification.json | 46a3fc310a2e8177f7465bcf23e1d3ddd06eba9aa26ca83a76656ad29376e2e6 |
| conditional_gradient.py | 19cd35b7d0069e3244a6a89b9baec6a61e702cc80b6e3f91f1a5689926e40927 |
| supervised_retrieval.py | 2940338c5378de03303befb74e3834fbad631c0eb18f4ecb55d2cc39a471f879 |
| E041 main.py | 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073 |
| E025 main.py | 00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9 |
| synthetic UNICEF | 8e7c659d277c5145c7a8a6d055ac59a7dd3c35699317741239b6b1969bce1488 |
| synthetic WB | 4592bed873410c5248edf1205e5cab41dd30494926e3b49f8da598e266758c8a |
| synthetic UNHCR | 5d00075706e0a7beafdc8a70acfe07cde1f489048741eb2f3ae1fababdb72774 |

S0는 NPZ/Parquet를 재검증하지 않았다. 해당 hash는 기존 기록을 승계한 값이다.
r6 운영 문서와 옛 S1 freeze의 차이는 운영 개정으로 별도 기록하며 과거 파일로
되돌리지 않는다. 예상 밖 과학 source/input 차이는 임의 복구·정당화하지 않는다.

## 재사용과 release 절차

1. 진입 gate/source/input/환경/현재 계약/limits와 SCORES 사전 arm을 동결한다.
   기존 출력 경로가 있으면 덮어쓰지 말고 실제 완료 상태를 확인한다.
2. S1 R3/H3 raw는 완료 기록을 재사용한다. R3와 E062 clean E0413의 전체 raw
   equality 및 source/snapshot 대응·frame/role/order/floor/version으로 E041
   비교를 연결한다. 점수 같음만으로 연결하지 않는다. 별도 R fit은 허용하지 않는다.
3. E062 clean E0253도 snapshot/input/환경/완료 receipt/hash/order가 일치하면 재사용.
   E025만의 기존 provenance가 부족하면 사전에 이유를 기록한 뒤 **fresh clean E025
   all3 최대1회**를 아래 새 예산으로 허용한다. 입력 차이나 R/H 재실행 구제용이 아니다.
4. 새 assembly의 namespace/dispatch/factory/원래 fallback·helper 보존을 최소 영향
   검사로 확인한다. 이미 성공한 S1 suite는 반복하지 않는다.
5. assembly H all3 1회. source H의189649 vectors exact parity, UNICEF17856/WB39520
   exact E041, UNHCR132273 출력 계약과 원래 변화, metric/activity/donor/replay
   불변을 확인한다.
6. root main.py·필요 requirements·notice를 담은 ZIP을 한 개 새로 만든다.
   stock ZIP checker와 snapshot/archive/extracted bytes equality를 확인한다.
7. 추출본 official score.py --phase 1을 세 기관 각1회, **합계900초** 안에 수행한다.
   이 출력으로 source/assembly/extracted raw parity도 확인한다. 별도 parity용 fit 없음.
8. 동일 truth/order/floor.001로 clean 비교: **E025와 absolute skill 차이 <=.002/기관**,
   **candidate−E041 >=−.002/기관**. E041 signed 차이도 전부 기록한다.
   Release 기준이지 효능 증거가 아니다. 새 subgroup/seed/threshold 진단은 하지 않는다.

모든 query PREDICT는 model entry 전에 mask한다. DEV truth는 fresh 후보 출력이
동결된 뒤 평가 worker만 읽는다. Model worker에 DEV 답변을 전달하지 않는다.
기존 TRAIN 내부 선택/refit/replay 재사용과 편향은 그대로 기록하며 새 audit이라 하지 않는다.

## 신규 예산과 시도 상한

사용자가 이 배치를 승인할 때만 적용되는 **새 예산**이다.

- Gross180분: 첫 entry부터 읽기/수리/기록 포함. 마지막15분은 종료·기록용.
  끝낼 시간이 부족한 stage는 시작하지 않는다.
- 계산3600초 합계: identity/prep/검사/checker/평가/실패/수리 프로세스 포함.
  Nested fit 시간은 외부 wall에 두 번 더하지 않는다. 역할 전환으로 초기화하지 않는다.
- 각 all3 공유900초: import/load/삼기관 호출/출력/driver overhead 포함.
- Scientific all3 시작 최대4회: assembly H1, official extracted H1,
  조건부 E0251, **무효 release arm 기술수리 재시도1**.
  Official 삼기관 process는 한 묶음으로 사전 등록하며 중간 실패도 그 시도를 소비한다.
  성공 arm과 유효한 불리한 결과는 재실행하지 않는다.
- 정상 baseline 재사용6pipeline/18neural/16metric. Fresh E025 포함9/27/16.
  H 무효 arm 재시도까지 최대12/36/24. Checker no-fit predict는 별도 계수.
- 새 assembly 영향 검사/수리 합300초·최대3cycle, 전체3600초에도 포함.
  일반 오류는 같은 세션에서 원인 확인·최소 수정·영향 검사 후 계속한다.
- CPU numerical threads2/가능한 affinity2, GPU0, heavy1. 소유 tree RSS/private
  각각8GiB 감시. 초과 시 소유 tree만 종료. Sample gap/peak 의미·종료 확인 기록.
- 새 지출/credit USD0. 기존 로컬 환경만. 설치·Modal/H100·새 유료 자원·모델 취득 없음.

E063 S2 약1215초/E062 S2 약1257초/E064 H 약377초를 근거로 정한 상한이다.
완료 보장이나 전량 소비 목표가 아니다. S1의877.3776708초와 과거 작업 비용은
역사 열에 별도로 두고 남은 옛 예산을 재사용하지 않는다.

## 판독과 종료

모든 gate PASS: RELEASE_QUALIFIED_FOR_USER_REVIEW, E064 parked 유지, S0 반환.
기술FAIL/비교 기준FAIL/경계 위반/한도 소진은 구체적 closeout. 새 가설·data/정책/
기준/예산 변경은 S0로 돌린다. 원모델 의미 변경은 ordinary assembly 수리가 아니다.
실패 산출물 보존, 새 attempt/freeze 추가, 사용 시간/횟수 증가 없이 수리한다.

SCORES의 comparator: E041 ID933094, Finished Development/phase29772,
사용자 API .6433333333/.52/.49/.92, submissions/hosted-scores/2026-09-27.json.
Status/phase/ID/filename/keys/precision/출처가 비교 가능해야 한다. Scorer 버전
미확인을 숨기지 않는다. UNHCR+Grand 상승/control 공개값 동일=favorable noisy
whole-policy evidence, 둘 다 tie=UNRESOLVED, 어느 쪽 하락=adverse.
역방향/control 변화는 mixed·귀속 미해결도 기록. 실패technical, 필수값/출처 모순HOLD.
정확한 효과0·hidden head·예측/활성 동일은 추정하지 않는다. 자동 승격·재제출 없음.
사용자가 나중에 같은 채팅에 결과를 주면 사후 기록만 수행하며 새 fit/ZIP을 만들지 않는다.

## 쓰기 범위와 산출물

신규 docs/analysis/E064-outputs/s2/ 및 tmp/e064-b01-release/에 assembly/harness/
영향 검사·attempt·freeze·증거를 쓴다. 원래 S1 outputs는 읽기 전용.
submissions/YYYY-MM-DD-E064/ 및 동일명 ZIP은 **실제 제작일**로 한 세트만 만든다.
검증일/업로드일과 구분한다.
Status/log는 소유 기간에 추가한다. submissions/SCORES.md는 준비 기록만 명시해
추가할 수 있다. Source/실험원문/이전snapshot/tree/옛manifest·registration은 수정하지 않는다.

필수 산출물: batch-entry, source-input-env freeze, reuse 표, SCORES 사전 arm,
assembly/official parity·E025/E041 비교·checker 증거, notice/의존성 공개,
ZIP bytes/SHA256/제작시각, 자원·전체 시도 장부, 수리 이력, exposure/preservation,
closeout/S0 handoff, jobs/쓰기 해제. Upload bytes/ID/slot/account는 미확인 상태 유지.
자동 upload/commit/push/S3/서브에이전트 없음.

모든 STOP/HOLD,17999명/12339SSUID·집계·A022 역할, E059 소비oracle1918/1124·
selection2007/1130 및 보호audit2074/1177·calibration1866 유지.
E041 incumbent/E025 fallback, parked 정책, A_half 비승격/A018 사용자 미확정 유지.
