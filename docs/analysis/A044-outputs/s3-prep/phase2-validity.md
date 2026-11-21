# S3-PREP-A044 — phase2 validity and preserved delivery identities

Categories: **CURRENT_IDENTITY**, **HISTORICAL_REUSABLE**, **INVALIDATED**, **UNKNOWN**.
They apply per boundary, never as one overall current phase2 PASS.

| Boundary | Current inspection | Historical evidence / verdict |
|---|---|---|
| E041 source/snapshot | A018 source and dated main hashes match; static dispatch/partition/selector/replay text read | CURRENT_IDENTITY; A012 source-to-assembly442425 raw equality remains HISTORICAL_REUSABLE |
| E025 source/snapshot | Dated main and preserved source hashes match | CURRENT_IDENTITY; A018 fresh equality was assembly-to-frozen-assembly, not fresh modular-source parity |
| Both September25 archives | Read-only bytes/hash/member list; main+starter MIT only, both member hashes match snapshots | CURRENT_IDENTITY; old checker PASS reused historically, not rerun |
| Both dated method PDFs/Markdown | Hashes match A018 freeze | CURRENT_IDENTITY of old bytes; four-page layout/visual review historical only; current wording outdated |
| Synthetic input/frame/roles | No response/Parquet/key/NPZ/cache access or rehash | UNKNOWN current identity; old frame/hash/role reports inherited only |
| Raw outputs/order | No arrays opened/recomputed | UNKNOWN current raw identity; A012/A018442425-vector/order parity HISTORICAL_REUSABLE for those runs |
| Public scorer/schema/checker | Old local hashes match A018; pinned-current comparison compatible, newline equality explicit | CURRENT_IDENTITY locally plus compatible public contract; no semantic invalidation observed |
| Runtime environment | Read old environment reports; no current package import/freeze/install | HISTORICAL_REUSABLE Python3.13.14/torch2.13.0+cpu/threads2; current environment and hosted image UNKNOWN |
| E041 official run/log | A018 official summary and logs match frozen hashes | HISTORICAL_REUSABLE all3 PASS, official359.448694s, orchestration364.340160s |
| E025 official provenance | Existing report retained, no new evidence invented | UNKNOWN full raw/scorer/data binding; already-known gap, not a newly failed run |
| Shared all3 resource rehearsal | Frozen E041/E025 resource JSON matches | HISTORICAL_REUSABLE336.554468/332.782386s, includes import/load/input/scoring/parity |
| Old calendar/final-choice prose | Current calendar differs; user says choice open | INVALIDATED as current instructions; historical files kept unchanged |

Shared-process peak working set/private commitment bytes:
E0411,493,135,360 /1,604,792,320; E0251,469,911,040 /1,557,315,584.
Observed Windows CPU process peaks are not Linux cgroup/H100 VRAM guarantees.
Native GPU optimizer timing and hidden-data activation remain unmeasured.
No linear refit scaling or speed forecast follows from these values.

Historical phase2 paired skills (UNICEF/WB/UNHCR):
E041 .490197770701/.462029504790/.564665364947;
E025 .490197770701/.462029504790/.565173813942.
Difference0/0/−.000508448996 satisfies A012/A018's **absolute .002** release
criterion. B01 separately specifies absolute difference<=.002 versus E025 and
signed candidate−E041>=−.002; do not rewrite either criterion retrospectively.
Neither is an efficacy/adoption test.

Disclosed deviations preserved: A012 baseline workers scored before raw saving and
supplementary provenance followed fitting; original one-sided report was corrected
in a derived absolute-threshold report without refitting. A018 first E025 attempt
was stopped for concurrent work; initial guards enforced limits after instruments,
with post-run guard repairs recorded separately. Completed timings stayed below
their caps. No renewed allowance or retrospective stronger enforcement claim.

E025 historical official minus A012 UNICEF/WB differences +.000007983303 and
−.000012753036 remain unexplained. Re-reading this gap is not a new failure.
E041's fresh official/source binding is stronger. See [revalidation plan](revalidation-plan.md)
for the narrowly conditional next work; no such execution was authorized here.

## Exact preserved paths — not an instruction to submit

| Candidate | ZIP / bytes | SHA256 |
|---|---|---|
| E041 provisional | `submissions/2026-09-25-E041.zip` /14314 | `bd5d2b7df3c39338f68cb08f125f85695073f37c9f4be3f6adcb8961941cd132` |
| E025 alternative | `submissions/2026-09-25-E025.zip` /11240 | `142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f` |

Each matching directory contains `main.py`, `LICENSE-starter-kit.txt`,
`method-4p.md`, `method-4p.pdf`, `SCORES.md`. Methods remain separate attachments.
PDF SHA256: E041 `13713a04c57d9efda5b4c9aef7d20b4a7c05e9589e8c00f8a4389e1a1cf2e8a2`;
E025 `24f042a7def50b11d73914236a3c57ce9675359a96ba20ae2a22b0e01a69e3fd`.
They identify the old documents, not approval of their now-stale
selected/date/Terms wording.
Source main hashes: E041 `22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`;
E025 `00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9`.

Evidence files: [identity-checks.json](identity-checks.json),
[archive-identities.json](archive-identities.json), [kit-hashes.json](kit-hashes.json).
No arrays were traversed from manifests. The initial source-hash allowlist was
overbroad: it also hashed unrelated `src/*.py` entries named by A018, beyond the
direct-dependency scope. This metadata-only deviation is retained in the112-item
record; no unrelated model was imported, executed, evaluated or modified, and
no protected input was read. Subsequent inspection is restricted to named sources.
