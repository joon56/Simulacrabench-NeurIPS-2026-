"""Bounded, aggregate-only audit of the official SIPP 2023 hospital channel.

No model is fitted. The local Parquet extract is restricted and must stay ignored.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "external" / "sipp-2023"
ZIP = CACHE / "pu2023_csv.zip"
SCHEMA = CACHE / "pu2023_schema.json"
PLAN = ROOT / "docs" / "plans" / "2026-09-24-A014.md"
OUTPUT = ROOT / "docs" / "analysis" / "A014-outputs" / "data-audit.json"
EXTRACT = CACHE / "a014-month12-restricted.parquet"
MANIFEST = CACHE / "a014-partitions.json"
PRE_RUN = ROOT / "docs" / "analysis" / "A014-outputs" / "pre-run.json"
REGISTRATION = ROOT / "docs" / "analysis" / "A014-outputs" / "audit-registration.md"

KEYS = ["SSUID", "PNUM", "MONTHCODE", "ERESIDENCEID"]
GIVEN = ["TAGE", "ESEX", "ERACE", "EORIGIN", "EEDUC", "EMS"]
REASONS = ["EHREAS_DT", "EHREAS_BIR", "EHREAS_OS", "EHREAS_NST", "EHREAS_OTH", "EHREAS_COR"]
FLAGS = ["AHOSPNIT", "AHREASON"]
FIELDS = KEYS + ["THHLDSTATUS", "TAGE_EHC"] + GIVEN + ["THOSPNIT"] + FLAGS + REASONS
ROLES = [("fit", 50), ("calibration", 65), ("oracle", 80), ("selection", 90), ("audit", 100)]


def _digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _bucket(namespace: str, *parts: str) -> str:
    payload = "\0".join((namespace, *parts)).encode("utf-8")
    bucket = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big") % 100
    return next(role for role, upper in ROLES if bucket < upper)


def assign_roles(frame: pd.DataFrame, grouped: bool = False) -> pd.Series:
    """Stable role per person or conservative sample unit, independent of row order."""
    namespace = "A014-household-v1" if grouped else "A014-person-v1"
    if grouped:
        values = [_bucket(namespace, str(ssuid)) for ssuid in frame["SSUID"]]
    else:
        values = [_bucket(namespace, str(ssuid), str(pnum)) for ssuid, pnum in zip(frame["SSUID"], frame["PNUM"])]
    return pd.Series(values, index=frame.index, name="role")


def validate_unique(frame: pd.DataFrame) -> None:
    if frame[["SSUID", "PNUM", "MONTHCODE"]].eq("").any(axis=None):
        raise ValueError("blank person-month key")
    if frame.duplicated(["SSUID", "PNUM", "MONTHCODE"]).any():
        raise ValueError("duplicate person-month key")


def encode_reasons(frame: pd.DataFrame) -> pd.DataFrame:
    """Encode only documented blank+flag-zero sentinel; retain answered contradictions."""
    out = frame[REASONS].copy() if set(REASONS).issubset(frame.columns) else frame.filter(regex=r"^EHREAS_").copy()
    for column in out:
        blank = out[column].eq("")
        ambiguous = blank & ~frame["AHREASON"].eq("0")
        if ambiguous.any():
            raise ValueError(f"ambiguous missing reason: {column}, {int(ambiguous.sum())} rows")
        out.loc[blank, column] = "0"
        invalid = ~out[column].isin(["1", "2"]) & ~blank
        if invalid.any():
            raise ValueError(f"invalid reason value: {column}")
    return out


def _metadata() -> dict:
    records = json.loads(SCHEMA.read_text(encoding="utf-8"))
    by_name = {record["name"]: record for record in records}
    absent = sorted(set(FIELDS) - by_name.keys())
    if absent:
        raise ValueError(f"missing selected metadata fields: {absent}")
    return by_name


def _archive_member(archive: ZipFile):
    entries = archive.infolist()
    if len(entries) != 1 or entries[0].filename != "pu2023.csv" or entries[0].is_dir():
        raise ValueError("archive must contain exactly pu2023.csv")
    member = entries[0]
    if member.file_size > 12 * 1024**3 or member.file_size <= 0:
        raise ValueError("decompressed release exceeds bound")
    if ZIP.stat().st_size > 1024**3:
        raise ValueError("raw release exceeds 1 GiB bound")
    return member


def _counts(series: pd.Series) -> dict[str, int]:
    return {str(k): int(v) for k, v in sorted(series.value_counts(dropna=False).items(), key=lambda kv: str(kv[0]))}


def _integer_range(series: pd.Series, low: int, high: int) -> pd.Series:
    parsed = pd.to_numeric(series, errors="coerce")
    return series.str.fullmatch(r"-?\d+").fillna(False) & parsed.between(low, high)


def run() -> dict:
    for destination in (EXTRACT, MANIFEST, OUTPUT, PRE_RUN, REGISTRATION):
        if destination.exists():
            raise FileExistsError(f"refusing overwrite: {destination}")
    metadata = _metadata()
    source_hashes = {"zip_sha256": _digest(ZIP), "schema_sha256": _digest(SCHEMA),
                     "script_sha256": _digest(Path(__file__)), "plan_sha256": _digest(PLAN)}
    PRE_RUN.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PLAN, REGISTRATION)
    PRE_RUN.write_text(json.dumps({"source": "https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html",
                                   "metadata": "https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2023/2023_SIPP_Data_Dictionary.pdf",
                                   "selected_columns": FIELDS, "hashes": source_hashes}, indent=2), encoding="utf-8")
    month_frames: list[pd.DataFrame] = []
    person_months: Counter[tuple[str, str]] = Counter()
    seen_keys: set[tuple[str, str, str]] = set()
    total = 0
    with ZipFile(ZIP) as archive:
        member = _archive_member(archive)
        with archive.open(member) as stream:
            chunks = pd.read_csv(
                stream, sep="|", usecols=FIELDS, dtype=str, keep_default_na=False,
                chunksize=5000, encoding="utf-8", on_bad_lines="error",
            )
            for chunk in chunks:
                total += len(chunk)
                if total > 2_000_000:
                    raise ValueError("release exceeds 2 million row bound")
                validate_unique(chunk)
                keys = set(zip(chunk["SSUID"], chunk["PNUM"], chunk["MONTHCODE"]))
                if seen_keys.intersection(keys):
                    raise ValueError("duplicate person-month key across chunks")
                seen_keys.update(keys)
                person_months.update(zip(chunk["SSUID"], chunk["PNUM"]))
                selected = chunk.loc[chunk["MONTHCODE"].eq("12"), FIELDS]
                if not selected.empty:
                    month_frames.append(selected.copy())
    month = pd.concat(month_frames, ignore_index=True)
    validate_unique(month)
    person_roles = assign_roles(month)
    group_roles = assign_roles(month, grouped=True)
    eligible_mask = month["THHLDSTATUS"].isin(["1", "2"]) & _integer_range(month["TAGE_EHC"], 1, 200)
    eligible = month.loc[eligible_mask]
    parent_valid = _integer_range(eligible["THOSPNIT"], 0, 365)
    parent = pd.to_numeric(eligible["THOSPNIT"], errors="coerce")
    child_values = {field: _counts(eligible[field]) for field in REASONS}
    blank_reason = eligible[REASONS].eq("")
    ambiguous = blank_reason.any(axis=1) & ~eligible["AHREASON"].eq("0")
    invalid_reasons = eligible[REASONS].apply(lambda column: ~column.isin(["", "1", "2"])).any(axis=1)
    contradictions = {
        "parent_zero_answered_reason": int((parent.eq(0) & eligible[REASONS].isin(["1", "2"]).any(axis=1)).sum()),
        "parent_positive_any_blank_reason": int((parent.gt(0) & blank_reason.any(axis=1)).sum()),
        "parent_positive_all_no_or_blank": int((parent.gt(0) & ~eligible[REASONS].isin(["1"]).any(axis=1)).sum()),
    }
    candidate_copies = {}
    for field in GIVEN:
        candidate_copies[field] = {}
        for target in ["THOSPNIT", *REASONS]:
            comparable = eligible[field].ne("") & eligible[target].ne("")
            matching = eligible.loc[comparable, field].eq(eligible.loc[comparable, target])
            candidate_copies[field][target] = {
                "comparable": int(comparable.sum()), "equal": int(matching.sum()),
                "exact_copy": bool(comparable.sum() >= 100 and matching.all() and eligible.loc[comparable, target].nunique() > 1),
            }
    person_counts = pd.Series(list(person_months.values()), dtype="int64")
    household_size = eligible.groupby(["SSUID", "ERESIDENCEID"], sort=False).size()
    role_counts = {"person": _counts(person_roles), "sample_unit": _counts(group_roles)}
    role_eligible = {"person": _counts(person_roles.loc[eligible_mask]),
                     "sample_unit": _counts(group_roles.loc[eligible_mask])}
    hospitalized_mask = eligible_mask & pd.to_numeric(month["THOSPNIT"], errors="coerce").gt(0)
    role_hospitalized = {"person": _counts(person_roles.loc[hospitalized_mask]),
                         "sample_unit": _counts(group_roles.loc[hospitalized_mask])}
    group_overlap = int((pd.DataFrame({"SSUID": month["SSUID"], "role": group_roles})
                         .groupby("SSUID")["role"].nunique() > 1).sum())
    flag_crosstabs = {
        "THOSPNIT_by_AHOSPNIT": {str(k): int(v) for k, v in eligible.groupby(["AHOSPNIT", "THOSPNIT"]).size().items()},
        **{f"{field}_by_AHREASON": {str(k): int(v) for k, v in eligible.groupby(["AHREASON", field]).size().items()}
           for field in REASONS},
    }
    usable_given = [field for field in GIVEN if eligible[field].ne("").sum() >= 5000 and eligible.loc[eligible[field].ne(""), field].nunique() >= 2]
    direct_copies = [field for field, checks in candidate_copies.items() if any(check["exact_copy"] for check in checks.values())]
    technical_eligible = (len(eligible) >= 5000 and int(parent.gt(0).sum()) >= 200
                          and len(usable_given) >= 4 and not direct_copies
                          and bool(parent_valid.all()) and not bool(ambiguous.any())
                          and not bool(invalid_reasons.any()))
    result = {
        "source": {"archive": "pu2023_csv.zip", "member": "pu2023.csv", "member_bytes": member.file_size,
                   **source_hashes},
        "selected_columns": FIELDS,
        "metadata": {field: {"label": metadata[field]["label"], "dtype": metadata[field]["dtype"]} for field in FIELDS},
        "rows": {"all_months": total, "month_12": len(month), "eligible": len(eligible),
                 "hospitalized": int(parent.gt(0).sum()), "invalid_parent": int((~parent_valid).sum()),
                 "ambiguous_reason_missing": int(ambiguous.sum()), "invalid_reason": int(invalid_reasons.sum())},
        "raw_values": {field: _counts(eligible[field]) for field in ["THHLDSTATUS", "TAGE_EHC", "THOSPNIT", *FLAGS, *GIVEN, *REASONS]},
        "reason_values": child_values,
        "flag_value_crosstabs": flag_crosstabs,
        "parent_reason_crosstab": {
            field: {str(k): int(v) for k, v in eligible.groupby(["THOSPNIT", field], dropna=False).size().items()}
            for field in REASONS
        },
        "contradictions": contradictions,
        "candidate_target_copy": candidate_copies,
        "person_repetition": _counts(person_counts.astype(str)),
        "households": {"eligible_households": len(household_size), "multiple_person": int(household_size.gt(1).sum()),
                       "max_people": int(household_size.max()) if len(household_size) else 0},
        "roles": {"all_month_12": role_counts, "eligible": role_eligible,
                  "hospitalized": role_hospitalized, "sample_unit_role_overlap": group_overlap},
        "technical_gate": {"eligible": technical_eligible, "usable_given": usable_given,
                           "direct_candidate_copies": direct_copies},
        "verdict": "pending_public_missing_semantics" if technical_eligible else "fail_technical_gate",
        "verdict_reason": "Public blank/flag mapping requires independent interpretation of observed cross-tabs.",
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    month.to_parquet(EXTRACT, index=False)
    MANIFEST.write_text(json.dumps({"month": 12, "person_namespace": "A014-person-v1",
                                    "sample_unit_namespace": "A014-household-v1", "roles": role_counts,
                                    "extract_sha256": _digest(EXTRACT)}, indent=2), encoding="utf-8")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"rows": result["rows"], "verdict": result["verdict"]}))
    return result


if __name__ == "__main__":
    run()
