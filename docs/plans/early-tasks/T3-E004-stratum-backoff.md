# T3 — E004 GIVEN-stratum backoff + 보간 가중치 튜닝 — D3 오후, 3~4h

parent: E002 (gate 결합 유지) — E003과 형제. 설계 근거: Chen & Goodman §2–3
(Jelinek–Mercer / Witten–Bell 보간), `docs/domain.md` §7.1 예고.

## 왜

held-out 응답자는 GIVEN 블록을 보여준다. 현재 E002는 그걸 gate 부모로만
쓰고 답 분포는 crowd 하나다. item별 분포를 GIVEN stratum으로 조건화하면
(1) 직접 이득, (2) **부모 예측이 respondent별이 되어 unhcr 155개 PREDICT
부모 gate가 열림** (E002 structural conclusion). 샌드박스는 trait_scale 2.0
이라 respondent 의존성이 있으니 로컬에서도 측정 가능 — 단 GIVEN 항목이
trait과 얼마나 엮였는지는 실행해 봐야 안다.

## stratum 후보 (스키마 GIVEN 실측)

| 스키마 | 1차 stratum | 2차(선택) |
|---|---|---|
| unicef | `Country` (10) | `Q05` (10) |
| world_bank | `user.country` (5) | `user.educationLevel` (11), `user.gender` |
| unhcr | `s1_2_country_asylum_lbl` (4) × `wave` (2) = 8 | `s2_1c_education_level_lbl` |
| sample | GIVEN 첫 항목 | — |

스키마에 하드코딩 금지 — `schema["items"]`에서 `class == "GIVEN"`인 항목을
읽어 **카디널리티가 가장 작은 1~2개**를 자동 선택하는 규칙으로 (실데이터에
같은 규칙이 적용돼야 함). 규칙은 docstring에 적는다.

## 알고리즘

item i, stratum 값 s:

```
p_strat(v | s) = (count_{i,s}(v) + 0.5) / (n_{i,s} + 0.5·K)
λ_s = n_{i,s} / (n_{i,s} + κ)                 # Witten–Bell/JM 류, 카운트 의존 가중치
p_i(v | s) = λ_s · p_strat(v | s) + (1 − λ_s) · p_marginal(v)
```

gated item은 asked-only 조건부에도 같은 식을 적용 → E002의 `conditional[item]`
자리에 `p_i(·|s)`를 꽂는다. 부모 belief가 respondent별이 되므로 gate 사다리가
그대로 전파된다.

κ 튜닝: **가시 행(TRAIN) 내부 held-out**으로. TRAIN의 20%를 떼어 PREDICT 셀을
가리고(역할 구조 그대로 흉내), κ ∈ {1, 3, 10, 30, 100}에서 log score 최대를
고른다. 이 분할 코드는 `src/eval/split.py` 같은 작은 모듈로 빼두면 T1의
"실제 제출용 T 피팅"과 T4에서 재사용.

## 파일

- `src/models/stratum_backoff.py` (신규) — `predict(frame, schema)`
- `src/eval/split.py` (신규, ~20줄) — `holdout_visible(frame, schema, frac, seed)`
  → (fit_frame, holdout_frame_with_blanks, truth)
- `tests/test_stratum_backoff.py`
- `docs/experiments/E004-stratum-backoff.md` (생성됨, 채울 것)

## 수용 기준

1. 테스트: (a) κ→∞ 이면 E002와 동일 벡터, (b) 모든 출력 벡터 합 1·유한·비음,
   (c) `split.holdout_visible`이 GIVEN을 남기고 PREDICT만 가린다.
2. runner 4 스키마 결과 + κ 선택 근거 표(κ별 held-out log score)를 E004에.
   Δ mean(sample 제외) > +0.005면 adopted. unhcr에서 처음으로 Δ>0이
   나오는지가 구조적 관전 포인트 — 표 밑에 한 줄로 해석.
3. wall-clock: 4 스키마 합 < 60 s (runner가 찍어줌). 파이썬 루프 per-row면
   unhcr 1,449 × 285에서 느려질 수 있음 — stratum별 벡터를 dict로 미리 만들고
   row 루프 안에선 조회만.

## 함정

- stratum 셀이 비면 λ=0 → marginal. 이게 MRP의 "empty cell" 문제의 1단계
  해법이고 D4 T4가 이걸 계층으로 확장한다.
- 두 stratum을 곱(country×wave)으로 쓸 때 셀 수 = 8, 단일 항목보다 희소.
  κ가 그걸 흡수하는지 κ 표로 확인.
- 과신 체크: 작은 stratum에서 0.5 스무딩 + λ 덕에 안전하지만, 결과를 T1으로
  한 번 통과시켜 T≈1 확인해두면 방어 논리가 완성된다.
