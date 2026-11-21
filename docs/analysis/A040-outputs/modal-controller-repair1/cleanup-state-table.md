# Cleanup reading contract

All observations below are mocked local cases. No current remote state was read.

| Observation | Recorded termination | Action/meaning |
|---|---|---|
| Preparation fails before create intent | NO_CREATE_ATTEMPT | No create/stop attempted |
| Create requested but response/ID lost | ID_UNKNOWN | Preserve intent; no discovery, recreate or invented stop ID |
| Known App, construction/build failure | Depends on exact-ID query | Primary exception preserved; stop at most once |
| Stop ACK, App still running | UNCONFIRMED | ACK is not termination |
| App stopped, nonzero tasks | UNCONFIRMED | Task completion not established |
| Stop timeout/failure | UNCONFIRMED unless query proves stopped+task0 | Preserve stop error and exact owned ID |
| Status query timeout/error | UNCONFIRMED | No stop reissue or build retry |
| Explicit STOPPED and successful task query empty | TERMINAL_TASK0_CONFIRMED | Only this pair confirms the mocked remote contract |
| Controller/process exits or parent kills it | No additional remote evidence | Client exit never promotes remote state |
| Whole worker deadline expires | UNCONFIRMED_WATCHDOG | Preserve partial journal/owned ID; parent kills only its worker |

Image outcome and cleanup outcome are separate fields. BUILD_COMPLETED and exit0
in a fake build case do not override UNCONFIRMED cleanup. Every consumer must read
the termination field; neither return code nor stop_ack is a remote success gate.
Primary error/traceback and cleanup errors coexist. No successful cleanup changes
a failed build into success. Terminal task0 alone does not prove installer/image,
H100 runtime, scientific effect, cost finality or release qualification.
