#!/usr/bin/env python3
"""Read-only corrected entrypoint; frozen original artifacts are not resealed.

The original checker adapter lacked __fspath__, causing TypeError during
unchanged binding_digest replay. This process-local adapter supplies only the
canonical repository path; it changes no binding function, data or artifact.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
EXPECTED_V1 = "dd48ed2bba56a633f179bf3ee65a936b0d3357abb08c3b1ba8bda557cdbca047"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    original = args.out.resolve() / "verify-author-package.py"
    assert hashlib.sha256(original.read_bytes()).hexdigest() == EXPECTED_V1
    spec = importlib.util.spec_from_file_location("c31_frozen_readonly_verify", original)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.Overlay.__fspath__ = lambda self: str(self.repo)
    result = module.verify(args.repo.resolve(), args.out.resolve())
    result["verifier_entrypoint"] = "verify-author-package-v2.py"
    result["frozen_v1_failure"] = "IMPLEMENTATION_FAILED: missing Overlay.__fspath__; corrected process-locally, no artifact reseal."
    print(json.dumps(result, ensure_ascii=False, indent=2))
