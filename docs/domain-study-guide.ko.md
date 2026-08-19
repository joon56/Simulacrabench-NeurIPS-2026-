# 도메인 공부 가이드 (한국어) — domain.md 실행판

[[domain]]의 한국어 학습 가이드. 원문(영어)이 canonical — 상세 서지는 원문 참조.
이 문서는 "무엇을, 어떤 깊이로, 어떤 산출물을 남기며 읽나"를 정한다.
각 문항에 논문 제목과 링크 포함 — 이 문서만으로 바로 읽기 시작 가능.

## 0. 총론 — "논문을 순서대로 정독"은 틀린 방법

이 리스트는 ~40편. 전부 정독하면 대회가 끝난다. 원칙 4개:

1. **실험이 논문을 부른다.** E003(soft gating)을 시작하면 그때 §9.1과 Chen &
   Goodman을 읽는다. 읽기가 실험을 만드는 게 아니라 실험 큐가 읽기 큐를 만든다.
2. **논문당 산출물 1개.** 코드 조각, 실험 파일의 설계 결정 한 줄, 또는 이 문서에
   추가하는 요약 3줄. 산출물 없는 읽기는 안 한 것과 같다 (discipline rule 6과 동일).
3. **3-pass 읽기** (Keshav): ① 초록+그림+결론 5분 → 버릴지 결정. ② 본문 훑되
   증명 건너뜀 30분 → 아이디어 추출. ③ 재현 수준 정독 — **구현할 논문에만**.
4. **티어를 지킨다.** 아래 각 문항에 붙인 티어:
   - **[구현]** = 3-pass 전부. 수식을 코드로 재현. 4~5편뿐.
   - **[설계]** = pass 2까지. 특정 섹션만. 설계 결정에 인용.
   - **[스킴]** = pass 1만 (15~30분). "이런 게 있고 왜 안 쓰는지"를 알기 위함.
   - **[사전]** = 통독 금지. 필요할 때 해당 장만 찾아 읽는 참고서.

주간 리듬: 실험 코딩 중심, 읽기는 하루 1~2편 pass 1–2, [구현] 정독은 주 1편.

**진행 방식: 세션당 논문 1편, `/paper-session` 스킬로.** 새 세션에서
"/paper-session 3.2" 또는 "Guo 2017 시작"이라고 하면: ① 읽을/스킵할 논문 내부
섹션 지도 + 자가확인 질문 3개 제시 → ② 읽는 동안 질문 응답 → ③ 티어별 산출물
공동 제작 → ④ 이 문서에 ✅+3줄 요약 기록, `study:` 커밋. 완료 항목은 첫 줄에
`✅ (날짜)` 표시.

---

## §3. Proper scoring rule과 캘리브레이션 ← **최우선 (메트릭 그 자체)**

> 리더보드 = log score. 유일한 local strictly proper rule. 과신한 오답을 무한히
> 벌하고(플로어 덕에 −6.9 nats로 캡), 진짜 믿는 분포를 내는 게 기대점수 최적.
> 0.01→0.05로 올리면 +1.6 nats, 0.9→0.99는 +0.1 — 비대칭. 헤지가 이긴다.

- **3.1** [설계] Gneiting & Raftery (2007), **"Strictly Proper Scoring Rules,
  Prediction, and Estimation"**, *JASA* — <https://doi.org/10.1198/016214506000001437>
  Proper rule 이론의 결정판. 공부법: §1–2(정의·특성화)와 log score 항목만.
  증명 스킵. 산출물: "왜 최적 제출 = 진짜 사후분포인가" 3줄 요약. 90분.
- **3.2** [구현] Guo, Pleiss, Sun & Weinberger (2017), **"On Calibration of
  Modern Neural Networks"**, *ICML* — <https://arxiv.org/abs/1706.04599>
  현대 신경망은 과신, 스칼라 온도 하나로 복구. 공부법: 방법 섹션(§4)만 정독 후
  **20줄 구현**(held-out log-loss 최소화하는 T 피팅)을 src/eval에 넣어둠.
  모든 학습 모델의 출구에 붙일 부품. 2시간.
