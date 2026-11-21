# T1 — Temperature scaling (가이드 §3.2 산출물) — D1 오후, 2~3h

## 목표

모든 학습 모델 출구에 붙일 부품: held-out log-loss를 최소화하는 스칼라 T를
피팅하고, 확률 벡터에 적용한다. Guo 2017 §4.2의 temperature scaling을
**로짓이 아니라 확률 벡터**에 적용하는 형태 (우리 모델은 로짓을 안 내므로
`p ∝ p^(1/T)`; log p에 1/T를 곱하는 것과 동일).

## 파일

- `src/eval/calibrate.py` (신규, ~40줄)
- `tests/test_calibrate.py` (신규)
- `src/eval/runner.py` — `run()`에 `return_raw=False` 인자 추가: True면
  `{schema: (vectors, truth, cells)}`도 함께 반환 (피팅용 held-out 확보).
  기존 호출·출력은 바뀌면 안 됨.

## API (제안 — 바꿔도 됨, 단순하게)

```python
def apply_temperature(vectors, T):
    """vectors: list of 1-D arrays (각 셀의 확률벡터, 길이 제각각). p^(1/T) 후 정규화."""

def nll(vectors, truth_idx):
    """mean -log p[truth] over cells. truth_idx: 셀별 정답 인덱스."""

def fit_temperature(vectors, truth_idx, grid=np.geomspace(0.25, 4, 41)):
    """grid에서 nll 최소 T 반환 (1-D이므로 grid+주변 미세탐색이면 충분, scipy 불필요)."""
```

주의: 그레이더는 1e-3 플로어 믹싱 후 채점. `nll`은 `src/eval/logloss.py`의
`floor_mix`를 통과시킨 뒤 계산해야 리더보드와 같은 양을 최적화한다.

## 수용 기준

1. `tests/test_calibrate.py`:
   - 정답 one-hot에 가까운 **과신** 벡터를 랜덤 오류 섞어 만들면 fitted T > 1,
     fitted 후 nll이 전보다 작다.
   - 균등에 가까운 **저신** 벡터(정답에 약간만 몰아줌)는 T < 1.
   - `apply_temperature(v, 1.0)`은 원본과 동일 (정규화 오차 내).
   - 전체 `pytest -q` 통과 (기존 11 + 신규).
2. 측정 기록 (E파일 아님, log.md 한 줄): E002 벡터를 unicef 샌드박스 DEV 셀
   절반에서 T 피팅 → 나머지 절반 nll 전/후. 카운트 기반 marginal은 이미
   캘리브돼 있으니 **T≈1, Δ≈0이 기대값**. 그게 나오면 도구가 맞는 것.
   (DEV 셀로 피팅하는 건 샌드박스 도구 검증용. 실제 제출용 T는 TRAIN 내부
   held-out으로 — T3에서 그 분할을 만든다.)

## 힌트

- 셀 벡터 길이가 item마다 다르므로 2-D 배열로 쌓지 말고 `np.concatenate`로
  정답 확률만 뽑아 `-log`.
- T 곡선은 1-D 볼록에 가까움: `np.geomspace` 41점 → 최소 주변 ±1 칸을
  11점으로 한 번 더. 충분.
- Guo §4.2 핵심 문장 하나를 docstring에 인용해 둘 것 (왜 랭킹/정확도는 안
  변하고 NLL만 변하는가).

## 읽기-구현 연결 (자가확인)

- 온도 T>1이 확률 벡터를 어떻게 바꾸는가 → 우리 메트릭에서 왜 이득인가?
- 왜 하나의 스칼라로 충분한가, 언제 부족한가(§3.3 Dirichlet, NA_GATED 같은
  희귀 레벨)?
