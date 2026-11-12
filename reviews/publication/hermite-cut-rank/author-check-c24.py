"""Read-only author-packet integrity, not independent review or Lean acceptance."""
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SHA = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
LOAD = lambda path: json.loads(path.read_text(encoding="utf-8"))


def main():
    frozen = LOAD(HERE / "author-freeze.json")
    for name, expected in frozen["artifacts"].items():
        assert SHA(ROOT / name) == expected, name
    for row in frozen["production_inputs"]:
        assert SHA(ROOT / row["path"]) == row["sha256"], row["path"]
    record = LOAD(HERE / "publication-candidate.json")
    inventory = LOAD(ROOT / "web/library/declarations.json")["declarations"]
    names = [r["fullName"] for r in inventory if r["source"] == record["module"]]
    assert len(names) == 20 and record["declarations"] == names
    ctx = LOAD(HERE / "author-formal-context.json")
    for row in ctx["files"]:
        assert "".join(row["full_source_lines"]).encode() == (ROOT / row["path"]).read_bytes()
    repair = LOAD(HERE / "author-lexical-repair-v2.json")
    assert SHA(HERE / "author-formal-context.json") == repair["author_v1_context_sha256"]
    assert SHA(HERE / "author-formal-context-v2.json") == repair["author_v2_context_sha256"]
    current = LOAD(HERE / "author-formal-context-v2.json")
    assert current["files"] == ctx["files"]
    assert [r["source_exact"] for r in current["declarations"]] == [r["source_exact"] for r in ctx["declarations"]]
    for row in current["declarations"]:
        body = row["definition_or_proof_source"]
        assert body.startswith(":=") and row["source_exact"].endswith(body)
        assert row["source_exact"][:-len(body)].rstrip() == row["statement_source"]
    packet = LOAD(HERE / "author-decoder-packet-v2.json")
    assert packet["formal_context_sha256"] == SHA(HERE / "author-formal-context-v2.json")
    assert packet["binding_sha256"] == record["binding_sha256"] == repair["publication_binding_unchanged"]
    graph = LOAD(HERE / "author-graph-views.json")["views"]["source-construction-graph"]
    nodes = {r["id"] for r in graph["nodes"]}
    assert len(nodes) == len(graph["nodes"])
    assert len(graph["hyperedges"]) == 20
    for edge in graph["hyperedges"]:
        assert edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= nodes
    sys.path.insert(0, str(ROOT))
    from website.scripts import check_research_publications as checker
    real_load = checker.load
    source = LOAD(HERE / "author-source-row-candidate.json")["source"]
    def prospective_load(root, name):
        data = real_load(root, name)
        if name == "website/research/sources.json":
            assert not any(r["id"] == source["id"] for r in data["sources"])
            data["sources"].append(source)
        return data
    with patch.object(checker, "load", prospective_load):
        assert checker.binding_digest(ROOT, record) == record["binding_sha256"]
    current_inventory = {r["fullName"]: r for r in inventory}
    existing = LOAD(ROOT / "website/research/publications.json")["records"]
    for item in existing:
        checker.validate_record(ROOT, item, current_inventory)
    print(json.dumps({"status": "AUTHOR_FROZEN_REVIEW_PENDING_NOT_ADMITTED",
                      "author_public_roots": len(names), "existing_records_still_valid": len(existing),
                      "binding": record["binding_sha256"], "independent_acceptance": False,
                      "new_Lean_execution": False, "main_admission": False, "scientific_ROOT": False}, indent=2))


if __name__ == "__main__":
    main()
