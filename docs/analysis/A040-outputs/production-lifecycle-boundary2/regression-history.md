# 범위 내 수리·실패 이력

전체45분, 마지막10분 기록, 검사420초. 매 실행 전 최악60/210초를 수용하는지
`run_check.ps1`에서 확인했다. `*-preflight.json`에 당시 소스·검사 hash와 잔여량이 있다.
각 output·source snapshot·실패 stderr·감독자 receipt는 보존했다.

| 시도 | 관측·변경 |
|---|---|
| image-success1 | 실제 build/회수/terminal assertion 완료. 종료 access violation. 최종 PASS 아님. |
| image-exit-diagnostic2 | faulthandler만 추가. 종료 GC의 native 접근 위반 재현. |
| image-exit-repair3 | 이미 시작된 SDK thread의 profile 해제도 적용. 종료 오류 유지. |
| image-observer4 | 전역 profile 대신 특정 코드 monitoring. 오류 유지. profile만의 문제라는 가설 반박. |
| builder-failure1 | 새로 허용된 실패 전이. Sandbox0/science0/App 정리 관측 후 같은 오류. Sandbox/stream만의 원인으로 좁힐 수 없음. |
| builder-gc-diagnostic2 | 명시적 GC 자체는 반환. 이후 interpreter 종료 GC에서 실패. |
| builder-loop-close3 | SDK loop를 명시적으로 종료해도 실패. 변경은 로컬 계측에 한정. |
| builder-message4 | fixture가 요청 protobuf 하위 객체를 오래 보관하지 않고 metadata만 기록. 실패 유지. |
| builder-await5 | 전역 tracing 제거·SDK 대기 연결 읽기로 변경. 새 actual-Python affinity 설정의 HANDLE 타입 오류로 SDK 전에 중단. |
| builder-await6 | ctypes HANDLE argtypes/restype 수정. 실제 build 실패 전이 assertion 완료, 종료 GC 오류 유지. |
| real-stall1 | 생산120초 대기1회.120.0091624초 뒤 취소, metadata terminal. 감독자125.9060169초. 최종 native 오류 유지. |

반복은 미해결 process exit 경계에 대한 수정/진단이었다. 기존에 정상 종료까지 통과한 사례나
과거 성공11-case suite는 반복하지 않았다. native 원인 미확정 상태에서 진단을 더 확장하지 않았다.
검사 내부 assertion과 process exit 판정을 분리했다. 초기 child의 PASS 텍스트는 전체 판정을
대신하지 않는다. 종료 코드는 항상 `*-process.json`을 함께 본다.

감독자 실행 예시는 아래와 같다. 새로운 실행 권한을 뜻하지 않으며 현재 S1은 종료한다.
새 검토에서 허용되더라도 기존 이름·디렉터리/latch를 재사용하지 않는다.

```powershell
& .\docs\analysis\A040-outputs\production-lifecycle-boundary2\run_check.ps1 -Attempt NEW_UNUSED_NAME -Case success
& .\docs\analysis\A040-outputs\production-lifecycle-boundary2\run_check.ps1 -Attempt NEW_UNUSED_NAME -Case builder_fail
& .\docs\analysis\A040-outputs\production-lifecycle-boundary2\run_check.ps1 -Attempt NEW_UNUSED_NAME -Case stall
```

기존 SDK1.6.0만 사용. 실제 Image.build·function/mount/resolver·Sandbox/FS/process/streams는
보존했다. `boundary_transport.py`는 외부 서비스 응답·인증·전송에 작은 protocol 결과를 제공한다.
legacy `fixture_transport.image_build_response`는 이번 경로에서 사용하지 않았다.
Endpoint 생성 시 image_builder 인자를 주지 않았고 기본 bound method identity를 확인했다.
후반 trace에는 실제 SDK task의 await chain에 `_Image.build`와 `Endpoint._build`가 기록된다.

원래 성공 byte-count metadata를 실제 데이터 출력 수로 재해석하지 않는다.
모델/installer 실행은 없었고, 최초 SDK 소스 요청의 checksum·전송 요청 bytes를 독립 확인했다.
