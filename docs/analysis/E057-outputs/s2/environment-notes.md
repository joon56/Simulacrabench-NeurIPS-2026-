# E057 S2 environment scope

Public official API queried without credentials on2026-09-25; curated response
in official-rules.json. DEV current, execution900s, one submission/day,
no phase-total cap. Anonymous used-submission counters cannot establish the
authorized account's slot. Account availability remains unknown; no upload date.
API DEV end2026-10-31 00:00UTC; website lists October30. No upload is scheduled.

Sources: https://www.codabench.org/api/competitions/17822/ and
https://simulacrabench.org/ . Local and remote starter-kit main both ee427a9.

API top-level docker_image is python:3.12-slim. Current starter-kit README
describes the submission runtime as Python3.13 with scientific packages
preinstalled; config.yml's local Docker base is python:3.13-slim. The top-level
Codabench image is not independently established as the isolated submitted-code
runtime. Do not silently claim those fields match or that local tests identify
the actual hosted library versions. This environment-metadata discrepancy and
Windows CPU versus H100 differences remain deployment uncertainty, with no
observed contract change requiring a local source rewrite. Before a real upload,
recheck organizer guidance if the runtime contract changes.

Local verification uses the S1-recorded environment without installation or
upgrades: Python3.13.14, numpy2.5.1, pandas3.0.5, sklearn1.9.0, torch2.13.0+cpu.
No requirements/models download needed by this archive. No external respondent
data or weights bundled; SIPP/Adult/TabPFN use belongs to development history,
not a claim of private-survey access or E057 hosted inference dependencies.
