# 다음 세션 제목

HSCC · S1 · A039 VAF 실제 CSV 헤더와 문서 대응 확인

# 새 S1 세션에 붙여 넣을 프롬프트

```text
SimulacraBench / HSCC S1 — A039 제한적 export metadata 확인을 실행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

이 채팅은 별도 S1이다. 아래 문서와 CSV 첫 헤더 행만 확인한다.
응답/키 값 분석, 학습, 모델 구현, 제출물 제작은 지시하지 않는다.

시작:
AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신 3개 →
docs/workflow.md 순서로 읽고 역할·작업 유형·개정·허용/금지를 보고한다.
HEAD·dirty files·active jobs 확인. 원래 미커밋 변경을 보존한다.
새 세션·서브에이전트는 만들지 않는다.

필수 입력:
- docs/analysis/A039-outputs/s0-plan.md, s0-entry.json, s0-verification.json
- docs/analysis/A038-vaf-local-document-intake.md
- docs/analysis/A038-outputs/next-actions.ko.md, document-comparison.json, inventory.json
- docs/analysis/A032-outputs/readiness-contract.ko.md, researcher-guide.txt,
  routing-metadata.json, source-register.md, terms-of-use.html
필요한 공개 문서 원문과 VAR/LABEL 설명표는 아래 범위에서만 보충한다.

소스 식별:
HEAD만으로 미커밋 문서를 식별하지 않는다. S0 verification의 현재 문서
해시와 entry의 수정 전 해시를 구분한다. 허용 문서만 비교하고, status/log
추가 등 차이가 있으면 경위를 기록한다. 과거 manifest에 맞춰 되돌리지 않는다.
manifest에 경로가 있다는 이유로 응답 파일 전체를 해시하지 않는다.

목적과 기존 작업과의 차이:
A038은 공개 DDI1519개 변수와 동봉 labels1491개 행을 비교했다.
DDI에는 householdindex 등, labels에는 ID_main/ID_ind가 있었지만 실제
CSV 헤더는 아직 읽지 않았다. 이번에는 실제 배포 열 이름을 처음 확인해
설명표의 누락인지, 실제 export 명칭 차이인지, 다른 불일치인지 구분한다.
키 의미·연결 cardinality·독립 가구·실제 gate 오류는 헤더로 증명할 수 없다.
문서에 없는 답을 실제 파일에도 없다고 미리 단정하지 않는다.

허용 입력:
1. 기존 A032/A038 문서, 루트 공개 XML, KOBO 빈 양식, guide와 reports.
   기존 추출본 우선. 원문은 특정 누락을 확인할 때만 읽고 전체 추출기를 재실행하지 않는다.
2. 아래 폴더의 *_labels_*.csv 6개: VAR/LABEL 문서 전체를 읽을 수 있다.
   응답 행이 아니다. 공개 다운로드 여부와 문서 내용 유형을 혼동하지 않는다.
3. 아래에 정확히 열거한 실제 CSV 6개의 첫 헤더 행만:
   폴더 UNCHR_data/microdata/UNHCR_JOR_2023_VAF_HOST_data_v2_1/
   - UNHCR_JOR_2023_VAF_HOST_data_main_v2.1.csv
   - UNHCR_JOR_2023_VAF_HOST_data_case_v2.1.csv
   - UNHCR_JOR_2023_VAF_HOST_data_family_v2.1.csv
   - UNHCR_JOR_2023_VAF_HOST_data_member_v2.1.csv
   - UNHCR_JOR_2023_VAF_HOST_data_sharing_group_long_v2.1.csv
   - UNHCR_JOR_2023_VAF_HOST_data_sharing_group_short_v2.1.csv

읽기 경계:
- 로컬 경로를 정확히 고정하고, 위 6개 이외 파일을 glob으로 확대하지 않는다.
- 각 CSV를 첫 물리적 줄의 LF까지만 읽는다. UTF-8 BOM/CRLF는 처리 가능.
  최대128KiB/파일, 여섯 파일 합계768KiB. 헤더에 인용된 줄바꿈이 있거나
  UTF-8 해석/CSV 문법/줄 경계가 불명확하면 추가 행을 읽지 말고 중단한다.
- 응답 행으로 read-ahead하지 않는 방식을 쓴다. 예: 표준 라이브러리의
  unbuffered binary stream에서 1byte씩 LF까지 읽은 뒤 그 바이트만 CSV 파싱.
  pandas.read_csv(nrows=0), Import-Csv, 전체 ReadAllText처럼 내부적으로
  응답 바이트까지 미리 읽을 수 있는 로더를 실제 data CSV에 사용하지 않는다.
  OS 내부 캐시 동작과 애플리케이션이 요청/파싱한 바이트 범위는 구분한다.
- 헤더 공백/중복 열 이름을 자동 보정하거나 pandas식 이름 변경으로 숨기지 않는다.
  예상하지 못한 숫자/값 형태 등 헤더 여부가 의심되면 원문을 출력하지 않고 중단한다.
- 파일 크기·mtime 같은 stat, 읽은 헤더 바이트 수와 헤더 자체 SHA256만 기록 가능.
  헤더 해시를 전체 CSV 해시로 표시하지 않는다. 전체 CSV/DTA 해시 금지.
- 키 값(ID_main/ID_ind/Form 포함), 응답 행, 행 수, 중복률, 결측률,
  데이터 타입 추정용 샘플, join, 역할 분할은 이번 범위가 아니다.
- DTA, callback working-children XLSX, ZIP, Parquet/NPZ/모델 캐시는 열지 않는다.

할 일:
1. 실제 헤더와 해당 labels/DDI를 파일별로 비교한다. 열 개수, 순서,
   양쪽에만 있는 이름, 중복 이름을 기록한다. 문항 수/표본 수와 구분한다.
2. ID_main/ID_ind/Form 및 문서상 계층 index의 존재와 문서 정의를 따로 적는다.
   문서에 정의가 없으면 의미 UNKNOWN. 동일 이름/유일성 추정으로 join을 승인하지 않는다.
3. 결측·분기·편집 플래그가 문서에 정의돼 있다면 그 열의 존재를 확인한다.
   이름만 비슷한 열은 후보일 뿐이다. 플래그 열이 없다는 이유로 일반 열의
   코드에도 정보가 없다고 단정하지 않는다. 코드 정의는 기존 문서로만 확인한다.
4. A032의 명명된 예 FamilyRegistered/NotRegIDFamilyType, IndAge/WGQSeeing에
   필요한 열이 어디에 존재하는지 문서와 대응한다. chapter와 물리적 파일을
   혼동하지 않는다. 없는 열을 값 추정/대체 열/인위적 section으로 보충하지 않는다.
5. 파일에서 확인한 사실, 문서에서만 설명된 의미, 여전히 제공기관에 물어야
   하는 사항을 구분한다. 기존 문의 초안은 발송하지 말고 남은 질문만 축약한다.

범위·비용:
정보 확인 과제이며 모델 실험이 아니다. 총40분, CPU1·GPUoff, 병렬 없음,
새 패키지 설치 없음. 표준 라이브러리의 작은 헤더 전용 도구가 필요하면
아래 s1 산출물 폴더 안에만 작성한다. 모델/기존 생산 소스는 수정하지 않는다.
읽기 경계 확인용 새 인메모리 예시(정상/인용/비정상 헤더)만 허용하며
기존 연구 fixture·성공한 테스트·공식 checker/score 재실행은 금지한다.
형식 오류나 비용 한도 도달 시 TECHNICAL_HOLD로 기록하고 다른 로더로 우회하지 않는다.

종료 조건·판독:
- HEADER_RECONCILED: 실제 헤더와 설명표의 대응 확인. 이것은 기술적 구조 사실뿐이다.
- HEADER_DIVERGENCE: 실제 차이를 정확히 기록. 데이터 손상/전체 부적합으로 확대하지 않는다.
- TECHNICAL_HOLD: 헤더를 정해진 경계로 확인할 수 없음. 원인만 기록하고 종료.
별도로 키/결측 의미의 문서 근거를 DOCUMENTED/PARTIAL/UNRESOLVED로 구분한다.
여섯 파일의 비교 또는 안전한 중단 기록과 남은 질문 정리가 끝나면 종료한다.
기존 가설의 oracle, 실제 효과, 독립 평가 정밀도는 이번에 계산할 수 없다.
헤더만 같아도 역할 분할·키 검사·fit으로 자동 진행하지 않는다.

산출물(전용 폴더 docs/analysis/A039-outputs/s1/):
- entry.json: 실제 읽기·HEAD·dirty/workflow 개정·허용 문서 식별
- header-comparison.json: 열 이름/대응/헤더 범위·해시, 응답/키 값 제외
- exposure-ledger.md: 승인 파일의 헤더 접근은 명시, 응답 값 노출과 구분
- remaining-questions.ko.md: 로컬 확인으로 해결된 질문과 남은 정확한 질문
- closeout.md, s0-handoff.ko.md, verification.json
필요한 최소 status/log 결과 갱신. A039 S0 산출물/기존 A038 기록은 덮어쓰지 않는다.
원본 자료·.gitignore·docs/tree.md·모델·제출 snapshot 수정 금지.

승인/노출 승계:
사용자 보고상 microdata 접근 승인 완료. 공개 XML/KOBO/reports/guide는
승인 없이 다운로드. 사용자는 다운로드·압축 해제만 했다고 확인했다.
기존 공통 약관 사본은 A032에 있으며 사용자의 승인 신청 내용과 동일하다고
단정하지 않는다. 이번은 로컬 메타데이터 확인뿐이며 배포/상용/hosted 사용
허가의 법적 판단이나 새로운 승인 신청을 수행하지 않는다.
17999명/12339SSUID 및 공개 집계/A022 원래 역할 노출을 유지한다.
E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866을 건드리지 않는다.

E041 incumbent/E025 fallback, E057/E060/E061 parked.
E058 STOP/E059 STOP_SELECTION과 모든 STOP/HOLD, A023/A024 empirical HOLD 유지.
A037의 P는 R/E041과 다르며 D-P/D-R를 구분한다. A_half 승격 없음.
A018 TEST 사용자 미확정, S3 중단, S2 후보 없음.
새 E기록·실험·fit/optimizer/predict/score·응답 데이터 탐색·웹/다운로드/연락·
commit/push·ZIP/제출·S2/S3 전환은 금지한다. 끝나면 S0에 결과를 돌려준다.
```
