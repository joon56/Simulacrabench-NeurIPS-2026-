# 다음 세션 제목

**HSCC · S1 · UNHCR 전체·조건부 출력층 공유 후보 검증**

아래 프롬프트를 **별도 S1 채팅**에 붙여 넣는다. 이 파일 작성은 실행이 아니며,
작성한 S0 채팅이 이를 발견하거나 다시 읽어도 직접 실행하지 않는다.

```text
SimulacraBench / HSCC S1 연구 세션을 시작한다.
이 별도 S1 채팅에서 아래 범위의 구현·합성 기술 검증을 실행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: 1d223340d4e1fa3993b411dc5daafab9cb37d0cd

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md 순서로 읽고 workflow r4의 실제 개정·역할·허용 범위를 보고한다.
HEAD·dirty files·active jobs를 확인한다. 다른 쓰기/학습 세션과 겹치면 실행하지
않고 상태를 보고한다. 이미 있는 변경·모델·제출 snapshot은 보존한다.

필수 입력:
- docs/analysis/A033-dev-handoff-and-role-repair.md
- docs/analysis/A033-outputs/{candidate-inputs,verification}.json
- docs/analysis/A033-outputs/codabench-score-access.ko.md
- docs/experiments/E012-shared-trunk.md, E029-seed-temp.md,
  E041-supervised-retrieval.md, E056-conditional-leaf-content.md,
  E060-content-target-retrieval.md
- src/models/shared_trunk.py, supervised_retrieval.py, link_sharp.py, hh_cap.py
- submissions/2026-09-19-E041/main.py 및 submissions/2026-09-09-E025/main.py
  위 두 파일은 기준 소스로 읽으며 수정하지 않는다.

소스 식별은 HEAD와 candidate-inputs.json의26개 허용 문서·소스 해시를 사용한다.
workflow/status/log가 정상적으로 갱신된 경우 경위를 확인하며 과거 해시에 맞춰
되돌리지 않는다. 고정 모델 입력이 바뀌었으면 효과 실행 전 차이를 보고한다.
E061·tied_content_heads 관련 이름 충돌부터 확인한다. 사용 중이면 덮어쓰거나
자동 재번호 실행하지 않는다. E061은 이번에 처음 등록할 예정 번호이며 S0에서
만든 모델/실험 기록이 아니다.

목적/연구 유형:
한 개의 UNHCR-only 탐색 DEV 후보를 구현하고 S2 인계 자격을 판단한다.
독립 실증 효과 증명이나 TEST 선택이 아니다. VAF 승인을 기다리지 않아도
가능한 기존 합성 채널의 기술·회귀·비용 검증이다. 합성의 개선/비개선은 실제
ERPIS 효과를 확정하지 않는다. 보호된 실제 proxy/audit로 후보를 구제하지 않는다.

기존 작업과의 차이/가설:
E012/E041은 gated item의 full softmax head와 asked-only conditional head를
별도로 학습한다. 같은 GIVEN에서 두 head의 일반 응답 상대비가 다를 수 있다.
후보는 기존 full head의 일반 응답 logits를 conditional head로도 사용한다.
별도 conditional Linear의 자유도를 제거하는 parameter tying이 개입이다.
새 conditional 모델이라는 이름 자체는 새로움이 아니다.
E056/E057의 독립 tree 추가, E060의 retrieval fitting target 변경,
A023의 selector 목적함수, E029의 seed/temperature 변경을 재실행하지 않는다.
이 불일치가 실제 손해라는 관측은 아직 없다. 공유가 유연성을 줄여 손해를
낼 수도 있으므로 버그 수정이나 개선 보장으로 보고하지 않는다.

고정 개입:
1. K개 ordinary outcome+sentinel의 full logits z에 대해 conditional logits는
   같은 z의 ordinary K개 요소다. softmax(z_ordinary)를 안정적으로 계산한다.
   작은 1-p_sentinel로 확률을 직접 나누지 않는다. ordinary/sentinel 순서는
   schema option 의미로 검증하며 임의 순서를 가정하지 않는다.
2. 기존 full CE+asked-only conditional CE의 support·가중치·분모를 유지한다.
   full/conditional head가 같은 parameter에 gradient를 전달하도록만 바꾼다.
   conditional loss 삭제, sentinel 재가중, auxiliary 계수·temperature 추가 금지.
3. UNHCR gated neural heads에만 tying. 일반 head 구조는 유지하되 shared trunk
   학습 때문에 UNHCR 전체213문항 수치가 바뀔 수 있음을 인정한다.
   sentinel은 계속 학습된 범주다. schema gate를 정확한 관측으로 강제하지 않는다.
4. 기존 configs (64,2,0.0)/(128,2,0.1), torch seed0, 학습률/정규화/epoch/patience,
   내부 split, ladder, blend grid, E041 donor/metric/selector, lambda minimum30/
   zero fallback, recursive renderer의 알고리즘은 그대로 둔다.
   new base에 따라 원래 절차가 다시 정하는 lambda 값은 바뀔 수 있다.
   전체 절차 비교이며 frozen-lambda 또는 D-P 통제 비교라고 부르지 않는다.
5. UNICEF/WB는 원래 E041 control 경로로 위임한다. 별도 모델 선택·seed·정규화
   변경을 이 두 기관에 적용하지 않는다. tied/untied 모델 간 새 선택 grid도 없다.

허용 파일/산출물:
- 새 src/models/tied_content_heads.py
- 새 tests/test_tied_content_heads.py
- 새 scripts/check_e061_tied_heads.py (연구 검증만, assembly/ZIP 기능 없음)
- 새 docs/experiments/E061-tied-content-heads.md
- 새 docs/analysis/E061-outputs/ 아래 registration, entry, test/review 결과,
  비교 수치·resource log·exposure-ledger·manifest·closeout·필요 시 s2-handoff.ko.md
- docs/status.md와 docs/log.md의 해당 작업 기록.
기존 shared_trunk 등 production 파일은 수정하지 않는다. 새 모듈은 필요한
최소 구현을 분리하고 전역 monkeypatch로 기준 모델을 바꾸지 않는다. 이 범위로
불가능하면 필요한 차이를 보고하고 중단한다. docs/tree.md는 기존 dirty 변경을
보존하며 이번에는 수정/재생성하지 않고 미반영 E061 링크를 종료 기록에 남긴다.

허용 데이터/실행 경계:
공개 schema/config/source와 이미 사용한 다음 synthetic Parquet3개만 허용한다:
external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet
이3개는 합성 기술 검증 입력이며 실제 응답 데이터가 아니다. S0는 이번에 읽거나
재해시하지 않았다. S1에서 기존 E057 preflight의 출처/해시와 실제 지정 파일을
검증한 뒤 사용한다. 누락/불일치면 자동 다운로드·재생성하지 않는다.
phase1 공식 sample_rows 의미를 유지: 모델에는 TRAIN이 보이고 DEV의 PREDICT는
가린다. DEV truth는 후보 고정 후 외부 검사에만 쓴다. 재사용된 합성 DEV를 새
독립 audit으로 부르지 않는다. phase2/TEST 평가, 새 synthetic seed 탐색 금지.
새 불변조건용 작은 임의 tensor/행 fixture는 허용하되 실증 효과 근거로 쓰지 않는다.
기존 model/prediction pickle 캐시는 읽지 않는다. 필요 기준은 고정 source로
범위 내 실행한다. src/eval/runner의 자동 생성 경로나 기존 check_e060의
cache/assembly/ZIP 경로를 통째로 호출하지 않는다.

실행 전 registration을 저장한다. 유효한 ERPIS 효과 oracle이 현재 없음을
명시한다. 공개 메타데이터·합성 정답의 oracle이 실제 ERPIS gain을 상한으로
묶는다고 주장하지 않는다. A023 실증 조건을 낮추거나 다른 이름으로 우회하지 않는다.

검증·종료 기준(수치를 보기 전에 고정):
A. 새 의미 있는 tests: full/conditional 확률 항등식, schema option 대응,
   극단 logits 안정성, 동일 parameter gradient, asked mask/CE 분모 보존,
   held-out PREDICT 접근 금지 및 control dispatch. 성공한 기존 fixture 반복 금지.
   neural 항등식은 float 오차1e-6 이내; 최종 ladder/gate mixture의 항등식으로
   확대하지 않는다. test-only marker/tensor를 실제 feature로 넣지 않는다.
B. 후보와 두 기준(E041/E025)을 지정 합성3종 phase1에서 각각 최대 한 번 검증.
   official score.py의 check/floored/score 의미를 사용하되 파일 실행·환경 설치·
   패키징은 하지 않는다. 입력/후보를 먼저 동결하고 모든 후보 벡터 생성 후 점수를
   읽는다. 결과를 보고 모델/seed/threshold를 바꾸지 않는다.
C. 모든 vector가 공식 shape/finite/nonnegative/normalization 계약을 만족.
   UNICEF/WB candidate-E041 최대 절대 차이<=1e-10. UNHCR 실제 최종 벡터 중
   차이>1e-10인 것이 최소1개 있어야 한다. 전부 같으면 NO_OP로 종료, 강제 활성 금지.
D. 기관별 candidate skill >= E025 skill-.002 및 >= E041 skill-.002.
   이는 사전 탐색 release 회귀 제한이며 통계 유의성/개선 증명이 아니다.
   합성에서 +.005 개선을 S2 탐색의 필수 조건으로 새로 요구하지 않는다.
E. 전체3종 candidate 호출의 실제 누적 wall<=900초, 전체 owned process-tree
   RSS 및 private/commitment 각각<=8GiB. CPU numerical threads2, GPU 사용 없음.
   측정하지 못하면 resource-qualified라고 주장하지 않는다. 로컬 시간은 hosted
   H100 보장이 아니다. S2가 최종 공식3종 및 패키지 비용을 별도로 확인한다.
F. 위 실패/초과/데이터 충돌이면 범위 내 STOP/TECHNICAL_FAILURE/NO_OP 기록.
   회귀 실패 뒤 tying 강도·head 목록·학습 손실·threshold·seed를 조절하지 않는다.
   통과해도 EXPLORATORY_SOURCE_QUALIFIED까지만 선언한다. E041 채택 유지.

자원 상한:
전체 S1 wall120분, 계산 worker 누적 wall1800초, 위 memory/thread 제한.
full-stack predict 최대9회(E025/E041/후보 각각3기관), neural training 호출 최대27회
(각 호출 원래2config fit+1refit); 실제 호출 수/epoch/metric optimizer와 전체 시간을
기록한다. helper 실행에 숨은 추가 fit을 세지 않는 보고 금지. 새로운 optimizer
grid 없음. 경량 gradient 단위 검증은 별도 횟수 기록. 한 heavy worker만 실행한다.
관련 없는 다른 세션 프로세스는 종료하지 않는다. 재실행은 명확한 기술 결함의
수정만 원인과 노출을 기록하고 같은 상한 안에서 허용; 과학적 실패 구제 금지.

S2 인계 시 사전 hosted 판독:
- 새 best가 확인되면 전체 후보의 유리한 noisy evidence로 S0 검토에 전달.
- Grand 동일/best update 없음이면 효과 미해결·후보 parked, E041 유지.
- Grand 하락이면 해당 실행의 adverse reading, E041 유지.
- 실패/timeout은 technical arm; 통계적 열등 판정으로 확대하지 않는다.
기관별 점수가 없을 수 있음을 전제로 한다. API에서 공식 제공 점수를 확인해도
Grand에서 숨겨진 기관 점수·활성 상태·정확한 효과를 역산하지 않는다.
동일 정책 반복 제출·미세 조정으로 판독을 구제하지 않는다.

정당한 예비 작업:
주력 중단 시30분 이내 실패 원인·재개 조건·보존 확인 closeout만 작성한다.
또 다른 모델, VAF 재검색, E056/E058/E059/E060 재실행으로 넘어가지 않는다.

보존/금지:
VAF 승인 요청은 사용자 제출 완료·승인 대기. VAF 응답 다운로드/열람 금지.
실제 GIVEN/PREDICT·SIPP/Adult/원천 key Parquet·기존 model cache 접근/재해시 금지.
누적17999명/12339SSUID 사용·집계 노출·A022 원래 역할을 승계한다.
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177와 과거calibration1866
유지. A022 잔여8700/4975는 새 데이터나 audit이 아니다.
E041 incumbent/E025 fallback, E057/E060 parked, 모든 STOP/HOLD,
E058 STOP/E059 STOP_SELECTION, A_half 비승격 유지. A018 TEST 사용자 미확정/S3중단.
E061 source 자격 판정 전 S2 후보 없음. 기존 제출 snapshot·ZIP·tree 수정,
assembly/공식 CLI release/ZIP 제작·업로드·commit/push·S2/S3실행·TEST선택 금지.
S2 인계문을 작성한 뒤 종료하며, 이 S1에서 그 인계문을 실행하지 않는다.
```
