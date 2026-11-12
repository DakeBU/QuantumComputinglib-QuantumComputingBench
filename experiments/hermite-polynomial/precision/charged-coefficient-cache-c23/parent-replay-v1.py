"""Re-elaborate the frozen C23 sources without changing any frozen import output."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest_path = HERE / "final-binding-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pins = {HERE / name: expected for name, expected in manifest["artifact_hashes"].items()}
    pins.update({HERE / name: expected for name, expected in manifest["ignored_private_cache_hashes"].items()})
    for key in ("selected_direct_imports_and_companions_at_freeze", "selected_import_source_snapshots_at_freeze"):
        pins.update({ROOT / name: expected for name, expected in manifest[key].items()})
    pins.update({ROOT / name: expected for name, expected in
                 manifest["pre_gate_bindings"]["sources_and_inherited_cache_pins"].items()})
    pins[manifest_path] = sha(manifest_path)

    def verify():
        for path, expected in pins.items():
            assert path.is_file() and sha(path) == expected, "Bound input changed: " + path.relative_to(ROOT).as_posix()

    verify()
    prefix = subprocess.run(["lake", "env", "lean", "--print-prefix"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8", check=True)
    binary = Path(prefix.stdout.strip()) / "bin/lean.exe"
    assert sha(binary) == manifest["pre_gate_bindings"]["lean_executable_sha256"]
    packages = subprocess.run(["lake", "env", "powershell", "-NoProfile", "-Command", "$env:LEAN_PATH"],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    priority = manifest["pre_gate_bindings"]["lean_path_priority"]
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join([str(ROOT / name) for name in priority] + [packages.stdout.strip()])
    version = subprocess.run([str(binary), "--version"], cwd=ROOT, env=env,
                             capture_output=True, text=True, encoding="utf-8", check=True)
    assert "version 4.33.0" in version.stdout
    records = []
    for name, expected_reports, needed in (
        ("ChargedSourceCache", 6, ("ActualCoefficients", "QuantumBlockEncoding/StoredGivens")),
        ("CacheConsumerChecks", 4, ("ChargedSourceCache", "QuantumBlockEncoding/StoredHermiteCoefficients")),
    ):
        verify()
        source = (HERE / (name + ".lean")).relative_to(ROOT).as_posix()
        deps = subprocess.run([str(binary), "--deps", source], cwd=ROOT, env=env,
                              capture_output=True, text=True, encoding="utf-8", check=True)
        selected = []
        for line in deps.stdout.splitlines():
            path = Path(line.strip())
            if not line.strip().endswith(".olean"):
                continue
            if not path.is_absolute():
                path = ROOT / path
            path = path.resolve()
            if path.is_relative_to(ROOT):
                relative = path.relative_to(ROOT).as_posix()
            else:
                relative = "[lean-toolchain]/lib/lean/" + path.as_posix().split("/lib/lean/", 1)[1]
            selected.append({"cache": relative, "sha256": sha(path)})
        for module in needed:
            expected = priority[0] + "/" + module + ".olean"
            assert any(row["cache"] == expected for row in selected), "Unexpected direct provider: " + module
        proc = subprocess.run([str(binary), source], cwd=ROOT, env=env,
                              capture_output=True, text=True, encoding="utf-8")
        output = (proc.stdout + proc.stderr).replace(str(ROOT), ".").replace(ROOT.as_posix(), ".")
        log = HERE / ("parent-v1-" + name + ".log")
        assert not log.exists(), "Never overwrite earlier replay logs"
        log.write_text(output, encoding="utf-8", newline="\n")
        reports = re.findall(r"depends on axioms: \[([^\]]*)\]", output)
        ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", item)) <=
                       {"propext", "Classical.choice", "Quot.sound"} for item in reports)
        record = {"source": source, "source_sha256": sha(ROOT / source), "exit": proc.returncode,
                  "axiom_reports": len(reports), "ordinary_axioms_only": ordinary,
                  "log": log.name, "log_sha256": sha(log), "selected_imports": selected}
        records.append(record)
        print(json.dumps({key: record[key] for key in ("source", "exit", "axiom_reports", "ordinary_axioms_only")}), flush=True)
        assert proc.returncode == 0 and ordinary and len(reports) == expected_reports
        verify()
    receipt = {"status": "PARENT_FROZEN_SOURCE_REPLAY_PASS", "lean_version": version.stdout.strip(),
               "manifest_sha256": sha(manifest_path), "records": records,
               "pre_post_bound_inputs": len(pins), "symbolic_axiom_reports": 10,
               "ordinary_axioms_only": True, "fresh_target_source_elaborated": True,
               "new_olean_emitted": False, "clean_transitive_rebuild": False,
               "import_scope": "Exact frozen fresh-v3 project providers; inherited Mathlib and C19/C20/C21 providers remain explicitly bound.",
               "independent_review": False, "main_admission": False, "scientific_ROOT": False,
               "full_runtime": False, "finite_bit_GCD_bound": False}
    out = HERE / "parent-verification-v1.json"
    assert not out.exists(), "Never overwrite earlier replay receipts"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": receipt["status"], "receipt_sha256": sha(out), "pre_post_bound_inputs": len(pins)}))


if __name__ == "__main__":
    main()
