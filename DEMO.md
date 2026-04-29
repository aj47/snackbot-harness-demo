# SnackBot Comparison Demo: One-Shot Prompt vs Autoresearch Harness

This demo compares two ways of using an agent on the same task:

1. **Single agent prompt** — one best-effort edit to `strategy.py`.
2. **Autoresearch harness** — many small edit/eval/keep-or-revert loops in under 5 minutes.

The point is not that the model is smarter in the second version. The point is that the harness gives it a measurable loop, evidence, and safe rollback.

## Reset before each run

```bash
cd /Users/ajjoobandi/Development/snackbot-harness-demo
cp examples/baseline_strategy.py strategy.py
rm -f .strategy.best.py
python3 freeze_baseline.py
python3 eval.py
```

Baseline expected score is about `132`.

## Run A: single agent prompt

Reset, then give the agent:

```text
prompts/single_agent_prompt.md
```

The agent should make one edit and run:

```bash
python3 run_attempt.py --once --note "single agent one-shot"
```

Record:

- score
- delivered count
- late orders
- constraints pass/fail
- whether it was kept or reverted

## Run B: autoresearch harness

Reset again, then give the agent:

```text
prompts/autoresearch_harness_prompt.md
```

The agent should loop for less than 5 minutes. Each attempt runs:

```bash
python3 run_attempt.py --once --revert --note "hypothesis name"
```

Record:

- best score
- number of attempts
- best heuristic
- progress log rows as evidence

## Fast scripted smoke test

To prove the harness can distinguish strategies:

```bash
cp examples/baseline_strategy.py strategy.py
python3 run_attempt.py --once --note "baseline"

cp examples/bad_overfit_strategy.py strategy.py
python3 run_attempt.py --once --revert --note "bad tip-only one-shot"

cp examples/improved_strategy.py strategy.py
python3 run_attempt.py --once --revert --note "generic improved heuristic"
```

Known result from repo creation: improved example scored about `273`, while baseline scored about `132`.

## Suggested talk track

- One-shot prompting asks for a good answer once.
- Harnessing asks for a measurable process.
- The harness narrows the editable surface to `strategy.py`.
- The evaluator turns subjective progress into a score.
- The log creates receipts.
- The revert rule lets the agent explore without permanently breaking the repo.
- In under 5 minutes, the harness can try many ideas and keep only the winner.
