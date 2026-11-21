# S0 인계 — A041 WB 순서형 head 정보 조사 완료

이 문서는 **S0 검토 인계**다. 구현·실험·S2 실행 지시가 아니다.

판정 **DESIGN_READY_FOR_S0_REVIEW**. CORAL/CORN 원전2개와 허용 생산 소스로 한 후보를 설계했다. CORN식 여섯 substantive 범주 조건부 확률에 Not answered logistic을 분리하고, 정확한 일곱 범주 NLL/기존 pooled denominator를 유지한다. 기전은 순서별 affine conditional-logit의 학습 편향이며 실제 이득은 미확정이다.

먼저 [closeout](closeout.md), [contract](contract.md), [cost-accounting](cost-accounting.md), [verification](verification.json)을 읽는다. entry/source-register/exposure-ledger에 현재 identity·읽기·노출 경계를 남겼다. HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`. 이전 dirty 변경 보존, commit/push 없음.

S0가 판단할 내용:

1. WB16 head의 순서 조건부 함수족을 bounded exploratory 후보 하나로 진행할 가치. E011 null/과거 STOP, nominal softmax도 정상 분포라는 반대 근거 포함.
2. 비응답 분리·초기확률 비대칭·나머지 WB60개 변화까지 전체 절차의 개입으로 수용할지. 순서 효과만 분리된 비교라는 주장은 하지 않는다.
3. 기존 config2/inner-stop/outer config+w/final refit/λ 재사용을 유지하는 귀속과 channel 한계. fresh oracle 없고 synthetic은 engineering; 선택/replay 통계는 독립 검증 아님.
4. 후속 CPU2/worker1/로컬8GiB/candidate all3≤900s, 비교+검증 worker≤1800s/전체120분 제안의 적정성. 정상 pipeline9/neural27; 실제 비용 미측정. 새 환경/클라우드 계획 없음.

긍정 시 다음 일은 **사용자의 prospective WB 기관 변경 지시와 별도 S1 등록 후 구현/기술 검증**이다. S0 검토만으로 현 S1 범위를 확대하지 않는다. 모델 코드/E번호/실험 명령/ZIP은 아직 없다. 정보 계약 자체의 반복 조사 대신 위 구체 설계를 검토한다. 기각 시 불수용 계약/비용/채널 조건을 특정한다.

미완료: 수치/마스킹/초기화 검증, fixed UNICEF·UNHCR exact raw parity, 전체 WB76/all3 시간·메모리, clean E025 absolute.002/기관 및 E041 비교. S2 source/assembly parity·ZIP checker·official all3·SCORES 판독도 모두 미실행. synthetic 양성만으로 채택하지 않는다. 공개 hosted 점수와 원점수/실제 효과를 구분한다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, E058 STOP/E059 STOP_SELECTION, A039/A040와 모든 STOP/HOLD 유지.17999/12339·A022 역할/집계·E059 소비 oracle1918/1124/selection2007/1130·보호 audit2074/1177/calibration1866 유지. A_half 비승격, A018 미확정, S3 중단, S2 없음. 다른 세션/서브에이전트/원격/commit/push 자동 시작 없음.
