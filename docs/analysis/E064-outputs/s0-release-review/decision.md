# E064 S0 — 고정 후보 DEV 탐색 제출 1회 권고

2026-10-23 KST. **RECOMMEND_ONE_FIXED_DEV_SUBMISSION_FOR_USER_DECISION**.
E064는 parked, E041 DEV incumbent/E025 fallback 유지. 이번 문서는 사용자 제출
결정용이며 S0 업로드·재실행·TEST 선택 권한을 만들지 않는다.

## 판단과 정보 가치

기존 고정 ZIP 한 번의 DEV 탐색을 권고한다. E064는 독립 asked-only head를 유지하면서
conditional CE의 trunk 직접 gradient만 차단한다. E061의 logits tying/head 제거,
E063의 round 조건부 metric과 구별된다. 공유 표현의 학습 신호를 바꾸는 이 전체 정책이
실제 DEV에서 공개 해상도를 넘는 유리하거나 불리한 관측을 내는지가 다음 판단이다.
Gradient 충돌 자체나 그 인과효과를 hosted 점수로 분리해 측정하는 실험은 아니다.

배포 일치성·release 성능 정책·자원 기준은 고정 계약대로 통과했다. 실제 UNHCR 효과를
측정할 새 독립 oracle은 없다. 정확 gate의 노출된 synthetic은 실제 approximate gate
환경을 대표하지 못한다. 따라서 기술 PASS와 제한된 hosted 판독 가치를 근거로 권고하며,
이미 들인 비용이나 빈 일일 slot을 근거로 삼지 않는다.

반대 근거: E012 공동 학습 이점, E061 adverse, E064 자체 합성 UNHCR 하락
H−E041 −0.000084353601793 및 H−E025 −0.000570498449168. Conditional 표현의
학습 신호 제거가 손해일 수 있다. E062/E063 공개 동점과 게시 노이즈/반올림 때문에 작은
차이는 이번에도 미해결일 수 있다. 예상 Grand·승률·읽을 수 있는 개선 확률은 추정하지 않는다.

주력은 사용자 계정의 사용 가능한 DEV slot에서 동일 ZIP 1회 제출 검토다. Slot/계정/
현재 phase가 확인되지 않거나 사용자가 보류하면 그대로 parked 유지한다. 같은 정책 재제출,
seed/head/threshold 조정, 새 학습·패키징으로 구제하지 않는다.

## 검토 근거와 한계

- S2 artifact-manifest의 해시는 final verification과 일치했고, 명시한 핵심 문서·SCORES
  12개 해시도 일치했다. 이 S0는 ZIP/배열/Parquet/cache를 열거나 재해시하지 않았다.
- S2 기록상 source/assembly/extracted 189649 raw exact, UNICEF/WB exact controls,
  UNHCR 132225개 변화, 원래 invariant/lambda 일치. Stock checker/official all3 PASS.
- Assembly 553.078441초, official 전체 763.146280초/900초. 관측 RSS/private
  2.944355/2.500275GiB, sampler 최대 gap 0.144542초. 측정한 로컬 CPU 경로이며
  hosted/H100/숨은 frame의 runtime·memory 보장은 아니다.
- 계산 실측 1407.881025초와 보수적 준비/기록 차감420초를 분리한다. 합계
  1827.881025/3600초, gross 보수적3084.70878초/10800초. All3 시작2, 재시작0,
  6pipeline/18neural/16metric, 현금0. 종료된 B01의 남은 한도는 다음 작업에 전용하지 않는다.
- Manifest reader 오류와 마지막 memory predicate 결함은 기록·수리됐다. 수리 전
  assembly의 실제 관측 peak는 상한 아래였고, 후속 경계 검사 및 official은 보완 코드로
  완료됐다. 최초 감시기를 소급해 완전했다고 하지 않는다. 성공 학습 재실행 사유는 없다.
- Baseline 재사용은 원래 완료 raw/hash/source/frame/role/order/mask와 기록된 공통
  Python/NumPy/pandas/PyTorch/thread/CUDA 근거로 수용한다. E064 R와 clean E041의
  189649 raw exact 연결도 있다. 누락된 과거 executable hash·SciPy/sklearn/pyarrow
  버전은 미확정이다. 보존된 clean 출력과의 비교이지 완전 동일 환경의 fresh E025
  실행 증명이 아니다. 현재 의미 불일치 증거 없이 누락 필드를 채우려고 성공 실행을 반복하지 않는다.
- verification 내부 package의 PENDING_OFFICIAL과 technical.remaining은 이전 stage
  receipt다. 최종 official.json/resource/전체 verification의 PASS 및 명시적 쓰기 해제를
  함께 읽는다. 그 역사 필드를 수정하거나 새 scientific retry를 요구하지 않는다.

## 사용자에게 전달할 고정 산출물

`submissions/2026-10-23-E064.zip`, **16305 bytes**.
SHA256 **002028ce0c7fa7cb3549d198cef3e4c13060fdf9aa47ce7a7f7a773ee1c74f1c**.
package-path 기록의 제작 시각은 **2026-10-23T15:37:47.637369+09:00**.
이 값은 S2의 로컬 식별 기록을 승계한다. 실제 업로드 bytes/path/hash/ID/시각은 미확인이다.
ZIP을 변경하거나 재제작하지 않는다. 이번 S0는 플랫폼·계정·slot을 조회하지 않았다.

## 사전 판독과 결과 반환

원래 [SCORES](../../../../submissions/2026-10-23-E064/SCORES.md)를 유지한다.
Comparator는 E041 ID933094, Finished Development/phase29772의 사용자 API
Grand .6433333333 / UNICEF .52 / WB .49 / UNHCR .92다. 비교 가능한 실제 결과에서:

- UNHCR·Grand 상승, 통제 공개값 동일: 유리한 noisy whole-policy 관측, S0 재검토.
- 두 값 동점: UNRESOLVED, E041 유지/E064 parked, 동일 정책 추가 우선순위 낮춤.
- 어느 쪽 하락: 해당 실행 adverse. 반대 방향·통제 변화는 mixed/귀속 미해결도 병기.
- 실패: technical. 필수 값 부재·출처/phase 불일치: 필요한 근거를 명시한 HOLD.

상승도 자동 채택이나 TEST 선택이 아니다. 동점도 실제 효과0·예측 동일·기전 전체 반증이
아니다. 전체 API 문자열과 score key/precision/phase/status/ID/filename/출처를 확인하고,
현재 scorer-version·best-update event·remote bytes는 제공된 근거까지만 기록한다.
결과는 [같은 B01 세션의 문서 기록](s2-result-handoff.ko.md)으로 반환한다.

E025 phase2 provenance 보완·방법/license 최종화는 A044의 별도 미승인 후속 과제로 유지한다.
새 batch/가설, A039/A040 재개, 최종 TEST 결정은 이 결과 검토에서 만들지 않는다.
기존 STOP/HOLD·17999명/12339SSUID·집계/A022 역할/E059 소비·보호 역할,
A_half 비승격/A018 사용자 미확정을 보존한다.

이번 S0는 문서 기록만 수행했다. S2 명시적 해제 후 인수했으며, 이 폴더/status/log만
기록하고 final verification에서 해제한다. Git 목록은 접근 제한으로 불완전하며,
보존 확인은 명시한 문서 해시·status/log 역사에 한정한다. 모델·검증·ZIP·업로드·git 작업0.
