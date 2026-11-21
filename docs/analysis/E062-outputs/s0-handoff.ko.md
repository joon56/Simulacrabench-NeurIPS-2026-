# S0 인계 — E062 WB16 순서 조건부 head

판정: **EXPLORATORY_SOURCE_QUALIFIED**. 사용자 전달 범위의 구현·합성 기술 검증 완료.
실제 WB 효과·S2 release 자격·TEST 채택은 미확정. S0에서 다음 범위를 판단한다.
새 모델 실행·S2 전환·ZIP·업로드·commit/push 권한은 이 인계로 생기지 않는다.

읽을 핵심: [closeout](closeout.md), [verification](verification.json),
[comparison](comparison.json), [자원 장부](resource-summary.json),
[구현·재현 계약](implementation-contract.md), [노출 장부](exposure-ledger.md).
새 구현은 `src/models/wb_ordinal_heads.py`, 집중 테스트는
`tests/test_wb_ordinal_heads.py`, 실행기는 `scripts/check_e062_wb_ordinal.py`.
사전 등록은 `docs/experiments/E062-wb-ordinal-heads.md`와 불변 registration.md.

## 사실과 판독

- 새 영향 검사13개 통과. 최초 예상 RED 보존. clean E025/E041/후보를 각 fresh
  process에서 all3 한 번씩 실행. 아홉 raw 출력 동결 후 공식 함수로 한 번씩 채점.
- UNICEF17856/WB39520/UNHCR132273 출력 계약 통과. UNICEF·UNHCR 후보−E041 raw 차이0.
  WB35613개 변경, 최대 절대 차이.1600416005. NO_OP 아님.
- 후보 skill: UNICEF .5006484231 / WB .4549896845 / UNHCR .5624627289.
  E041 대비0 / +.0002723772 / 0. E025 대비0 / +.0002723772 / −.0004861448.
  모든 기관의 두 −.002 기준 통과. UNHCR의 E025 대비 소폭 하락도 기록했다.
- **대상16은 하락**: 평균 log score 차이−.0007987550. 나머지60은+.0009093584.
  대상 Not answered−.0044084735, substantive−.0003982108. 전체 WB의 소폭 상승을
  순서형 대상 개선으로 해석하면 안 된다. head/seed/threshold 변경·추가 진단 없음.
- WB w1/config128·2·.1 유지, 최종 epoch는 E041193/후보184. 따라서 초기화·비응답
  분리·trunk·선택/refit를 포함한 전체 절차 비교다. 순서 제약만의 인과효과 아님.

## 비용과 보존

후보 fresh all3 **357.522443/900초**, E025324.976598초/E041342.965921초.
실패 검사·준비·평가 포함 computational child **1123.196596/1800초**.
실제 pipeline9/9, neural27/27, metric optimizer16; 추가 학습 허용량 없음.
CPU 수치 threads2/GPU0/heavy1, 관측 RSS1.3085GiB/private1.4520GiB<각8GiB.
실측은 로컬 전체 경로다. hosted/H100/실제 release 환경900초 보장 아님.
세션 시작·종료/gross는 entry 및 closeout-receipt, 세부 계수는 call-summary 참고.

허용 synthetic TRAIN/DEV 해시 일치. TEST 행 요청0, 모델 worker의 DEV 답변 열 요청0.
평가기는 출력 동결 후에만 DEV 답변 접근. lambda replay는 fit-label 재사용이며 새 audit 아님.
보호 자료·이전 cache·원격·설치·ZIP·tree·commit/push·서브에이전트 미실행.
HEADa43f4379 유지, 기존 dirty 보존, status/log 결과 추가. 원본 모델/snapshot 미변경.

## S0의 다음 판단

기술 후보 검토 가치는 확보됐다. 효과 근거는 부족하고 대상16 하락도 있다.
S0가 이 한계를 포함해 S2 release 검증 진행 여부를 결정한다. 현재는 S0 반환으로 종료.
새 seed/head 실험이나 A040 재개를 자동 제안·실행하지 않는다.

향후 S2를 별도로 허용할 경우 남은 항목: source/assembly parity, ZIP checker,
official all3 shared900s/메모리, clean E025/E041 release 비교와 기관별 absolute.002,
SCORES 판독표(Grand·각 기관·게시 노이즈/반올림·상태/ID). 실제 WB 효과·최종 채택은
별도 판단이며 합성 양성만으로 채택하지 않는다. 이 S1은 ZIP/제출물을 만들지 않았다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039/A040 유지.17999명/12339SSUID·집계·A022 원래 역할,
E059 소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866 보존.
A_half 비승격, A018 사용자 미확정, S3 중단, S2 release 후보 없음 유지.
