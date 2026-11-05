#!/usr/bin/env python3
"""Exclusive sparse metadata-v4 author successor for OPEN-F3-D1 only.

Replay with logical placeholders: --old AUTHOR_PACKAGE_DIRECTORY --out
METADATA_V4_DIRECTORY --repo REPOSITORY_ROOT --reviewer STATIC_REVIEW_DIRECTORY
--recipe AUTHOR_SERIALIZATION_RECIPE. Never overwrites a frozen artifact.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AUTHOR = "/root/primitive_compiler_metadata_c31"
WIP = "AUTHOR_METADATA_V4_SPARSE_WIP_NOT_ADMITTED"
PREFIX = "reviews/publication/primitive-compiler-c31/metadata-v4/"
REVIEW = {"phase2-v3-static-report.md": "520b426f5c2843d3442a4f6e4f2ac7b1a5aeea9108908b32ef2c9f056000308a",
          "phase2-v3-static-seal.json": "899008a641eec2aceb371c168ff57ffe4c4ddb4deca2ce8561efff2c0c863e42"}


def sha(raw): return hashlib.sha256(raw).hexdigest()
def load(path): return json.loads(path.read_bytes())
def pin(path, logical):
    raw = path.read_bytes()
    return {"path": logical, "sha256": sha(raw), "bytes": len(raw)}
def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main(args):
    old, out, repo, reviewer = args.old.resolve(), args.out.resolve(), args.repo.resolve(), args.reviewer.resolve()
    assert out == old / "metadata-v4"
    assert {p.name for p in out.iterdir()} == {"build-sparse-v4.py", "verify-sparse-v4.py"}, "Fresh sparse output only; no overwrite."
    v3 = old / "metadata-v3"
    snapshot = [pin(p, p.relative_to(old).as_posix()) for p in sorted(old.rglob("*")) if p.is_file() and out not in p.parents]
    for name, expected in REVIEW.items(): assert sha((reviewer / name).read_bytes()) == expected
    audit = module(out / "verify-sparse-v4.py", "new_readonly_sparse_checker_only")
    mechanical = module(args.recipe.resolve(), "author_serializer_only")
    emit = lambda name, obj: mechanical.emit(out, name, obj)
    raw_emit = lambda name, raw: mechanical.emit_raw(out, name, raw)
    old_graph_raw = (v3 / "author-graph-views.json").read_bytes()
    assert sha(old_graph_raw) == audit.OLD_GRAPH_SHA
    graph = json.loads(old_graph_raw)
    edge = next(e for e in graph["views"]["source-construction-graph"]["AND_hyperedges"] if e["id"] == audit.TARGET)
    assert audit.TAIL not in edge["tails"]
    edge["tails"].append(audit.TAIL)
    old_graph = json.loads(old_graph_raw)
    sparse = audit.check_sparse(old_graph, graph)
    emit("author-graph-views.json", graph)
    graph_hash = sha((out / "author-graph-views.json").read_bytes())
    emit("graph-path-diff.json", {"status": WIP, "scope": "OPEN-F3-D1_ONLY", "old_graph_sha256": sha(old_graph_raw), "new_graph_sha256": graph_hash,
                                  "json_path_diff": sparse["exact_path_diff"], "strictly_corresponding_functor_consumers": [],
                                  "all_other_graph_JSON_values_unchanged": True, "graph_embedded_metadata_version": "Unchanged v3 marker; v4 projection identity is external so the graph has exactly one JSON-path change.",
                                  "interpretation": "Actual finite-circuit definition calls the compiler; this adds a construction producer edge, not a public theorem hypothesis or a new proof.",
                                  "full_topology_acceptance": False})
    emit("sparse-checks.json", {"positive": sparse, "negative_tests": audit.negative_tests(old_graph, graph), "independent_acceptance": False})
    original_freeze = load(old / "metadata-freeze.json")
    mechanical.assert_current(repo, original_freeze["whole_ambient_binding_inputs"] + original_freeze["strict_config_and_external_inputs"])
    catalog_raw = (repo / "website/research/sources.json").read_bytes()
    catalog = json.loads(catalog_raw)
    source = (old / "source-only.md").read_bytes()
    row = load(old / "author-source-row-candidate.json")["source"]
    existing = [r for r in catalog["sources"] if r["id"] == row["id"]]
    assert not existing or existing == [row]
    if not existing: catalog["sources"].append(row)
    binding, checker_hash = mechanical.binding_function(repo)
    assert checker_hash == original_freeze["checker_sha256"]
    candidates, derivatives = [], []
    derivatives.append({"kind": "ONE_JSON_TAIL_ADDITION_NOT_BYTE_ALIAS", "original_ref": "../metadata-v3/author-graph-views.json", "original_sha256": sha(old_graph_raw),
                        "derived_path": "author-graph-views.json", "derived_sha256": graph_hash, "exact_diff_receipt": "graph-path-diff.json"})
    for stem in ("PrimitiveMacros", "UniformlyControlledRy", "CubicAmplitudePrimitive"):
        name = "publication-candidate-" + stem + ".json"
        prior = load(v3 / name)
        candidate = copy.deepcopy(prior)
        contribution = candidate["graph_contribution"]
        contribution.update(source_graph_sha256=graph_hash, metadata_version=4,
                            sparse_correction_trigger_report_sha256=REVIEW["phase2-v3-static-report.md"],
                            v4_sparse_review_status="PENDING_SAME_ORIGINAL_REVIEWER_NO_PRIOR_VERDICT_INHERITED")
        candidate.update(status=WIP, metadata_version=4, graph_views=PREFIX + "author-graph-views.json",
                         v3_predecessor_binding_sha256=prior["binding_sha256"], v3_predecessor_candidate_sha256=sha((v3 / name).read_bytes()),
                         sparse_correction_scope="OPEN-F3-D1_ONLY_NOT_FULL_TOPOLOGY_ACCEPTANCE",
                         evidence_paths_status="UNATTACHED_PENDING_SPARSE_V4_REVIEW_NO_ACCEPTANCE_INHERITED")
        overlay = mechanical.OverlayRoot(repo, {candidate["lesson_path"]: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()})
        candidate["binding_sha256"] = binding(overlay, candidate)
        emit(name, candidate)
        candidates.append({"module": candidate["module"], "prior_v3_binding_sha256": prior["binding_sha256"], "new_prospective_binding_sha256": candidate["binding_sha256"], "accepted": False})
        derivatives.append({"kind": "SPARSE_GRAPH_REBIND_CANDIDATE_NOT_BYTE_ALIAS", "original_ref": "../metadata-v3/" + name, "original_sha256": sha((v3 / name).read_bytes()),
                            "derived_path": name, "derived_sha256": sha((out / name).read_bytes()),
                            "candidate_JSON_path_diff": audit.pathdiff(prior, candidate), "seven_slot_contract_fields_unchanged": True})
    emit("prospective-bindings.json", {"status": WIP, "bindings": candidates, "source_coverage_binder_formal_context_unchanged": True,
                                       "no_rebinding_of_independent_decoder_or_review_evidence": True, "new_review": "PENDING_SPARSE_V4", "acceptance": False})
    references = ["source-only.md", "source-freeze.json", "author-formal-context.json", "author-source-row-candidate.json", "metadata-v3/author-source-coverage.json",
                  "metadata-v3/author-binder-definition-audit.json", "metadata-v3/author-graph-views.json", "metadata-v3/metadata-v3-seal.json"]
    references += ["metadata-v3/publication-candidate-" + name + ".json" for name in ("PrimitiveMacros", "UniformlyControlledRy", "CubicAmplitudePrimitive")]
    exact_refs = [pin(old / name, "../" + name) for name in references]
    emit("input-references.json", {"status": WIP, "exact_unchanged_references": exact_refs,
                                   "actual_ambient_and_config_pins": original_freeze["whole_ambient_binding_inputs"] + original_freeze["strict_config_and_external_inputs"],
                                   "source_catalog_snapshot_sha256": sha(catalog_raw), "checker_sha256": checker_hash,
                                   "no_large_formal_source_bundle_duplicated": True, "actual_signature_axiom_native_checks": "NOT_PERFORMED"})
    emit("derivative-allowlist.json", {"status": "EXPLICIT_SPARSE_DERIVATIVES_NOT_ORIGINAL_ALIASES", "derivatives": derivatives,
                                       "unchanged_natural_source_coverage_binder_formal_context": True, "old_bindings_preserved": True})
    raw_emit("reviewer-sparse-diff.txt", (
        "C31 metadata-v4: author-only sparse successor for OPEN-F3-D1\n\n"
        "Same author /root/primitive_compiler_metadata_c31; original natural author /root; historical formalizer UNKNOWN. The authorized original-reviewer v3 STATIC report and seal were completely read. No decoder/CI/runtime/native result was read.\n\n"
        "Exactly one graph JSON-path addition: append claim:compiler-definition to and:finite-program-definition.tails. The finite circuit literally invokes the compiler. No strictly corresponding functor consumer exists, so all functor tails remain unchanged. All other graph fields, including the embedded v3 version/provenance marker, remain identical; this package's v4 identity is external.\n\n"
        "Preserved: all32 AND records (31 byte-equivalent JSON records plus the one appended-tail record), all7 OPEN gaps, original local eight-case OR XOR proof option, all-required guarded cases, no full compiler alternative, all seven quantum-slot boundary fields. F1/F2 static findings are not reopened. This is not acceptance of full F3 topology.\n\n"
        "Natural source, formal context, binder and coverage are exact references, not copied big packages. Original source-level87=79 public+8 private and all source/scalar/register/phase/control/workspace/error/resource boundaries remain unmodified. The three publication candidates are explicitly versioned graph-hash rebindings with old/new candidate/binding hashes, not aliases or inherited independent evidence.\n\n"
        "Checks: graph-path-diff.json; sparse-checks.json (one positive sparse equality check plus ten rejected out-of-scope mutations); input-references.json; prospective-bindings.json; derivative-allowlist.json; metadata-v4-seal.json. All are AUTHOR/WIP mechanical evidence only.\n\n"
        "Replay: python verify-sparse-v4.py --package METADATA_V4_DIRECTORY --old AUTHOR_PACKAGE_DIRECTORY --repo REPOSITORY_ROOT\n\n"
        "No existing validator/verifier, scoring, production Lean, natural source, frozen artifact, publication registry or historical binding is edited. No Lean/Git/network/canonical write. F4 generic Props versus concrete actual unitary/clean-entry semantics and F5 native/formal/finite-bit/executable limitations remain. No SourceAgreement, native/formal acceptance, ROOT/MAIN/PURIFIED or full-topology closure is claimed.\n\n"
        "STOP. Return this sparse version to the same original reviewer for separately authorized independent v4 review. Public-safe allowlisting is content classification, not permission to publish or admit.\n"
    ).encode())
    for p in snapshot: assert pin(old / p["path"], p["path"]) == p
    emit("metadata-v4-seal.json", {"status": WIP, "author": AUTHOR, "authorized_static_review_pins": REVIEW, "predecessor_files_preserved": snapshot,
                                  "new_files": [pin(p, p.name) for p in sorted(out.iterdir()) if p.is_file()],
                                  "no_source_binder_coverage_formal_context_changes": True, "scope": "ONE_GRAPH_TAIL_PLUS_PROSPECTIVE_BINDING_DERIVATIVES_ONLY",
                                  "full_F3_topology_acceptance": False, "independent_acceptance": False, "self_hash_excluded": True})
    derived_names = {d["derived_path"] for d in derivatives}
    emit("public-allowlist.json", {"status": "PUBLICSAFE_SPARSE_PRIVATE_WIP_NOT_PUBLICATION_AUTHORITY",
                                   "new_originals": [pin(p, p.name) for p in sorted(out.iterdir()) if p.is_file() and p.name not in derived_names],
                                   "versioned_derivatives": [pin(out / name, name) for name in sorted(derived_names)], "exact_references": exact_refs,
                                   "derivative_receipt": "derivative-allowlist.json", "self_hash_excluded": True,
                                   "no_host_paths": True, "private_original_handoff_not_exported": True,
                                   "standalone_public_verification_of_private_history": False, "independent_acceptance": False})
    print(json.dumps(audit.verify(out, old, repo), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("old", "out", "repo", "reviewer", "recipe"): parser.add_argument("--" + name, required=True, type=Path)
    main(parser.parse_args())
