"""V2 corrects actual import priority without changing the mathematical route."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import shutil
import replay

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / ".cache" / "fresh-v3"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert not OUT.exists(), "Do not overwrite a prior private cache"
    prefix = subprocess.run(["lake", "env", "lean", "--print-prefix"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8")
    packages = subprocess.run(["lake", "env", "powershell", "-NoProfile", "-Command", "$env:LEAN_PATH"],
                              cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert prefix.returncode == 0 and packages.returncode == 0
    binary = Path(prefix.stdout.strip()) / "bin" / "lean.exe"
    assert binary.is_file()
    env = os.environ.copy()
    inherited = [ROOT / "experiments/hermite-polynomial/precision" / d / ".cache"
                 for d in ("piecewise-kernel-assembly-c21", "piecewise-kernel-producer", "piecewise-kernel-uniform-c20")]
    env["LEAN_PATH"] = os.pathsep.join([str(OUT), *[str(p) for p in inherited], packages.stdout.strip()])
    OUT.mkdir(parents=True)
    # Lean selects namespace roots, not a missing-file fallback per module.
    # Copy the complete project namespace so every fresh provider can be loaded.
    shutil.copytree(ROOT / ".lake/build/lib/lean/QuantumBlockEncoding", OUT / "QuantumBlockEncoding")

    def invoke(args):
        return subprocess.run([str(binary), *args], cwd=ROOT, env=env, capture_output=True,
                              text=True, encoding="utf-8")

    pins = json.loads((HERE / "pre-gate-bindings.json").read_text(encoding="utf-8"))["sources_and_inherited_cache_pins"]
    pins[(HERE / "replay-v3.py").relative_to(ROOT).as_posix()] = digest(HERE / "replay-v3.py")
    pins[(HERE / "focused-verification-v1.json").relative_to(ROOT).as_posix()] = digest(HERE / "focused-verification-v1.json")
    extra_pins = {}

    def verify():
        for rel, expected in pins.items():
            assert digest(ROOT / rel) == expected, "Bound input changed: " + rel
        for p, expected in extra_pins.items():
            assert digest(p) == expected, "Actual selected import changed: " + replay.label(p)

    version = invoke(["--version"])
    assert version.returncode == 0 and "version 4.33.0" in version.stdout
    pre = HERE / "pre-gate-bindings-v3.json"
    assert not pre.exists()
    pre.write_text(json.dumps({"sources_and_inherited_cache_pins": pins,
        "lean_executable_sha256": digest(binary), "lean_path_priority": [replay.label(OUT), *[replay.label(p) for p in inherited]],
        "library_tail": "Resolved lake package paths, behind explicit private paths",
        "correction": "Direct toolchain binary; complete copied project namespace before selected fresh source gates. Mathlib Cast freshly gated in isolation but inherited Mathlib cache intentionally consumed.",
        "not_clean_transitive_rebuild": True}, indent=2) + "\n", encoding="utf-8")
    records = []
    for rel, module in replay.PROVIDERS:
        verify()
        dep = invoke(["--deps", rel])
        assert dep.returncode == 0
        imports = []
        for line in dep.stdout.splitlines():
            if not line.strip().endswith(".olean"):
                continue
            p = Path(line.strip())
            if not p.is_absolute():
                p = ROOT / p
            p = p.resolve()
            assert p.is_file()
            imports.append({"selected_cache": replay.label(p), "sha256": digest(p)})
            extra_pins[p] = digest(p)
            for suffix in (".private", ".server"):
                companion = Path(str(p) + suffix)
                if companion.is_file():
                    extra_pins[companion] = digest(companion)
        for needed in {"ChargedSourceCache": ["ActualCoefficients", "QuantumBlockEncoding/StoredGivens"],
                       "CacheConsumerChecks": ["ChargedSourceCache", "QuantumBlockEncoding/StoredHermiteCoefficients"]}.get(module, []):
            expected = replay.label(OUT / (needed + ".olean"))
            assert any(i["selected_cache"] == expected for i in imports), "Fresh provider not selected: " + needed
        target = OUT / (module + ".olean")
        if module.startswith("Mathlib/"):
            target = OUT / "isolated-mathlib" / (module + ".olean")
        target.parent.mkdir(parents=True, exist_ok=True)
        proc = invoke(["-o", str(target), rel])
        output = replay.clean(proc.stdout + proc.stderr)
        log = HERE / ("fresh-v3-" + module.replace("/", "-") + ".log")
        assert not log.exists()
        log.write_text(output, encoding="utf-8", newline="\n")
        reports = re.findall(r"depends on axioms: \[([^\]]*)\]", output)
        ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", r)) <=
                       {"propext", "Classical.choice", "Quot.sound"} for r in reports)
        rec = {"source": rel, "source_sha256": digest(ROOT / rel), "exit": proc.returncode,
               "log": log.name, "log_sha256": digest(log), "axiom_reports": len(reports),
               "ordinary_axioms_only": ordinary, "selected_direct_imports": imports}
        if target.is_file():
            rec.update({"fresh_cache": replay.label(target), "fresh_cache_sha256": digest(target)})
        records.append(rec)
        print(json.dumps(rec), flush=True)
        assert proc.returncode == 0 and ordinary
        verify()
    receipt = HERE / "focused-verification-v3.json"
    assert not receipt.exists()
    result = {"status": "FOCUSED_FRESH_SOURCE_GATE_PASS", "lean_version": version.stdout.strip(),
        "records": records, "bound_inputs_checked_pre_post": len(pins) + len(extra_pins),
        "pre_gate_bindings_sha256": digest(pre), "core_axiom_reports": records[-2]["axiom_reports"],
        "consumer_axiom_reports": records[-1]["axiom_reports"], "actual_private_project_provider_selection_verified": True,
        "mathlib_cast_scope": "Fresh source elaboration in isolated private output; consumers use inherited Mathlib cache, no transitive freshness claim",
        "selected_import_and_companion_pins": {replay.label(p): h for p, h in extra_pins.items()},
        "clean_transitive_rebuild": False, "full_repository_gate": False, "full_documentation_gate": False,
        "independent_review": "PENDING", "scientific_ROOT": False,
        "resource_boundary": "Exact rational scalar/word counters; not bitlength/GCD/full C22 runtime"}
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt_sha256": digest(receipt), "status": result["status"]}), flush=True)


if __name__ == "__main__":
    run()
