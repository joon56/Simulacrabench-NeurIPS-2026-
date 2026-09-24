# A012 archived verification

Raw source and official prediction vectors are retained with their original
JSON/log bytes. Verification and post-run provenance are in
submissions/phase2-E041-preparation/. The executed verifier is a historical
byte-exact copy, not the current corrected script; do not rerun this namespace.

The frozen-artifact probe is the verbatim reviewer-authored script executed
from tmp/. Copy it to tmp/ before rerunning with the project Python environment:
its repository-root lookup intentionally retains that original location.
It verifies stored hashes, vectors, roles and arithmetic without model fitting
or new scoring. The .log is the original root execution transcript; the final
review distinguishes reviewer checks from root execution.
