#!/usr/bin/env python3
"""Export train-only checked whole-root Lean supervision; never launch training."""
import argparse
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import write_json
from qcb_course_registry import load_course_registry
from qcb_course_training import export_training, reference_records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh output; previous exports are preserved")
        views, qualification = load_course_registry()
        result = export_training(views, qualification, reference_records())
        write_json(args.output, result, immutable=True)
        print(json.dumps({"output": str(args.output), "distinct_train_cores": result["distinct_shared_cores"],
                          "training_launched": False}))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
