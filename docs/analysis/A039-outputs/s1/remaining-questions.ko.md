# A039 — 해결된 구조 질문과 남은 의미 질문

실제 CSV 6개의 첫 헤더는 각각 동봉 labels의 VAR 이름·순서와 완전히 일치한다.
총1491개 파일별 열 출현이며 표본 수나 독립 문항 수가 아니다. DDI1519개 정의와의
차이는 실제 export에도 있다. 헤더 확인을 다시 의뢰할 필요는 없다.

해결된 사실:

- ID_main/Form은 6개 모두, ID_ind는 member에 있다. 기존 계층 index는 없다.
- FamilyRegistered는 family, NotRegIDFamilyType은 case에 있다.
- IndAge와 WGQSeeing은 원래 chapter가 다르지만 둘 다 member에 있다.
- breakoff_1~5에 해당하는 열이 있고, 문서는 중도중단/계속 의미를 설명한다.
- WGQDepression 문서에는 Refused/DontKnow가 명시된다. 모든 결측이 같은 상태라는
  주장도, 별도 플래그가 없으면 어떤 정보도 없다는 주장도 성립하지 않는다.

제공기관 명세나 아직 제공되지 않은 export 문서로 해결할 최소 질문:

1. **v2.1 연결 규칙:** ID_main/ID_ind는 어떤 단위의 어떤 변환된 식별자인가?
   Form 내/간 범위와 기존 household/sharing/family/case/individual index의 대응은?
   한 household의 여러 family/case/sharing group과 member를 구분·연결하는
   배포 열 또는 공식 crosswalk는 무엇인가? 같은 가구가 두 form에 걸칠 수 있는가?
   개인정보·실제 ID 값이나 원래 등록번호는 요청하지 않는다.
2. **배포 결측·편집 명세:** breakoff 열, 일반 응답 코드와 빈칸이 구조적 미질문,
   중도중단, refusal/DK, 일반 결측, imputation/edit를 어떻게 구분하는가?
   DDI의 `Missing value`는 CSV의 어떤 표현을 뜻하며, 이유별 구분이 보존됐는가?
   구분할 수 없다면 그 범위를 명시해 달라. 빈칸을 NA_GATED로 임의 치환하지 않는다.
3. **빈 양식과 v2.1 변환:** IndAge 계산 입력(IndAge_yn/ind_age/IndDOB),
   FileNumberFromSample 및 long-form 반복 계산 index가 export에 없는 상황에서
   배포된 나이·asked 상태를 해석할 공식 변환/익명화 설명이 있는가?
   RestaurantInKindExternalOrders 제외도 알려진 export 차이인가?
   대체 정보가 없다고 단정하거나 임의 열을 대입하지 않는다.

별도 미래 용도의 조건: 사용자 보고상 접근 승인은 완료됐고 다운로드·압축 해제만
했다. A032 공통 약관 사본을 다시 요구하지 않는다. 승인 신청 목적과 로컬 proxy,
학습, hosted 제출, 파생물 공개의 적용 조건은 각각 필요해질 때 확인한다.
이번 로컬 헤더 확인을 위해 재신청·법적 판단을 만들지 않는다.

S0는 위 질문이 향후 결정에 필요한지 검토하고, 기존 문서의 새 근거 또는 필요 시
사용자가 선택하는 문의로 확보한다. 기존 A038 문의문을 수정·발송하지 않았다.
새 명세가 오면 문서 검토부터 재개하며 키 값 검사·응답 분석·역할 배치·fit은
각각 별도 범위가 필요하다. 동일 헤더 감사·공개 검색·빈 HOLD 기록 반복은 하지 않는다.
