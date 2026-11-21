# A043 S0 — 계약 수용, 제한된 구현·합성 기술 검증 권고

2026-10-11 KST. **ACCEPT_CONTRACT / RECOMMEND_BOUNDED_S1_IMPLEMENTATION.**
현재 S0가 모델 구현·실행을 시작하거나 S2 후보를 승인한 것은 아니다.
별도 S1에 사용자가 [새 인계문](s1-implementation-handoff.ko.md)을 전달할 때만 그 범위를 실행한다.

## 판단

[S1 계약](../s1/contract.md)의 정보·설계 판정을 수용한다. 기존 독립 conditional
heads·초기화·forward·CE를 유지하면서 conditional CE의 trunk 직접 gradient만
차단한다는 개입이 구체화됐다. Factory만 추가하면 원래 `_train_on`에 연결되지 않는
문제, indirect stop/config/refit 영향, None/zero gradient와 Adam 상태, 실제 renderer
소비 경로까지 정해져 있다. 동일 계약을 다시 조사할 필요는 없다.

진행 가치는 효과가 입증돼서가 아니다. E061의 logits tying/독립 head 제거와 구별되며,
기존과 같은 정상 학습 호출 수로 잘못된 연결·head 무학습·NO_OP·자원 초과를 직접
기각할 수 있다. 그 기술 조건을 통과한 한 정책은 향후 별도 DEV 관측으로 우선순위를
바꿀 수 있다. 추가 환경·클라우드·새 보호 데이터가 필요하지 않은 설계다.

반대 근거는 유지한다. E012 공동 학습의 과거 이득, E061 hosted adverse, 실제 gradient
충돌·현재 E041 손실 지도·새 oracle 부재 때문에 향상 크기나 승률은 추정할 수 없다.
Conditional head를 계속 학습시켜도 해당 표현의 학습 신호를 줄이면 손해일 수 있다.
공개 tie는 미세 효과를 분리하지 못한다. 이번 한 번의 기술 비교를 양성 결과가 나올
때까지의 탐색이나 자동 제출 단계로 확대하지 않는다.

## S0의 영향 범위 정정

앞선 [A043 S0](../../A043-post-e063-priority.md)는 metric activity/replay 자격까지
변할 수 있다고 넓게 썼다. **현재 source에서는 그 부분을 정정한다.**
`supervised_retrieval.fit_sections`와 GIVEN 기반 donor/weight 계산은 neural 출력을
인자로 받지 않는다. 같은 입력·환경에서는 metric weights, section activity, donor
identity/order, replay eligibility, concentration 분류 및 ladder/agreement가 기대 불변이다.
이것은 새 실행 parity PASS가 아니라 정적 의존성 판단이며, 미래 R/H에서 검사한다.

Neural trajectory/config/epoch/w, full-proxy replay의 p_model, lambda와 최종 parent/child
출력은 변할 수 있다. Metric 활성과 lambda 활성은 구분한다. `if not lam: return {}, {}`
이후의 held-query evidence는 한 arm에서 아예 계산되지 않을 수 있다. 따라서 대응 경로가
실제로 평가됐을 때 donor/bucket identity를 비교하며, 정당한 생략을 metric 변동으로
오판하거나 검사용 추가 전체 예측을 실행하지 않는다. 원래 S0/S1 기록은 소급 수정하지 않는다.

## 다음 S1의 확정 범위

- 주력: 고정 H 하나 구현, 사전 등록·새 영향 검사, fresh R/H all3 각 1회,
  6개 raw 출력 동결 후 단일 합성 평가. R은 E041 source. 별도 E025 fit·assembly·ZIP 없음.
- 범위: UNHCR만 변경, UNICEF/WB original R delegation. 기존 config2/seed/선택/refit/
  renderer/lambda 정책 유지. 학습 결과로 나온 epoch/w/lambda를 같게 강제하지 않는다.
- 자원: gross120분(기록10분 포함), computational child 총1800초, 작은 영향검사 총300초
  포함·각60초, 각 all3 shared900초, CPU2/GPU0/heavy1/RSS·private 각각8GiB.
  정상6pipeline/18neural/16metric. 문서·단위검사 호출은 전체 학습과 따로 계수한다.
- 수리: 일반 구현 오류는 r5에 따라 같은 세션에서 수정. 무효가 된 full arm만 전체
  최대1회 재시작 예비를 허용하는 인계다. 전체3all3/9pipeline/27neural/24metric과
  시간 한도를 함께 지킨다. 성공 arm·실제 NO_OP·하한 실패·정책 선택 결과는 재시도하지 않는다.
- 기술 PASS: 초기/gradient/정보/controls/기대 불변 경계·확률·자원 통과,
  UNHCR raw 변화>=1, 기관별 H-R skill>=−.002. 개선·+.005는 필수 조건이 아니다.
  STOP_NO_OP/REGRESSION_HOLD/TECHNICAL_FAIL/RESOURCE_LIMIT/INCOMPLETE를 구분한다.
- 예비: 실패 원인·소비 예산·정확한 재개 입력을 기록하는 closeout만. 다른 기전으로 전환하지 않는다.

미래 scientific registration에 도달할 때 E064 번호를 재확인한다. 현재 filename 조사에서
E064/conditional_gradient 소스 충돌은 없었지만 이번 S0는 E064 문서·모델을 만들지 않았다.
S1은 실행 전에 새 코드/환경/입력/판정 freeze를 완성한다. 세 synthetic Parquet 해시는
E063 freeze 기록을 승계한 설계 입력이며 **이번 S0에서 재검증하지 않았다**.

수치 oracle이 없는 이유는 변하는 학습 trajectory의 target-domain headroom을 기존
예측 라이브러리나 허용 독립 labels로 산정할 수 없기 때문이다. 이미 노출된 synthetic은
공학 채널이며 실제 ERPIS 효과·독립 audit·A021 목적함수 비교가 아니다. 기존 base의 S/L
재사용과 in-sample full-proxy replay 한계를 보존한다.

S1 종료 후 S0가 실제 차이·손해·비용을 검토한다. S2에는 clean E025 기관별−.002와 E041
release 비교, source/assembly/extracted parity, ZIP checker, official all3/shared900초,
메모리·bytes provenance·사전 SCORES가 남는다. 정상 전체 계획15pipeline/45neural/32metric,
S2 추가 계산3600초는 미래 설계일 뿐 이번/다음 S1의 실행량이 아니다.

## 근거·보존

AGENTS/CLAUDE/status 최신부/log 최신3개/workflow r5/A043 인계·계약·closeout·verification
및 생산 소스의 관련 경로를 읽었다. S1 receipt는 세션 보고와 read evidence를 검토했으며
다른 채팅 준수의 포괄 인증이 아니다. 현재 source/문서 identity는 [entry](entry.json).
S1 contract/closeout/handoff 해시는 기록과 일치. Status/log의 S1 진입 대비 차이는
해당 S1 결과 추가이며 completion의 after 해시와 일치한다. 과거 해시로 되돌리지 않는다.

E041 incumbent/E025 fallback; E057/E060/E061/E062/E063 parked, E062/E063 UNRESOLVED.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040와 모든 STOP/HOLD,
17999명/12339SSUID·집계·A022 원래 역할·E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866 유지. A_half 비승격/A018 미확정/S3 중단/S2 후보 없음.
새 S0 문서와 status/log 추가만 작성. 모델/응답/cache/ZIP/검증 실행·플랫폼·원격·서브에이전트·
commit/push 없음. [문서 보존 검증](verification.json).
