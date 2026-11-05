#!/usr/bin/env python3
"""Read-only sparse AUTHOR metadata check, not an old-validator modification.

Logical replay: python verify-sparse-v4.py --package METADATA_V4_DIRECTORY
--old AUTHOR_PACKAGE_DIRECTORY --repo REPOSITORY_ROOT
No independent decoder/reviewer verdict, native or runtime input is consumed.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
TARGET = "and:finite-program-definition"
TAIL = "claim:compiler-definition"
OLD_GRAPH_SHA = "65223a13b86a1cf2168c9b4d6fbfc5bf5e38cee5715b779d59d25bf304a281d5"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pathdiff(left, right, path=""):
    if type(left) is not type(right):
        return [{"op": "replace", "path": path, "old": left, "new": right}]
    if isinstance(left, dict):
        result = []
        for key in sorted(set(left) | set(right)):
            child = path + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in left:
                result.append({"op": "add", "path": child, "value": right[key]})
            elif key not in right:
                result.append({"op": "remove", "path": child, "old": left[key]})
            else:
                result += pathdiff(left[key], right[key], child)
        return result
    if isinstance(left, list):
        result = []
        for index in range(min(len(left), len(right))):
            result += pathdiff(left[index], right[index], path + "/" + str(index))
        result += [{"op": "remove", "path": path + "/" + str(i), "old": left[i]} for i in range(len(right), len(left))]
        result += [{"op": "add", "path": path + "/" + str(i), "value": right[i]} for i in range(len(left), len(right))]
        return result
    return [] if left == right else [{"op": "replace", "path": path, "old": left, "new": right}]


def check_sparse(old_graph, new_graph):
    sg_path = "/views/source-construction-graph/AND_hyperedges"
    old_source = old_graph["views"]["source-construction-graph"]
    new_source = new_graph["views"]["source-construction-graph"]
    old_edges, new_edges = old_source["AND_hyperedges"], new_source["AND_hyperedges"]
    require(len(old_edges) == len(new_edges) == 32, "All32 AND records must remain.")
    indices = [i for i, e in enumerate(old_edges) if e["id"] == TARGET]
    require(len(indices) == 1, "Unique authorized construction edge required.")
    index = indices[0]
    old_edge, new_edge = old_edges[index], new_edges[index]
    require(old_edge["tails"] == ["claim:finite-table-and-bound", "natural:finite-wires", "natural:finite-angle", "natural:finite-phase"], "Authorized v3 tail baseline differs.")
    expected = [{"op": "add", "path": sg_path + "/" + str(index) + "/tails/4", "value": TAIL}]
    actual = pathdiff(old_graph, new_graph)
    require(actual == expected, "Graph delta must be exactly one authorized appended tail, no other JSON-path changes.")
    require(new_edge["tails"] == old_edge["tails"] + [TAIL], "Existing tail order/content changed.")
    nodes = {n["id"] for n in new_source["nodes"]}
    require(len(nodes) == len(new_source["nodes"]) and TAIL in nodes, "Tail must reference existing unique producer node.")
    require(len(new_source["open_source_gap_ids"]) == 7 and new_source["open_source_gap_ids"] == old_source["open_source_gap_ids"], "Seven OPEN gaps changed.")
    require(new_source["guarded_exhaustive_cases"] == old_source["guarded_exhaustive_cases"], "Exhaustive cases changed.")
    require(new_source["local_alternative_proofs"] == old_source["local_alternative_proofs"] and new_source["full_compiler_alternative_routes"] == [], "Local OR/compiler-alternative meaning changed.")
    consumers = [e for e in new_graph["views"]["functor-hypergraph"]["hyperedges"] if e["source_hyperedge"] == TARGET]
    require(not consumers, "Current pinned graph has no strictly matching functor consumer; no additional derivative tail is authorized.")
    for edge in new_edges:
        require(edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= nodes, "Malformed complete AND reference.")
        require(len(edge["tails"]) == len(set(edge["tails"])), "Duplicate AND tail.")
    for edge in new_graph["views"]["functor-hypergraph"]["hyperedges"]:
        source = next(e for e in new_edges if e["id"] == edge["source_hyperedge"])
        require(edge["tails"] == source["tails"] and edge["heads"] == source["heads"], "Functor/source full-tail correspondence broken.")
    adjacency = {identifier: [] for identifier in nodes}
    for edge in new_edges:
        for tail in edge["tails"]:
            adjacency[tail] += edge["heads"]
    done, live = set(), set()
    def visit(node):
        require(node not in live, "Construction DAG cycle.")
        if node in done:
            return
        live.add(node)
        for child in adjacency[node]:
            visit(child)
        live.remove(node)
        done.add(node)
    for node in nodes:
        visit(node)
    return {"status": "AUTHOR_SPARSE_DIFF_PASS_NOT_FULL_TOPOLOGY_ACCEPTANCE", "exact_path_diff": actual,
            "AND_records_preserved": 32, "unchanged_other_AND_records": 31, "OPEN_gaps_preserved": 7,
            "strict_functor_consumers_of_changed_edge": 0, "OR_cases_and_other_graph_bytes_structurally_unchanged": True,
            "no_new_source_hypothesis": True, "construction_DAG_cycle": False}


def negative_tests(old_graph, new_graph):
    tests = []
    def reject(name, mutate):
        graph = copy.deepcopy(new_graph)
        mutate(graph)
        try:
            check_sparse(old_graph, graph)
        except ValueError as error:
            tests.append({"test": name, "result": "REJECTED_EXPECTED", "reason": str(error)})
        else:
            raise AssertionError("Invalid sparse mutation accepted: " + name)
    def changed(graph):
        return next(e for e in graph["views"]["source-construction-graph"]["AND_hyperedges"] if e["id"] == TARGET)
    reject("remove the required compiler producer again", lambda g: changed(g)["tails"].pop())
    reject("duplicate the compiler tail", lambda g: changed(g)["tails"].append(TAIL))
    reject("replace producer with semantic theorem", lambda g: changed(g)["tails"].__setitem__(-1, "claim:semantic-compiler"))
    reject("edit a preexisting finite-data tail", lambda g: changed(g)["tails"].__setitem__(0, "claim:compiler-definition"))
    reject("rename graph metadata version", lambda g: g.update(metadata_version=4))
    reject("close one scientific OPEN gap", lambda g: g["views"]["source-construction-graph"]["open_source_gap_ids"].pop())
    reject("promote XOR option to compiled alternate", lambda g: g["views"]["source-construction-graph"]["local_alternative_proofs"][0].update(compiled_alternative_construction=True))
    reject("change exhaustive-case semantics", lambda g: g["views"]["source-construction-graph"]["guarded_exhaustive_cases"][0].update(alternative_constructions=True))
    reject("drop conceptual transport AND-tail", lambda g: g["views"]["functor-hypergraph"]["hyperedges"][0]["tails"].pop())
    reject("add unrelated wrapper resource premise", lambda g: next(e for e in g["views"]["source-construction-graph"]["AND_hyperedges"] if e["id"] == "and:verified-wrapper-correctness")["tails"].append("claim:Ry-count"))
    return tests


def leaves(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values(): yield from leaves(child)
    elif isinstance(value, list):
        for child in value: yield from leaves(child)


HOST = re.compile(r"(?i)(?<![\w])[a-z]:[\\/][^\s\"<>]*|(?:/Users/|/home/)[^/\s|()\[\]{}]+(?:/|$)|\\\\[A-Za-z0-9_.-]+\\[^\s]+")
SECRET = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_|sk-(?:proj-)?)[A-Za-z0-9_-]{20,}|\bAKIA[A-Z0-9]{16}\b|(?i:bearer)\s+[A-Za-z0-9._-]{24,}")


class Shadow:
    def __init__(self, path, raw): self.path, self.raw = path, raw
    def resolve(self): return self.path.resolve()
    def is_file(self): return True
    def read_bytes(self): return self.raw
    def read_text(self, encoding="utf-8"): return self.raw.decode(encoding)


class Overlay:
    def __init__(self, repo, replacement): self.repo, self.replacement = repo, replacement
    def __fspath__(self): return str(self.repo)
    def resolve(self): return self.repo.resolve()
    def __truediv__(self, name):
        key = str(name)
        return Shadow(self.repo / key, self.replacement[key]) if key in self.replacement else self.repo / key


def verify(package, old, repo):
    load = lambda path: json.loads(path.read_bytes())
    v3 = old / "metadata-v3"
    old_raw = (v3 / "author-graph-views.json").read_bytes()
    require(sha(old_raw) == OLD_GRAPH_SHA, "Pinned v3 graph changed.")
    old_graph, new_graph = json.loads(old_raw), load(package / "author-graph-views.json")
    sparse = check_sparse(old_graph, new_graph)
    negative = negative_tests(old_graph, new_graph)
    require(load(package / "sparse-checks.json") == {"positive": sparse, "negative_tests": negative, "independent_acceptance": False}, "Static replay differs from recorded author checks.")
    require(load(package / "graph-path-diff.json")["json_path_diff"] == sparse["exact_path_diff"], "Recorded exact graph path diff differs.")
    seal = load(package / "metadata-v4-seal.json")
    def check(base, pin):
        raw = (base / pin["path"]).read_bytes()
        require(sha(raw) == pin["sha256"] and len(raw) == pin["bytes"], "Immutable pin mismatch: " + pin["path"])
    for pin in seal["predecessor_files_preserved"]: check(old, pin)
    for pin in seal["new_files"]: check(package, pin)
    inputs = load(package / "input-references.json")
    for pin in inputs["exact_unchanged_references"]: check(package, pin)
    for pin in inputs["actual_ambient_and_config_pins"]: check(repo, pin)
    checker = repo / "website/scripts/check_research_publications.py"
    checker_raw = checker.read_bytes()
    require(sha(checker_raw) == inputs["checker_sha256"], "Binding-function source changed.")
    ns = {"__file__": str(checker), "__name__": "c31_v4_binding_only"}
    exec(compile(checker_raw, str(checker), "exec"), ns)
    catalog_raw = (repo / "website/research/sources.json").read_bytes()
    require(sha(catalog_raw) == inputs["source_catalog_snapshot_sha256"], "Source catalog drift; no reseal.")
    catalog = json.loads(catalog_raw)
    row = load(old / "author-source-row-candidate.json")["source"]
    existing = [r for r in catalog["sources"] if r["id"] == row["id"]]
    require(not existing or existing == [row], "Source row differs.")
    if not existing: catalog["sources"].append(row)
    source = (old / "source-only.md").read_bytes()
    bindings = []
    for stem in ("PrimitiveMacros", "UniformlyControlledRy", "CubicAmplitudePrimitive"):
        name = "publication-candidate-" + stem + ".json"
        candidate, prior = load(package / name), load(v3 / name)
        # Preservation of the seven slots is by exact unchanged source/contract
        # fields, not a newly performed semantic or independent source review.
        for field in ("module", "source_id", "source_statement", "source_anchor", "lesson_path", "declarations", "obligation_map", "assumption_deltas", "formalizer", "residual_boundary", "source_proof_coverage", "binder_definition_audit", "formal_context", "formal_packet", "purification"):
            require(candidate[field] == prior[field], "Out-of-scope candidate semantic/reference change: " + field)
        require(candidate["v3_predecessor_binding_sha256"] == prior["binding_sha256"], "History link missing.")
        overlay = Overlay(repo, {candidate["lesson_path"]: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()})
        require(ns["binding_digest"](overlay, candidate) == candidate["binding_sha256"], "Prospective binding replay failed.")
        require(not candidate["independent_acceptance"] and not candidate["main_admission"] and not candidate["scientific_ROOT"], "Acceptance overclaim.")
        require(candidate["graph_contribution"]["source_graph_sha256"] == sha((package / "author-graph-views.json").read_bytes()), "Graph binding mismatch.")
        bindings.append({"module": candidate["module"], "binding_sha256": candidate["binding_sha256"]})
    allowlist = load(package / "public-allowlist.json")
    for pin in allowlist["new_originals"] + allowlist["versioned_derivatives"]: check(package, pin)
    for pin in allowlist["exact_references"]: check(package, pin)
    files = [package / p["path"] for group in ("new_originals", "versioned_derivatives", "exact_references") for p in allowlist[group]] + [package / "public-allowlist.json"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        values = leaves(json.loads(text)) if path.suffix == ".json" else [text]
        for value in values: require(not HOST.search(value) and not SECRET.search(value), "Privacy pattern finding: " + path.name)
    return {"status": "AUTHOR_V4_SPARSE_REPLAY_PASS_NOT_INDEPENDENT_REVIEW", "sparse_graph": sparse, "negative_tests": len(negative),
            "new_prospective_bindings": bindings, "all_predecessor_files_unchanged": True,
            "public_allowlist_sha256": sha((package / "public-allowlist.json").read_bytes()),
            "seal_sha256": sha((package / "metadata-v4-seal.json").read_bytes()), "decoded_JSON_privacy_findings": 0,
            "full_F3_topology_acceptance": False, "SourceAgreement": False, "native_formal_admission": False,
            "decoder_CI_runtime_read": False, "Lean_Git_network_canonical_writes": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package", "old", "repo"): parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.package.resolve(), args.old.resolve(), args.repo.resolve()), ensure_ascii=False, indent=2))
