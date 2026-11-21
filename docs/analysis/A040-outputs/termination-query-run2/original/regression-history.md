# Local evidence and failures

SDK1.6.0, Python3.13.14, existing venv only. Four focused child processes,
CPU affinity3 (two logical processors), hidden Windows launch, each below30s.
No old15/39/14/6 suite or science fixture rerun. Total outer wall: 3.1790341s.

1. `reproduce_wrapper.py`: actual old call extracted by AST, actual installed
   UnaryUnaryWrapper/direct, fake transport. Original timeout/default-retry
   InvalidError reproduced before transport (transport0).
2. `tests_query.cycle1.py`:20 fixed cases. Trace reaches the final billing assertion;
  19 earlier cases therefore completed their assertions in order. This is a
   control-flow inference, not19 separately captured PASS records. The final fake
   raised an already-converted SDK ServiceError instead of native GRPCError.
   Failure and source retained. Early process records have null/missing exit codes
   due to the PowerShell process-handle recording defect; stdout/trace is evidence.
3. Only the affected billing fake changed to native GRPCError. `tests_query.py
   billing_fail` passed through the real wrapper/auth manager; independent normal
   auth and external network negatives blocked. No successful whole-suite repeat.
4. First live entry failed before Query.run/Client.from_env: create_blocking does
   not accept the bound method. Same-session fix wraps it in a plain async
   function. `test_entry.py` reproduces that failure and validates the real SDK
   synchronizer with fake external transport. ENTRY_DISPATCH_PASS, captured exit0.

Final helper branch logic is unchanged by the entry repair. Main's same-window
file/deadline guard was added; a parent pre-launch guard refused continuation.
The entry test covers the synchronizer boundary, not a full live CLI/auth path.
Local checks establish only these named boundaries, not remote terminal status.

Reproduction recipe for a later authorized local check (not executed again here):
use the existing sdk-venv Python with `-I -c`, explicitly insert only this artifact
directory in sys.path, set sys.argv for the named case, then runpy.run_path with
run_name='__main__'. Plain `-I script.py` omits that import directory and is not a
valid recipe for these sibling modules. For example, from the repository root:

```powershell
& 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe' -I -c "import sys,runpy; from pathlib import Path; p=Path('docs/analysis/A040-outputs/termination-query-repair1').resolve(); sys.path.insert(0,str(p)); sys.argv=['tests_query.py','billing_fail']; runpy.run_path(str(p/'tests_query.py'),run_name='__main__')"
```

Historical checks used hidden CPU2 children with30s process limits; a later
reproduction must retain those limits. The source paths/case names and preserved
stdout/stderr identify the runs; this shorthand is not an archived full launcher.
Do not run confirm_terminal.py again under the consumed window. No token values
are stored in the artifacts. No successful suite was repeated for this closeout.
