# Domain reading list — SimulacraBench

Study document for the six technical areas underlying this competition: probabilistic completion of a categorical/ordinal survey response matrix, scored by mean log-loss (skill = 1 + log_score/U). The metric makes this a *calibration* contest, not an accuracy contest, so the reading list is weighted toward (1) psychometric response models that give per-item categorical likelihoods, (2) low-rank structure across respondents and items, (3) proper scoring rules and probability calibration, (4) deep generative imputers and the evidence on when they beat simple baselines, (5) survey methodology — especially skip-logic/structural missingness, since NA_GATED is a scored answer level here — and (6) LLM survey simulation, whose known calibration failures define the competition's hybrid differentiation angle. All links verified against primary sources (arXiv, publisher pages, official proceedings); entries within each section are ranked by importance for this competition. Competition mechanics and the exact submission contract live in [[starter-kit-notes]]; experiment history in [[log]]. §8 (2026-08-17) adds the areas the launch kit made load-bearing: prediction-powered inference as the official downstream framing, adaptive-analysis limits of the noised leaderboard, cognitive-test norm priors for the re-classed World Bank items, the organizer-sanctioned LLM-prior recipe, and `torch_measure`. (Terminology note: some "Relevance" lines below say "Track A"/"Track B" from the original briefing. The official task has no tracks — read "Track B" as the actual task (held-out respondents, GIVEN block visible) and "Track A" as auxiliary within-respondent MCAR validation.)

---

## 1. Item Response Theory for imputation

