import ctypes
from ctypes import wintypes

class MemoryTree:
    """Read only an owned Windows process tree; fail if counters unavailable."""
    class Entry(ctypes.Structure):
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
                    ('pid', wintypes.DWORD), ('heap', ctypes.c_size_t),
                    ('module', wintypes.DWORD), ('threads', wintypes.DWORD),
                    ('parent', wintypes.DWORD), ('priority', ctypes.c_long),
                    ('flags', wintypes.DWORD), ('exe', ctypes.c_wchar * 260)]

    class Counters(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('faults', wintypes.DWORD)] + [
            (n, ctypes.c_size_t) for n in ('peak_rss', 'rss', 'qpp', 'qp', 'qnp',
                                          'qn', 'page', 'peak_page', 'private')]

    def __init__(self, pid):
        self.pid = pid
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        self.kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        for name in ('Process32FirstW', 'Process32NextW'):
            getattr(self.kernel, name).argtypes = [wintypes.HANDLE, ctypes.POINTER(self.Entry)]
        self.kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.kernel.OpenProcess.restype = wintypes.HANDLE
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api = ctypes.WinDLL('psapi', use_last_error=True).GetProcessMemoryInfo
        self.api.argtypes = [wintypes.HANDLE, ctypes.POINTER(self.Counters), wintypes.DWORD]

    def sample(self):
        snapshot = self.kernel.CreateToolhelp32Snapshot(2, 0)
        if snapshot == ctypes.c_void_p(-1).value:
            raise OSError('Cannot enumerate processes')
        parents = {}
        entry = self.Entry()
        entry.dwSize = ctypes.sizeof(entry)
        try:
            more = self.kernel.Process32FirstW(snapshot, ctypes.byref(entry))
            if not more:
                raise OSError('Empty process snapshot')
            while more:
                parents[int(entry.pid)] = int(entry.parent)
                more = self.kernel.Process32NextW(snapshot, ctypes.byref(entry))
        finally:
            self.kernel.CloseHandle(snapshot)
        owned = {self.pid}
        while True:
            expanded = owned | {pid for pid, parent in parents.items() if parent in owned}
            if expanded == owned:
                break
            owned = expanded
        totals = {'rss': 0, 'commitment': 0}
        for pid in owned:
            handle = self.kernel.OpenProcess(0x410, False, pid)
            if not handle:
                raise OSError('Owned process counters unavailable')
            counters = self.Counters()
            counters.cb = ctypes.sizeof(counters)
            try:
                if not self.api(handle, ctypes.byref(counters), counters.cb):
                    raise OSError('Memory query failed')
                totals['rss'] += max(int(counters.rss), int(counters.peak_rss))
                totals['commitment'] += max(int(counters.private), int(counters.peak_page))
            finally:
                self.kernel.CloseHandle(handle)
        return totals


