"""Check the frozen author packet without producing independent review evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    sys.path.insert(0, str(ROOT))
    from website.scripts.check_research_publications import validate_record

    freeze = json.loads((HERE / "author-freeze.json").read_text(encoding="utf-8"))
    assert freeze["status"] == "AUTHOR_FROZEN_REVIEW_PENDING_NOT_ADMITTED"
    assert freeze["whole_module_public_inventory_count"] == 15
    proc = subprocess.run([sys.executable, str(HERE / "author-freeze.py")],
                          cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert proc.returncode == 0, "Author packet regeneration failed"
    outputs = json.loads(proc.stdout)["outputs"]
    for name, contents in outputs.items():
        assert (ROOT / name).read_bytes() == contents.encode("utf-8"), name
    pins = {ROOT / row["path"]: row["sha256"] for row in freeze["raw_production_inputs"]}
    pins.update({ROOT / freeze_path: freeze[key] for freeze_path, key in (
        ("QuantumBlockEncoding/ConstructiveTensorTrain.lean", "module_sha256"),
        ("docs/lessons/constructive-tensor-train-canonicalization.md", "lesson_sha256"),
        ("lean-toolchain", "toolchain_sha256"),
        ("lake-manifest.json", "manifest_sha256"),
        ("lakefile.lean", "lakefile_sha256"),
        ("website/research/publications.json", "canonical_publications_sha256_observed"),
        ("website/research/sources.json", "canonical_sources_sha256_observed"),
    )})
    pins.update({HERE / name: expected for name, expected in freeze["author_supporting_artifacts"].items()})
    pins[HERE / "author-formal-context.json"] = freeze["formal_context_sha256"]
    pins[HERE / "author-decoder-packet.json"] = freeze["decoder_packet_sha256"]
    pins[HERE / "author-source-row-candidate.json"] = freeze["owned_proposed_source_row_sha256"]
    for path, expected in pins.items():
        assert sha(path) == expected, path.relative_to(ROOT).as_posix()
    registry = json.loads((ROOT / "website/research/publications.json").read_text(encoding="utf-8"))
    inventory = {row["fullName"]: row for row in json.loads(
        (ROOT / "web/library/declarations.json").read_text(encoding="utf-8"))["declarations"]}
    for record in registry["records"]:
        validate_record(ROOT, record, inventory)
    context = json.loads((HERE / "author-formal-context.json").read_text(encoding="utf-8"))
    for declaration in context["declarations"]:
        reconstructed = declaration["statement_source"]
        if declaration["definition_or_proof_source"] is not None:
            reconstructed += "\n" + declaration["definition_or_proof_source"]
        assert re.sub(r"\s+", " ", reconstructed).strip() == re.sub(
            r"\s+", " ", declaration["source_exact"]).strip()
    canonicalize = next(row for row in context["declarations"] if row["name"].endswith(".canonicalize"))
    assert canonicalize["statement_source"].endswith("→ Result C")
    assert canonicalize["definition_or_proof_source"].lstrip().startswith("| _, _, _, .nil")
    owned = [ROOT / "docs/lessons/constructive-tensor-train-canonicalization.md"]
    owned += [HERE / name for name in (
        "author-binder-definition-audit.json", "author-checks.json", "author-decoder-packet.json",
        "author-formal-context.json", "author-freeze.json", "author-freeze.py", "author-graph-views.json",
        "author-source-coverage.json", "author-source-row-candidate.json", "publication-candidate.json",
        "parent-author-check-v1.py")]
    # A type annotation such as C:\mathrm{Chain} is mathematics, not a drive.
    forbidden = re.compile(r"[A-Za-z]:[\\/][^\\/\s]+[\\/]|file" + r":/{3}|/(?:Users|home)/|github_pat_[A-Za-z0-9]+|ghp_[A-Za-z0-9]+")
    def strings(value):
        if isinstance(value, str):
            return [value]
        if isinstance(value, dict):
            return [s for key, item in value.items() for s in strings(key) + strings(item)]
        if isinstance(value, list):
            return [s for item in value for s in strings(item)]
        return []
    for path in owned:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            text = "\n".join(strings(json.loads(text)))
        assert str(ROOT).casefold() not in text.casefold()
        assert ROOT.as_posix().casefold() not in text.casefold()
        text = re.sub(r"\$\$.*?\$\$|\$[^$\n]*\$", "", text, flags=re.S)
        assert not forbidden.search(text), "Privacy check failed: " + path.relative_to(ROOT).as_posix()
    receipt = {
        "status": "AUTHOR_CHECKPOINT_VERIFIED_REVIEW_PENDING",
        "binding_sha256": freeze["binding_sha256"],
        "author_freeze_sha256": sha(HERE / "author-freeze.json"),
        "observed_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                         capture_output=True, text=True, check=True).stdout.strip(),
        "bound_input_count": len(pins), "generated_outputs_byte_identical": len(outputs),
        "disclosures_checked": len(context["declarations"]),
        "existing_publication_records_validated": len(registry["records"]),
        "privacy_checked_paths": len(owned),
        "owned_artifact_hashes": {path.relative_to(ROOT).as_posix(): sha(path) for path in owned},
        "fresh_Lean_execution": False, "independent_review": False,
        "main_admission": False, "scientific_ROOT": False,
        "boundary": "Author packet integrity only; distinct decoder/source-first review and integrated gates remain pending."
    }
    output = HERE / "parent-author-verification-v1.json"
    assert not output.exists(), "Do not overwrite prior receipts"
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: receipt[key] for key in (
        "status", "binding_sha256", "bound_input_count", "generated_outputs_byte_identical",
        "disclosures_checked", "existing_publication_records_validated", "privacy_checked_paths")}))


if __name__ == "__main__":
    main()
