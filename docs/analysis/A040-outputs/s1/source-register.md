# A040 S1 sources — 2026-10-01

Role: information investigation only. Outcome: **HOLD_SPECIFIC_INPUT**; see
[closeout](closeout.md). No model execution. Entry/read receipt: [entry](entry.json).

## Bounded official source ledger

Twelve distinct official resources, including two failed guessed paths. The cap
is exhausted; no further source investigation in this session. Repeated access
to the same resource/transport retry is identified below, not counted as a new
document. Required existing local research/source/schema reads are listed separately.

Code revision throughout: `0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3`.

| # | Official resource | Access/result and evidence retained |
|---|---|---|
| 1 | [PMLR paper page](https://proceedings.mlr.press/v306/qu26a.html) | Web abstract/metadata read. No PDF or broad literature survey. Supports changed pretrained family; no HSCC effect evidence. |
| 2 | [TabICL repository](https://github.com/soda-inria/tabicl) | Web view and successful text retrieval; `github-root.html`. Embedded currentOid identifies pinned commit. Initial restricted-network transport failed before successful retrieval. |
| 3 | [Official checkpoint metadata](https://huggingface.co/api/models/jingang/TabICL?blobs=true) | Web tool Internal Error, restricted-network failure, then successful text retrieval; `hf-metadata.json`. No weight bytes. |
| 4 | [Guessed classifier path](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src/tabicl/sklearn/classifier.py) | HTTP404; counted. No source obtained. |
| 5 | [Guessed base path](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src/tabicl/sklearn/base.py) | HTTP404; counted. No source obtained. |
| 6 | [Package metadata](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/pyproject.toml) | HTTP200; `pyproject.toml.txt`. Dependencies/Python support; version dynamically sourced, semver not established. |
| 7 | [License](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/LICENSE) | HTTP200; `LICENSE.txt`. BSD3 classifier code; separate forecast notice outside proposed use. |
| 8 | [Official HSCC README](https://raw.githubusercontent.com/SituatedEvals/public/main/README.md) | HTTP200; `hscc-README.md.txt`. Mutable main, saved bytes hashed. Runtime-training wording at171; resources at278–295; offline/bundling at305–325. |
| 9 | [Pinned repository tree](https://api.github.com/repos/soda-inria/tabicl/git/trees/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3?recursive=1) | HTTP200; `github-tree.json`. File metadata only; located `_sklearn` paths. |
| 10 | [Classifier implementation](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src/tabicl/_sklearn/classifier.py) | HTTP200; `classifier.py.txt`. Read loader, fit, cache construction, batched forward, probability alignment/aggregation. |
| 11 | [Base implementation](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src/tabicl/_sklearn/base.py) | HTTP200; `base.py.txt`. Read device/AMP/FA3/inference config and persistence boundaries; not every persistence method audited. |
| 12 | [Preprocessing implementation](https://raw.githubusercontent.com/soda-inria/tabicl/0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src/tabicl/_sklearn/preprocessing.py) | HTTP200; `preprocessing.py.txt`. Read numerical encoder and ensemble fit/transform; not a complete dependency audit. |

`fetch-batch1.json` retains failed URLs and first successful batch. Its failed
entries name attempted destination filenames; the current classifier/base files
come from successful corrected URLs #10/#11. Source/record hashes appear in
[verification](verification.json); file times are acquisition evidence, not
upstream publication dates. Failed network attempts were not model/data downloads.

## Identity and reading limits

- Weight repo `jingang/TabICL`, revision
  `4dcd344ece2c00be9e831fdd35bed57b5ad83e19`; filename
  `tabicl-classifier-v2-20260212.ckpt`; advertised110,368,038bytes.
- Advertised LFS SHA256
  `bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0`.
  This is remote metadata, **not a locally verified checkpoint hash**.
- Metadata declares `bsd-3-clause` independently of the code license. No weight
  deserialization, package resolution, native-class-cap inspection or model import.
- Model transformer/cache internals and `sklearn_utils` were not fetched/read.
  No assertion of all upstream leakage freedom, exact hierarchical operation
  counts, numerical equivalence, or installability follows from wrapper reading.
- README says `config.yml` is authoritative. This session did not fetch a new
  config or competition Terms page, query accounts/slots, or authenticate policy.
  README's offline-training sentence is a concrete unresolved conflict with the
  retained runtime E041 optimizers, not proof that organizers rejected E041.
- README also both describes `models.txt` build-time acquisition and says nothing
  is prefetched. Proposed local bundled checkpoint avoids relying on that ambiguity;
  no claim that `models.txt` has been removed.

## Local evidence actually used

Ordered AGENTS/CLAUDE/status/latest3log/workflow read and S0 identities are recorded
in entry.json. Current workflow r4 SHA256:
`a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642`.
S0's after-state hashes, rather than before-state hashes, identify shared records.

Read E041/E048/E049/E051 experiment records, current submissions/SCORES.md and
E061 post-result scorecard/handoff. Read permitted production source:
`supervised_retrieval`, `link_sharp`, `shared_trunk`, `hh_cap`, `hier_backoff`,
local `logloss`, and the immutable E041 main.py snapshot. No import.
[Local hashes](local-source-hashes.json) and [schema inventory](schema-accounting.json)
identify these inputs. Public JSON schemas only; no survey response data.

Small schema-accounting shell errors (OrderedDictionary property enumeration,
incorrect guessed `wb.json` path) were diagnosed and corrected to PSCustomObject
and actual `world_bank.json`. The final inventory supersedes that incomplete
intermediate record. This was metadata arithmetic, not a model fixture/test.
