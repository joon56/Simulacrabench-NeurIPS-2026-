# CLAUDE.md — SimulacraBench / HSCC (NeurIPS 2026 Competition)

Working folder for SimulacraBench, officially the Humanitarian Survey Completion Competition (HSCC). Original briefing: `SIMULACRABENCH.md` (Korean, partially outdated — this file wins on conflicts). Official site: <https://simulacrabench.org> · Starter kit: <https://github.com/SituatedEvals/public> (cloned at `external/starter-kit/`, gitignored) · Leaderboard: <https://www.codabench.org/competitions/17822/> · Terms/forum: Codabench org 4076 · Contact: team@simulacrabench.org. (Pre-launch URLs situatedevals.org and the `notebooks` repo are dead.)

## Session entry and workflow (adopted 2026-09-25)

Read this file, `docs/status.md`, then the newest three `docs/log.md` entries,
in that order. Follow `docs/workflow.md` for the user-adopted research process;
copy-ready session prompts are in `docs/session-prompts.ko.md`. Existing user
authorization persists. Distinguish technical qualification, release performance
checks, DEV exploration and final TEST selection. These prospective clarifications
do not rewrite any earlier preregistration, STOP or hosted result.

Codex repository entry is `AGENTS.md`. Regardless of entry route, complete the
workflow read receipt defined in `docs/workflow.md` before substantive work.
On resuming after an instruction revision, reread the current files rather than
assuming an existing chat automatically received the change.

Role clarification adopted 2026-09-27: `docs/workflow.md` is the persistent
session-role and research-entry contract; prompt templates implement it rather
than redefine it. The user's current explicit scope overrides repository defaults.
Every session states its role, task type, permitted operations and stop condition
before work. S0 owns strategy, records and handoff; it does not automatically run
S1 experiments or S2 packaging. A request to make progress or work toward a
submission does not by itself change an established S0 role. Follow an explicit
user role/scope change without asking again; otherwise prepare the next handoff.
Information acquisition, technical validation, confirmatory research and bounded
DEV exploration have different entry requirements; use the workflow's table.
Do not repeat a HOLD review without new input: define a bounded acquisition task
if feasible, or record the unavailable input and concrete resumption trigger.

Role enforcement revision 2026-09-27-r4: the operating S0 chat stays S0 until
the user explicitly directs this chat to execute another role or a named bounded
exception. "Obtain all resumption inputs", "start work" and "try experiments"
alone describe pipeline goals, not parent-S0 execution authority. Under r7, hand
bounded authorized work to the assigned S1/S2 child; separate chats are optional.
An assistant's role declaration
or generated prompt cannot authorize itself. Record the actual user instruction
before a transition; do not retroactively call an inferred transition explicit.
User-authorized S0 platform/document research and workflow edits stay within that
named scope; they do not authorize scientific implementation or packaging.

Current workflow revision **2026-10-26-r7** adds user-authorized delegated operation
under [A045](docs/analysis/A045-outputs/decision.md). S0 assigns bounded child tasks
and reviews artifacts; the user need not copy handoffs between chats. Delegation
authorization does not supply undefined scientific/data/budget permission.
The parent remains document/coordinator-only. Root alone dispatches; children do
not redelegate. Root and reviewers cannot write while an executor owns this
checkout. Use the current epoch/task ID and explicit release, not a stale prompt
or the same old receipt. These records coordinate agents, not an atomic lock.
No indefinite background/new-day execution is promised. See workflow r7 for the
active-run, ownership and escalation contract.

The r6 foundation retains user-approved execution batches.
S0 decides candidate/batch/budget/reading arms and reviews results; it remains
document-only. An assigned executor child or separate session may perform the named S1 and conditional S2
stages in order when the user's batch instruction prospectively authorizes the
transition. Record the gate, source identity and remaining aggregate budget; do
not require another handoff for that preauthorized transition. Never replay a
completed successful S1 merely because the session changed. S3 preparation and
comparison use a separate approved scope; A018's historical selected wording is
not the user's final TEST decision. Only one checkout writer at a time; explicit
ownership/job handover is required. New hypotheses, data, budgets or scientific
criteria outside the batch return to S0. No automatic upload, paid resources or
commit/push follow from a batch label. Child launch follows the current user's
delegated-operation authority, not merely the batch label.

