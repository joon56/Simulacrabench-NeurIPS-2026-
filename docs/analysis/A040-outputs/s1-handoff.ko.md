# 다음 세션 제목

HSCC · S1 · A040 TabICLv2 독립 확률 예측기의 실행 계약

# 붙여 넣을 프롬프트

```text
SimulacraBench / HSCC S1 — A040 정보 조사를 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1
이 채팅은 별도 S1이며 아래 문서·소스 조사만 실행한다. 모델 실행 지시가 아니다.

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md를
순서대로 읽고 실제 역할·개정·허용 범위를 보고한다. HEAD/dirty files/active jobs
확인, 기존 변경 보존. A040 s0-entry/s0-verification의 허용 문서 해시 확인.
미커밋 차이를 과거 manifest에 맞춰 되돌리지 않는다. 에이전트 자동 실행 금지.

필수 입력:
- docs/analysis/A040-outputs/{s0-decision,source-register}.md,
  s0-entry.json, s0-verification.json
- docs/experiments/E041-supervised-retrieval.md
- docs/experiments/E048-tabpfn-gate-parents.md
- docs/experiments/E049-adaptive-tabpfn-parents.md
- docs/experiments/E051-direct-content-tree.md
- submissions/SCORES.md 및 E061 사후 scorecard
필요 시 A037/A039의 HOLD·노출 문서를 참고하되 VAF 연구를 재개하지 않는다.

판단 질문:
고정 TabICLv2가 GIVEN만으로 UNHCR 완전 응답 분포(NA_GATED 포함)를 예측하는
독립 전문가로 쓰일 수 있는가? API/확률 의미/오프라인 배포/전체 비용과
효과 판독을 연결한 실행 계약을 만들 수 있는가?
현재 후보 범위는 전체213 PREDICT의 직접 분포이며 UNICEF/WB는 E041 유지다.
실행비용이 안 맞는다고 부모4개나 참조512명으로 자동 축소하지 않는다.
그 경우 한계/새 설계 필요를 보고한다. 이번 정보 조사에서 모델을 만들지 않는다.

기존 작업과 차이/반대 근거:
E049는 TabPFN-v2·부모4개·참조512명·응답자별 선택기였다.
이번 검토는 다른 고정 사전학습 prior와 완전 응답 head 범위, 실제 이용 가능한
context 및 비용을 다룬다. E041도 이미 비선형 예측을 하므로 '상호작용 학습'만으로
새 가설이라 하지 않는다. E051은 이미 직접 완전분포 트리를 시험했고 작은 oracle로
STOP했다. E048 PFN 단독 손실/E049 oracle-to-policy 격차도 반드시 비교한다.
단순 예측 불일치는 유용한 보완성이 아니다. 최종 floor 적용 log score가 기준이다.
E025 .79/.10을 E041 손실 분해로 재사용하지 않는다. .65 또는 개선량을 예측하지 않는다.

주력, 한도:
정보 조사 한 번, 총60분·공식 핵심 문서/소스 최대12개. 미확인 링크도 횟수에
기록한다. 처음부터 논문 전체 역사/모델 순위를 조사하지 않는다.
최초 단서는 공식 논문 https://proceedings.mlr.press/v306/qu26a.html,
https://github.com/soda-inria/tabicl, https://huggingface.co/jingang/TabICL.
선택된 모델 단서는 tabicl-classifier-v2-20260212.ckpt. 버전/코드 commit/weight
revision을 문서로 식별한다. clone·install·weight 다운로드·역직렬화는 금지한다.
기존 로컬 생산 소스/공개 schema와 공식 웹 문서·소스만 읽는다. source 파일은
실행/import하지 않는다. 필요 문서/작은 텍스트 소스만 전용 산출물에 저장 가능.

확인할 내용:
1. 정확한 코드/weight 버전과 각각의 이용·배포 조건, 의존성 및 HSCC 환경 호환성.
   공식 현재 제출 계약을 필요한 범위에서 확인. 계정/로그인/슬롯 조회는 하지 않는다.
2. predict_proba의 classes 순서, 미관측/단일 클래스, 범주형 GIVEN/결측 처리,
   >10클래스 지원, NA_GATED를 보통 목표 클래스에 포함시키는 방법.
   모든 schema 옵션에 정렬된 유효 확률을 만드는 조건과 필요한 후속 검증을 적는다.
3. fit 호출의 실제 계산 의미, import-time weight load와 context별 계산의 분리,
   자동 네트워크 호출 차단, 클래스/feature permutation 및 내부 앙상블 비용.
   캐시가 X만 공유하는지 y/target에 의존하는지 소스로 확인한다.
4. 전체213개 head의 공개 class 수/fit-visible n/query n과 head별 필요 호출 수,
   shadow validation·선택·최종 refit/context 재구축까지 accounting 표 작성.
   UNHCR만이 아니라 E041 controls+import/load+all3의 합계900s DEV,
   3600s TEST/16GB host RAM/1H100이라는 기존 기록을 현 공식 문서와 대조한다.
   host RAM/VRAM/cache/offload를 구분. 단일 target 홍보 속도를 HSCC 보장이나
   무근거 선형 외삽으로 쓰지 않는다. 실제 런타임 미측정은 그대로 명시한다.
5. 가장 작은 후속 기술 검증 계약 한 개: 가짜 자료/공개 schema만으로 offline,
   클래스 정렬, fitting-only, 최종 출력 및 전체 비용을 확인하는 범위·횟수·예산.
   이번에 구현/생성/실행하지 않는다. 모델 호출을 'smoke'로 이름 바꿔 실행 금지.
6. 기술 검증 뒤 실제 유용성을 판독할 수 있는 경로를 구체화한다.
   (a) 새 전문가 출력이 없으므로 현재 수치 oracle은 없다. 미래 oracle이 가능하면
   고정 mixture family의 best-constant 범위와 필요한 역할/출력을 명시한다.
   per-row hindsight oracle을 고정 혼합의 근거로 쓰지 않는다.
   (b) 기존 관측 자료는 소비 이력을 승계하며 새 seed가 새 평가 표본은 아니다.
   새 자료·미열람 audit을 임의로 가정하지 않는다.
   (c) VAF 없이 가능한 bounded exploratory DEV 경로라면 실제 hosted visible
   TRAIN 내부에서 숨길 fitting/selection/evaluation 역할, 최종 분포 비교,
   계산비용과 사전 판독 한계를 설계 수준으로 적는다. 숨겨진 DEV/TEST 정답은
   접근 불가. 후보 전체의 hosted 결과는 기제 단독 인과 효과가 아니다.
   (d) 합성자료 PASS가 ERPIS 효과가 아니며, 효과를 판독할 경로가 없다면
   단순 API 호환만으로 CONTRACT_READY를 선언하지 않는다.
7. 후속 실증에서 고정해야 할 comparator/source, 전문가 범위·context·혼합 정책,
   모델/전처리 fit 경계, 확률 floor, 비용, favorable/adverse/unresolved/failed
   판독 항목을 명시한다. 지금 alpha/seed/head/threshold 탐색은 하지 않는다.
   복잡한 응답자별 selector를 새로 제안해 E049의 문제를 자동 반복하지 않는다.

결과와 종료:
- CONTRACT_READY: 문서/소스상 근거와 제한, 실행 가능한 최소 기술 검증 계약,
  이어지는 효과 판독 경로까지 있다. S0에 반환하며 자동 실행하지 않는다.
- NO_GO: 명확한 구현/확률/오프라인/비용 불일치 또는 독립 가설/판독 가치 부재.
  이유를 기록하고 종료. 과거 STOP을 해제하거나 즉석 다른 모델로 갈아타지 않는다.
- HOLD_SPECIFIC_INPUT: 결정에 필요한 사실 하나가 남으면 출처·확보 주체·재개 조건을
  특정하고 종료. 같은 조사 연장/새 HOLD 기록 반복 금지.
정당한 예비 작업은 차단 조건과 종료 기록 작성뿐이다. +.005 보편 문턱 적용 금지.

산출물 docs/analysis/A040-outputs/s1/:
entry.json, source-register.md, contract.md(이전 실험 대비표 포함),
cost-accounting.md, observation-plan.md, exposure-ledger.md,
closeout.md, s0-handoff.ko.md, verification.json.
필요한 status/log 갱신. S0 산출물·기존 연구/모델/제출 snapshot/tree/.gitignore는 보존.
후속 기술 작업은 계획만 적는다. S2 실행 프롬프트나 ZIP을 만들지 않는다.

경계:
VAF/UNCHR_data 전부, SIPP/Adult 원자료·키·응답, Parquet/NPZ/pickle/cache는
읽거나 재해시하지 않는다. 기존 집계와 공개 schema/문서만 허용한다.
17999명/12339SSUID·집계 노출, A022 원래 역할, E059 소비 oracle1918/1124·
selection2007/1130, 보호 audit2074/1177·calibration1866을 승계한다.
실제 fit/optimizer/predict/score·fixture/테스트 실행·새 E기록·데이터 취득·
패키지/weight 설치·연락·업로드·commit/push·S2/S3/TEST 선택은 금지한다.
E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
A_half 비승격·A018 사용자 미확정·S3 중단을 유지한다.
```
