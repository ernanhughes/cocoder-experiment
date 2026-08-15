from __future__ import annotations

import re


def normalize_key(value: str) -> str:
    """Normalize a human-facing field name into a stable ASCII-style key.

    This baseline is intentionally straightforward rather than optimized. The
    engineering task for this repository is to improve its throughput without
    changing the documented behavior.
    """

    text = value.strip()
    text = re.compile(r"[^A-Za-z0-9]+").sub("_", text)
    text = re.compile(r"_+").sub("_", text)
    text = re.compile(r"^_+").sub("", text)
    text = re.compile(r"_+$").sub("", text)
    return text.lower()
