"""Behavioral invariants for the bounded A014 public-data audit."""

import pandas as pd
import pytest

from scripts.audit_a014_sipp import assign_roles, encode_reasons, validate_unique


def test_duplicate_person_month_rejected():
    frame = pd.DataFrame({"SSUID": ["s", "s"], "PNUM": ["1", "1"], "MONTHCODE": ["12", "12"]})
    with pytest.raises(ValueError, match="duplicate person-month"):
        validate_unique(frame)


def test_roles_survive_row_reorder_and_keep_sample_unit_together():
    frame = pd.DataFrame({"SSUID": ["a", "a", "b", "c"], "PNUM": ["1", "2", "1", "1"]})
    first = assign_roles(frame, grouped=True).tolist()
    reordered = assign_roles(frame.iloc[[3, 1, 0, 2]], grouped=True).tolist()
    assert first[0] == first[1]
    assert reordered == [first[i] for i in [3, 1, 0, 2]]
    assert set(first) <= {"fit", "calibration", "oracle", "selection", "audit"}


def test_ambiguous_missing_reason_rejected():
    frame = pd.DataFrame({"AHREASON": ["1"], "EHREAS_DT": [""]})
    with pytest.raises(ValueError, match="ambiguous missing"):
        encode_reasons(frame)


def test_answered_child_retained_despite_parent_contradiction():
    frame = pd.DataFrame({"THOSPNIT": ["0"], "AHREASON": ["0"], "EHREAS_DT": ["1"]})
    encoded = encode_reasons(frame)
    assert encoded.loc[0, "EHREAS_DT"] == "1"


def test_literal_zero_reason_is_not_invented_answer():
    frame = pd.DataFrame({"AHREASON": ["1"], "EHREAS_DT": ["0"]})
    with pytest.raises(ValueError, match="invalid reason"):
        encode_reasons(frame)


def test_blank_person_key_rejected():
    frame = pd.DataFrame({"SSUID": [""], "PNUM": ["1"], "MONTHCODE": ["12"]})
    with pytest.raises(ValueError, match="blank person-month"):
        validate_unique(frame)