- **3.3** [설계] Kull et al. (2019), **"Beyond temperature scaling: Obtaining
  well-calibrated multi-class probabilities with Dirichlet calibration"**,
  *NeurIPS* — <https://arxiv.org/abs/1910.12656>
  클래스별 미스캘리브레이션엔 온도 하나로 부족(희귀 레벨 NA_GATED/refused vs
  다수 Likert 중간값). 공부법: temperature가 underfit할 때만 소환. 지금은
  pass 1만. 30분.
- **3.4** [구현] Chen & Goodman (1996), **"An Empirical Study of Smoothing
  Techniques for Language Modeling"**, *ACL* — <https://aclanthology.org/P96-1041/>
  카운트 모델 스무딩의 실증 플레이북. add-one은 나쁘고 하위분포와의 보간
  (Jelinek–Mercer)이 강하다. 공부법: §2–3만. 산출물: 우리 backoff 사다리
  (stratum→marginal→uniform)의 보간 가중치를 held-out으로 튜닝하는 코드 —
  E004+ 재료. 2시간.

## §9. 런칭 후 우선순위 (08-19) ← **§3 다음으로 먼저**

- **9.1** [구현·논문 아님] **근사 gate = 추정 구조.** unhcr gate 일치도 중앙값
  0.83. hard coupling은 17%에서 −6.9 nats. 공부법: 논문 없음 — [[domain]] §9.1
  설계 노트를 읽고 E003으로 구현: 가시 행에서 item별 일치율 → beta-binomial
  수축 → 혼합 가중치. 이것이 첫 번째 새 실험.
- **9.2** [설계·데이터 읽기] **RPIS 공개 라운드** (UNHCR 악기 = Enhanced RPIS):
  - 9차 보고서 (2024.6): <https://reliefweb.int/report/lebanon/nineth-regional-survey-syrian-refugees-perceptions-and-intentions-return-syria-rpis-egypt-iraq-lebanon-jordan-june-2024>
  - Flash 조사 (2025.2): <https://www.3rpsyriacrisis.org/wp-content/uploads/2025/02/UNHCR_Flash_Intention_Survey2025.pdf>
  - ERPIS 보고서 (2025.9, 필드워크 일치): <https://reliefweb.int/report/syrian-arab-republic/enhanced-regional-survey-syrian-refugees-perceptions-and-intentions-return-syria-egypt-iraq-jordan-lebanon-september-2025>
  공부법: 논문 읽듯 말고 **집계표 추출 작업**으로 — PDF에서 문항별 분포표를
  CSV로 옮김 → bundled_artifact 형태의 prior 파일. 산출물 = 데이터 파일 +
  출처 기록(method 공개 의무). 반나절.
- **9.3** [구현·논문 아님] **wave 조건화.** 59개 multi-select의 라운드
  confound. sentinel rate를 wave(GIVEN)로 조건화. E00X 한 줄 설계.
- **9.4** [스킴] **캡 제거 후 제출 정책** — §8.2와 같이 읽음. 아래 참조.

## §1. IRT — 잠재특성 응답 모델

> 응답행렬의 생성 스토리. GRM(순서형)·Bock nominal(무순서)·GPCM이 문항형별
> 카테고리 우도를 줌. 행렬분해와 같은 것(§1.5)이 핵심 통찰.

- **1.1** [설계] Samejima (1969), **"Estimation of latent ability using a
  response pattern of graded scores"**, *Psychometrika Monograph* —
  <https://doi.org/10.1007/BF03372160>
  순서형 Likert의 기본 우도(GRM: 누적 2PL 경계curve 차분). 공부법: 원논문
  정독 불필요 — 아무 IRT 교재 GRM 장이 더 빠름. 산출물: GRM 확률식 1개를
  torch로 10줄. 1시간.
- **1.2** [설계] Bock (1972), **"Estimating item parameters and latent ability
  when responses are scored in two or more nominal categories"**,
  *Psychometrika* — <https://doi.org/10.1007/BF02291411>
  무순서 카테고리 = 잠재특성 위 softmax. "우리 모델 head는 intercept+slope
  softmax"라는 결론만. NA_GATED를 하나의 nominal level로 두는 근거. 30분.
