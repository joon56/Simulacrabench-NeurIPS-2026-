# WB76-TABICLV2-GLOBAL-01 — 미래 단일 배치 제안

2026-10-26. **PROPOSED / MODEL_EXECUTION_NOT_AUTHORIZED.**
현재 **MODEL_BATCH_NOT_EXECUTION_READY / DEPLOYMENT_SPECIFIC_INPUT**이다.
아래420분 상한은 보존할 고정 제안이며 지금 실행 승인·시작을 추천하지 않는다.
[고정 계약](contract.md)이 과학 정책이다. r7 자동 배정은 이 실행 예산을 승인하지 않는다.
Root가 사용자에게 아래 하나의 envelope를 제시하고 실제 승인 문구·시각·epoch를 기록한
뒤에만 executor를 배정한다. 현재 E번호는 만들지 않는다. 구현 시작 전 root가 E번호와
`submissions/YYYY-MM-DD-E0XX` 경로를 배정하되 후보/정책/예산은 바꾸지 않는다.

## 범위와 입력

목적: 전체WB76 expert 한 후보의 로컬 full-path 가능성, 통과 시 조건부 S2 release.
별도 UNHCR 후보·A040/C6/C7/Modal 재개·다음 날 반복·두 번째 seed는 없다.
원본 A040 코드/실패/latch/inputs는 보존하고 새 작업 산출물만 생성한다.

미래 허용 source는 contract의 E041/E025 snapshot, A040 adapter·orchestration·observer·
schema_entry·runner, 고정 TabICL source/weight와 기존 두 interpreter/lock,
현재 public schema3개/config.yml/make_sandbox.py/score.py/tools/check_submission_zip.py,
필요한 직접 라이선스·dependency metadata다. Manifest 안의 모든 경로가 허용되는 것은 아니다.
추가 pure-Python vendoring은 기존 `tmp/a040-local-technical/venv/Lib/site-packages/`
아래 `einops`, `tqdm`과 각각 `einops-0.8.1.dist-info`, `tqdm-4.67.1.dist-info`의
source/metadata/license만 제안한다. 실제 identity·license/import closure가 먼저 확인돼야
하며 native psutil/Windows binary 복사, upstream API 제거·대체는 금지한다.
새 source는 `src/models/wb_tabicl_expert.py`, 새 해당 경계 테스트/조립·검증 script,
root 배정 E-output·submission 경로만. 실제 code 경로 목록/해시는 첫 모델 전에 동결한다.

이 문서의 정적 확인은 아래 숫자 파일을 열거나 재해시하지 않았다. 미래 S2에 한해서
다음 **3개** synthetic 입력의 identity를 검사하고 TRAIN/DEV projection만 허용한다.

| 정확한 경로 | 기록상 SHA256 |
|---|---|
| external/starter-kit/_sandbox/unicef/respondents.parquet | 8e7c659d277c5145c7a8a6d055ac59a7dd3c35699317741239b6b1969bce1488 |
| external/starter-kit/_sandbox/world_bank/respondents.parquet | 4592bed873410c5248edf1205e5cab41dd30494926e3b49f8da598e266758c8a |
| external/starter-kit/_sandbox/unhcr/respondents.parquet | 5d00075706e0a7beafdc8a70acfe07cde1f489048741eb2f3ae1fababdb72774 |

출처: `docs/analysis/E064-outputs/s2/numeric-identity.json` 및 E062 frozen-inputs.
기존 NPZ/raw probability/다른 Parquet/old fake/keys/cache/Adult/SIPP/VAF/보호 응답은
허용하지 않는다. 과거 CPU baseline은 새 GPU환경과 달라 숫자 재사용하지 않는다.
S1은 새 seed4500 full-shape fake family 한 번만 생성; S2는 위 기존 synthetic을 사용.
두 채널을 혼동하거나 full-shape fake의 양성 guard를 release 성능으로 쓰지 않는다.

