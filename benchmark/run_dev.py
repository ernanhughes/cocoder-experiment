from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cocoder_experiment.matcher import normalize_key


def _load_cases() -> list[tuple[str, str]]:
    payload = json.loads((ROOT / "benchmark" / "dev_cases.json").read_text(encoding="utf-8"))
    return [(str(value), str(expected)) for value, expected in payload]


def main() -> int:
    cases = _load_cases()
    iterations = int(os.environ.get("COCODER_EXPERIMENT_ITERATIONS", "50000"))

    for value, expected in cases:
        actual = normalize_key(value)
        if actual != expected:
            print(
                json.dumps(
                    {
                        "valid": False,
                        "error": f"{value!r} -> {actual!r}, expected {expected!r}",
                        "case_count": len(cases),
                        "iterations": iterations,
                    },
                    sort_keys=True,
                )
            )
            return 1

    checksum = 0
    start = perf_counter()
    for _ in range(iterations):
        for value, _expected in cases:
            checksum += len(normalize_key(value))
    elapsed_ms = (perf_counter() - start) * 1000.0

    print(
        json.dumps(
            {
                "valid": True,
                "latency_ms": round(elapsed_ms, 6),
                "case_count": len(cases),
                "iterations": iterations,
                "checksum": checksum,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