Repair autonomy from r5 remains. The owning session diagnoses and repairs ordinary implementation
errors, verifies the affected boundary, and continues within its existing task and
aggregate budget. Do not require a new S0 review for each small defect. Preserve
failed records and scientific/data policy; escalate changed scope, authority,
exhausted allowance or unresolved remote side effects. See workflow.md for exact
rules. Existing chats reread current instructions before applying the change.

## Task summary (per official starter kit README)

**2026-11-08 official refresh (supersedes the 10-22 dates and the 1/day limit below):**
DEV closes 2026-11-14 12:00 UTC (21:00 KST); Final 2026-11-15 12:00 UTC to 11-20
12:00 UTC (21:00 KST each); DEV 3 submissions/day, Final 1 successful submission,
failed submissions do not count; Final scored exact (no noise/rounding); skill now
normalized by the crowd-marginal reference (kit aa03186, 10-26), so leaderboard values
before/after 10-26 are on different scales; every team owes a 4-page OpenReview
writeup plus code URL/license by 11-20 10:59 UTC. Sprint mode A047 is active.
See [A047 rules snapshot](docs/analysis/A047-sprint/rules-2026-11-08.md).

**2026-10-22 current-rule caution:** the official website and online config now
list DEV through November 13 and Final November 14–18, replacing the historical
dates below/in A018. Exact platform timestamps and current Terms were not obtained
in this S0 web read. Current kit/schema/scorer compatibility is not certified by
old local passes. See [A044 rules snapshot](docs/analysis/A044-outputs/official-rules-snapshot.md)
and the separately approved S3 preparation handoff. Do not execute historical
window-day commands or treat past method/license proposals as current authority.

Three unpublished survey instruments (post-launch schema update 2026-08-19): UNICEF v1.1 "Faith & Immunisation" 19 items / 12 scored / 8 gated (19,846 rows, 10 countries); World Bank "Skills Assessment" 106 / 76 scored / 40 gated (6,927 rows, 3 countries, youth job-seekers); UNHCR ERPIS v1.3 285 / 213 scored / 156 gated (10,349 rows — Syrian refugees in Egypt/Iraq/Jordan/Lebanon, 2 CATI rounds treated as independent cross-sections). Schema `description` fields now carry real instrument metadata — read them, they are modelling input. Visible respondents arrive complete; **held-out respondents show only their `GIVEN` block — every `PREDICT` cell is blank and scored** (cross-respondent generalization; there are no separate Track A/B).

