"""Portable mechanical AUTHOR/WIP check. No Lean, Git, network or cache writes."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
SHA = lambda b: hashlib.sha256(b).hexdigest()
LOAD = lambda p: json.loads(p.read_text(encoding="utf-8"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    a = p.parse_args()
    root, packet = a.root.resolve(), a.packet.resolve()
    freeze = LOAD(packet/"author-freeze.json")
    for name, expected in freeze["artifacts"].items():
        assert SHA((packet/name).read_bytes()) == expected, name
    for row in freeze["production_inputs"] + freeze["other_fixed_inputs"]:
        assert SHA((root/row["path"]).read_bytes()) == row["sha256"], row["path"]
    for name, expected in freeze["provider_and_existing_lesson_inputs"].items():
        assert SHA((root/name).read_bytes()) == expected, name
    source = (packet/"finite-real-tensor-train-canonicalization-and-gram.md").read_bytes()
    assert SHA(source) == freeze["source_sha256"]
    coverage = LOAD(packet/"author-source-coverage.json")
    assert "".join(row["exact_text"] for row in coverage["source_paragraphs"]).encode() == source
    offset = 0
    for row in coverage["source_paragraphs"]:
        exact = row["exact_text"].encode()
        assert row["start_utf8_byte"] == offset
        assert row["end_utf8_byte"] == offset+len(exact)
        assert SHA(exact) == row["sha256"]
        assert row["disposition"] == "NODE" and row["nodes"] or row["disposition"] == "EXCLUDED" and row["reason"]
        offset += len(exact)
    assert offset == len(source)
    context = LOAD(packet/"author-formal-context.json")
    assert len(context["declarations"]) == 49
    assert sum(r["canonical_inventory_root"] for r in context["declarations"]) == 48
    assert SHA((packet/"author-formal-context.json").read_bytes()) == coverage["full_source_context_sha256"]
    for file in context["files"] + context["toolchain_manifest"]:
        exact = "".join(file["full_source_lines"]).encode()
        assert SHA(exact) == file["sha256"]
        assert exact == (root/file["path"]).read_bytes()
    assert "statement_source" not in (packet/"author-formal-context.json").read_text(encoding="utf-8")
    assert not context["scope"]["private_helpers_in_targets"]
    inventory = LOAD(root/"web/library/declarations.json")["declarations"]
    for module, count in context["scope"]["target_inventory_counts"].items():
        names = [r["fullName"] for r in inventory if r["source"] == module]
        assert len(names) == count
        assert names == [r["declaration"] for r in context["declarations"] if r["module"] == module and r["canonical_inventory_root"]]
    graph = LOAD(packet/"author-graph-views.json")
    assert graph["coverage_sha256"] == SHA((packet/"author-source-coverage.json").read_bytes())
    sg = graph["views"]["source-construction-graph"]
    nodes = {r["id"]:r for r in sg["nodes"]}
    assert len(nodes) == len(sg["nodes"])
    assert len(sg["hyperedges"]) == 22
    for edge in sg["hyperedges"]:
        assert edge["logic"] == "AND" and edge["tails"] and edge["heads"]
        assert set(edge["tails"]+edge["heads"]) <= set(nodes)
    assert len(sg["independent_source_gap_ids"]) == 7
    for ident in sg["independent_source_gap_ids"]:
        assert nodes[ident]["status"] == "OPEN" and not nodes[ident]["mathematical_proof_node"]
    assert {r["to"] for r in sg["source_gap_links"]} == {r["id"] for r in sg["nodes"] if r["kind"] == "SOURCE_GAP"}
    assert len(graph["views"]["lean-graph"]["target_import_edges"]) == 3
    assert len(graph["views"]["lean-graph"]["ownership_edges"]) == 49
    assert not graph["views"]["lean-graph"]["theorem_dependency_edges"]
    assert graph["views"]["functor-hypergraph"]["certified_transport"] is False
    assert not graph["views"]["functor-hypergraph"]["implication_hyperedges"]
    obligations = {r["id"]:r for r in coverage["obligations"]}
    assert len(obligations) == 49
    for row in obligations.values():
        assert row["output_logic"] == "AND" and row["output_conjuncts"] and row["source_paragraphs"]
        assert all(x["classification"] == "SOURCE" and x["not_typing_or_output"] for x in row["logical_inputs"])
    assert [r["binder"] for r in obligations["TC-32"]["logical_inputs"]] == ["hl","columns"]
    assert [r["binder"] for r in obligations["TC-33"]["logical_inputs"]] == ["hl","hr","hA"]
    assert [r["binder"] for r in obligations["TC-17"]["logical_inputs"]] == ["hC"]
    assert [r["binder"] for r in obligations["TC-19"]["logical_inputs"]] == ["hv"]
    assert [r["binder"] for r in obligations["TC-20"]["logical_inputs"]] == ["hC"]
    assert [r["binder"] for r in obligations["TC-26"]["logical_inputs"]] == ["hU"]
    assert [r["binder"] for r in obligations["TN-11"]["logical_inputs"]] == ["hD"]
    assert [r["binder"] for r in obligations["TN-15"]["logical_inputs"]] == ["hD"]

    # Invoke the public binding function itself. Mocking in-memory readers is an
    # explicit prospective overlay, not a rewrite of the trusted implementation.
    spec = importlib.util.spec_from_file_location("ttc_author_public_checker",root/"website/scripts/check_research_publications.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    original_file, original_load = checker.local_file, checker.load
    row = LOAD(packet/"author-source-row-candidate.json")["source"]
    lesson = "docs/lessons/finite-real-tensor-train-canonicalization-and-gram.md"
    def prospective_file(r,n):
        return packet/"finite-real-tensor-train-canonicalization-and-gram.md" if n == lesson else original_file(r,n)
    def prospective_load(r,n):
        data = original_load(r,n)
        if n == "website/research/sources.json":
            existing = [item for item in data["sources"] if item["id"] == row["id"]]
            assert not existing or existing == [row]
            if not existing: data["sources"].append(row)
        return data
    bindings=[]
    with patch.object(checker,"local_file",prospective_file), patch.object(checker,"load",prospective_load):
        for name in ("publication-candidate-canonical.json","publication-candidate-norm-environment.json"):
            record=LOAD(packet/name)
            assert checker.binding_digest(root,record) == record["binding_sha256"]
            assert record["main_admission"] is False and record["scientific_ROOT"] is False
            assert record["status"] == "AUTHOR_WIP_NOT_ADMITTED"
            assert record["evidence_paths_status"] == "PROPOSED_FUTURE_PATHS_NOT_ASSERTED_PRESENT_OR_ACCEPTED"
            assert set(record["declarations"]) == {r["declaration"] for r in obligations.values() if r["module"] == record["module"] and r["canonical_inventory_root"]}
            assert set(record["declarations"]) == {n for item in record["obligation_map"] for n in item["declarations"]}
            bindings.append({"module":record["module"],"binding_sha256":record["binding_sha256"]})
    dp=LOAD(packet/"author-decoder-packet.json")
    assert dp["opaque_bindings"] == bindings
    assert dp["formal_context_sha256"] == SHA((packet/"author-formal-context.json").read_bytes())
    for name in ("author-decoder-packet.json","author-formal-context.json"):
        text=(packet/name).read_text(encoding="utf-8")
        assert "aspbe-local-finite-real-tt-canonicalization-and-gram" not in text
        assert "895ec97fe7e95146" not in text
        assert "assumption_deltas" not in text
    # Portable output JSON must not contain the local machine's drive paths.
    for name in freeze["artifacts"]:
        text=(packet/name).read_text(encoding="utf-8")
        for drive in ("C","D"):
            for separator in ("/","\\\\"):
                assert drive+":"+separator+"Users"+separator not in text
    print(json.dumps({"status":"MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION","source_bytes":len(source),"source_paragraphs":len(coverage["source_paragraphs"]),"canonical_roots":48,"named_ambient_instances":1,"whole_named_inventory":49,"actual_target_import_edges":3,"independent_source_AND_chains":22,"independent_open_source_gaps":7,"additional_author_explanatory_gap":1,"public_prospective_bindings":bindings,"validate_record_called":False,"Lean_executed":False,"independent_review_fabricated":False,"main_repository_mutated":False,"main_admission":False,"scientific_ROOT":False},ensure_ascii=False))


if __name__ == "__main__": main()
