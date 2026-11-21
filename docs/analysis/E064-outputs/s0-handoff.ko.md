# S0 인계 — E064 조건부 gradient 기술 검증 완료

**LOCAL_TECHNICAL_PASS_FOR_S0. E064 parked.**
S0가 [closeout](closeout.md), [verification](verification.json),
[고정 비교](attempts/score-01/comparison.json), [비용](cost-time-ledger.json)을 검토한다.

- 독립 conditional head는 학습한다. Conditional→trunk 직접 gradient만 차단.
  초기 state/forward/RNG/CE·분모 parity, branch gradient·head 갱신, 실제 tune/refit
  연결 등 신규10개 검사 통과. 원래 source와 기존 기록 보존.
- Fresh R/H all3 각각1회. 정상6pipeline/18neural/16metric, 재시작0.
  R379.994초/H376.841초; 검사·준비·평가·실패 포함877.378/1800초.
  보수적 RSS/private1.3013/1.4157GiB; CPU2/GPU0. 첫 launcher 접근 실패는
  별도 보존했고 환경을 교체하지 않았다.
- UNICEF/WB raw exact0. UNHCR132225/132273 vectors 변화.
  **UNHCR skill Δ−.000084353601793**, log Δ−.0001064333428662.
  작지만 하락이다. 사전−.002 하한 통과이며 합성 개선 판정이 아니다.
- Metric/donor/activity/replay 자격/bucket/ladder/agreement 기대 불변 모두 일치.
  Lambda12쌍 변화; config128x2/dropout.1,w.9 공통, 최종 epoch110→121.
  Pure direct effect·A021 D-P/D-R·independent audit 주장은 없다.

S0 판단 질문: **이 한 고정 정책에 별도 S2 release 검증을 허용할 가치가 있는가?**
기술적으로 진행 가능한 입력은 확보했다. 실제 효과·S2 자격은 미확정이다.
작은 synthetic 하락을 숨기거나 실제 UNHCR 효과의 반증으로 확대하지 않는다.
이 세션에서는 S2 실행 인계문/ZIP을 확정하지 않았다.

S2 잔여: clean E025 기관별−.002/E041 release 비교, source/assembly/extracted
parity, ZIP checker, official all3 shared900초·메모리, bytes provenance,
SCORES 사전 판독표. 현재 전부 별도 범위다. E041 incumbent/E025 fallback 유지.
No fresh oracle/current E041 loss map; 노출된 synthetic·원래 base S/L 재사용과
in-sample replay 한계 그대로. Actual hosted favorable/adverse/unresolved 판독은
A043 계약8절을 별도 제출 전에 동결하며 동일 정책 반복/seed·head 구제 없음.

E057/E060/E061/E062/E063 및 E064 parked, E062/E063 공개 동점UNRESOLVED.
모든 STOP/HOLD/보호 역할·17999/12339·A022·E059 소비/보호/집계 이력 보존.
A_half 비승격/A018 사용자 미확정/S3 중단/새 S2 후보 없음.
추가 fit/score/데이터/ZIP/원격/commit/push 없이 S0 검토로 반환한다.
