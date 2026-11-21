# S0 인계 — A040 resume5 준비 실패

판정: **REMOTE_PREPARATION_FAIL / SANDBOX_HANDLE_LOOP_MISMATCH**.
과학 실행0. 코드 수정·재시도·S2 이관 없이 S0 검토로 반환한다.

우선 미완료 조건: workspace joon56, App `ap-XiMVzlJgrNrCiFpIN1kB4W`는
STOPPED/task0 관측. Sandbox `a040-resume5-20261005-094405-gpu`는 ID 복구 실패,
**terminal UNCONFIRMED**. 사용자에게 종료 확인 및 살아 있으면 해당 자원만
종료하도록 즉시 알렸다. 정리60초 소진 후 추가 원격 호출 없음. 최종 billing도
미완료이며 비용0으로 기록하지 않는다.

새 사실: builder의 controller_core 전달·고정34pins 설치 완료. 이미지
`im-XZ95GDfkfa6PwWUeFyciYM`. 이후 SandboxCreate 응답 뒤 SDK StreamReader의
이벤트 루프 assertion 실패. 같은 raw 경로의 이름 복구도 실패했다. Sandbox
생성0/GPU 비용0의 근거가 아니다. 원인·소스 위치는 failure-analysis.md 참고.

allowlist112+source12/145605744bytes 로컬 해시 통과. Sandbox payload 전송 전
중단. boundary/reference/candidate NOT_RUN;900초·GPU/driver/메모리·출력·효과·
release 미검증. raw worker166.169042초에 정리60.0100353초 포함. 과학 누적
4process/1077.3504532초 유지. 준비 누적과 중복 없는 계수는 session ledger 참고.

raw metered 집계0.00178978USD는 귀속 미확정·최종 청구 아님. GPU timer가
시작되지 않은 관리값의 누락을 명시하고2400초 Sandbox 계획을 별도 예약으로
표시했다. 예산·cash0 불변. HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1,
source12/config/pins 불변, 기존 dirty·실패·PASS·manifest/latch 보존. commit/push 없음.

읽기: closeout.md → verification.json → failure-analysis.md →
run/termination-receipt.json → session-cost-time-ledger.json.

다음 판단은 종료/청구 증거 정리와 실제 SDK create/recover/stream 경계를 포함한
별도 로컬 검증의 타당성이다. 이 인계는 새 수리·원격 실행 허가가 아니다.
현재 시도 allowance를 되살리지 않는다. E041/E025, parked, 모든 STOP/HOLD 및
보호 노출 유지. A018 미확정, A_half 비승격, S3 중단, S2 후보 없음.
