from __future__ import annotations

import re

_SEPARATOR_RUN = re.compile(r"[^A-Za-z0-9]+")


def normalize_key(value: str) -> str:
    text = _SEPARATOR_RUN.sub("_", value.strip())
    return text.strip("_").lower()
