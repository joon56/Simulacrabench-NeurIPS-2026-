# S1 — A040 계측 충돌 수정 및 고정 로컬 계약 1회 재검증

작성 자체는 실행 허가가 아니다. 사용자가 별도 S1에 아래 범위를 지시하면
그 세션에서 수행한다. S0에서는 코드 수정·실행하지 않았다.

```text
SimulacraBench / HSCC S1 — A040 계측 수정 및 제한된 재검증.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md → CLAUDE.md → docs/status.md → docs/log.md 최신3개 →
docs/workflow.md를 읽고 실제 개정·S1 technical 역할·범위를 보고한다.
HEAD/dirty/active jobs 확인. 원래 실패 산출물·기존 변경 보존.
다른 세션/서브에이전트·commit/push·S2/S3 실행 금지.

필수 입력:
- docs/analysis/A040-outputs/s0-local-failure-review/{decision.md,verification.json}
- docs/analysis/A040-outputs/local-technical/{closeout.md,result.json,resources.json,
  verification.json,provenance.md,requirements.lock.txt,exposure-ledger.md,
  runner.py,tests_local.py,prototype.py,watchdog.py,scientific-started.json}
- 같은 폴더 frozen-inputs/{registration.md,run-manifest.json}
- docs/analysis/A040-outputs/s0-policy-resolution/decision.md

기존 설치·취득 승인과 주최측 runtime 정책 해소를 승계한다. 다시 문의하거나
설치를 반복하지 않는다. 이번 지시는 아래 계측 수정과 새 scientific run1회만
허용한다. 원래 LOCAL_CONTRACT_FAIL은 역사로 보존한다.

목적/차이:
event(name,**values)에 event('many_class_head',name=name,...)를 전달한
계측 충돌을 수정하고, 중단된 동일 로컬 계약을 완결한다. 모델·가설·정책을
변경하거나 유리한 결과를 찾는 실험이 아니다.

보존/위치:
새 docs/analysis/A040-outputs/local-technical-retry1/ 및
tmp/a040-local-technical-retry1/만 사용한다. 이미 있으면 상태 확인 후
덮어쓰기/삭제 금지. 원래 local-technical/ 코드·manifest·latch·결과·events와
원래 fixture를 보존한다. latch를 지워 원래 명령을 재실행하지 않는다.
기존 승인된 tmp/a040-local-technical/venv와 고정 public source/checkpoint만
재사용. 다른 모델/cache/응답 접근 및 새 설치·모델 취득 금지.

수정 허용:
retry copy의 해당 호출 metadata key를 name에서 head_name으로 바꾸는 최소
수정 우선. 소비자·모든 event 호출의 binding 확인. prototype.py 원본 바이트,
모델 options/deps/seed/head/context/정책/assertion/tolerance 유지.
새 출력·fake fixture 경로, 독립 latch, 새 entry+60분 deadline, manifest 연결만
기계적으로 조정한다. 과거 고정 deadline이나 원래 latch를 변경하지 않는다.
source/checkpoint 경로는 기존 승인 바이트를 가리킨다. 원본 대비 diff 기록.
더 넓은 모델/검증 변경이 필요하면 실행 전 근거를 남기고 S0로 반환한다.

1. 모델 없는 logging regression 먼저:
stdlib만 사용; torch/TabICL/prototype/scientific runner import 금지.
runner는 import만 해도 파일을 열므로 실제 event 정의만 AST 등으로 추출해
메모리 sink에서 검사한다. 별도 logger 복제품만 고쳐 통과시키지 않는다.
원래 호출 TypeError와 수정 호출 JSON의 event/head_name/classes 보존 확인.
실제 다른 call site도 인자 binding 확인. 총60초 이내; 실패하면 모델 실행0.

2. 동결 후 scientific invocation1회:
retry code/registration/정확 pins/새 deadline과 허용 source/checkpoint 해시
동결. checkpoint 바이트 확인 후만 로드. 보호 데이터는 재해시하지 않는다.
seed4000, F45/S3/E3/Q3,17 GIVEN/213 targets/834칸, 기존 수치 assertion 유지.
같은 생성 코드로 새 tmp에 fixture 재생성, 기록된 원래 SHA256
a532ee2dcd337cc72e278365234e7b55b08aec528a9bc9a1b718d666ee0d5a48과 비교.
원래 fixture/partial predictions를 읽어 이어붙이지 않는다.
fresh process에서 원래 suite 전체1회. 성공 prefix는 shared-state/counters/
before-after hash 일관성을 위한 필수 회귀로만 포함한다. 별도 반복 금지.
all213·네 K>10 heads·1917 canonical vectors, 실제 fake-model S/E 선택/guard,
final frozen parameter/buffer equality,216fit/217predict/2load 및 원래
fallback/injection 수를 모두 확인한다. 실제 E041 pipeline 실행은 금지한다.

비용/종료:
작업 wall60분(수정·검증·기록 포함), model-free60초, scientific child1개/120초.
RTX3070한개/CPU2/heavy1, host cap16000000000bytes,1초 process-tree RSS/private
commitment 감시, GPU allocated/reserved 기록. 첫 오류/한도에서 자기 tree만 종료.
deadline 연장·두 번째 scientific process·seed/head/context/grid/threshold/
tolerance 구제 금지. 원래1회와 이번1회의 비용을 각각 기록하고 누적도 합산한다.

산출물:
logging-regression 결과, 원본 대비 diff, entry/frozen manifest/registration,
events/result/resources/exposure-ledger/verification/closeout/S0 handoff.
전체 suite 통과만 LOCAL_CONTRACT_PASS. logging 수정만으로 PASS 금지.
계약 오류 LOCAL_CONTRACT_FAIL, 자원한도 LOCAL_RESOURCE_LIMIT, 시간부족
INCOMPLETE, 환경 누락 BLOCKED_RESOURCE. 실패/누락 closeout만 예비 작업.
새 실패를 즉시 추가 수정·재실행하지 않는다. status/log 최소 갱신 후 S0 반환.

금지/한계:
실제 응답·키·보호 Parquet/NPZ·기존 모델cache/VAF 접근·재해시,
실제 E041/all3/full-context/refit, H100/유료서버/계정접근, 새 E기록,
ZIP/checker/official release score/업로드, tree/원래 manifest/submissions 수정,
commit/push·S2/S3/TEST 선택. 고정 공개 checkpoint 검증·로드만 예외다.
tiny fixture PASS는 효과·900초 전체경로·H100·release PASS가 아니다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 기존 STOP/HOLD 보존.
A040 규칙 해석은 해소 상태, 원래 local failure는 역사로 보존.
17999명/12339SSUID·A022 원래 역할·E059 소비 oracle/selection 및 보호
audit2074/1177·calibration1866 유지. A039 HOLD 별개, A_half 비승격.
A018 미확정/S3 중단. PASS여도 S0 검토 전 S2 이관하지 않는다.
```
