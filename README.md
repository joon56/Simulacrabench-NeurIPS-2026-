# SimulacraBench / HSCC

Humanitarian Survey Completion Competition research workspace.
Current decisions live in [docs/status.md](docs/status.md); historical outcomes
and exposure boundaries must survive changes of agent or chat.

- **Codex entry:** [AGENTS.md](AGENTS.md).
- **Shared project rules:** [CLAUDE.md](CLAUDE.md).
- **Session roles and boundaries:** [workflow](docs/workflow.md).
- **Copy-ready session prompts:** [Korean templates](docs/session-prompts.ko.md).
- **Windows/Codex setup, checks and folder map:** [setup guide](docs/codex-setup.ko.md).
- **Research references and records:** [documentation index](docs/index.md).

Start with CLAUDE.md, status, the newest three log entries, then workflow and
the task's handoff. Setup/check instructions are not permission to run research,
recreate a dataset, package a submission, commit or push.

For a wiring/environment-metadata check from the repository root in PowerShell:

```powershell
& .\.venv\Scripts\python.exe -B scripts/check_workspace.py
```

This reads a fixed list of operating documents and installed package metadata.
It does not import models, collect research tests or read response data. A PASS
does not prove that another chat loaded the instructions or that a model runs.

## Outcome (2026-11-21)

Team Odyssey, NeurIPS 2026 SimulacraBench: final rank 47, test-phase skill 0.4791 (UNICEF 0.3427,
World Bank 0.2345, UNHCR 0.8600).

- Submitted code, byte for byte, with rebuild scripts:
  [submissions/2026-11-15-E077/release](submissions/2026-11-15-E077/release) (BSD 3-Clause).
- Technical report: [docs/writeup/report.pdf](docs/writeup/report.pdf).
- What was tried and what each attempt read: [experiment tree](docs/tree.md),
  [experiments](docs/experiments), [log](docs/log.md).
- Files that are not in this repository and why:
  [docs/analysis/not-in-repository.md](docs/analysis/not-in-repository.md).

No competition data are in this repository.
