# A043 — E063 사후 우선순위와 조건부 gradient 경로 검토

2026-10-11 KST. S0 문서 판단. **E063 UNRESOLVED / DEPRIORITIZE_FIXED_POLICY.**
다음 주력은 **S1 정보·설계 검토 한 건 제안**이며, 구현·실험·S2 실행을 승인한 기록이 아니다.
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; dirty 소스는
[entry.json](A043-outputs/entry.json)의 현재 문서·소스 해시로 함께 식별한다.

## E063 판독 수용

[S2 사후 기록](E063-outputs/s2/post-result/result.ko.md)과
[비교](E063-outputs/s2/post-result/comparison.json)의 동점 arm 적용을 수용한다.
ID972597은 제공 자료상 Finished / Development / phase29772다.
Grand `0.6433333333`, UNICEF `0.5200000000`, WB `0.4900000000`,
UNHCR `0.9200000000`: 등록 비교기 E041 ID933094의 네 전체 문자열과 같다.
공개 값에서 읽을 수 있는 개선 없음. 정확한 효과 0, 동일 예측·활성, 전체 round
가설 반증은 아니다. best-update 이벤트는 없으며 membership 필드로 보충하지 않는다.

플랫폼 생성 시각은 2026-10-10 00:29:35.752090 KST. 업로드/완료 시각의 독립 관측이
아니다. E041 extract에 task/scorer 필드가 없어 scorer 버전 동일성은 미입증이다.
기록된 로컬 ZIP 15,720 bytes / SHA256 `5469b5374f6fb3745cabf64071183ed3de5bbe240ea4f18c034049d560d532d9`
승계만 한다. 이번 S0는 ZIP을 열거나 재해시하지 않았고 원격 bytes/path/hash는 미확정이다.

기술·release PASS, E025 identity의 늦은 확인 보완, synthetic gain +.000017579 및
16개 section×wave 중 8개 하락, proxy/selection·in-sample replay·독립 audit 부재를
보존한다. 새로운 효과 근거가 아니므로 **같은 E063 정책의 재제출·조정은 주력에서 제외**한다.
E041 DEV incumbent / E025 fallback / E063 parked. TEST 선택은 별개다.

## 비교한 경로

| 경로 | 근거와 반대 근거 | 다음 결정에 주는 정보·비용 | 판단 |
|---|---|---|---|
| E063 재제출 또는 round/seed/head/threshold 조정 | 실제 구현·release는 통과했으나 새 공개 개선 없음. 동점은 효과 0의 증명이 아님 | 동일 관측의 반복은 이번 기전을 분리하지 못함. 새 선택 편향과 제출 비용만 추가할 위험 | 진행하지 않음. 기존 정책 parked |
| A039 VAF / A040 TabICL·Modal 재개 | 잠재적 별도 채널·표현이 있으나 linkage/missingness와 native 종료 결함의 새 해결 근거 없음 | 같은 문의 대기·같은 준비 실패를 반복해도 다음 판단이 바뀌지 않음 | 해당 HOLD 유지. 새 공식 문서 또는 구체적 원인·수리 근거가 생길 때 별도 검토 |
| 용량·seed·tree/전문가 추가 | E012의 과거 모델군 교체 이득은 존재. E015/E017/E029, E039/E040/E046 등은 특정 설계·선택기의 한계를 보임 | 과거 부정 결과는 계열 전체 상한이 아니지만, 이번에 새로 특정된 상호작용·보완성·판독 근거 없음 | 포괄적 모델 탐색은 선정하지 않음 |
| **조건부 head의 trunk gradient 차단 계약** | 현재 별도 full/conditional heads가 동일 trunk를 학습시킴. 한 경로만 분리하면 forward 함수족·head 수를 유지한 개입 가능성이 있음. 반대로 공동 학습은 E012의 장점이며 conditional 표현을 약화할 수 있음 | 보호 응답·GPU 없이 소스·수식으로 변경 범위, E061과 차이, 최종 출력/선택 경로, 전체 호출 비용을 확정할 수 있음. 효과는 확정 불가. S1 최대 40분 제안 | **정보·설계 과제 한 건**. 반복 설명으로 끝나면 후보화하지 않음 |

