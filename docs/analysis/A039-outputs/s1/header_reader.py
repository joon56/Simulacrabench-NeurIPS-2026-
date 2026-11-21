"""A039 fixed-path metadata audit; no response read-ahead or model imports."""
import csv
import hashlib
import io
import json
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DATA = ROOT / "UNCHR_data/microdata/UNHCR_JOR_2023_VAF_HOST_data_v2_1"
TABLES = ("main", "case", "family", "member", "sharing_group_long", "sharing_group_short")
FILE_IDS = dict(zip(TABLES, ("file_id", "f3", "f4", "f2", "f5", "f6")))
LIMIT = 128 * 1024


class HeaderHold(Exception):
    """Only fixed error codes; never includes possibly sensitive input."""


def read_header(stream, limit=LIMIT):
    raw = bytearray()
    for _ in range(limit):
        byte = stream.read(1)
        if not byte:
            raise HeaderHold("NO_LF")
        raw.extend(byte)
        if byte == b"\n":
            break
    else:
        raise HeaderHold("HEADER_LIMIT")
    try:
        text = bytes(raw).decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError:
        raise HeaderHold("UTF8_INVALID") from None
    text = text[:-1]
    if text.endswith("\r"):
        text = text[:-1]
    if "\r" in text or "\n" in text or "\x00" in text:
        raise HeaderHold("AMBIGUOUS_LINE")
    # csv.reader permits quotes embedded in unquoted fields; reject that syntax.
    state = "start"
    for char in text:
        if state == "start":
            state = "quoted" if char == '"' else ("start" if char == "," else "plain")
        elif state == "plain":
            if char == '"':
                raise HeaderHold("CSV_QUOTE_SYNTAX")
            if char == ",":
                state = "start"
        elif state == "quoted":
            if char == '"':
                state = "closed"
        elif state == "closed":
            if char == '"':
                state = "quoted"
            elif char == ",":
                state = "start"
            else:
                raise HeaderHold("CSV_QUOTE_SYNTAX")
    if state == "quoted":
        raise HeaderHold("QUOTED_NEWLINE_OR_UNCLOSED_QUOTE")
    try:
        names = next(csv.reader([text], strict=True))
    except (csv.Error, StopIteration):
        raise HeaderHold("CSV_SYNTAX") from None
    if not names or any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_ .:/(),-]*", n.strip()) for n in names):
        raise HeaderHold("SUSPICIOUS_HEADER")
    return bytes(raw), names


def duplicates(names):
    return [{"name": n, "positions_1based": [i + 1 for i, x in enumerate(names) if x == n]}
            for n, count in Counter(names).items() if count > 1]


def compare(actual, reference):
    return {
        "same_order_and_names": actual == reference,
        "actual_only": [n for n in actual if n not in reference],
        "reference_only": [n for n in reference if n not in actual],
        "shared_relative_order_equal": ([n for n in actual if n in reference]
                                        == [n for n in reference if n in actual]),
        "actual_duplicates": duplicates(actual),
        "reference_duplicates": duplicates(reference),
    }


