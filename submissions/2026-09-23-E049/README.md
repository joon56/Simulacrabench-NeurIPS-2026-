# TabPFN-HSCC E049

Built with PriorLabs-TabPFN.

Exploratory UNHCR-only adaptive gate-parent challenger over immutable E041.
The ZIP contains main.py, exact requirements, the original public V2 checkpoint,
its license and attribution. Use the ZIP at ../2026-09-23-E049.zip.

See SCORES.md for preregistered interpretation arms and measured validation.
verification.json binds completed checks to exact artifact hashes. Official
all3/checker/raw assembly parity PASS; 29 tests pass. Official offline runtime
639.517s; conservative forced-active all3 profile 753.797s, both <900s.
Clean and household outputs equal E041; no local gain or .65 forecast claimed.
E041 remains the DEV incumbent; E025 remains the validated phase2 fallback.
No competition upload is performed by the preparation workflow.

Rebuild with `tmp/e049-env/Scripts/python scripts/assemble_e049.py` after
installing the pinned dependencies. Source weights used in this session are
under tmp/e048-model; the monolithic archive loads its bundled checkpoint.
Local validation constraints preserve the existing CPU baseline versions;
they are not extra hosted requirements. The official grader independently
installs the packaged requirements into its own local validation environments.
For a fresh source checkout, copy this folder's checkpoint to
tmp/e048-model/tabpfn-v2-classifier.ckpt; its SHA256 is asserted on import.
The shipped ZIP is self-contained and does not use that source-only path.
