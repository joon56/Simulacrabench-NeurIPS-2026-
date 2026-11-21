# 다음 세션 제목

**HSCC · S2 · E061 고정 후보 조립·DEV 제출물 검증**

S0 A034가 S2 검증 이관을 결정했다. 아래 코드블록을 별도 S2에 붙여 넣는다.
작성·열람 자체는 실행이 아니다. 작성한 S0와 종료한 S1은 이를 실행하지 않는다.

```text
SimulacraBench / HSCC S2 E061 release 검증을 시작한다.
이 별도 S2 채팅에서 아래 범위의 조립·검증·제출물 제작을 실행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md 순서로 읽고 실제 개정·역할·허용 범위를 보고한다.
workflow r4 적용. HEAD·dirty files·active jobs와 쓰기 주체를 확인한다.
다른 쓰기/학습 세션이 진행 중이면 공유 파일을 수정하거나 worker를 시작하지 않는다.
기존 미커밋 변경을 보존하고 과거 HEAD/manifest로 되돌리지 않는다.

필수 입력:
- docs/analysis/A034-e061-s0-review.md
- docs/analysis/A034-outputs/{entry,verification}.json
- docs/analysis/E061-outputs/{closeout,registration,exposure-ledger,review}.md
- docs/analysis/E061-outputs/{manifest,frozen-inputs,frozen-predictions-01,
  phase1-inputs-01,comparison,run-01-resources,source-review,environment-01}.json
- src/models/tied_content_heads.py 및 S1 manifest의 허용 의존 소스
- submissions/2026-09-19-E041/main.py, submissions/2026-09-09-E025/main.py
- submissions/SCORES.md, submissions/hosted-scores/2026-09-27.json
기존 E061-outputs/s2-handoff.ko.md는 S0 판단 이전 참고 초안이다.
이번 실행 범위는 이 확정 인계문이다.

목적:
S1 EXPLORATORY_SOURCE_QUALIFIED 후보를 고정한 채 조립·공식 패키지 검증을 마치고,
통과하면 사용자가 검토할 DEV ZIP과 사전 SCORES 판독표를 만든다.
새 모델 연구·실제 ERPIS 개선 증명·업로드·TEST 선택은 아니다.
후보는 UNHCR full head의 ordinary logits를 conditional logits로 공유한다.
CE/support/분모, 원래2config·seed0·split·학습/선택/refit·lambda minimum30/
zero fallback 및 renderer 규칙을 바꾸지 않는다. 별도 conditional Linear 제거의
난수 소비 차이도 기존 후보 일부다. UNICEF/WB는 E041 경로를 유지한다.

동결 소스:
src/models/tied_content_heads.py SHA256
f9449d41d30041f6e9714c7a25777965ec4d25cfa2563b018fb08c94dde20833
S1의 현재 소스·실행 복사본·의존 소스는 manifest로 식별한다.
A034의 status/log 추가는 정상 문서 변경이다. 소스 차이가 있으면 이유를 확인하고
해결 전 실행하지 않는다. 기존 production 파일·S1 기록·모델·snapshot을 수정하지 않는다.

허용 산출물:
- 새 scripts/assemble_e061.py, scripts/check_e061_release.py
- 필요한 새 tests/test_e061_assembly.py (조립에 새로 생기는 경계만)
- docs/analysis/E061-outputs/s2/ 아래 entry·사전 release 계약·검증·자원·노출·
  source/archive manifest·closeout·S0 인계
- submissions/YYYY-MM-DD-E061/ 및 같은 이름의 .zip
  날짜는 실제 제작일이며 업로드일로 주장하지 않는다. 기존 경로가 있으면 덮어쓰지 않는다.
- 해당 작업의 docs/status.md·docs/log.md 기록
docs/tree.md는 이번에도 보존하고 미반영 링크를 종료 기록에 남긴다.
기존 E061 실험/registration/manifest/성공한 S1 결과는 변경하지 않는다.

허용 데이터와 기존 결과 재사용:
기존 synthetic phase1 세 파일만 사용한다:
external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet
S1 frozen-inputs에 기록된 해시와 비교 후 TRAIN/DEV 역할만 사용한다.
모델에는 공식 sample_rows의 TRAIN 및 DEV GIVEN만 제공하며 DEV PREDICT는 가린다.
TEST/phase2·재생성·새 seed·실제 응답·VAF/SIPP/Adult·원천 key Parquet 접근은 금지한다.

S1 reference로 다음 9개 숫자 배열만 읽기/해시 확인할 수 있다:
docs/analysis/E061-outputs/vectors-01-{candidate,E041,E025}-{unicef,world_bank,unhcr}.npz
frozen-predictions-01 및 manifest의 해시, 소스·schema/config·분할·환경/CPU2 조건을
먼저 확인한다. numpy 로드는 allow_pickle=False; 임의 모델/예측 캐시 탐색은 금지한다.
조건이 맞으면 이미 동결된 source 후보·E041/E025 기준 벡터/점수를 재사용한다.
식별 불일치·파일 누락이면 STOP과 필요한 입력을 기록한다. S1 성공 실행이나
기준 모델을 자동 재학습해 맞추지 않는다. 같은 합성 DEV이며 새 독립 audit이 아니다.

실행 전 release 계약과 SCORES를 고정한다:
1. 단일 파일 조립 시 원래 _Net/_train/_train_on/tune_and_train과 후보 TiedNet/
   학습 함수를 명시적으로 구분한다. 이름 충돌·전역 덮어쓰기로 control 경로를 바꾸지 않는다.
   조립 입력 의존성과 결과 import를 검토하고 repo 경로 없이도 작동하게 만든다.
2. 조립 후보의 all3 raw vector를 S1 동결 source 후보와 비교한다.
   모든 원소 최대 절대 차이<=1e-10, 공식 shape/finite/nonnegative/positive-total
   계약 및 raw 합 오차<=1e-6. UNICEF/WB는 E041과<=1e-10.
   UNHCR은 E041 대비>1e-10 변화가 있어야 하며 실패 시 활성 강제 금지.
3. 기관별 clean E025 절대 skill 차이<=.002 및 candidate>=E041-.002를 확인한다.
   S1 결과는 두 기준보다 낮아 이 release 조건도 만족했지만 조립 확인을 대체하지 않는다.
   +.005 합성 개선을 새 필수 조건으로 추가하지 않는다. 실제 ERPIS 효과를 주장하지 않는다.
4. ZIP root/main.py, 허용 의존성·NOTICE/출처·선언, 금지 파일/외부 경로를 검토한다.
   official ZIP checker와 추출 패키지의 공식 score.py all3 phase1을 실행한다.
   조립 main과 추출 main의 바이트 동일성, all3 공식 결과와 고정 후보의 일치를 확인한다.
   공식 검증 결과를 좋은 값으로 대체하거나 결과에 맞춰 모델을 바꾸지 않는다.
5. 실제 추출 패키지의 startup/import/load/all3 전체 시간을 측정한다.
   기관별 별도 CLI라면 startup 포함 세 실행을 합산한다. 개별900초가 아니다.
   단일 파일 조립 PASS나 S1 함수 호출 PASS만으로 release PASS를 선언하지 않는다.

자원·실행 상한:
세션 wall120분, 모든 계산 worker 누적2400초, heavy worker1개.
CPU numerical threads2/GPU off, owned process-tree RSS 및 private/commitment 각각8GiB.
후보 조립 all3와 추출 패키지 all3는 각각 startup 포함 합산900초 이내.
기본은 조립3회+공식 추출패키지3회=full-stack6, neural18, metric16회 이내.
명확한 조립/검증 결함의 한정 수정에만 동일 누적 한도 안에서 추가 최대3 full-stack 허용:
전체 최대9 full-stack/27 neural/24 metric. 실패·fallback도 횟수와 비용에 포함한다.
새 경량 조립 tests 비용도 누적한다. S1의1098.523초·9/27/16회는 별도 역사로 승계하며
이번 S2 비용과 합산 보고한다. 추가 baseline fit·S1 재실행·새 학습 grid는 금지한다.
필요 비용이 상한을 넘으면 범위를 임의 확대하지 않고 STOP한다.
소유 worker만 감시/정지하며 측정 실패도 STOP. 다른 세션 프로세스를 종료하지 않는다.
CPU 검증을 hosted H100 비용 보장으로 표현하지 않는다.

사전 hosted 판독:
- 검증된 새 best: 후보 전체에 대한 유리한 noisy evidence로 S0 검토. 자동 채택 없음.
- Grand 동일/best update 없음: 효과 미해결, E061 parked, E041 유지.
- Grand 하락: 해당 실행의 adverse reading, E041 유지.
- 실패/timeout: 기술 실패, 통계적 열등으로 확대하지 않음.
- 제출 ID/bytes/판독 모순: 출처 확인 전 판단 보류.
기관별 공식 보고 값이 있으면 기록한다. Grand만으로 숨은 값·활성·정확 효과를 역산하지 않는다.
E060947705 Finished, Grand.6433333333 / UNICEF.52 / WB.49 / UNHCR.92는
E041과 같은 공개 보고 값이다. 원점수나 효과0의 증명이 아니며 parked 유지.
SCORES에는 준비일·실제 업로드일/ID·ZIP해시를 구분하고 미확인 값은 미확인으로 둔다.
계정/당일 slot은 확인된 것으로 가정하지 않는다. 이번 S2는 로그인·업로드하지 않는다.

종료:
모두 통과하면 RELEASE_QUALIFIED_FOR_USER_REVIEW, ZIP·SCORES·정확한 해시·공식3종
결과·parity·전체 자원·노출·남은 불확실성을 보고하고 S0로 인계한 뒤 멈춘다.
실패 시 원인·기존 결과·재개 입력/책임자/범위를 남긴다. 예비는30분 이내 실패 closeout뿐이며
전체120분 안에 포함한다. 다른 후보나 seed/head/threshold 탐색으로 넘어가지 않는다.

누적17999명/12339SSUID·A022 원래 역할·집계 노출을 승계한다.
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177 및 calibration1866 유지.
E041 incumbent/E025 fallback, E057/E060 parked, E058 STOP/E059 STOP_SELECTION,
모든 STOP/HOLD·A_half 비승격·A018 TEST 사용자 미확정·S3 중단을 보존한다.
업로드·commit/push·S3/TEST 선택·다른 모델 제작은 허용하지 않는다.
```
