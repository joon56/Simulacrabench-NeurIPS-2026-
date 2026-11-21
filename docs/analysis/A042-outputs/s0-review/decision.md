# A042 S0 — round 조건부 metric 계약 검토

2026-10-09 KST. **RECOMMEND_BOUNDED_S1_TECHNICAL_IMPLEMENTATION**.
[완성 S1 프롬프트](s1-implementation-handoff.ko.md). 이 문서는 권고와 범위 정의이며
이번 S0의 실행 허가가 아니다. 사용자가 별도 S1에 전달해 실행을 지시할 때만 적용한다.

## 판단

S1의 CONTRACT_READY_FOR_S0_REVIEW를 수용한다. 이제 같은 정보 조사를 반복하기보다
고정 후보 하나를 구현해 정확한 연결·자연 활성·전체 출력 변화·전체 비용을 확인할 가치가 있다.
E063을 이 후속 모델 과제에 예약한다. docs/src/scripts/tests의 텍스트 검색 및 지정 경로에
충돌 없음을 확인했다. 이번에는 E 실험 파일이나 모델 코드를 만들지 않았다.

근거는 세 가지다. 첫째, query wave에 따른 GIVEN 일치 가중치는 고정 공통 가중치나
일치×일치 항과 다른 순위를 표현할 수 있다. 둘째, 원래 K32·base·selection·lambda
알고리즘을 유지하는 단일 계약과 정확한 R fallback이 명시됐다. 셋째, 새 자료·환경·원격
자원 없이 기존 CPU 경로에서 검증할 수 있다. 실제 처리시간은 여전히 미측정이다.

반대 근거도 유지한다. E041은 이미 wave를 사용한다. K32에 유용한 대안이 없거나
round별 표본이 부족할 수 있다. 18→35좌표가 이득보다 분산을 늘릴 수 있다.
E045/E047의 oracle와 learned gain 간 차이, E058/E059 STOP, E060/E062 공개 동점은
복잡도 증가를 낙관하지 않을 이유다. 이 계약의 유용성·효과·우승확률을 입증하지 않는다.
A040 재개나 의미 미확정 VAF 분석보다 현재 범위·비용·판독이 구체적이라는 상대적 판단이다.

## 계약 대조와 수용 한계

- 실제 supervised_retrieval.py의 objective, F-only optimizer slice, first10-of-K32
  proxy, .003/2SE selector, seed4101, replay/lambda 흐름과 대조했다. 공개 schema의
  wave1/2·round별 기록 차이 및 candidate_indices의 순서 계약도 확인했다.
- H의 고정 penalty와 gradient는 수식상 일관된다. w1=w2에서 원래 loss로 줄어들며
  두 weight gradient를 합치면 공통 weight gradient가 된다. 수치 검사는 아직 없다.
  이 등식은 H optimizer의 실행 결과가 bit-exact R이라는 뜻이 아니다.
- C=R은 원래 생산 E041 함수를 직접 쓰는 비교다. 새로운 common fit 또는 H/C 선택기를
  넣지 않는다. 두 독립 비교·반복 실증으로 세지 않는다. snapshot과 조립 parity는 이후
  release 과제이며 소스 해시 일치만으로 이미 검증됐다고 하지 않는다.
- F/S 각각 round당30은 사전에 정한 공학 eligibility로만 수용한다. support 부족 때
  전체 기관을 원래 경로로 보내며 optimizer 두 번/전체 base 두 번을 호출하지 않는다.
  원래 visible<500 등의 fallback은 그대로다. 30을 정밀도·독립성 근거로 쓰지 않는다.
- S를 8개 section에 재사용하고 base/replay가 in-sample이라는 한계는 해결되지 않는다.
  H의 activity·replay 자격·lambda·재귀 출력 변화까지 포함한 전체 절차 비교다.
  A021의 D-P/D-R 연구나 독립 audit으로 승격하지 않는다.

