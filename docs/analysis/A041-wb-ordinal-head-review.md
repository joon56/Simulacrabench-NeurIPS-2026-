# A041 — A040 이후 World Bank 순서형 head 연구 계약 검토

2026-10-07 KST. S0 전략·문서 검토. 상태: INFORMATION_TASK_PROPOSED.
주력: World Bank 16개 구간형 응답의 순서 정보를 학습 단계에서 쓰는 계약을
45분 S1 정보 조사로 구체화한다. 구현·fit·S2·기관 변경 실험은 아직 승인하지 않는다.
A040 추가 수리 보류와 모든 기존 STOP/HOLD는 그대로 유지한다.

## 선택 근거

사용자는 STOP 통보에서 흐름이 끝나지 않도록 다음 실행 가능한 작업을 요청했다.
S0가 다음 판단과 담당 범위를 제공할 책임이 있다. 준비된 모델이 없다는 사실은
새로운 기전의 적합성을 조사할 수 없다는 뜻이 아니다.

현재 공개 world_bank.json에서 PREDICT이며 gate=null인 16개 문항이 정확히
같은 여섯 구간과 Not answered를 가진다. Big Five, Growth Mindset,
Proactive Personality, Emotional Intelligence, RIASEC 하위척도가 포함된다.
목록과 schema SHA는 [inputs.json](A041-outputs/inputs.json)에 고정했다.
범주가 여섯 개로 정렬된다는 문서 사실이지, 실제 분포의 단봉성/빈도/희소성 근거가 아니다.
숫자 간격이 같다는 가정이나 원점수 복원도 하지 않는다.

E041의 neural full head는 일반 softmax이며 범주 순서를 명시적으로 제약하지 않는다.
shared trunk가 이미 문항 간 표현을 공유하고 비선형성을 학습한다는 점을 반대 근거로 둔다.
새 질문은 이 16개 응답의 ordered cumulative probabilities를 이용한 구조적 제약이
명목형 head보다 더 안정적인 확률을 만들 수 있는가다. 효과와 회복 가능한 손실량은 미측정이다.

E011은 E010 출력의 숫자 순위에 Gaussian kernel을 적용한 사후 평활화다.
숫자로 파싱되는 값이 K-1개 이상이어야 하며, 위 구간 라벨들은 이 규칙을 통과하지 않는다.
따라서 이 16개 구간형 head의 학습 시 순서 제약은 E011과 문항·개입 위치가 다르다.
그러나 E011의 두 가상 실험 null은 단순한 '순서 정보면 이득' 주장에 불리한 근거로 유지한다.
E030은 GIVEN 검색 서명의 인접 일치, E017/E026은 trunk 용량, E029는 seed/온도,
E061은 UNHCR full/conditional logits 공유다. 그 STOP/parked를 재개하지 않는다.
실험 문서/모델 소스/상위 A문서에서 확인한 범위상 같은 순서형 head 실험 기록은 찾지 못했다.
미기록 실험까지 전부 없었다고 보증하지 않는다.

