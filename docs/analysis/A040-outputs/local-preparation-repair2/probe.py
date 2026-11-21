"""Interpreter entry only; no SDK, account, model or data access."""
import sys
import time
from pathlib import Path
gate = Path(sys.argv[2])
end = time.monotonic() + 5
while not gate.exists():
    if time.monotonic() >= end:
        raise TimeoutError('Parent CPU-affinity gate missing')
    time.sleep(.01)
print(sys.version)
print(sys.executable)
print(sys.base_prefix)
