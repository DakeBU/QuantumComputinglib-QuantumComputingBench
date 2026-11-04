"""Independent response-artifact grader; never execute submitted code."""
import json
import sys
from pathlib import Path

from qcb_bench_runtime import read_jsonl, score

root = Path(__file__).resolve().parent
try:
    registry = json.loads((root / "registry.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    report = score(registry, manifest, read_jsonl(sys.argv[1]), read_jsonl(sys.argv[2]) if len(sys.argv) > 2 else [])
    print(json.dumps(report, indent=2))
except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
    print("GRADING_PROTOCOL_ERROR: " + str(error), file=sys.stderr)
    raise SystemExit(1) from error
