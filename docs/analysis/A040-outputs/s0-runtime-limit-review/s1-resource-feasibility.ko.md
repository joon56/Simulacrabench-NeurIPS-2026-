# S1 — A040 H100 재현환경·전체 비용 확인: 정보 조사만

문서 작성은 실행 허가가 아니다. 사용자가 별도 S1에 아래 정보 조사를 지시할 때
적용한다. H100 임대·접속·설치·모델 실행 프롬프트가 아니다.

```text
SimulacraBench / HSCC S1 — A040 resource feasibility information only.
작업 폴더 C:\Users\USER\Desktop\SimulacraBench
기준 HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS → CLAUDE → status → log 최신3개 → workflow.md를 읽고 실제 개정·
S1 information 역할·허용 범위를 보고한다. HEAD/dirty/active jobs 확인·보존.

입력(모두 docs/analysis/A040-outputs/ 아래):
- s0-runtime-limit-review/decision.md, verification.json
- full-path-resume1/closeout.md, resources.json, verification.json,
  candidate/partial-observations.json, source.diff, frozen-inputs/manifest.json
- s0-policy-resolution/decision.md 및 s1/contract.md, cost-accounting.md
  기존 자원 조사 내용이 있으면 우선 재사용하고 새로운 미확정 조건만 확인한다.
manifest는 metadata만 읽는다. 열거된 입력/모델/cache를 열거나 해시하지 않는다.

판단 질문:
동결된 A040 전체 경로의900초 계약을 실측할 H100 환경을 실제로 확보할 수
있는가? CPU/OS/의존성/메모리/오프라인 조건 차이와 총비용까지 구체화할 수
있는가? 현재 RTX3070/CPU2에서는 candidate900초 초과. H100 결과는 미확정.

기존 작업과의 차이:
TabICL 모델/API 적합성·schema·시작 메모리를 다시 조사하지 않는다.
실측된 전체 경로를 옮길 수 있는 명명된 자원·비용·접근 조건만 확인한다.
가짜 S/E 수락은 실제 효과 증거가 아니며 임대 타당성을 수익처럼 계산하지 않는다.

허용:
기존 기술 문서/공개 소스의 읽기 전용 검토, 필요한 공개 공식 자원 문서 조사.
최대45분, 최대2개 자원 제안/새 공식 문서6개. 공식 가격·사양·과금/종료 조건의
URL·조회일·확인 범위를 남긴다. 이미 사용자에게 제시된 특정 환경이 있으면
그 환경을 먼저 확인한다. 공급사 광고로 실제 재고·계정 권한을 확정하지 않는다.

각 제안에 필요한 정보:
- 정확한 H100 형태/VRAM, 전체 GPU 여부와 MIG/공유 여부, RAM/vCPU,
  OS/container/driver/CUDA와 고정 TabICL·E041 환경의 차이.
- setup/install/weight 취득·검증과 실행 단계의 네트워크 분리 가능 여부,
 16GB host 한도·CPU2·단일 GPU·자기 process tree/time cap을 집행할 방법.
- 실제 계정/기관 권한 확인 주체, 비용 단위/최소 과금/스토리지/전송/종료 후
  청구 여부. 설치·취득·환경 준비도 유료 시간에 포함한다. 알고 있는 단가와
  미측정 setup 시간을 분리하고 전체 비용의 보장을 지어내지 않는다.
- 후속 실행 전 필요한 사용자 총지출 상한·자원 선택. 미제공이면 미확정으로
  남긴다. 예산을 임의 설정하거나 문의/구매/무료체험 가입을 대신하지 않는다.

후속 실행 제안은 범위까지만:
동일 모델/context/head/alpha/guard/입력 유지, 새 target reference와 candidate
각1회/각900초·전체 검증·새 출력·첫 오류 STOP을 기본으로 명시한다.
Windows 경로/RTX3070 assertion/watchdog의 이식 필요성을 밝히고, 환경 변경에
따른 exact parity/의존성 검증을 계획한다. 과거 실패를 PASS로 바꾸지 않는다.
부분 head 시간으로 전체 완료시간/H100 배속을 외삽하지 않는다.
완료 로그의641.0873초는 expert predict 호출+CUDA 동기화 시간이며 GPU 단독
시간이 아니다. 정책 축소/즉석 최적화/deadline 연장 제안으로 대체하지 않는다.

종료:
구체적인 환경·조건·비용·미확정 사용자 입력을 확보하면
RESOURCE_OPTION_DOCUMENTED / EXECUTION_NOT_AUTHORIZED로 S0 반환.
환경/접근/예산 조건이 부족하면 HOLD_SPECIFIC_INPUT. 빠진 사실·확보 주체·
재개 조건만 기록하고 같은 검색을 반복하지 않는다. 정당한 예비 작업은 closeout.

산출물:
새 docs/analysis/A040-outputs/resource-feasibility/ 경로의 entry,
source-register, 최대2개 옵션 비교, 비용/포팅 범위, exposure-ledger,
verification, closeout, S0 handoff. 경로 충돌 먼저 확인. status/log 최소 갱신.
새 A/E번호 불필요. 실행용 모델 코드·실행 latch·ZIP은 만들지 않는다.

금지:
계정/인증정보 탐색·로그인·문의 발송·접근 신청·임대·결제·원격 접속,
설치/취득·container build·모델 import/fit/predict/score·fixture/test,
기존 입력/응답/키/Parquet/NPZ/checkpoint/cache/VAF 읽기·재해시,
새 모델·seed/head/context/guard 탐색·최적화 구현·부분상태 재개,
ZIP/업로드/기존 snapshot/tree 변경·commit/push·다른 세션/서브에이전트·S2/S3.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD,
17999명/12339SSUID·A022 원래 역할·집계 노출·E059 소비oracle1918/1124 및
selection2007/1130, 보호audit2074/1177·calibration1866 보존.
A039 HOLD 별개, A_half 비승격, A018 미확정·S3 중단·S2 후보 없음 유지.
```
