# S0 반환 — A040 boundary2

**LOCAL_PRODUCTION_LIFECYCLE_HOLD / REMOTE_MEASUREMENT_NOT_AUTHORIZED.**
사용자가 명시한 두 경계를 같은 S1에서 수행했다. 원래 repair1 HOLD는 보존했다.

읽을 파일: [closeout](closeout.md), [verification](verification.json),
[실제120초 시간축](stall-timing.json), [회귀 이력](regression-history.md),
[소스 manifest](source-manifest.json), [cost-time-ledger](cost-time-ledger.json).

새로 관측한 사실:

- 기본 Endpoint._build와 실제 SDK Image.build/function/mount/resolver를 통과했다.
  controller_core.install_pins의 정확한 단일 프로젝트 소스와 생성 image의 Sandbox 전달,
  작은 protocol 회수/terminal을 확인했다. installer·모델은 실행하지 않았다.
- builder 실패는 Sandbox0·과학 명령0·App 정리로 연결됐다.
- 실제120.0091624초 대기 후 생산 timeout·취소·metadata terminal 저장을 관측했다.
  create1/terminate1, boundary/reference/candidate0. 강제 종료 없이 감독자125.9060169초.

**미해결은 정상 프로세스 종료다.** assertion 뒤 Python이 최종 GC에서 c0000005로 종료된다.
해당 소유 PID의 Windows 오류는 python313.dll. 전역 계측을 제거해도 재현했고,
정확한 root cause는 미확정이다. 일부 child 파일의 `BOUNDARY_PASS`를 최종 판정으로 읽지 않는다.
감독자 exit_code와 전체 verification이 우선이다. 실제 crash를 성공 종료로 우회하지 않았다.

다음 S0 판단: 이 model-free 종료 오류를 재현·축소할 구체적 로컬 조사 범위가 타당한지 검토한다.
현재 기록만으로 의존성/SDK/인터프리터 교체가 필요하다고 단정하지 않는다.
새 조사라면 허용 소스·환경 변경 범위·시간을 먼저 정한다. 원격 H100으로 우회 검증하거나
성공 전이·120초 대기를 근거 없이 다시 반복하는 과제는 권하지 않는다.
그 범위나 신뢰할 수정 근거가 없으면 현재 HOLD를 유지한다.

생산 변경은 cleanup/terminal 시각 event2개와 경로 배치뿐; 다른10파일 동일.
검사11회/184.9543889초, 실제 원격·과학·GPU·비용 행동0. 이전 준비17197.7879076초에
이번 active wall만 가산, 과학4/1077.3504532초 불변. 상세 PID/시간/초기 affinity 한계는 장부.
HEADa43f4379 불변, 사용자 dirty 보존, status/log만 추가, commit/push 없음.
기존 실Sandbox 종료 완료·기존 평가 경계·E041/E025·parked·모든 STOP/HOLD·A018 미확정/
S3 중단/S2 없음 유지. 이 인계는 원격 실행이나 S2 권한이 아니다.
