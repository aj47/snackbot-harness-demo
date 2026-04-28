#!/usr/bin/env python3
"""Attempt logger and keep/revert helper for SnackBot.

This script does not call an agent. It evaluates the current strategy.py, compares
it with prior logged attempts, and appends an evidence row to logs/progress.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from eval import evaluate

ROOT = Path(__file__).resolve().parent
PROGRESS = ROOT / "logs" / "progress.md"
BASELINE = ROOT / "baselines" / "baseline.json"
STRATEGY = ROOT / "strategy.py"
BACKUP = ROOT / ".strategy.best.py"

FORBIDDEN_TRACKED = {
    "README.md",
    "program.md",
    "eval.py",
    "run_attempt.py",
    "freeze_baseline.py",
    "requirements.txt",
    ".gitignore",
}
FORBIDDEN_PREFIXES = ("data/", "baselines/", "examples/")


def git_changed_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)
    except Exception:
        return []
    files: list[str] = []
    for line in out.splitlines():
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path)
    return sorted(files)


def forbidden_changes(changed: list[str]) -> list[str]:
    bad = []
    for path in changed:
        if path == "strategy.py" or path.startswith("logs/") or path == ".strategy.best.py":
            continue
        if path in FORBIDDEN_TRACKED or path.startswith(FORBIDDEN_PREFIXES):
            bad.append(path)
    return bad


def ensure_progress() -> None:
    PROGRESS.parent.mkdir(exist_ok=True)
    if not PROGRESS.exists() or not PROGRESS.read_text().strip():
        PROGRESS.write_text(
            "# SnackBot Progress\n\n"
            "| attempt | time | score | delivered | travel | late | penalty | runtime_ms | constraints | decision | note |\n"
            "|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|\n"
        )


def read_scores() -> list[int]:
    if not PROGRESS.exists():
        return []
    scores = []
    for line in PROGRESS.read_text().splitlines():
        if not line.startswith("|") or line.startswith("| attempt") or line.startswith("|---"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 3:
            try:
                scores.append(int(parts[2]))
            except ValueError:
                pass
    return scores


def load_baseline_score() -> int | None:
    if BASELINE.exists():
        try:
            return int(json.loads(BASELINE.read_text())["score"])
        except Exception:
            return None
    return None


def append_row(attempt: int, result: dict, decision: str, note: str) -> None:
    now = datetime.now(timezone.utc).strftime("%H:%M:%S")
    constraints = "pass" if result["constraints_passed"] else "fail"
    safe_note = note.replace("|", "/")[:120]
    row = (
        f"| {attempt} | {now} | {result['score']} | {result['delivered']}/{result['total_orders']} | "
        f"{result['travel_steps']} | {result['late_orders']} | {result['invalid_route_penalty']} | "
        f"{result['runtime_ms']} | {constraints} | {decision} | {safe_note} |\n"
    )
    with PROGRESS.open("a") as f:
        f.write(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="evaluate and log current strategy once")
    parser.add_argument("--note", default="", help="short attempt note")
    parser.add_argument("--revert", action="store_true", help="revert strategy.py if current attempt does not improve")
    args = parser.parse_args()

    ensure_progress()
    changed = git_changed_files()
    bad_changes = forbidden_changes(changed)
    result = evaluate("eval")
    if bad_changes:
        result["constraints_passed"] = False
        result["violations"] = sorted(set(result["violations"] + [f"forbidden file changed: {p}" for p in bad_changes]))
        result["score"] = min(int(result["score"]), -1000)

    previous_scores = read_scores()
    baseline_score = load_baseline_score()
    best_before = max(previous_scores + ([baseline_score] if baseline_score is not None else []), default=None)
    improved = result["constraints_passed"] and (best_before is None or int(result["score"]) > best_before)
    decision = "keep" if improved else "revert"

    if improved:
        shutil.copy2(STRATEGY, BACKUP)
    elif args.revert and BACKUP.exists():
        shutil.copy2(BACKUP, STRATEGY)
        decision = "reverted"

    attempt = len(previous_scores) + 1
    append_row(attempt, result, decision, args.note)

    print(json.dumps({"decision": decision, "best_before": best_before, **result}, indent=2, sort_keys=True))
    return 0 if result["constraints_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
