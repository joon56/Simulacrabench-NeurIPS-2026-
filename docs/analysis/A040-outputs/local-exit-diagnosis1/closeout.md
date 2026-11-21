# A040 S1 종료 crash 축소 — HOLD

**LOCAL_EXIT_DIAGNOSIS_HOLD / REMOTE_MEASUREMENT_NOT_AUTHORIZED.**
정확한 원인은 미확정이다. 검증된 수리나 새 실행 후보는 없다.

HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, dirty89 보존.
AGENTS/CLAUDE/status/log 최신3개/workflow r5/완성 인계문 읽기와 SHA는 entry.json.
기존13개 생산 소스 identity를 확인했다.

builder_fail은 예상 실패/App 정리 뒤 c0000005로 종료됐다. 동일 import와 SDK
관리 loop는 정상 종료했다. A040 launcher/Context를 제거해도 crash가 남았고,
image 정의까지만 수행하면 정상 종료했다. coroutine 관측 제거와 출력 wrapper
제거도 각각 crash를 없애지 못했다. 현재 최초 구분 경계는 실제 build/resolve다.
특정 SDK 함수·protobuf·guard·Python DLL 자체의 결함으로 확정할 수 없다.

5개 비교/6개 Python 실행, 감독자 합27.3473137초. 각30초 이내, 강제 종료0,
회수 후 관련 Python jobs0. launcher와 실제 Python PID/exit를 따로 기록했다.
C6 protobuf 대조는 준비만 됐고 시간 gate가 실행을 거절했다. 결과 없음.

**시간 준수 실패:** 세션 gross wall이40분을 넘었다. 확인되지 않은 대기 시간을
임의 차감하지 않고 장부에 보수적으로 합산했다. deadline을 연장하지 않았으며
차단 후 검사 없이 종료 기록만 작성했다. 검사240초 준수와 전체 wall 초과는 별개다.

새 복사본의 출력 wrapper 제거는 실패한 진단 대비이며 생산 수리가 아니다.
현재 진단 소스를 원격 후보로 사용하면 안 된다. 원본 boundary2/repair1와
설치 환경·manifest/latch·실패는 보존했다. 이전 Image.build/source mount/
120초 취소/terminal 관측은 유지되지만 완전한 lifecycle PASS는 여전히 아니다.
성공 전체 경로·120초·기존11-case suite·과학 fixture를 반복하지 않았다.

공식 protobuf issue22067은 다른 버전/OS의 유사 증상일 뿐 원인 증거가 아니다.
source-register.md 참조. 환경 교체·새 전체 suite·원격 재시도를 자동 제안하지 않는다.

S0 다음 판단: build/resolve 동안 생성되는 객체와 native 종료 실패를 연결하는
추가 원인 근거가 확보 가능한지 검토한다. 현재 축소 재현/정상 대조는 남겼으나
원인 수준 최소성은 미입증이다. 추가 실행에는 별도 한정 범위가 필요하다.
장부·보존·평가 보호·기존 STOP/HOLD는 verification과 각 ledger에 기록했다.