- **1.3** [구현] Wu, Davis, Domingue, Piech & Goodman (2020), **"Variational
  Item Response Theory: Fast, Accurate, and Expressive" (VIBO)**, *EDM* —
  <https://arxiv.org/abs/2002.00276> · 코드: <https://github.com/mhw32/variational-item-response-theory-public>
  인코더가 응답→능력 사후분포 (amortized IRT). 공부법: 모델·ELBO 섹션 정독 +
  공개 코드 훑기. 우리 잠재요인 모델의 뼈대 후보. 산출물: 사후 불확실성이
  예측분포에 들어가는 경로 요약 + 프로토타입 계획. 3시간.
- **1.4** [코드 읽기] **py-irt / torch_measure** —
  <https://github.com/nd-ball/py-irt> · <https://aimslab.stanford.edu/torch_measure/>
  논문 대신 API. torch_measure의 polytomous 지원 여부부터 실물 확인(§8.5),
  없으면 py-irt. 1시간 코드 탐색.
- **1.5** [스킴] Bergner et al. (2012), **"Model-Based Collaborative Filtering
  Analysis of Student Response Data: Machine-Learning Item Response Theory"**,
  *EDM* — <https://eric.ed.gov/?id=ED537194>
  IRT는 logistic link 저랭크 분해 — §1과 §2를 하나로 묶는 면허장. 20분.
- **1.6** [스킴] Muraki (1992), **"A Generalized Partial Credit Model"**,
  *APM* — <https://doi.org/10.1177/014662169201600206>
  GRM의 인접카테고리 대안. 캘리브레이션 다를 수 있어 A/B 후보로만 기억. 20분.

## §2. 저랭크 행렬완성

> 같은 문제의 다른 프레임. 범주형이므로 finite-alphabet 완성(≈다항 우도 +
> nuclear norm)이 직접 해당 — 결국 §1과 수렴.

- **2.1** [스킴] Davenport, Plan, van den Berg & Wootters (2014), **"1-Bit
  Matrix Completion"**, *Information and Inference* —
  <https://arxiv.org/abs/1209.3672>
  이진 관측 저랭크 복원 이론. 목적함수 = trace-norm 정칙 log-loss라는 사실만. 20분.
- **2.2** [설계] Lafond, Klopp, Moulines & Salmon (2014), **"Probabilistic
  low-rank matrix completion on finite alphabets"**, *NIPS* —
  <https://papers.neurips.cc/paper/5358-probabilistic-low-rank-matrix-completion-on-finite-alphabets.pdf>
  이 태스크와 이론적으로 가장 가까움(범주형+우도+log-loss). 공부법: 문제
  설정·목적함수만 정독, 복원 정리 스킵. 산출물: lowrank 모델 목적함수 확정
  한 줄. 1시간.
- **2.3** [스킴] Candès & Recht (2009), **"Exact Matrix Completion via Convex
  Optimization"**, *FoCM* — <https://arxiv.org/abs/0805.4471>
  고전 정리. whole-respondent 마스킹은 uniform sampling 가정 위반이라는
  경고가 수확. 15분.
- **2.4** [코드 읽기] Mazumder, Hastie & Tibshirani (2010), **"Spectral
  Regularization Algorithms for Learning Large Incomplete Matrices"
  (softImpute)**, *JMLR* — <https://jmlr.org/papers/v11/mazumder10a.html>
  논문 말고 구현체로. 원핫→SVD→정규화 sanity check용. 30분.
- **2.5** [스킴] van Buuren & Groothuis-Oudshoorn (2011), **"mice: Multivariate
  Imputation by Chained Equations in R"**, *JSS* —
  <https://doi.org/10.18637/jss.v045.i03>
  고전 통계 베이스라인. FCS(각 문항을 나머지로 회귀) 멘탈모델만. 20분.
- **2.6** [스킴] Stekhoven & Bühlmann (2012), **"MissForest — non-parametric
  missing value imputation for mixed-type data"**, *Bioinformatics* —
  <https://doi.org/10.1093/bioinformatics/btr597>
  RF 반복 대치. RF 투표확률은 미캘리브 — §3 재캘리브 필요 사례로 기억. 15분.

## §4. 딥 생성 대치 모델 ← **읽는 목적이 "면역"**

