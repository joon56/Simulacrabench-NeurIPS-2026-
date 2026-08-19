# Method description (4-page) — template

> Required with the phase-2 submission (per competition terms on
> Codabench). Keep to 4 pages when rendered. Fill sections as the final
> model solidifies; keep numbers in sync with docs/log.md and submissions/.

## 1. Problem framing

- Task: probability distributions over answer options for every PREDICT cell
  of held-out respondents, three instruments, scored by skill
  (1 + log_score/U, plain mean across instruments).
- What we optimize: held-out log-loss on locally built sandboxes/splits;
  calibration over sharpness.

## 2. Preprocessing and skip logic

- Schema-driven option vectors (values + NA_GATED slot for gated items);
  option order from schema, never from data.
- Gate handling: coupling P(child = NA_GATED) = 1 − P(parent ∈ observed_if);
  chain closure; softened toward observed sentinel rates where gates are
  approximate (unhcr: schema-documented agreement median 0.83).
  [Describe exact implementation.]
- Treatment of nonresponse levels ("Prefer not to answer", "Don't know") as
  ordinary levels. [IRTree factorization if used.]

## 3. Model

[Architecture: per-item conditionals / latent-factor (IRT/FM) / hierarchical
pooling over GIVEN cells. One paragraph per component; state what each adds
in held-out skill.]

## 4. Calibration

[Smoothing/interpolation weights, temperature or Dirichlet calibration,
where fitted and on what held-out cells. Show reliability evidence.]

## 5. Training and compute budget

- Fitted state loaded at module import; `predict()` runs on the delivered
  frame only (no external state, no network).
- Wall-clock per instrument (measured on sandbox, hardware): [table].
  Phase-2 limit 3600 s for the whole run — import + all three instruments.
- Dependencies (pinned, beyond the hosted image's pre-installs): [list].
  External models: [models.txt HF repo ids and/or bundled artifacts, or
  "none"]; external resources disclosed per FAQ.

## 6. Results

| Model variant | sample | unicef | world_bank | unhcr | mean skill |
|---|---|---|---|---|---|
| crowd marginal (reference) | | | | | |
| [variant] | | | | | |

Local-vs-leaderboard agreement: [expected vs observed on phase-1
submissions, from submissions/README.md log.]

## 7. Reproducibility

- Repo layout, seed policy, one-command rerun of the local evaluation.
- License note [verify exact obligations against the Codabench terms the
  team accepted at registration].