Model worker는 TRAIN generated items와 DEV GIVEN/order만 요청한다. DEV PREDICT
전체를 NaN으로 넣고 EXCLUDE 제거. E025/E041/H source 출력 모두 freeze한 다음 별도
evaluator만 DEV truth를 읽는다. 공식 CLI staging에는 TRAIN/DEV만 넣고 원래 role/count/
schema/options/masked frame round-trip을 확인한다. TEST 행 요청0. 새 숫자 outputs도
배치 경로 안에 whitelist하고 세부 응답을 chat/telemetry에 노출하지 않는다.

## 고정 단계와 자동 gate

1. **Entry/구현:** 사용자 envelope, root dispatch/release/acceptance, 코드·checkpoint·
   환경·public contract identity, named jobs, resource 가용성을 먼저 확인. 실제 checkpoint
   hash는 승인 뒤 역직렬화 전 확인한다. **첫 checkpoint load/모델 fixture/fit 전에**
   기존 자산과 허용 pure-Python vendoring으로 offline 배포 경로가 성립하는지 정적
   DEPLOYMENT_FEASIBILITY gate를 먼저 닫는다. 현재 hosted psutil 등 의존성의 명시적
   설치 근거는 미확정이다. 공식 목록에 이름이 없다는 사실이 실제 부재 증거는 아니다.
   기존 허용 기록으로 충족을 입증하지 못하면 DEPLOYMENT_FEASIBILITY_HOLD로 반환하며
   full-path 예산부터 쓰지 않는다. 새 설치/원격/필수 requirements 삭제로 구제하지 않는다.
   배포 gate 통과 후에도 full-path 전에 위 synthetic3의 정확한 경로 존재/size 등
   파일 metadata와 기록된 출처·완료 provenance를 확인한다. 이 선행 확인은 숫자 내용/
   hash 접근이 아니며, S2의 허용 identity/projection 검사를 대신하지 않는다. 부재/출처
   미확정이면 release 입력 HOLD로 반환한다.
   원본 A040 성공 tiny suite를 다시 돌리지 않고
   새 WB/K26/역할/dispatch 영향 검사만 구현한다. 새 model implementation은 이때 시작.
2. **S1 technical:** tiny 새 경계 검사, fresh full-shape E041 reference all3 한 번,
   최대 active WB candidate all3 한 번. 자연 정책과 별도 engineering alpha.25 결과,
   exact controls/fallback, class/order/state/input/role/cost PASS가 모두 필요하다.
   부분 완료·시간/OOM·invalid probability·새 과학 정책 필요는 S2 gate 불충족.
3. **Conditional S2 entry:** 위 PASS, 동일 frozen source/policy, 잔여 누적 예산,
   synthetic3 identity/projection, 모델 interpreter/평가기 분리, dependency/build
   계약이 충족되면 같은 executor가 role receipt를 남기고 계속한다. 새 수동 인계 불필요.
   추가 설치·필수 의존성의 미확정·Linux native 경로 문제는 DEPLOYMENT_HOLD. 최소
   requirements를 빼서 PASS하거나 stock scorer 설치 동작을 우회하지 않는다.
4. **S2 release:** 같은 GPU model 환경에서 fresh E025/E041/H source all3 각1회.
   정해진 synthetic release gate 통과 뒤 assembly all3 한 번, ZIP checker와 실제
   추출본 stock official phase1 all3 한 번. 정확한 raw parity와 control invariant를
   확인한다. 성공한 source/reference는 이 배치 안에서 재사용하며 추가 fit하지 않는다.
5. **Closeout:** release-qualified 또는 technical/resource/deployment/adverse/HOLD
   중 원래 arm, 실제 usage·failures·출처·jobs·explicit release를 root에 반환한다.
   파일 준비는 upload 허가가 아니다. 실제 사용자 upload 결과가 오면 원래 arms로만 기록.

S1 local full-path PASS는 H100/hosted900초 또는 효과 PASS가 아니다. 배포 조건을 충족
못하면 source technical 결과만 반환한다. 이 가능성을 숨긴 무조건 S2 약속은 하지 않는다.

## 새 aggregate 상한 — 과거 예산 승계/재생성 없음

