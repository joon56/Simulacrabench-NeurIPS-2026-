# A041 S0 — WB 순서형 head 설계 검토

2026-10-07 KST. **RECOMMEND_BOUNDED_S1_IMPLEMENTATION**.
이번 S0는 문서·허용 소스 검토와 인계만 수행한다. 현재 모델 실행 권한/S2 후보는 없다.

## 판단

다음 주력은 **WB16 CORN식 조건부 head 한 후보의 구현·합성 기술 비교**다. 정보 조사를 반복하지 않는다. A040 인프라 수리는 현재 우선순위에서 제외한 상태를 유지한다. 새 환경·H100·UNHCR 문의 회신 없이 기존 로컬 환경으로 검증할 수 있도록 범위를 정한다. 실제 환경 정상 동작과 비용은 아직 미측정이다.

S1의 DESIGN_READY_FOR_S0_REVIEW를 지지한다. 기존 softmax가 정상 분포라는 점, E011의 null과 기존 STOP, 별도 fresh WB oracle 부재를 포함해도 제한된 구현의 정보 가치가 있다. 이유는 점수 상승 확신이 아니라 공개 문항 의미에 연결된 하나의 구체적 함수족, 고정 비교기, 출력·비용·회귀 판독을 이미 명시할 수 있기 때문이다. 예상 Grand나 우승 확률은 산정하지 않는다.

| 근거 | 반대 근거/한계 | S0 판단 |
| --- | --- | --- |
| 여섯 substantive 범주의 순서가 공개 schema에 명시됨 | 순서가 단봉성·등간격·오류 크기·headroom을 뜻하지 않음 | 순서 조건부 parameterization만 시험; Gaussian smoothing/MAE 목적함수 아님 |
| E011 범주 탐지는 현재 range 문자열을 제외; 개입도 post-hoc kernel과 다름 | E011 null은 단순 순서 도입에 대한 반대 근거이며 유지 | 이전 실패의 재명명이 아닌 한 후보로 취급 |
| 조건부 확률의 곱으로 일곱 범주 분포와 정확한 NLL 구성 가능 | E041 nominal softmax도 유효한 누적분포; 정합성 자체가 개선 근거 아님 | 유한 affine conditional-logit의 학습 편향이 명명된 기전 |
| 새 checkpoint/환경/선택기·fit 단계 추가가 설계상 없음 | epoch/config/w가 바뀌며 실제 시간·메모리 미측정 | CPU2/로컬 비용을 직접 측정; 900초 보장 아님 |
| 고정 UNICEF/UNHCR raw control, 전체 WB 결과로 판독 가능 | synthetic은 기존 노출 engineering 자료; 실제 WB 효과 미확정 | 기술 후보 여부만 판단; S2/hosted는 이후 별도 판단 |

## 수용하는 개입과 귀속

