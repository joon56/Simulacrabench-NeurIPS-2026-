# S0 인계 — A040 실제 전체 경로, 후보900초 제한

**LOCAL_RESOURCE_LIMIT. reference PASS, 후보 최종 expert에서900초 종료.**
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`, 기존 변경·과거 기록 보존.
`closeout.md`, `resources.json`, `verification.json`, 양쪽 events/resources,
`candidate/partial-observations.json`, `source.diff`, `frozen-inputs/manifest.json`
근거로 검토한다. 후보 terminal result는 timeout으로 작성되지 않았다.

원래182개 해시/34개 dependency 일치, 새202개 사전 동결. 코드 변경2줄:
runner 출력TEMP와 watchdog deadline만. 지정된 기존 fake3개 그대로 사용,
입력 재생성·성공 schema/tiny 검사 재실행0회. 단일 진입 가용량 검사와
각 watchdog 시작 gate는 통과했다. 이번 실패 원인은 시작 메모리 부족이 아니다.

관측:

- reference all3 PASS,189649vectors,123.218초. E0413pipeline/9neural/8metric.
- candidate controls 및 final E041 UNHCR 출력은 reference와 exact parity.
  E0414pipeline/12CUDA neural/16metric 완료, 기록된 CPU fallback 없음.
- F6279/query2000 expert shadow213head 완료338.430초.
  가짜 S alpha.5 선택, 동결 후 가짜 E guard 수락(lower.03121557).
  절차 실행 확인이며 ERPIS 효과 근거가 아니다.
- visible8279/query621 final expert:199fit/198predict 완료 후900초 cap.
  전체 expert 완료 수412fit/411predict, import checkpoint load event1.
  최종 혼합·engineering alpha.25·inactive/empty driver·최종 state hash·
  완전한 all3 후보 출력 미완료. 저장된 후보 출력은 controls뿐이다.
- 후보 parent900.036초, RSS표본 peak2.629GB/commitment7.372GB.
  CUDA 마지막 관측 peak하한 allocated3.113GB/reserved4.886GB; 종료 peak미확정.
  메모리 OOM/한도 초과 기록 없음. 전체 무제한 완료시간은 측정하지 않았다.
- 자기 tree 종료, 잔여 작업 없음. 추가실행·수정·threshold 완화 없음.
  이번2process parent1023.254초, 과거2회 포함4회/1077.350초. 메모리 peak비합산.

S0 다음 판단: 이 고정 경로를 보류할지, 별도 자원/실행 가능성 범위를 마련할지
결정한다. 현재 RTX3070/CPU2/900초 계약은 통과하지 못했다. 완료된 단계 시간은
그 판단의 입력이며 H100 통과/실패 예측값은 아니다. 같은 시작 메모리 확인을
반복하거나 일부 head 시간으로 전체를 외삽하지 않는다.
자동 유료/H100 전환·context/head 축소·정책/guard 변경·코드 최적화·deadline
연장·부분 상태 이어붙이기·재실행 금지. 새 실행은 별도 승인 범위가 필요하다.

S2 후보 없음. 전체 기술검증 후에도 source/assembly parity, ZIP checker,
official all3, E025기관별absolute.002/E041비교, SCORES 판독표, uploaded bytes,
hosted900초/native-egress/model disclosure 검증은 별도다. 여기서 실행하지 않았다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD 유지.
17999명/12339SSUID·A022 원래 역할/집계 노출·E059 소비oracle1918/1124,
selection2007/1130 및 보호audit2074/1177·calibration1866 보존.
A039 HOLD 별개, A_half 비승격, A018 미확정/S3 중단. commit/push 없음.