IRT models the probability of each response level of item *j* by respondent *i* through a low-dimensional latent trait — exactly the generative story of a survey matrix. The classical family (2PL for binary; Samejima's graded model for ordered Likert; Bock's nominal model for unordered categories; Muraki's generalized partial credit in between) supplies per-item-type categorical likelihoods; modern amortized/variational inference makes them fit in minutes on this competition's ~37k respondents × up to 285 items, and the matrix-factorization view connects them directly to Section 2. (The 2PL itself originates in Birnbaum's chapters of Lord & Novick's 1968 *Statistical Theories of Mental Test Scores*; the modern references below cover it operationally.)

1. **Samejima, F. (1969). "Estimation of latent ability using a response pattern of graded scores." *Psychometrika Monograph Supplement No. 17*.**
   Link: <https://doi.org/10.1007/BF03372160>
   Introduces the Graded Response Model (GRM): cumulative 2PL boundary curves whose differences give the probability of each ordered category, with ML estimation of the latent trait from a full graded response pattern. Still the default IRT model for Likert-type data.
   Relevance: the canonical likelihood for the competition's ordered Likert items — GRM category probabilities are exactly the per-level distribution a submission must output for ordinal cells.

2. **Bock, R. D. (1972). "Estimating item parameters and latent ability when responses are scored in two or more nominal categories." *Psychometrika* 37(1), 29–51.**
   Link: <https://doi.org/10.1007/BF02291411>
   Introduces the Nominal Response Model: a multinomial-logistic (softmax) link from the latent trait to unordered category probabilities, estimated by Newton–Raphson/EM-style maximum likelihood.
   Relevance: gives the categorical-logistic likelihood for nominal items (and multi-select items decomposed into indicators); a softmax over per-category intercept+slope is also the natural head for any latent-factor model here, including treating NA_GATED as one more nominal level where gating cannot be predicted deterministically.

3. **Wu, M., Davis, R. L., Domingue, B. W., Piech, C., & Goodman, N. (2020). "Variational Item Response Theory: Fast, Accurate, and Expressive." *Proc. Educational Data Mining (EDM) 2020*.**
   Link: <https://arxiv.org/abs/2002.00276> · Code: <https://github.com/mhw32/variational-item-response-theory-public>
   Derives VIBO, an amortized variational lower bound for IRT: an inference network maps a respondent's observed responses to a posterior over ability, trained jointly with item parameters. Matches HMC accuracy while being orders of magnitude faster (e.g. 1.56M respondents: 217 h HMC vs ~800 s VIBO) and extends cleanly to deep/nonlinear response functions.
   Relevance: the template for both tracks — for Track A, amortized inference imputes masked items from a respondent's unmasked ones in one forward pass; for Track B, the encoder can be conditioned on the demographic block only. Fits comfortably inside the 900 s whole-run budget.

4. **Lalor, J. P., & Rodriguez, P. (2023). "py-irt: A Scalable Item Response Theory Library for Python." *INFORMS Journal on Computing* 35(1).**
   Link: <https://arxiv.org/abs/2203.01282> · Code: <https://github.com/nd-ball/py-irt>
   A Pyro/PyTorch library for Bayesian IRT (1PL/2PL/4PL, multidimensional variants) with GPU-accelerated stochastic variational inference, built for large response matrices.
   Relevance: fastest route to a working 2PL/GRM baseline without hand-rolling SVI; pinnable dependency for the offline Docker submission.

5. **Bergner, Y., Dröschler, S., Kortemeyer, G., Rayyan, S., Seaton, D. T., & Pritchard, D. E. (2012). "Model-Based Collaborative Filtering Analysis of Student Response Data: Machine-Learning Item Response Theory." *Proc. EDM 2012* (ERIC ED537194).**
   Link: <https://eric.ed.gov/?id=ED537194>
   Shows Rasch, 2PL, and multidimensional M2PL are special cases of logistic model-based collaborative filtering fit by regularized alternating optimization with cross-validated hyperparameters — i.e., IRT *is* low-rank matrix factorization with a logistic link.
   Relevance: the bridge between Sections 1 and 2 — licenses fitting "IRT" with ALS/SGD machinery, choosing latent rank by held-out log-loss on the sandbox, and viewing the planned lowrank and irt model families as one continuum.

6. **Muraki, E. (1992). "A Generalized Partial Credit Model: Application of an EM Algorithm." *Applied Psychological Measurement* 16(2), 159–176.**
   Link: <https://doi.org/10.1177/014662169201600206>
   Generalizes the partial credit model with an item-level discrimination parameter, estimated via EM; adjacent-category logits instead of GRM's cumulative logits.
   Relevance: the main alternative ordinal likelihood to GRM — worth A/B-testing per instrument since adjacent-category vs cumulative parameterizations can differ in calibration on skewed Likert marginals.

## 2. Low-rank matrix completion for categorical/survey data

The alternative (and complementary) framing: the response matrix is approximately low-rank, and masked cells are recovered from observed ones. The classical theory is for real-valued matrices under a squared loss; the entries here are categorical, so the directly applicable line is one-bit/finite-alphabet completion, which replaces the Gaussian observation model with a logistic/multinomial likelihood — at which point it converges with the IRT-as-factorization view above. MICE and missForest are the classical imputation baselines any deep method must beat.

1. **Davenport, M. A., Plan, Y., van den Berg, E., & Wootters, M. (2014). "1-Bit Matrix Completion." *Information and Inference* 3(3), 189–223.**
   Link: <https://arxiv.org/abs/1209.3672>
   Recovers a low-rank matrix from binary observations generated through a link function (logistic/probit), via nuclear-norm-constrained maximum likelihood, with near-optimal error bounds; shows the noisy binary problem is well-posed where the noiseless one is degenerate.
   Relevance: the rigorous version of "low-rank + logistic link" for the binary items; its constrained-MLE objective is exactly a trace-norm-regularized log-loss — training objective equals competition metric.

2. **Lafond, J., Klopp, O., Moulines, E., & Salmon, J. (2014). "Probabilistic low-rank matrix completion on finite alphabets." *NIPS 2014*, 1727–1735.**
   Link: <https://papers.neurips.cc/paper/5358-probabilistic-low-rank-matrix-completion-on-finite-alphabets.pdf>
   Extends one-bit completion to entries over a finite alphabet (multinomial observations) with nuclear-norm-penalized multinomial likelihood and recovery guarantees; explicitly motivated by incomplete survey data and voting patterns.
   Relevance: the closest theoretical match to this task's data model — categorical survey entries, likelihood-based low-rank completion, log-loss-native. Treat NA_GATED as one alphabet symbol and this is nearly the competition, minus the structure exploited by explicit skip-logic handling.

3. **Candès, E. J., & Recht, B. (2009). "Exact Matrix Completion via Convex Optimization." *Foundations of Computational Mathematics* 9, 717–772.**
   Link: <https://arxiv.org/abs/0805.4471>
   The foundational result: an n×n rank-r incoherent matrix can be exactly recovered from O(n^1.2 · r log n) uniformly sampled entries by nuclear-norm minimization.
   Relevance: background theory — explains when a survey-scale response matrix is a benign completion regime, and why incoherence/sampling assumptions matter here, where masking is whole-respondent (structured), not uniform.

4. **Mazumder, R., Hastie, T., & Tibshirani, R. (2010). "Spectral Regularization Algorithms for Learning Large Incomplete Matrices." *JMLR* 11, 2287–2322.**
   Link: <https://jmlr.org/papers/v11/mazumder10a.html>
   SoftImpute: iterative soft-thresholded SVD for nuclear-norm-regularized completion, scaling to very large matrices; the practical workhorse behind ALS-style completion.
   Relevance: the cheap, fast real-valued completion baseline (complete one-hot/ordinal-coded matrix, then normalize into probabilities) — useful as a speed-friendly component under the 900 s limit and as a sanity check on latent rank.

5. **van Buuren, S., & Groothuis-Oudshoorn, K. (2011). "mice: Multivariate Imputation by Chained Equations in R." *Journal of Statistical Software* 45(3).**
   Link: <https://doi.org/10.18637/jss.v045.i03>
   The reference implementation paper for MICE: fully conditional specification, imputing each variable from all others by iterated regression (logistic/polytomous for categoricals), producing multiple imputations that reflect uncertainty.
   Relevance: the classical survey-statistics baseline; its conditional-model view (each item given all others) is also the right mental model for Track A, and pooled multiple imputations give an honest predictive distribution rather than a point guess.

6. **Stekhoven, D. J., & Bühlmann, P. (2012). "MissForest — non-parametric missing value imputation for mixed-type data." *Bioinformatics* 28(1), 112–118.**
   Link: <https://doi.org/10.1093/bioinformatics/btr597>
   Iterative random-forest imputation for mixed continuous/categorical data; handles interactions and nonlinearity without a specified model, frequently outperforming MICE and KNN on point-imputation error.
   Relevance: strong nonlinear baseline; note RF class-vote frequencies are usable as probabilities but are typically miscalibrated — a concrete case where Section 3's recalibration (temperature/Dirichlet) is worth score.

## 3. Proper scoring rules and calibration

The leaderboard metric is the log score, the only local strictly proper scoring rule: expected score is uniquely maximized by reporting the true conditional distribution, and it punishes overconfident errors without bound (hence the floor/U-normalization in the skill formula). Practical consequences: never emit a near-zero probability for an event you cannot rule out; mix every prediction toward a marginal/uniform prior (Laplace-style smoothing, with the mixing weight tuned on held-out log-loss); and recalibrate any learned model's logits post hoc. Hedging beats confident wrong answers because log-loss is asymmetric in the extremes — moving a true-class probability from 0.01 to 0.05 gains ~1.6 nats, while moving it from 0.9 to 0.99 gains only ~0.1.

1. **Gneiting, T., & Raftery, A. E. (2007). "Strictly Proper Scoring Rules, Prediction, and Estimation." *JASA* 102(477), 359–378.**
   Link: <https://doi.org/10.1198/016214506000001437>
   The definitive theory of proper scoring rules: characterizes (strictly) proper rules via convex functionals, covers the logarithmic, Brier, and CRPS families, and links scoring to Bayes acts and information measures.
   Relevance: the theoretical foundation of the competition metric; makes precise why the optimal submission is the true posterior over answer levels and why "sharpness subject to calibration" is the right optimization target.

2. **Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). "On Calibration of Modern Neural Networks." *ICML 2017*.**
   Link: <https://arxiv.org/abs/1706.04599>
   Shows modern deep networks are systematically overconfident, introduces ECE-style diagnostics, and finds that temperature scaling — a single scalar dividing the logits, fit on a validation set — is remarkably effective at restoring calibration.
   Relevance: the single cheapest score-improving post-processor here: fit one temperature (per instrument, or per item type) on held-out cells by minimizing log-loss. Any neural/IRT/LLM-derived logits should pass through this before submission.

