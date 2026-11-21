"""Exact declared file transport; payload bytes enter only through an endpoint."""
from pathlib import Path
from contract import safe_relative, sha


class FileReader:
    def __init__(self, root, allowed, plan):
        if plan.scope != "LIVE" or not plan.execution_authorized:
            raise PermissionError("Real payload reading not authorized")
        self.root = Path(root).resolve()
        self.allowed = set(allowed)
    def __call__(self, name):
        safe_relative(name)
        if name not in self.allowed:
            raise PermissionError("Undeclared payload")
        unresolved = self.root / name
        path = unresolved.resolve()
        if self.root not in path.parents or any(p.is_symlink() for p in (unresolved, *unresolved.parents)):
            raise PermissionError("Payload path escape")
        return path.read_bytes()


class Payload:
    def __init__(self, original, extra, reader, extra_reader, scope):
        self.original, self.extra = original, extra
        self.reader, self.extra_reader = reader, extra_reader
        self.files = original + extra
        if len({r["path"] for r in self.files}) != len(self.files):
            raise ValueError("Duplicate transfer path")
        if scope == "LIVE" and (len(original) != 112 or sum(r["bytes"] for r in original) != 145542095):
            raise ValueError("Original112 payload contract mismatch")
        for row in self.files:
            safe_relative(row["path"])
        for row in extra:
            if not row.get("reason") or Path(row["path"]).suffix not in (".py", ".json", ".txt"):
                raise ValueError("Undeclared nondata addition")

    def _bytes(self, row, extra=False):
        raw = (self.extra_reader if extra else self.reader)(row["path"])
        if len(raw) != row["bytes"] or sha(raw) != row["sha256"]:
            raise ValueError("Payload identity mismatch: " + row["path"])
        return raw

    def verify(self):
        for extra, rows in ((False, self.original), (True, self.extra)):
            for row in rows:
                self._bytes(row, extra)
        return {"files": len(self.files), "bytes": sum(r["bytes"] for r in self.files), "verified_at_endpoint": True}

    async def transfer(self, filesystem, operation):
        # Recheck each exact byte buffer immediately before sending it.
        for extra, rows in ((False, self.original), (True, self.extra)):
            for row in rows:
                raw = self._bytes(row, extra)
                await operation(filesystem.write_bytes(raw, "/work/" + row["path"]), "transfer")
        return {"files": len(self.files), "bytes": sum(r["bytes"] for r in self.files)}