> 벤치마크 증거: 튜닝된 단순 방법이 딥 생성 대치와 대등 이상, GAN은 불안정.
> phase 2 후보로만, 로컬에서 이기면.

- **4.4** [설계] Jäger, Allhorn & Bießmann (2021), **"A Benchmark for Data
  Imputation Methods"**, *Frontiers in Big Data* —
  <https://doi.org/10.3389/fdata.2021.693674>
  **이 섹션에서 이것부터.** 69개 데이터 결과표만 정독. "딥은 증명 후 채용"
  원칙의 실증 근거. 1시간.
- **4.2** [설계] Mattei & Frellsen (2019), **"MIWAE: Deep Generative Modelling
  and Imputation of Incomplete Data Sets"**, *ICML* —
  <https://arxiv.org/abs/1812.02633>
  유일하게 우도로 학습, p(missing|observed)가 곧 제출 분포. 딥 업그레이드
  1순위. ELBO 섹션 pass 2. 1.5시간.
- **4.1** [스킴] Kotelnikov et al. (2023), **"TabDDPM: Modelling Tabular Data
  with Diffusion Models"**, *ICML* — <https://arxiv.org/abs/2209.15421>
  multinomial diffusion. 샘플링 기반 분포추정은 log-loss 비싸다는 점만. 20분.
- **4.3** [스킴] Yoon, Jordon & van der Schaar (2018), **"GAIN: Missing Data
  Imputation using Generative Adversarial Nets"**, *ICML* —
  <https://arxiv.org/abs/1806.02920>
  우도 없음, 불안정. 안 쓰는 이유를 말할 수 있으면 끝. 15분.

## §5. 서베이 방법론 ← **읽기보단 어휘 장착**

- **5.1** [설계] Rubin (1976), **"Inference and missing data"**, *Biometrika* —
  <https://doi.org/10.1093/biomet/63.3.581>
  MCAR/MAR/MNAR과 ignorability. 정의부만. 산출물: "NA_GATED는 결측이 아니라
  gate의 결정함수, nonresponse level은 MNAR 가능" 구분을 preprocess 주석에
  명문화. 1시간.
- **5.2** [사전] Little & Rubin, ***Statistical Analysis with Missing Data***
  (3rd ed., Wiley) — <https://doi.org/10.1002/9781119482260>
  통독 금지. 논쟁 생길 때 해당 장만.
- **5.3** [사전] Groves et al., ***Survey Methodology*** (2nd ed., Wiley) —
  routing/universe 어휘용. 스킵 패턴 장만.
- **5.4** [스킴] de Leeuw (2005), **"To Mix or Not to Mix Data Collection Modes
  in Surveys"**, *J. Official Statistics* —
  <https://bebr.ufl.edu/sites/default/files/To%20Mix%20or%20Not%20to%20Mix%20Data%20Collection%20Modes%20in%20Surveys.pdf>
  국가=모드=응답스타일 시프트 → 국가를 1급 조건 변수로. 20분.

## §6. LLM 서베이 시뮬레이션 ← **"왜 안 되는가"를 아는 게 목적**

> 결론 먼저: 페르소나 프롬프팅 원샷은 log-loss에 불리 (순서 편향, 과예리
> 분포). 유효한 사용법은 ① 옵션 텍스트 prior를 backoff 밑바닥으로(§8.4),
> ② 분포 매칭 파인튜닝(6.6/6.7), ③ 명시적 분포 발화 유도(6.5).

- **6.1** [설계] Dominguez-Olmedo, Hardt & Mendler-Dünner (2024),
  **"Questioning the Survey Responses of Large Language Models"**, *NeurIPS
  oral* — <https://arxiv.org/abs/2306.07951>
  순서편향 제거하면 균등분포로 붕괴. LLM 컴포넌트의 옵션 순서 랜덤화가 필수인
  이유. 결과 그림 중심 pass 2. 1시간.
- **6.2** [스킴] Santurkar et al. (2023), **"Whose Opinions Do Language Models
  Reflect?"**, *ICML* — <https://arxiv.org/abs/2303.17548>
  인구통계 스티어링으로 갭 안 닫힘 (OpinionQA). 30분.
