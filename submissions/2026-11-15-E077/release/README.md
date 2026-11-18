# Team Odyssey — SimulacraBench / HSCC 2026 test-phase submission

This repository holds the code that team **Odyssey** ran in the test phase of the
NeurIPS 2026 SimulacraBench competition (Humanitarian Survey Completion Competition), and
the two scripts needed to rebuild the uploaded archive. The method is described in the
team's technical report on OpenReview.

Test-phase entry: Codabench submission 1053618, `skill` 0.4790691441
(`skill_unicef` 0.3427149262, `skill_world_bank` 0.2344919185, `skill_unhcr` 0.8600005877).

## What is here

| Path | Content |
|---|---|
| `main.py` | Entry point called by the grader: `predict(frame, schema)`, once per instrument. Seed averaging, tree and TabICL experts, pooling / copy-share / calibration chains and the in-run S/E guard that decides whether a chain is applied. Build constants for this submission are at the top of the file. |
| `e041_core.py` | The base predictor (hierarchical backoff tables, shared-trunk network, soft gate coupling, donor evidence with supervised section metrics on UNHCR). |
| `vendor/` | Unmodified third-party source bundled with the submission: TabICL 2.2.0, einops 0.8.1, tqdm 4.67.1. |
| `weights/` | Place of the TabICL v2 checkpoint (110 MB, not stored in git; see below). |
| `LICENSES/`, `NOTICE.txt` | Licenses and origin of the third-party components. |
| `MANIFEST.sha256` | SHA256 of every file of the uploaded archive, in archive order. |
| `tools/fetch_checkpoint.py` | Downloads and verifies the public checkpoint. |
| `tools/make_zip.py` | Rebuilds the uploaded archive and checks every file against the manifest. |

No competition data are in this repository. The predictor learns only from the visible
rows the grader passes to `predict` at run time; nothing fitted on survey responses is
stored here.

## Rebuild the submission

```
python tools/fetch_checkpoint.py        # TabICL v2 checkpoint from Hugging Face, SHA256-checked
python tools/make_zip.py submission.zip # same files as the uploaded archive
```

The uploaded archive has SHA256
`7ebb1972e327adc57947a977baa188036ee28c6fd30bb860a357ed2a6cd62ac8`. `make_zip.py` verifies
each file against `MANIFEST.sha256`; the archive bytes are identical when the local zlib
compresses the same way, and the script says which case applies.

## Run it

The archive runs in the organizers' environment without a `requirements.txt` and without
network access (Python 3.13 image with numpy, pandas, scipy, scikit-learn and torch
pre-installed; one H100; 3600 s in the test phase). To score it with the official starter
kit (<https://github.com/SituatedEvals/public>) on the kit's synthetic sandbox:

```
python make_sandbox.py --schema data/unhcr.json --out _sandbox/unhcr
python score.py --submission /path/to/this/repository --data _sandbox/unhcr --schema data/unhcr.json --phase 2
```

A CUDA device is required (the TabICL expert and the base network run on GPU). On one
RTX 3070 the three instruments take about 1,120 s in phase 2 on the synthetic sandbox.
The sandbox has the real shape but invented answers, so its scores say nothing about the
real instruments; reproducing the test-phase score requires the organizers' data.

## Determinism

Seeds are fixed in the code (network seeds, the S/E/F split, tree fitting). Results are
repeatable up to GPU floating-point noise (differences of about 1e-7 in single
probabilities were observed between two runs of the same archive).

## License

Team code (`main.py`, `e041_core.py`, `tools/`): BSD 3-Clause, see `LICENSE`.
Third-party components keep their licenses: TabICL source and checkpoint (BSD 3-Clause),
einops (MIT), tqdm (MPL-2.0 and MIT), starter-kit material (MIT); see `NOTICE.txt`.