CORAL은 순서 일관성을 가진 neural output의 선행 예이며, CORN은 공유 가중치 제약의
표현력 한계를 지적한다. 원 논문의 결과를 HSCC log score 개선 근거로 전용하지 않는다.
S0는 초록/개요를 읽었으며 full-paper loss/확률 복원 계약 확인은 S1의 남은 일이다.
출처: [CORAL](https://arxiv.org/abs/1901.07884v7),
[CORN](https://arxiv.org/abs/2111.08851v5).

## 비교와 비용

| 경로 | 근거 | 반대 근거/비용 | 선택 |
| --- | --- | --- | --- |
| WB 16개 구간형 head 계약 | 스키마에 명명된 순서 구조, E011 비대상, 현 head와 차이 명확 | 제약이 오히려 확률을 왜곡할 수 있음; 효과/전체 시간 미측정 | 주력 정보 조사45분, 원격·학습0 |
| 기존 nominal head에 floor-aware loss | 학습 CE와 최종 flat floor 차이 존재 | 차이 자체는 유의한 오류량 근거가 아님; 드문 응답 학습 약화 위험 | 이번에 선정하지 않음 |
| 추가 A040 수리/새 대형 모델/RL | 다른 가설 가능성 자체는 남음 | A040 한도 소진, 다른 방법의 목표 오류·새 판독 근거 부족 | 자동 재개/도입 없음 |
| VAF 답변 대기 또는 의미 가정으로 연구 실행 | 실제 설문 채널 확보 가능성 | 연결·결측 의미 미확정; 문의 부재를 임의 확정으로 대체할 수 없음 | A039 HOLD 유지 |

이 비교는 현재 확인한 선택지의 정보 가치 판단이며 전역 최적/우승 확률 순위가 아니다.
WB 공개 점수 .49가 낮다는 이유나 과거 E025 손실 지도를 선택 근거로 쓰지 않는다.
기존 Torch/NumPy 범위에서 계약을 설계할 수 있는지 검토하므로 새 checkpoint/Modal 환경을
선행 조건으로 삼지 않는다. 실제 구현의 비용은 아직 측정하지 않았다.

## S1이 바꿔야 할 결정

S1은 한 개의 후보 parameterization, 범주 확률과 Not answered 처리,
학습/선택/최종 출력 목적함수, 비교와 역할 경계, 전체 fit 횟수/비용 계획을 제출한다.
CORAL/CORN 이름만 붙이거나 'ordinal error가 감소하니 log score도 증가'라고 결론 내리지 않는다.
숫자 예시나 수학적 도출은 문서로 가능하며 코드/fixture/학습은 실행하지 않는다.

관측 채널은 기존 공개 스키마·생산 소스·과거 결과와 논문뿐이다.
기존 synthetic DEV는 이미 노출된 공학 자료이며 지금 다시 열거나 채점하지 않는다.
향후 사용하더라도 순서 구조가 없는 generator 결과는 target 효능 oracle이 아니다.
현재는 고정 후보의 예측도 독립 응답 평가도 없으므로 유효한 수치 oracle을 계산할 수 없다.
향후 visible TRAIN 내부 검증은 hosted 모델 내부 선택 수단이며 S0가 미리 읽을 자료가 아니다.

새 head를 shared trunk에 연결하면 같은 WB의 나머지 문항도 달라질 수 있다.
'16개 head 교체'와 '최종16개만 변화'를 구분하고 전체 WB76개 및 all3 비용을 계획한다.
UNICEF/UNHCR 원본 경로 유지와 raw parity가 향후 기관별 귀속 설계의 기본이다.
실제 WB 변경 실험은 이 정보 조사와 별도 사용자 지시/등록 범위다.

완료 판정은 DESIGN_READY_FOR_S0_REVIEW 또는 NOT_READY_WITH_SPECIFIC_REASON.
전자는 효과/실행/제출 PASS가 아니다. 후자는 원인과 재개를 바꿀 입력을 명시한다.
동일 문항 감사·같은 논문 요약을 반복하지 않는다. 정당한 예비 작업은
구체적 기각·누락 조건 closeout이며 다른 모델 탐색은 이번 S1 범위가 아니다.

## 연속성과 보존

이후 STOP 보고는 '종료되는 경로', '유지되는 자산', '다음 판단과 담당자'를 함께 적는다.
사용자에게 다음 아이디어를 매번 요구하지 않는다. 다음 실행을 근거 없이 만들어내지도 않는다.
이번에는 [완성 S1 정보 조사문](A041-outputs/s1-handoff.ko.md)을 마련했다.

S0 읽기: 현재 status/최신3log 갱신 확인, 연속된 같은 역할의 AGENTS/CLAUDE/workflow r5
읽기 증거 승계; A004/A008/A025/A039 의미 질문, E011/E012/E017/E026/E029/E030/E061,
E041 snapshot 관련 source와 ordinal_smooth/supervised_retrieval/hh_cap, 공개 WB schema.
현재 shared_trunk.py 전체는 해시 식별만 했으며 해당 학습 구조는 E041 snapshot에서 읽었다.
workflow SHA256 a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, dirty89, 이름 기준 python/pythonw/uv0.
A041 경로 충돌 없음을 확인했다. 실제 읽기/해시·보존은 inputs/verification에 구분한다.

모델/평가 코드·보호 응답/키/Parquet/NPZ/캐시/checkpoint 접근·hash·fit/predict/score·
fixture/설치/Modal/ZIP/tree/commit/push/S2/S3/서브에이전트0.
E041/E025, parked E057/E060/E061, E058 STOP/E059 STOP_SELECTION,
A039/A040 및 모든 STOP/HOLD,17999명/12339SSUID·A022 역할/집계,
소비 oracle1918/1124·selection2007/1130, 보호 audit2074/1177·calibration1866,
A_half 비승격/A018 미확정/S3 중단/S2 후보 없음을 보존한다.

