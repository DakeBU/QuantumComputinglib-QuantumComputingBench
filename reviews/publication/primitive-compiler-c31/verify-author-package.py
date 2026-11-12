#!/usr/bin/env python3
"""Read-only C31 AUTHOR integrity check. Not Lean, source review or admission.

Usage: python verify-author-package.py --repo REPO --out THIS_DIRECTORY
Only reads C31 artifacts, pinned actual source/config/catalog bytes and the
unchanged checker binding_digest function. Never inspects independent output.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class ShadowFile:
    def __init__(self, path, raw):
        self.path, self.raw = path, raw
    def resolve(self):
        return self.path.resolve()
    def is_file(self):
        return True
    def read_bytes(self):
        return self.raw
    def read_text(self, encoding="utf-8"):
        return self.raw.decode(encoding)


class Overlay:
    def __init__(self, repo, replacement):
        self.repo, self.replacement = repo, replacement
    def resolve(self):
        return self.repo.resolve()
    def __truediv__(self, name):
        key = str(name)
        return ShadowFile(self.repo / key, self.replacement[key]) if key in self.replacement else self.repo / key


def verify(repo, out):
    load = lambda name: json.loads((out / name).read_bytes())
    manifest = load("outputs-manifest.json")
    freeze = load("metadata-freeze.json")
    def check(base, rec):
        name = rec["path"]
        assert not Path(name).is_absolute() and ".." not in Path(name).parts
        raw = (base / name).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], name
    for rec in manifest["artifacts"] + freeze["original_immutable_inputs"] + freeze["new_artifacts"]:
        check(out, rec)
    for rec in freeze["whole_ambient_binding_inputs"] + freeze["strict_config_and_external_inputs"]:
        check(repo, rec)
    current = [{"path": path.relative_to(repo).as_posix(), "sha256": sha(path.read_bytes()), "bytes": len(path.read_bytes())}
               for directory in ("QuantumBlockEncoding", "ABEISTests") for path in sorted((repo / directory).rglob("*.lean"))]
    assert current == freeze["whole_ambient_binding_inputs"] and len(current) == 202
    formal, packet = load("author-formal-context.json"), load("author-decoder-packet.json")
    context_sha = sha((out / "author-formal-context.json").read_bytes())
    packet_sha = sha((out / "author-decoder-packet.json").read_bytes())
    assert packet["formal_context_sha256"] == packet["opaque_context_binding_sha256"] == context_sha
    seal = load("formal-input-seal.json")
    assert seal["formal_context_sha256"] == context_sha and seal["formal_packet_sha256"] == packet_sha
    files = formal["target_files"] + formal["provider_index"]
    known = {rec["path"] for rec in files}
    for rec in files + formal["dependency_context"]:
        raw = "".join(rec["full_source_lines"]).encode()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"] and raw == (repo / rec["path"]).read_bytes()
        for imp in rec.get("imports", []):
            if imp.startswith("QuantumBlockEncoding."):
                assert imp.replace(".", "/") + ".lean" in known, imp
    roots = formal["inventory"]
    assert len(roots) == 87 and len({r["name"] for r in roots}) == 87
    assert sum(not r["private"] for r in roots) == 79 and sum(r["private"] for r in roots) == 8
    assert [len(rec["full_source_lines"]) for rec in formal["target_files"]] == [638, 422, 230]
    coverage = load("author-source-coverage.json")
    source = (out / "source-only.md").read_bytes()
    lesson = manifest["lesson_path"]
    assert source == (out / Path(lesson).name).read_bytes()
    assert "".join(p["exact_text"] for p in coverage["source_paragraphs"]).encode() == source
    offset = 0
    for p in coverage["source_paragraphs"]:
        raw = p["exact_text"].encode()
        assert p["start_utf8_byte"] == offset and p["end_utf8_byte"] == offset + len(raw)
        assert source[offset:offset + len(raw)] == raw and sha(raw) == p["sha256"]
        assert p["disposition"] in {"NODE", "EXCLUDED"} and (p["source_nodes"] or p["reason"])
        offset += len(raw)
    obligations = coverage["whole_module_inventory"]
    assert len(obligations) == 87 and {o["name"] for o in obligations} == {r["name"] for r in roots}
    for o in obligations:
        assert o["source_paragraphs"]
        assert sha(o["definition_audit"]["exact_source_region"].encode()) == o["definition_audit"]["sha256"]
        assert all(b["classification"] in {"SOURCE", "TYPING", "STANDING", "RULED"} for b in o["binder_audit"])
    audit = load("author-binder-definition-audit.json")
    bundles = audit["project_owned_bundle_expansions"]
    for bundle in bundles.values():
        assert all(name in bundles for name in bundle["recursive_expansions"])
    expected_fields = {
        "MonomialProgram": {"program", "phase", "permutation", "exact"},
        "PrimitiveProgramRefinement": {"program", "target", "exact"},
        "PrimitiveProgram": {"circuit", "globalPhase"},
        "OperatorBlockEncodingCandidate": {"auxiliaryQubits", "target", "unitary", "layout", "circuit", "schedule", "resource", "layoutMatches", "isUnitary", "blockContainsTarget"},
        "VerifiedOperatorBlockEncoding": {"candidate", "unitaryProof", "blockProof"},
    }
    for name, expected in expected_fields.items():
        assert {field["name"] for field in bundles["QuantumBlockEncoding." + name]["fields"]} == expected, name
    graph = load("author-graph-views.json")
    sg = graph["views"]["source-construction-graph"]
    ids = {node["id"] for node in sg["nodes"]}
    assert len(ids) == len(sg["nodes"])
    assert all(p["source_nodes"][0] in ids for p in coverage["source_paragraphs"] if p["disposition"] == "NODE")
    for edge in sg["AND_hyperedges"] + graph["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= ids
    assert len(graph["views"]["lean-graph"]["ownership_edges"]) == 87
    assert not graph["views"]["lean-graph"]["elaborated_theorem_dependencies"]
    checker = repo / freeze["checker_path"]
    raw_checker = checker.read_bytes()
    assert sha(raw_checker) == freeze["checker_sha256"]
    namespace = {"__name__": "c31_readonly_binding_only", "__file__": str(checker)}
    exec(compile(raw_checker, str(checker), "exec"), namespace)
    catalog_raw = (repo / freeze["source_catalog_path"]).read_bytes()
    assert sha(catalog_raw) == freeze["source_catalog_sha256"], "Source catalog drift: no reseal."
    catalog = json.loads(catalog_raw)
    row = load("author-source-row-candidate.json")["source"]
    assert not any(s["id"] == row["id"] for s in catalog["sources"])
    catalog["sources"].append(row)
    overlay = Overlay(repo, {lesson: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()})
    bindings = []
    for rec in formal["target_files"]:
        candidate = load("publication-candidate-" + Path(rec["path"]).stem + ".json")
        expected = {r["name"] for r in roots if r["module"] == rec["path"] and not r["private"]}
        assert len(candidate["declarations"]) == len(expected) and set(candidate["declarations"]) == expected
        assert {name for edge in candidate["obligation_map"] for name in edge["declarations"]} == expected
        assert candidate["graph_contribution"]["formal_context_sha256"] == context_sha
        assert candidate["graph_contribution"]["formal_packet_sha256"] == packet_sha
        assert candidate["status"] == "AUTHOR_WIP_NOT_ADMITTED"
        assert not candidate["independent_acceptance"] and not candidate["main_admission"] and not candidate["scientific_ROOT"]
        assert namespace["binding_digest"](overlay, candidate) == candidate["binding_sha256"]
        bindings.append({"module": candidate["module"], "binding_sha256": candidate["binding_sha256"]})
    assert bindings == load("author-binding-bridge-proposal.json")["bindings"]
    registry_raw = (repo / freeze["registry_path"]).read_bytes()
    assert sha(registry_raw) == freeze["registry_sha256"]
    registry = json.loads(registry_raw)
    assert len(registry["records"]) == 23
    assert not {c["module"] for c in bindings} & {r["module"] for r in registry["records"]}
    for forbidden in (row["id"], lesson, "source-only.md", "author-source-coverage", "assumption_deltas", "SOURCE_GAP"):
        assert forbidden not in (out / "author-formal-context.json").read_text(encoding="utf-8")
        assert forbidden not in (out / "author-decoder-packet.json").read_text(encoding="utf-8")
    return {"status": "MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION", "target_modules": 3, "source_named_roots": 87, "public_roots": 79, "private_helpers": 8,
            "whole_ambient_files": 202, "local_provider_closure_modules": len(formal["provider_index"]), "lossless_source_paragraphs": len(coverage["source_paragraphs"]),
            "AND_edges": len(sg["AND_hyperedges"]), "SOURCE_GAPs": len(sg["open_source_gap_ids"]), "formal_context_sha256": context_sha, "formal_packet_sha256": packet_sha,
            "binding_replays": bindings, "registry_count_unchanged": 23, "manifest_sha256": sha((out / "outputs-manifest.json").read_bytes()),
            "Lean_executed": False, "Git_executed": False, "independent_results_inspected": False, "validate_record_called": False, "read_only": True,
            "main_admission": False, "scientific_ROOT": False, "PURIFIED": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.repo.resolve(), args.out.resolve()), ensure_ascii=False, indent=2))
