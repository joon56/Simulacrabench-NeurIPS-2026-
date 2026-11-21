# S1 — A041 World Bank 순서형 head 적용 계약 정보 조사

사용자가 이 문서를 담당 S1에 작업 지시로 전달할 때 시작한다.
작성된 파일 자체는 실행 허가가 아니다. 이번 작업은 정보 조사/설계이며 구현·학습은 아니다.

작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md,
docs/analysis/A041-wb-ordinal-head-review.md, A041-outputs/inputs.json을 읽는다.
실제 역할·개정·읽기·허용 범위를 보고한다. 기준 HEAD:
a43f4379ec78dbc2de260463eef67bb1d567d7e1.
현재 HEAD·dirty·관련 jobs를 확인하고 충돌하는 writer가 있으면 shared 문서를 덮어쓰지 않는다.
inputs의 허용 문서/source/schema 해시를 비교하고 차이를 보고한다. 과거 해시에 맞춰 되돌리지 않는다.

목적:
WB 16개 ungated 구간형 head에 학습 시 순서 구조를 사용하는 단일 후보가
E041과 비교할 만한 독립적 탐색인지 결정하고, 긍정이면 실행 가능한 후속 실험 설계를 만든다.
주력은 확률/학습/판독/전체 비용 계약 한 개다. 예비는 정확한 기각 사유/재개 입력 closeout.

이미 확인된 내용은 반복 과제로 만들지 않는다:
- inputs에 고정한16개 모두 six ordered bins + Not answered, gate=null.
- E011 숫자 파싱 kernel의 비대상이며 사후 평활화와 학습 시 제약은 다르다.
- E041 일반 softmax 및 shared trunk가 존재. 표현 공유 자체는 새 기전이 아니다.
- E011의 null 및 E017/E026/E029/E030/E061 과거 결과/STOP을 유지한다.

남은 질문과 작업:
1. CORAL/CORN 원 논문 또는 필요한 cumulative-link 원전까지 최대3개 primary source를 읽는다.
   현재 S0는 두 논문의 개요만 읽었다. probability recovery/학습 loss/제약과 한계를 확인한다.
   비교 후 한 개 parameterization만 추천하거나 기각한다. grid/여러 모델 실험 계획을 만들지 않는다.
2. 여섯 substantive 범주의 순서를 이용하되 Not answered를 낮은/높은 응답으로 취급하지 않는다.
   별도 범주 확률을 포함한 일곱 출력의 비음수/합1/순서/극단값/희소범주 계약을 수식으로 명시한다.
   구간 간 동일 거리·분포 단봉성·실제 missing 이유·원점수 복원을 가정하지 않는다.
   EXCLUDE/PREDICT 응답을 query feature로 쓰지 않는다.
3. 정확한 HSCC 범주 log score와 학습 loss의 관계를 도출한다.
   ordinal MAE/threshold BCE 개선을 최종 log score 개선으로 대체하지 않는다.
   floor는 공식 최종 분포 기준으로 처리하고 중복 floor/임의 label smoothing을 추가하지 않는다.
   shared trunk/pooled denominator/early stopping/config 선택/refit에 미치는 영향을 설명한다.
4. baseline E041, 한 후보, 목표 WB/고정 UNICEF·UNHCR 통제의 귀속 설계를 작성한다.
   shared trunk 영향으로 WB 나머지60개 출력까지 바뀔 수 있음을 명시한다.
   기존 width/seed/holdout/배합/선택 기준을 편의상 바꾸지 않는다. 필수 변경은 사전에 드러낸다.
   기존 E061 기술비용 기록은 참고만 하며 새 후보 시간 보장으로 쓰지 않는다.
5. 실제 관측 채널과 사전 판독표를 작성한다.
   현재 fresh oracle 없음. 이미 노출된 synthetic 자료는 공학/회귀 채널이며 실제 WB 효과 상한 아님.
   ordinal 가정이 주입된 예제의 이득을 실증으로 부르지 않는다.
   장래 visible TRAIN fitting/selection/refit 역할과 전체 PREDICT 마스킹을 정의하되 지금 접근하지 않는다.
   유용한 추가 oracle이 없는 이유를 쓰고 +.005를 보편 조건으로 강제하지 않는다.
6. 실제 코드 경로에서 전체 pipeline/neural fit/선택/refit/비교 횟수와 비용 항목을 센다.
   기존 CPU2/단일 로컬 worker로 기술 검증을 설계할 수 있는지 판단한다.
   기존 Torch/NumPy로 불가능하면 그 이유를 적고 새 환경/클라우드 구축으로 확대하지 않는다.
   미래 all3 shared900s, 메모리, E025 absolute.002/기관 및 E041 비교,
   source/assembly parity/ZIP checker/official all3는 S2 잔여 조건으로 분리한다.

판정:
- DESIGN_READY_FOR_S0_REVIEW: 구체적 기전·확률 계약·기존 실험과 차이·채널 한계·
  한 후보의 전체 비용과 판독을 명시할 수 있음. 구현 권한·효과·S2 자격 아님.
- NOT_READY_WITH_SPECIFIC_REASON: 중복/확률 정합성/해석/비용/관측 경계 문제를 특정.
  조건을 낮추거나 같은 계약조사를 자동 재개하지 않는다.
- 이 정보 조사에서 E번호/모델 코드/실험 실행문을 활성화하지 않는다.
  후속 WB 구현은 사용자의 prospective 기관 변경 지시와 별도 S1 등록이 필요하다.

상한:
세션45분, 마지막10분 기록. 새 primary 문서 최대3개. 설치/모델/계산 실험0.
일반 문서/경로 오류는 같은 세션에서 고치되 한도를 초기화하지 않는다.
같은 공개 문항 inventory/성공 fixture를 다시 만드는 작업은 제외한다.
추가 조사가 필요하면 무한 HOLD 대신 결정에 필요한 정확한 입력과 현재 범위의 기각 이유를 쓴다.

허용:
고정 공개 schema·production source·기존 문서/허용 hash 읽기, 논문/저자 원전 웹 열람,
문서 수식/학습·비용 설계, 새 A041-outputs/s1/ 산출물과 status/log 추가.
금지:
응답/키/Parquet/NPZ/cache/checkpoint/VAF 열람·재해시, import/fit/predict/score,
가짜자료/fixture/테스트 실행, 설치/weights 취득/원격 접속·빌드·Modal,
기존 모델/연구/snapshot/tree 변경, E기록/ZIP/업로드/commit/push/S2/S3,
다른 세션·서브에이전트 자동 실행.

산출물은 A041-outputs/s1/의 contract.md(후속 실험 설계 포함),
source-register.md, cost-accounting.md, exposure-ledger.md, verification.json,
closeout.md와 s0-handoff.ko.md. 기존 S0 inputs/문서를 보존한다.
검토한 사실·추론·미측정을 구분하고 시작/종료·소스 해시·기존 변경 보존을 기록한다.

E041 incumbent/E025 fallback, E057/E060/E061 parked,
E058 STOP/E059 STOP_SELECTION 및 A039/A040/모든 STOP/HOLD 유지.
17999/12339·A022 역할/집계 노출, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 미확정/S3 중단/S2 없음.

