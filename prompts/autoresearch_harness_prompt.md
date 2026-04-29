# Autoresearch Harness Prompt: SnackBot 5-Minute Loop

You are running an autoresearch loop to improve SnackBot's route planning.

Read `README.md`, `program.md`, current `strategy.py`, and `logs/progress.md`.

You have less than 5 minutes. Run many small experiments. Each experiment must edit only `strategy.py`, test one clear hypothesis, and then evaluate with:

```bash
python3 run_attempt.py --once --revert --note "short hypothesis name"
```

Goal: maximize the score from `python3 eval.py` while keeping constraints passing.

Hard rules:

- Edit only `strategy.py`.
- Do not edit data, evaluator, logs except via `run_attempt.py`, examples, README, or program files.
- Do not hardcode the eval route or use order-ID lookup tables.
- Do not read/write files, call external APIs, use subprocess/network/OS modules, or use randomness without a fixed seed.
- Use deterministic generic routing heuristics.
- Keep winners, revert losers using the harness evidence.

Loop:

1. Inspect the current best score from `logs/progress.md`.
2. Make one small strategy change.
3. Run `python3 run_attempt.py --once --revert --note "..."`.
4. If score improved and constraints passed, keep it as the new best.
5. If it regressed or failed constraints, let `--revert` restore the previous best.
6. Try a different hypothesis.
7. Stop when 5 minutes is nearly up, after 8 attempts without improvement, or after 20-50 attempts.

Good hypotheses to try:

- value per travel step
- deadline urgency
- late penalty avoidance
- max-step budget awareness
- dropping far low-value orders
- two-step lookahead
- local adjacent swaps
- balancing tip, distance, deadline, and remaining budget

Final response: report best score, number of attempts, best heuristic, and cite `logs/progress.md` as evidence.
