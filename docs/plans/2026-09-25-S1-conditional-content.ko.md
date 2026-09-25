# S1 · HSCC · E056 말단 문항의 조건부 답변 보강

아래 전체를 새 세션에 붙여 넣는다. S0에서는 실행하지 않는다.

```text
SimulacraBench / HSCC S1 연구 세션이다.
작업 폴더: C:\Users\USER\Desktop\SimulacraBench
목표: 최종 TEST 후보를 늘릴 가치가 있는지, 기존 gate 확률을 보존하는
말단 문항의 조건부 답변 예측으로 한 번만 검증한다. 개선을 가정하지 마.

1. 시작·기준
CLAUDE.md → docs/status.md → docs/log.md 최신 3개 순서로 읽고,
docs/workflow.md와 docs/analysis/A016-next-research-decision.md를 적용해줘.
기술 기준 커밋은 7f712e136896b8b89a83d724a5d355d3c5c764fe.
S0 후속 문서 커밋은 허용하되 HEAD와 차이를 기록하고 reset하지 마.
branch·dirty files·active jobs 확인. 사용자 변경 .gitignore,
.claude/skills/paper-session/SKILL.md, .claude/settings.local.json, trip/ 보존.
이 세션이 단일 통합 담당. 동시에 무거운 fit 하나만 실행해줘.

기준 E041: submissions/2026-09-19-E041/main.py
SHA256 22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
기준 ZIP: submissions/2026-09-19-E041.zip
SHA256 1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50.
읽을 파일:
- docs/analysis/A006-dev-validation-audit.md, A009-post-E049-strategy-review.md,
  A014-observed-gated-channel.md
- docs/experiments/E046-honest-tree-selector.md,
  docs/experiments/E051-direct-content-tree.md
- docs/experiments/E055-coupled-star-replay.md
- scripts/screen_e055.py, scripts/audit_a014_sipp.py
- src/eval/recursive_candidates.py, src/eval/logloss.py
- src/models/link_sharp.py, supervised_retrieval.py, shared_trunk.py
- docs/domain.md §9

2. 사전 등록·허용 범위
E056 예약 충돌부터 확인. docs/experiments/E056-conditional-leaf-content.md에
아래 가족·역할·상한·판정을 점수 접근 전에 등록하고 커밋해줘.
E046/E051/E053/E055 STOP과 옛 파일은 유지해줘.
E041에는 이미 conditional head가 있다. 새로 검증할 것은 asked-only tree의
보완성과 최종 leaf-content 개입이지, 조건부 분해 자체가 아니다.
E051의 full-answer tree와 E055의 donor-share 재보정을 재실행하지 마.

새 진단 코드 scripts/screen_e056.py와 tests/test_e056_conditional_content.py,
기록 docs/analysis/E056-outputs/만 만들 수 있다. 필요하면 새 보조 모듈만 추가.
기존 src 모델·제출 snapshot·환경을 수정하지 말고 새 production 모델,
main.py 조립, ZIP, 업로드, 유료 자원, 새 데이터 다운로드는 하지 마.
코드·주석은 영어. karpathy-guidelines 적용해 최소 변경과 성공 조건 검증.

3. 데이터·노출 경계
E055의 기존 고정 12000-person 표본과 A014 SSUID-group 역할만 사용.
scripts/screen_e055.py의 prepare('group') 정의와 표본/역할 해시를 검증해줘.
같은 source에서 oracle 결과가 이미 노출됨을 기록. 새 독립 표본이라 부르지 마.
fit만 E041·donor·tree 학습에 사용. 나머지 응답자의 전체 PREDICT block은
모든 fit 전에 마스킹. GIVEN은 기존 여섯 demographic 필드만.
ID·flag·실제 parent·다른 target은 입력 금지. 실제 non-sentinel 여부는
fit 안에서 asked-only 학습행을 고를 때만 사용. 추론 대상 선택에는 쓰지 마.
calibration role은 끝까지 마스킹·점수 미열람. person-view도 사용하지 마.
oracle은 최초 feasibility만, selection은 가중치 선택만,
audit은 완전히 고정된 최종 절차 평가에 한 번만 접근해줘.
fit/selection/audit 사이 SSUID 겹침이 없어야 한다.
원본 microdata·개인키·행 단위 배열은 Git에 넣지 말고 ignored external/e056/
아래 보관. 공유 산출물에는 해시·집계·재현 명령만 기록해줘.

4. 고정된 최소 가족
실제 generic E041 stack을 쓰되 작은 schema의 public-wrapper fallback은 금지.
link_sharp + supervised_layer + hh_cap.CONFIGS 사용.
기존 cache는 source/data/roles/마스킹 해시와 필요한 예측 coverage가 맞을 때만
재사용. 불충분하면 같은 group fit 역할로 E041 fit 최대 한 번 허용.
E055 선택 oracle 출력이 아니라 변경 없는 E041 endpoint가 comparator다.

대상은 SIPP 여섯 EHREAS_* 말단 child. 부모 HOSPITALIZED는 변경하지 마.
각 child의 fit 중 실제 non-sentinel 행만으로 GIVEN-only
HistGradientBoostingClassifier를 하나씩 학습해줘.
E051의 고정 TREE_PARAMETERS를 복사해 사용. 별도 grid·seed 탐색 금지.
asked fit 행 100 미만 또는 관측 클래스가 둘 미만이면 그 child는 exact E041.
complete schema 순서로 확률 정렬. q = .99*tree + .01*Laplace marginal,
marginal은 asked fit count에 클래스별 1을 더해 정규화. 추가 calibration 금지.

E041 raw vector p, sentinel 인덱스 g, non-sentinel mass M에 대해:
p'[g] = p[g]
p'[answers] = (1-alpha)*p[answers] + alpha*M*q
alpha는 child별 상수 {0,.25,.5}. alpha=0은 원본 vector 그대로 반환.
부모와 비대상 출력은 그대로 유지. 조건부 M=0도 원본 그대로 반환.
원본 total mass와 raw sentinel 보존을 검증. 공식 floor 후 sentinel은
간접적으로 달라질 수 있으므로 그 차이는 측정·공개하고 동일하다고 쓰지 마.
이 개입은 말단만 대상으로 하며 부모/descendant 재렌더링을 바꾸지 않는다.

5. 실행 순서·판정
모든 역할의 후보 예측과 코드/분할 provenance를 label 점수 접근 전에 저장.
공식 normalization/floor .001을 적용한 일곱 문항 pooled skill이 주 지표.
asked-only conditional loss는 보조 지표. skill/3도 보고하되 Grand 예측 금지.

먼저 oracle에서 child별 고정 share의 정확한 최대값을 구해줘.
이것은 해당 finite library만의 상한. delta skill <=1e-10이면 STOP.
>1e-10은 수치적 가능성만 통과이며 유의성/채택 기준이 아니다.
새 conditional predictor 가족에서 값싼 선택 단계로 갈 조건일 뿐,
E055의 +.005 실패를 통과로 바꾸는 기준이 아님을 명시해줘.

통과하면 selection에서 child별 최고 log-score share 선택.
차이가 같은 경우 작은 alpha 우선. 양의 paired mean gain이 SSUID-cluster
standard error를 초과할 때만 nonzero 선택, 아니면 alpha=0.
cluster uncertainty 계산식은 실행 전에 등록하고 검증해줘.
선택된 share를 동결한 뒤 audit 한 번. 일곱 문항 pooled paired delta skill,
2000회 SSUID-cluster bootstrap 95% percentile interval, random seed 5601,
changed-vector 비율, asked fit 수, raw/post-floor sentinel 차이,
총 시간·메모리를 보고해줘. 이 interval은 학습 변동·domain shift를 포함하지 않는다.

audit delta>0이고 95% 하한>0이면 후속 UNHCR 구현 검토 가치 있음으로 판정.
그 외는 비양성/불확실로 종료. 표본·모수·selector를 다시 고르지 마.
모든 alpha=0이면 audit를 열지 않고 무개입 STOP. 실패 범위는 이 가족/표본뿐.
기술 자격·DEV 탐색·TEST 채택은 별도다. 양성도 즉시 제출/채택하지 마.
기술 검증은 누수 방지, schema 순서, alpha=0 parity, raw sentinel/mass 보존,
부모 불변, 공식 floor, oracle 최대값, 선택/audit 분리에 집중해줘.

6. 자원·종료
주력 연구 wall 상한 90분, 누적 fit wall 상한 20분, CPU 2 threads,
GPU/유료 자원 없음, 작업 프로세스 합산 메모리 상한 8 GiB.
E041 최대 1 fit + child tree 최대 6 fit. 재사용 가능 cache면 중복 fit 금지.
측정 수단·중단 방법을 fit 전에 정하고, 상한 접근 시 부분 산출물 보존 후 종료.
상한은 성능 예상치가 아니다. 검증·기록은 마무리하되 새 연구는 시작하지 마.

주력이 무효/STOP/불확실/상한 초과이면 예비 최대 30분:
docs/phase2-preparation.md, submissions/phase2-E041-preparation/SCORES.md,
submissions/phase2-E025-preparation/SCORES.md,
docs/analysis/A012-phase2-baseline-and-calibration-gate.md,
docs/analysis/A013-probe-resolution-and-method.md만 검토.
docs/analysis/E056-outputs/test-readiness-gap.md에 E041/E025 비교,
사전 TEST 선택 기준, 기존 검증의 유효 범위, 실제 미해결 항목과 다음 S3 행동 작성.
기존 phase2 검증 재학습·PDF/ZIP 재생성·최종 선택은 하지 마.
일정 충돌은 기록하고 추후 공식 재확인 항목으로 남겨줘.

7. 산출물·인계
E056 사전 등록/판정, 재현 코드·집중 테스트, 동결 manifest/집계 결과,
노출 역할 장부, 측정 비용, 조건부 예비 보고서, 다음 완성 세션 프롬프트.
양성이면 다음 세션은 UNHCR 적용·runtime·no-regression 연구 인계다.
production candidate와 release 검증이 아직 없으므로 S2-ready라고 하지 마.
향후 S2에는 E025 absolute .002 per-instrument no-regression, E041 비교,
source/assembly parity, ZIP checker, official all3, shared 900s 검증이 필요하다.
E041 DEV incumbent/E025 fallback 유지, E054 parked 유지, 업로드 금지.
E파일 추가/상태 변경 시 scripts/render_tree.py 실행.
status/log는 간결히 갱신. 작업 파일만 commit·push하고 remote HEAD 확인.
최종 보고에 HEAD, 파일/해시, 판정 범위, 열린 점수 역할, 남은 작업,
실행 중인 프로세스/로그 또는 시작한 작업이 종료됐음을 명시해줘.
```
