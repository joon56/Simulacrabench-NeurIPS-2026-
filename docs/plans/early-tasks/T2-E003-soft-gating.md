# T2 — E003 soft (agreement-weighted) gating — D2 오후, 3h

parent: E002 `src/models/gated_marginal.py`. 설계 근거: `docs/domain.md` §9.1.

## 왜

unhcr v1.3 실제 데이터: gate-vs-data 일치도 중앙값 0.83 (0.29–0.98). E002의
hard coupling은 일치하는 83%에서 이기고, 어긋나는 17%에서 셀당 log(1e-3)
= −6.9 nats를 낸다. 문항별 일치율 ã_i로 hard와 관측 sentinel rate를 섞으면
기대 log score가 오른다. 샌드박스는 gate를 정확히 강제하므로 로컬에선
ã≈1 → E002와 동일해야 한다 (**안 지는 것**이 로컬 통과 기준, 이기는 건
실데이터에서).

## 파일

- `src/models/soft_gated_marginal.py` (신규, E002 복사 후 수정)
- `tests/test_soft_gating.py` (신규)
- `docs/experiments/E003-soft-gating.md` (이미 생성, 결과·Decision 채울 것)

## 알고리즘

가시 행(= 완전한 TRAIN 행)에서 gated item i마다:

```
n_i = parent가 NaN 아닌 가시 행 수
k_i = 그중 (child == NA_GATED) == (parent ∉ observed_if) 인 행 수   # gate가 맞은 행
m   = 악기 전체 k_i/n_i 의 중앙값 (또는 평균)
ã_i = (k_i + α·m) / (n_i + α)        # beta-binomial 수축, α=20 정도에서 시작
```

예측 (respondent별):

```
hard_i  = E002와 동일: [p_asked · cond_i , 1 − p_asked]
soft_i  = 가시 행 전체의 full marginal (sentinel 포함, 스무딩)
pred_i  = ã_i · hard_i + (1 − ã_i) · soft_i
```

chain: 부모 belief는 pred(부모)를 그대로 쓴다 (E002처럼 앞에서 계산한 것).

선택(stretch, §9.3): `soft_i`를 `wave`(unhcr GIVEN)로 조건화 — 59개
multi-select sentinel이 round 2에만 있다는 점을 직접 반영. wave별 카운트가
작으면 marginal로 backoff (T3 보간식 재사용).

## 수용 기준

1. **동일성 테스트**: ã_i를 전부 1.0으로 강제하면 E002 벡터와 동일
   (`np.allclose`). 샌드박스 자연 추정값(ã≈1)으로도 runner mean Δ > −0.002.
2. **위반 시뮬레이션 테스트** (이게 핵심 증거): 샌드박스 unhcr frame을 복사해
   gated 자식 셀의 17%를 랜덤하게 "gate 위반"으로 뒤집는다 (asked였던 셀을
   NA_GATED로, NA_GATED였던 셀을 cond에서 샘플한 값으로). 가시 행도 같이
   뒤집어야 ã 추정이 그 위반을 본다. 그 frame에서 hard(E002) vs soft(E003)
   log score 비교 — soft가 **분명히** 좋아야 한다 (차이 수치를 E003 파일에
   기록). 이 측정이 없으면 E003은 adopt 근거가 없다.
   - 구현 힌트: runner를 쓰지 말고 `score.py`의 `sample_rows` → frame/truth를
     받아 직접 뒤집은 뒤 `floored` + `grade` 호출 (runner.run 코드 10줄 그대로).
3. E003 파일 Result 표: (a) 정상 샌드박스 4 스키마, (b) 17% 위반 unhcr
   hard vs soft. Decision: 로컬 샌드박스 기준 "안 짐" + 위반 시뮬레이션 이득
   → **adopted (real-data motivated)** 또는 parked. 솔직하게.

## 함정

- 부모가 PREDICT인 gate (unhcr 156개 중 155개)는 E002에서 crowd로 떨어져
  marginal과 같아진다 — E003도 마찬가지. unhcr에서 진짜 이득은 T3이 부모를
  respondent별로 예측할 때 열린다. 지금은 "안전장치 설치"가 목표.
- α 튜닝은 샌드박스로 못 한다 (위반이 없으니). α=20 고정, 근거 한 줄 적어둠.
- 다중 선택 family(sentinel이 round 2에만)는 ã가 낮게 나올 것 — 실데이터
  에서 그 item들의 ã 분포를 찍어보는 게 첫 제출 후 진단 항목.
