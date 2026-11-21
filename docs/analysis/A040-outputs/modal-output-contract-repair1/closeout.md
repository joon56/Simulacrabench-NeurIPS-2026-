# A040 S1 — 출력 생산자·회수기 계약 보완

**LOCAL_OUTPUT_CONTRACT_PASS / REMOTE_EXECUTION_NOT_AUTHORIZED.**
2026-10-04 KST. S0 검토로 반환한다.

기존 exporter에 생산자와 같은 `world_bank` 메타데이터를 넣어
`Output export manifest mismatch`를 재현했다. 기존 대역이 같은 잘못된
`wb` 키를 사용해 이 결함을 놓쳤다는 S0 검토와 일치한다. 기존39-case PASS와
실패 기록·manifest/latch는 그대로 보존했다.

새 복사본의 변경은 exporter 한 파일의 키·개수 검사다. `world_bank`만
허용하며 기관별 정수 개수를 정확히 비교한다: unicef17856,
world_bank39520, unhcr132273. Candidate 추가 두 파일은 hash/files에만
포함한다. 경로 배치 변경 두 줄은 placement.diff로 별도 구분했다.
과학 runner를 포함한 생산 모듈9개는 원본과 바이트가 같다.

생산자 manifest/result 메타데이터와 source에서 독립 확인한 계약으로
영향 회귀14개 PASS. 정상 reference/candidate 회수, world_bank 경로,
wb 오기·키 누락/추가·같은 총합의 잘못된 기관별 개수·hash 오류·파일 누락
거절을 확인했다. Reference 회수 실패 시 candidate0이다.
재현 포함2cycle/2.6014084초; 기존39/15 suite·과학 fixture 재실행 없음.

초기 실행 요청은 원본 result 직접 읽기에 대한 자동 승인 검토에서 거절됐다.
프로세스 시작 전 거절이며, 검사 입력을 이미 추출한 최소 메타데이터로
좁히고 원본 경로 접근을 차단한 뒤 승인된 회귀를 수행했다.

원래 자료22개 identity와 새 source12개를 확인했다. HEADa43f4379 유지,
사용자 dirty work 보존. 새 출력 폴더와 status/log 추가만 작성했다.
실제 배열·모델·인증·RPC·GPU·원격 비용 발생 작업0; commit/push 없음.
시간은 cost-time-ledger.json에 과거 준비/controller와 과학 비용을 분리 기록.

이 PASS는 출력 metadata/file 계약만 인증한다. 실제 Linux/native enforcement,
계정/image/dependencies/112파일 parity, H100900초, 원격 cleanup/청구,
효과/release는 미검증이다. 프로토콜 `[]`를189649개 예측으로 주장하지 않는다.
원래 STOP/HOLD와 노출 경계를 유지하고, S0 검토 전 다음 단계로 가지 않는다.

[계약](producer-consumer-contract.md) · [회귀](regression-history.md) ·
[변경](source.diff) · [배치](placement.diff) · [검증](verification.json) ·
[S0 인계](s0-handoff.ko.md)
