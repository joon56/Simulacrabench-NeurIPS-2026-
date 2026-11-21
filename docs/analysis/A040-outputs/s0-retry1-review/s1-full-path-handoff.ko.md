# 다음 S1 — A040 실제 E041 결합 및 전체 크기 로컬 경로 검증

준비된 인계문. 사용자가 별도 S1에 지시할 때 아래 범위를 실행한다.
작성 자체와 retry1 PASS는 추가 실행·S2·유료 자원 허가가 아니다.

```text
SimulacraBench / HSCC S1 — A040 실제 E041 결합·전체 크기 로컬 검증.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md → CLAUDE.md → status → log 최신3개 → workflow.md를 읽고
실제 개정/S1 technical 역할/범위를 보고한다. HEAD/dirty/active jobs 확인.
기존 작업·원본·latch 보존. 다른 세션/서브에이전트 자동 실행 금지.

필수 문서:
- docs/analysis/A040-outputs/s0-retry1-review/{decision.md,verification.json}
- docs/analysis/A040-outputs/local-technical-retry1/{closeout.md,verification.json,
  result.json,resources.json,source.diff,prototype.py,requirements.lock.txt,
  frozen-inputs/run-manifest.json}
- docs/analysis/A040-outputs/s1/{contract.md,cost-accounting.md,observation-plan.md}
- docs/analysis/A040-outputs/s0-policy-resolution/decision.md

기존 설치/취득 승인·주최측 정책 해소 승계. 재설치·취득·문의하지 않는다.
이번 지시는 아래 새 코드와 새 가짜자료의 명명된 기술 검증만 허용한다.
원래 실패와 retry1 LOCAL_CONTRACT_PASS를 모두 보존하고 재실행하지 않는다.

목적/차이:
이전45행 context 검증은 expert 내부 계약만 확인했다. 이번에는 실제 E041
전체 예측기, F/S/E 선택과 최종 visible refit, 모든 설문 출력까지 연결한다.
새 모델·혼합정책 탐색이나 ERPIS 효과 실험이 아니다. tiny40초를 전체 비용으로
외삽하지 않는다. H100 대신 보유 RTX3070에서 먼저 측정하는 새 S0 범위다.

고정 입력:
- E041 submissions/2026-09-19-E041/main.py
  SHA256 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073
- retry1 prototype과 동결 TabICL code/dependencies/weight는 manifest 그대로.
  code0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3,
  HF revision4dcd344ece2c00be9e831fdd35bed57b5ad83e19,
  checkpoint SHA256 bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0.
  승인된 tmp/a040-local-technical/venv/source/acquisition 사용; 새 취득 없음.
- external/starter-kit/data/{unicef,world_bank,unhcr}.json 공개 schema만.
source/hash 차이는 원인 확인 후 기록; 과거 manifest로 현재 파일을 되돌리지 않는다.

쓰기 경계:
새 docs/analysis/A040-outputs/full-path-local/에 prototype/runner/문서,
새 gitignored tmp/a040-full-path-local/에 가짜 입력·출력만 저장한다.
이미 있으면 덮어쓰지 않고 상태 확인. 기존 src/실험/제출/성공 suite/manifest/
환경/fixture/latch 변경 금지. 원본 E041은 읽기 전용 module로 호출한다.
공개 checkpoint를 바이트 검증 후 로드하는 것만 기존 모델 접근 금지의 예외다.

전체 입력은 이번에 새로 생성:
seed4000 한개, 공개 option/type/order를 지킨 가짜 값. 생성 규칙·입력 해시를
모델 호출 전에 동결한다. 각 visible context가 모든 public class를 포함하도록
설계하되 실제 데이터·gate 오류를 모사했다고 주장하지 않는다. 효과 판단 금지.
phase1 전체 row shape: UNICEF TRAIN14885/query1488, WB5195/520,
UNHCR8279/621. 실제 TEST행은 만들거나 사용하지 않는다.
query PREDICT는 처음부터 모두 NaN, GIVEN만 전달. 기존 가짜 fixture나
partial predictions를 열거나 재사용하지 않는다. row-position 매핑을 명시한다.

구현 계약:
1. UNICEF/WB는 실제 E041.predict를 그대로 호출하고 반환 vector를 그대로 사용.
2. UNHCR의 complete visible8279행을 PCG64(4001) 고정 permutation으로
   S1000/E1000/F6279에 배정. observation-plan의 순서와 동일하게 한다.
   F-only shadow frame에서 S/E와 external621행의 PREDICT 전부 마스킹.
   실제 E041 shadow predict는 이 frame에1회 호출, S/E 결과를 canonical
   위치로 복원한다. 원래 E041의 inner tuning/metric/lambda/renderer를 유지.
   E041 내부에서 visible<500인 tiny fallback으로 전체 경로를 대신하지 않는다.
3. Expert는17 GIVEN/213 heads, 원래 options/adapter, F6279 context와
   S+E2000 query만 사용. y-dependent encoder/context 공유 금지.
   S final-floor log score로 alpha{0,.25,.5} 선택, 동률 최소alpha.
   alpha 동결 후 E만 열어 원래1.645 SE guard, zero-variance 규칙 적용.
   shadow fit/preprocess에 S/E truth가 닿지 않음을 계측한다.
4. 최종 실제 E041은 원래 all-visible8279 frame에1회 호출해 query621 예측.
   정상 정책은 alpha0/E거절이면 그 raw output 그대로 반환하고 final expert 생략.
   수락 시 expert도 전체8279 context로 새로 구성, query621에 동일alpha 적용.
   최종 raw 완전분포에서 혼합; 평가 floor만1회. gate 재렌더링·double floor 금지.
   final refit는 shadow와 다른 허용 역할임을 명시하고 실제 호출로 확인한다.
5. final refit도 측정하기 위해 engineering-only driver에서 active 경로를
   반드시 실행한다. 실제 S/E 선택·guard 결과는 그대로 기록한다. 거절이어도
   별도로 final expert와 alpha.25 출력을 만들어 최대 활성 경로를 계측하되,
   정상 정책 출력과 구분 저장한다. 생산 경로의 guard 우회/강제 활성화 금지.
   같은 final R/q로 alpha0·empty fallback·active rendering을 검증하며 추가 fit 금지.
6. schema canonical output: 총189649 vectors(17856/39520/132273),
   finite/nonnegative/complete widths/order 확인. query truth를 채점하지 않는다.
   실제 E041 vector와 UNICEF/WB 및 inactive/fallback exact parity 요구.
   예측 전후 input frame 보존 확인. 상태 격리·import-time checkpoint1회 확인.
   observer hook는 논리·숫자를 바꾸지 않고 비용에 포함한다.

검증 순서/실행 상한:
- 새 orchestration의 row/role mapping·branch·logger를 model-free spy/정적 검사로
  먼저 확인(총60초). 이는 실제 모델 parity 증거가 아니다. 성공 suite 재실행 금지.
- 모든 code/inputs/arms/pins/자원 cap 동결 후 reference E041 all3 fresh process
  1회(900초). 그 다음 integrated forced-active all3 fresh process1회(900초).
  reference가 실패하면 후보 실행 금지. 별도 tiny model 실행·세 번째 run 금지.
  reference와 candidate는 동일 fake bytes, 설문 호출 순서, 환경과 E041 seed.
  reference의 이번 새 출력만 후보 parity에 사용; 그 읽기 비용도 측정에 포함.
  자체 새 input 생성·무모델 검사는 scientific run으로 위장하지 말고 별도 기록.

자원:
전체 task wall120분(구현/검증/기록 포함), scientific child 누적1800초,
process각900초(import/model load/all3/검증/직렬화 포함). RTX3070한개,
CPU/torch/TabICL threads2, heavy1, host RSS/private commitment16000000000bytes,
1초 watchdog, CUDA allocated/reserved/device capacity 기록. 가용 자원 사전 확인.
후보 예상상한426 context fit/predict + E041 pipeline4/정상neural12/metric16,
reference pipeline3/정상neural9/metric8. 실제 stage/call/fallback 수를 기록하고
상한을 실측처럼 쓰지 않는다. checkpoint load·반복 전처리·렌더링 비용도 포함.
기존 E041 CUDA-to-CPU fallback은 변경하지 않고 시간에 포함, 새 expert CPU
rescue 금지. 첫 오류/한도에서 자기 process tree 종료. 코드수정 후 추가run 금지.

결과/종료:
LOCAL_FULL_PATH_PASS는 전체 역할·출력·parity·두context·자원 검증 통과에만.
fake E거절을 후보 효과기각으로, 강제 활성경로를 실제정책 활성증거로 쓰지 않는다.
참조/후보 phase별 time/resource와 정상결정/engineering출력을 구분한다.
OOM/900초 초과는 LOCAL_RESOURCE_LIMIT, invariant/동등성 오류는
LOCAL_FULL_PATH_FAIL, 환경 미확보 BLOCKED_RESOURCE, 준비시간 부족 INCOMPLETE.
GPU 비결정성으로 exact parity가 깨져도 사후 tolerance로 통과시키지 않는다.
로컬 한도 실패를 H100 불가능으로 확대하지 않는다. 마지막 완료 단계와 비용을
기록해 S0가 H100 필요성을 판단하게 한다. 자동 유료서버/축소/튜닝/추가run 없음.

산출물:
새 entry/registration/source manifest/diff/dependency identity,
새 fixture hash/role schema, code/runner, boundary/parity checks,
reference 및 candidate 분리 result/resources/호출 내역, 누적 A040 비용,
exposure-ledger/verification/closeout/S0 handoff. status/log만 최소 갱신.
성공 시에도 실제 효과·H100·hosted900초·release PASS는 미확정. S0로 반환.

금지:
실제 응답/키/보호 Parquet·NPZ·기존 모델cache/VAF/기존 가짜자료 접근·재해시,
성공 tiny suite 반복, model/seed/head/context/grid/threshold 변경, 새 E기록,
네트워크 사용 모델 실행, 유료·원격·계정 접근, ZIP/checker/official release
all3/E025 release평가/업로드, tree/기존 snapshot 수정, commit/push·S2/S3.
Python audit만으로 OS/native egress PASS를 주장하지 않는다. 기존 offline
방어를 유지하되 native 차단 확인은 후속 release의 미검증 항목으로 남긴다.
E041 incumbent/E025 fallback, E057/E060/E061 parked 및 모든 STOP/HOLD 보존.
17999명/12339SSUID·A022 원래 역할·E059 소비oracle/selection과 보호audit2074/1177,
calibration1866 유지. A039 HOLD 별개, A_half 비승격, A018 미확정/S3 중단.
```
