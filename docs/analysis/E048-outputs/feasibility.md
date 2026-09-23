# E048 TabPFN V2 feasibility (2026-09-23)

Status: source/metadata feasibility PASS with modern package and explicitly selected original V2 checkpoint. Runtime import, numerical inference, memory, and 900-second budget remain UNTESTED by this read-only subtask. No packages installed or production files changed.

## Package decision

Use `tabpfn==8.0.8` and `tabpfn-common-utils==0.2.23`. Both have pure-Python wheels. TabPFN requires Python >=3.10 and explicitly lists Python 3.13. Its requirements accept installed metadata torch 2.13.0+cpu, sklearn 1.9.0, pandas 3.0.5, scipy 1.18.1, and typing_extensions 4.16.0. This is metadata compatibility, not a completed runtime test. [Official release metadata](https://pypi.org/pypi/tabpfn/8.0.8/json), [common-utils metadata](https://pypi.org/pypi/tabpfn-common-utils/0.2.23/json).

TabPFN 8.0.8 direct non-extra requirements, verbatim constraints:

```text
torch>=2.5
safetensors>=0.4.0
numpy>=1.21.6
scikit-learn>=1.2.0
typing_extensions>=4.12.0
scipy>=1.11.1
pandas>=1.4.0
einops>=0.4.0
huggingface-hub>=0.23.0
pydantic>=2.8.0
pydantic-settings>=2.10.1
joblib>=1.2.0
tqdm>=4.66.0
tabpfn-common-utils[telemetry-interactive]>=0.2.13
filelock>=3.11.0
lightgbm>=3.0
mlx>=0.29.3; sys_platform == "darwin" and platform_machine == "arm64"
```

common-utils 0.2.23 requires filelock>=3.19.1, numpy>=1.21.6, nvidia-ml-py>=13.590.48, pandas>=1.4.0, platformdirs>=4, posthog>=6.7, requests>=2.32.5, scikit-learn>=1.2.0, typing-extensions>=4.12. Parent should freeze resolved missing packages after installation; this report does not claim a fully tested dependency lock.

Rejected pins: 2.0.9 and 2.1.3 require sklearn<1.7 and pandas<3. Also avoid common-utils 0.2.13: it requires pandas<3. 2.0.9 reloads weights in every fit and has no model-spec object path; 2.1.3 adds model-spec objects but retains dependency conflicts. [2.0.9 metadata](https://pypi.org/pypi/tabpfn/2.0.9/json), [2.1.3 metadata](https://pypi.org/pypi/tabpfn/2.1.3/json).

## Exact pretrained artifact

- Repository: `Prior-Labs/TabPFN-v2-clf`.
- File: `tabpfn-v2-classifier.ckpt` (original V2 classifier).
- Exact size: 29,016,968 bytes, from public Git LFS pointer.
- SHA256: `f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f`.
- [Public checkpoint download](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/resolve/main/tabpfn-v2-classifier.ckpt), [pointer](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/raw/main/tabpfn-v2-classifier.ckpt), [file metadata](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/blob/main/tabpfn-v2-classifier.ckpt).
- Current model license: [Prior Labs 1.1](https://huggingface.co/Prior-Labs/TabPFN-v2-clf/raw/main/LICENSE.txt). Preserve license and required attribution in distributed artifact. Parent already verified naming/attribution obligations; this report adds no legal interpretation.

WARNING: 8.0.8 default constructor selects V3. Even `create_default_for_version(ModelVersion.V2)` chooses `tabpfn-v2-classifier-finetuned-zk73skhh.ckpt` by default. Explicitly override with original checkpoint/specs below.

## Import-time, offline API (source-verified; not executed)

```python
import os
from pathlib import Path

# Must precede tabpfn imports. Verified in common-utils 0.2.23 source.
os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

from tabpfn import TabPFNClassifier
from tabpfn.base import ClassifierModelSpecs
from tabpfn.constants import ModelVersion
from tabpfn.model_loading import load_model_criterion_config

CHECKPOINT = Path(__file__).resolve().parent / "tabpfn-v2-classifier.ckpt"
MODELS, CRITERION, CONFIGS, INFERENCE_CONFIG = load_model_criterion_config(
    model_path=CHECKPOINT,
    check_bar_distribution_criterion=False,
    cache_trainset_representation=False,
    which="classifier",
    version="v2",
    download_if_not_exists=False,
)
V2_SPEC = ClassifierModelSpecs(MODELS[0], CONFIGS[0], INFERENCE_CONFIG)

# Construct sequential per-item estimators from this already-loaded spec.
classifier = TabPFNClassifier.create_default_for_version(
    ModelVersion.V2,
    model_path=V2_SPEC,
    n_estimators=1,
    device="cpu",
    fit_mode="fit_preprocessors",
    n_jobs=1,
    random_state=42,
)
```

`initialize_tabpfn_model` has an explicit `ClassifierModelSpecs` branch: returns model/config objects without disk or download. `load_model_criterion_config(... download_if_not_exists=False)` raises if checkpoint missing. Plain classifier construction alone does not load weights. Shared model object implies sequential fits/predictions; do not run overlapping item estimators against it without validating mutation behavior.

Reference count 512 satisfies CPU <=1000 guard (warning begins above 200). V2 config limits classes to 10; schema K must include gated sentinel. Runtime fitting may observe fewer classes, so map `classes_` back to complete schema order. No score, transfer, or speed claim follows from compatibility.

## Evidence and remaining checks

Official wheels downloaded and extracted solely under `tmp/e048-feasibility/`; no installation. 8.0.8 wheel SHA256: `b6c945c8bf23b86f595697fcfa4ce58d84105441baf7e1313edc7865d7d29658`.

Relevant extracted source: `wheel808/tabpfn/classifier.py` (V2 factory ~527; model spec accepted ~223), `base.py` (spec ~57; no-load branch ~134), `model_loading.py` (offline loader ~608), `inference_config.py` (10-class V2 limit ~309), `validation.py` (CPU guard ~280). Telemetry switch: `common-latest/tabpfn_common_utils/telemetry/core/service.py` ~84.

Next required evidence: install without downgrading baseline dependencies; hash verified checkpoint; block sockets during import/fit/predict smoke test; verify 512-reference fit with 1 estimator; then bounded timing and official grading. Current sandbox Python process launch failed through normal permissions although package metadata was readable; parent reports escalated execution works.
