# cocoder-experiment

A small Python target for engineering-research experiments.

## Goal

Improve the throughput of `normalize_key()` while preserving its behavior.

The function converts human-facing field names into stable ASCII-style keys:

- trim leading/trailing separators and whitespace
- lowercase ASCII letters
- collapse each run of non-alphanumeric characters to a single underscore
- preserve digits

Examples:

```text
User-ID          -> user_id
 account number  -> account_number
HTTP Status      -> http_status
Version 2 Name   -> version_2_name
```

## Setup

```bash
python -m pip install -e .[test]
pytest -q
python benchmark/run_dev.py
```

`benchmark/run_dev.py` prints a machine-readable JSON object containing `latency_ms`, `case_count`, `iterations`, and `checksum`.

## Engineering task

Optimize `src/cocoder_experiment/matcher.py` for the development benchmark without changing the documented behavior or breaking the visible test suite.