| 구분 | 새 gross | 모든 계산 child 누적 | all3 시작 | 부수·수리 포함 |
|---|---:|---:|---:|---|
| S1 | 180분 | 3000초 | 정상2, 최대3 | tiny/preparation<=180초; 나머지120초 여유. 무효 arm 재시도1 포함 |
| S2 | 240분 | 6000초 | 정상5, 최대6 | 부수 검사/조립/checker/준비600초; 무효 arm 재시도1 포함 |
| 전체 | 420분 | 9000초 | 정상7, 최대9 | 각 stage cap도 별도로 적용; 상호 초과 차용 없음 |

각 all3는 import/model load/모든 기관/output/관찰 overhead/종료까지 **공유900초**.
공식3 CLI 합도 wrapper 포함900초다. 원래 공식 per-instrument timeout을900초로 각각
쓰기만 하고 총2700초를 허용하지 않는다. Prep·실패·stock checker·기존 E041 CPU retry도
실제 parent wall에 한 번씩 계수한다. 중첩 phase spans는 또 더하지 않는다.
S1/S2 마지막 각15분은 기록·owned-job 종료용으로 남긴다. 조기 종료는 미사용 시간 소비
명분이 아니다. 새 agent/process/context/date가 시작·시간·노출 수를 초기화하지 않는다.

기존 RTX3070 하나, numerical CPU2,heavy1. Owned controller+descendants의 RSS와
private commitment 각각<=16,000,000,000bytes; 시작 physical/commit 가용성도 각각
16,000,000,000bytes 이상. CUDA capacity/allocated/reserved를 별도 기록한다. 기존
guard를 낮추거나 다른 앱을 종료하거나 paging/환경을 바꾸지 않는다. Expert offload/
CPU rescue 없음. Monitor gap/종료 증거 누락은 PASS가 아니다. cash0,remote0,install0.

### 호출 회계

WB 활성 candidate all3: E041 pipeline4/neural `_train`12/UNHCR metric minimization8,
expert fit/predict 각각최대152(76shadow+76final),checkpoint import1. E041 reference
all3는3/9/8, E025는3/9/0. WB shadow에는 UNHCR metric8개를 추가하지 않는다.
최종 ladder table600개 기대(UNICEF19+WB2x106+UNHCR369); 내부 selection tables,
lambda replay,donor/ranking/render 및 hierarchical class 연산은 별도 실제 비용으로 관찰.

| 범위 | pipeline | neural `_train` | metric minimize | expert fit/predict 각각 최대 |
|---|---:|---:|---:|---:|
| S1 정상 reference+candidate | 7 | 21 | 16 | 152 |
| S1 최대, candidate 무효 arm1 추가 | 11 | 33 | 24 | 304 |
| S2 정상 E025+E041+H+assembly+official | 18 | 54 | 32 | 456 |
| S2 최대, candidate 무효 arm1 추가 | 22 | 66 | 40 | 608 |
| 전체 정상 / 최대 | 25 /33 | 75 /99 | 48 /64 | 608 /912 |

Singleton/불활성 시 expert 수는 줄 수 있으나 예산에서 미리 공제하지 않는다. 기존
E041 GPU-to-CPU fallback까지 `_train_on` 최대198, 그 시간도9000초 안이다. Tiny/checker
등 부수 경로 전체 expert fit/predict 각각64회 이하,checkpoint load6회 이하 추가 상한.
Tiny 모델 suite 최대2cycle이며 새 영향 검사만,180초 안; 실패 보존. 부수 fixture에서
E041 optimizer fit은 허용하지 않는다. Official3 CLI는 import/load3회라 정상 전체
full-path checkpoint load6회, 두 무효 arm이 최대로 쓰면10회; 부수까지 최대16회.
152predict는 hierarchy 내부 attention/classification 연산 수의 상한이 아니다.

### 예산 근거와 수리 규칙