- Item classes: `GIVEN` (visible, never scored), `PREDICT` (held out, scored), `EXCLUDE` (never shown, stays in schema — filter on `class`, don't assume columns line up).
- **Respondent roles, fixed at dataset build:** one `respondents.parquet` with a `role` column ∈ {`TRAIN`, `DEV`, `TEST`} (renamed from FINAL), counts published in `schema["split"]`: unicef 14,885/1,488/3,473 · world_bank 5,195/520/1,212 · unhcr 8,279/621/1,449. **Nothing is subsampled** (`data_fraction` removed): phase 1 = all TRAIN visible, all DEV scored (exact scored cells: unicef 17,856 · wb 39,520 · unhcr 132,273); phase 2 = TRAIN+DEV visible, TEST scored. TEST rows not shipped in phase 1. Scored set fixed within a phase → leaderboard entries directly comparable.
- **Gates are approximate on real UNHCR data**: schema states gate-vs-data agreement has median 0.83, range 0.29–0.98; the three s3_11 return-intention branches overlap in the file; five multi-select families mark the sentinel in round 2 only; five gates approximate conditions the one-parent format can't express (the `GATE_CORRECTIONS.md` reference was removed from the schema 2026-09-01; organizer email 2026-09-02: "<5 gating changes" to unhcr still unshipped — re-run the full harness when a kit update lands). **Hard gate coupling (P=1) is unsafe on unhcr — soften toward observed sentinel rates.** Sandbox gates remain exact, so this failure mode is invisible locally.
- **`NaN` means exactly one thing: held out, predict it.** Genuine non-response ("Prefer not to answer", "Refused") is an ordinary level.
- **Gated items get one extra final slot for `schema["gated_value"]` (`NA_GATED`)** — "never asked" is a real scored answer. Predicting who gets skipped is worth as much as predicting what they say. Option order comes from the schema, never from the data.

## Metric (leaderboard = skill)

- Per cell: log(p) of the realized answer, averaged over all blank cells (pooled, not per-item).
- **`skill = 1 + log_score / U`**, U = mean over scored items of log K (K includes gate sentinel; schema-only). 0 = uniform guess, 1 = perfect. Leaderboard = plain mean of the three instruments' skills.
- Vectors are renormalized and mixed with a flat vector so no probability falls below `scoring.floor` = 1e-3 — no need to floor your own numbers, but a confidently wrong cell still costs log(1e-3). Hedge where evidence is thin.
- **Phase-1 scores are noised** (Laplace, ε=10, rounded to 0.01). Leaderboard shows per-instrument skill and the mean, but never per-item detail. Local harness is the only precise signal.

## Submission constraints

- Zip (≤ 1 GB, no zip-inside-zip, no folder wrapping) with `main.py` **at the archive root**; build with `cd my_submission && zip -r ../sub.zip .`. Validate the archive with `python tools/check_submission_zip.py sub.zip` before spending a submission.
- `requirements.txt` is **optional** — the hosted image (Python 3.13) pre-installs numpy, pandas, pyarrow, scipy, scikit-learn, torch, torchvision, Pillow, transformers, sentence-transformers, tokenizers, sentencepiece, tiktoken, huggingface_hub, accelerate, safetensors, bitsandbytes, autoawq, protobuf, and `torch_measure` (organizer IRT/latent-trait lib). Only declare what the image lacks, **pinned exact versions** (unpinned → `HSCC-BUILD-002`). Installed at image build, off the clock.
- **HF models via `models.txt`** (one repo id per line, e.g. `Qwen/Qwen2.5-1.5B-Instruct`): downloaded into the image cache at build time, `from_pretrained()` finds them offline. Other fitted artifacts (`.pt`, `.safetensors`, `.joblib`, …) must be bundled in the zip and loaded from a local path. FAQ: disclose external models/data used.
- `predict(frame, schema)` is called **once per instrument**, returns one probability vector per blank cell — rows top-to-bottom, items in `schema["items"]` key order (not `frame.columns` order), each vector finite, non-negative, sum > 0 (grader renormalizes+floors). Load weights at **module import**, not inside `predict()`.
- Network removed before import; no downloads at runtime (`HSCC-NETWORK-*` / `HSCC-HF-CACHE`).
- Compute: **1× H100, 16 GB RAM (hard limit), 8 CPUs. Phase 1: 900 s; Phase 2: 3600 s — the budget covers the whole run: import + model load + all three instruments together, NOT per instrument.** Same `predict()` must PASS all three schemas.
- Phase 1: **1 leaderboard submission/day — the 20-total cap was removed 2026-08-18** (config.yml commit "Removed max per participant submission number"; Codabench shows 1/day only). Phase 2: single final submission + 4-page method description (`docs/method-4p.md`). Submissions stay disciplined regardless: local-harness verification first, preregistered readings and actual outcomes logged.
- Failures come back as sanitized `HSCC-*` codes only — no stdout, no tracebacks (exception *type* survives, message dropped). Debug locally; the platform will not tell you more.
- Data exfiltration / re-identification attempts = disqualification (contractual, third-party enforceable).

## Local pipeline (verified end-to-end)

```
# from external/starter-kit/
python make_sandbox.py --schema data/sample.json --out _sandbox/sample   # writes respondents.parquet + schema.json
python score.py --submission baseline/marginal_counts --data _sandbox/sample --schema data/sample.json --phase 1
python tools/check_submission_zip.py sub.zip                             # archive contract, says nothing about score
```

Fast iteration: `src/eval/runner.py` scores any `predict()` in-process on all four sandboxes with exact (un-noised) skill, using the kit's own scoring functions.

Sandbox has the real shape (same columns/options/skip logic/roles) but invented marginals: **a model tuned to sandbox content will not transfer; a pipeline debugged against it will.** Since launch, `sandbox.trait_scale` = 2.0 (was 0.6 in the draft) — respondent-level dependence is now strong enough locally to test conditional models, not just column-marginal ones. An LLM world-knowledge prior is *by construction* useless on the sandbox (answers are random) — don't read a sandbox non-gain as the prior failing (organizers' own warning in `baseline/external_model`).

