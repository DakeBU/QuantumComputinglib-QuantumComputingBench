#!/usr/bin/env python3
"""Check author integrity only. Does not inspect independent results or admit work."""
import argparse
import json
import runpy
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ap=argparse.ArgumentParser()
ap.add_argument("--repo",type=Path,required=True)
ap.add_argument("--out",type=Path,default=Path(__file__).resolve().parent)
args=ap.parse_args()
scope=runpy.run_path(str(args.out/"author-package-build.py"),run_name="author_selftest_import")
print(json.dumps(scope["verify"](args.repo.resolve(),args.out.resolve()),ensure_ascii=False,indent=2))