41개 허용 문서/소스/공개 schema 해시는 S1 verification 기록과 일치했다.
S1의 tool chunk를 포함한 읽기 증거는 session-reported이며, 이번 S0의 실제 읽기와
구별해 verification에 남긴다. HEAD a43f4379, dirty104, 조회한 python/pythonw/uv jobs0.
이 관측은 모든 타 세션·원격 작업의 부재 증명이 아니다.

## 다음 한 작업과 판독

주력: **한 고정 round metric의 구현과 노출된 합성 자료에서의 기술 검증**.
현재 적합한 독립 실제 자료/응답 권한이 없어 유효한 target numeric oracle은 없다.
Adult/SIPP의 과거 oracle, A022 잔여 역할, 보호 audit으로 대체하지 않는다.
새 공학 fixture는 순위·gradient·정보 흐름을 검증할 뿐 자연적 보완성의 증거가 아니다.

다음 S1에 제안하는 한도는 gross120분/마지막10분 기록, 전체 computational child1800초,
각 fresh all3 process900초, CPU2/GPU0/heavy1, owned RSS/private 각각8GiB다.
정상 R/H 두 process는6pipeline/18neural/16metric. 작은 영향 검사·평가·실패도
같은1800초에 포함한다. 사전에 ordinary implementation repair용 full-process
재시작 최대1회를 포함해 상한9/27/24로 제한한다. 성공한 정상 비교를 더 돌리는
예산이 아니며 시간·정책·자료·판정 기준을 바꿀 수 없다. 비용 예상값이 아니다.

S1의1800초 제안을 유지하고, 누락된 gross·검사·수리 계수를 이번에 prospective하게
명시했다. 과거 한도·판정을 수정하거나 소진된 A040 실행량을 되살리는 변경이 아니다.

판독 조건은 응답을 열기 전에 등록한다:
- 기술·자원·controls·확률 계약 통과, 자연적으로 활성인 H section 존재,
  최종 UNHCR raw 변화 존재, 기관별 H-R skill>=-.002이면 LOCAL_TECHNICAL_PASS_FOR_S0.
  gain>0 또는 보편적+.005를 요구하지 않는다. 작은 손실도 그대로 보고한다.
- all-equal이면 STOP_NO_OP. support fallback 또는 H active0이면
  STOP_INACTIVE_ON_ENGINEERING. H active0인데 R와 달라지는 경우는 기존 R evidence를
  잃는 변화일 수 있어 의도한 조건부 reranking의 qualification으로 쓰지 않는다.
  이는 이번 S0가 추가한 미래 기술 판독 조건이며 원래 S1 문서를 소급 변경하지 않는다.
- 누수·control/parity/확률 결함은 기술 실패, 한도는 RESOURCE_LIMIT,
  H-R 하한 미달은 REGRESSION_HOLD. routine defect만 r5와 남은 예산 안에서 고친다.
- 어느 결과도 실제 UNHCR 이득·가설 전체 반증·S2/release/DEV 채택/TEST를 뜻하지 않는다.

정당한 예비 작업은 실패/비활성/한도 closeout과 정확한 다음 입력 기록뿐이다.
다른 모델·seed·threshold·round support를 찾아 자동 전환하지 않는다.

다음 S0는 실제 코드·자연 활성·전체 비교·비용을 보고 S2의 가치와 범위를 정한다.
S2의 clean E025 기관별-.002와 E041 비교, source/assembly parity, ZIP checker,
official all3/shared900초·메모리, SCORES 판독표는 아직 미완료다.

## 보존

E041 incumbent/E025 fallback; E057/E060/E061/E062 parked. E058 STOP,
E059 STOP_SELECTION, A023/A024 empirical HOLD, A039/A040 및 모든 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격, A018 사용자 미확정/S3 중단.
E062 공개 동점 UNRESOLVED 불변. 새 S2 후보 없음.

현재 S0는 허용 문서·정적 소스·해시 검토 및 이 폴더/status/log 작성만 수행한다.
응답·Parquet·NPZ·cache·ZIP 접근/재해시, 모델/검사 실행, 원격, commit/push 없음.
[읽기·보존 기록](verification.json). 원래 A042/S1 기록과 연구·snapshot·tree는 보존한다.

