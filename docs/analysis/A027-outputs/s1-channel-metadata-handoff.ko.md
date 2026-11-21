# S1 — UNHCR VAF 관측 채널 문서 적합성 조사

이 프롬프트 작성은 실행 허가가 아니다. 사용자가 다음 S1에 전달해 시작할 때
아래 공개 문서 조사만 수행한다. 현재 S0에서는 실행하지 않는다.

```text
SimulacraBench / HSCC S1 정보 확보 세션을 시작한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: 1d223340d4e1fa3993b411dc5daafab9cb37d0cd
워크플로우: docs/workflow.md, 개정2026-09-27-r2 또는 그 이후 현재본.
현재 HEAD·dirty files·active jobs를 확인하고 기존 변경을 보존한다.
A027 verification의 허용된 문서/소스 해시로 미커밋 지침을 식별한다.
불일치는 변경 경위를 확인하고, 과거 해시로 현재 파일을 덮어쓰지 않는다.

CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md 순서로 읽고,
docs/analysis/A027-workflow-role-revision.md,
docs/analysis/A026-post-e060-strategy-review.md,
docs/analysis/A024-channel-precision-review.md,
docs/analysis/A008-winning-strategy-hypotheses.md,
docs/analysis/A023-candidate-boundary-contract.md를 참고한다.

역할: S1. 유형: 정보 확보. 모델 연구/패키징 아님.
목적: 기존 Jordan VAF 관측 채널 단서가 후속 연구 설계를 검토할 만큼 적합한지,
현재 공개된 공식 문서로 답한다. 긍정적 모델 효과나 완성된 power 계획은
문서 조사에 진입하기 위한 조건이 아니다.

주력 출처는 기존에 기록된 UNHCR 공식 catalog1030:
https://microdata.unhcr.org/index.php/catalog/1030/study-description
그 자료의 공식 questionnaire/codebook/방법론·이용 조건 문서만 추적한다.
과거403을 현재 접근 불가로 단정하지 않는다. 현재 접근 실패 시 해당 자료의
공식 공개 문서 위치를 검색할 수 있으나 인증/접근 제한을 우회하지 않는다.
범위는 이 자료/명시된 release에 한정하며, 다른 데이터셋으로 무한 확장하지 않는다.

확인할 것:
1. 자료의 정확한 제목·버전·연도·대상 모집단과 공개 문서 출처/확인일.
2. 접근/이용 조건과 문서상 가능한 이용 범위. 신청·계정·추가 승인 필요 여부.
3. 서로 다른 문항 section 간 부모-자식 routing을 보여주는 구체적 문항 번호.
   서로 다른 조사 wave나 나라라는 이유만으로 cross-section 문항 구조라 하지 않는다.
4. never-asked sentinel, refusal/DK, 결측·imputation·routing error의 코딩 구분.
   문서에 실제 routing 불일치 근거가 있는지, 없으면 미확정으로 명시한다.
5. 개인/가구/반복조사의 연결 단위·표본설계·공개된 규모 및 노출 이력의 확인 범위.
   새 역할 배정이나 counts만으로 평가 정밀도를 주장하지 않는다.

기존 A024/A026과의 차이:
기존 로컬 기록 재요약이 아니라 새로운 현재 공식 메타데이터를 확보한다.
응답 분석이 없으므로 실제 gate 오차·모델 차이 분산·효과는 측정하지 않는다.

허용:
공개 공식 페이지/문서 검색·열람, 필요한 공식 questionnaire/codebook PDF 등
응답 없는 문서의 저장, 출처/인용/근거표 작성, 허용 문서 해시 확인.
새 A번호는 충돌 확인 후 등록한다. docs/analysis의 새 A기록/출력과
docs/status.md·docs/log.md만 작성한다. 생산 소스와 기존 연구 기록은 보존한다.

한도:
시작부터60분 이내, 자료1개, 핵심 문서 최대12개. fit/GPU/유료 사용0.
핵심 조건이 확인되거나 명확히 부적합하면 일찍 종료한다.
정당한 예비 작업은 접근/메타데이터 누락 조건 closeout뿐이다.

금지:
응답 microdata/Parquet/키/캐시 다운로드·열람·재해시·역직렬화,
계정 생성·접근 신청·이메일/메시지 발송·인증 우회,
fit/optimizer/predict/score·새 simulation·fixture 재실행,
기존 역할 재배정·인위적 section/gate 구성·새 E번호/모델,
ZIP·업로드·tree 수정·commit/push·S2/S3 실행·TEST 선택.

종료 판정과 다음 행동:
- 문서상 적합성 근거가 충분: “후속 설계 검토 가능”으로 S0에 전달한다.
  실제 응답 접근·독립 역할·정밀도·adapter·비용은 별도 미충족 조건으로 남긴다.
  empirical HOLD를 해제하거나 모델 작업을 시작하지 않는다.
- 구조/코딩/이용 조건이 질문과 부적합: 그 자료의 경로를 종료하고 근거를 기록한다.
  전체 UNHCR 연구 불가능으로 확대하지 않는다.
- 접근 실패/문서 누락/한도 도달: 미확정 조건·시도한 공식 출처·재개 입력을 명시한다.
  같은 문서를 재검색할 자동 후속 세션을 만들지 않는다.

산출물:
출처·확인일·사실/미확정·적합성 근거표, 접근 및 저장 내역,
위 세 판정 중 하나와 결과별 후속 행동, S0 인계문, status/log 갱신.
긍정적 연구 결과나 제출 후보가 없어도 이 정보 과제는 완료할 수 있다.

E041 incumbent/E025 fallback/E057·E060 parked, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD 및 모든 기존 STOP을 보존한다. A_half 승격 없음.
A018 TEST 선택 사용자 미확정, S3 중단 유지. 누적17999명/12339SSUID 노출,
A022 원래 역할과 E059 소비 oracle/selection·보호 audit/calibration을 승계한다.
```
