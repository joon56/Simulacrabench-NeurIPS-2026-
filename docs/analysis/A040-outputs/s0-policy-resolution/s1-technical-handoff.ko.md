# 다음 세션: S1 — A040 TabICLv2 로컬 계약 사전 검증

준비된 인계안. 작성 자체는 실행 허가가 아니다. 사용자가 별도 S1에 이 범위를
지시한 뒤 기존 RTX3070에서 실행한다. 새 유료 자원은 필요하지 않다.
H100 전체 경로 검증은 후속 별도 범위다. S0에서 실행하지 않는다.

```text
SimulacraBench / HSCC S1 — A040 TabICLv2 로컬 계약 사전 검증.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md를 순서대로 읽고 실제 개정·S1 technical 역할·범위를 보고한다.
HEAD/dirty files/active jobs를 확인하고 기존 변경과 원본을 보존한다.
다른 세션·서브에이전트를 시작하지 않는다. 기존 성공 실험을 재실행하지 않는다.

필수 입력:
- docs/analysis/A040-outputs/s0-policy-resolution/{decision.md,organizer-reply.txt,verification.json}
- docs/analysis/A040-outputs/s0-policy-resolution/environment-check.md
- docs/analysis/A040-outputs/s1/{contract.md,cost-accounting.md,observation-plan.md,
  source-register.md,schema-accounting.json,exposure-ledger.md,verification.json}
과거 manifest로 현재 파일을 되돌리지 않는다. 허용 문서·소스 해시만 비교한다.

주최측 답변은 사용자 전달 출처다. delivered visible rows를 이용한 runtime
최적화, 동결 모델의 전처리/context, 내부 선택·검증/refit는 양 phase에서 허용.
모두 기존 실행시간 예산에 포함된다. 외부 자료로 학습하는 것은 제출 전에
끝내고 산출물을 포함해야 한다. 이 답변은 자료 접근·S3·유료 자원 허가가 아니다.
A040 규칙 해석 HOLD만 해소했다. VAF A039 및 다른 STOP/HOLD는 유지한다.

목적/차이:
완료된 S1은 문서·소스만 확인했다. 이번에는 고정 계약을 구현하고 새 가짜
자료에서 출력·격리·loader 동등성의 작은 사전 검증을 수행한다.
질문은 고정 expert의 클래스·확률·전처리/context 경계와 공유 weight adapter를
정확히 구현할 수 있는가이다. ERPIS 효과나 900초 전체 실행 가능성은 판정하지 않는다.
2026-10-02 S0 범위 조정: 원래 H100 전체검증 계약의 작은 fixture 부분만 먼저
RTX3070에서 검증한다. 후보 head/context를 축소하는 정책 변경이 아니며,
기존 contract.md는 보존한다. 작은 fixture 비용을 전체 비용으로 외삽하지 않는다.

자원 진입 조건:
S0가 nvidia-smi로 RTX3070/8192MiB/driver591.86을 확인했다. H100은 로컬에서
확인되지 않았다. 이 인계문을 사용자가 실행 지시하면 기존 PC의 해당 GPU,
격리된 로컬 환경과 아래 고정 공개 source/checkpoint의 취득·설치를 허용한다.
환경·가용 RAM·다른 GPU 작업을 S1이 확인하고 경합을 피한다. 자동 cloud 생성/
유료 결제/SSH/계정 탐색/자격증명 읽기/원격 전송 금지. 로컬 결과로 H100
전체 성능 PASS를 주장하지 않는다. 공용 환경과 기존 설치·캐시는 수정하지 않는다.

고정 식별:
- E041: submissions/2026-09-19-E041/main.py
  SHA256 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
- TabICL code commit 0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3
- HF jingang/TabICL revision 4dcd344ece2c00be9e831fdd35bed57b5ad83e19
- tabicl-classifier-v2-20260212.ckpt, advertised110368038bytes
  SHA256 bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0
실제 취득 바이트 검증 전 역직렬화하지 않는다. 코드/weight provenance와
라이선스를 각각 유지한다. moving latest/PyPI 버전으로 대체하지 않는다.

허용 범위(사용자가 별도 S1에서 이 작업을 지시한 경우):
고정 공개 source/dependencies/checkpoint의 격리된 취득·설치, 공개 schema,
이번 작업에서 만든 seed4000 가짜 자료, 계약 구현과 명명된 기술 검증만.
새 코드는 docs/analysis/A040-outputs/local-technical/의 독립 연구 prototype과
runner/tests로 한정한다. 이 폴더가 이미 있으면 상태부터 확인하고 덮어쓰지 않는다.
원본 src/models, 기존 실험, submissions snapshot은 수정하지 않는다.
큰 weight/가짜 자료/환경은 기존 gitignored 위치의 A040 전용 하위경로만
사용하고 경로를 기록한다. 외부 원격 전송은 별도 허용된 파일만 사용한다.

구현/검증 계약:
- UNHCR17 GIVEN, 전체213 targets, gate sentinel 포함834 확률 칸. K최대15,
  K>10인4개 head도 포함. 부모4개/참조512명 축소 금지. UNICEF/WB는 E041.
- contract.md의 모든 고정 옵션 유지. import-time checkpoint1회 로드 adapter,
  head별 encoder/context/class mapping 분리, y 의존 cache 공유 금지.
  stock-vs-adapter 가짜자료 동등성·누수·공유 상태 검증. runtime network 차단.
- classes_를 전체 schema 순서에 배치. 미관측 class/raw0, singleton/empty
  context 규칙, 정규화·floor1회·원래 출력 순서 확인. invalid vector는 실패.
- alpha{0,.25,.5}, 동률 최소alpha와 동결 후 E 접근을 작은 고정 fixture에서
  확인한다. shadow에는 F만 접근, S/E/query의 PREDICT 전부 마스킹.
  full-shape F/S/E=6279/1000/1000 및 최종refit 비용 검증은 후속 H100 범위다.
  tiny fixture의 역할 크기·입력·검증 항목은 모델 실행 전에 고정해 기록한다.
- 작은 fixture suite 최대120초: class누락/15classes/singleton/empty,
  categorical unknown/missing, 열 순서, target/state격리, raw/floor, alpha0 parity.
- alpha0/fallback의 최종 distribution 보존은 고정된 가짜 E041형 입력 vector로
  산술 확인한다. 이는 실제 E041 full pipeline/control parity가 아니다.
  실제 E041 fit, 전체 all3, 전체 context 재구성은 이번 로컬 범위에 넣지 않는다.
  stock/adapter 확률 동등성은 같은 작은 fixture에서 확인하고,
  nondeterminism이면 기록한다. 결과를 본 뒤 tolerance를 만들지 않는다.

비용/종료:
작업 wall60분, 작은 suite scientific process1회, 누적 model wall120초.
기존 RTX3070한개, CPU최대2/TabICL threads2, heavy job1개. host memory
16000000000bytes 상한, process-tree RSS/commitment 1초 감시;
VRAM allocated/reserved/device capacity 별도 기록. 가용 자원이 상한보다
부족하면 무리하게 시작하지 않는다. 자기 작업 process tree만 한도/실패 시 종료.
CPU재시도 금지. 실제 context fit/predict/load/fallback 수와 측정시간 기록.
원래 full contract의426 context fit/predict 및 E041비용은 이번에 측정되지 않는다.
다운로드/설치/구현도 작업 wall에 포함. 시간 부족은 INCOMPLETE, PASS가 아니다.
고정 정책/seed/head/context/threshold 구제와 추가 full run 금지.

산출물:
local-technical/entry.json, frozen-inputs/manifest, 정확 dependency pins/provenance,
prototype/runner/tests, fixtures 결과, loader/isolation/control parity,
resources.json(로컬 suite 비용·미측정 full-path 구분), exposure-ledger.md, verification.json,
closeout.md와 S0 인계문. status/log는 자신 작업의 결과만 최소 갱신한다.
LOCAL_CONTRACT_PASS는 명명된 작은 검증 통과에만 사용한다. full TECHNICAL_PASS나
release PASS는 금지. 계약 오류는 LOCAL_CONTRACT_FAIL, 로컬 GPU 메모리 부족은
LOCAL_RESOURCE_LIMIT, 자원 부재는 BLOCKED_RESOURCE, 시간 부족은 INCOMPLETE.
RTX3070 한도 실패를 H100 불가능 또는 가설 반증으로 확대하지 않는다.
실패/누락 closeout만 예비 작업으로 허용한다.

금지:
실제 응답/키/Parquet/기존 NPZ나 모델 cache/UNCHR_data 접근·재해시,
보호 audit·calibration 열람, 과거 synthetic 실험 재실행, 실제 hosted 실행,
새 E기록/다른 후보/튜닝, ZIP/checker/official release all3/업로드,
tree/기존 manifest 수정, commit/push, S2/S3/TEST 선택.
이번에 검증 후 취득한 고정 공개 checkpoint만 기술 작업의 역직렬화 예외다.

E041 incumbent/E025 fallback, E057/E060/E061 parked와 A_half 비승격 유지.
17999명/12339SSUID, A022 원래 역할·집계 노출, E059 소비 oracle1918/1124와
selection2007/1130, 보호 audit2074/1177·calibration1866 승계.
E058 STOP/E059 STOP_SELECTION 및 A039 포함 다른 HOLD 유지.
A018 사용자 미확정, S3 중단. 종료 후 S0로 반환; PASS여도 S2 자동 이관 없음.
```
