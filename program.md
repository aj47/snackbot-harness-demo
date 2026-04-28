# Program: SnackBot Route Optimizer

## Objective

Improve SnackBot's delivery route by editing `strategy.py`.

SnackBot starts at `city["start"]`, visits order locations, and earns points for delivering high-tip snacks quickly. The route is a list of order IDs.

## Primary metric

Maximize `score` from:

```bash
python eval.py
```

Higher is better.

## Secondary metrics

The evaluator also reports:

- `delivered`
- `travel_steps`
- `late_orders`
- `deadline_bonus`
- `constraints_passed`
- `runtime_ms`

## Editable surface

You may edit only:

- `strategy.py`

## Forbidden changes

Do not edit:

- `eval.py`
- `run_attempt.py`
- `freeze_baseline.py`
- `data/*`
- `baselines/*`
- `logs/*`
- `examples/*`
- `README.md`
- `program.md`

## Forbidden behavior inside `strategy.py`

Do not:

- read or write files
- import network, subprocess, multiprocessing, or OS modules
- hardcode a complete route for the eval set
- hardcode order IDs as a lookup table
- call external APIs
- use randomness without a fixed seed
- modify inputs in a way that breaks future calls

## Allowed behavior

You may implement any deterministic routing heuristic inside `strategy.py`, including:

- nearest-neighbor routing
- value-per-distance scoring
- deadline urgency
- max-step awareness
- dropping low-value far orders
- 1-step or 2-step lookahead
- local swaps / route improvement

Use only Python standard library modules that are safe and deterministic, such as `math`, `itertools`, `collections`, and `functools`.

## Attempt budget

For the workshop, target:

- 20–50 attempts
- 10 minutes total
- stop after 8 attempts without improvement

## Keep / revert / stop rules

Keep an attempt if:

- constraints pass
- score improves over the best previous score
- runtime remains under the evaluator timeout

Revert if:

- score regresses
- constraints fail
- invalid route penalties appear
- runtime times out

Stop if:

- budget is exhausted
- no improvement after 8 attempts
- the same kind of failed edit repeats

## Logging format

After every attempt, run:

```bash
python run_attempt.py --once --note "short description"
```

This appends a row to `logs/progress.md`.
