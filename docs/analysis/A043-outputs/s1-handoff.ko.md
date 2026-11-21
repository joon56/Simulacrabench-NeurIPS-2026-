# S1 제안 — A043 UNHCR 조건부 gradient 경로 계약

S0의 다음 작업 제안. **이 파일 작성·존재만으로 실행을 시작하지 않는다.**
사용자가 별도 S1에 아래 범위를 전달했을 때 그 정보·설계 작업만 수행한다.
새 모델 구현·실험·S2·제출 권한이 아니다.

```text
SimulacraBench / HSCC — 이 별도 S1에서 A043 정보·설계 검토 한 건을 수행한다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
기준 HEAD: a43f4379ec78dbc2de260463eef67bb1d567d7e1

AGENTS.md, CLAUDE.md, docs/status.md, docs/log.md 최신 3항목,
docs/workflow.md 순서로 읽고 역할·현재 개정·허용 범위를 보고한다.
HEAD/branch/dirty/named active jobs를 확인하고 기존 변경을 보존한다.
S0는 workflow 2026-10-05-r5를 읽었다. 현재 지침이 다르면 현재 것을 읽는다.
문서 해시만으로 읽기·준수를 주장하지 않는다.

입력:
- docs/analysis/A043-post-e063-priority.md
- docs/analysis/A043-outputs/entry.json, verification.json
- docs/analysis/E063-outputs/s2/post-result/{result.ko.md,comparison.json,exposure-ledger.md}
- docs/experiments/E012-shared-trunk.md, E061-tied-content-heads.md,
  E060-content-target-retrieval.md, E062-wb-ordinal-heads.md,
  E063-round-conditioned-metric.md
- docs/analysis/A033-dev-handoff-and-role-repair.md,
  A037-winning-priority-review.md, A042-post-e062-priority.md
- src/models/shared_trunk.py, link_sharp.py, supervised_retrieval.py,
  hh_cap.py, logit_blend.py, tied_content_heads.py
허용 생산 소스의 직접 import 대상은 필요한 함수의 텍스트만 추가 확인 가능하다.
import/실행은 금지다. 파일 identity는 entry의 허용 소스/문서 해시와 비교한다.
HEAD만으로 미커밋 소스를 식별하지 말고, 차이는 경위를 기록하며 되돌리지 않는다.
manifest에 있는 데이터/캐시/ZIP 경로는 접근 허가가 아니다.

목적:
E041 UNHCR의 독립 asked-only conditional head는 계속 학습시키되, 그 CE가
공유 trunk로 전달하는 직접 gradient만 차단하는 한 개입의 구현 계약과
판독 가치를 확정하거나 기각한다. 새로운 효과를 입증하는 과제가 아니다.

현재 알려진 사실을 반복하는 조사로 끝내지 않는다. shared_trunk는 full/cond에
같은 z를 주고 두 CE와 셀 수를 합친다. conditional heads는 실제 출력에 쓰인다.
공동 학습은 E012의 장점이기도 하며, gradient 충돌·실제 손해는 미측정이다.
E061은 logits tying/독립 head 제거였고 hosted adverse였다. 이 질문은 독립
head·파라미터·초기화·forward 함수족을 보존하는 직접 gradient 경로 변경이다.

확인할 미해결 내용:
1. 생산 E041의 tune hook부터 inner-stop/outer config/w/final refit와 최종
   gate/evidence renderer까지 full/cond의 실제 소비·학습 경로를 연결한다.
   stop-gradient가 제거하는 직접 영향과 남는 간접 선택 영향을 명시한다.
   masked PREDICT/visible TRAIN 경계도 source로 추적한다.
2. 동일 상태의 forward logits/CE/denominator/파라미터 순서/RNG 소비를
   유지하면서 trunk gradient만 바꿀 계약을 수식으로 명시한다.
   conditional head gradient, Adam weight decay/state, dropout, empty asked
   mask, fallback을 빠뜨리지 않는다. 초기 동등성을 학습 후 동등성으로
   확대하지 않는다. conditional target의 전체 영향 제거라고 부르지 않는다.
3. 원래 알고리즘(config2, seed, split, early stop, w 선택, 최종 refit,
   K32/metric/renderer, lambda minimum30/zero fallback)을 고정할 수 있는가?
   산출 epoch/config/w/activity/lambda는 학습 결과로 달라질 수 있다.
   알고리즘 변경·결과값 강제 고정·별도 selector·loss 계수 탐색은 제안하지 않는다.
4. 기존 E061/E060/E062/E063 및 과거 base 실험과 같은 질문인지 비교한다.
   공동 학습 제거의 손해 가능성, conditional 출력 수요와 전체 절차 귀속을
   명시한다. 단순히 다르다는 이유만으로 가치 있다고 판정하지 않는다.
5. 향후 한 R/H 비교와 clean E025/S2 잔여까지 포함한 전체 호출·시간·메모리
   계획을 만든다. 정상 arm3 pipeline/9 neural/8 metric, refit 포함이라는
   S0 계획을 source로 확인하고 조건부 fallback/검증 비용을 따로 적는다.
   과거 E063 실측을 새 실행 보장으로 쓰지 않는다. 새 환경·클라우드는 제외.
6. 구현 전 유효한 수치 oracle이 없는 이유, 노출된 synthetic의 공학 한계,
   실제 hosted 전체 정책 favorable/adverse/unresolved/technical/HOLD 판독과
   무엇이 다음 행동을 바꾸는지 명시한다. 기존 공개 동점으로 미세 효과를
   구별할 수 있다고 주장하지 않는다. 현재 E041 손실 지도를 확보했다고
   쓰거나 E025의 과거 분해/E049 oracle을 재사용하지 않는다.
7. 미래에 필요한 최소 영향 검사를 설계하되 실행하지 않는다:
   초기 forward/state/RNG parity, gradient 전달/차단과 cond 학습 가능성,
   마스킹·선택/refit 경계, UNICEF/WB controls, 전체 UNHCR 출력/비용.

범위·비용:
정보·수식·정적 소스 검토 한 건. 총 gross 40분(마지막 10분 기록 포함).
모델/과학 계산 0, 현금/원격 0. 기존 정보로 해결하면 일찍 종료한다.
기존 기록과 허용 source/doc 해시만 읽는다. 공개 schema 텍스트는 필요한 경우만.
새 웹 조사·다운로드·문의·설치·auth/RPC·응답/키/Parquet/NPZ/cache/ZIP 접근·해시,
모델 import/autograd/fit/optimizer/predict/score/fixture/test 실행은 금지다.
모델/실험 코드·기존 연구·snapshot·tree 수정, E064 생성, commit/push,
서브에이전트·S2/S3·TEST 선택도 금지다. 작은 코드 실행을 수식 조사로 부르지 않는다.
문서 작성 도구의 일반 오류는 같은 범위/총시간 안에서 고치고 계속한다.

종료 판정:
- CONTRACT_READY_FOR_S0_REVIEW: 위 미해결 계약·전체 비용·향후 판독을
  한 개입으로 구체화하고 제한된 구현/기술 검증의 판단 입력을 확보함.
  효과·모델·release PASS 또는 다음 실행 허가가 아니다.
- REJECT_DUPLICATE_OR_UNINFORMATIVE: 과거 질문 재포장, 결정 가치 없음,
  또는 conditional predictor를 실질적으로 학습하지 못하게 하는 설계.
  이유를 기록하고 새 모델/계수/데이터 경로로 전환하지 않는다.
- HOLD_SPECIFIC_INPUT: 중요한 경로·권한·전체 비용 조건이 남으면 누락 입력,
  확보 주체·허용 작업·재개 조건만 명시한다. 같은 HOLD 검토 자동 반복 없음.
실제 효과 미확정 자체는 이 정보 계약의 실패도 PASS도 아니다.

산출물은 docs/analysis/A043-outputs/s1/의 contract.md, closeout.md,
verification.json, s0-handoff.ko.md로 제한한다(읽기·hash·노출·비용 내역 포함).
status/log에는 결과만 추가한다. S0 원본 A043 기록을 소급 수정하지 않는다.
예비 작업은 불수용 조건·정확한 재개 입력의 closeout뿐이다.

E063 공개 동점 UNRESOLVED/E041 incumbent/E025 fallback 유지.
E057/E060/E061/E062/E063 parked, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD/A039/A040 및 모든 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·
selection2007/1130, 보호 audit2074/1177·calibration1866 보존.
A_half 비승격, A018 사용자 미확정, S3 중단, 새 S2 후보 없음.
```