- **6.3** [스킴] Argyle et al. (2023), **"Out of One, Many: Using Language
  Models to Simulate Human Samples"**, *Political Analysis* —
  <https://arxiv.org/abs/2209.06899>
  silicon sampling 원조 낙관론. 상관 fidelity 생존, 캘리브 분포 fidelity 사망
  — 6.1/6.2와 세트로. 30분.
- **6.4** [스킴] Tjuatja et al. (2024), **"Do LLMs Exhibit Human-like Response
  Biases? A Case Study in Survey Design"**, *TACL* —
  <https://arxiv.org/abs/2311.04076>
  + Bisbee et al. (2024), **"Synthetic Replacements for Human Survey Data? The
  Perils of Large Language Models"**, *Political Analysis*.
  LLM은 인간 응답편향(묵종·극단화) 재현 실패 + 페르소나 분포는 과예리
  (log-loss 최악 실패형). 30분.
- **6.5** [설계] Meister, Guestrin & Hashimoto (2025), **"Benchmarking
  Distributional Alignment of Large Language Models"**, *NAACL* —
  <https://arxiv.org/abs/2411.05403>
  분포 추출 방식이 성능 좌우: 토큰확률 < 명시적 분포 발화. LLM 쓸 경우의 추출
  프로토콜. 1시간.
- **6.6** [설계] Cao et al. (2025), **"Specializing Large Language Models to
  Simulate Survey Response Distributions for Global Populations"**, *NAACL* —
  <https://arxiv.org/abs/2502.07068>
  국가별 분포매칭 파인튜닝은 통함, 미본 문항 일반화가 한계. 지금 pass 1. 30분.
- **6.7** [설계] Suh et al. (2025), **"Language Model Fine-Tuning on Scaled
  Survey Data for Predicting Distributions of Public Opinions" (SubPOP)**,
  *ACL* — <https://arxiv.org/abs/2502.16761>
  "인구통계 블록 → 분포"가 대규모 파인튜닝으로 학습됨의 최강 증거. phase 2에
  LLM 갈지 결정할 때 정독. 지금 pass 1. 30분.
- **6.8** [스킴] 묶음: Huang, Wu & Wang (2025), **"How Many Human Survey
  Respondents is a Large Language Model Worth?"** —
  <https://arxiv.org/abs/2502.17773> (LLM prior의 유효표본크기 = ALPHA 정하는
  프레임, 나중에 승격 가능) · Choi et al. (2026), **"Beyond the Mean:
  Three-Axis Fidelity"** — <https://arxiv.org/abs/2606.28963> · Park et al.,
  **"LLM Agents Grounded in Self-Reports"** — <https://arxiv.org/abs/2411.10109>
  · Kim & Lee (2023), **"AI-Augmented Surveys"** —
  <https://arxiv.org/abs/2305.09620>. 총 30분.

## §7. 대회 모양에 맞는 기계 (08-11 보강)

- **7.1** [구현] Park, Gelman & Bafumi (2004), **"Bayesian Multilevel
  Estimation with Poststratification: State-Level Estimates from National
  Polls" (MRP)**, *Political Analysis* —
  <https://sites.stat.columbia.edu/gelman/research/published/parkgelmanbafumi.pdf>
  held-out 응답자 = GIVEN 셀. 계층 부분풀링이 empty-cell fallback의 원리적
  해법. 공부법: 모델 구조만 정독, Stan 재현 불필요 — 계층 스무딩 카운트로
  근사. 산출물: GIVEN-stratum backoff의 풀링 구조 설계. 2시간.
- **7.2** [설계] Rendle (2010), **"Factorization Machines"**, *ICDM* —
  <https://doi.org/10.1109/ICDM.2010.127>
  cold-start를 feature 잠재요인으로. lowrank가 미본 응답자를 못 다루는 문제의
  표준 다리. 모델식만. 45분.
- **7.3** [스킴] Niculescu-Mizil & Caruana (2005), **"Predicting Good
  Probabilities with Supervised Learning"**, *ICML* —
  <https://doi.org/10.1145/1102351.1102430>
  어떤 분류기가 확률을 제대로 내는가: RF/NN 그럭저럭, 부스팅·NB 왜곡. GBDT
  쓰면 재캘리브 필수. 30분.