## Key dates (2026)

- **Launched (Codabench live 2026-08-19, site says launch Aug 18). Registered — auto-approve.**
- Current public schedule observed 2026-10-22: DEV through **Nov13**, Final **Nov14–18**,
  single Final submission. Exact platform timestamps/current Terms remain unverified;
  see A044. The former Oct30/31 DEV and Nov1–14 TEST schedule is historical.
- Dec: NeurIPS Sydney session. Top-3 = proceedings co-authorship. New: **"Roots of the Data Prize"** for top teams based in the 14 data-collection countries (not us).
- Codabench leaderboard columns: Grand Prize (mean skill) + per-instrument UNICEF / World Bank / UNHCR.

**Verification history:** launch kit audited 2026-08-17; post-launch kit update pulled 2026-08-19 (8 commits: FINAL→TEST rename, split counts, cap removal, real instrument metadata in schema descriptions, unhcr/wb gating rework, disjunctional-gating documentation). Baselines three: `marginal_counts`, `bundled_artifact` (bundled-CSV prior shape), `external_model` (HF LLM prior via `models.txt` + gate recursion + Dirichlet backoff).

## Folder structure (keep to this)

```
data/            # schema + synthetic sandbox only (real data never leaves closed environment)
notebooks/       # EDA, item-type analysis
src/preprocess/  # encoding, skip-logic handling
src/models/      # irt / lowrank / diffusion / hybrid
src/eval/        # local log-loss harness (reproduces official metric)
submissions/     # dated submission snapshots + leaderboard score log
docker/          # submission image definitions
docs/            # method-4p.md, log.md (daily experiment log)
docs/analysis/   # A-series process records (EDA, domain research): append-only attempt logs, every method/version/dead end — see TEMPLATE.md there
```

## Operating discipline (how every modelling decision is made)

