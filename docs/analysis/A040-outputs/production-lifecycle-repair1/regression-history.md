# 이번 로컬 검사 이력

이전15/39/14/6 suite, 과학 fixture, 종료 조회를 재실행하지 않았다.
각 process의 시작/종료 wall과 exit는 `*-process.json`, 실패 traceback은 해당 stderr에 보존했다.

| 기록 | 결과·수정 |
|---|---|
| loop-red | 실제 `_Sandbox._new_hydrated`의 독립 loop에서 StreamReader assertion 거절. 기대된 음성 검사. |
| cycle1 | 정상 경로는 reference/candidate 회수와 exact terminal까지 도달. 대역이 존재하지 않는 AppStopResponse를 만들어 최종 STOP. 실제 proto 정의의 Empty로 수정. 최초 terminal 파일의 시각도 최초 저장으로 고정. |
| cycle2 | 새8개 lifecycle 사례 통과. 실제 create/hydration/FS/exec/streams 사용. 기본 guard의 금지 접근 시도0. |
| cycle3 | SDK scheduling 실패 후 자동 종료·metadata 확인 사례1개 통과. 다음 create_stall은 생산120초 cap 때문에30초에서 감시 종료. 부모 wall30.0874074. 성공 처리하지 않음. 이후 미실행 사례만 계속. |
| cycle4 | 미실행 stream 실패/cash 모순2개 통과. 새로운 cash predicate의 true/false 경로 포함. 기존 통과8개 무변경 반복 없음. |
| cli | 실제 script __main__의 LOCAL 기본 진입·무허가 LIVE 거절2개. |
| parent-cli | Windows audit event의 executable=None을 guard가 거절. 자식 생성 전 실패. 실패본 보존. |
| parent-cli2 | 정확한 명령 문자열과 None 또는 정확한 executable만 허용하도록 guard 최소 수정. 실제 부모/숨김 자식 연결 통과. 별도 허용되지 않은 자식 명령은 거절. |

cycle1/2 source manifest와 변경 전 코드가 남아 있다. cycle3 이후 생산 source는 현재 manifest와 같다.
cycle2 이후 생산 변경은 최종 billing의 기존 cash0 정책을 cleanup에서도 유지하는 조건이다.
새 diff·새 실패마다 별도 S0 승인을 요구하지 않고 같은 세션에서 수정했다.

create_stall은 실패한 추가 검사이며 기본 suite에 없었다.120초 cap을 낮추거나 가짜 시계로
성공시키지 않았다. 생산 cap은 보존하고 향후 호출 시 이30초 범위에서 해당 사례를 거절한다.
그 기록 때문에 이번 전체 판정은 HOLD다. 총 check wall은 비용 장부를 따른다.

재현 시에는 새 미사용 cycle/output 이름과 같은 SDK1.6.0/source freeze를 사용하고,
인증/RPC 차단·CPU2·29초 자기 process 감시를 먼저 적용해야 한다. 아래 명령은 설명이며
이번 세션의 추가 실행 권한이 아니다.

```powershell
& .\tmp\a040-modal-full-path1\sdk-venv\Scripts\python.exe -I .\docs\analysis\A040-outputs\production-lifecycle-repair1\tests_lifecycle.py NEW_UNUSED_CYCLE normal hydrate id_lost timeout cancel reference_fail unknown_terminal billing_fail schedule_fail stream_fail billing_cash
& .\tmp\a040-modal-full-path1\sdk-venv\Scripts\python.exe -I .\docs\analysis\A040-outputs\production-lifecycle-repair1\test_cli_parent.py NEW_UNUSED_NAME
```

첫 정상 suite와 실패 이력은 `protocol-evidence/`에 작은 새 메타데이터로 보존했다.
기존 actual/fake 응답 배열을 이 폴더로 복사하지 않았다.
