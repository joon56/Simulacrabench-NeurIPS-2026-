# A040 로컬 준비 경계와 builder source 계약

2026-10-05 KST. **LOCAL_BUILDER_SOURCE_CONTRACT_PASS / REMOTE_NOT_AUTHORIZED**.
이번 로컬 범위를 완료하고 S0 검토로 반환한다.

## 변경과 근거

생산 의미 변경은 sdk_endpoint.py의 `include_source=False`를 `True`로 바꾼
한 곳이다. contract.py와 live_launcher.py의 새 폴더 prefix 2곳은 placement
변경이다. 나머지9개 모듈은 byte-identical이며 controller_core/installer와
linux_runner도 포함된다. 원래 실패·미검증 복사본·manifest·latch는 보존했다.

새 source manifest SHA256:
`c782c99e29cfceeaba132018d48f2be2a844e7f8b51ba8840157f9ebfa845765`.
[의미 diff](source.diff), [placement diff](placement.diff), [manifest](source-manifest.json).

## 실제 관측

| 검사 | 결과·근거 |
|---|---|
| Python 진입 | 기존 SDK venv/Python3.13.14, CPU affinity3(논리 CPU2), 숨김 프로세스 |
| 로컬 IPC | SDK 전 Proactor, SDK 후 Selector, synchronicity 스레드와 Runner의4쌍 모두 정상 생성·종료. [result2](result-2.json) |
| 금지 동작 음성 검사 |11회 차단: main/worker client, RPC, image build, resolution, 외부/일반 loopback connect, DNS, subprocess, dummy credential path, installer 진입. 예상 밖 시도0 |
| 원본 SDK 구성 | 실제 FILE 함수 controller_core.install_pins. client mount1, 프로젝트 파일0. [result3](result-3.json) |
| 원본 격리 import | 빈 디렉터리에서 ModuleNotFoundError controller_core. [result4](result-4.json) |
| 수정 SDK 구성 | 실제 spec/dependency 목록 일치. mount2 = 기본 nonlocal client + 프로젝트 파일1. /root/controller_core.py, FILE·module/function 일치. [result5](result-5.json) |
| 잘못된 목록 | 누락·추가·local/remote 경로·바이트 hash 불일치 거절 |
| 수정 격리 import | SDK가 선택한 동일 바이트만 staging. 원본 경로 없는 -I/-S 프로세스에서 import·함수 식별·hash 확인. 전이 import는 stdlib/builtin. [result6](result-6.json) |

원격 default client mount는 로컬에서 해석한 미해결 handle이며 실제 업로드/조회는
없다. SDK source의 기본 이름은 modal-client-mount-1.6.0으로 결정되지만,
원격 존재·contents는 확인하지 않았다. 프로젝트 파일 목록은 실제 `_select_files`
결과다. source-discovery/FunctionSourceInfo/mount 처리는 대역화하지 않았다.
외부 image-build endpoint만 캡처 후 예외로 중단했으며 fake build 성공은 없다.

최초 일반 PowerShell 호출은 실행 정책에서 거부되어 자식 프로세스가 시작되지
않았다. 정상 도구 승인 후 같은 venv를 사용했다. ACL·계정·SDK 설치 변경 없음.
새 검사 프로세스6개 모두 exit0, **wall 합4.5988881초 /180초**, 각각30초 이내,
잔여 PID0. 프로세스가 시작된 이후 예상 밖 실패·수정 반복은 없었다.
과거2회 실패 기록/한도는 소비 상태 그대로다. 이전 성공 suite 재실행 없음.

## 해석·한계·다음 행동

이전 broad socket.connect 차단과 달리, 이번 guard는 실제 stdlib self-pipe
호출 코드·스레드 범위·자기 listener/csock endpoint를 확인했다. 다른 loopback
통신은 차단했다. 이는 **협조적인 Python 검사 경계**이며 OS/native egress
보장이나 Linux 실행 증명은 아니다. installer 음성 호출은 body 진입 전에 차단됐다.

실제 원격 module upload/import/build, Linux 의존성·driver·native 자원 집행,
112-file 현재 identity, H100·900초 전체 경로·효과·S2 release는 미검증이다.
34pins 정책과 installer는 변경하지 않았다. pins 파일 내용은 이번에 열거나
재해시하지 않았으므로 현재 pin-file identity를 새로 검증했다고 주장하지 않는다.

S0는 새 source identity와 이 제한을 검토한 뒤 별도 원격 범위를 결정한다.
이번 세션에서 원격 build/인증/청구 조회·모델 실행·S2 제작으로 전환하지 않는다.
원래 STOPPED/task0 종료 증거와 모든 과학 STOP/HOLD·노출 경계는 유지한다.

준비 시간·역사 비용은 [ledger](cost-time-ledger.json), 전후 보존·검사 해시는
[verification](verification.json), 경계 설계는 [design](boundary-design.md)에 기록했다.
입력·권한·읽기 근거는 [entry](entry.json), 다음 판단은 [S0 인계](s0-handoff.ko.md).
