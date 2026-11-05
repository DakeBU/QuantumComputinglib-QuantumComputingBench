"""Fresh bounded source gate, private outputs only; not a transitive rebuild."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / ".cache" / "fresh-v1"
PROVIDERS = (
    ("QuantumBlockEncoding/StoredGivens.lean", "QuantumBlockEncoding/StoredGivens"),
    (".lake/packages/mathlib/Mathlib/Data/Nat/Choose/Cast.lean", "Mathlib/Data/Nat/Choose/Cast"),
    ("experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualCoefficients.lean", "ActualCoefficients"),
    ("QuantumBlockEncoding/StoredHermiteCoefficients.lean", "QuantumBlockEncoding/StoredHermiteCoefficients"),
    ("experiments/hermite-polynomial/precision/charged-coefficient-cache-c23/ChargedSourceCache.lean", "ChargedSourceCache"),
    ("experiments/hermite-polynomial/precision/charged-coefficient-cache-c23/CacheConsumerChecks.lean", "CacheConsumerChecks"),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(path):
    path = path.resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        parts = path.as_posix().split("/lib/lean/")
        assert len(parts) == 2, "Unexpected external dependency location"
        return "[lean-toolchain]/lib/lean/" + parts[1]


def clean(text):
    return text.replace(str(ROOT), ".").replace(ROOT.as_posix(), ".")


def run():
    assert not OUT.exists(), "Never overwrite a frozen or prior gate cache"
    OUT.mkdir(parents=True)
    env = os.environ.copy()
    inherited = [ROOT / "experiments/hermite-polynomial/precision" / d / ".cache"
                 for d in ("piecewise-kernel-assembly-c21", "piecewise-kernel-producer", "piecewise-kernel-uniform-c20")]
    env["LEAN_PATH"] = os.pathsep.join(str(p) for p in [OUT, HERE / ".cache", *inherited])
    pins = {}
    for rel in ("lean-toolchain", "lake-manifest.json", "tasks/SP-HERMITE-POLY-002.md",
                "reports/process-memory.json", "AGENTS.md", "HARNESS.md",
                "docs/theorem-publication-protocol.md", "docs/proof-digestion-protocol.md",
                "docs/evidence-routed-memory-protocol.md", ".agents/skills/qbe-substantive-worker/SKILL.md",
                ".lake/packages/mathlib/Mathlib/Data/Nat/Choose/Basic.lean",
                ".lake/packages/mathlib/Mathlib/Data/Nat/Factorial/Basic.lean"):
        pins[ROOT / rel] = digest(ROOT / rel)
    for rel, _ in PROVIDERS:
        pins[ROOT / rel] = digest(ROOT / rel)
    for rel in ("statement-seal-v1.json", "statement-seal-v2.json", "replay.py"):
        pins[HERE / rel] = digest(HERE / rel)
    for directory in inherited:
        for file in directory.rglob("*"):
            if file.is_file():
                pins[file] = digest(file)
        for file in directory.parent.glob("*.lean"):
            pins[file] = digest(file)
    for rel in ("RationalBlocks.lean", "StoredProducer.lean", "AccountedTraffic.lean"):
        p = ROOT / "experiments/hermite-polynomial/precision/piecewise-kernel-stored-c22" / rel
        pins[p] = digest(p)

    def invoke(args):
        return subprocess.run(["lake", "env", "lean", *args], cwd=ROOT, env=env,
                              capture_output=True, text=True, encoding="utf-8")

    def verify():
        for path, expected in pins.items():
            assert path.is_file() and digest(path) == expected, "Bound input changed: " + label(path)

    version = invoke(["--version"])
    assert version.returncode == 0 and "version 4.33.0" in version.stdout
    verify()
    pre = HERE / "pre-gate-bindings.json"
    assert not pre.exists()
    pre.write_text(json.dumps({"sources_and_inherited_cache_pins": {label(p): h for p, h in pins.items()},
        "lean_path_order": [label(p) for p in [OUT, HERE / ".cache", *inherited]],
        "cache_resolution": "C21 finite-middle ConsumerChecks; C20 duplicate excluded by order",
        "fresh_source_scope": [rel for rel, _ in PROVIDERS],
        "not_clean_transitive_rebuild": True}, indent=2) + "\n", encoding="utf-8")
    records = []
    dependency_pins = {}
    for number, (rel, module) in enumerate(PROVIDERS):
        dep = invoke(["--deps", rel])
        assert dep.returncode == 0
        paths = []
        for line in dep.stdout.splitlines():
            if line.strip().endswith(".olean"):
                p = Path(line.strip())
                if not p.is_absolute():
                    p = ROOT / p
                p = p.resolve()
                assert p.is_file()
                dependency_pins[p] = digest(p)
                paths.append({"selected_cache": label(p), "sha256": digest(p)})
        target = OUT / (module + ".olean")
        target.parent.mkdir(parents=True, exist_ok=True)
        proc = invoke(["-o", str(target), rel])
        output = clean(proc.stdout + proc.stderr)
        log = HERE / ("fresh-v1-" + module.replace("/", "-") + ".log")
        assert not log.exists()
        log.write_text(output, encoding="utf-8", newline="\n")
        reports = re.findall(r"depends on axioms: \[([^\]]*)\]", output)
        ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", r)) <=
                       {"propext", "Classical.choice", "Quot.sound"} for r in reports)
        record = {"source": rel, "source_sha256": digest(ROOT / rel), "exit": proc.returncode,
                  "log": log.name, "log_sha256": digest(log), "axiom_reports": len(reports),
                  "ordinary_axioms_only": ordinary, "selected_direct_imports": paths}
        if target.is_file():
            record.update({"fresh_cache": label(target), "fresh_cache_sha256": digest(target)})
        records.append(record)
        print(json.dumps(record), flush=True)
        assert proc.returncode == 0 and ordinary
        verify()
    for p, h in dependency_pins.items():
        assert digest(p) == h, "Selected dependency changed: " + label(p)
    result = {"status": "FOCUSED_FRESH_SOURCE_GATE_PASS", "lean_version": version.stdout.strip(),
              "records": records, "bound_inputs_checked_pre_post": len(pins),
              "pre_gate_bindings_sha256": digest(pre), "core_axiom_reports": records[-2]["axiom_reports"],
              "consumer_axiom_reports": records[-1]["axiom_reports"], "clean_transitive_rebuild": False,
              "full_repository_gate": False, "full_documentation_gate": False,
              "independent_review": "PENDING", "scientific_ROOT": False,
              "resource_boundary": "Exact rational scalar/word counters only; bitlength/GCD/control/allocator/full C22 runtime open"}
    receipt = HERE / "focused-verification-v1.json"
    assert not receipt.exists()
    receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt_sha256": digest(receipt), "status": result["status"]}), flush=True)


if __name__ == "__main__":
    run()
