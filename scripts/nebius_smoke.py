"""Compatibility entry point for the strictly one-request Nebius evaluation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nebius_once import run_once

if __name__ == "__main__":
    try:
        result = run_once()
        print("One-request evaluation:", result["status"], "— see local evidence/nebius-run.json")
        raise SystemExit(0 if result["status"] == "completed" else 1)
    except RuntimeError as exc:
        raise SystemExit(str(exc))
