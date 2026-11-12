"""Immutable parent integrity and whole-source replay, not scientific acceptance."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from website.scripts.check_research_publications import binding_digest, validate_record


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result_path = HERE / "parent-admission-c18-v1.json"
    log_path = HERE / "parent-admission-c18-v1.log"
    if result_path.exists() or log_path.exists():
        raise SystemExit("Frozen parent replay exists; no overwrite")
    candidate = json.loads((HERE / "publication-candidate.json").read_text(encoding="utf-8"))
    raw = json.loads((ROOT / "web/library/declarations.json").read_text(encoding="utf-8"))
    inventory = {d["fullName"]: d for d in raw["declarations"]}
    validate_record(ROOT, candidate, inventory)
    artifact = json.loads((HERE / "reviewer-artifact.json").read_text(encoding="utf-8"))
    receipt = json.loads((HERE / "reviewer-receipt-c17-v3.json").read_text(encoding="utf-8"))
    assert receipt["exit_code"] == 0 and receipt["changed_context"] == []
    assert receipt["allowed_reads_before"] == receipt["allowed_reads_after"]
    pins = receipt["allowed_reads_before"] + artifact["content_pins"]
    for pin in pins:
        assert sha(ROOT / pin["path"]) == pin["sha256"], pin["path"]
    declarations = [d["name"] for d in artifact["declarations"]]
    assert len(declarations) == 29 and set(declarations) == set(candidate["declarations"])
    assert all(d["binder_audit"]["excess"] == [] for d in artifact["declarations"])
    target = (ROOT / candidate["module"]).read_text(encoding="utf-8")
    probe = (ROOT / artifact["independent_probes"]["source"]).read_text(encoding="utf-8")
    assert not re.search(r"(?m)^import\s+QuantumBlockEncoding.StoredMatrixProductChain\b", probe)
    checks = "\n".join("#check " + name + "\n#print axioms " + name for name in declarations)
    whole = target + "\n" + checks + "\n" + probe
    before = {p["path"]: sha(ROOT / p["path"]) for p in pins}
    started = time.perf_counter()
    run = subprocess.run(["lake", "env", "lean", "--stdin"], input=whole, cwd=ROOT,
                         encoding="utf-8", errors="replace", stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    output = run.stdout.replace(str(ROOT), "<repo>").replace(ROOT.as_posix(), "<repo>")
    output = re.sub(r"[A-Za-z]:[\\/][^\r\n'\"<>]*", "<private-path>", output)
    log_path.write_text(output, encoding="utf-8")
    after = {name: sha(ROOT / name) for name in before}
    axioms = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", output, flags=re.S)
    unexpected = sorted({a.strip() for group in axioms for a in group.split(",")
                         if a.strip() not in {"propext", "Classical.choice", "Quot.sound"}})
    passed = run.returncode == 0 and before == after and len(axioms) >= 29 and not unexpected
    result = {
        "schema_version": 1, "status": "passed" if passed else "failed",
        "scope": "Exact local whole-module correspondence; no main, provider-wide, finite-bit or scientific ROOT admission",
        "binding_sha256": binding_digest(ROOT, candidate),
        "reviewer_artifact_sha256": sha(HERE / "reviewer-artifact.json"),
        "reviewer_evidence_sha256": sha(HERE / "reviewer-evidence.json"),
        "reviewer_receipt_sha256": sha(HERE / "reviewer-receipt-c17-v3.json"),
        "source_assembly_sha256": hashlib.sha256(whole.encode()).hexdigest(),
        "source_whole_target": True, "public_declarations": len(declarations),
        "provider_cache_scope": receipt["cache_scope"],
        "unique_rehashed_inputs": len(before), "inputs_before": before,
        "inputs_after": after, "inputs_unchanged": before == after,
        "command": ["lake", "env", "lean", "--stdin"],
        "exit_code": run.returncode, "seconds": time.perf_counter() - started,
        "printed_axiom_roots": len(axioms), "unexpected_axioms": unexpected,
        "log": log_path.relative_to(ROOT).as_posix(), "log_sha256": sha(log_path),
        "source_gap_policy": "G01-G03 remain frozen supplier boundaries; no source-first graph or lesson repair",
        "root_closed": False, "main_admitted": False, "purified": False,
    }
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in ["inputs_before", "inputs_after"]}, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
