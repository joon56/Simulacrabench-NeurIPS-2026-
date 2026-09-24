# A013 Task2 - E041 method candidate report

Status: candidate draft ready for independent review. No final-model promotion,
submission upload, source-model change, or commit.

## Exact artifacts

- Source: `docs/method-4p.md`
- PDF: `output/pdf/method-4p.pdf`
- Four inspected page images: `output/pdf/method-4p-page-{1,2,3,4}.png`
- E025 byte-preserved fallback: `submissions/phase2-E025-preparation/method-4p-E025.{md,pdf}`
- E041 review copy: `submissions/phase2-E041-preparation/method-4p-E041.{md,pdf}`
- Hashes, page count, type sizes: `submissions/phase2-E041-preparation/method-validation.json`

## Content correspondence

- UNHCR-only dispatch and section grouping, diagonal GIVEN-equality weights,
  fixed top-32 candidate bank, disjoint metric-fit/selection/replay/reference
  partitions, selection rule and retained E025 concentration/replay behavior
  checked against `src/models/supervised_retrieval.py`.
- Historical E025-only loss map separated from unmeasured E041 map. A011
  membership diagnostics and E053's scoped ungated STOP retain limitations.
- A005 synthetic GIVEN-only Bayes reference restored (0.5085 versus 0.5062
  base, unrounded gap about 0.0024), with explicit synthetic-only scope.
  E025 loss-map components now carry the rounded/noised probe-resolution
  qualification (practical UNHCR difference resolution about 0.015-0.03).
  Initial E032 changed all three instruments; E033/E034 changed UNHCR only.
- A012 skills/deltas, 442,425 exact raw-vector parity, ZIP checker and
  367.177-second inclusive local time checked against A012/SCORES.md.
- Adult/TabPFN development resources disclosed; neither is bundled or used
  by E041 inference. Historical second-account reading retained and qualified.
- Public UCI Adult CC BY 4.0, SituatedEvals MIT license and Prior Labs V2
  classifier weight license were checked against their official pages. The
  live Codabench HTML did not expose agreement text to the web reader; clause
  7 wording follows the existing phase2-preparation audit of the API terms.

## Validation

- PDF marker ran successfully exactly once before initial edits; it was not
  rerun for this revision.
- Existing renderer type sizes retained; only footer/title/author metadata
  changed. Four-page render passed. Text-order assertions confirm intended
  section opening on each page; PDF metadata title checked. Every page image
  visually reviewed, with page 4 reinspected after the E032/E033/E034
  correction; no
  clipping, overlap or footer collision.
- E041 source/copy Markdown SHA256:
  `b6346b682f77300b3ed758641047c26e372ff35072da746549bb75a0c388b8d4`.
- E041 PDF/copy SHA256:
  `1e76420052b5d523c46d477d875a54ccb5a49f2812109ec3333dcdae72fb27cd`.
- E025 backup Markdown SHA256:
  `3573c018507c1e7a716ce645fcfcb51b5e680e1bc211b7b13d09798b387c10fb`.
- E025 backup PDF SHA256:
  `6eb5fa7907ef5647aa98c433fed01a3f7273ace7dd05f3d50a293b47b67437bc`.
- E041 copy hashes match source/output; `git diff --check` passed.

Unrelated pre-existing worktree edits were left untouched.
