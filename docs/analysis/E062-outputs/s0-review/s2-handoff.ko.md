# 다음 세션 제목

S2 — E062 고정 WB 후보 조립·release 검증

사용자가 아래 블록을 별도 S2에 전달하면 해당 범위의 실행 지시가 된다. S0의 작성 자체는 실행 허가가 아니다.

```text
SimulacraBench / HSCC 별도 S2에서 고정 E062의 조립·release 검증을 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

이번 지시는 WB만 바꾼 고정 후보의 아래 조립·합성 검증·ZIP 제작을 허용한다.
새 모델 탐색/정책 변경/업로드/commit/push/S3/TEST 선택은 허용하지 않는다.
S1의 소진된 예산을 재개하지 않고 이번 S2 예산을 별도로 등록한다.

1. 진입과 고정 근거

AGENTS → CLAUDE → docs/status.md → docs/log.md 최신3개 → docs/workflow.md를
실제 읽고 역할 S2, 작업 유형 release technical validation, 개정과 범위를 보고한다.
현재 HEAD/dirty/active jobs 확인; 기존 변경 보존. 과거 manifest로 되돌리지 않는다.
현재 workflow r5 SHA256:
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23

docs/analysis/E062-outputs/ 아래를 읽는다:
- s0-review/decision.md, s0-review/verification.json, 이 인계문
- closeout.md, verification.json, comparison.json, resource-summary.json
- implementation-contract.md, registration.md, exposure-ledger.md
- frozen-inputs.json, frozen-predictions.json, artifact-manifest.json
- environment-candidate-01.json 및 두 baseline 환경/완료/자원 metadata
- docs/experiments/E062-wb-ordinal-heads.md

고정 source src/models/wb_ordinal_heads.py SHA256:
5a718f08bc7dd3342ea6b8ba48d63dcb4dbf1e9a2bc70fee9d1b6ec03ac33338
S1 frozen-inputs.json SHA256:
7a7333b5660488eeb7c3e1685348028fd4a412486cb2c9b64d98afd308068bfd
S1 registration.md SHA256:
c6b7d587dcc928a761f65b510f8c6018b6c26f7c6b2e59d11a28a4cf0c6389d9
E041 snapshot submissions/2026-09-19-E041/main.py SHA256:
22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
E025 snapshot submissions/2026-09-09-E025/main.py SHA256:
00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9
의존 source/공식 schema/config/score identity는 S1 허용 목록으로 대조한다.

2. 목적·해석 경계

목적은 research source와 같은 실제 배포 파일, 공식 전체 경로·비용·회귀 검증이다.
S1은 EXPLORATORY_SOURCE_QUALIFIED. WB skill+.0002723772이지만 target16
log score-.0007987550, other60+.0009093584. Not answered도 하락했다.
이는 순서형 대상 개선 증거가 아니다. 초기화/비응답/trunk/선택/refit를 포함한
전체 절차의 탐색 후보다. synthetic 양성·release PASS로 실제 효과를 주장하지 않는다.
E041 incumbent/E025 fallback, E062 parked 유지. 기존 S1 본문·실패·manifest 불변.

3. 허용 파일·데이터와 구현 범위

새 scripts/assemble_e062.py, scripts/check_e062_release.py,
tests/test_e062_assembly.py, docs/analysis/E062-outputs/s2/ 기록을 만들 수 있다.
기존 E061 조립/검증 소스는 읽어 최소 재사용하되 그 원본/기존 suite는 수정·재실행하지 않는다.
새 제출 snapshot은 실제 제작일 KST의 submissions/YYYY-MM-DD-E062/ 및 같은 ZIP.
기존 경로가 있으면 덮어쓰지 말고 상태를 확인한다. main.py는 ZIP 루트에 둔다.
원본 src 모델·S1 실행기·S1 결과/registration·기존 snapshot·tree 수정 금지.
새 SCORES/검증 기록·status/log 결과 추가만 허용. 새 E번호/모델 변형 없음.

이번 S2에 한해 허용:
- external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet
  세 기존 synthetic 파일의 해시와 TRAIN/DEV 역할 읽기. 정확한 hash는 S1 freeze.
- docs/analysis/E062-outputs/vectors-{E025,E041,candidate}-{unicef,world_bank,unhcr}.npz
  정확히9개. S1 manifest와 해시 대조, allow_pickle=False로 확률/offset만 읽기.
  모델 가중치 cache가 아닌 이번 E062의 알려진 synthetic raw 확률 비교 자료다.
- 새 S2 출력/공식 staging의 허용 synthetic 자료와 예측 파일.

다른 NPZ/Parquet/모델 cache, 실제 응답/키/Adult/SIPP/VAF/보호 역할 접근·재해시 금지.
Parquet는 TRAIN/DEV 필터와 필요한 열 projection으로 읽으며 TEST 행 요청0.
모델에는 DEV GIVEN만, 전체 DEV PREDICT는 missing, EXCLUDE 제거.
truth는 평가기만 접근. 공식 CLI staging은 TRAIN/DEV만 포함하고 schema/role/
masked-frame round-trip을 모델 실행 없이 먼저 확인한다. 원자료를 바꾸지 않는다.
이전에 노출된 synthetic engineering이며 새 독립 평가나 audit이 아니다.

기존 .venv/CPU 환경만 사용한다. 새 설치/취득/환경/Modal/H100/원격/유료 작업 없음.
source/global binding 충돌, OrdinalNet이 원래 nominal _Net을 상속하는 연결,
E041 control dispatch와 WB factory를 조립 과정에서 정확히 보존한다.
head/seed/초기화/config/w/epoch 규칙/λ minimum30/zero fallback/floor를 바꾸지 않는다.

4. 실행 전에 등록할 순서와 통과 조건

A. source/입력/runtime schema/role·마스킹/환경/S1 출력 identity를 확인한다.
S1 아홉 출력은 이미 fresh clean E025/E041/candidate에서 만들었다. 동일성이
성립할 때만 새 조립/추출 출력과 비교하는 reference로 사용한다. baseline/source
학습을 성공 반복하지 않는다. 환경 또는 자료 identity가 달라지면 기존 결과를
현재 검증으로 둔갑시키거나 자동 재학습하지 말고 정확한 불일치를 S0에 반환한다.
S0가 Parquet/NPZ를 새로 검증했다고 쓰지 않는다. 이번 S2 접근을 별도 계수한다.

B. 새 조립 경계만 집중 검사한다. 외부 repository 경로 없이 standalone import,
원본 의미/함수 binding·세 기관 dispatch·archive root/허용 파일 계약을 확인한다.
작은 모델 없는/optimizer 없는 입력을 사용한다. S1 성공13개 suite는 반복하지 않는다.
release source/input/scorecard/예산을 모델 실행 전에 동결한다.

C. 조립된 main.py의 fresh all3 한 번. UNICEF17856/WB39520/UNHCR132273,
총189649 vectors의 schema 순서/shape/finite/nonnegative/positive mass 확인.
S1 candidate와 모든 raw vector max차이0. UNICEF/UNHCR는 clean E041과도 exact0.
WB 변화를 유지하며 inactive/선택값 구제로 불일치를 숨기지 않는다.

D. 고정 bytes로 ZIP 제작·정식 tools/check_submission_zip.py 실행.
ZIP을 새 경로에 추출하고 snapshot/ZIP entry/extracted source byte parity를 확인한다.
추출한 실제 ZIP의 main.py에 대해 정식 score.py phase1 세 기관을 한 suite로 실행한다.
별도 임의 scorer나 in-process 검사만으로 공식 CLI PASS를 대체하지 않는다.
세 기관 합산 startup/import/predict/평가/프로세스 종료 전체를 shared900초로 감시한다.
같은 공식 실행에서 얻은 raw 출력으로 source→assembly→extracted exact parity를 확인;
이를 위해 별도 세 번째 성공 후보 all3를 돌리지 않는다.

E. 공식 floor .001/skill 계산을 사용해 각 기관 candidate-E025≥-.002 AND
candidate-E041≥-.002를 확인한다. 정확한 동일성으로 연결된 S1 clean baseline과
이번 release 출력을 비교한다. 기준을 완화하지 않는다. S1 target16 하락/other60
상승은 기록을 승계하며 새 subgroup 탐색·head 선별을 하지 않는다.
완성 package 전체 runtime/owned memory, dependencies/models/external-data disclosure,
offline import/runtime 계약과 숨은 로컬 경로 의존 여부를 기록한다.
로컬 Python network guard는 native egress 차단 증명이라고 부르지 않는다.
원격/H100 실행 없이 확인할 수 없는 hosted 보장은 미확정으로 남긴다.

5. 자원과 같은 세션 수리

gross120분, 마지막10분 기록. CPU numerical threads2/GPU0/heavy1.
owned controller+child RSS 및 private commitment 각각8GiB, .1초 관측.
조립 all3≤900초, ZIP 추출본 공식 all3 전체≤900초, 새 computational child 합≤2400초.
문서 준비/오류 수정도 gross에 포함; parent/child/stage 겹침을 중복 합산하지 않는다.
기존 S1 computational1123.1965955초/pipeline9/neural27/metric16은 별도 역사로 승계한다.

정상 S2 모델 작업은 두 all3: pipeline6/neural18/metric16.
구체적인 조립·실행기 구현 결함이 확인돼 그 경계 재검증이 필요할 때만
추가 all3 상당량을 최대 한 번 허용한다. 총 S2 attempt cap pipeline9/neural27/
metric24와2400초는 그대로다. 실패/부분 실행도 소비. 원본 모델 정책 변경 금지.
예비량은 낮은 점수·시간/메모리 초과·유리한 seed 탐색·무변경 성공 반복에 사용하지 않는다.
checker의 tiny no-fit predict는 별도 기록하고 실제 neural 호출이 생기면 cap에 포함한다.

한도 초과/invalid output/과학 오류는 해당 owned worker를 중단한다. r5에 따라
원인과 diff를 남기고 같은 범위의 일반 구현 오류는 이 S2에서 수리한다.
오류마다 새 S0 인계를 요구하지 않는다. 남은 합산 예산/횟수로 검증 불가하거나
원본 정책/환경/자료를 바꿔야 하면 S0로 반환. 기존 실패/latch/freeze는 보존한다.

6. SCORES 사전 판독과 종료 산출물

실행/업로드 전 SCORES에 고정 후보·local 결과의 한계와 아래 arm을 기록한다.
E041 사용자 API 기준 ID933094, Development: Grand .6433333333,
UNICEF .52/WB .49/UNHCR .92. submissions/SCORES.md 및 hosted-scores/
2026-09-27.json의 기존 출처를 사용한다. 현재 live 플랫폼 인증으로 쓰지 않는다.
Grand 화면 .64와 전체 API 값을 구분; 세부값은 Grand에서 역산하지 않는다.

- Finished/동일 phase·비교 가능한 출처 + WB/Grand 상승, 두 통제 공개값 동일:
  고정 전체 후보의 favorable noisy evidence로 S0 검토. 실제 정확한 효과/대상16
  개선/통계적 유의성/자동 incumbent·TEST 승격은 아님.
- WB/Grand 동점: unresolved, E041 유지/E062 parked. 효과0으로 단정하지 않는다.
- WB 또는 Grand 하락: adverse observation. 반대 방향이나 통제 공개값 변화는
  mixed/귀속 미해결도 명시하고, 변화만으로 코드 누수나 raw 예측 변화로 단정하지 않는다.
- 실패: technical. phase/scorer/파일/ID 출처 모순 또는 필요한 값 부재: 판단 보류.
어느 arm도 동일정책 자동 재제출·seed/head/threshold 구제·S3 재개를 허용하지 않는다.

모든 필수 release 검증을 통과하면 RELEASE_QUALIFIED_FOR_USER_REVIEW로 S0 반환.
미완료/불일치면 구체적인 HOLD/FAIL과 남은 검증을 기록; source PASS를 덮어쓰지 않는다.
산출물: source/archive/extracted manifest와 SHA256/bytes, 조립·checker·official 로그,
raw parity/clean regression/환경·resource·exposure·비용·수리 기록, verification,
closeout, s0-handoff.ko.md, 준비본 ZIP 및 SCORES. 실패본은 release로 표시하지 않는다.
원래 S1 manifest/registration/실험 본문은 보존하고 status/log에 새 결과만 추가한다.
준비일은 업로드일이 아니다. 실제 upload ID/time/bytes/계정·slot은 미확정으로 둔다.
사용자 업로드 결정 전 로그인/조회/업로드하지 않는다. commit/push/tree/S3 실행 없음.

E041 incumbent/E025 fallback, E057/E060/E061/E062 parked. 모든 STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039/A040 및17999명/12339SSUID·집계·A022 역할,
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866 보존.
A_half 비승격, A018 사용자 미확정, S3 중단. 다른 세션/서브에이전트 자동 실행 금지.
```
