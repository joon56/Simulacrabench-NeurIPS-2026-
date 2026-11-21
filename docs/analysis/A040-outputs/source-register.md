# A040 S0 primary-source leads — checked 2026-10-01

1. [Official ICML2026 paper page](https://proceedings.mlr.press/v306/qu26a.html).
   S0 read the abstract, not the full paper. Authors report classification and
   regression benchmarks and changed pretraining/architecture. No HSCC comparison.
2. [Official repository](https://github.com/soda-inria/tabicl).
   S0 read README material. It documents the v2 classification checkpoint,
   classifier API, local model path/automatic-download controls and caching.
   These establish investigation leads, not tested offline compatibility or
   whole-HSCC runtime. Main is mutable; S1 must pin the reviewed revision.
3. [Author model repository](https://huggingface.co/jingang/TabICL).
   Landing/model-card metadata only; no binary weights downloaded or loaded.
   Exact artifact identity, current code/weight terms and dependencies remain
   part of the S1 contract review.

The author/research-organization repository is the canonical lead, not a mirror
or replication found in search. S0 downloaded no model, paper corpus or dataset.
No private platform/data access. Public browsing is limited strategy/source
selection; it is not the deeper S1 implementation-contract investigation.

Local evidence: the exact document paths and SHA256 are in s0-entry.json.
Old experiment statements about unavailable hosted components are reconciled
against submissions/SCORES.md. No saved arrays/cache or protected responses read.
