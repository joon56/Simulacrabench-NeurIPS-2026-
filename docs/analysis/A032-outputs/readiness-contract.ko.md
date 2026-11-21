# A032 — 확보 문서로 만든 후속 구현·실증 진입 계약

현재 판정: **문서 입력 진전 / 실증 HOLD**. 이 문서는 실행 허가나 완료된
adapter가 아니다. 공개 메타데이터 산출물은 이미 제작했다. 원래 A023
후보·lambda·선택 규칙과 과거 STOP은 바꾸지 않는다.

## 이미 제작한 작업물

- `routing-metadata.json`: long/short별 설문 행·원문 chapter·직접 분기 참조,
  상위 group/repeat 조건, 계산식, required/disabled 상태, DDI 파일 대응.
- `questionnaire-cells.json`: 원본 XLSForm3개 sheet의 비어 있지 않은 cell과
  Excel 행 번호. 응답자의 행이 아니라 빈 설문 정의의 행이다.
- `extract_metadata.py`: 위 공개 문서만 읽는 재현 가능한 목록 추출기.
  식을 실행하지 않고 원문을 보존한다. 모델 코드와 연결하지 않았다.

## 후속 adapter가 지켜야 할 구체적 조건

1. 식별자는 `(release, form, file, variable)` 단위. 반복 문항은 repeat 경로까지
   보존한다. DDI 숫자 코드를 파일 간 공통 답으로 간주하지 않는다.
2. `Form + householdindex`는 문서상 연결 후보다. 개별 index만으로 join 금지.
   식별자 문자열 단순 연결 대신 충돌 없는 tuple 표현을 사용한다. 전체 가족/
   case/개인 반복과 실제 동일 household 연결은 하나의 평가 역할에 묶는다.
   실제 행·키·중복은 읽지 않았으므로 연결 검증 PASS를 주장하지 않는다.
3. 직접 relevant뿐 아니라 상위 relevant, repeat, disabled, 중도중단,
   계산식·날짜·폼 버전을 해석해야 asked 상태를 논할 수 있다. 원문 chapter를
   새 section으로 임의 치환하지 않는다. long/short chapter 차이도 보존한다.
4. `Refused`, `DontKnow`, `NotApplicable`, 구조적 미질문, 일반 결측, 편집값은
   별개다. 문서가 이유를 주지 않는 빈칸은 UNKNOWN으로 보존한다.
   UNKNOWN을 NA_GATED로 채워 모델 성능을 측정하는 설계는 기각한다.
5. 예: `FamilyRegistered`/Family와 `NotRegIDFamilyType`/Case는 실제 문서상
   교차 장 연결이다. `IndAge`/IndBioData와 `WGQSeeing`/HEALTH는 나이 계산
   의존이다. 둘을 대회의 미지 PREDICT 부모와 동일한 기제로 취급하지 않는다.
6. `MedicalAccess`의 Main과 Members는 코드·빈도·단위가 다르다. 이름만 같은
   열을 합치면 안 된다. `WGQDepression`의 Refused/DontKnow는 명시된 답이다.
7. 두 form에 공통 문항이 있어도 상위 breakoff 조건이 다르다. 공통 문항만
   선택해서 버전 차이가 사라졌다고 주장하지 않는다.

## 부족한 입력·담당·재개 조건

| 입력 | 확보 주체 | 충족 기준 |
|---|---|---|
| catalog1030 이용 승인/적용 계약 | 사용자·연구책임자, UNHCR 승인자 | 정확한 release, 승인 연구 목적·팀·처리 환경 확인. 계정 보유만으로 부족 |
| 대회/ML·파생물 사용 범위 | 해당 계약 또는 UNHCR 데이터 담당자 | 외부 proxy 평가, 모델 학습, hosted 대회 사용, 파생 weights/code 공개 및 검토·인용 의무 구분. 미허용이면 학습·배포 설계 제외 |
| export·결측·편집 대응 | UNHCR release 담당자 | never-asked/중도중단/refusal/DK/일반 결측/imputation을 구분할 코드·플래그 또는 구분 불가능하다는 명시. 배포 form 버전과 v2.1 변환 대응 |
| 실제 근사 gate 관측 가능성 | release 명세·담당자; 이후 별도 승인된 진단 | routing 불일치를 중도중단/편집/결측 오해와 구분할 수 있어야 함. 단순 DQA 실시·결측 수로 충족 불가 |
| 연결·독립 단위 | release 명세·담당자, 이후 허용된 키 검증 | Form 내/간 동일 가구·반복/중복 및 공개 index의 의미 확인. 타 조사와 재식별 연결은 요구하지 않음 |
| 역할·정밀도 | S0 설계 후 명시된 S1 | 실제 허용 표본을 학습/보정/선택/평가 역할로 사전 고정. 집계 노출 승계. 최종 평가 응답을 열어 분산·threshold를 맞추지 않음 |
| 구현·전체 비용 | 승인된 S1 기술 과제 | production adapter parity와 fitting-only 경계, 실제 base/neural/전체3종 실행시간·합산 메모리 확인. A023 stub PASS로 대체 불가 |

조건부 순서: 이용·관측 적합성 확인 후, 별도로 범위를 등록한 진단과 기술 구현.
그 결과가 기제·독립 역할을 지지할 때만 실증 연구 등록. 본 문서는 그 작업의
자동 시작 지시가 아니다. 계정/계약만 확보돼도 남은 코딩 조건을 건너뛰지 않는다.

## 평가 정밀도 설계 입력

기존 A024를 승계한다. P와 R/E041은 다르며 D-P는 목적함수 통제 비교,
D-R은 전체 절차 비교다. 선택 S에서 c_P/c_D를 고정한 뒤 독립 E에서 둘의
실제 배포 출력 차이를 paired 비교한다. 같은 선택이면 D-P=0이라는 논리와
실제 관측 결과를 구분한다. 두 개별 주장에는 사전97.5% 구간 두 개를 사용하는
보수적 동시95% 설계안을 유지하되, 실제 독립 군집·가중치에 맞는 구간 방법을
확정해야 한다. 아직 실행 가능한 실증 등록은 아니다.

공개5357 household 규모는 사용 가능한 E 군집 수가 아니다. paired 차이의
군집 분산·가중치·표본 배치 없이는 유효 표본수/검정력도 정해지지 않는다.
필요한 값은 두 비교 각각의 실용적 차이/허용 구간폭, 정당화된 분산 또는
보수적 시나리오, 실제 평가 군집 수·크기/층화다. 자료를 얻기 전 임의의
효과·분산을 측정값처럼 채우지 않는다. 기존 lambda minimum30/zero fallback
유지. 원래 STOP의 threshold를 낮춰 이 경로를 통과시키지 않는다.

## 다음 행동

사용자의 기존 이용 승인 여부를 확인하고, 없으면 첨부한 미발송 문의안을
검토한 권한 있는 주체가 공식 절차를 진행한다. 아직 연락·계정·신청·동의는
수행하지 않았다. 새 승인·명세 없이 같은 공개 검색이나 HOLD 기록을 반복하지
않는다. 후속 실제 데이터/모델 작업은 그때의 입력·범위·비용을 새로 고정한다.
