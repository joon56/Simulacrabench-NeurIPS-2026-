# S1 — A040 Modal H100 전체 경로 단일 검증

아래는 별도 S1 세션용 실행 프롬프트다. S0의 작성 자체는 실행이 아니다.

```text
SimulacraBench / HSCC S1 — A040 Modal H100 이식 및 전체 경로 기술 검증.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1.

이 프롬프트로 이 S1에 아래 준비·이식·제한된 원격 실행을 지시한다.
S0 판단을 대신하거나 S2 제작을 시작하지 않는다. 서브에이전트 없음.
AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md 순서로 읽고 실제 개정·역할·허용 범위를 보고한다.
HEAD·dirty files·active jobs를 확인한다. 기존 변경을 되돌리지 않는다.

필수 입력:
- docs/analysis/A040-outputs/s0-modal-plan/{decision.md,verification.json}
- docs/analysis/A040-outputs/resource-feasibility/{closeout.md,cost-and-porting.md}
- docs/analysis/A040-outputs/full-path-resume1/의 registration.md, input-reuse.md,
  closeout.md, resources.json, verification.json, source.diff,
  dependency-identity.json, requirements.lock.txt, fixture-manifest.json,
  manifest-classification.json, frozen-inputs/manifest.json 및 허용 소스.
- 필요한 원래 정책 문서는 위 기록의 링크를 따라 읽되 금지 데이터는 열지 않는다.

목적: 고정 E041+TabICLv2 경로가 명시한 H100/Linux 자원 경계에서 전체
출력·선택·refit·parity 계약을900초 안에 완료하는지 확인한다.
실제 UNHCR 효과나 TEST 개선을 검증하는 실증 연구가 아니다.
RTX3070 LOCAL_RESOURCE_LIMIT, tiny PASS 및 이전 실패는 모두 보존한다.
기존 주최측 runtime fitting 허용/설치 승인 결론을 다시 문의하지 않는다.

자원·비용:
- 사용자 Modal Starter 계정, 화면 workspace joon56, 결제수단 등록/$30 credits.
  spend limit$0/usage limit$30 설정 확인은 사용자 보고이며 독립 확인 전이다.
- 총 USD5 무료 크레딧 이내, 현금 USD0. 이 범위의 설치·이미지 준비·
  명시된 공개 코드/모델 및 fake 입력 전송·Sandbox 생성·실행·회수·종료 허용.
  계정 권한/남은 크레딧/기존 설정을 가능한 범위에서 확인하고 불일치면 중단.
  사용자 보고를 허위 live 인증으로 바꾸지 않는다. 추가 구매/한도 상향 금지.
- 정상 Modal 인증이 필요하면 사용자가 로컬 로그인 절차를 수행하도록 안내.
  토큰을 채팅·로그에 요구/출력하지 않는다. 다른 자격증명 검색 금지.
  계정 토큰/호스트 HOME/환경 전체를 과학 실행 컨테이너에 전달하지 않는다.
- 총 작업120분, 준비60분 이내. 준비/build/전송 상한$1, H100 컨테이너
  최대2400초, 총액$5 안에 종료·기타 비용 여유$1을 확보한다.
  실제 가격/상한 계산이 안 맞으면 실행 시간을 사전에 줄이거나 HOLD한다.
  reference/candidate 각900초는 늘리지 않는다. 대시보드 갱신만으로 비용을
  통제하지 말고 hard lifetime·CPU/RAM cap·1컨테이너와 비용 장부를 사용한다.
- H100! 단일 GPU, 기본 비할증 지역 선택, GPU fallback/복수 GPU 금지.
  NVIDIA identity/메모리/MIG 정보를 기록하고 전체 H100 할당 근거 확인.
  재고가 없거나 할당 실패면 자동 재요청/다른 GPU 전환 없이 반환한다.

허용 이식 범위:
- 새 docs/analysis/A040-outputs/modal-full-path1/ 및 tmp/a040-modal-full-path1/
  아래만 구현/출력. 충돌하면 기존 파일 덮어쓰지 말고 invocation을 구분한다.
  격리 Modal SDK·Linux 이미지/의존성 준비, OS 경로·watchdog·계측·전송·
  종료 wrapper만 수정한다. 기존 연구 소스/모델/제출 snapshot은 보존한다.
- 원래 Python3.13.14 및34 dependency pins를 출발점으로 Linux wheel/driver/
  CUDA/SDK/image identity를 고정한다. 플랫폼별 바이트 차이를 명시한다.
  맞는 배포물을 구하지 못하면 임의 최신 버전·다른 모델로 교체하지 않는다.
- GPU Sandbox runtime=gvisor, block_network=True, inbound tunnel/secret 없음.
  설치·취득은 과학 컨테이너 밖에서 끝내고 과학 import 전에 차단한다.
  새 OS/network/CPU/memory/latch 경계의 모델 없는 검증만 누적60초 허용.
  성공한 schema/tiny/model suite는 재실행하지 않는다.
- cpu=(1,1) physical core request/cap, 모델·torch·TabICL threads2 및 허용된
  logical CPU2 affinity를 적용/기록한다. Modal physical core와 기존 CPU2를
  같은 수치라고 간주하지 않는다. affinity/quota 검증 실패 시 실행하지 않는다.
- memory=(15258,15258)MiB:15,999,172,608bytes의 컨테이너 전체 hard cap,
  swap 없음. 모델/자식뿐 아니라 controller overhead도 포함한다.
  이는 사전 정의한 Linux 계약이며 Windows private commitment와 동일하지 않다.
  실제 enforcement 근거, owned-tree RSS/private 자료, CUDA peak를 별도 기록.
  가용 메트릭을 private commitment라고 바꿔 부르거나 cap을 늘리지 않는다.
- 과학 실행을 자동 재호출하는 Function/배포/cron 사용 금지. Sandbox의
  새 reference/candidate 명령을 각각 한 번만 요청한다. 로컬 지속 launch
  기록과 원격 원자적 latch로 중복 차단. RPC 응답 유실/중단 시 기존 ID만
  조회·정리하며 새 컨테이너/명령 재발행 금지. retries=0만으로 보장하지 않는다.
- 시작 전 SDK/API 계약과 새 모델 없는 경계 검증을 고정한다. 첫 예상 밖
  검증 오류면 기록·종료한다. 의도한 negative assertion은 실패가 아니다.

전송/입력 allowlist:
- 분류된 manifest의 공개 생산 소스/공개 schema/config/고정 TabICL 소스,
  E041 snapshot main.py 및 위 wrapper와 dependencies만 전송한다.
  저장소·tmp·사용자 HOME 통째 업로드 금지. 파일별 허용 목록/해시를 먼저 만든다.
- 딱 세 기존 fake 입력만 읽기·해시·전송·사용 허용:
  tmp/a040-full-path-local-retry1/unicef.json,
  tmp/a040-full-path-local-retry1/world_bank.json,
  tmp/a040-full-path-local-retry1/unhcr.json.
  원래 fixture-manifest/역할 배열과 대조. 새 생성·부분 결과 재사용 없음.
- 공개 checkpoint만 별도 허용:
  tabicl-classifier-v2-20260212.ckpt,
  SHA256 bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0.
  TabICL source0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3.
  HF revision4dcd344ece2c00be9e831fdd35bed57b5ad83e19.
  기존 승인된 공개 checkpoint를 재사용하며 의존성/이미지는 빌드에서 취득 가능.
- E041 main.py SHA256:
  22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
  기준 freeze manifest SHA256:
  b5f7effaa0a9ad427c403dfb2d524b8747c469968bb2cbb86419867911c8cacc.
  HEAD만으로 미커밋 소스를 식별하지 않는다. 불일치를 과거 파일 복구로 해결 금지.
- 실제 응답/키/Parquet/NPZ/옛 예측·모델cache/VAF/그 외 fake는 열거나 해시하지
  않는다. manifest에 있다는 이유만으로 허용되지 않는다.

실행:
1. 비용·권한·환경·전송 목록·경계 증거를 확보하고 변경 diff와 새 코드/입력/
   이미지/실행 명세를 prospective freeze한다. 시작 후 수정/재실행 금지.
2. 새 reference process1회<=900초: 같은 target에서 실제 E041 all3.
3. reference PASS이면 새 candidate process1회<=900초. 동시에 heavy1개.
   두 시간 모두 import/weight load/all3/검증/출력 포함, GPU 전체 lifetime2400초.
   두 과학 process 합<=1800초. 실패/중단 시 부분 상태 이어붙이기 없음.
4. 원래 F6279/S1000/E1000, visible8279/query621,213heads, shadow+final context,
   alpha0/.25/.5 및 최소 tie, 원래 floor·guard·seed·n_estimators·batch·AMP 등
   모든 모델/정책을 유지한다. 결과가 기존 fake alpha.5와 같도록 강제하지 않는다.
   자연 경로와 별도 engineering alpha.25를 구분하고 final expert 재활용은
   원래 같은 실행 내 설계만 허용한다. 추가 학습/대안 정책/사후 tolerance 없음.
5. 전체189649vectors, controls/final-E041/inactive/fallback exact parity는 새
   target reference 기준. RTX와 cross-device byte equality를 새 요구로 만들지
   않는다. 전체 head/state isolation/최종 hash/S-E 접근/engineering render 등
   원래 미완료 assertion을 모두 완료한다. 실제 모델 import/load/fit/predict/
   pipeline/metric 횟수·실패 시도·elapsed·전체 memory/CUDA peak를 기록한다.
6. 첫 오류/900초/메모리/비용/작업 deadline 도달 시 과학 작업 중단·증거 회수·
   정확한 remote ID 종료. 새 run/정책변경/한도완화 없이 S0로 반환한다.
   종료·회수는 성공/실패 모두 필수. 연결 유실이면 사용자에게 정확한 Sandbox
   ID와 수동 종료 방법을 전달한다. 플랫폼 terminal 상태와 잔여 작업 확인.

판독:
- 전체 통과: H100_FULL_PATH_PASS, 이 명명된 Linux/fake 계약에 한정.
- cap/OOM: H100_RESOURCE_LIMIT; 모델 결함/전체 가설 반증으로 확대 금지.
- 불변식/출력/경계 실패: H100_FULL_PATH_FAIL.
- 시작 전 권한·자원·의존성·제어 부족: BLOCKED_SPECIFIC_INPUT.
- 시간/비용으로 미완료: INCOMPLETE. 부분 통과를 전체 PASS로 승격하지 않는다.
항상 S0 검토로 반환. H100 PASS도 hosted900초/실제 ERPIS 개선/release PASS 아님.

산출물:
entry/registration, diff 및 사전 source-input-image manifest, allowlist,
port-contract와 모델 없는 새 경계 결과, reference/candidate events·resources·
result(없으면 정확한 실패 기록), all-in cost-ledger, remote IDs/termination receipt,
exposure-ledger, verification, closeout, s0-handoff.ko.md; status/log 최소 갱신.
비용 확정 지연은 estimate/posted usage를 분리하고 미확정 항목으로 남긴다.
메모리 peak는 합산하지 않고 역사4회1077.3504532초와 새 실행을 구분한다.

금지: 원래 소스 수정·성공 fixture 재실행, 임의 코드 최적화·context/head/seed/guard
변경, 실제 데이터 접근, 새 E기록, official score.py/ZIP checker/release 제작,
업로드/commit/push/tree 수정, S2/S3 실행, TEST 선택, 자동 과금 연장.
이후 E025기관별absolute.002/E041 비교·source/assembly parity·공식 all3·
SCORES 판독·model disclosure/hosted 비용·upload byte 검증은 별도 범위다.
E041/E025, parked E057/E060/E061, 모든 STOP/HOLD와 A039, 노출17999/12339,
A022 원래 역할, E059 소비oracle1918/1124·selection2007/1130 및 보호audit2074/1177·
calibration1866 보존. A_half 비승격, A018 사용자 미확정, S3 중단, S2 후보 없음.
```
