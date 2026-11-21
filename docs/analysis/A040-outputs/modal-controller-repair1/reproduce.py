"""Stdlib-only original encoding failure, no SDK or inputs."""
import io
import json
import time

started = time.monotonic()
stream = io.TextIOWrapper(io.BytesIO(), encoding="cp949", errors="strict")
try:
    stream.write("   \u2022 unpacking rootfs ... 한글")
except UnicodeEncodeError as exc:
    assert exc.encoding == "cp949" and exc.object[exc.start] == "\u2022"
    print(json.dumps({"original_cp949_reproduced": True, "error": repr(exc),
                      "seconds": time.monotonic() - started}))
else:
    raise AssertionError("Original cp949 defect not reproduced")
