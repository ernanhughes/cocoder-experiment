from __future__ import annotations

import json
from pathlib import Path

import pytest

from cocoder_experiment.matcher import normalize_key


CASES = [
    tuple(item)
    for item in json.loads(
        (Path(__file__).resolve().parents[1] / "benchmark" / "dev_cases.json").read_text(
            encoding="utf-8"
        )
    )
]


@pytest.mark.parametrize(("value", "expected"), CASES)
def test_visible_normalization_cases(value: str, expected: str) -> None:
    assert normalize_key(value) == expected


def test_empty_and_separator_only_values() -> None:
    assert normalize_key("") == ""
    assert normalize_key(" --- ") == ""


def test_digits_are_preserved() -> None:
    assert normalize_key("Field 123") == "field_123"
