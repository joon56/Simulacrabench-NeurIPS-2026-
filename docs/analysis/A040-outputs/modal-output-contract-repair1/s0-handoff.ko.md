# S0 인계 — A040 출력 계약 보완 결과

**LOCAL_OUTPUT_CONTRACT_PASS / REMOTE_EXECUTION_NOT_AUTHORIZED.**
S0에서 검토 후 다음 범위를 판단한다. 이 인계는 실행 허가가 아니다.

읽을 자료: closeout.md, producer-consumer-contract.md, source.diff,
placement.diff, verification.json, regression/cycle1-result.json 및
cycle2-result.json, source-manifest.json/contract-manifest.json.

기존 exporter가 실제 생산자 키 world_bank를 거절하는 오류를 재현했다.
새 exporter는 world_bank로 일치시키고 기관별 정수 개수를 정확히 검사한다.
기대 계약은 기존 fixture-manifest·reference result 메타데이터와 runner
쓰기/읽기 source에서 확인했다. 소비자 상수만 복사한 기대값이 아니다.
Candidate 추가2파일은 원래3기관 output_counts에 포함하지 않는다.

변경 영향 회귀14개 통과, 재현 포함2cycle/2.6014084초. 정상 두 mode 회수,
오기·누락·추가·같은 총합/다른 기관별 개수·hash·파일 오류 거절,
reference 회수 실패 시 candidate0. 원래39/15 suite 재실행 없음.
초기 자동 승인 거절은 검사에서 원본 result 직접 접근을 제거해 해소했다.
실제 예측 배열 접근·모델·인증·RPC·원격 실행·비용 발생 작업0.

생산 변경은 sandbox_stage.py뿐. contract.py의 원격 문서 경로와
live_launcher.py의 source prefix만 새 폴더로 배치했다. Linux runner는
바이트 동일하며 원래 임시 출력 경로도 유지한다. 원본22개/새source12개
identity 검증, HEADa43f4379/dirty/기존39-case PASS·STOP/HOLD 보존.

S0 판단: 이 출력 계약 결함의 보완을 인정할지, 이후 별도 bounded 원격
측정을 제안할 가치가 있는지. 현재 실행 권한은 없으며 자동 재시도·추가
수리·S2 제작을 시작하지 않는다. 실제 Linux 자원/native 강제·image/계정/
112파일 identity·H100900초·cleanup/청구·효과/release는 여전히 미검증.
새 source-manifest SHA256:
`0060ed98fc7e3c9ecc5625bd24f5c276971b026817dbb06c92fc2744dec83815`.

누적 준비/controller는7553.1022106초에 이번 ledger 시간을 더하고 과학
4process/1077.3504532초는 별도 유지한다. USD1/5 계획·cash0·과거
billing0/component0.00001152USD·귀속/미게시 미확정 유지.
E041/E025, parked E057/E060/E061, 모든 STOP/HOLD/E058/E059/A039,
노출17999/12339·A022·E059 소비/보호 역할 유지. A_half 비승격,
A018 미확정/S3 중단/S2 후보 없음.