3. **Kull, M., Perello-Nieto, M., Kängsepp, M., Silva Filho, T., Song, H., & Flach, P. (2019). "Beyond temperature scaling: Obtaining well-calibrated multi-class probabilities with Dirichlet calibration." *NeurIPS 2019*.**
   Link: <https://arxiv.org/abs/1910.12656>
   Generalizes temperature/Platt scaling to a multi-class map (matrix scaling with off-diagonal regularization, derived from Dirichlet distributions), introducing classwise-ECE; consistently improves log-loss over temperature scaling when miscalibration differs by class.
   Relevance: survey items plausibly have per-level miscalibration (e.g. rare NA_GATED or "refused" levels vs common Likert midpoints); Dirichlet calibration is the natural upgrade when a single temperature underfits.

4. **Chen, S. F., & Goodman, J. (1996). "An Empirical Study of Smoothing Techniques for Language Modeling." *ACL 1996* (extended TR: Harvard TR-10-98).**
   Link: <https://aclanthology.org/P96-1041/>
   Systematic empirical comparison of additive (Laplace/Lidstone), Good–Turing, Katz, and interpolated smoothing for categorical count models under held-out cross-entropy; shows plain add-one is poor and interpolation with lower-order (backoff) distributions is consistently strong.
   Relevance: the empirical playbook for the competition's simplest layer — smoothed marginal and conditional frequency tables. Interpolating cell-level predictions with item marginals and global level frequencies (weights tuned on held-out log-loss) is exactly Jelinek–Mercer interpolation, and is the hedge that protects against the floored log score.

## 4. Deep generative tabular models for imputation

Deep generative imputers are the main "complex model" temptation. The three canonical families are GAN-based (GAIN), deep-latent-variable/importance-weighted (MIWAE — the only one trained directly on a log-likelihood bound), and diffusion (TabDDPM). The benchmark evidence is sobering: under realistic conditions, tuned simple methods are highly competitive, and GAN imputers in particular are unstable. Given a calibration-scored metric and a 900 s budget, these are candidates for the extended test-phase version only, and only if they beat the IRT/low-rank stack on the local harness.

1. **Kotelnikov, A., Baranchuk, D., Rubachev, I., & Babenko, A. (2023). "TabDDPM: Modelling Tabular Data with Diffusion Models." *ICML 2023*.**
   Link: <https://arxiv.org/abs/2209.15421>
   Applies denoising diffusion to heterogeneous tabular data — Gaussian diffusion for numerical features and multinomial diffusion for categoricals — and outperforms GAN/VAE tabular generators on generation quality across many benchmarks.
   Relevance: the strongest current deep generative prior for mixed-type survey rows; usable for imputation by conditioning/inpainting masked cells. Multinomial diffusion is the right categorical machinery, but sampling-based distribution estimates need many samples plus smoothing to be log-loss-competitive.

2. **Mattei, P.-A., & Frellsen, J. (2019). "MIWAE: Deep Generative Modelling and Imputation of Incomplete Data Sets." *ICML 2019*.**
   Link: <https://arxiv.org/abs/1812.02633>
   Trains a deep latent variable model on MAR-incomplete data by maximizing an importance-weighted (IWAE) bound on the observed-data likelihood, and imputes via self-normalized importance sampling from the conditional distribution of missing given observed.
   Relevance: the most metric-aligned deep option — it is trained on and evaluates an actual likelihood, and its importance-sampled p(missing | observed) is directly the categorical distribution a submission must output. The most principled deep upgrade path from amortized IRT.

