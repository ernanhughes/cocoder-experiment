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
    payload = json.loads((ROOT / "sealed" / "holdout_cases.json").read_text(encoding="utf-8"))
    return [(str(value), str(expected)) for value, expected in payload]


def main() -> int:
    cases = _load_cases()
    iterations = int(os.environ.get("COCODER_EXPERIMENT_ITERATIONS", "50000"))

    failures: list[dict[str, str]] = []
    for value, expected in cases:
        try:
            actual = normalize_key(value)
        except Exception as exc:  # evaluator records candidate failure rather than crashing
            failures.append({"value": value, "expected": expected, "error": repr(exc)})
            continue
        if actual != expected:
            failures.append({"value": value, "expected": expected, "actual": actual})

    if failures:
        print(
            json.dumps(
                {
                    "valid": False,
                    "case_count": len(cases),
                    "correct_cases": len(cases) - len(failures),
                    "failed_cases": len(failures),
                    "failures": failures,
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
