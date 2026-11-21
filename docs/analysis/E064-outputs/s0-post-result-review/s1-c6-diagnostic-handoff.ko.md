# S1-A040-C6 — 모델 없는 종료 crash 충분성 비교 한 건

**PROPOSED / NOT_EXECUTED. 이 문서 작성은 실행 허가가 아니다.**
사용자가 별도 실행 세션에 아래 범위를 지시할 때만 새 허용량이 생긴다.
S1 기술 진단이며 S2 자동 전환·새 후보/E 기록·A040 전체 재개를 포함하지 않는다.

## 시작과 소유권

작업 폴더 `C:\Users\USER\Desktop\SimulacraBench`.
기준 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; dirty 상태이므로 HEAD만 믿지 않는다.
AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신3개, docs/workflow.md 순서로 읽고
현재 역할·실제 개정·workflow 해시·허용 범위를 기록한다. r6의 일반 오류 수리 원칙 적용.

먼저 같은 폴더의 [결정](decision.md), [entry](entry.json), [검증·쓰기 해제](verification.json)를 읽는다.
Outgoing S0-E064-POST-RESULT /root의 명시적 해제와 현재 HEAD/dirty/named jobs 확인 후
incoming S1-A040-C6가 단독 인수한다. 다른 writer/진행 중 관련 작업이 있으면 쓰지 않는다.
원본을 과거 manifest에 맞추려고 되돌리지 않는다. 문서 해시와 실행 소스 해시를 구별한다.

## 질문·근거·허용 입력

질문 하나: **C3 image 정의-only 대조에 fixture FunctionCreate protobuf 응답 graph의
생성·실제 FunctionInfo parser 소비만 추가해도 Windows native 종료 crash가 재현되는가?**
사전 모델/과학 결과나 실제 응답은 필요 없다. 통계적 이득 oracle이 아닌 기술 충분성 비교다.

원래 경로 `docs/analysis/A040-outputs/local-exit-diagnosis1/`에서 읽을 자료:

- C6-registration.md, c6-blocked-receipt.json, closeout.md, reproduction.md,
  regression-history.md, verification.json, source-register.md,
  source-manifest.json/artifact-manifest.json, 해당 C3/C5의 process/stderr/동결 기록.
- 로컬 검사 source `check_boundary.py`, `run_check.ps1` 및 이 두 파일의 진단 분기가
  직접 쓰는 SDK 대역/fixture source. 필요하면 source manifest로 정확한 경로부터 확인한다.
  넓은 모델/데이터 검색 대신 진단 의존성만 목록화한다.
- 설치 환경 `tmp/a040-modal-full-path1/sdk-venv/`의 pyvenv.cfg/관련 METADATA와
  Modal/protobuf/FunctionInfo/동기화 경계의 직접 설치 소스. 환경 수정·설치 금지.
  Python3.13.14/Modal1.6.0/synchronicity0.12.5/protobuf6.33.6/grpclib0.4.9는
  역사 기준이다. 현재 identity와 과거 기준의 대응을 먼저 확인한다.

C6는 코드가 준비됐지만 시간 gate로 실행되지 않았다. 기존 C3는 정상 exit0이다.
C4의 await 관측 제거, C5의 output wrapper 제거는 진단용 변화이며 수리 후보가 아니다.
현재 latest source manifest를 모든 과거 시도의 공통 source로 오인하지 않는다.
C3와 C6의 공통 코드/환경을 per-attempt 기록과 source diff로 연결하고, 차이를 위
graph/parser 한 가지 및 관측/경로 배치에 한정할 수 있어야 한다.
그 대응이 불충분하거나 환경이 달라졌다면 BLOCKED_IDENTITY로 종료한다.
이를 해결하려고 C1–C5를 재실행하거나 새 환경을 설치하지 않는다.

## 새 예산·허용 작업

- 새 gross **30분**, 마지막 **5분 closeout**. 읽기·수리·실패·기록까지 포함하며 연장하지 않는다.
- 진단 자식/영향검사 총 wall **90초**, 각 자식 **30초 이내**. 최대 **3회 시작**.
  정상적인 C6 진단 측정은 **1회**뿐이다. 나머지 최대2회는 parser 경계에 도달하기 전
  인자/경로/관측기 등 일반 오류의 영향 검사·무효 실행 수리에만 쓴다. 전부 합산한다.
  감독·정리 시간도 합계에 포함한다. 각 호출은 실행25초/정리5초 안으로 설계하고,
  실제 초과 시 LIMIT로 기록한다. 30초 대기 뒤 정리를 추가해 준수했다고 하지 않는다.
- CPU2/GPU0/heavy1, owned process tree의 sampled RSS/private 각각 **2GiB** 한도.
  예산·감시·자기 tree 종료 근거를 기록한다. 표본 peak를 연속 상한 증명으로 표현하지 않는다.
- 현금/클라우드 사용 **0**, 모델/과학 호출 **0**. 과거 예산·남은 allowance 재사용 없음.

