# T4 — D4 오후: (A) 계층 backoff 사다리(MRP-lite) 또는 (B) 첫 제출 준비

D3 결과에 따라 고른다. E004가 adopted면 A, E004가 애매하거나 시간이 적으면 B.
둘 다 하면 가장 좋다 (B는 90분짜리).

---

## A. 계층 backoff 사다리 (E004 확장, 가이드 §7.1 MRP 산출물) — 3h

MRP의 부분 풀링을 카운트 스무딩으로 근사: 셀(country×wave×edu) → 상위 셀
(country×wave) → country → marginal → uniform. 각 단계는 바로 위 단계를
사전분포(pseudo-count)로 쓴다:

```
p_L(v) = (count_L(v) + κ_L · p_{L-1}(v)) / (n_L + κ_L)      # L=1..depth, p_0 = marginal
```

T3의 JM 식과 같지만 (1) 여러 단계, (2) 사전이 uniform 0.5가 아니라 상위
단계 분포. κ_L은 T3의 `split.holdout_visible`로 단계별 1-D 탐색 (아래부터).

- 파일: `src/models/hier_backoff.py`, E004 파일에 "A" 결과 행 추가 (별도
  E005 파일로 빼도 됨 — parent: E004).
- 수용: 테스트 (depth=1, κ 동일 → E004와 동일 벡터), runner 4 스키마, Δ vs E004.
- stratum 선택 규칙: GIVEN 항목을 카디널리티 오름차순으로 최대 3개. 규칙 자체를
  docstring에. 실데이터 hardcode 금지.
- 관전 포인트: depth 2→3에서 이득이 줄거나 음수가 되면 그게 "풀링 없이는
  셀이 빈다"는 MRP 논지의 실측. 한 줄 기록.

---

## B. 첫 제출 준비 (제출은 돌아와서 해도 됨) — 90분

후보 = 그 시점 로컬 최고 (아마 E004 또는 E003+E004 결합). 절차는
`submissions/README.md` 그대로:

1. `submissions/2026-08-2X-<name>/` 에 `main.py` 단독 파일로 구성 — 우리
   `src/`를 import하지 말고 **필요한 코드를 main.py 하나에 인라인** (zip 루트에
   main.py, 의존 모듈은 같이 넣되 상대 import 확인). requirements.txt 불필요
   (numpy/pandas 이미지 내장).
2. zip 빌드: `cd submissions/<dir> && zip -r ../sub.zip .` (zip 없으면
   `python -m zipfile -c ../sub.zip .`이 아니라 폴더 래핑 없이 루트에 main.py
   오게 — `python tools/check_submission_zip.py sub.zip`으로 확인).
3. 공식 그레이더 3 스키마:
   ```
   cd external/starter-kit
   python score.py --submission <path-to-unzipped-dir> --data _sandbox/unicef --schema data/unicef.json --phase 1
   (world_bank, unhcr 반복)
   ```
   3개 PASS + 각 소요시간 기록 (합 < 900 s, 실제는 수십 초).
4. `submissions/README.md` 로그 표에 행 추가: 로컬 skill 4개, **Expected LB**
   (= unhcr 열은 soft gating 때문에 로컬보다 낮을 수 있음 — 예상을 적어둠),
   Reported 비움.
5. 예상-실제 비교는 돌아와서 1/day 제출 후.

주의: `predict()`는 악기당 1회, 모델 가중치는 import 시점 로드, 네트워크 없음.
우리 카운트 모델은 가중치 파일이 없으니 해당 없음.

---

## D4 마무리 (어느 쪽이든, 30분)

- `docs/log.md`에 4일 항목: 각 T의 가설→숫자→결론, 읽은 논문 4~5편 ✅ 상태,
  열린 질문 (예: 실데이터 ã 분포, wave 조건화 효과).
- `python scripts/render_tree.py` → `docs/tree.md` 갱신.
- `git push`.
