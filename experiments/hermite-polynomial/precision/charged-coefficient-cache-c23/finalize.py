"""Freeze an exact handoff; emits new evidence only inside the C23 directory."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    manifest = HERE / "final-binding-manifest.json"
    assert not manifest.exists(), "Do not rewrite frozen handoff evidence"
    gate = json.loads((HERE / "focused-verification-v3.json").read_text(encoding="utf-8"))
    assert gate["status"] == "FOCUSED_FRESH_SOURCE_GATE_PASS"
    assert gate["core_axiom_reports"] == 6 and gate["consumer_axiom_reports"] == 4
    pre = json.loads((HERE / "pre-gate-bindings-v3.json").read_text(encoding="utf-8"))
    for rel, expected in pre["sources_and_inherited_cache_pins"].items():
        assert digest(ROOT / rel) == expected, "Bound source/cache changed: " + rel
    for rec in gate["records"]:
        assert digest(ROOT / rec["source"]) == rec["source_sha256"]
        assert digest(HERE / rec["log"]) == rec["log_sha256"]
        assert digest(ROOT / rec["fresh_cache"]) == rec["fresh_cache_sha256"]
    raw = {p.name: digest(p) for p in HERE.glob("*.raw.log")}
    raw_receipt = HERE / "private-raw-provenance.json"
    assert not raw_receipt.exists()
    raw_receipt.write_text(json.dumps({"private_raw_log_hashes": raw,
        "raw_not_public": True, "prior_failed_receipts_preserved": True}, indent=2) + "\n", encoding="utf-8")
    result = {"status": "PROVED_LOCAL_FROZEN_AWAITING_INDEPENDENT_REVIEW",
        "direction_fingerprint": "C23_ACTUAL_CHARGED_SOURCE_COEFFICIENT_CACHE",
        "slice": "actual rational source coefficients only",
        "entry_root": "HermiteChargedSourceCache.produceSourceCache_entry",
        "actual_root": "HermiteChargedSourceCache.produceSourceCache_actual",
        "same_return_root": "HermiteChargedSourceCache.same_cache_contract",
        "per_op_bound": "52*(k+1)^2", "total_bound": "416*(k+1)^2",
        "focused_gate_sha256": digest(HERE / "focused-verification-v3.json"),
        "symbolic_roots_ordinary_axioms": 10, "independent_review": "PENDING",
        "source_admitted": False, "scientific_ROOT": False, "middle_coefficients_produced": False,
        "full_runtime": False, "finite_bit_GCD_bound": False, "clean_transitive_rebuild": False,
        "full_repository_gate": False, "full_documentation_gate": False,
        "failure_class": "NONE", "prior_failures": ["ENV_BLOCKED", "IMPLEMENTATION_FAILED"],
        "purification": "local bounded provider cleaned; global independent Exposition Seal pending"}
    result_path = HERE / "result.json"
    assert not result_path.exists()
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    artifacts = {p.name: digest(p) for p in HERE.iterdir() if p.is_file() and not p.name.endswith(".raw.log")}
    for rel in artifacts:
        if rel.endswith((".json", ".md", ".public-v1.log", ".log")):
            text = (HERE / rel).read_text(encoding="utf-8-sig")
            assert not re.search(r"[A-Za-z]:[\\/]", text), "Public absolute path leak: " + rel
    cache = {p.relative_to(HERE).as_posix(): digest(p) for p in (HERE / ".cache").rglob("*") if p.is_file()}
    extra = {}
    import_sources = {}
    for rec in gate["records"]:
        for dep in rec["selected_direct_imports"]:
            rel = dep["selected_cache"]
            if rel.startswith("[lean-toolchain]"):
                continue
            assert digest(ROOT / rel) == dep["sha256"]
            extra[rel] = dep["sha256"]
            base = ROOT / rel
            candidate = None
            task_prefix = HERE.relative_to(ROOT).as_posix() + "/.cache/fresh-v3/"
            if rel.startswith(task_prefix + "QuantumBlockEncoding/"):
                candidate = ROOT / (rel.removeprefix(task_prefix).removesuffix(".olean") + ".lean")
            elif rel.startswith(".lake/build/lib/lean/"):
                candidate = ROOT / (rel.removeprefix(".lake/build/lib/lean/").removesuffix(".olean") + ".lean")
            elif rel.startswith(".lake/packages/mathlib/.lake/build/lib/lean/"):
                candidate = ROOT / ".lake/packages/mathlib" / (rel.removeprefix(".lake/packages/mathlib/.lake/build/lib/lean/").removesuffix(".olean") + ".lean")
            elif "/.cache/" in rel and not rel.startswith(HERE.relative_to(ROOT).as_posix()):
                module = base.stem
                for directory in ("piecewise-kernel-assembly-c21", "piecewise-kernel-producer", "piecewise-kernel-uniform-c20", "finite-middle-source"):
                    p = ROOT / "experiments/hermite-polynomial/precision" / directory / (module + ".lean")
                    if p.is_file():
                        candidate = p
                        break
            if candidate is not None and candidate.is_file():
                import_sources[candidate.relative_to(ROOT).as_posix()] = digest(candidate)
            for suffix in (".private", ".server"):
                p = Path(str(base) + suffix)
                if p.is_file():
                    extra[p.relative_to(ROOT).as_posix()] = digest(p)
    manifest.write_text(json.dumps({"status": "FROZEN", "artifact_hashes": artifacts,
        "ignored_private_cache_hashes": cache, "private_raw_log_hashes": raw,
        "pre_gate_bindings": pre, "selected_direct_imports_and_companions_at_freeze": extra,
        "selected_import_source_snapshots_at_freeze": import_sources,
        "companion_pin_scope": "Companions hashed at freeze, not falsely claimed as all pre-gate transitive inputs",
        "focused_gate_sha256": digest(HERE / "focused-verification-v3.json"),
        "independent_review": "PENDING", "source_admitted": False}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest_sha256": digest(manifest), "artifact_count": len(artifacts),
        "private_cache_count": len(cache), "status": "FROZEN"}), flush=True)


if __name__ == "__main__":
    run()