새 폴더 `docs/analysis/A040-outputs/local-exit-c6/` 충돌 확인 후 생성한다.
원래 검사 코드를 새 위치에 복사해 정적 검토하고, 필요한 최소 경로/새 deadline/진단
진입점·관측기 수리를 같은 세션에서 수행할 수 있다. 원래 폴더/실패/deadline/latch 불변.
실제 SDK를 사용하되 인증·외부 RPC·설치·프로필/토큰 접근을 차단한 모델 없는 검증만 허용한다.
Windows 내부 event-loop IPC는 외부 네트워크와 구별한다. 차단을 무력화해 검사를 통과시키지 않는다.
실행 전 새 검사 source/input fixture/environment 식별과 금지 경로를 동결한다.

실제 응답 graph/parser까지 도달한 crash 또는 정상 종료는 **유효 관측**이다.
불리한 결과라는 이유로 무효화/수리 후 재측정하지 않는다. 관측기 결함으로 판단 불가면
INCONCLUSIVE로 남기고, 이 문서의 한 건 측정 권한을 늘리지 않는다.
작은 구현 오류마다 S0에 반환하지 않되, 목적·입력·예산·판정 기준은 바꾸지 않는다.

## 판독·종료 조건

1. 경계 도달 확인 후 c0000005 재현: **SUFFICIENT_TRIGGER_REPRODUCED**.
   이 테스트 환경에서 더 작은 경로의 충분성을 지지한다. upstream protobuf 결함이나
   전체 root cause로 단정하지 않는다. 정확한 최소 경로와 별도 수리에 필요한 근거만 인계한다.
2. 경계 도달·assertion 충족·실제 정상 exit0: **NOT_REPRODUCED**.
   graph/parser만의 충분성을 지지하지 않는다. build/resolve 복합 경로는 미해결이며 HOLD 유지.
3. identity/차단 경계 부족, 다른 실패·timeout·초과·잔여 프로세스:
   **BLOCKED_IDENTITY / BLOCKED_BOUNDARY / INCONCLUSIVE / LIMIT** 중 근거에 맞게 기록한다.

자식 파일의 PASS/assertion만으로 정상 종료라 하지 않는다. 감독자 exit code와 Windows
native 종료, 실제 경계 도달·잔여 PID까지 확인한다. os._exit, GC 비활성화, 예외 무시,
backend/version 교체로 종료를 우회하지 않는다. 유효 C6 결과 뒤 추가 수리는 이 범위 밖이다.
원인 기반 다음 수리 제안은 가능하지만 C7·전체 suite·120초 stall·원격 재시도는 실행하지 않는다.
예비 작업은 누락 조건·실패·소비 비용의 closeout뿐이다.

## 금지와 산출물

금지: 실제 Image.build/resolve, mount thread pool 실행, live authentication/RPC,
기존 원격 Sandbox 조회/생성/종료, H100·유료 자원, 설치/버전 변경, 112 payload/checkpoint/
가짜 모델 입력/Parquet/NPZ/키/응답/cache/VAF 접근·해시, 모델 import/fit/predict/score,
기존 성공 suite·과학 반복, 모델/seed/head/context/threshold 변경, ZIP/제출/commit/push,
서브에이전트·S2/S3·TEST 선택. 기존 실제 Sandbox 종료 확인은 재검사하지 않는다.

새 폴더에 최소한 다음을 남긴다: entry/사전 source·environment 식별, 원래 코드 대비 diff,
C6 assertion/경계 도달/프로세스 exit·stderr·자원 receipt, 실패·수리·시간 합계,
closeout.md와 s0-handoff.ko.md, 보존·named jobs·쓰기 해제 verification.json.
status/log에는 현재 결과와 링크만 추가한다. 옛 실험/결과/SCORES/tree/모델/환경은 수정하지 않는다.
모든 소유 자식 종료와 명시적 writer 해제 후 S0로 반환한다. 다른 세션 작업 종료 금지.

E041 incumbent/E025 fallback, E057/E060/E061/E062/E063/E064 parked,
E062/E063/E064 공개 tie UNRESOLVED, 모든 STOP/HOLD와 A039/A040 유지.
17999명/12339SSUID·집계/A022 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격, A018 미확정/S3 중단 승계.
어느 C6 판독도 실제 효과·전체 lifecycle/release PASS나 S2 후보를 만들지 않는다.

## 사용자용 실행 요청 — 별도 S1에 전달할 때만

```text
이 세션을 S1-A040-C6 기술 진단 실행자로 지정한다.
C:\Users\USER\Desktop\SimulacraBench\docs\analysis\E064-outputs\s0-post-result-review\s1-c6-diagnostic-handoff.ko.md를 읽고 그 범위만 실행해줘.
새 gross30분/진단 자식 합90초·최대3회 시작/유효 C6 측정1회/현금0을 승인한다.
일반 진입 오류는 같은 세션에서 한도 안에 수정하되, 모델·원격·환경 변경·추가 비교·S2/S3는 금지한다.
기존 writer 해제와 source/environment 대응을 먼저 확인하고, 결과·비용·보존·쓰기 해제를 남겨 S0로 반환해줘.
```
