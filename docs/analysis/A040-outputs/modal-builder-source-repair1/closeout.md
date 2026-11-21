# A040 builder source repair — 로컬 검사 미완료

2026-10-05 KST. **STOP_LOCAL_VALIDATION_INCOMPLETE**.
2회 한도 소진. 생산 소스 수정·원격 실행 없이 S0로 반환한다.

## 관측

1. Cycle1: 기존 SDK venv가 기반 Python에 접근하지 못했다. 경로 메타데이터
   조회도 `Access is denied`. 실행 파일 부재가 아니라 sandbox 접근 제한으로
   좁혀졌다. 검사 스크립트 미시작. 외부 wall0.1067439초. 최초 wrapper의
   exit_code는 null이므로 임의 값을 채우지 않았다.
2. Cycle2: 같은 venv의 로컬 검사에 sandbox 밖 실행을 요청해 승인받았다.
   검사 스크립트는 시작했으나 `socket.connect` 전면 차단이 Windows
   `asyncio`의 로컬 `socketpair` 생성까지 막았다. `PermissionError:
   Network/command disabled`; exit1, 내부0.0399672초, 외부0.3848652초.
   부분 초기화된 event loop의 종료 경고와 unawaited coroutine 경고도 보존했다.

검사 총 외부 시간 **0.4916091초 / 2회**. 첫 환경 실패도 회차에 포함했다.
Cycle2는 원본 재현 후 수정본 확인을 순서대로 하도록 준비했지만 baseline
시작 중 실패해 수정·fixed 단계는 실행되지 않았다. 성공 검사 반복 없음.

## 판정과 한계

실패 원인은 이번에 작성한 로컬 검사 도구의 차단 범위다. SDK import 전이므로
실제 builder 함수/mount 목록, FILE 분류, 정확한 파일의 격리 import는 모두
**미검증**이다. 원래 모듈 누락을 로컬에서 재현했다고도 주장하지 않는다.
소스 검토상 include_source=False의 문제는 이전 근거대로 남는다.

생산 소스12개는 새 복사본에서도 전부 원본과 동일하다. `include_source=True`
수정과 placement 변경은 적용되지 않았다. source.diff/placement.diff가 빈 것은
무변경 증거이며 수리 완료를 뜻하지 않는다. 새 manifest는 **미검증 복사본**이다.
검사/실행 스크립트는 실패한 진단 산출물로 보존하며 실행 준비 완료로 취급하지 않는다.

이번 RPC·인증·설치·전송·build·Sandbox·GPU·reference·candidate0.
보호 응답/키/배열/112payload/checkpoint/cache/VAF 접근·재해시0.
이전 App STOPPED/task0 기록만 보존했고 재조회하지 않았다.
새 source/pins/model/정책 변경·commit/push·S2/S3/ZIP 없음.

다음 판단: S0가 이 경로를 계속할 가치가 있다고 판단할 경우에만, Windows
이벤트 루프의 로컬 IPC와 외부 RPC 차단을 구분하는 검사 설계에 별도 제한 범위를
부여한다. 현재 실패 스크립트의 정적 검토가 먼저다. 여기서 세 번째 검사나
새 수리를 자동 시작하지 않는다. 실제 원격 build/H100/900초/효과/release 판단은 없다.

근거: [entry](entry.json), [검증](verification.json), [실패 결과](baseline-result.json),
[cycle1](cycle1.json), [cycle2](cycle2.json), [시간·비용](cost-time-ledger.json),
[보존](preservation-after.json), [S0 인계](s0-handoff.ko.md).

재현 이력: `run_local.ps1`은 cycle2-started.json으로 추가 실행을 거부한다.
과거 성공 suite39/15/14·과학 fixture는 실행하지 않았다.
