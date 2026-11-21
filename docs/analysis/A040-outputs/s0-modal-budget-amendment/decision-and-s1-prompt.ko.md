# A040 — 비용 관리 방식 변경과 S1 재개

2026-10-03 KST. S0 문서 작업. 기준 HEAD:
`a43f4379ec78dbc2de260463eef67bb1d567d7e1`.

사용자는 준비비$1을 계획 예산으로 바꾸고 전체$5를 목표로 사용량·시간·종료를
관리하되 정확한$5 이하 보장은 하지 않는 제안에 **“그냥 그렇게 진행하자.”**라고
동의했다. 이번 변경은 그 비용 계약에만 적용한다. 계정 한도 상향, 현금 지출,
모델/선택 기준 변경, 추가 실행 또는 S0의 S1 전환을 뜻하지 않는다.

## 변경된 판단

- 준비$1·전체$5는 계획 예산이다. 모든 builder/pull/snapshot/retry/cancel
  비용의 엄밀한 최악 상한을 사전에 증명해야 한다는 요구를 해제한다.
- 알고 있는 가격·자원·예상 소요를 기록하고, 실시간 추정/게시 사용량과
  시간 제한으로 관리한다. 청구 지연·취소 후 반영으로 계획액 초과 가능성은
  사용자에게 설명됐으며, 이를 무제한 사용이나 의도적 초과 허가로 해석하지 않는다.
- 현금 지출 권한$0, spend limit$0·기존 usage limit 유지. 설정 변경 없음.
  기존 사용자 설정 확인 보고는 사용자 근거로 승계한다. S0가 live 검증한
  것으로 쓰지 않는다. 정상 API 확인이 거부됐다는 이유만으로 재로그인이나
  같은 예산 조회를 반복하지 않는다. 실제 설정 모순/잔액 부족은 별도 차단이다.
- 공급사 문의는 필수 아님. 미발송 초안 보존; 새 문의/동일 검색 없이 재개 가능.
  과거 BUILD_BUDGET_CONTROL_UNRESOLVED는 당시 계약의 역사적 판정으로 남긴다.
  비용 조건 변경은 Linux 경계/전체 경로 PASS가 아니다.

기존 S1 누적2295.2633125초를 승계한다. 남은 준비 약21분44초/전체81분44초
안에서 새 재개 범위를 준비21분/전체81분으로 정한다. 로그인 대기 등 세션 간
시간은 별도 기록한다. 과학 allowance는 미사용이며 추가 횟수로 바꾸지 않는다.
주력은 기존 고정 경로 기술 검증, 예비는 정확한 실패/미완료 기록과 종료뿐이다.

## 기존 S1에 그대로 전달할 프롬프트