A040 tiny retry1 parent40.831초(F45/query9), E041 full reference123.218초,
UNHCR candidate900.036초 capped;shadow expert338.430초,final expert 미완료.
WB는 head 수가 적지만 K>10이19개/max26이며 context/query도 다르다.76/213 환산 또는
최종 시간 보장은 하지 않는다. E062 S2 actual1257.289초/2400초, E064 charged1827.881초/
3600초는 작은 CPU package의 기록이다. 새 pretrained release와 동일 비용으로 보지 않는다.
S2 fresh baseline3개+assembly+official로 중복 없는5회가 필요해6000초 ceiling을 둔다.

일반 구현·인자·로그·encoding·observer 오류는 같은 executor가 최소 수정하고 실제
영향 경계만 확인한다. 각 stage의 무효 all3 arm 예비1회와 모든 상한 안에서만 계속한다.
유효 adverse/timeout/OOM/정책 실패 뒤 head/context/seed/alpha/guard를 바꿔 재시도하지
않는다. 성공 unchanged all3/suite 반복 금지. 역할·label 경계 위반, source/input 변동,
새 설치/비용·과학 기준 필요, 소유권 불명, cap 소진은 root 반환. Remote branch 자체 없음.

## 공개 결과 판독 — 실제 업로드는 별도

Comparator E041 ID933094: Grand.6433333333/UNICEF.5200000000/WB.4900000000/
UNHCR.9200000000. Package source/hash와 실제 업로드 bytes/time/ID/account/phase/scorer
근거는 분리한다. 사전 SCORES에 아래 arms를 그대로 기록한다.

- **Favorable:** 비교 가능한 Finished, WB와 Grand 모두 상승, 두 공개 control값 동일.
  전체 guarded procedure의 noisy 긍정 관측. 정확한 gain·expert 단독 인과·TEST 채택 아님.
- **Adverse:** 비교 가능한 WB 또는 Grand 하락. 반대 방향이나 control 변화도 함께
  보존하고 attribution mixed로 표시. 후보 parked; seed/threshold/동일 재제출 구제 없음.
- **Unresolved:** WB/Grand 동점 또는 한쪽만 상승하고 다른 쪽 동점. 작은 효과/비활성/
  noise/rounding 구별 불가. 좋은 방향이 있어도 가설 입증·효과0로 해석하지 않는다.
- **Mixed:** control값 변화 또는 WB/Grand 반대 방향; 부호 facts와 adverse 여부는
  함께 기록하되 WB 개입으로 단독 귀속하지 않는다. 로컬 controls exact 의무는 별개다.
- **Technical:** build/import/offline/output/runtime/isolation 실패. 효과 결론 없음.
- **HOLD:** 공개 점수를 비교할 필수 component/API precision/phase 또는 출처가 부족하거나 모순이면
  판독 HOLD. 사용자/API 제공 점수는 그 근거 수준으로 기록한다. 원격 bytes/hash나 scorer
  완전 동일성 미확정만으로 공개 판독을 항상 막지 않는다(E064 관례); 그 경우 고정 local
  artifact와 remote 실행의 연결·정확한 효과/귀속은 미인증으로 남긴다. 누락 사실만 확보;
  새로운 fit·noise averaging·계정/slot polling 자동 승인 없음.

누구도 Grand에서 hidden 기관 값을 역산하거나 alpha/응답 통계를 예측 출력에 부호화하지
않는다. E041 incumbent/E025 fallback와 모든 parked/STOP/HOLD/보호 노출 유지.
현재 root가 결정할 것은 **DEPLOYMENT_SPECIFIC_INPUT을 얻는 최소 범위**다. 필요 입력은
현재 공식 hosted 필수 dependency(특히 compatible psutil와 나머지 import closure) 증거,
또는 stock scorer/필수 dependency를 포함하는 별도 유한 isolated install·배포 검증 범위다.
후자는 새 사용자 권한이 필요하며 이 제안에 자동 추가하지 않는다. 해소 전에는420분
모델 배치를 실행 추천하지 않는다. 별도 S3/TEST 선택,실제 upload,권리자의 license grant,
paid/cloud,commit/push도 포함되지 않는다. 이번 정보 작업은 이 구체적 gap에서 종료한다.
