#!/usr/bin/env python3
"""Inspect the Lean evaluation frontier or export answer-free existing warmups."""
import argparse
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_agentic import audit_catalog, export_warmups
from qcb_core import write_json
from qcb_curriculum import load_catalog


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=("audit", "export-warmups"))
    p.add_argument("--output", type=Path)
    p.add_argument("--split", choices=("train", "dev", "test_public"))
    args = p.parse_args()
    try:
        if args.command == "audit" and args.split:
            raise ValueError("audit covers the whole catalog; --split is for export-warmups")
        if args.output and args.output.exists():
            raise FileExistsError("choose a fresh output path; prior evidence is preserved")
        catalog, items, _ = load_catalog()
        result = (audit_catalog(catalog) if args.command == "audit"
                  else export_warmups(catalog, items, split=args.split))
        if args.output:
            write_json(args.output, result, immutable=True)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