순위는 검토한 대안과 현재 입력에 한정한다. 승률·예상 Grand·최선의 모델이라는 수치
주장은 없다. 빈 제출 slot이나 이미 쓴 준비 비용은 새 후보의 근거가 아니다.

## 새 질문: full/conditional 학습 연결을 분리할 가치가 있는가

**관측한 소스 사실:** [shared_trunk.py](../../src/models/shared_trunk.py)의 `_Net.forward`
는 같은 `z = trunk(x)`를 독립 full/conditional Linear heads에 전달한다. `_pooled_ce`는
full 셀 CE와 유효한 asked-only conditional 셀 CE를 더해 그 셀 수 합으로 나눈다.
`_train_on`은 이 손실로 trunk와 두 head 집합을 함께 갱신한다. Conditional heads는
최종 gate 경로에 쓰이는 실제 예측기다. 불필요한 보조 출력이나 확인된 버그가 아니다.

**검토할 한 개입:** 독립 conditional heads와 원래 초기화를 유지하고, 학습에서
conditional heads에 전달하는 representation만 stop-gradient 처리한다. Full 경로는
기존대로 유지한다. Conditional head 자신의 파라미터는 계속 학습한다. Conditional
loss 삭제, head tying, loss 가중치 탐색, 새 네트워크/optimizer/seed는 포함하지 않는다.

동일 상태에서 `L = (L_full + L_cond) / N`의 forward 값은 그대로일 수 있다.
원래 trunk gradient는 `(g_full + g_cond) / N`; 제안 경로는 `g_full / N`이다.
이는 자동미분 실행 결과가 아닌 소스와 chain rule에서의 설계 추론이다. Adam의
weight decay·상태, dropout/RNG 및 실제 연결이 이 명세와 맞는지는 후속 계약 대상이다.

**유리할 수 있는 이유는 아직 가설이다.** Full 손실과 asked-only 손실의 gradient가
충돌한다면 full 경로에 필요한 표현의 타협을 줄일 수 있다. 그러나 실제 충돌·손해는
측정되지 않았다. 같은 방향이면 유용한 supervision을 제거한다. Full 셀에는 sentinel이
포함되므로 sparse conditional 내용을 잘 배우던 경로가 약해질 수도 있다. 두 종류 CE가
있다는 사실만으로 중복 계산 오류나 목표 함수 불일치에 의한 손해를 단정하지 않는다.

**E061과의 차이:** [E061](../experiments/E061-tied-content-heads.md)은 conditional logits를
full ordinary logits에 묶고 독립 conditional 모듈을 없앴다. 원래 두 CE와 denominator는
유지했으며 모듈 제거가 RNG 소비에도 영향을 주었다. 이번 질문은 그 독립 모듈·forward
함수족을 유지하면서 직접 gradient 전달만 바꾼다. E061의 hosted 하락은 관련 반대 근거지만
이 경로를 이미 실행한 증거는 아니다. E062의 WB 순서 head와 E063의 retrieval metric도
같은 개입이 아니다. 허용된 실험/분석 문서와 소스 검색에서 동일 개입은 찾지 못했으며,
모든 미기록 과거 실행의 부재까지 증명하지는 않는다.

**남은 핵심:** 현재 early stopping과 outer config 선택은 conditional CE를 계속 사용한다.
따라서 직접 gradient를 차단해도 conditional target의 간접 영향은 남는다. Epoch/config/w,
최종 refit, metric activity·replay/lambda·모든 UNHCR 출력이 달라질 수 있다. 정책을 유지한
전체 절차 비교이며, conditional supervision의 순수 인과효과나 A021 D-P 비교가 아니다.
후속 S1은 생산 renderer까지 이 경로를 추적해야 한다. 위 사실 재확인만으로는 충분하지 않다.

## 관측 채널·비용·전환 조건

