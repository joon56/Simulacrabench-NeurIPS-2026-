# E056 pre-fit review

Registration commit: 18ab9e6. Input S0: 4166130; later A017 documentation
commit 0557615 is unrelated to this experiment. User edits and A018 files
are excluded from E056 commits. A018 release verification is a separate
session; wait for its active fit to finish before the six small tree fits.

No new model score accessed. Label-free cache validation passed: source/code
hashes, all role positions, masked-frame pickle hash, capture hash, original
endpoint parity flag and all6078 non-fit rows covered. Original group counts:
5922 fit,1866 calibration,1872 oracle,1148 selection,1192 audit. SSUID role
overlap zero. Sample SHA256
fe456797e61f7c074a84bfaa7171c0ba7e0fb86cdd089ba716f8dfd0c0b13d6c.
Masked frame SHA256
7445cef0df2f713183b5e980204096771339d25660951c50c40fe3c9bc53075f.
Therefore reuse actual generic E041, zero new E041 fits.

Nine E056 synthetic tests plus ten reused A014/E055 tests PASS (5.78s).
RED first failed because screen_e056 did not exist. Tests cover official
floor source, independent729-way maximum, unequal-cluster SE and bootstrap,
masking, asked-fit guards, class ordering, identity, parent and mass preservation.
Self-review corrected audit scoring before execution to score only frozen
selected predictions and comparator; no unused audit-arm comparison.

Installed Python3.13.14/numpy2.5.1/pandas3.0.5/sklearn1.9.0. psutil absent;
no installation or environment change. Native Windows process enumeration/RSS
preflight passed at319135744bytes. Fits use two numerical threads, no GPU;
native monitor measures worker+descendants and enforces8GiB/1200fit seconds.
Worker stage caps supplement the root's cumulative90-minute research clock.

Source review: only schema GIVEN features enter trees; fit/non-fit target
masking verified first. Gate truth only selects training rows. All candidate
arrays and hashes are frozen before evaluation label mapping; role-open markers
forbid re-access. Oracle family is additive across six leaves, parent fixed.
One-SE guard is operational, not a significance claim. SIPP evidence has no
automatic humanitarian transfer. No independent reviewer or target gain claimed.

Reproduction after this reviewed code commit:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_e056_conditional_content.py tests/test_e055_star.py tests/test_a014_sipp.py -q
.venv/Scripts/python.exe scripts/screen_e056.py library
.venv/Scripts/python.exe scripts/screen_e056.py oracle
# Only on oracle PASS:
.venv/Scripts/python.exe scripts/screen_e056.py selection
# Only when selection has a nonzero share:
.venv/Scripts/python.exe scripts/screen_e056.py audit
```

Commands refuse existing artifacts; preserve completed outputs, never delete
them to force a second score exposure. Local restricted data/cache required.