- **7.4** [설계+실험] Hollmann et al. (2025), **"Accurate predictions on small
  data with a tabular foundation model" (TabPFN v2)**, *Nature* —
  <https://www.nature.com/articles/s41586-024-08328-6> · 코드:
  <https://github.com/PriorLabs/TabPFN>
  공부법: 논문 반, 실험 반 — 샌드박스에서 직접 돌려봄(행 제한, 다클래스,
  NA_GATED 처리). 읽기보다 측정. 반나절.
- **7.5** [설계] Böckenholt (2012), **"Modeling Multiple Response Processes in
  Judgment and Choice" (IRTree)**, *Psychological Methods* —
  <https://doi.org/10.1037/a0028111>
  응답 = 이진 의사결정 트리 분해. P(gated)×P(refuse|asked)×P(값|응답)이 우리
  옵션벡터 구조와 정확히 일치. E00X 후보 설계로 정독. 1.5시간.

## §8. 런칭 보강 (08-17)

- **8.1** [설계] Angelopoulos, Bates, Fannjiang, Jordan & Zrnic (2023),
  **"Prediction-Powered Inference"**, *Science* —
  <https://arxiv.org/abs/2301.09633> · 후속: **PPI++** —
  <https://arxiv.org/abs/2311.01453>
  주최측 공식 프레임. 본문 아이디어(모델 오차를 라벨 표본으로 측정·차감)만.
  산출물: method-4p §1 서사 문단 1개. 1.5시간. **method 쓰기 전 필독.**
- **8.2** [스킴] Dwork et al. (2015), **"The reusable holdout: preserving
  validity in adaptive data analysis"**, *Science* —
  <https://doi.org/10.1126/science.aaa9375> · Blum & Hardt (2015), **"The
  Ladder: A Reliable Leaderboard for Machine Learning Competitions"** —
  <https://arxiv.org/abs/1502.04585>
  노이즈 리더보드의 정보 한계. 결론만 pass 1로 근거 확보. 30분. **첫 제출 전.**
- **8.3** [설계+데이터] Woods et al. (2011), **"Improving digit span assessment
  of short-term verbal memory"**, *JCEN* (digit span 규준: forward ML≈6.8±1.1)
  · Kessels et al. (2000), **"The Corsi Block-Tapping Task: Standardization and
  Normative Data"**, *Applied Neuropsychology* (span≈6.2±1.3, 교육 민감).
  공부법: 규준 분포를 숫자로 추출 → wb informed prior CSV. RPIS와 같은
  "표 추출 작업". 2시간.
- **8.4** [코드 읽기] **`external_model` 독스트링** —
  `external/starter-kit/baseline/external_model/main.py`.
  주최측 공인 LLM 레시피 설계 문서. 정독 1시간. LLM prior 실험 전 필독.
- **8.5** [코드 읽기] **torch_measure** — §1.4와 같이. polytomous 확인이 1번 과제.

---

## 주차 플랜 (실험 일정에 종속)

| 주 | 실험 | 그 주의 읽기 (티어 포함) |
|---|---|---|
| 이번 주 | E003 soft gating + 첫 제출 | §3.2 temperature [구현], §9.1, 8.2 [스킴], 3.1 [설계] |
| +1주 | E004 GIVEN-stratum backoff | §3.4 Chen&Goodman [구현], 7.1 MRP [구현], 5.1 [설계] |
| +2주 | unhcr/wb prior 아티팩트 | §9.2 RPIS 표 추출, 8.3 규준 추출, 8.4 코드 |
| +3주 | 잠재요인 (IRT/FM/TabPFN) | §1.3 VIBO [구현], 7.2 FM, 7.4 TabPFN 실측, 1.5 |
| +4주~ | IRTree·하이브리드·캘리브 | §7.5, 4.4→4.2, 3.3, §6 설계 3편 |
| phase 2 전 | method-4p 집필 | §8.1 PPI 정독, §6.6/6.7 (LLM 갈 경우) |

**금지사항**: 실험 큐가 비었는데 읽기만 쌓는 것. 논문이 실험을 앞지르면 멈추고
코딩. 반대로 [스킴] 문서를 정독하며 시간 쓰는 것도 금지 — 티어가 곧 예산.
