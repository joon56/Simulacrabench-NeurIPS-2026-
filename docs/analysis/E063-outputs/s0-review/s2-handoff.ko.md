# 다음 세션: S2 · E063 고정 UNHCR round metric 조립·release 검증

사용자가 아래 전체 블록을 별도 S2에 실행 지시로 전달할 때만 적용한다.
S0의 문서 작성 자체는 실행 허가가 아니다.

```text
SimulacraBench / HSCC 별도 S2 — 고정 E063 조립·release 검증을 수행한다.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1
이 채팅을 실행 담당 S2로 지정한다. 아래 고정 후보의 조립/합성 검증/ZIP 제작만 허용한다.
새 모델 탐색·업로드·commit/push·원격·S3/TEST 선택은 허용하지 않는다.

1. 진입과 고정 입력
AGENTS → CLAUDE → docs/status.md → docs/log.md 최신3개 → docs/workflow.md를 읽고
실제 개정/역할/작업 유형/권한·읽기 증거를 기록한다. HEAD/dirty/active jobs 확인.
기존 사용자 변경과 과거 실패/manifest/latch를 보존하며 과거 HEAD로 복원하지 않는다.

docs/analysis/E063-outputs/:
- s0-review/decision.md, verification.json, 이 인계
- registration.md, closeout.md, verification.json, implementation-contract.md, exposure-ledger.md
- freeze-01.json, artifact-manifest.json, package-marker-identity.json, unit-qualification.json
- cost-time-ledger.json, attempts/{R-01,H-01}/{complete,environment,resources}.json
- attempts/score-01/{comparison,frozen-predictions}.json
원래 docs/experiments/E063-round-conditioned-metric.md도 읽는다.

주요 SHA256:
src/models/round_metric_retrieval.py
  5595bebdcdc697fc9e1eba149e10735cac4ae434b20b0ce3e93c968e8b35106b
E063 freeze-01.json
  86662430e7cd0c8cfd09eb6ddf0f08ca43ebd7bda96adbfc4cfe2d40edfebc9a
E063 registration.md
  e29a7600c9bd1bca75c6927a092adc706b3c49b7e6ea649d979e58816696a49c
E041 source src/models/supervised_retrieval.py
  2940338c5378de03303befb74e3834fbad631c0eb18f4ecb55d2cc39a471f879
E041 snapshot submissions/2026-09-19-E041/main.py
  22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
E025 snapshot submissions/2026-09-09-E025/main.py
  00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9

2. 목적과 고정 정책
S1 LOCAL_TECHNICAL_PASS_FOR_S0의 동작을 실제 배포 파일에서도 보존하는지 확인한다.
S1 H 자연 활성7/8, UNHCR46405 vectors/lambda37 변화, UNICEF/WB raw exact0.
합성 UNHCR skill +0.0000175788678469; section×wave16개 중8개 하락.
효과 근거는 매우 약하다. synthetic gain·release PASS를 실제 ERPIS/TEST 이득으로 쓰지 않는다.
selector/proxy·in-sample replay 한계, 독립 audit 없음, E063 parked를 유지한다.

고정35좌표 metric/penalty.001/원래 K32/seed/config/지원30/.003·2SE/lambda minimum30/
zero fallback/all-cell loss/재귀 renderer를 그대로 조립한다. head/round/seed/threshold/
허용오차/정책 변경·새 H-C selector·부분 성공 결과의 정책 전환 금지.
C=원래 E041/R 하나. 새 baseline family나 여러 후보를 만들지 않는다.

3. 허용 경로와 자료
새 scripts/assemble_e063.py, scripts/check_e063_release.py,
tests/test_e063_assembly.py 및 docs/analysis/E063-outputs/s2/에만 새 구현/기록.
기존 조립/검증 소스는 읽어 최소 재사용, 원본 변경/기존 성공 suite 재실행 금지.
준비본 submissions/YYYY-MM-DD-E063/와 같은 이름 ZIP은 실제 제작일 KST 사용.
경로 충돌 시 덮어쓰지 않는다. main.py는 ZIP 루트. 새 SCORES/NOTICE/manifest 작성 가능.
원래 S1 source/실험 본문/registration/manifest/snapshot/tree 변경 금지.
status/log에는 이번 결과만 추가한다.

이번 S2에 한해 다음 exact allowlist의 identity와 내용 접근을 허용한다:
A. E063 freeze의 세 synthetic _sandbox/{unicef,world_bank,unhcr}/respondents.parquet.
   전체바이트 hash 허용; 내용은 TRAIN/DEV filter·필요 columns만. TEST 요청/분석0.
B. E063-outputs/attempts/{R-01,H-01}/vectors-{unicef,world_bank,unhcr}.npz 정확히6개.
C. E062-outputs/vectors-{E025,E041}-{unicef,world_bank,unhcr}.npz 정확히6개.
D. 새 S2의 TRAIN/DEV 전용 staging/새 예측·공식 출력.
B/C는 manifest/hash 확인 뒤 allow_pickle=False로 flat/offset 확률만 읽는다.
학습된 model cache가 아닌 허용 synthetic 고정 비교 출력이다.
그 외 NPZ/Parquet/key/모델 cache/Adult/SIPP/VAF/UNCHR_data/실제 응답 접근·해시 금지.
S0가 이 raw 파일들을 재검증했다고 쓰지 않는다.

모델 worker에는 TRAIN과 DEV GIVEN만, 모든 DEV PREDICT를 입구 이전 missing으로,
EXCLUDE 제거. truth는 평가기만 접근, 출력/source freeze 뒤 평가.
공식 CLI staging은 TRAIN/DEV만 새로 복사하고 runtime schema/order/mask/roles의
round-trip을 모델 없이 먼저 검증한다. 원본 데이터 재생성/역할 변경 없음.

4. Baseline 재사용 및 조건부 최소 fresh 비교
E062-outputs의 frozen-inputs.json, frozen-predictions.json, artifact-manifest.json,
environment-{E025,E041}-01.json, {E025,E041}-complete.json 및 자원 기록을 읽는다.
문서상 세 기관 phase1 메타데이터가 E063과 같고 R raw SHA가 E062 clean E041과 같다.
이것은 재사용 단서이며 이번 S2의 파일/배열 검증을 대신하지 않는다.

동일 snapshot/source, schema/config/scorer, synthetic bytes, canonical row/order/
mask/roles, 완료/출력 provenance를 먼저 대조한다. 공유 환경 필드를 같은 import 시점에서
비교한다. E062/E063 environment JSON의 구조·threadpool 목록은 기록 시점이 다르므로
문자열 전체 동등성을 요구하거나 미기록 package version을 추정하지 않는다.
누락된 환경 근거·비교 범위는 그대로 공개한다.

입력/원본 snapshot hash가 맞고, 필요한 identity가 확인되면 기존 clean reference 재사용.
E063 R와 clean E041 reference의 모든189649 raw vector exact parity로 source R 연결도 확인.
기존 E025/E041 학습을 성공 반복하지 않는다. 원래 R/H source all3도 재실행하지 않는다.

고정 입력·E063 실행 환경은 확인되지만 특정 baseline의 완료/raw reference/환경 근거가
부족해 재사용 판정 불가인 경우에만 그 원래 snapshot의 fresh all3 한 번을 허용한다.
가능하면 model 실행 전에 metadata-only 판단으로 결정·동결한다.
최대 E0251회/E0411회; 원래 모델·seed/config·동일 입력만. 새로운 baseline은 아니다.
기존 raw 파일의 불일치는 숨기지 않고 보존하며 신뢰하지 않은 배열은 읽지 않는다.
fresh E041을 사용해도 E063 R와 exact parity가 필요하다.
입력/원본 source hash 불일치 또는 R≠clean E041이면 HOLD. 새 fit으로 구제하지 않는다.
추가 baseline 여부는 점수를 본 뒤 유리한 기준을 고르기 위한 분기가 아니다.

5. 조립·검증 순서
새 S2 사전 등록에 fixed source/input/scorecard/예산/재사용 분기/판독 기준을 동결한다.
세 empty package markers도 지금 manifest에 포함하되 S1 freeze 누락을 소급 수정하지 않는다.
기존 .venv/CPU 환경만 사용. 새 설치/의존성 변경/취득/클라우드 없음.

A. 새 조립 경계만 작은 no-fit fixture로 검사한다.
원래 E041 prefix/binding과 H를 분리한다. metric_objective/fit_sections/
_replace_evidence/LAST_DIAGNOSTICS 등 동명 global을 덮어써 원래 fallback을 바꾸지 않는다.
original.predict, original._retrieval_log, shared renderer/config 연결을 명시한다.
namespace 격리/명시 mapping과 standalone import 검증. src/scripts/local path 의존 없음.
실제 새 assembly의 controls/fallback/지원 H dispatch를 검사한다. S1 성공10개 반복 금지.

B. 조립 main.py fresh all3 한 번. 총189649, UNICEF17856/WB39520/UNHCR132273,
schema 순서/크기/유한/비음수/양의 합, sum error<=1e-6.
S1 H와 모든 raw max차이0. UNICEF/WB clean E041 exact0.
자연 활성·정책·기존 UNHCR 변화 보존. 불일치를 round/head 선택으로 숨기지 않는다.

C. 동일 고정 bytes로 ZIP 제작, 공식 tools/check_submission_zip.py PASS.
새 경로에 실제 ZIP 추출, snapshot/archive/extracted source byte parity.
추출본으로 정식 score.py phase1 세 기관 전체를 하나의 shared900초 suite로 실행한다.
세 기관 import/startup/predict/평가/종료 합계다. 기관당900초가 아니다.
그 공식 실행에서 보존한 raw 출력으로 S1 source→assembly→extracted exact parity 확인.
parity를 위해 별도의 세 번째 성공 candidate all3를 돌리지 않는다.

D. 공식 normalize/floor.001/skill로 각 기관 candidate-E025>=-.002 AND
candidate-E041>=-.002. 기존 baseline 출력도 새 release 평가의 동일 truth/order/scorer로 비교.
두 하한 모두 필수. 불필요한 subgroup/seed/grid 탐색 없음.
전체 score와 S1의16개 descriptive 하락/상승을 구분해 승계한다.
의존성·외부 모델/데이터 disclosure·offline import/runtime 확인.
Python network guard를 native egress 완전 차단 증명으로 쓰지 않는다.
H100/hosted 설치·전체900초 미관측은 미확정으로 기록한다.

6. 총량·관측·같은 세션 수리
gross120분, 마지막10분 기록. 계산 합계3600초: 준비/새 검사/실패/평가/모든 model stage 포함.
assembly all3, extracted official all3, 조건부 baseline 각각<=900초.
CPU numerical threads2/GPU0/heavy1, owned controller+descendants RSS/private 각각8GiB.
monitor는 import 전 시작·.1초 polling, 실제 monotonic 최대 sample gap도 기록한다.
관측된 peak와 연속 시간 보장의 차이를 명시. monitor failure 중 계속 실행 금지.
종료/cleanup 포함 실제 stage wall로 총량 계산, 겹친 parent/child/nested spans 중복 가산 금지.
새 focused tests 합<=300초/각 child<=60초로 같은3600초 안에 포함한다.

정상 S2: 후보 all3 두 단위,6pipeline/18neural/16metric.
재사용 불가 baseline만 추가: E025 +3/9/0, E041 +3/9/8, 각각 최대1회.
실제 조립/실행기 구현 결함의 영향 재검증용 추가 all3 상당량 최대1회.
절대 합산 상한 all3 상당량5개/pipeline15/neural45/metric32 및3600초.
이는 최대 허용량이며 baseline 재사용이 되면 해당 fit0, 수리 없으면 reserve0.
공식 suite가 여러 OS process를 써도 위 all3 단위/호출 수로 계수하고 실제 PID는 별도 기록.
checker tiny no-fit predict 별도 기록; 실제 neural/optimizer가 생기면 상한에 포함한다.

실패 worker 중단·증거 보존 후 ordinary argument/import/path/encoding/assembly 오류는
같은 S2에서 원인 확인→최소 수정→영향 경계 검증→새 freeze로 계속한다.
변경으로 무효화된 검사만 재실행. 실패/latch/source bytes 보존. 오류마다 S0 인계 금지.
정책/자료/원본 모델 변경, regression/resource 실패 구제, 성공 무변경 반복은 금지.
남은 총량으로 유효 비교 불가면 구체적 INCOMPLETE/HOLD로 S0 반환.
과거 S1 754.551699초/6pipeline/18neural/16metric는 별도 역사로 승계한다.

7. 사전 hosted 판독표와 종료
SCORES는 실행/업로드 전 고정. 기준은 E041 ID933094 사용자 제공 Development/phase29772:
Grand .6433333333 / UNICEF .52 / WB .49 / UNHCR .92.
submissions/SCORES.md 및 hosted-scores/2026-09-27.json 출처를 사용.
원격 직접 인증·동일 scorer 버전 확인으로 확대하지 않는다. 화면.64와 API 문자열 구별.
과거 E062 공개 동점 UNRESOLVED 유지.

- 비교 가능한 Finished/phase/ID/filename/출처, UNHCR와 Grand 상승+UNICEF/WB 공개값 동일:
  고정 전체 정책에 favorable noisy evidence. 자동 채택/유의성/정확한 효과는 아님.
- UNHCR/Grand 동점과 통제 동일: UNRESOLVED, E041 유지/E063 parked.
- UNHCR 또는 Grand 하락: 해당 실행 adverse. 반대 방향·통제 공개값 변화는
  mixed/귀속 미해결도 명시. 공개값 변화만으로 raw control 변화/누수를 확정하지 않는다.
- 실행 실패: technical. 필수 값 부재/출처·phase·scorer 모순: 판단 보류.
숨겨진 round/head 효과·원점수를 Grand에서 역산하지 않는다.
어느 arm도 동일정책 자동 재제출·seed/head/threshold 구제·S3/TEST 선택을 허용하지 않는다.

모든 필수 release 조건 통과 시 RELEASE_QUALIFIED_FOR_USER_REVIEW로 S0 반환.
산출물: ZIP/main/SCORES/NOTICE, source/archive/extracted manifest와 SHA256/bytes,
reference 재사용 또는 conditional fresh 근거, 조립/공식 checker/score logs,
raw parity/기관별 regression/resource/call/exposure/수리/verification/closeout/s0-handoff.
미완료면 qualification 대신 정확한 실패/누락 조건과 보존 증거를 남긴다.
예비 작업은 closeout뿐. 새 모델이나 다른 과제로 넘어가지 않는다.

준비일은 업로드일이 아니다. 계정/slot/upload ID·시각·remote bytes는 미확정.
사용자가 제출을 결정하기 전 로그인/조회/업로드하지 않는다.
원래 S1 기록·source·manifest·실험 본문·snapshot·tree 보존, commit/push/서브에이전트 없음.
E041 incumbent/E025 fallback, E057/E060/E061/E062/E063 parked.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040와 모든 STOP/HOLD,
17999명/12339SSUID·집계·A022 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단.
현재 준비 결과를 실제 DEV/TEST 채택으로 자동 전환하지 않는다.
```

