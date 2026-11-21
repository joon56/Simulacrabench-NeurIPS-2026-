# 다음 S1 기술 작업 프롬프트 — 아직 실행하지 않음

제목: HSCC · S1 · 실제 후보 생성 경계와 전체 비용 명세

```text
SimulacraBench / HSCC S1 기술 검토를 진행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: 1d223340d4e1fa3993b411dc5daafab9cb37d0cd.
A020/E059/A021/A022는 미커밋 상태다. HEAD만으로 식별하지 말고
docs/analysis/A022-outputs/session-manifest.json의 입력 해시도 확인한다.

CLAUDE.md → docs/status.md → docs/log.md 최신3개 → docs/workflow.md 순서로
읽고 docs/session-prompts.ko.md, A021-selector-comparison-contract.md,
A021-outputs/verification.json, A022-remaining-role-audit.md,
A022-outputs/verification.json과 technical-retry.md를 적용한다.

목적: A021 통제 P/D 비교를 실제 후보 생성 절차로 연결할 수 있는지,
그리고 전체 실행을 어떻게 계수·제한할지 기술적으로 판단한다.
A021의 수기 확률표 계약 재증명이나 E056/E059 재실행이 아니다.
P는 원래 R/E041과 다르다. D-P는 목적함수 비교, D-R은 전체 절차 비교다.

주력은 후보 생성 경계와 비용 계약 구현이다. 실제 데이터는 사용하지
않고, 생산 소스를 읽어 다음 내용을 문서화하고 작은 stub/fixture로 검증한다.
1. 유한 후보 목록과 선택 근거, 필요한 학습 산출물, donor 순서·동률,
   activity-dependent lambda, 고정 legacy bucket, 전역 재귀 렌더링을
   입력→출력으로 연결한다. A021의 C0..C3는 기계적 예시일 뿐이다.
   실제 스키마 후보를 정한다면 공개 구조만으로 사전 정의하고,
   데이터 역할·채널이 그 기제를 검증할 수 있는지도 별도로 판단한다.
2. P/D가 동일 후보·lambda·역할·규칙·구축 예산을 공유하도록 한다.
   후보/lambda를 S 전 동결, 선택을 E 전 동결한다. 선택기에서 학습기로
   돌아가는 경로를 금지한다. 새 proxy 목적함수·guard를 끼워 넣지 않는다.
3. 생산 함수는 호출하지 않는 주입형 stub으로 정보 접근과 fit 호출을
   기록한다. calibration/selection/evaluation 응답이 금지된 단계에
   전달되면 실패하는 테스트, 후보 동결/동일성 테스트만 추가한다.
   Stub PASS를 실제 upstream 누수 없음이나 모델 동등성으로 주장하지 않는다.
4. 정상 경로의 base pipeline2개와 내부 neural call6개의 차이를 소스로
   확인한다. metric optimizer/ladder/lambda/render/optional refit와 실패·
   fallback 경로까지 계수표와 미래 실행 계측 위치를 작성한다.
   미측정 시간·메모리는 미측정으로 둔다. fit 없이 실제 비용을 측정했다고
   쓰지 않는다. 최소 설계는 refit 없음; refit는 미래 별도 범위다.

평가 경계: A022 잔여8700명/4975SSUID는 독립된 새 데이터셋도 새 audit도
아니다. 기존 A014 household 역할별 fit4275/2453, calibration1368/779,
oracle1333/764, selection842/478, audit882/501을 보존한다.
역할별 숫자는 향후 설계 검토 입력이지 실제 역할 부여·읽기 허가가 아니다.
SIPP 단일 section/정확 gate를 UNHCR section 간/근사 gate 증거로 포장하지
말고 인위적 section 변경으로 이를 해결하지 않는다. 적절한 채널이 없으면
실증 HOLD 유지. 필요한 평가 정밀도·다중 후보/두 비교 처리는 응답을 열기
전에 설계해야 한다. 기존 lambda minimum30과 zero fallback을 보존한다.

E059 oracle1918/1124SSUID와 selection2007/1130은 소비된 개발 근거다.
E059 audit2074/1177, 과거 calibration1866과 기존 역할은 보호한다.
누적17999명/12339SSUID 사용, 원천 집계 노출, A022 키/적격 필드 재검사
이력을 승계한다. 새 seed/chat은 새 자료가 아니다.

허용: 소스·공개 스키마·기존 문서/집계/해시 읽기, 독립 기술 명세와
실제 학습을 호출하지 않는 fixture/stub 코드 작성·검증.
예정 A023은 시작 시 충돌 확인 후 A 분석으로만 사용한다. 허용 파일은
docs/analysis/A023-*.md, docs/analysis/A023-outputs/*,
scripts/check_a023_*.py, tests/test_a023_*.py, docs/status.md, docs/log.md.
기존 모델·실험·A021/A022·사용자 파일과 docs/tree.md는 수정하지 않는다.

금지: source/key Parquet 재열람, 실제 PREDICT/GIVEN 응답 접근,
모델 캐시 역직렬화, 실제 fit/optimizer/예측/score 호출, E060 생성,
threshold/seed/head 변경을 통한 구제, 설치·다운로드·GPU·유료 자원,
commit/push, ZIP·제출·S3 재개. 평가 역할을 실행상 재배정하지 않는다.

한도: 60분, CPU2, 작은 fixture만, 합산 RSS/commitment2GiB.
자원 측정 불가하면 측정됐다고 주장하지 말고 중단 사유를 기록한다.
기술 주력이 식별 불가능하면 정당한 예비 작업은 누락된 입력·역할·채널·
비용 조건을 명시하는 문서 closeout뿐이다. 다른 모델 실험으로 넘어가지 않는다.

종료: 기술 계약과 계수표를 검증하면 TECHNICAL_PASS/EMPIRICAL_HOLD,
누수·동결·의미 불일치나 자원 초과는 해당 기술 작업 STOP,
평가 채널/정밀도/후보가 미정이면 미정 항목을 명시하고 HOLD.
어느 결과도 실제 학습·응답 열람·S2 후보를 자동 허가하지 않는다.

산출물: 후보/정보흐름 계약, 소스 근거가 있는 비용·호출 계수표,
fixture 결과와 한계, 해시 manifest, 노출/실행0 기록, S0 인계와 다음 판단.
E041 incumbent/E025 fallback/E057 parked, E058 STOP/E059 STOP_SELECTION,
모든 기존 STOP 유지. A_half 자동 승격 없음. A018 TEST 선택 사용자 미확정,
S2 후보 없음. 종료 후 S0로 돌려보낸다.
```
