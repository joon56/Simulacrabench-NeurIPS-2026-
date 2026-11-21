# E063 S0 — 동일 고정 ZIP의 DEV 탐색 제출 권고

2026-10-10 KST. **RECOMMEND_ONE_USER_DEV_SUBMISSION**.
S2의 **RELEASE_QUALIFIED_FOR_USER_REVIEW**를 문서 검토 범위에서 수용한다.
E063은 parked, E041 incumbent/E025 fallback 유지. 실제 업로드·DEV 채택·TEST 선택은 별개다.

## 판단

**같은 ZIP을 사용자 계정의 사용 가능한 Development slot에서 한 번 제출할 것을 권고한다.**
추가 로컬 학습·성공 검증·재조립을 요구할 새 결함은 이번 기록에서 확인되지 않았다.
제출 전 계정/phase/현재 slot은 사용자가 확인한다. S0는 조회하거나 업로드하지 않았다.

목표 기전은 original K32 안에서 query round에 따라 GIVEN 거리 가중치를 달리하는 것이다.
같은 단일 정책이 source/assembly/extracted 전체189649 raw에서 보존됐고,
UNICEF/WB exact controls, UNHCR46405 변화/lambda37 변화/자연7/8 활성도 유지됐다.
따라서 이 파일의 hosted 결과는 이 고정 전체 절차의 우선순위를 바꿀 수 있다.
round metric만의 인과효과나 hidden round별 효과를 분리하는 실험은 아니다.

반대 근거도 남는다. 합성 UNHCR +.0000175789는 매우 작고16개 section×wave 중8개는 하락했다.
노출된 synthetic, 기존 proxy/selection 및 in-sample base/replay, 독립 audit 부재 때문에
실제 ERPIS 이득·정밀도·예상 Grand를 추정할 수 없다. E025 대비 합성-.000468566도 보존한다.
기술적으로 작동한다는 사실만으로 효능을 인정하지 않는다.

그럼에도 원래 두 기관별-.002 기준·공식 전체 실행·동일성 검증이 모두 충족됐고,
기전이 실제 패키지에서 바뀌거나 사라지지 않았다는 근거가 있다. 제한된 공개 판독을
고정 정책 한 번의 다음 결정에 쓰는 범위는 타당하다. 빈 slot/이미 쓴 비용이 근거는 아니다.
새로 드는 비용은 사용자 제출·결과 확인과 DEV 관측1회다. 실제 hosted 시간/성능과
그 기회비용의 수치 예측은 없다. 다른 준비된 후보보다 전역 최선이라는 주장도 하지 않는다.

동점이면 효과0으로 단정하지 않고 이 고정 정책의 추가 우선순위를 낮춘다.
하락이면 해당 실행에 불리한 관측으로 유지한다. 둘 모두 동일정책 재제출이나
seed/head/threshold 구제 없이 종료한다. 상승일 때만 다음 S0에서 채택 근거를 검토한다.
제출하지 않거나 slot이 없으면 parked 유지가 예비안이며 다른 실험을 자동 시작하지 않는다.

## release 근거와 E025 보완 수용

[종료](../s2/closeout.md), [검증](../s2/verification.json), [비용](../s2/cost-time-ledger.json),
[보완](../s2/repair-record.md), [identity](../s2/baseline-identity-supplement.json),
[사전 판독표](../../../../submissions/2026-10-09-E063/SCORES.md)를 대조했다.

- 조립465.731014초, official phase1 all3 공유701.724240초/900, checker PASS.
  clean E025/E041 원래 raw를 재사용했고 baseline fit0. S2 계산1214.583438초/3600,
 6pipeline/18neural/16metric; S1 포함1969.135137초. 성공 source/suite 반복 없음.
- RSS/private 관측2.286743/2.468193GiB, 최대 실제 sample gap.120082800초.
  로컬 CPU2/GPU0 결과이며 연속 메모리 상한·hosted H100/의존성/900초 보장은 아니다.
- 최초 current-byte E025 hash 확인은 누락됐다. 기존 raw provenance는 있었고
  E025는 후보 실행 의존성이 아니다. 14:46:22.662100Z에 지정 해시가 확인됐으며,
  assembly 시작 후지만 evaluator/ZIP/official 이전이다. 별도 보완 동결·후속 확인도 있다.
  이는 원래 순서상의 결함을 없애지 않지만 후보·기준·기준값을 결과에 맞춰 변경한
  근거는 아니다. 해당 한계를 남기고 최종 qualification을 수용한다. 재실행은 요구하지 않는다.
- S2 읽기는 chunk와 영수증이 있는 session-reported 근거로 분류한다.
  이번 S0 실제 읽기와 구별하며 다른 채팅 전체 준수를 인증하지 않는다.

현재 허용 문서·소스29개는 저장된 식별과 일치했고 final-receipt는 별도 현재 해시를 기록했다.
S2 manifest/verification의 종료 영수증 해시 연결도 일치한다.
ZIP/Parquet/NPZ/cache는 이번 S0가 읽거나 재해시하지 않았다.

## 사용자에게 전달할 동일 준비본

- 파일: `submissions/2026-10-09-E063.zip`
- S2 기록 bytes: **15,720**
- S2 기록 SHA256: `5469b5374f6fb3745cabf64071183ed3de5bbe240ea4f18c034049d560d532d9`
- 제작: 2026-10-09 23:51:00.484781 KST. 종료일10월10일과 구분.
  파일명 날짜를 오늘로 바꾸거나 다시 만들 필요 없다.
- 현재 업로드 ID/시각/remote bytes/계정/slot/hosted 결과: 미확정.

사용자 제출 후 JSON/결과를 **기존 E063 S2**에 전달한다.
[결과 기록용 완성 프롬프트](s2-result-handoff.ko.md)는 그때 사용할 문서이며 현재 실행 지시가 아니다.
원문/API 공개 문자열과 phase/status/ID/filename/출처를 기록하고,
원격 bytes는 제공된 증거가 없으면 미확정으로 둔다. created_when을 독립 업로드 완료 시각으로 쓰지 않는다.

비교 기준 E041 ID933094, 공개 Grand .6433333333 / UNICEF .52 / WB .49 / UNHCR .92.
UNHCR+Grand 상승/controls동일=favorable noisy, 동점=UNRESOLVED,
하락=해당 실행 adverse, 반대방향/controls변화=mixed도 기록, 실패=technical,
필수 값/출처 모순=HOLD. 원래 SCORES 그대로 적용한다. 숨은 raw/head 효과 역산 없음.

## 작업과 보존

S0 허용 문서·소스 식별 검토, 새 이 폴더와 status/log 추가만 수행했다.
모델/테스트/채점/보호자료/ZIP/원격/플랫폼/commit/push/서브에이전트0.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, 진입 dirty114, named local jobs0.
[읽기·보존 기록](verification.json). 새 A/E 번호 없이 E063 안에 기록한다.

E041 incumbent/E025 fallback, E057/E060/E061/E062/E063 parked; E062 tie UNRESOLVED.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040 및 모든 STOP/HOLD,
17999명/12339SSUID·집계·A022 원래 역할,
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866 유지.
A_half 비승격/A018 사용자 미확정/S3 중단. 제출 권고가 TEST 선택이나 업로드 실행 권한은 아니다.
