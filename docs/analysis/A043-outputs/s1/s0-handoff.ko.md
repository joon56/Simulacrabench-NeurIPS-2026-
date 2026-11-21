# S0 인계 — A043 조건부 gradient 계약 검토 완료

판정: **CONTRACT_READY_FOR_S0_REVIEW**. 정보·정적 설계 완료이며 모델/효과/release
PASS·구현 허가·새 S2 후보가 아니다. [계약](contract.md), [종료](closeout.md),
[읽기·해시·비용·보존 근거](verification.json)를 검토한다.

S0가 판단할 한 가지: **독립 asked-only head를 유지한 채 conditional CE의 trunk 직접
gradient만 차단하는 H에 대해 별도 제한된 구현·합성 기술 검증을 허용할 가치가 있는가?**
이 파일 자체는 다음 실행 프롬프트가 아니며 승인·실행을 자동 발생시키지 않는다.

계약의 핵심:

- 같은 constructor/parameter 순서/seed/RNG/단일 trunk forward·dropout/full·cond logits,
  CE·denominator 유지. Head는 계속 학습한다. Config2/원래 stop·w·final refit 유지.
- 초기 parity는 학습 후 parity가 아니다. Conditional의 denominator·선택 간접 영향은 남음.
  전체 CE finite difference 대신 분기별 gradient 및 head parameter 갱신을 검사해야 함.
- **Metric weights/section activity/donor/replay 자격은 기대 불변**. Neural 출력을
  metric fit에 넣는 경로가 없다. Lambda/최종 부모·자식 출력은 변할 수 있다.
  S0 원문의 넓은 영향 목록을 이 경계로 구체화했으며 과거 기록은 보존했다.
- 정상 fresh R/H6pipeline/18neural/16metric. Fresh clean E025 및 assembly·official까지
  정상 합15/45/32. 미래 S1 계산합1800초/S2 추가3600초 제안, all3별 shared900초,
  CPU2/GPU0/heavy1/RSS·private 각각8GiB. 실측/완료 보장이 아니며 별도 권한 필요.
- 모든 query PREDICT를 entry 전에 mask. 기존 base/refit의 S/L 재사용과 in-sample
  full-proxy replay 한계 유지. No fresh oracle, synthetic은 engineering뿐.

E012 공동 학습 이점과 E061 adverse를 반대 근거로 유지한다. 새 기전의 이득·손실,
전체 비용과 source/assembly parity는 아직 미검증이다. 미래 기술 PASS 후에도 clean
E025 기관별 .002, E041 release 비교, ZIP checker/official all3/bytes provenance/
사전 SCORES 판독표가 남는다. 이 세션에서 구현·검사·실제 답변 접근0.

권고: S0는 계약을 수용 또는 구체적 결함으로 반환한다. 수용하더라도 새 사용자 지시로
동결 등록·최소 영향검사·fresh R/H만 한정한다. 현재 E064 생성·실행문 활성화 없음.
Host favorable/adverse/unresolved/technical/HOLD 판독은 계약8절. 공개 tie는 정확한
효과0이 아니며 동일 정책 반복·seed/head/계수 구제 근거가 아니다.

HEAD/dirty와 기존 source·S0 기록 보존. E041 incumbent/E025 fallback,
E057/E060/E061/E062/E063 parked/E063 UNRESOLVED; E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD/A039/A040/all STOP/HOLD, 노출17999/12339·A022 역할,
E059 소비1918/1124·2007/1130/보호2074/1177·calibration1866 유지.
A_half 비승격/A018 사용자 미확정/S3 중단/S2 후보 없음. Commit/push·원격·ZIP0.