현재 허용된 것은 **문서와 생산 소스**다. 수치 oracle은 없다. 고정 예측기 혼합의 최적
계수가 아니라 학습 trajectory를 바꾸는 개입이므로 기존 E049 oracle이나 E025 손실 지도로
그 headroom을 산정할 수 없다. 현재 E041의 base/조건부 손실 분해도 확보하지 않았다.
Gradient cosine을 향후 구하더라도 그 자체가 최종 점수 개선의 oracle은 아니다.

노출된 synthetic은 미래에 별도 허용된 경우 연결·마스킹·parity·실행 비용을 확인하는
공학 채널이다. 실제 ERPIS 이득이나 독립 audit을 제공하지 않는다. 실제 visible TRAIN의
기존 내부 선택도 새 독립 평가가 아니다. 공개 DEV 관측은 노이즈·반올림이 있는 전체 정책
결과이며, 향후 같은 값이면 개선 부재를 읽는 데 한정된다. 숨은 gradient 효과는 복원 못 한다.

주력 S1은 최대 40분(gross, 마지막 10분 기록 포함), 모델/과학 계산 0, 원격/현금 0인
정보·계약 검토로 제안한다. 기존 E041 구조상 정상 all3 한 arm은 3 pipeline/9 neural/
8 metric이며 refit 포함이다. 이것은 현재 소스에서의 계획 근거일 뿐 새 후보 비용 실측이
아니다. S1은 비교기 실행·재사용 조건, E025 및 S2 검증까지 포함한 미래 전체 비용을
명시해야 한다. E063의 327.6초 또는 공식 701.7초를 새 후보 보장 시간으로 쓰지 않는다.

- **CONTRACT_READY_FOR_S0_REVIEW:** 직접·간접 학습 경로와 최종 소비 경로, E061과의
  실질적 차이, 원래 초기화/forward/조건부 학습을 보존할 경계, 호출·자원 상한,
  미래 영향 검사 및 comparable DEV 판독이 한 개입으로 구체화됨. 이는 S0가 별도
  제한된 구현·기술 검증을 판단할 입력이며 실행 허가·효과 PASS가 아님.
- **REJECT_DUPLICATE_OR_UNINFORMATIVE:** 이미 답한 개입, 새로운 결정을 못 바꾸는 재서술,
  또는 conditional predictor를 실질적으로 학습하지 못하게 만드는 설계이면 기각.
  새 coefficient/grid/다른 모델로 바꾸지 않는다.
- **HOLD_SPECIFIC_INPUT:** 허용 소스로 중요한 경로·권한·비용을 특정할 수 없으면 정확한
  누락 입력, 확보 주체, 재개 조건만 기록한다. 효과가 미확정이라는 일반론만 반복하지 않는다.

정당한 예비 작업은 불수용 조건과 재개 입력의 closeout뿐이다. 같은 계약 조사 반복·모델
코드·실험 번호·자동 S2 작업으로 이어지지 않는다. [S1 제안 인계](A043-outputs/s1-handoff.ko.md).

## 보존·접근

S0 실제 읽기 및 현재 해시는 [entry](A043-outputs/entry.json), 종료 문서 검증은
[verification](A043-outputs/verification.json). S2의 read receipt는 세션 보고와 chunk 참조를
검토한 것으로, 타 채팅의 실제 준수를 포괄 인증하지 않는다. 지정 post-result 문서 9개의
현재 해시가 그 manifest와 일치했다. SCORES의 과거 대비 차이는 사후 추가 기록이며 복원하지 않았다.

E041 incumbent/E025 fallback; E057/E060/E061/E062/E063 parked, E062/E063 UNRESOLVED.
E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/A039/A040 및 모든 STOP/HOLD 유지.
17999명/12339SSUID·집계·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130,
보호 audit2074/1177·calibration1866, A_half 비승격/A018 사용자 미확정/S3 중단 유지.
새 response 노출·모델/검증 실행·ZIP·플랫폼·설치·원격·서브에이전트·commit/push·TEST 선택 0.
새 A043 문서와 status/log 추가만 작성. 기존 원본·소스·snapshot·tree는 변경하지 않는다.
