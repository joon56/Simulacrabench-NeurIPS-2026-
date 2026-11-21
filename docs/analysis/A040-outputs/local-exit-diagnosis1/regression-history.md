# Local exit diagnosis

Fixed Python3.13.14 / Modal1.6.0 / synchronicity0.12.5 / protobuf6.33.6 /
grpclib0.4.9. Each named comparison registered before execution.

| Comparison | Changed boundary | Observation |
|---|---|---|
| C1 | Builder execution vs same imports/managed noop | builder c0000005; noop exit0 |
| C2 | Remove A040 launcher/Context orchestration | reduced Endpoint build still c0000005 |
| C3 | Stop after image definition instead of build | exit0 |
| C4 | Remove suspended-coroutine observer only | same build still c0000005 |
| C5 | Remove output-manager display wrapper only | same build still c0000005 |
| C6 | Proposed protobuf graph/parser addition to definition control | NOT RUN: time gate |

Six Python invocations, five executed comparisons, supervisor27.3473137s/240s.
Each process below30s, CPU affinity3; actual Python and venv launcher IDs/exits
separate; forced0 and no remaining observed Python jobs. GC/crash stderr retained.
Child assertions never override native failure. c1-loop's generic verdict file
expects an incorrect result path; its actual c1-loop-result.json plus both exit0
receipts support the loop observation. That old verdict is preserved.

C5 tool JavaScript quoting failure occurred before command execution; corrected
without a Python invocation. C6 was prepared, then launch rejected by time gate.
Closeout writer had a PowerShell parse error before executing any statement;
corrected as document work only. All failed tool results remain in transcript.
No120s replay, full success lifecycle or previous successful suites.
Gross session40min exceeded. No unverified waiting deduction, cap reset or
deadline extension. Further execution stopped; only required closeout followed.