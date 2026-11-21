# E061 S2 인계 초안 — S0 검토·이관 판단 대기

**EXPLORATORY_SOURCE_QUALIFIED.** 우선 [S0 검토](s0-handoff.ko.md)에 인계한다.
이 문서는 S0가 S2 이관을 결정할 경우 사용할 release 검증 참고 초안이다.
이 문서를 작성·읽는 것만으로 S2 실행·업로드·commit/push를 허가하지 않는다.
S1은 여기서 종료한다. E041 incumbent 유지, 실제 ERPIS 개선·TEST 채택 미확정.

## 시작 입력과 식별

AGENTS → CLAUDE → status → log 최신3개 → 현재 workflow 순서로 실제 읽고
개정/역할/허용 범위를 보고한다. S1은 workflow2026-09-27-r4를 적용했다.
종료 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; E061 변경은 미커밋 상태다.
진입 HEAD는 `1d223340d4e1fa3993b411dc5daafab9cb37d0cd`였다. S0가 점수 문서36개만
커밋했고 push는 사용자 확인이다. E061 종료 동일성 검사에서 뒤늦게 발견해 기록을
보류했으며, 사용자 보충 지시 후 문서만 마무리했다. 소스·판정 변경이나 재실험 없음.
현재 HEAD·dirty files·active jobs와 [manifest](manifest.json)의 허용 소스/문서
해시로 식별한다. 과거 해시에 맞춰 사용자 변경을 되돌리지 않는다.

필수: [closeout](closeout.md), [등록](registration.md),
[frozen-inputs](frozen-inputs.json), [comparison](comparison.json),
[resource log](run-01-resources.json), [exposure](exposure-ledger.md),
`src/models/tied_content_heads.py`, `tests/test_tied_content_heads.py`,
`scripts/check_e061_tied_heads.py`와 manifest가 식별한 원래 의존 소스.
원래 E041/E025 submission main은 변경 금지 기준이다.

새 모듈 SHA256:
`f9449d41d30041f6e9714c7a25777965ec4d25cfa2563b018fb08c94dde20833`.
S1 실행 코드 복사본도 같은 폴더에 보존했다. 기존 pickle cache는 읽지 않았다.

## 변경과 확인한 범위

UNHCR gated neural head156개의 conditional logits를 같은 full head의 ordinary
logits에 연결했다. CE/support/분모·원래2config·seed0·split·선택/refit 규칙 유지.
원래 tune_fn 연결점 사용, production 파일과 전역 model 함수 수정 없음.
UNICEF/WB는 원래 E041 경로. UNHCR 전체213개 출력은 trunk·lambda 변화 가능.
신규 neural/loss/head grid 없음. 별도 conditional Linear 제거에 따른 난수
소비 차이도 사전 기록했다. 완전한 절차 비교이며 frozen-lambda/D-P가 아니다.

- 집중 tests9 PASS; 기존 train/tune AST는 공유 연결 부분 외 동일.
- 합성3종 phase1, 각 model/instrument1회: full-stack9, neural27, metric16회.
- 모든568947 벡터 공식 계약 PASS. UNICEF/WB candidate-E041 차이0.
- UNHCR132225/132273 벡터 변화, 최대 entry 차이.164548426867.
- UNHCR skill: E061 .562391878130 / E041 .562462728858 / E025 .562948873705.
  두 기준 대비-.000070850727 / -.000556995575, 모두 사전-.002 한도 통과.
  다른 기관 skill은 양쪽 기준과 동일. 합성 개선은 관측되지 않았다.
- 후보 import/startup/준비/all3 포함340.093초; 전체 worker+tests1098.523초.
  보수적 process-tree RSS1.991GiB / commitment1.514GiB. CPU numerical threads2,
  GPU 없음. 로컬 실행비용이며 hosted H100 보장은 아니다.
- 모든 후보·기준 벡터를 동결한 뒤에만 합성 DEV 점수를 계산했다.
  반복 사용한 synthetic DEV는 engineering 자료이며 새 audit이 아니다.

## S2에서 아직 필요한 검증

