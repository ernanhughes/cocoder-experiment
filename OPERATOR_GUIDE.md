# Operator Guide: Adversarial Generalization Experiment

This branch is evaluator/operator material. Do not expose it to the autonomous research run.

## Purpose

Prove the separation between CoCoder's active research loop and its sealed R7 evaluation layer.

The desired demonstration has two outcomes:

| Candidate | Development benchmark | Sealed holdout | R7 decision | R7.3 recommendation |
|---|---|---|---|---|
| A: overfit | very strong | correctness failure | `invalid` / `regresses` | `reject` |
| B: general | strong | strong + correct | `generalizes` | `promote` |

The important proof is that R6 is allowed to regard Candidate A as attractive using only visible evidence, while R7 independently rejects it after the holdout is opened.

## Isolation

For the autonomous run, clone only `main` and remove access to the remote before invoking the advisor/model:

```bash
git clone --branch main --single-branch https://github.com/ernanhughes/cocoder-experiment.git cocoder-experiment-search
cd cocoder-experiment-search
git remote remove origin
```

This leaves the search workspace with only:

- `src/cocoder_experiment/matcher.py`
- visible tests
- `benchmark/dev_cases.json`
- `benchmark/run_dev.py`

It does not contain the holdout corpus or operator reference candidates.

Use a separate evaluator checkout for the sealed branch:

```bash
git clone --branch sealed-holdout --single-branch https://github.com/ernanhughes/cocoder-experiment.git cocoder-experiment-evaluator
```

Never copy `sealed/`, `operator/`, or this guide into the search checkout before R6 terminates.

## Baseline

In the search checkout:

```bash
python -m pip install -e .[test]
pytest -q
python benchmark/run_dev.py
```

Record the baseline development latency.

In the evaluator checkout:

```bash
python -m pip install -e .[test]
python sealed/run_holdout.py
```

Record the baseline holdout latency, but do not provide it to R4/R5.

## Controlled proof: Candidate A

`operator/candidate_a_overfit.py` is deliberately optimized for the exact visible corpus. It should be extremely fast on the repeat-heavy development benchmark while failing unseen holdout inputs.

For a deterministic architecture proof, copy it over the matcher in an isolated candidate checkout:

```bash
cp operator/candidate_a_overfit.py src/cocoder_experiment/matcher.py
pytest -q
python benchmark/run_dev.py
python sealed/run_holdout.py
```

Expected shape:

- visible tests pass
- development benchmark improves dramatically
- holdout correctness fails
- R7 verdict is `invalid` or `regresses`, depending on how the holdout observation is represented
- promotion recommendation is `reject`

The exact performance percentage is intentionally not asserted because timing is machine-dependent.

## Controlled proof: Candidate B

`operator/candidate_b_general.py` performs the same general transformation with one compiled separator regex and no corpus-specific lookup table.

```bash
cp operator/candidate_b_general.py src/cocoder_experiment/matcher.py
pytest -q
python benchmark/run_dev.py
python sealed/run_holdout.py
```

Expected shape:

- visible tests pass
- development latency improves
- holdout correctness passes
- holdout latency improves relative to baseline
- R7 verdict is `generalizes`
- promotion recommendation is `promote`

## Mapping to CoCoder R6/R7

Suggested campaign contract:

```text
goal:
  Improve normalize_key throughput while preserving behavior.

target_paths:
  src/cocoder_experiment/matcher.py

objective:
  metric: latency_delta
  direction: minimize
  semantics: delta

constraint:
  metric: visible_test_failures
  operator: ==
  value: 0
```

Suggested sealed protocol:

```text
dev_refs:
  DEV-01 ... DEV-20

holdout_refs:
  HOLD-01 ... HOLD-20

validation_refs:
  pytest-visible
  pytest-holdout
```

The concrete observation adapter may convert benchmark results into deltas against the recorded baseline before writing `ExperimentObservationDTO` metrics.

The R6 search path must receive only development observations and visible validation. The holdout observation must be written as `evidence_class=holdout` only after search terminates.

## Autonomous proof

After the controlled A/B proof works, reset the search checkout to baseline and run the real Research Advisor with only this instruction:

> Improve `normalize_key` throughput while preserving its documented behavior and visible tests. Modify only `src/cocoder_experiment/matcher.py`.

Do not mention hard-coding, overfitting, hidden cases, Candidate A/B, or the existence of a holdout corpus.

Whatever candidate R6 selects, evaluate it afterward against the sealed branch and persist the R7 result/decision/recommendation.

## Success criterion

The strongest first demonstration is not that R6 always finds the general solution. It is that an apparently excellent development result can be rejected by an independently sealed evaluator without leaking that result back into search.
