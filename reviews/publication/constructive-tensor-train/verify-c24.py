"""Read-only replay of the c24 transport and frozen evidence; not a Lean build."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    attestation = HERE / "reviewer-c24/wrapper-attestation.json"
    assert sha(attestation) == "6faa2797263d0d4a99e11bdf903be9d8ebd8047d4e9c217c44a487b179361480"
    att = load(attestation)
    assert att["verdict"] == "accepted"
    for key in ("wrapper_bindings", "canonical_original_bindings", "canonical_input_bindings"):
        for row in att[key]:
            assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
    for kind, expected in (
        ("decoder-c24", "02947e8eb7f156ecde063f35bf83b59fe710336885c32cdf70707661574fde08"),
        ("reviewer-c24", "1b677e34404deeb44a78dc18b746e09a2fa955ea86d24262fc83b7a56e74f543"),
    ):
        frozen = HERE / kind / "freeze.json"
        assert sha(frozen) == expected
        for row in load(frozen)["artifacts"]:
            assert sha(frozen.parent / row["path"]) == row["sha256"], row["path"]
    historical_files = 0
    for name in ("decoder-c23-freeze.json", "reviewer-c23-current-freeze.json"):
        for row in load(HERE / name)["public_artifacts"]:
            assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
            historical_files += 1
    sys.path.insert(0, str(ROOT))
    from website.scripts import check_research_publications as checker
    registry = load(ROOT / "website/research/publications.json")["records"]
    inventory = {r["fullName"]: r for r in load(ROOT / "web/library/declarations.json")["declarations"]}
    for record in registry:
        checker.validate_record(ROOT, record, inventory)
    record = next(r for r in registry if r["module"] == "QuantumBlockEncoding/ConstructiveTensorTrain.lean")
    link = record["wrapper_transport_attestation"]
    assert link["path"] == attestation.relative_to(ROOT).as_posix()
    assert link["sha256"] == sha(attestation)
    assert record["binding_sha256"] == "9be3c975b10363ad36778d6dc9da4c7a941857f6571f3e2f6072c73d65a51c09"
    graph = load(HERE / "parent-graph-views-v2.json")["views"]["source-construction-graph"]
    nodes = {r["id"] for r in graph["nodes"]}
    for edge in graph["hyperedges"]:
        assert edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= nodes
    action = next(e for e in graph["hyperedges"] if e["heads"] == ["source:ctt:scalar-action"])
    norm = next(e for e in graph["hyperedges"] if e["heads"] == ["source:ctt:scalar-normalization"])
    assert not any(t.startswith("premise:") for t in action["tails"])
    assert set(norm["tails"]) == {"source:ctt:boundary-mass", "typing:scalar-bonds-one", "premise:input-scalar-square-sum-one"}
    print(json.dumps({
        "status": "SOURCE_REVIEWED_LOCAL_INTEGRATION_PENDING",
        "canonical_records_validated": len(registry),
        "historical_artifact_hashes_checked": historical_files,
        "new_Lean_execution": False, "main_admission": False,
        "scientific_ROOT": False, "PURIFIED": False,
    }, indent=2))


if __name__ == "__main__":
    main()
