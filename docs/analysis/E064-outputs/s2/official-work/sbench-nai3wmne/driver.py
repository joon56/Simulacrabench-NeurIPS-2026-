import socket


class NetworkAccessDenied(OSError):
    pass


def _denied(*args, **kwargs):
    raise NetworkAccessDenied(
        "the submission tried to use the network; scoring runs offline")


class _DeniedSocket(socket.socket):
    """Refuses to be opened.

    Stays a class rather than becoming a function because the standard library
    subclasses socket.socket -- ssl does `class SSLSocket(socket)` at import
    time -- and a function there raises a baffling TypeError instead of a
    message that tells the participant what they actually did wrong.
    """

    def __init__(self, *args, **kwargs):
        _denied()


socket.socket = _DeniedSocket

for _name in ("create_connection", "socketpair", "getaddrinfo",
              "gethostbyname", "gethostbyname_ex", "create_server"):
    if hasattr(socket, _name):
        setattr(socket, _name, _denied)

import json
import sys

import pandas as pd

work, submission = sys.argv[1], sys.argv[2]
sys.path.insert(0, submission)

with open(work + "/data.json", encoding="utf-8") as fh:
    payload = json.load(fh)
frame = pd.DataFrame(payload["data"], columns=payload["columns"])

with open(work + "/schema.json", encoding="utf-8") as fh:
    schema = json.load(fh)

import main

vectors = main.predict(frame, schema)

with open(work + "/predictions.json", "w", encoding="utf-8") as fh:
    json.dump([[float(x) for x in vector] for vector in vectors], fh)
