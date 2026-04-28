# SnackBot Harness Demo

A tiny hands-on repo for teaching **harness engineering**:

> Designing the system around the model so LLM work becomes reproducible, measurable, and trustworthy.

SnackBot must deliver snacks around a grid city. Your agent may only edit `strategy.py`. A fixed evaluator scores each route, logs attempts, and tells you whether to keep, revert, or stop.

## The loop

1. Define the task in `program.md`
2. Freeze the baseline
3. Give the agent a narrow editable surface: `strategy.py`
4. Run repeated attempts
5. Score each attempt with `eval.py`
6. Log results in `logs/progress.md`
7. Keep, revert, or stop based on evidence

## Quickstart

Requires Python 3.10+. No packages, no API keys, no network.

```bash
python eval.py
python freeze_baseline.py
python run_attempt.py --once
```

Then give `program.md` to an agent and tell it to improve `strategy.py` only.

Recommended workshop flow:

```bash
# 1. reset to baseline
cp examples/baseline_strategy.py strategy.py

# 2. freeze baseline
python freeze_baseline.py

# 3. let a raw agent edit strategy.py once, then score
python run_attempt.py --once --note "raw agent one-shot"

# 4. let an autoresearch-style agent repeatedly edit strategy.py
#    after each edit, run:
python run_attempt.py --once --note "harness attempt"
```

## Score

Higher is better.

```txt
score = delivered_tip_value + deadline_bonus - travel_cost - late_penalty - undelivered_penalty
```

The evaluator also reports:

- delivered orders
- travel steps
- late orders
- invalid route violations
- mean runtime

## Files

```txt
README.md
program.md                # harness contract for the agent
strategy.py               # only editable file
eval.py                   # fixed evaluator
freeze_baseline.py        # writes baselines/baseline.json
run_attempt.py            # scores current strategy and appends logs
data/city.json
data/orders_train.json    # visible practice orders
data/orders_eval.json     # fixed evaluation orders
baselines/baseline.json
logs/progress.md
examples/
```

## What this teaches

The point is not that the agent is magic. The point is that the environment is narrow, measurable, logged, and constrained.

A one-shot agent may find one reasonable heuristic. A harnessed agent can try many heuristics, measure each one, keep winners, and revert losers.