1. 현재 입력·코드·환경·분할 해시 확인 후 source와 조립 산출물의 전체3종
   raw vector parity를 검증한다. 새 tying 강도/head/seed/손실/grid는 금지.
   조립하면서 `_train`, `_train_on`, `tune_and_train`, `_Net`의 이름 충돌로
   control 경로를 덮어쓰지 않도록 원래/후보 연결을 분리해야 한다.
2. 새 E061 산출물만 준비한다. 기존 E041/E025와 다른 snapshot·ZIP은 보존한다.
   ZIP checker, 공식 all3 phase1 CLI, 실제 패키지 import/all3 전체 runtime·
   메모리를 별도로 검증한다. S1의 공식 함수 호출 PASS는 이를 대체하지 않는다.
3. clean E025 및 E041 기관별-.002 회귀 정책, UNICEF/WB raw parity<=1e-10,
   UNHCR nonidentity를 유지한다. S1 기준 벡터를 재사용하려면 지정 산출물의
   source/data/split/environment/hash 일치를 검증한다. 모델·seed 재탐색 금지.
4. 업로드 전 SCORES 판독표, 정확한 source/archive hash, 예정 일자와 실제
   업로드 시각/ID 구분, 사용 가능한 공식 점수 필드와 한계를 기록한다.
   실제 업로드와 commit/push는 별도 사용자 권한 없이는 수행하지 않는다.
5. S2 자원 한도·감시·STOP을 별도 등록한다. S1 성공 실행을 자동 재실행하거나
   S1 9/27회 한도를 새 세션 이름으로 숨겨 늘린 것으로 보고하지 않는다.
   새 release 실행 비용은 별도 명시하고 전체 개발 비용 이력을 승계한다.

| 향후 공식 판독 | 행동 |
|---|---|
| 새 best 확인 | 후보 전체에 대한 유리한 noisy evidence로 S0 검토; 자동 채택 금지 |
| Grand 동일 / best update 없음 | 효과 미해결, E061 parked, E041 유지 |
| Grand 하락 | 해당 실행의 adverse reading, E041 유지 |
| 실패 / timeout | 기술 실패 처리; 통계적 열등으로 확대 금지 |
| 제출 ID/bytes/판독 모순 | provenance부터 확인; 정확한 효과를 추정하지 않음 |

S0의 [새 점수 기록](../../../submissions/SCORES.md)에서 E060 ID947705 Finished,
Grand0.6433333333 / UNICEF0.52 / WB0.49 / UNHCR0.92 확인. 모두 E041과 같은
공개 보고 값이며 best 갱신 없음. E060 parked·효과 미해결 유지. 이 값은 노이즈·
반올림 이전 원점수가 아니며 E061의 후보·기준·판독표를 변경하는 근거로 쓰지 않았다.
업로드 bytes 동일성은 여전히 미확인이다. 향후 E061 기관별 점수 제공 여부는
실제 보고에서 확인한다. 본인 페이지에 공식 제공된 값만 기록하며 Grand로
숨은 기관 점수·활성 상태를 역산하지 않는다. 동일 정책 반복 제출이나 미세 조정으로
판독을 구제하지 않는다. 실제 ERPIS 효과 oracle/독립 실증/TEST 근거는 여전히 없다.

## 보존

VAF 승인 대기, 응답 접근 금지. 실제 GIVEN/PREDICT·SIPP/Adult/key Parquet·
기존 모델 cache 접근/재해시 금지. 누적17999명/12339SSUID, 원래 A022 역할,
E059 소비 oracle/selection·보호 audit/calibration 등 전체 노출 이력을 승계한다.
E041 incumbent/E025 fallback, E057/E060 parked, E058 STOP/E059 STOP_SELECTION,
기존 모든 STOP/HOLD, A_half 비승격 유지. A018 TEST 사용자 미확정, S3 중단.
S1은 docs/tree.md를 수정하지 않았으므로 E061 tree 링크는 미반영이다.
S1 commit/push·ZIP·upload0. 현재 연구 worker 없음. S0가 결과 검토 후 S2 이관
여부를 판단한다. 이관 전 S2를 시작하지 않으며, 이후에도 명시된 범위만 실행한다.