def main():
    destination = OUT / "header-comparison.json"
    if destination.exists():
        raise SystemExit("Existing result preserved; no repeated actual-header read")
    entry = json.loads((OUT / "entry.json").read_text(encoding="utf-8-sig"))
    deadline = datetime.fromisoformat(entry["deadline_utc"].replace("Z", "+00:00"))
    routing_path = ROOT / "docs/analysis/A032-outputs/routing-metadata.json"
    routing = json.loads(routing_path.read_text(encoding="utf-8"))
    report = {"scope": "FIRST_PHYSICAL_HEADER_ONLY", "tables": [], "response_bytes_requested": 0,
              "read_method": "Python FileIO buffering=0, read(1), stop at first LF; OS cache not audited",
              "max_bytes_per_file": LIMIT, "max_total_bytes": len(TABLES) * LIMIT,
              "routing_metadata_sha256": hashlib.sha256(routing_path.read_bytes()).hexdigest()}
    start = time.perf_counter()
    total = 0
    failure = None
    for table in TABLES:
        if datetime.now(timezone.utc) >= deadline:
            failure = "WALL_LIMIT"
            break
        data_path = DATA / f"UNHCR_JOR_2023_VAF_HOST_data_{table}_v2.1.csv"
        label_path = DATA / f"UNHCR_JOR_2023_VAF_HOST_labels_{table}_v2.1.csv"
        record = {"table": table, "data_path": data_path.relative_to(ROOT).as_posix()}
        report["tables"].append(record)
        try:
            if data_path.resolve() != data_path or label_path.resolve() != label_path:
                raise HeaderHold("PATH_REDIRECTION")
            label_bytes = label_path.read_bytes()  # VAR/LABEL documentation, not responses.
            labels = list(csv.DictReader(io.StringIO(label_bytes.decode("utf-8-sig")), strict=True))
            if not labels or set(labels[0]) != {"VAR", "LABEL"}:
                raise HeaderHold("LABEL_DOCUMENT_SHAPE")
            label_names = [row["VAR"] for row in labels]
            ddi = [v for v in routing["ddi_variables"] if v["file"] == FILE_IDS[table]]
            ddi_names = [v["name"] for v in ddi]
            stat = data_path.stat()
            record.update({"file_size_stat_bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns})
            with data_path.open("rb", buffering=0) as stream:
                try:
                    raw, names = read_header(stream)
                finally:
                    record["application_bytes_read"] = stream.tell()
                    total += stream.tell()
            record.update({
                "header_bytes_including_LF": len(raw), "header_sha256": hashlib.sha256(raw).hexdigest(),
                "hash_scope": "Header bytes only, including optional BOM and CRLF/LF; never whole CSV",
                "utf8_bom": raw.startswith(b"\xef\xbb\xbf"), "line_ending": "CRLF" if raw.endswith(b"\r\n") else "LF",
                "columns": names, "column_count": len(names),
                "whitespace_positions_1based": [i + 1 for i, n in enumerate(names) if n != n.strip()],
                "labels_path": label_path.relative_to(ROOT).as_posix(),
                "labels_sha256": hashlib.sha256(label_bytes).hexdigest(), "labels_rows": len(labels),
                "labels_order": label_names, "ddi_file": FILE_IDS[table],
                "ddi_count": len(ddi), "ddi_order": ddi_names,
                "header_vs_labels": compare(names, label_names), "header_vs_ddi": compare(names, ddi_names),
            })
            keys = ("ID_main", "ID_ind", "Form", "householdindex", "sharingindex", "familyindex",
                    "caseindex", "individualindex", "index", "parent_index")
            record["key_metadata"] = [{"name": key, "header_present": key in names,
                "labels": [row["LABEL"] for row in labels if row["VAR"] == key],
                "ddi_definitions": [v for v in ddi if v["name"] == key]} for key in keys]
            record["named_examples"] = [{"name": name, "header_present": name in names,
                "labels": [row["LABEL"] for row in labels if row["VAR"] == name],
                "ddi_definitions": [v for v in ddi if v["name"] == name]}
                for name in ("FamilyRegistered", "NotRegIDFamilyType", "IndAge", "WGQSeeing", "WGQDepression", "MedicalAccess")]
            pattern = re.compile(r"missing|imput|edit|skip|refus|dont.?know|not.?applic|break|interrupt|complete|disabled|reason", re.I)
            record["lexical_flag_candidates_not_semantic_proof"] = [
                {"name": row["VAR"], "label": row["LABEL"], "header_present": row["VAR"] in names}
                for row in labels if pattern.search(row["VAR"] + " " + row["LABEL"])]
            record["status"] = "HEADER_RECONCILED" if names == label_names == ddi_names else "HEADER_DIVERGENCE"
        except (HeaderHold, OSError, UnicodeError, csv.Error) as error:
            failure = str(error) if isinstance(error, HeaderHold) else type(error).__name__
            record.update({"status": "TECHNICAL_HOLD", "error_code": failure})
            break
    report.update({"total_header_bytes_requested": total, "wall_seconds": time.perf_counter() - start,
                   "ended_utc": datetime.now(timezone.utc).isoformat(), "failure_code": failure,
                   "status": "TECHNICAL_HOLD" if failure else (
                       "HEADER_RECONCILED" if all(t["status"] == "HEADER_RECONCILED" for t in report["tables"])
                       else "HEADER_DIVERGENCE")})
    with destination.open("x", encoding="utf-8") as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
    print(json.dumps({"status": report["status"], "files_attempted": len(report["tables"]),
                      "header_bytes": total, "failure_code": failure}))
    return 1 if failure else 0


if __name__ == "__main__":
    sys.exit(main())
