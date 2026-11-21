# S0 인계 — A040 전체 경로 입력 준비 실패

판정: **LOCAL_FULL_PATH_FAIL**. 첫 입력 생성에서 중단. 실제 모델 실행0회.
현재 HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`, 기존 dirty 보존.
상세 근거는 같은 폴더 `closeout.md`, `verification.json`, `resources.json`,
`source-manifest.json`, `generation-failure.txt`를 읽는다.

새 orchestration의 `layout()`이 UNICEF 공개 JSON에서 `gated_value`를 찾다가
KeyError를 냈다. UNICEF/WB raw schema에는 그 최상위 필드가 없고 UNHCR에만
NA_GATED가 있다. 작은 spy schema는 필드를 직접 넣어 PASS했으므로 이 차이를
검증하지 못했다. 원래 E041도 runtime schema에서 해당 필드를 요구한다.
입력 준비 결함이며 E041·TabICL full-context 실행 실패나 하드웨어 부족은 아니다.

모델 없는 검사2.09376초 PASS. 생성1회 실패, 도구 보고 wall0.7898181초.
고정 역할 배열만 생성됐고 가짜 응답 입력/출력은0개다. reference/candidate0회,
fit/predict/load/score0회. 코드+입력의 scientific freeze에 도달하지 않았다.
post-failure manifest를 사전 동결 manifest로 해석하지 않는다.
실제 전체 시간·RSS/commitment·CUDA peak·parity·강제 활성 경로는 미측정/미검증.
기존 원래 실패와 retry1 PASS 불변. 누적 과학 실행은 여전히2회/parent54.09619초.

이번 사용자의 첫 오류 중단 규칙에 따라 고치거나 다시 돌리지 않았다.
S0는 별도 S1 보완 가치만 판단한다. 재개 조건:

1. 공식 공개 소스로 raw schema→predict용 runtime schema의 정규화 계약 확인.
   generator와 runner가 같은 계약을 사용해야 한다. 임의 sentinel 추측 금지.
2. 세 실제 공개 schema 모두를 대상으로 모델 없는 진입 검증을 먼저 명시.
   이번 작은 spy PASS와 구분한다. 기존 모델·seed·head·context·정책은 보존.
3. 실패 폴더와 역할 배열 보존. 새 위치·사전 동결·1회씩 실행·중단/자원 한도를
   별도 범위로 정한 뒤 사용자가 해당 S1 실행을 지시할 때만 진행.

실제 모델 호출·추가 진단 실행·S2·유료/H100 작업으로 자동 전환하지 않는다.
전체 경로가 나중에 통과해도 실제 효과/H100/hosted900초/release PASS가 아니다.
source/assembly parity, ZIP checker, official all3, E025기관별absolute.002/E041
비교, SCORES 사전 판독표, native network 및 배포비용 검증은 모두 남았다.

E041 incumbent/E025 fallback, E057/E060/E061 parked, 모든 STOP/HOLD 유지.
17999명/12339SSUID·A022 원래 역할·E059 소비 oracle/selection과 보호audit2074/1177,
calibration1866 보존. A039 HOLD 별개, A_half 비승격, A018 미확정/S3 중단.
기존 주최측 정책 해소·설치 승인 승계. 이번 설치·취득·commit/push·제출0회.
S0 검토 전 S2 인계 없음.
