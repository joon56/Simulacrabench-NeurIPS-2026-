"""Download the public TabICL v2 classifier checkpoint into weights/ and verify it.

Source: Hugging Face jingang/TabICL, revision 4dcd344ece2c00be9e831fdd35bed57b5ad83e19.
The submission bundles this file unchanged and loads it from weights/ at import.
"""
import hashlib
import urllib.request
from pathlib import Path

NAME = "tabicl-classifier-v2-20260212.ckpt"
URL = ("https://huggingface.co/jingang/TabICL/resolve/"
       "4dcd344ece2c00be9e831fdd35bed57b5ad83e19/" + NAME)
SIZE = 110368038
SHA256 = "bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    target = Path(__file__).resolve().parents[1] / "weights" / NAME
    target.parent.mkdir(exist_ok=True)
    if not (target.is_file() and target.stat().st_size == SIZE and digest(target) == SHA256):
        urllib.request.urlretrieve(URL, target)
    if target.stat().st_size != SIZE or digest(target) != SHA256:
        raise SystemExit("checkpoint does not match the expected size / SHA256")
    print("ok", target)


if __name__ == "__main__":
    main()
