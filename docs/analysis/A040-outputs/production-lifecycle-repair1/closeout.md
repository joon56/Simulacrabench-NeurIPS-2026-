# A040 S1 생산 lifecycle 로컬 수리 결과

2026-10-05. **LOCAL_REPAIR_IMPLEMENTED / LOCAL_PRODUCTION_LIFECYCLE_HOLD /
REMOTE_MEASUREMENT_NOT_AUTHORIZED.** S0 검토로 반환한다.

사용자는 이 채팅을 S1로 지정하고 `s0-query-contract-review/terminal-accepted-next-task.ko.md`의
로컬 수리·통합 검증을 명시적으로 지시했다. 실제 읽기·r5 개정·workflow 해시·범위는
[entry](entry.json)에 기록했다. HEAD는 a43f4379ec78dbc2de260463eef67bb1d567d7e1 그대로다.
시작/종료 git 상태는 모두89개 항목이며, 종료 시 이름 기준 python/pythonw/uv jobs0이다.
Git 소유권 차이는 해당 읽기 명령의 safe.directory 옵션으로 처리했다. 전역 설정은 변경하지 않았다.

## 구현·관측

- 새 복사본의 CLI child dispatch를 plain async wrapper와 SDK synchronizer에 연결했다.
  설치 SDK의 assertion은 보존했다. 원래 독립 loop의 실제 StreamReader 생성 실패도 재현했다.
- Sandbox 요청 전에 고유 이름·intent·가능한2400초 예약USD2.965933453125를 저장한다.
  실제 SDK RPC wrapper 직전에 별도 fsync latch를 저장하고 create/terminate 재시도를 차단한다.
  SDK가 handle 반환 전 자체 종료를 요청하는 경로에도 같은 guard가 적용된다.
- 기존 검증된 Query의 metadata/인증/V1·V2/terminal 판독을 새 `cleanup_query.py`로 연결했다.
  handle이 없어도 exact App/name 목록에서 ID를 회수한다. terminal 증거는 billing 전에 저장하며,
  후속 save가 최초 관측 시각을 덮어쓰지 않는다. ID 불명확·미확인 status는 PASS를 막는다.
- `controller_core.py`의 installer와 Linux runner/boundary/watchdog를 포함한7개 복사본은
  바이트 동일하다.5개 orchestration 복사본과 새 cleanup 모듈만 생산 변경이다.
  [source.diff](source.diff), [placement.diff](placement.diff), [재사용 diff](cleanup-query-reuse.diff),
  [source manifest](source-manifest.json), [보존 검증](preservation.json)을 참조한다.

새로 정의한 lifecycle11개 사례의 assertion이 통과했다. 정상 회수, hydrate 거절,
ID 소실, 응답 TimeoutError/CancelledError, reference 실패 후 candidate0,
미확인 terminal, billing 실패 후 terminal 보존, SDK scheduling 실패 시 내부 종료,
stream 오류, 최종 cash 모순을 포함한다. 정상 사례에서 실제 SDK Sandbox, filesystem,
StreamReader/Writer와 실제 create/from_id/exec/read/write를 사용했다.
중복 create/terminate와 동일 출력 경로 재진입도 차단됐다.

실제 `__main__`에서 기본 fixture·무허가 LIVE를 거절했다. 실제 launcher 부모는 새 숨김
CLI 자식을 시작했고, 자식의 인증/transport guard 설치 뒤 새 protocol pins 불일치에서 멈췄다.
양성 경로는 같은 `main --child → child → dispatch`에 작은 입력 Context를 주입했다.
실제 고정 pins/payload는 읽지 않았다. 원격 과학 명령은 대역에 기록만 했고 실행하지 않았다.

## 전체 PASS를 보류한 이유

1. 추가한 실제 create-stall 검사는 생산120초 cap을 기다리므로 각 검사30초 계약과 맞지 않았다.
   cycle3은30초에서 종료됐고, 부모 계측/회수 wall은30.0874074초다. 엄격한 자식 수명≤30초를
   입증한 기록은 없다. 이 검사는 PASS가 아니며 실제120초 만료·정리 결과도 미완료다.
   이후29초 감시 여유를 적용했고, 이 stall 사례의 재실행을 코드에서 거절했다.
   짧은 TimeoutError/취소 처리 통과와 실제120초 타이머 검증은 구분한다.
2. 양성 fixture는 기존 builder 검증을 재사용하고 `image_builder`에 완료 image 제공자를 넣는다.
   실제 Sandbox/FS/stream은 보존하지만 SDK `Image.build` 전체를 실행한 것은 아니다.
   따라서 전체 build→CLI 경로에서 **외부 RPC/인증만** 교체했다는 강한 동등성 주장은 하지 않는다.

코드 수리와 위 명시된 사례의 관측은 유효하다. 이를 무조건적인
LOCAL_PRODUCTION_LIFECYCLE_PASS로 승격하지 않는다. 누락을 메우려고 모델·원격 실행,
120초 이상 검사, 정책 변경으로 전환하지 않았다. 다음 판단은 S0 소관이다.

## 비용·노출·한계

정확한 각 process wall·실패·누적은 [비용/시간 장부](cost-time-ledger.json)에 있다.
준비14777.0797748초에 이번 wall을 한 번만 추가했다. 중첩 CLI 자식 시간은 중복 합산하지 않았다.
과학4process/1077.3504532초는 불변. 이 작업의 실제 인증/RPC/billing 재조회/원격 생성/
전송/build/H100/GPU/model/설치/유료 행동은0이다. guard와 source/trace 근거이며 packet capture가 아니다.

작은 고정 bytes와 count metadata는 protocol fixture다.189649 실제 예측이나 H100/GPU 동작,
Linux native offline·메모리·watchdog·900초 성능을 입증하지 않는다. 실제 효과·release·S2 후보도 없다.
기존 terminal `sb-svFnVI39hH3DpUIZ4Z9LXK`의 TERMINATED 수용은 유지하며 재조회하지 않았다.
Workspace meteredUSD0.01009897/billed0은 과거 집계다. 최종 A040 귀속 비용과 실제 GPU 시간은 미확정이다.

E041 incumbent/E025 fallback, parked E057/E060/E061, E058 STOP/E059 STOP_SELECTION,
A039 HOLD와 모든 기존 STOP/HOLD 유지.17999명/12339SSUID·집계/A022 역할·소비
oracle1918/1124·selection2007/1130, 보호audit2074/1177·calibration1866 불변.
A_half 비승격, A018 사용자 미확정, S3 중단, S2 없음. commit/push/tree/ZIP 변경 없음.

[회귀 이력](regression-history.md), [검증 범위](sdk-boundary-evidence.md),
[S0 인계](s0-handoff.ko.md)를 함께 읽는다.
