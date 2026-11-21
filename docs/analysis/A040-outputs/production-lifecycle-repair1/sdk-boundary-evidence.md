# SDK 경계·대역 위치

기존 설치SDK1.6.0을 재사용했다. 아래 경로는 모두
`tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages/` 기준이다.

| 실제 소스/경계 | 읽은 근거·이번 사용 |
|---|---|
| modal/sandbox.py:599~616 | 실제 SandboxCreate→_hydrate→_get_task_id. scheduling 오류 시 shield(terminate). 실제 호출됐으며 두 번 생성/종료하지 않았다. |
| modal/io_streams.py, _StreamReader.__init__ | synchronizer loop assertion 보존. 원래 독립 loop 실패와 새 관리 loop 성공 확인. |
| modal/sandbox_fs.py | 실제 filesystem write/read가 실제 Sandbox.exec·process stdin/stdout을 사용. |
| modal/_utils/task_command_router_client.py | 실제 router 생성·stub/exec/process/stream 처리 유지. 연결 및 grpclib 송수신 응답만 작은 대역으로 제공. |
| modal/client.py, modal/_utils/auth_token_manager.py | 실제 generated wrapper와 token manager 사용. 정상 인증 진입은 guard로 차단. fixture subclass의 transport와 token fetch만 대역. |
| modal_proto/api_grpc.py:2708 | AppStop 반환형은 google.protobuf.Empty. 잘못된 fixture 응답을 이 정의로 수정. |
| live_launcher.py | 같은 argparse/child/SDK dispatch로 양성 입력 주입. __main__ 거절 검사, 실제 부모→자식 pins gate 검사도 별도 수행. |

실제 Sandbox 객체, from_id 회수, StreamReader/Writer, filesystem, exec/process 반환 객체를
fake 클래스로 바꾸지 않았다. SDK assertions/source는 수정하지 않았다. `Endpoint.connect`의
instance RPC mutation wrapper는 생산 코드의 중복 방지·durable intent 기능이며 실제 SDK
wrapper로 위임한다. 테스트가 생산 guard를 우회하지 않았다.

예외/한계: builder 완료 image는 기존 injectable `image_builder`를 통해 제공했다.
이는 RPC 응답 수준보다 넓은 대역이다. 전체 Image.build/function/mount/layer 처리의
이번 재검증은 아니다. 따라서 전체 경로의 외부 endpoint만 교체한 동등성 PASS는 보류했다.
실제 pinned112 input branch도 열지 않았다. 양성 입력은22bytes protocol 파일이다.

정상 fixture의 boundary flag와 count17856/39520/132273은 작은 metadata envelope다.
모델·Linux boundary/watchdog 명령은 backend.commands에만 기록했다.
모든 응답 bytes는 protocol 표시가 있는 작은 텍스트이며 예측 배열 생성 증거가 아니다.

local_guard는 실제 인증·외부 connect/DNS/sendto·보호 확장자·모델 import를 차단한다.
Windows asyncio의 소유된 stdlib socketpair IPC만 허용한다. 마지막 parent 검사에서만
정확한 local CLI 명령 하나를 허용했고 child sitecustomize에서 독립 guard를 설치했다.
그 child의 pins mismatch/guard/exit 증거는 protocol-evidence/parent-*에 보존했다.

모든 source/hash 확인은 허용된 생산 소스·SDK·기존 문서와 이번 작은 산출물에 한정했다.
네트워크 패킷을 캡처했다거나 기존 remote 부재를 재조회했다고 주장하지 않는다.
