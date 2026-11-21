# Local controller repair: facts, changes, limits

2026-10-04 KST. Original resume2 failure and all historical artifacts remain intact.

## Cause supported by evidence

The saved build-result traceback reports cp949 failing on U+2022 in streamed image
logs. `reproduce.py` reproduces that encoding failure with a strict TextIOWrapper;
it does not import Modal or replay the remote image. `launcher.py` now supplies
`-X utf8`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`; the worker reconfigures both
streams to UTF-8/strict. Parent pipes and redirected files retain binary bytes;
JSON files explicitly use UTF-8. Bullet/Korean characters and exceptions survive.
No character replacement, log suppression or exception-to-success conversion.

Original cancellation gather and AppStop await were unbounded. Original try/finally
also began after creation and image construction. New controller encloses prepare,
create, construction and build; records create intent and exact returned App ID
before proceeding; persists primary traceback before cleanup. No new create/build
or stop retry after a failure. A lost create response records ID_UNKNOWN, without
inventing an ID or discovering/recreating resources.

`bounded` uses finite asyncio.wait and finite cancellation grace, not wait_for's
potentially unbounded cancellation handshake. Cleanup has an overall monotonic
deadline and bounded stop/status waits. An isolated worker writes/flushes its
records then exits without asyncio.run shutdown's unbounded gather. Parent watchdog
kills only its worker; the worker audit hook prohibits child process creation.
Even a blocked event loop is bounded. Watchdog termination means UNCONFIRMED and
retains any partial journal/owned ID; it is never evidence of remote termination.

## SDK source evidence and uncertainty

SDK1.6.0 was already installed; no SDK import or account operation was needed.
Source reviewed: modal/client.py:_Client.from_env and _call_safely, app.py:_App.lookup,
_image.py:_Image.build and _image_await_build_result. `_call_safely` explicitly
warns when the running loop differs from its client cancellation-context loop.
Actual extracted method AST passed same-loop, different-loop warning and closed
client mocks (`sdk-contract-result.json`). Thus the warning has a specific source
condition; the complete historical hang and its precise trigger remain unproven.

The adapter consistently awaits internal async-shaped Client/Workspace/App/Image
objects and the same client's raw stub, without public .aio wrappers. Fake SDK
methods assert one event loop. This is not end-to-end real SDK interoperability:
there is no live binding in this repair, no actual SDK import, transport or server.
Future binding uses `_Client`, `_Workspace`, `_App`, `_Image` from the pinned SDK;
these are private/version-sensitive interfaces requiring future authorized review.
SDK/provider internal retries are outside these mock call counts. The controller
itself issues create/build/stop at most once; no new retry policy was introduced.

## Preserved policy and implementation boundary

Installer function source is identical after line-ending normalization. Registry
base python:3.13.14-slim, CPU(1,1), memory(8192,8192), installer600s,
include_source=False and original requirement/deadline arguments are retained.
The original .65 overhead estimate, resource rates,45s billing interval and
management4/deadline-45 shutdown checks remain in the injected adapter.
Requirements are opaque caller input; real34 pins, staging112, model/checkpoint,
protected responses/keys/caches were not read or hashed. This is source-preservation
evidence, not current input/recipe deployment parity or frozen Linux image proof.

`controller.py` replaces the old controller in a NEW directory. `source.diff`
compares it to the preserved original. The live top-level SDK/input reads and old
deadline/latch were removed from this new module in favor of explicit injection.
`launcher.py` and `fake_worker.py` are the tested local execution path, not a
remote retry command. Fixture phase0.12s/cleanup0.35s/watchdog3s (blocking case1s)
are local contract scales; no future900s/deployment deadline was assigned here.

## Regression history

1. Original cp949 reproducer succeeded (expected UnicodeEncodeError).
2. First suite failed in fake App.lookup logging: `note(name, name=...)` collision.
   Preserved suite1 sources and outputs. Changed metadata key to app_name only;
   no scientific/model/policy change. Parent exit code was not captured by the
   first PowerShell wrapper (null); stderr/assertion is direct failure evidence.
3. Corrected suite:15/15 PASS. Actual pipe/file launcher, normal/error Unicode,
   resistant task, stop timeout/failure, ACK running, stopped with tasks, stopped
   task0, create response loss, early prepare/construct errors, query timeout,
   blocked event-loop watchdog. Results and all redirected logs are retained.
4. Separate actual SDK AST method contract passed; no repeated successful suite.

Four top-level regression invocations,16 scenario workers (1 failed+15 complete).
Top-level measured subprocess wall6.5996745s includes child execution; do not add
child times again. Worker pending task counts in resistant cases are intentional;
their isolated process exit was observed by the parent. No worker survived.

Network evidence: only fake SDK binding exists in the executable worker; actual
SDK/model imports are forbidden; socket connection/DNS/send and subprocess audit
events are blocked. Each completed worker passes a synthetic socket audit-event
negative probe without opening a socket, then reports zero real blocked attempts.
This is local enforcement/evidence, not an OS packet capture or server observation.
All fake-owned IDs begin ap-FAKE; original remote IDs were never queried.

## Remaining work belongs to S0

LOCAL_CONTROLLER_CONTRACT_PASS means these local contracts only. S0 reviews diff,
private async binding risk, and a separately bounded future remote scope if useful.
That scope must cover live binding, required identity/status checks, new deadline,
cumulative time/cost and actual termination evidence. Old base-image SUCCESS is
historical metadata, not reusable full dependency image qualification. No remote
retry, image reuse, H100 request or scientific permission follows from this PASS.
