# Single Agent Prompt: SnackBot One-Shot

You are improving SnackBot's route planning.

Read `README.md` and `program.md`, then make exactly one best-effort edit to `strategy.py` only.

Goal: maximize the score from:

```bash
python3 eval.py
```

Rules:

- Edit only `strategy.py`.
- Do not edit data, evaluator, logs, examples, README, or program files.
- Do not hardcode the eval route or use order-ID lookup tables.
- Do not read/write files, call external APIs, use subprocess/network/OS modules, or use randomness without a fixed seed.
- Use a deterministic generic routing heuristic.

After editing, run:

```bash
python3 run_attempt.py --once --note "single agent one-shot"
```

Stop after that one attempt and report the score, decision, and what heuristic you tried.
