"""Non-mutating replay of frozen C22 sources; generate a new parent receipt.

Imports use the explicitly bound inherited cache order. No source or previous
receipt is rewritten, and no new olean is emitted. This is not a clean build.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    manifest_path = HERE / "final-binding-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    pins = {}
    for rel, expected in manifest["artifact_hashes"].items():
        pins[HERE / rel] = expected
    for rel, expected in manifest["ignored_cache_hashes"].items():
        pins[HERE / rel] = expected
    for key in ("accepted_inherited_source_equality",):
        for rel, expected in manifest[key].items():
            pins[ROOT / rel] = expected
    for key in ("sources", "frozen_c19_c20_c21"):
        for rel, expected in manifest["pre_gate_bindings"][key].items():
            pins[ROOT / rel] = expected
    pins[manifest_path] = digest(manifest_path)

    def verify():
        for path, expected in pins.items():
            assert path.is_file(), "A bound input is missing"
            assert digest(path) == expected, "A bound input changed: " + path.relative_to(ROOT).as_posix()

    verify()
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(str(ROOT / "experiments/hermite-polynomial/precision" / p) for p in (
        "piecewise-kernel-stored-c22/.cache", "piecewise-kernel-assembly-c21/.cache",
        "piecewise-kernel-producer/.cache", "piecewise-kernel-uniform-c20/.cache"))
    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=ROOT, env=env,
                             capture_output=True, text=True, encoding="utf-8")
    assert version.returncode == 0 and "version 4.33.0" in version.stdout
    records = []
    for name in ("RationalBlocks", "StoredProducer", "AccountedTraffic", "StoredConsumerChecks"):
        source = HERE / (name + ".lean")
        proc = subprocess.run(["lake", "env", "lean", source.relative_to(ROOT).as_posix()],
                              cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
        output = (proc.stdout + proc.stderr).replace(str(ROOT), ".").replace(ROOT.as_posix(), ".")
        log_path = HERE / ("parent-v1-" + name + ".log")
        assert not log_path.exists(), "Do not overwrite a prior replay"
        log_path.write_text(output, encoding="utf-8", newline="\n")
        reports = re.findall(r"depends on axioms: \[([^\]]*)\]", output)
        ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", r)) <=
                       {"propext", "Classical.choice", "Quot.sound"} for r in reports)
        record = {"source": source.relative_to(ROOT).as_posix(), "source_sha256": digest(source),
                  "exit": proc.returncode, "axiom_reports": len(reports),
                  "ordinary_axioms_only": ordinary, "log": log_path.name,
                  "log_sha256": digest(log_path)}
        records.append(record)
        print(json.dumps(record), flush=True)
        assert proc.returncode == 0 and ordinary and reports
    verify()
    assert sum(r["axiom_reports"] for r in records) == 14
    result = {"status": "FOCUSED_PARENT_REPLAY_PASS", "lean_version": version.stdout.strip(),
              "manifest_sha256": pins[manifest_path], "bound_inputs_checked_pre_post": len(pins),
              "fresh_source_elaborations": records, "source_or_cache_mutation": False,
              "inherited_imports": "Explicit C22/C21/C19/C20 cache order; not rebuilt wholesale",
              "consumerchecks_resolution": manifest["pre_gate_bindings"]["consumerchecks_resolution"],
              "full_repository_gate": False, "full_runtime_certified": False,
              "independent_publication_admission": False, "scientific_ROOT": False}
    receipt = HERE / "parent-verification-v1.json"
    assert not receipt.exists(), "Do not overwrite a prior receipt"
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt_sha256": digest(receipt), "status": result["status"]}))


if __name__ == "__main__":
    run()
