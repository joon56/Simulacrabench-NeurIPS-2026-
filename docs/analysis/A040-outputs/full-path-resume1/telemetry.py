"""Small JSONL logger; no scientific dependencies."""
import json
import time


class EventLog:
    def __init__(self, sink):
        self.sink = sink
        self.start = time.perf_counter()

    def emit(self, event_name, **details):
        self.sink.write(json.dumps(dict(event=event_name, elapsed=time.perf_counter()-self.start, **details))+'\n')
        self.sink.flush()
