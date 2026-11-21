# E062 package dependency and execution disclosure

The archive contains only root `main.py` and `NOTICE.txt`. NOTICE is the exact
starter-kit MIT license, with its original copyright/permission/warranty text.
No respondents, labels, schema, cache, fitted weights or reference probabilities
are packaged. No pretrained model, download, API, external weight or external
data path is used by main.py. Learned neural parameters are created in memory
from the frame supplied to predict under the unchanged original policy.

Direct nonstandard imports: numpy2.5.1, pandas3.0.5, torch2.13.0+cpu,
scikit-learn1.9.0, scipy1.18.1, threadpoolctl. Standard-library re is used.
Dependencies use the existing .venv; no install/requirements resolution occurred.
PyArrow25.0.1 belongs to the local scorer/staging environment, not a main.py
import. Threadpool implementation versions/settings are in preflight.json.
The archive has no requirements.txt: these imports require the execution
environment to provide compatible packages; local PASS does not certify every
hosted dependency version.

Four new boundary tests establish byte-preserved E041 prefix, isolated candidate
bindings, ordinal inheritance of the original nominal network, control/WB
dispatch, and no-optimizer forward/RNG parity. Static import inspection finds
no src/scripts import, repository path, sys.path patch, file I/O or network
client in main.py. The official model process imports the actual ZIP extraction
from its extraction directory. Its instrumentation is outside the ZIP and
observes roles/calls while setting CPU numerical/interop threads2; it is not
a model dependency and does not alter the fixed prediction policy. Measured
suite time includes this instrumentation overhead. No observer-free successful
all3 was repeated.

The stock score.py Python driver disables socket access in its model process.
This is a Python-level guard, not proof of native egress blocking. No network or
remote model invocation was requested. Actual output and resource qualification
is limited to the installed Windows CPU environment, GPU unavailable/disabled.
The unchanged model policy selects CUDA when available, with its existing CPU
fallback; no CUDA/H100 runtime, hosted execution, native egress guarantee,
current upload slot/account or remote bytes were verified.

Official CLI uses only the new TRAIN/DEV synthetic staging. The model gets
TRAIN generated items and DEV GIVEN; DEV PREDICT is missing and EXCLUDE removed.
Truth reaches the evaluator only. Exact role/frame/schema and neural-role
checks are recorded separately. This is previously exposed synthetic engineering,
not a fresh independent audit, real WB efficacy test or target16 improvement.