[계약](s1/contract.md)을 그대로 수용한다. 여섯 범주 conditional-logit 다섯 개와 별도 Not answered logistic, 기존 일곱 범주 NLL 및 pooled denominator를 유지한다. 원전 CORN의 risk-set denominator를 이식하지 않는다. 조건부 확률/곱의 근거는 [CORN 원전 §3](https://arxiv.org/html/2111.08851v5); HSCC의 비응답 분리·pooled loss·초기화는 이번 설계이며 논문의 HSCC 성능 보증이 아니다.

수용한 효과 대상은 **WB 전체 절차**다. 비응답 분리, 원래 head 행을 재사용하는 비대칭 초기화, 함수족, 공유 trunk를 통한 나머지60개 문항 변화, config/w/λ의 선택 결과까지 함께 달라질 수 있다. 순서만의 독립 효과라고 부르지 않는다. 초기화 보정·순서 반전·별도 nominal 비응답 arm을 추가하지 않는다. 이는 비용을 제한한 탐색이며 원인 분해는 미해결로 남는다.

초기화에서 먼저 원래 nominal net 전체를 만들고 대상 head의 행0..4와 행6을 복사한다. 추가 난수 소비를 허용하지 않는다. 비대상 초기 parameter/RNG 보존을 검사하되, 학습 후 WB60 raw parity는 요구하지 않는다. UNICEF/UNHCR 최종 raw parity는 요구한다.

기존 config2·inner-stop·outer config+w·final refit·λ 규칙을 유지한다. 선택값을 E041 값으로 고정하지 않는다. 최종 refit은 w=0이어도 기존대로 수행한다. 내부 선택·in-sample λ replay는 독립 검증이 아니다. 범주별/문항별 diagnostics로 head를 선별하거나 정책을 구제하지 않는다.

## 관측 채널과 판독

허용 예정 채널은 E061에서 이미 사용한 starter-kit synthetic TRAIN/DEV 세 파일과 이번에 만드는 작은 수식/경계 입력뿐이다. 현재 S0에서는 그 Parquet를 읽거나 재해시하지 않았다. 파일 identity는 기존 E061 frozen-inputs에서 승계하고, 다음 S1의 명시적 허용 범위에서 검증한다. synthetic TEST·실제 protected data·VAF·이전 prediction/model cache는 제외한다.

공개 schema와 원전으로 목표 WB의 수치 oracle을 만들 수 없다. 고정 후보 예측도 구현 전에는 없으며, 생성 가정을 주입한 oracle은 실제 손실 상한이 아니다. 따라서 가짜 oracle 통과를 추가 선행 조건으로 만들지 않는다. 목표 이득·분산·최종 TEST 전이는 미확정이다.

다음 S1에서 source/정책/입력/분할·판독을 점수 전 동결한다. candidate/E041/E025 all3 각1회, 아홉 출력 동결 뒤 평가한다. 공식 floor와 score 함수를 사용한 in-process engineering 비교를 허용하는 별도 프롬프트를 준비한다. ZIP checker/official CLI release는 이 단계에 포함하지 않는다.

- 필수 기술 조건: 수치·마스킹·초기화·전체 출력·자원 준수, UNICEF/UNHCR exact raw parity.
- 회귀 조건: 각 기관 skill(candidate)-skill(E025) ≥ -.002 및 skill(candidate)-skill(E041) ≥ -.002. 절대 skill 단위, 상대0.2%가 아니며 이득 상한도 아니다.
- 후보 WB 최종 출력이 E041과 모두 동일하면 NO_OP/판독 가치 미확인으로 반환. 활성화 강제·threshold 변경 없음.
- 조건 충족과 실제 WB 출력 변화가 있으면 EXPLORATORY_SOURCE_QUALIFIED로 S0 재검토. synthetic 상승이 필수는 아니며 실제 개선/채택 증거도 아니다. 작은 합성 손실도 수치 그대로 기록한다.
- 기술/자원 실패 또는 회귀 기준 미달은 해당 범위의 실패/보류. 기존 STOP을 해제하지 않는다.

## 비용과 다음 행동

[S1 비용안](s1/cost-accounting.md)의 CPU2/GPU0/heavy worker1, 로컬 owned-tree RSS 및 private commitment 각각8GiB, candidate all3≤900초, 전체 computational child wall≤1800초, 전체 세션120분/마지막10분 기록을 수용한다. 정상 세 절차 비교 pipeline9/neural27이며 실패도 한도에 포함한다. 기존 E061 비용은 참고 이력일 뿐 A041 예측치가 아니다.

사용자가 [새 S1 실행 프롬프트](s1-implementation-handoff.ko.md)를 별도 S1에 전달하면, 그 문구가 prospective WB 기관 변경과 한정된 구현/합성 기술 비교 지시가 된다. 이 S0의 권고나 파일 작성 자체는 실행 허가가 아니다. E062는 현재 미등록이며 receiving S1이 번호 충돌을 다시 확인한 후 등록한다.

예비 작업은 같은 범위의 구현 오류 수리와 실패 closeout뿐이다. r5에 따라 일반 오류마다 S0 인계를 만들지 않고 남은 총예산·시도 수 안에서 수리한다. 새로운 모델·환경·클라우드·추가 seed/표본/정책은 예비안으로 시작하지 않는다. 불완전 종료 시 빠진 검증과 구체적인 재개 입력을 남긴다.

## 읽기·보존 기록

역할 S0, 유형 결과 검토/전략/인계. AGENTS → CLAUDE → status → log 최신3개 → workflow r5 → A041 S1 closeout/contract/cost/verification/source-register/entry/exposure를 실제 읽었다. workflow SHA256 `a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23`. 추가로 E041 생산 source, E061 기록/합성 검증 harness source, session-prompts 및 CORN 원전을 읽었다. hash만으로 읽기 완료를 주장하지 않는다.

HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`, branch work/e050-submission. 20:48:43 KST 관측 dirty91, named local Python/pythonw/uv jobs0. 모든 채팅/원격 작업 부재를 뜻하지 않는다. S1 artifact10개 및 preservation 목록26개가 현재 해시와 모두 일치했다. 현재 파일을 과거 manifest에 맞춰 되돌리지 않았다. 상세한 쓰기 전후 보존은 s0-review-verification.json 참조.

E041 incumbent/E025 fallback; E057/E060/E061 parked. E058 STOP/E059 STOP_SELECTION 및 A039/A040·모든 기존 STOP/HOLD 유지. 누적17999명/12339SSUID·집계 노출·A022 원래 역할, E059 소비 oracle1918/1124·selection2007/1130 및 보호 audit2074/1177·calibration1866 유지. A_half 비승격, A018 사용자 미확정, S3 중단, S2 후보 없음. 이번 S0 model/fit/predict/score/test/보호자료/원격/ZIP/commit/push/서브에이전트0. 기존 연구·snapshot·tree 불변.