3. **Yoon, J., Jordon, J., & van der Schaar, M. (2018). "GAIN: Missing Data Imputation using Generative Adversarial Nets." *ICML 2018*.**
   Link: <https://arxiv.org/abs/1806.02920>
   Adapts GANs to imputation: a generator fills missing entries and a discriminator classifies which entries were imputed, with a hint mechanism ensuring the generator learns the true conditional distribution.
   Relevance: historically important baseline to know, but adversarial training gives no likelihood and benchmark evidence (below) shows instability — read to understand the literature, not as a submission candidate.

4. **Jäger, S., Allhorn, A., & Bießmann, F. (2021). "A Benchmark for Data Imputation Methods." *Frontiers in Big Data* 4:693674.**
   Link: <https://doi.org/10.3389/fdata.2021.693674> · Code: <https://github.com/se-jaeger/data-imputation-paper>
   Systematic benchmark of classical (mean/mode, KNN, random forest) vs deep (discriminative DL, GAIN/VAE-style generative) imputers on 69 real datasets across missingness mechanisms and fractions. Finds tuned classical/discriminative methods (esp. random-forest-based) are on par with or better than deep generative imputers on categorical data, and GAN imputation is often unstable.
   Relevance: the empirical justification for this repo's strategy priority (calibrated simple models before hybrids) — evidence that deep imputers must *prove* incremental log-loss value on the local harness before earning a slot in the 100-min test-phase submission.

## 5. Survey methodology: skip logic, missingness mechanisms, design

The competition's framing decisions live in this literature. Rubin's taxonomy (MCAR/MAR/MNAR) defines when ignoring the missingness mechanism is valid: Track A's masking is MCAR by construction (ignorable), but *within* the data, structural "never asked" gating is deterministic given the gate answer — a completely different object from item nonresponse ("refused"/"don't know"), which is plausibly MNAR. Because NA_GATED is a scored level, predicting it well reduces to predicting the gate variables, and probability mass must be routed accordingly. Cross-country design (weights, modes, translations) matters mainly as a warning: per-country response-style differences are real signal for Track B's demographic conditioning.

1. **Rubin, D. B. (1976). "Inference and missing data." *Biometrika* 63(3), 581–592.**
   Link: <https://doi.org/10.1093/biomet/63.3.581>
   Founds the modern theory of missing data: defines missing completely at random / missing at random / distinctness, and proves the conditions (ignorability) under which likelihood and Bayesian inference can ignore the missingness process.
   Relevance: the formal reason Track A's MCAR masking can be modeled with plain observed-data likelihoods, and the framework for arguing about what "refused"/"don't know" levels mean vs structurally-not-asked cells.

2. **Little, R. J. A., & Rubin, D. B. (2019). *Statistical Analysis with Missing Data*, 3rd ed. Wiley.**
   Link: <https://doi.org/10.1002/9781119482260>
   The standard reference on missing-data methods: mechanisms, likelihood-based methods, EM, and multiple imputation, with explicit treatment of the difference between nonresponse and data that could not exist for a unit.
   Relevance: reference text backing the preprocessing decisions in `src/preprocess/` — in its terms, NA_GATED cells are not missing data at all but a deterministic function of the gate item, so they should be predicted through the gate's distribution, not imputed as nonresponse.

3. **Groves, R. M., Fowler, F. J., Couper, M. P., Lepkowski, J. M., Singer, E., & Tourangeau, R. (2009). *Survey Methodology*, 2nd ed. Wiley.**
   Link: <https://www.wiley.com/en-us/Survey+Methodology%2C+2nd+Edition-p-9780470465462>
   The canonical textbook of the total survey error framework: questionnaire design (including skip patterns/routing and their "universe" definitions), sampling and weighting, nonresponse, interviewer and mode effects.
   Relevance: the vocabulary for reading the three UN instruments' codebooks correctly — routing universes tell you exactly which (respondent, item) cells are structurally gated, which is the "likely free score" identified in the project brief.

4. **de Leeuw, E. D. (2005). "To Mix or Not to Mix Data Collection Modes in Surveys." *Journal of Official Statistics* 21(2), 233–255.**
   Link: <https://bebr.ufl.edu/sites/default/files/To%20Mix%20or%20Not%20to%20Mix%20Data%20Collection%20Modes%20in%20Surveys.pdf>
   Reviews mixed-mode survey designs and the evidence on mode effects: the same question yields systematically different response distributions by mode (interviewer vs self-administered), including acquiescence, social desirability, and extreme-response differences.
   Relevance: multi-country UN surveys mix modes and languages across countries; mode/country-level response-style shifts are a reason to include country (and any mode indicator in the demographic block) as a first-class conditioning variable, especially for Track B.

## 6. LLM survey simulation and its calibration failures

The competition's hybrid angle: can LLM priors about "what a person like X answers" add signal over psychometric baselines? The 2022–2024 literature established both the promise ("algorithmic fidelity") and the failure modes — ordering/label bias, distributions collapsing toward uniformity or toward over-extreme caricature, and RLHF flattening human-like response biases. The 2025–2026 line has moved to exactly this competition's problem: predicting *distributions* over answer options, and calibrating/fine-tuning models against real survey marginals. Net takeaway matches the project brief: raw persona-prompting is log-loss-unfavorable; LLM-derived logits are only useful after distribution-level fine-tuning or post-hoc recalibration against observed data.