```text
SimulacraBench / HSCC S1 — A040 Modal 준비 재개2 및 고정 전체 경로 검증.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench.
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1. 기존 dirty 보존.

AGENTS → CLAUDE → status → log 최신3개 → workflow를 읽고 역할/범위를 보고한다.
다음을 읽는다:
- docs/analysis/A040-outputs/s0-modal-budget-amendment/decision-and-s1-prompt.ko.md
- docs/analysis/A040-outputs/modal-full-path1-resume1/의 closeout.md,
  build-control.md, account-read.json, cost-ledger.json, verification.json, entry.json
- docs/analysis/A040-outputs/s0-modal-plan/s1-modal-full-path.ko.md
- 원래 modal-full-path1의 allowlist.json/source-input-image-manifest.json과
  원래 전체 경로 registration/manifest 등 위 인계가 지정한 자료.

이 지시는 기존 S1에서 준비·원격 단일 검증을 이어갈 실행 지시다.
비용 부분은 이 새 문서가 과거의 엄밀한USD1/5 보장·공급사 답변 요구에 우선한다.
그 밖의 과학/데이터/자원/종료/역할 경계는 원래 인계를 그대로 적용한다.
S0로 예산 보장을 다시 문의하거나 같은 build-control 조사만 반복하지 않는다.

변경된 비용 관리:
1. 준비USD1·총USD5는 계획 예산. 정확한 최악 청구액 증명은 실행 전제가 아니다.
   원래USD1 종료/기타 여유를 가급적 확보한다. 현금 지출 허용은 여전히USD0.
   계정 spend/usage limit 상향·플랜/카드/크레딧 구매·다른 공급사 전환 금지.
2. 기존 인증 joon56/main 및 SDK1.6.0/staging을 재사용한다. 재로그인/재설치
   요구 금지(실제 인증 만료/오류는 별도). 이전 사용자 credits30/spend0/usage30
   확인 보고를 승계하되 현재 live 검증값과 구분한다. 정상 계정·청구 읽기로
   확인 가능한 값만 갱신한다. 예산 RPC PermissionDenied 자체는 재차단 사유가
   아니다. 사용자 근거를 API 검증으로 꾸미지 않는다. 설정 모순/현금 청구 위험이
   실제로 확인되거나 필요한 크레딧이 부족하면 실행하지 말고 그 사실만 보고한다.
3. 간단한 사전 비용 추정표와 실행별 시작/종료 기록을 만든다. 전체 추정이
   목표$5 안에 들어오는 준비 경로를 기존 검토한 경로 중 선택한다.
   보이지 않는 과금은0으로 쓰지 말고 미확정 overhead로 기재한다.
   새 코드/SDK 조사나 가격 확인은 구현에 필요한 부분만 수행한다.
4. build/app ID가 나오면 즉시 기록. 준비는 하나의 명시적 이미지 recipe로,
   클라이언트 차원의 재빌드/force_build/반복 설치 시도 없이 수행한다.
   provider 내부 재시도는 관측 가능한 만큼 기록하고 이상 지속 시 취소한다.
   빌드 단계가 여러 개인 것은 별도 후보 탐색이 아니다.
5. 원격 작업 중 사용량/추정을 주기적으로(가능하면60초 이내) 확인한다.
   게시된 작업 사용량과 자원시간 추정 중 큰 값을 관리값으로 삼되, 플랫폼
   전체 사용량과 작업 귀속을 구분한다. 시작 전 계정 baseline을 기록한다.
   추정/관측 누적$4에 이르면 새 비용 작업을 시작하지 않고 정상 종료를 시작해
   약$1의 회수/종료 여유를 둔다. 다음 단계가 그 여유를 침범할 것으로 보이면
   시작하지 않는다. 숫자가 늦게 반영돼도 timeout/로컬 비용 추정을 유지한다.
   $5를 넘긴 청구가 나중에 확인되면 숨기지 말고 즉시 기록·S0 반환한다.
   사용량 게시 지연만으로 무기한 polling하거나 정확한$5 이하를 주장하지 않는다.
6. client timeout/오류만으로 원격 종료됐다고 보지 않는다. 정확한 owned ID의
   취소/종료와 terminal 상태를 확인하고 게시 청구/미확정 항목을 구분한다.
   연결 단절 때는 기존 ID 조회·정리만 허용, 새 요청 재발행 금지.
   필요한 사용자 수동 조작은 정확한 ID/화면 경로와 함께 안내한다.

남은 범위:
- 이번 준비<=21분/전체<=81분. 기존2295.2633125초와 누적 기록하고 시작 시
  새 절대 deadline 동결. 과거 deadline/결과는 수정하지 않는다. 범위 안에
  끝낼 수 없으면 INCOMPLETE로 종료하며 시간을 자동 연장하지 않는다.
- SDK/staging 재사용. 과거 자료를 덮지 말고 새 modal-full-path1-resume2/
  문서·tmp 경로 사용. 입력 전송 직전 허용112파일 identity를 필요한 범위에서
  확인한다. 저장소/사용자 HOME 통째 전송 금지. 다른 응답/키/cache/VAF 금지.
- H100!1개, 동시heavy1, 컨테이너<=2400초. 원래 CPU2/model threads2,
  physical request/cap1 및15258MiB hard memory, native offline, duplicate-launch
  방지 계약 유지. 새 모델 없는 경계 검사 누적60초. 원래 성공 suite 반복 금지.
- Linux 경로/watchdog/계측/환경 이식과 사전 source/input/image freeze 완료 후
  새 target reference1회<=900초, PASS이면 candidate1회<=900초.
  두 실행 모두 import/load/all3/검증/출력 포함. 추가 S0 확인 없이 수행 가능.
  첫 예상 밖 오류/자원·비용·시간 제한이면 STOP, 수정 후 재실행 없음.
- 원래 3개 fake 입력·공개 checkpoint·E041 source·TabICL source와 정책 유지.
  F/S/E·전체213heads/context/refit·alpha/guard/floor/seed/tolerance 변경 금지.
  전체189649vectors, controls/inactive/fallback parity, 최종 state/weight hash,
  자연/engineering alpha.25 경로 등 원래 미완료 검증을 그대로 완료한다.

결과와 산출물:
원래 H100_FULL_PATH_PASS/FAIL, RESOURCE_LIMIT, BLOCKED_SPECIFIC_INPUT,
INCOMPLETE 판독을 적용한다. 과거 비용 보장 미해결을 해결됐다고 소급하지 않는다.
새 entry/변경 비용 정책/추정·게시 비용 ledger, diff/freeze/경계 검증,
reference/candidate events/resources/results, remote ID·종료 확인,
exposure/verification/closeout/s0-handoff와 status/log 최소 갱신.
실행 전 중단이면 NOT_RUN 그대로. H100 성공도 실제 효과·hosted/release PASS 아님.

S2 제작/ZIP/checker/official release score/업로드/commit/push/tree/S3/TEST 선택 금지.
모든 과거 STOP/HOLD와 A039·E041 incumbent/E025 fallback·E057/E060/E061 parked,
17999/12339·A022 역할·E059 소비oracle/selection과 보호audit/calibration 유지.
A_half 비승격/A018 사용자 미확정/S3 중단/S2 후보 없음. 항상 S0로 결과 반환.
```

## S0 작업 내역

2026-10-03 사용자 동의에 따른 사전 비용 정책 변경. 워크플로우 r4의 S0 경계는
유지한다. 실제 ordered read112259, HEAD/dirty/job 및 기존 판단/장부 읽기dbcd9c.
워크플로우 SHA256과 문서 보존 검사는 verification.json에 기록한다.
원격 작업/계정 접근/설치/입력·checkpoint 열람·해시/모델·검증 실행/문의 발송0.
기존 파일은 수정하지 않고 새 문서와 status/log만 갱신한다. 기존 named process
조회는 비어 있었으며, 호스트/계정 전체 작업 부재를 증명하지 않는다.
