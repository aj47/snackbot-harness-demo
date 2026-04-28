#!/usr/bin/env python3
"""Freeze the current strategy.py score as the workshop baseline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from eval import evaluate

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "baselines" / "baseline.json"


def main() -> None:
    result = evaluate("eval")
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **result,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