1. **Dominguez-Olmedo, R., Hardt, M., & Mendler-Dünner, C. (2024). "Questioning the Survey Responses of Large Language Models." *NeurIPS 2024* (oral).**
   Link: <https://arxiv.org/abs/2306.07951>
   Evaluates 43 LLMs on the US Census American Community Survey and finds responses are dominated by ordering/labeling biases (strong "A" preference); after randomizing answer order to remove these biases, models of all sizes trend toward *uniformly random* answers, unlike any human population, and entropy-based signatures distinguish model from human response batches.
   Relevance: the sharpest warning for the hybrid: raw LLM answer distributions on census-style items carry little population signal and are dominated by artifacts. Any LLM component here must randomize/marginalize over option orderings and be validated on held-out log-loss before trusting it.

2. **Santurkar, S., Durmus, E., Ladhak, F., Lee, C., Liang, P., & Hashimoto, T. (2023). "Whose Opinions Do Language Models Reflect?" *ICML 2023*.**
   Link: <https://arxiv.org/abs/2303.17548>
   Builds OpinionQA from Pew American Trends Panel polls and compares LM answer distributions to those of 60 US demographic groups; finds substantial misalignment (comparable to the Democrat–Republican gap on climate change) that persists under explicit demographic steering.
   Relevance: defines the evaluation pattern this competition scales up (predict a demographic group's response distribution, compare distributionally) and shows demographic prompting alone does not close the gap — motivating training on the unmasked matrix instead of relying on the LLM's prior.

3. **Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J., Rytting, C., & Wingate, D. (2023). "Out of One, Many: Using Language Models to Simulate Human Samples." *Political Analysis* 31(3), 337–351.**
   Link: <https://arxiv.org/abs/2209.06899>
   The founding "silicon sampling" paper: conditioning GPT-3 on rich socio-demographic backstories from ANES respondents produces response distributions that correlate with the corresponding human subgroups ("algorithmic fidelity").
   Relevance: the optimistic case for Track B (demographics → response distribution via LLM); read together with #1, #2, and Bisbee et al. to see which parts of the claim survived replication — correlational fidelity did, calibrated distributional fidelity largely did not.

4. **Tjuatja, L., Chen, V., Wu, T., Talwalkar, A., & Neubig, G. (2024). "Do LLMs Exhibit Human-like Response Biases? A Case Study in Survey Design." *TACL* 12.**
   Link: <https://arxiv.org/abs/2311.04076> · Code: <https://github.com/lindiatjuatja/BiasMonkey>
   Tests whether LLMs reproduce known human response biases (acquiescence, allow/forbid asymmetry, odd/even scale effects, opinion floating) under controlled question perturbations; across nine models, LLMs — especially RLHF'd ones — generally fail to show human-like bias patterns while being sensitive to perturbations humans ignore.
   Relevance: response-style effects (acquiescence, extreme responding) are real structure in human Likert data that a good model of this matrix will capture — and LLMs specifically fail to reproduce them, another reason the psychometric layer must carry that signal. **Companion finding:** Bisbee, J., Clinton, J. D., Dorff, C., Kenkel, B., & Larson, J. M. (2024), "Synthetic Replacements for Human Survey Data? The Perils of Large Language Models," *Political Analysis* 32(4), 401–416 (<https://www.cambridge.org/core/journals/political-analysis/article/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models/B92267DC26195C7F36E63EA04A47D2FE>): persona-prompted ChatGPT feeling thermometers exaggerate extremity and understate variance vs matched humans — i.e., LLM-simulated distributions are over-sharp, the worst possible failure under log-loss.

5. **Meister, N., Guestrin, C., & Hashimoto, T. (2025). "Benchmarking Distributional Alignment of Large Language Models." *NAACL 2025*.**
   Link: <https://arxiv.org/abs/2411.05403>
   Benchmarks LMs on matching demographic groups' opinion *distributions*, systematically varying steering method and — critically — how the distribution is elicited (token log-probabilities vs sampling vs asking the model to verbalize a distribution). Finds log-prob-based readouts systematically understate achievable alignment, and models are better at *describing* a group's distribution than at simulating members of it.
   Relevance: directly actionable for the hybrid: if an LLM is used, elicit an explicit verbalized/expressed distribution over answer levels rather than reading token probabilities or sampling personas, then recalibrate (Section 3) on the unmasked shard.

6. **Cao, Y., Liu, H., Arora, A., Augenstein, I., Röttger, P., & Hershcovich, D. (2025). "Specializing Large Language Models to Simulate Survey Response Distributions for Global Populations." *NAACL 2025*.**
   Link: <https://arxiv.org/abs/2502.07068>
   Fine-tunes LLMs on country-level response distributions from two global cultural surveys (World Values Survey-style) using a first-token-probability objective that minimizes divergence between predicted and observed distributions; specialized models clearly beat zero-shot prompting, but still struggle on unseen questions.
   Relevance: the closest published analogue to this competition's cross-country setting — distribution-matching fine-tuning on multinational survey marginals works, but generalization to unseen items is the hard part; a caution for expecting LLM transfer to the unreleased UN items.

7. **Suh, J., Jahanparast, E., Moon, S., Kang, M., & Chang, S. (2025). "Language Model Fine-Tuning on Scaled Survey Data for Predicting Distributions of Public Opinions." *ACL 2025*.**
   Link: <https://arxiv.org/abs/2502.16761>
   Builds SubPOP (3,362 Pew/GSS-derived questions, ~70K subpopulation–response-distribution pairs) and fine-tunes LLMs to output subgroup response distributions directly; fine-tuning substantially reduces distributional distance to human data (up to ~46% over baselines) and improves generalization to unseen surveys and subgroups.
   Relevance: the strongest evidence that "demographic block → answer distribution" (exactly Track B) is learnable by LLM fine-tuning at scale; its distribution-matching loss is the log-loss-compatible way to train an LLM component, if compute and pinned-weights rules permit.

8. **Further recent work (2025–2026), verified but lower priority:** Huang, C., Wu, Y., & Wang, K. (2025), "How Many Human Survey Respondents is a Large Language Model Worth? An Uncertainty Quantification Perspective" (<https://arxiv.org/abs/2502.17773>) — a statistical framework quantifying the effective sample size of LLM-simulated respondents under model–human misalignment; useful for deciding how much weight an LLM prior deserves in an ensemble. Choi, E. C., Kim, Y., Pugalenthi, P., Chen, H.-E., & Huang, B.-R. (2026), "Beyond the Mean: Three-Axis Fidelity for Aligning LLM-Based Survey Simulators from Small Pilot Data," *Pluralistic Alignment @ ICML 2026* (<https://arxiv.org/abs/2606.28963>) — separates structural/marginal/individual fidelity and finds fine-tuning on small pilot data gives the best balance, mirroring this competition's "train on the unmasked shard" opportunity. Park, J. S., et al. (2024, rev. 2026), "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals" (<https://arxiv.org/abs/2411.10109>) — interview/self-report-grounded agents simulating 1,000+ real individuals' survey responses; the maximalist version of respondent-level simulation. Kim, J., & Lee, B. (2023), "AI-Augmented Surveys: Leveraging Large Language Models and Surveys for Opinion Prediction" (<https://arxiv.org/abs/2305.09620>) — fine-tuned LLM + question/respondent embeddings for missing-data imputation in the GSS (AUC ≈ 0.87), essentially an LLM-flavored version of this competition's Track A, and a template for injecting item *text* semantics into the matrix model.

## 7. Gaps filled on review (2026-08-11): cross-respondent machinery the six areas skip

The original six areas under-covered the specific *shape* of this competition's inference problem: predict a full categorical distribution for a respondent you have never seen, given only a demographic block, across countries of very different sizes. That is (a) exactly what survey statistics calls MRP, (b) exactly what recommender systems call cold-start with side information, and (c) a setting where per-item discriminative models and tabular foundation models are strong practical baselines the literature above never names.

1. **Park, D. K., Gelman, A., & Bafumi, J. (2004). "Bayesian Multilevel Estimation with Poststratification: State-Level Estimates from National Polls." *Political Analysis* 12(4), 375–385.** (Precursor: Gelman, A., & Little, T. C. (1997). "Poststratification into many categories using hierarchical logistic regression." *Survey Methodology* 23(2), 127–135, <http://www.stat.columbia.edu/~gelman/research/published/poststrat3.pdf>.)
   Link: <https://sites.stat.columbia.edu/gelman/research/published/parkgelmanbafumi.pdf>
   Multilevel regression and poststratification (MRP): fit a hierarchical logistic model of a response given demographic cells, with partial pooling across sparse cells, then aggregate over the population's cell structure. The survey field's standard machinery for "demographics → opinion estimate" in groups too small to estimate directly.
   Relevance: the closest statistical ancestor of this competition's core task — held-out respondents are exactly "cells" defined by the GIVEN block. Partial pooling across country × demographic cells is the principled answer to small-country instruments (and to the organizers' observed empty-support fallback problem: hierarchical shrinkage interpolates between cell-conditional and crowd marginal automatically, instead of hard-switching).

2. **Rendle, S. (2010). "Factorization Machines." *ICDM 2010*.** (Companion for theory: Jain, P., & Dhillon, I. S. (2013). "Provable Inductive Matrix Completion," <https://arxiv.org/abs/1306.0626>.)
   Link: <https://doi.org/10.1109/ICDM.2010.127>
   Factorization machines model all pairwise feature interactions through learned latent factors, unifying matrix factorization with feature-based regression — usable when a "user" is described only by features. Inductive matrix completion gives the recovery theory for completion with side information.
   Relevance: test respondents are cold-start users — no observed responses, only side features (the GIVEN block). FM-style "latent factors from features" is the standard bridge from the low-rank machinery of §2 (which alone cannot score a never-seen respondent) to this competition's actual setting.

3. **Niculescu-Mizil, A., & Caruana, R. (2005). "Predicting Good Probabilities with Supervised Learning." *ICML 2005*.**
   Link: <https://doi.org/10.1145/1102351.1102430>
   Compares ten learning methods by the quality of their predicted probabilities: boosting, SVMs, and naive Bayes are systematically distorted (each in a characteristic way), while bagged trees/random forests and neural nets are closer to calibrated; Platt scaling and isotonic regression repair most of the damage.
   Relevance: the missing practical baseline in §1–§4 is the obvious one — per-item gradient-boosted or forest classifiers conditioned on the GIVEN block (plus observed items where present). This paper says exactly which of those emit usable probabilities raw and which must pass through §3's recalibration before the log score sees them.

4. **Hollmann, N., Müller, S., Purucker, L., Krishnakumar, A., Körfer, M., Hoo, S. B., Schirrmeister, R. T., & Hutter, F. (2025). "Accurate predictions on small data with a tabular foundation model." *Nature* 637, 319–326.**
   Link: <https://www.nature.com/articles/s41586-024-08328-6> · Code/weights: <https://github.com/PriorLabs/TabPFN>
   TabPFN v2: a transformer pre-trained on millions of synthetic tabular tasks that performs in-context Bayesian-like prediction on a new table in seconds, outputting full class-probability distributions; outperforms tuned GBDT ensembles on datasets up to ~10k rows without any training.
   Relevance: a potential shortcut to a strong, *calibrated* per-item conditional model within the 900 s budget (fit is a forward pass), and the weights ship via `models.txt` (HF repo id) or bundled in the zip, with external resources disclosed per the FAQ. Constraints to test on the sandbox: row limits vs 5–15k TRAIN respondents per instrument, many-class items, and how it treats the NA_GATED level.

5. **Böckenholt, U. (2012). "Modeling Multiple Response Processes in Judgment and Choice." *Psychological Methods* 17(4), 665–678.**
   Link: <https://doi.org/10.1037/a0028111>
   IRTree models: decompose a categorical survey response into a tree of binary pseudo-decisions (e.g. respond vs refuse → direction → intensity), each with its own IRT model, separating content traits from response-style/nonresponse processes.
   Relevance: the competition scores "Prefer not to answer" / "Don't know" / "Refused" as ordinary levels, and NA_GATED adds a structural branch on top. An IRTree factorization — P(gated) × P(refuse | asked) × P(substantive answer | responded) — matches the data-generating process exactly and lets each branch borrow strength separately; likely the cleanest way to model the sentinel-augmented option vectors.

---

## 8. Launch addendum (2026-08-17): domains the launch kit makes newly load-bearing

The launch kit re-verification (see [[starter-kit-notes]]) changed not just facts but priorities. Five areas that were peripheral or absent above are now directly load-bearing.

1. **Prediction-powered inference — the official downstream framing.**
   **Angelopoulos, A. N., Bates, S., Fannjiang, C., Jordan, M. I., & Zrnic, T. (2023). "Prediction-Powered Inference." *Science* 382(6671), 669–674.** Link: <https://arxiv.org/abs/2301.09633>. Sequel with strictly better estimators: **PPI++** (<https://arxiv.org/abs/2311.01453>). Classical ancestor: model-assisted survey estimation / GREG (Särndal, Swensson & Wretman 1992, *Model Assisted Survey Sampling*).
   Use model predictions on the whole frame, then use the labeled subsample to measure and subtract the model's error: valid whether the model is good or bad, narrower than interview-only exactly when the model is good. Tutorial part 2 builds this estimator explicitly ("a better skill on the leaderboard is a narrower confidence interval in the field"), and the sample schema's GIVEN block is now framed as *sampling-frame variables* (roster/admin data) against the *expensive interviewed* PREDICT block.
   Relevance: this is what the organizers say the benchmark is *for* — it does not change the scored objective (still per-cell log score), but it is the frame for the 4-page method description, the NeurIPS session, and any "why this matters" argument. It also sharpens the modelling target: the value of skill is monotone in CI width, so calibrated probabilities matter more than argmax accuracy — consistent with everything in §3.

2. **Adaptive data analysis under a noised leaderboard.**
   **Dwork, C., Feldman, V., Hardt, M., Pitassi, T., Reingold, O., & Roth, A. (2015). "The reusable holdout: preserving validity in adaptive data analysis." *Science* 349(6248).** Link: <https://doi.org/10.1126/science.aaa9375>. Companion: **Blum, A., & Hardt, M. (2015). "The Ladder: A Reliable Leaderboard for Machine Learning Competitions."** Link: <https://arxiv.org/abs/1502.04585>.
   Phase 1 is literally this mechanism: a *fixed* DEV set queried by every submission, defended by Laplace ε=10 noise, 0.01 rounding, and a 20-query cap (`privatize()` in `score.py` says so in as many words).
   Relevance: quantifies what a leaderboard query is worth — with skill-scale noise σ≈0.14/ε per query and 20 queries max, the leaderboard can *confirm* a large local improvement but cannot *rank* close variants. Operational consequence (already discipline rule 4): model selection happens entirely on the local harness; leaderboard submissions only validate pipeline health and large, pre-registered deltas.

3. **Cognitive-test norms — real-world priors for the new World Bank items.**
   The launch schema re-classed the *raw* cognitive scores as PREDICT: Digit Span forward/backward maximal length (options "1"–"14") and Corsi block span ("1"–"7"), citing Woods 2011 in the item text itself. **Woods, D. L., et al. (2011). "Improving digit span assessment of short-term verbal memory." *J. Clinical & Experimental Neuropsychology* 33(1), 101–111** (norms: forward ML ≈ 6.8±1.1, backward shorter by ≈1). **Kessels, R. P. C., et al. (2000). "The Corsi Block-Tapping Task: Standardization and Normative Data." *Applied Neuropsychology* 7(4), 252–258** (span ≈ 6.2±1.3 in adults, education-sensitive).
   Relevance: published norm distributions are legitimate offline priors for exactly these option lists — an informed marginal over "1"–"14" (unimodal near 6–7, backward shifted down, adjusted for the youth-jobseeker population) beats both uniform and thin visible counts on long option lists, at zero runtime cost. Same logic applies to the occupation items (SOC-style major groups): occupational distribution priors for young job-seekers exist in ILO/LFS statistics. This is the organizer-sanctioned "world knowledge" lever (`external_model` docstring), and it survives on real data precisely where the sandbox cannot measure it.

4. **The organizer-sanctioned LLM recipe: prior + backoff, not persona-prompting.**
   `baseline/external_model/main.py` is itself the key reference — read it as a design document. The ladder: stratum counts (GIVEN columns chosen by mutual information with the item) → coarser counts → base measure from LLM next-token logits over *option text*, combined as `(counts + ALPHA·coarser)/(total + ALPHA)` with ALPHA in units of respondents.
   Relevance: this reframes §6 — the viable LLM use here is not simulating respondents but supplying a *base measure* worth a fixed number of pseudo-respondents, diluted automatically by real data. It composes with hierarchical shrinkage (§7.1) and calibration (§3), runs in one forward pass per item (fits the whole-run budget), and ships via `models.txt` with no bundling. The organizers' own warning: its value is invisible on the sandbox by construction — judge it on structure (does backoff hurt anywhere?) locally, and on real data only via a deliberate leaderboard submission.

5. **`torch_measure` — the organizer-provided psychometrics library in the runtime image.**
   Stanford AIMS lab, PyPI `torch-measure`: PyTorch-native IRT (Rasch/2PL/3PL, ML + Bayesian estimation), factor models, adaptive testing, reliability/information diagnostics, GPU throughout. Docs: <https://aimslab.stanford.edu/torch_measure/>.
   Relevance: pre-installed, so an IRT component costs nothing in `requirements.txt`. Caveat before relying on it: public docs describe *binary* response matrices; the graded/nominal likelihoods this competition needs (§1.1, §1.2) may need a hand-rolled softmax/GRM head on top of torch anyway. Verify polytomous support against the actual package before designing around it; py-irt (§1.4) remains the fallback.

Also newly relevant, no literature needed: the whole-run budget (900 s covers import + model load + all three instruments) favors **one shared backbone** over three per-instrument models, and makes module-import time a first-class measured quantity in every profile.

---

## Suggested reading order

**First week (foundations the first submissions are built on):**
1. Gneiting & Raftery 2007 (§3.1) + Guo et al. 2017 (§3.2) — internalize the metric first; every later modeling choice is judged by it.
2. Rubin 1976 (§5.1) + the skip-logic/universe material in Groves et al. (§5.3) — settle the NA_GATED-vs-nonresponse preprocessing before any model is trained; this is the brief's "free score."
3. Samejima 1969 (§1.1) + Bock 1972 (§1.2) — the per-item-type likelihoods for the 2PL/GRM starter baseline.
4. Wu et al. VIBO (§1.3) + py-irt (§1.4) — how to actually fit those likelihoods fast, and the amortized-inference pattern for both tracks.
5. Chen & Goodman 1996 (§3.4) — the smoothing/interpolation playbook for the marginal baseline already in the harness.
6. Skim Jäger et al. 2021 (§4.4) and Dominguez-Olmedo et al. (§6.1) now — they set expectations and prevent wasted weeks on deep/LLM detours.

**Later (weeks 2+, in support of model upgrades and the hybrid):**
7. Park, Gelman & Bafumi (§7.1) + Böckenholt IRTrees (§7.5) — the two structural upgrades that match this task's actual shape: partial pooling over demographic × country cells, and tree-factorized handling of gated/nonresponse levels.
8. Niculescu-Mizil & Caruana (§7.3) + TabPFN (§7.4) — the practical per-item conditional baselines; benchmark both against the IRT stack on the sandbox before investing further.
9. Bergner et al. 2012 (§1.5), Davenport et al. (§2.1), Lafond et al. (§2.2), Rendle FM (§7.2) — unify IRT, low-rank completion, and feature-based factorization; pick latent rank by held-out log-loss.
10. Candès & Recht (§2.3), softImpute (§2.4), mice (§2.5), missForest (§2.6) — completion theory background and the classical baselines to beat.
11. Kull et al. 2019 (§3.3), Muraki 1992 (§1.6) — second-order calibration and likelihood refinements once the pipeline is stable.
12. MIWAE (§4.2) then TabDDPM (§4.1), with GAIN (§4.3) as background — only pursue if they beat the calibrated IRT/low-rank stack locally.
11. Area 6 in order 6.1 → 6.2 → 6.3/6.4 → 6.5 → 6.6/6.7 → 6.8, plus Little & Rubin (§5.2) and de Leeuw (§5.4) as reference — the LLM hybrid is a test-phase differentiator, and the recent fine-tuning line (Cao, Suh) defines what a viable version looks like.

**Launch additions (slot in early — see §8):**
13. Angelopoulos et al. PPI (§8.1) — read before drafting any of `docs/method-4p.md`; it is the organizers' own framing of what skill buys.
14. Dwork et al. reusable holdout (§8.2) — before the *first* leaderboard submission; it sets the submission-spending policy.
15. Woods 2011 + Kessels 2000 norms (§8.3) and the `external_model` docstring (§8.4) — before building the World Bank informed-prior component; cheapest expected real-data gains after gate closure.
