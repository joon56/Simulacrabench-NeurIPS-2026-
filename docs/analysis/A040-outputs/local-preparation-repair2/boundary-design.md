# Local boundary, registered before SDK checks

Only local preparation; execution cutoff09:53:15Z, closeout10:03:15Z on2026-10-05.
Installed SDK1.6.0/Python3.13.14 reused. No account or protected input needed.

Guard is installed before any event loop or SDK import. Wrap stdlib socketpair
without changing its implementation. Accept calls only from the exact stdlib
selector/proactor `_make_self_pipe` code objects. A thread-local token scopes the
call. Audit bind/connect must originate inside the actual `_fallback_socketpair`
code, refer to its own lsock/csock, and use the listener's own loopback endpoint.
Retain socket objects and process/thread IDs; prove both endpoints closed after
each loop lifetime. No general localhost/DNS exception. SDK changes Windows loop
policy; exercise a pre-import loop, post-import loop, and synchronicity worker loop.

Independently block config/token/protected-file reads, model imports, subprocess/
shell execution, external DNS/connect, client acquisition/authentication, RPC,
image build and resolver entry. Trace guards stop installer before its first body
line. Expected negative controls use dummy arguments and are recorded separately;
unexpected forbidden-operation attempts STOP. No source-discovery/mount/function
constructor is replaced. External image-build endpoint is an explicit capture/
interrupt, never a fake successful build.

SDK mount/spec/dependency inspection precedes minimal production flag change.
Require FILE, controller_core.install_pins, exact /root/controller_core.py and
one project file separate from the SDK default client mount. Validate actual
selected bytes, not consumer constants alone. Exact bytes staged into a fresh
directory; a separate -I/-S process adds only that directory to sys.path.
Installer is never executed. Missing/extra/path/hash negatives are local only.

Parent launcher: hidden child, affinity two logical CPUs before controlled work,
27s timeout, owned tree termination if needed, residual PID check, append-only
process receipts/snapshots; sum<=180s. No nested test subprocesses. Environment
probe first. Generic successful suites not repeated. Cooperative Python guards
are not native/OS egress certification or actual remote delivery proof.

Source basis: Python socket.py `_fallback_socketpair` binds ephemeral listener,
connects its own csock, checks reciprocal peers, closes listener. Modal
async_utils.py:43 sets WindowsSelectorEventLoopPolicy; synchronicity
synchronizer.py:212-262 creates/joins a thread loop; async_utils.Runner creates
another loop. Modal _image.py:2772-2788 creates real FunctionSourceInfo/_Function;
_functions.py:771-775 selects source/client mounts; function_utils.py:382-395
selects one defining FILE. No installed source edits.
