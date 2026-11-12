#!/usr/bin/env python3
"""Read-only author static metadata audit and mutation-negative tests.

Not a Lean verifier, scoring change, independent review or native acceptance.
Replay uses logical placeholders: --package METADATA_V3_DIRECTORY --old
AUTHOR_PACKAGE_DIRECTORY --repo REPOSITORY_ROOT.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def exact_edge(graph, name):
    return next(e for e in graph["views"]["source-construction-graph"]["AND_hyperedges"] if e["id"] == "and:" + name)


def audit_metadata(coverage, binder, graph, source):
    paragraphs = coverage["source_paragraphs"]
    require("".join(p["exact_text"] for p in paragraphs).encode() == source, "Lossless source partition changed.")
    require(len(paragraphs) == 34 and sha(source) == coverage["source_sha256"], "Natural-source identity changed.")
    offset = 0
    for p in paragraphs:
        raw = p["exact_text"].encode()
        require(p["start_utf8_byte"] == offset and p["end_utf8_byte"] == offset + len(raw), "Paragraph offset discontinuity.")
        require(source[offset:offset + len(raw)] == raw and sha(raw) == p["sha256"], "Paragraph source hash mismatch.")
        require(p["disposition"] in {"NODE", "EXCLUDED"} and bool(p["source_nodes"] or p["reason"]), "Missing exhaustive source disposition.")
        offset += len(raw)
    atoms = {a["id"]: a for a in coverage["source_atoms"]}
    for a in atoms.values():
        raw = source[a["start_utf8_byte"]:a["end_utf8_byte"]]
        require(raw == a["exact_quote"].encode() and sha(raw) == a["sha256"], "Atom quote is not exact natural-source evidence.")
        p = next(p for p in paragraphs if p["id"] == a["source_paragraph"])
        require(p["disposition"] == "NODE" and p["source_region"] == a["source_region"], "Source atom points to excluded/wrong region.")
    roots = coverage["whole_module_inventory"]
    require(len(roots) == 87 and sum(not r["private"] for r in roots) == 79 and sum(r["private"] for r in roots) == 8, "Source-root inventory changed.")
    by_id = {r["id"]: r for r in roots}
    bmap = {r["id"]: r for r in binder["whole_module_inventory"]}
    for r in roots:
        links = r["source_links"]
        require(1 <= len(links) <= 4, "Source links must be bounded declaration-specific excerpts, not whole-module paragraph sets.")
        selected = [atoms[l["natural_atom"]] for l in links]
        require(r["source_paragraphs"] == list(dict.fromkeys(a["source_paragraph"] for a in selected)), "Source paragraph projection is not exact narrowed links.")
        require(r["source_regions"] == list(dict.fromkeys(a["source_region"] for a in selected)), "Source region projection is not exact narrowed links.")
        require(all(l["source_sha256"] == a["sha256"] and l["reviewer_Nxx_mapping_used_as_source"] is False for l, a in zip(links, selected)), "Wrong link authority/hash.")
        require(r["binder_audit"] == bmap[r["id"]]["binder_audit"], "Duplicate binder records disagree.")
        require(r["definition_audit"] == bmap[r["id"]]["definition_audit"], "Definition/source regions changed.")
        require(sha(r["definition_audit"]["exact_source_region"].encode()) == r["definition_audit"]["sha256"], "Whole source block not preserved.")
        require(all(b["classification"] in {"SOURCE", "STANDING", "TYPING", "RULED"} for b in r["binder_audit"]), "EXCESS/unclassified input.")
    require([l["natural_atom"] for l in by_id["C31-009"]["source_links"]] == ["natural:lift"], "Lifting multiplication linked to unrelated macro network.")
    require([l["natural_atom"] for l in by_id["C31-010"]["source_links"]] == ["natural:lift"], "Scalar lifting linked to unrelated macro network.")
    for identity in ("C31-055", "C31-056"):
        root = by_id[identity]
        inputs = root["binder_audit"]
        require(len(inputs) == 6, "Missing complete leading-qubits + five result-Pi inputs.")
        require([b["audit_label"] for b in inputs[1:]] == ["controls", "wires", "target", "target-avoidance", "angles"], "Pi input order changed or omitted.")
        require([b["classification"] for b in inputs] == ["TYPING", "TYPING", "TYPING", "TYPING", "SOURCE", "TYPING"], "Pi guard/typing classification is wrong.")
        require(inputs[4]["exact_lexical_binder"] == "(∀ control, wires control ≠ target)", "Target-avoidance guard weakened/changed.")
        require(root["standing_semantics_not_extra_parameter"]["classification"] == "STANDING", "Angle convention erased as mere typing or new parameter.")
        require(root["standing_semantics_not_extra_parameter"]["computational_access_assumed"] is False, "Free numeric access invented.")
        require(not any("Injective" in b["exact_lexical_binder"] or "injective :" in b["exact_lexical_binder"] for b in inputs), "Control-map injectivity was invented.")
        region = root["complete_lexical_dependent_type_region"]
        require(all(b["exact_lexical_binder"] in region for b in inputs[1:]), "Pi list does not match actual raw dependent type region.")
    sg = graph["views"]["source-construction-graph"]
    ids = {n["id"] for n in sg["nodes"]}
    require(len(ids) == len(sg["nodes"]), "Duplicate graph node.")
    require(all(p["source_nodes"][0] in ids for p in paragraphs if p["disposition"] == "NODE"), "Substantive paragraph lost from source graph.")
    edge_ids = {e["id"] for e in sg["AND_hyperedges"]}
    for e in sg["AND_hyperedges"] + graph["views"]["functor-hypergraph"]["hyperedges"]:
        require(e["logic"] == "AND" and set(e["tails"] + e["heads"]) <= ids, "Invalid/incomplete typed source hyperedge.")
        require(len(e["tails"]) == len(set(e["tails"])) and bool(e["tails"]), "Duplicate or silently empty AND-tail.")
    expected = {
      "recursive-evaluation": {"claim:compiler-definition", "claim:recursive-matrix-definition", "claim:circuit-append-law", "claim:recursive-eval-IH-pair"},
      "semantic-compiler-direct": {"claim:independent-spec", "claim:compiler-definition", "claim:circuit-append-law", "claim:zero-control-block", "claim:cx-context-block", "claim:exact-half-angle-evaluation", "claim:Ry-addition", "claim:X-Ry-X", "claim:reindex-block-product-laws", "claim:head-tail-assignment-reconstruction", "claim:semantic-tail-IH-pair", "claim:head-zero-branch", "claim:head-one-branch"},
      "flat-unitarity": {"claim:flat-matrix-definition", "claim:primitive-program-unitarity", "claim:reindex-unitarity-law"},
      "flat-clean-entries": {"claim:flat-matrix-definition", "claim:named-wire-clean-entries", "claim:clean-index-and-LE-inverse-laws"},
      "verified-wrapper-correctness": {"claim:concrete-candidate-predicates", "claim:concrete-target-normalizer-layout", "claim:flat-unitarity", "claim:flat-clean-entries"},
      "resource-ownership": {"claim:finite-program-definition", "claim:primitive-resource-definition", "natural:resource-ownership"},
    }
    for name, tail in expected.items():
        require(set(exact_edge(graph, name)["tails"]) == tail, "Incorrect complete AND-tail: " + name)
    for e in graph["views"]["functor-hypergraph"]["hyperedges"]:
        source_edge = next(s for s in sg["AND_hyperedges"] if s["id"] == e["source_hyperedge"])
        require(e["tails"] == source_edge["tails"] and e["heads"] == source_edge["heads"], "Conceptual transport silently drops source AND-tail.")
        require(e["certified"] is False and e["independent_review"] == "PENDING_V3", "Conceptual transport promoted without review.")
    for case in sg["guarded_exhaustive_cases"]:
        require(case["semantics"] == "EXHAUSTIVE_CASES_ALL_BRANCHES_REQUIRED" and case["alternative_constructions"] is False, "Guarded cases misreported as independent OR constructions.")
        if "required_branch_ids" in case:
            edge = next(e for e in sg["AND_hyperedges"] if e["id"] == case["consuming_hyperedge"])
            require(set(case["required_branch_ids"]) <= set(edge["tails"]) and len(case["required_branch_ids"]) == 2, "An exhaustive head branch is absent.")
    require(not sg["full_compiler_alternative_routes"], "Source-local proof option falsely promoted to alternative compiler.")
    local = sg["local_alternative_proofs"]
    require(len(local) == 1 and local[0]["logic"] == "OR_OF_SUFFICIENT_LOCAL_PROOF_ROUTES", "Local source E-proof OR lost.")
    require(local[0]["compiled_alternative_construction"] is False and set(local[0]["route_hyperedges"]) == {"and:phase-exponent-eight-cases", "and:phase-exponent-xor"}, "Local OR compiled-alternative overclaim.")
    require(set(local[0]["route_hyperedges"]) <= edge_ids, "Local alternative route edge missing.")
    require(all(next(e for e in sg["AND_hyperedges"] if e["id"] == i)["heads"] == ["claim:phase-exponent"] for i in local[0]["route_hyperedges"]), "Local OR branches prove different targets.")
    require(len(sg["open_source_gap_ids"]) == 7, "Stronger open consumers silently closed.")
    require(not graph["views"]["lean-graph"]["elaborated_theorem_dependencies"], "Metadata presented as elaborated proof-term dependencies.")
    require(graph["views"]["lean-graph"]["actual_static_source_traces"]["direct_semantic_calls_recursive_root"] is False, "Direct induction conflated with recursive-evaluation root.")
    require(graph["views"]["compressed-quantum-spine"]["purification"] == "PENDING", "PURIFIED overclaim.")
    return {"status": "AUTHOR_STATIC_METADATA_STRUCTURE_PASS_NOT_SEMANTIC_OR_FORMAL_ACCEPTANCE", "source_roots": 87, "public": 79, "private": 8,
            "lossless_paragraphs": 34, "exact_source_atoms": len(atoms), "AND_hyperedges": len(sg["AND_hyperedges"]), "local_proof_OR": 1,
            "full_compiler_verified_alternatives": 0, "SOURCE_GAPs": 7, "F1_F2_F3_author_repairs_only": True}


def negative_tests(coverage, binder, graph, source):
    tests = []
    def reject(name, mutate):
        c, b, g = copy.deepcopy(coverage), copy.deepcopy(binder), copy.deepcopy(graph)
        mutate(c, b, g)
        try:
            audit_metadata(c, b, g, source)
        except (ValueError, KeyError, StopIteration) as error:
            tests.append({"test": name, "result": "REJECTED_EXPECTED", "reason": str(error)})
        else:
            raise AssertionError("Negative mutation unexpectedly accepted: " + name)
    reject("F1 omit target-avoidance Pi input", lambda c, b, g: c["whole_module_inventory"][54]["binder_audit"].pop(4))
    reject("F1 SOURCE guard reclassified TYPING", lambda c, b, g: c["whole_module_inventory"][55]["binder_audit"][4].update(classification="TYPING"))
    reject("F1 invented control injectivity", lambda c, b, g: c["whole_module_inventory"][54]["binder_audit"].append({"classification": "SOURCE", "exact_lexical_binder": "(injective : Function.Injective wires)"}))
    reject("F2 return module-wide coverage projection", lambda c, b, g: c["whole_module_inventory"][8].update(source_regions=["S2", "S3", "S4"]))
    reject("F2 break natural-source quote", lambda c, b, g: c["source_atoms"][0].update(exact_quote="different source"))
    reject("F3 force semantic compiler through recursive evaluation", lambda c, b, g: exact_edge(g, "semantic-compiler-direct")["tails"].append("claim:recursive-evaluation"))
    reject("F3 unitary depends on clean entry", lambda c, b, g: exact_edge(g, "flat-unitarity")["tails"].append("claim:named-wire-clean-entries"))
    reject("F3 wrapper correctness assumes count theorem", lambda c, b, g: exact_edge(g, "verified-wrapper-correctness")["tails"].append("claim:Ry-count"))
    reject("F3 remove wrapper target-normalizer AND tail", lambda c, b, g: exact_edge(g, "verified-wrapper-correctness")["tails"].remove("claim:concrete-target-normalizer-layout"))
    reject("F3 omit head-one exhaustive branch", lambda c, b, g: exact_edge(g, "semantic-compiler-direct")["tails"].remove("claim:head-one-branch"))
    reject("F3 guarded case becomes independently sufficient OR", lambda c, b, g: g["views"]["source-construction-graph"]["guarded_exhaustive_cases"][0].update(alternative_constructions=True))
    reject("F3 XOR option falsely compiled alternate compiler", lambda c, b, g: g["views"]["source-construction-graph"]["local_alternative_proofs"][0].update(compiled_alternative_construction=True))
    reject("F3 conceptual transport loses full AND tail", lambda c, b, g: g["views"]["functor-hypergraph"]["hyperedges"][-1].update(tails=["claim:flat-unitarity"]))
    # Rational/finite counterexamples to interpretations already excluded by
    # the natural source. These are not new native or kernel certificates.
    require(Fraction(2) ** 2 != 1, "Nonunit monomial diagnostic failed.")
    amplitudes = [Fraction(j, 4) ** 3 for j in range(4)]
    require(amplitudes[0] == 0 and sum(a * a for a in amplitudes) == Fraction(397, 2048) != 1, "Finite nonunitary/unnormalized diagnostic failed.")
    repeated_tuples = {(bit, bit) for bit in (0, 1)}
    require((0, 1) not in repeated_tuples and (1, 0) not in repeated_tuples, "Repeated-control consistency diagnostic failed.")
    tests += [
        {"test": "Source counterexample: arbitrary monomial p=2 is not unitary", "result": "FINITE_RATIONAL_SCREEN", "witness": "One-dimensional M=[2], M* M=[4] != [1]."},
        {"test": "Source counterexample: finite diagonal clean block is not unitary/normalized SP", "result": "FINITE_RATIONAL_SCREEN", "witness": "D2 e0=0; coefficient squared norm397/2048 !=1. This does not refute whole-program unitarity."},
        {"test": "Source counterexample: repeated controls cannot expose all independent tuples", "result": "FINITE_ENUMERATION_SCREEN", "witness": "w0=w1 permits only00/11; inconsistent01/10 do not occur, while source theorem requires no injectivity."},
    ]
    return tests


def string_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from string_values(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from string_values(child)


HOST = re.compile(r"(?i)(?<![\w])[a-z]:[\\/][^\s\"<>]*|(?:/Users/|/home/)[^/\s|()\[\]{}]+(?:/|$)|\\\\[A-Za-z0-9_.-]+\\[^\s]+")
SECRET = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_|sk-(?:proj-)?)[A-Za-z0-9_-]{20,}|\bAKIA[A-Z0-9]{16}\b|(?i:bearer)\s+[A-Za-z0-9._-]{24,}")


class Shadow:
    def __init__(self, path, raw): self.path, self.raw = path, raw
    def resolve(self): return self.path.resolve()
    def is_file(self): return True
    def read_bytes(self): return self.raw
    def read_text(self, encoding="utf-8"): return self.raw.decode(encoding)


class Overlay:
    def __init__(self, repo, replacements): self.repo, self.replacements = repo, replacements
    def __fspath__(self): return str(self.repo)
    def resolve(self): return self.repo.resolve()
    def __truediv__(self, name):
        key = str(name)
        return Shadow(self.repo / key, self.replacements[key]) if key in self.replacements else self.repo / key


def verify_package(package, old, repo):
    load = lambda name: json.loads((package / name).read_bytes())
    coverage, binder, graph = (load(name) for name in ("author-source-coverage.json", "author-binder-definition-audit.json", "author-graph-views.json"))
    source = (old / "source-only.md").read_bytes()
    positive = audit_metadata(coverage, binder, graph, source)
    negative = negative_tests(coverage, binder, graph, source)
    stored = load("author-static-tests.json")
    require(stored["positive"] == positive and stored["negative_mutation_tests"] == negative, "Stored author test output differs from read-only replay.")
    seal = load("metadata-v3-seal.json")
    def check(base, pin):
        raw = (base / pin["path"]).read_bytes()
        require(sha(raw) == pin["sha256"] and len(raw) == pin["bytes"], "Immutable pin mismatch: " + pin["path"])
    for pin in seal["old_artifact_hashes_preserved"]:
        check(old, pin)
    for pin in seal["new_artifact_pins"]:
        check(package, pin)
    for pin in seal["whole_ambient_source_pins"] + seal["config_and_external_pins"]:
        check(repo, pin)
    checker = repo / "website/scripts/check_research_publications.py"
    raw = checker.read_bytes()
    require(sha(raw) == seal["checker_sha256"], "Unchanged binding checker pin mismatch.")
    namespace = {"__file__": str(checker), "__name__": "c31_v3_binding_digest_only"}
    exec(compile(raw, str(checker), "exec"), namespace)
    catalog_raw = (repo / "website/research/sources.json").read_bytes()
    require(sha(catalog_raw) == seal["source_catalog_snapshot_sha256"], "Source catalog drift; no reseal.")
    catalog = json.loads(catalog_raw)
    row = json.loads((old / "author-source-row-candidate.json").read_bytes())["source"]
    existing = [r for r in catalog["sources"] if r["id"] == row["id"]]
    require(not existing or existing == [row], "Conflicting source row.")
    if not existing: catalog["sources"].append(row)
    bindings = []
    for stem in ("PrimitiveMacros", "UniformlyControlledRy", "CubicAmplitudePrimitive"):
        candidate = load("publication-candidate-" + stem + ".json")
        replacements = {candidate["lesson_path"]: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()}
        require(namespace["binding_digest"](Overlay(repo, replacements), candidate) == candidate["binding_sha256"], "Prospective binding replay failed.")
        require(not candidate["independent_acceptance"] and not candidate["main_admission"] and not candidate["scientific_ROOT"], "Candidate overclaim.")
        bindings.append({"module": candidate["module"], "binding_sha256": candidate["binding_sha256"]})
    allowlist = load("public-allowlist.json")
    named = set()
    for section in ("new_original_artifacts", "versioned_derivatives"):
        for pin in allowlist[section]:
            require(Path(pin["path"]).name == pin["path"], "Nonlocal new export filename.")
            check(package, pin)
            named.add(pin["path"])
    for pin in allowlist["exact_original_references"]:
        require(pin["path"].startswith("../") and Path(pin["path"][3:]).name == pin["path"][3:], "Unexpected exact reference.")
        check(package, pin)
    public_paths = [package / name for name in named] + [package / "public-allowlist.json"] + [package / p["path"] for p in allowlist["exact_original_references"]]
    for path in public_paths:
        text = path.read_text(encoding="utf-8")
        values = string_values(json.loads(text)) if path.suffix == ".json" else [text]
        for value in values:
            require(not HOST.search(value) and not SECRET.search(value), "Public privacy pattern finding in " + path.name)
    return {"status": "AUTHOR_METADATA_V3_STATIC_REPLAY_PASS_NOT_ADMISSION", "positive": positive, "negative_checks": len(negative),
            "all_predecessor_artifact_hashes_preserved": True, "binding_replays": bindings,
            "public_allowlist_sha256": sha((package / "public-allowlist.json").read_bytes()),
            "metadata_v3_seal_sha256": sha((package / "metadata-v3-seal.json").read_bytes()),
            "decoded_JSON_leaf_privacy_findings": 0, "decoder_CI_runtime_read": False, "Lean_Git_network_executed": False,
            "native_acceptance": False, "independent_acceptance": False, "ROOT_MAIN_PURIFIED": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify_package(args.package.resolve(), args.old.resolve(), args.repo.resolve()), ensure_ascii=False, indent=2))
