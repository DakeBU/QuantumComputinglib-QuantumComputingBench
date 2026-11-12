"""Check versioned graph bindings; independent mathematical review remains separate."""
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sys.path.insert(0, str(ROOT))
    from website.scripts import check_research_publications as checker
    old = read("publication-candidate.json")
    new = read("publication-candidate-v2.json")
    graph = read("parent-graph-views-v2.json")
    repair = read("parent-graph-repair-v2.json")
    assert new["module"] == old["module"] and new["declarations"] == old["declarations"]
    for key in ("source_statement", "source_anchor", "lesson_path", "obligation_map",
                "assumption_deltas", "formalizer", "residual_boundary"):
        assert old[key] == new[key], key
    source = read("author-source-row-candidate.json")["source"]
    original_load = checker.load
    def prospective_load(root, name):
        loaded = original_load(root, name)
        if name == "website/research/sources.json":
            loaded["sources"].append(source)
        return loaded
    with patch.object(checker, "load", prospective_load):
        assert checker.binding_digest(ROOT, new) == new["binding_sha256"]
    assert new["binding_sha256"] == repair["successor_binding_sha256"]
    a, b = read("author-decoder-packet.json"), read("author-decoder-packet-v2.json")
    assert a.pop("binding_sha256") == old["binding_sha256"]
    assert b.pop("binding_sha256") == new["binding_sha256"] and a == b
    assert sha(HERE / "author-formal-context.json") == b["formal_context_sha256"]
    sg = graph["views"]["source-construction-graph"]
    nodes = {node["id"] for node in sg["nodes"]}
    assert len(nodes) == len(sg["nodes"])
    for edge in sg["hyperedges"]:
        assert edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= nodes
    action = next(e for e in sg["hyperedges"] if e["heads"] == ["source:ctt:scalar-action"])
    norm = next(e for e in sg["hyperedges"] if e["heads"] == ["source:ctt:scalar-normalization"])
    assert not any(t.startswith("premise:") for t in action["tails"])
    assert set(norm["tails"]) == {"source:ctt:boundary-mass", "typing:scalar-bonds-one",
                                   "premise:input-scalar-square-sum-one"}
    review = read("reviewer-c23-topology-successor-review.json")
    assert review["status"] == "ACCEPTED_BOUNDED_SOURCE_TOPOLOGY_SUCCESSOR"
    assert review["successor_binding_sha256"] == new["binding_sha256"]
    assert review["successor_graph_sha256"] == sha(HERE / "parent-graph-views-v2.json")
    assert review["successor_coverage_sha256"] == sha(HERE / "parent-source-coverage-v2.json")
    assert repair["superseded_author_graph_sha256"] == sha(HERE / "author-graph-views.json")
    inventory = {row["fullName"]: row for row in checker.load(ROOT, "web/library/declarations.json")["declarations"]}
    records = checker.load(ROOT, "website/research/publications.json")["records"]
    for record in records:
        checker.validate_record(ROOT, record, inventory)
    receipt = {"status": "VERSIONED_GRAPH_INTEGRITY_PASS_FULL_ADMISSION_PENDING",
               "binding_sha256": new["binding_sha256"], "whole_public_inventory": len(new["declarations"]),
               "explicit_source_nodes": len(nodes), "complete_AND_edges": len(sg["hyperedges"]),
               "blind_packet_only_opaque_binding_changed": True,
               "graph_sha256": sha(HERE / "parent-graph-views-v2.json"),
               "coverage_sha256": sha(HERE / "parent-source-coverage-v2.json"),
               "independent_topology_review_sha256": sha(HERE / "reviewer-c23-topology-successor-review.json"),
               "existing_records_validated": len(records), "production_modified": False,
               "source_mathematics_repaired": False, "independent_decoder_complete": False,
               "main_admission": False, "scientific_ROOT": False}
    out = HERE / "parent-graph-verification-v2.json"
    assert not out.exists(), "Never overwrite an earlier receipt"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