1. **No claim without evidence of the stated scope.** Quantify improvement claims with held-out results on an identified channel or actual hosted readings; state uncertainty and transfer limits. Committing research code or a technically qualified exploratory candidate is not model adoption and does not require claiming an improvement. Local qualification, DEV incumbent selection and final TEST selection are separate decisions.
2. **Structure before parameters.** Exhaust deterministic structure (skip-logic gate coupling, chain closure) before adding learned components — the organizers measured gating alone at 0.98 → 0.76 log score.
3. **Overconfidence is the cardinal sin.** A confident wrong cell costs log(1e-3) ≈ −6.9 nats vs ≈ −1.4 for an honest hedge. When uncertain, shrink toward the marginal; check calibration before any submission.
4. **Submissions are ammunition** — 1/day (total cap removed 2026-08-18, but the noised leaderboard still can't rank close variants). Never spend a submission on unverified changes; preregister result-reading arms and next actions before submitting, then compare the actual result. A numerical expectation requires evidence; otherwise explicitly leave it unknown.
5. **Complexity must pay rent.** Compare each candidate with the calibrated incumbent, report measured gain and generalization limits, and profile the whole run. Local qualification follows its registered criterion; a qualified exploratory DEV test can proceed without a positive proxy result. A favorable DEV reading does not automatically select the final TEST model.
6. **Everything is logged** — hypothesis → result → conclusion in docs/log.md. An unreproducible experiment didn't happen.
7. **Every empirical conclusion is validated against background domain.** Two domain types, tracked separately: *technical* (methods — which technique, how implemented) and *background* (what the data means — populations, instruments, humanitarian context; independent of AI/statistics). An EDA finding or measured gain becomes a claim only after checking consistency with background domain knowledge (docs/domain.md, published survey reports). A finding that contradicts domain expectations is flagged — neither auto-rejected nor built upon as-is. Domain surprise raises the evidence bar, it does not veto: check for artifacts (leakage, coding error, confound) and replicate (different seed/split/instrument slice) before adopting; if it survives, consider adoption under the registered criteria and log it as a potential genuine discovery (surprising-but-real correlations exist — domain consensus can be wrong). Numbers-only correlation chains without this check produce contradictory hypotheses (lesson from prior work). Experiment files carry a "Domain check" section: expectation pre-registered before the run, verdict after.
8. **Keep stop decisions scoped.** Use an informative, validly scoped oracle before estimator construction. A failed registered gate stops that study, not all target-domain approaches. If a proxy cannot answer the mechanism, state why and preregister a distinct bounded exploration with all submission checks; never lower a failed study's threshold or search favorable seeds after the result. The user permits qualified, decision-relevant exploratory DEV submissions without local adoption.
9. **Bound work and preserve continuity.** Name the decision, main task, ready backup and resource cap before costly work. Continue authorized work within that scope, then hand off exact artifacts, evaluation exposure and running-job state. Use one integration owner per checkout; independent subagents may review or own disjoint tasks, but must not race edits, fits or commits. The user controls hosted uploads unless explicitly authorizing one.

Disjoint paths or branch names within this shared checkout do not permit simultaneous
writers. Root serializes every assigned writer, including its own document changes.

## Experiment tree (how approaches are recorded)

- **One experiment = one file** in `docs/experiments/E0XX-slug.md` (copy `TEMPLATE.md`): `parent:` header is the tree edge (which model it branches from), `status:` ∈ adopted / rejected / parked / superseded-by:E0YY. `docs/log.md` stays a daily journal and refers to experiments by ID.
- **Rejected model code is never deleted** — only its status changes. Approaches get revived and combined; deleting code falsifies the tree.
- **Commit messages carry the experiment ID** (`E003: given-stratum backoff`) so git history maps onto the tree.
- **Register the decision criterion before scoring.** The historical local default is Δ(3-instrument mean, sample excluded) > +0.005, motivated by old sandbox split-score SD about .0016 on 2026-08-12. It is an operational bar, not a universal significance level, paired-difference interval or external-proxy/TEST futility bound. State any justified different prospective criterion, its channel and scope before score access. Keep earlier registrations and verdicts unchanged. The experiment Decision section records separate local, DEV-exploration and TEST dispositions.
- `python scripts/render_tree.py` regenerates `docs/tree.md` (mermaid) from the headers — run it whenever an experiment file is added or its status changes.
- Leaderboard submissions snapshot into `submissions/` with the experiment ID, preregistered reading arms and actual scores. Include a justified numerical expectation only when available; do not invent one.
- Submission ZIPs use `submissions/YYYY-MM-DD-E0XX.zip`; matching source and scorecards use `submissions/YYYY-MM-DD-E0XX/`. Keep future deliverables in this established layout, not `output/dev/` (user preference, 2026-09-19).
- **End-of-day commit/push follows the active user's authorization.** Honor any
  no-commit/no-push scope; neither a session label nor an old template authorizes
  publishing changes. When authorized, commit task files only and verify origin.

## Study sessions

Domain study runs as one-paper-per-session via `paper-session`: Claude entry and
shared protocol at `.claude/skills/paper-session/SKILL.md`; Codex wrapper at
`.agents/skills/paper-session/SKILL.md`. Use the paper's own sections, three
self-check questions and the guide's tier-bound deliverable. Implementation
checks must stay within the user's permitted execution/data scope; unrun work is
unvalidated. Record the agreed summary in `docs/domain-study-guide.ko.md`.
Commit/push only under active user authorization, not automatically after study.
Windows/Codex environment setup is in `docs/codex-setup.ko.md`; no startup fit or
blanket test run is needed merely to resume a session.

## Rules for working here

- **All code, comments, and commit messages in English.**
- Never hardcode unverified assumptions about hidden competition responses. Use the synthetic sandbox, public schema/statistics and audited permitted public proxies such as the already approved Adult/SIPP channels. Keep external-data provenance, license/disclosure and leakage boundaries; never access or reconstruct private competition responses.
- The local harness precisely measures its own channel; it does not certify transfer. Prefer a qualified, decision-relevant DEV submission to an unused slot, but do not submit unverified changes or unreadable probes merely to fill the day. Follow `docs/workflow.md` for the mandatory submission checks and result interpretation.
- Log every experiment in `docs/log.md`; snapshot every submission in `submissions/`.
- Strategy priority: exact skip-logic handling → calibrated simple models (IRT + low-rank + smoothing) → hybrids. LLM persona-prompting is log-loss-unfavorable without calibration post-processing.
- `external/starter-kit/score.py` is the official grader — use it for final validation of any submission; keep `src/eval/` for fast in-process iteration and mirror its skill metric exactly.
