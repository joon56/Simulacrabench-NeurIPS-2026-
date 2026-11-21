# S1 — A040 공식 runtime schema 계약 보완 및 전체 경로 재시도

작성 자체는 실행 허가가 아니다. 사용자가 별도 S1에 아래 범위를 지시할 때 실행.
S0에서 코드 수정·진단 테스트·입력 생성·모델 실행하지 않았다.

```text
SimulacraBench / HSCC S1 — A040 runtime schema entry repair + full-path retry.
폴더 C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS → CLAUDE → status → log 최신3개 → workflow.md 순서로 읽고
실제 개정·S1 technical 역할·범위 보고. HEAD/dirty/active jobs 확인·보존.
다른 세션/서브에이전트·commit/push·S2/S3 실행 금지.

필수 입력:
- docs/analysis/A040-outputs/s0-schema-failure-review/{decision.md,verification.json}
- docs/analysis/A040-outputs/full-path-local/{closeout.md,verification.json,
  resources.json,source-manifest.json,generation-failure.txt,registration.md,
  generate_fixture.py,runner.py,orchestration.py,tests_model_free.py,roles.json}
- docs/analysis/A040-outputs/s0-retry1-review/s1-full-path-handoff.ko.md
- docs/analysis/A040-outputs/s1/{contract.md,cost-accounting.md,observation-plan.md}
- local-technical-retry1/closeout.md 및 s0-policy-resolution/decision.md
  (모두 docs/analysis/A040-outputs/ 아래)

이전 full-path는 입력 생성 실패/scientific0회, code+input freeze 미도달.
post-failure manifest를 사전 동결로 바꾸지 않는다. 이전 local failure와
retry1 PASS, failed full-path 코드/역할 배열/산출물 보존. 기존 설치/주최측
정책 승인 승계; 다시 문의·재설치·취득하지 않는다.

새 위치:
docs/analysis/A040-outputs/full-path-local-retry1/ 및
tmp/a040-full-path-local-retry1/. 기존 경로가 있으면 상태 확인, 덮어쓰기 금지.
실패 폴더의 코드를 새 위치로 복사하되 원본 수정·역할 재배정·latch reset 금지.
기존 승인된 tmp/a040-local-technical/venv/source/acquisition 재사용.
과거 fake 입력/예측/모델cache/보호자료 접근 금지; 기존 역할 배열은 공개
행 위치 metadata로 비교 가능. 실제 응답/키가 아니다.

수정 목적/허용:
raw JSON을 runtime schema로 취급한 결함만 보완한다.
공식 external/starter-kit/make_sandbox.py의 load_config/load_schema/options_for
계약을 따르는 공통 진입 helper를 generator와 runner 양쪽에서 사용한다.
공식 로컬 HEAD ee427a94f6cc6a0d9d653b6be68c835a032e7552 및 실제 파일 해시 기록.
load_schema는 config의 gated_value를 덮어 넣고 option/parent/dataset/split을
검증한다. config.yml의 값을 사용하며 hardcoded fallback/setdefault/원본
JSON 편집 금지. score.py의 loader·schema 전달 경로를 문서 근거로 연결한다.
schema helper는 모델 import/응답 생성/채점 부작용이 없어야 한다.
기존 PyYAML6.0.3 등 설치 환경 유지; import make_sandbox는 허용하지만
make_sandbox main/공식 generator/score.py main은 실행하지 않는다.

나머지 변경은 새 attempt 경로·deadline·latch·manifest·정규화 metadata 및
명명된 entry 검사 추가만. E041/adapter 바이트, 모델/seed/head/context/grid/
alpha/guard/tolerance·fake 값 생성 규칙·역할 순서·기존 assertions 유지.
추가 모델 정책 수정 필요 시 실행 전 이유를 남기고 S0 반환.

1. 실제 all3 공개 schema의 모델 없는 진입 검증(총60초 이내):
- unicef/world_bank/unhcr raw schema와 명시된 config 파일을 실제로 읽는다.
  손으로 gated_value를 넣은 spy만으로 통과시키지 않는다.
- 세 개 모두 공식 load_schema 결과와 generator/runner의 공통 helper 결과가
  동일하고, item/GIVEN/PREDICT/option 순서가 유지되는지 확인한다.
- layout의 모든 옵션을 공식 options_for와 비교. sentinel은 gated item에만
  마지막1회. 데이터셋/split 검증과 정확한 전체 option 폭·출력 개수 확인.
- UNICEF/WB raw field 부재, UNHCR raw field 존재 모두 처리. 복사본의 raw field가
  달라도 config가 우선하는 공식 동작 확인. 원본 파일은 변경하지 않는다.
- loader 검증 오류가 조용한 기본값으로 바뀌지 않는지 확인. 예외를 예상한
  negative test는 정상 회귀검사이며 예상하지 못한 실패와 구분한다.
- generator/runner가 실제 이 helper를 호출하는 연결까지 검사한다.
  runner import는 argparse/파일 생성/모델 부작용이 있으므로 직접 import하지
  말고 helper·안전한 metadata entry·정적 call-site 확인을 조합한다.
  새 경로 통합에 필요한 model-free role/branch 검사는 같은60초 안에 수행.
  성공한 TabICL tiny suite 또는 실제 E041 호출은 이 단계에서 금지.

2. 전체 fake 입력 생성1회:
entry PASS 후 같은 seed4000/PCG64(4001)과 원래 full-shape 생성 규칙으로 새
경로에 생성. 역할 SHA256은 기존 기록
0f61e0364bb4c2fb9465dffa18a71a391175afb2b149f4f730588f86ebdc3447과 비교.
이전에는 fake 값 파일이 없어 비교할 이전 response hash는 없다. 만들지 않는다.
UNICEF14885/1488, WB5195/520, UNHCR8279/621; external query truth 생성 금지.
각 raw schema/config/공식 loader와 normalized runtime schema의 해시·옵션
순서를 새 manifest에 연결한다. raw와 runtime 해시를 혼동하지 않는다.
generator/runner가 같은 정규화 결과를 쓰는지 metadata로 재확인한다.

3. code+input+환경을 새로 사전 동결한 뒤:
기존 full-path handoff의 모든 명명 검증을 유지한다. E041 source SHA256
22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
reference E041 all3 fresh process1회 최대900초; 성공 후만 candidate forced-active
all3 fresh process1회 최대900초. checkpoint 검증 후 로드, runtime network 방어.
실제 UNHCR F6279/S1000/E1000 및 final8279 context, alpha{0,.25,.5}/원래guard,
자연 정책 출력과 engineering alpha.25 활성경로 구분.189649 canonical vectors,
실제 controls/inactive/fallback exact parity·refit/격리·실측 비용을 확인한다.
fake guard 결과를 효과/채택 근거로 쓰지 않는다. 정책 변경·축소·사후 tolerance 금지.

한도/종료:
task wall120분, model-free 총60초, generator1회, scientific최대2회/합1800초.
RTX3070한개/CPU2/heavy1, host RSS/private commitment16000000000bytes,
1초 watchdog, CUDA peaks 및 모든 shadow/refit/fit/predict/load/renderer 비용 기록.
각 scientific900초는 import/load/all3/검증/직렬화 포함. 첫 예상 밖 오류·한도에서
중단하고 자기 process tree만 종료. input regeneration/추가run/사후수정·재실행 금지.
기존 과학누적2회/parent54.0961857초와 새 준비·과학 비용을 구분해 누적 기록.

산출물:
공식 계약 출처·해시, 원본대비 diff, all3 entry-test 결과, raw/runtime schema
manifest, 새 fixture/role 해시와 사전 scientific freeze, reference/candidate
결과·자원·parity/노출 내역, verification/closeout/S0 handoff. status/log 최소 갱신.
전체 통과만 LOCAL_FULL_PATH_PASS. entry만 PASS면 full PASS 아님.
입력/계약오류 LOCAL_FULL_PATH_FAIL, 한도 LOCAL_RESOURCE_LIMIT, 시간부족
INCOMPLETE, 환경미확보 BLOCKED_RESOURCE. 실패 closeout만 예비 작업으로 허용.
H100/hosted900초/실제 ERPIS 효과/release PASS는 어느 결과에서도 자동 주장 금지.

보존/금지:
실제 응답·키·보호 Parquet/NPZ·기존 모델cache/VAF·옛 fake 자료 접근/재해시 금지.
고정 공개 checkpoint 검증·로드와 이번 새 fake 입력/출력만 예외.
새 모델/E기록/원격·유료자원/설치·취득/ZIP/checker/official release all3/
E025 release평가/업로드/tree/기존 snapshot 수정/commit/push/S2/S3/TEST 금지.
기존 E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
A039 HOLD·A_half 비승격·A018 미확정/S3 중단 유지.17999명/12339SSUID·A022
원래 역할·E059 소비 oracle/selection과 보호 audit2074/1177·calibration1866 보존.
완료 후 S0로 반환. 이 인계는 S2 제작이나 유료 서버 허가가 아니다.
```
