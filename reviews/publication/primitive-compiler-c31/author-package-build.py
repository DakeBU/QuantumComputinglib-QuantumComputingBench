#!/usr/bin/env python3
"""C31 AUTHOR-only metadata producer; no Lean/Git/network/registry writes.

Inputs are parent-authored natural source and actual complete legacy modules.
The c29 author recipe supplies serialization mechanics only, never mathematics
or independent evidence. New outputs are exclusive bounded apply_patch writes.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AUTHOR = "/root/primitive_compiler_metadata_c31"
WIP = "AUTHOR_WIP_NOT_ADMITTED"
PREFIX = "reviews/publication/primitive-compiler-c31/"
LESSON = "docs/lessons/exact-primitive-macros-controlled-rotations-finite-cubic.md"
SOURCE_ID = "aspbe-local-exact-primitives-controlled-rotations-finite-cubic"
TARGETS = {
    "QuantumBlockEncoding/PrimitiveMacros.lean": "bd5ada5cb61430ea9d32ce1b3adbd84e6b13d8c3fe2c1b6f2758da2a06903664",
    "QuantumBlockEncoding/UniformlyControlledRy.lean": "78d1aed9bb4068bcee138b665bd93a389463bbb591108837758a6d80752a1cf1",
    "QuantumBlockEncoding/CubicAmplitudePrimitive.lean": "48c9a4a1c47c925c93493eede21eb7b492d23d2cb7dadf254782e4485c349cb3",
}
ORIGINAL = {
    "source-only.md": "5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168",
    "author-private-coverage.md": "fc0e1562a93f71f3f45ae594a35d3898e5db9d070e8053bec3f7ae6ad562ff6f",
    "source-freeze.json": "b4a2a5e93b834dd703a126dfb91322c5dd9da5dba490f6dcb06c25b09ab1ad86",
}
RESIDUAL = (
    "Retrospective implementation-informed local mathematics, original natural author /root, historical formalizer UNKNOWN. "
    "Exact full complex matrices/global phases, chronological execution, named wires, possibly noninjective controls and all actual distinctness guards retained. "
    "Reference multiplexor has 2^n Ry and 2(2^n-1) CX, not polynomial cost; zero opaque calls is not zero synthesis/preprocessing cost. "
    "Finite n=2 cubic target is diag((j/4)^3), normalizer one, signal wire2 with flat index j+4s, not rank-one state loading or scalable Hermite preparation. "
    "Generic certificate fields can contain arbitrary propositions; this particular instance uses real unitary and clean-entry theorems. "
    "Exact-real arccos/angles and an angle-placeholder presentation are not finite-bit synthesis or an angle-complete executable emitter. "
    "Independent decoder/topology/source review, actual elaborated signatures and axiom audit, native gates, publication, root admission and purification remain pending."
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def record(path, name, full=False):
    raw = path.read_bytes()
    result = {"path": name, "sha256": digest(raw), "bytes": len(raw)}
    if full:
        result["full_source_lines"] = raw.decode("utf-8").splitlines(keepends=True)
        assert "".join(result["full_source_lines"]).encode() == raw
    return result


def parse_binders(root, mechanical):
    header = root["exact_lexical_header"]
    match = mechanical.ROOT_RE.match(header)
    tail = header[match.end():].lstrip()
    output = []
    while tail and tail[0] in "({[":
        depth, end = [], None
        for index, char in enumerate(tail):
            if char in "({[":
                depth.append(char)
            elif char in ")}]":
                depth.pop()
                if not depth:
                    end = index + 1
                    break
        assert end is not None, root["name"]
        exact = tail[:end]
        logical = bool(re.search(r"≠|∀ control|≤|∈|=", exact))
        classification = "SOURCE" if logical else "TYPING"
        if exact.startswith("["):
            classification = "TYPING"
        bundles = [name for name in ("MonomialProgram", "PrimitiveProgramRefinement", "PrimitiveProgram", "ExactAngle", "OperatorBlockEncodingCandidate", "VerifiedOperatorBlockEncoding", "Resource") if re.search(r"\b" + name + r"\b", exact)]
        output.append({"exact_lexical_binder": exact, "classification": classification,
                       "reason": "Exact wire-separation guard of this conditional local identity; not an added premise of an unconditional preparation theorem." if logical else "Carrier/dimension/wire/index/matrix/phase data or finite enumeration infrastructure; bundled evidence expanded recursively, not silently erased.",
                       "project_owned_bundle_expansions": bundles,
                       "bundle_evidence_policy": "Stored exact evaluation equalities are internal producer evidence, not new SOURCE assumptions of downstream final state/oracle claims." if bundles else None})
        tail = tail[end:].lstrip()
    return output


def source_paragraphs(raw):
    text = raw.decode()
    pieces = re.findall(r"[^\n](?:.*?)(?:\n[ \t]*\n+|\Z)|\n+", text, re.S)
    assert "".join(pieces) == text
    section, offset, line, output = None, 0, 1, []
    for index, piece in enumerate(pieces, 1):
        heading = re.match(r"## (S\d+)\.", piece)
        if heading:
            section = heading[1]
        excluded = piece.lstrip().startswith("#") or not piece.strip() or section is None
        raw_piece = piece.encode()
        output.append({"id": f"paragraph:{index:03d}", "source_region": section,
                       "start_utf8_byte": offset, "end_utf8_byte": offset + len(raw_piece),
                       "source_lines": [line, line + piece.rstrip("\n").count("\n")],
                       "exact_text": piece, "sha256": digest(raw_piece),
                       "disposition": "EXCLUDED" if excluded else "NODE",
                       "reason": "Heading, blank separator or retrospective provenance; no mathematical inference excluded." if excluded else None,
                       "source_nodes": [] if excluded else [f"source:{index:03d}"],
                       "authority": "AUTHOR_PROVISIONAL_NOT_INDEPENDENT"})
        line += piece.count("\n")
        offset += len(raw_piece)
    assert offset == len(raw)
    return output


def region_map(original):
    result = {}
    blocks = re.split(r"(?m)^## ", original.decode())[1:]
    for block in blocks:
        name = block.splitlines()[0].strip()
        found = re.search(r"Module `([^`]+)`, source lines (\d+)–(\d+); (public|private) ([^;]+); natural region (S\d+)(?:–(S\d+))?\.", block)
        assert found, name
        begin, end = int(found[6][1:]), int((found[7] or found[6])[1:])
        result[name] = {"module": found[1], "source_lines": [int(found[2]), int(found[3])],
                        "visibility": found[4], "kind": found[5],
                        "source_regions": [f"S{i}" for i in range(begin, end + 1)],
                        "parent_original_private_record": block}
    assert len(result) == 87
    return result


def bundles_from(root, path, sha):
    body = root["clean_definition_body"]
    fields = []
    if root["kind"] == "structure":
        matches = list(re.finditer(r"^  (?P<name>[\w']+)\s*(?:\([^\n]*\))?\s*:", body, re.M))
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
            field = match["name"]
            text = body[match.start():end].strip()
            proof = field in {"exact", "layoutMatches", "unitaryProof", "blockProof"}
            prop_parameter = field in {"isUnitary", "blockContainsTarget"}
            fields.append({"name": field, "exact_source_field_region": text,
                           "classification": "SOURCE" if proof else "TYPING",
                           "semantic_role": "Stored equality/proof obligation; must be supplied by actual producers in concrete instances." if proof else "Arbitrary proposition parameter, not itself evidence of physical semantics." if prop_parameter else "Stored data/value/carrier/description, not an existence or cost theorem."})
    return {"name": root["name"], "provider_path": path, "provider_sha256": sha,
            "exact_source_region": root["source_block"], "exact_lexical_header": root["exact_lexical_header"],
            "fields": fields, "definition_classification": "literal",
            "recursive_expansions": [], "elaborated_type_inspected": False}


def graph(paragraphs, roots, targets, providers):
    nodes = [{"id": p["source_nodes"][0], "kind": "source-mathematics", "paragraph_id": p["id"],
              "region": p["source_region"], "sha256": p["sha256"], "status": "AUTHOR_PROVISIONAL"}
             for p in paragraphs if p["disposition"] == "NODE"]
    steps = [
        ("wire-lift", [], ["S1"], "One-target context splitting; distinct contexts have zero entries, lifting preserves products/scalars."),
        ("one-qubit-macros", ["wire-lift"], ["S2"], "H=i Ry(pi/2) Rz(pi); P(theta)=exp(i theta/2)Rz(theta); full phase-exact H/T/Tdg programs."),
        ("monomial-composition", [], ["S3"], "M(pR,sigmaR)M(pL,sigmaL)=M(pL(c)pR(sigmaL(c)),sigmaR o sigmaL); arbitrary p, not automatically unitary."),
        ("ccz-phase-network", ["one-qubit-macros", "monomial-composition"], ["S4"], "Pairwise distinct a,b,t; middle permutation identity AND exponent E=4abt give exact CCZ."),
        ("ccx-conjugation", ["ccz-phase-network", "wire-lift"], ["S4"], "H^2=I AND HZH=X AND fixed-context lifting give the exact CCX program/refinement including global phase."),
        ("independent-multiplexor-spec", ["wire-lift"], ["S5"], "Context-selected Ry block specification, every control differs from target; controls need not be injective."),
        ("half-angle-recursion", [], ["S6"], "alpha=(theta0+theta1)/2, delta=(theta0-theta1)/2; emit tail(alpha),CX,tail(delta),CX; zero controls one Ry."),
        ("recursive-evaluation", ["half-angle-recursion"], ["S6"], "List evaluation equals recursive matrix formula by chronological append and induction; not yet the independent specification."),
        ("semantic-multiplexor", ["independent-multiplexor-spec", "half-angle-recursion", "wire-lift"], ["S6"], "Fixed-context cases h=0/h=1, Ry addition AND X Ry(delta) X=Ry(-delta), then reassemble; repeated control wires permitted."),
        ("exponential-reference-cost", ["half-angle-recursion"], ["S7"], "r0=1,c0=0; r(n+1)=2r(n),c(n+1)=2c(n)+2 -> 2^n Ry AND 2(2^n-1)CX; opaque oracle count zero, not polynomial resources."),
        ("finite-cubic-table", [], ["S8"], "n=2, j=b0+2b1; d=(0,1/64,1/8,27/64), exact rational bound; theta=2 arccos(d)."),
        ("finite-cubic-program", ["semantic-multiplexor", "finite-cubic-table"], ["S8"], "Controls wires0,1 target2; program phase0; exact three-wire matrix with Ry selected by cubic value."),
        ("finite-clean-block", ["finite-cubic-program", "finite-cubic-table"], ["S9"], "Encode(s,j)=(j%2,(j/2)%2,s); same context iff r=c AND decoded control index j; arccos entry yields diag((j/4)^3)."),
        ("flat-unitary", ["finite-cubic-program", "finite-clean-block"], ["S9"], "Primitive evaluation unitary AND explicit little-endian equivalence j+4s preserve unitarity and transport clean entries."),
        ("verified-finite-wrapper", ["flat-unitary", "finite-clean-block", "exponential-reference-cost"], ["S9"], "Concrete unitaryProof/blockProof; normalizer1, system2/signal1/pure0; presentation angle placeholders, resource definitionally emitted list."),
    ]
    edges = []
    for key, tails, regions, formula in steps:
        nodes.append({"id": "result:" + key, "kind": "source-construction-step", "formula": formula,
                      "source_regions": regions, "source_paragraphs": [p["id"] for p in paragraphs if p["disposition"] == "NODE" and p["source_region"] in regions],
                      "status": "AUTHOR_PROVISIONAL_NOT_BUILD_EVIDENCE"})
        edges.append({"id": "construction:" + key, "logic": "AND", "tails": ["result:" + k for k in tails],
                      "heads": ["result:" + key], "status": "AUTHOR_PROVISIONAL", "empty_tail_means": "Literal definition/local exact algebra, not stronger physical or complexity closure." if not tails else None})
    gaps = {
        "GENERAL-CUBIC-PRODUCER": "Efficient general-n coherent cubic arithmetic/rotation and full charged resource theorem.",
        "POLYNOMIAL-HERMITE-SP": "Structured polynomial-size Hermite state-preparation construction, not supplied by exponential table multiplexing or finite cubic baseline.",
        "FINITE-BIT": "Uniform numerical angle evaluation, precision/error accumulation and finite-bit/logical synthesis.",
        "NORMALIZED-SP": "Nonzero normalized state-action, accepted probability, postselection/amplification and input preparation.",
        "FULL-RESOURCE": "Preprocessing/table storage, coherent input access, connectivity, scheduling and full ancilla/depth accounting at a matched model.",
        "EXECUTABLE-FAMILY": "Angle-complete emitter, independent saved-circuit replay and family-wide executable acceptance.",
        "INDEPENDENT-ADMISSION": "Independent formal-only decoder, source/topology review, compiler/axiom checks, publication and integration gates; metadata is not acceptance.",
    }
    gapids = ["SOURCE_GAP-" + k for k in gaps]
    nodes.extend({"id": "SOURCE_GAP-" + k, "kind": "SOURCE_GAP", "formula": v, "source_regions": ["S10"],
                  "status": "OPEN_STRONGER_CONSUMER_NOT_REFUTATION"} for k, v in gaps.items())
    cases = [
        {"id": "multiplexor-dimension", "logic": "OR", "guards": ["controls=0", "controls=n+1"], "routes": ["one empty-tuple Ry", "recursive half-sum/half-difference construction"], "exhaustive_case_split": True},
        {"id": "multiplexor-head", "logic": "OR", "guards": ["context(head)=0", "context(head)=1"], "routes": ["Ry(delta)Ry(alpha)", "XRy(delta)XRy(alpha)"], "exhaustive_case_split": True},
        {"id": "context-equality", "logic": "OR", "guards": ["contexts equal", "contexts different"], "routes": ["two-by-two target block", "zero entry"], "exhaustive_case_split": True},
        {"id": "ccz-active", "logic": "OR", "guards": ["a=b=t=1", "not all three one"], "routes": ["phase -1", "phase +1"], "exhaustive_case_split": True},
        {"id": "source-path-separation", "logic": "PARALLEL_OBJECTIVES_NOT_OR_ALTERNATIVES", "routes": ["macro CCX", "controlled Ry compiler", "finite cubic diagonal consumer"], "reason": "Different targets, not alternative sufficient constructions for one common final theorem; no false CCX->cubic edge."},
    ]
    transports = [
        {"id": "transport:monomial-program-composition", "logic": "AND", "tails": ["result:monomial-composition", "result:one-qubit-macros"], "heads": ["result:ccz-phase-network"],
         "formula": "Compose the actual phase/permutation witnesses along the exact chronological middle network.", "hypothesis_map": "Pairwise distinct a,b,t; all exact T/Tdg global phases; full finite basis.", "conclusion_map": "Only the exact CCZ middle matrix.", "failure_boundary": "Arbitrary phasePermutationMatrix is not unitary without additional phase constraints; not approximate equality."},
        {"id": "transport:context-selected-rotation", "logic": "AND", "tails": ["result:independent-multiplexor-spec", "result:half-angle-recursion", "result:wire-lift"], "heads": ["result:semantic-multiplexor"],
         "formula": "Fixed other-wire contexts transport the 2x2 multiplexor identity to the whole register.", "hypothesis_map": "Every selected control differs from target; no control-map injectivity premise; exact real angles and standard half-angle convention.", "conclusion_map": "Full complex matrix equality to backend-independent block specification.", "failure_boundary": "No polynomial table or gate bound, finite-bit implementation or independently realizable inconsistent repeated-control tuple."},
        {"id": "transport:finite-clean-diagonal-wrapper", "logic": "AND", "tails": ["result:finite-clean-block", "result:flat-unitary"], "heads": ["result:verified-finite-wrapper"],
         "formula": "Same explicit little-endian adapter and concrete unitary/clean-entry roots instantiate the generic operator wrapper.", "hypothesis_map": "Two system wires0,1; signal wire2; clean index j+4*0; normalizer1; actual candidate predicates.", "conclusion_map": "Finite diagonal D2 block encoding only.", "failure_boundary": "Not the rank-one cubic operator, normalized state loading, scalable Hermite SP or an angle-complete executable."},
    ]
    for edge in transports:
        edge.update(status="AUTHOR_CONCEPTUAL_NOT_CERTIFIED_FUNCTOR", independent_review="PENDING", source=LESSON, candidate_Lean_substrate=list(TARGETS), certified=False)
    return {"status": WIP, "views": {
        "source-construction-graph": {"status": "AUTHOR_PROVISIONAL_NOT_INDEPENDENT_TOPOLOGY", "nodes": nodes, "AND_hyperedges": edges, "guarded_OR_cases": cases,
                                      "alternative_sufficient_routes": [], "alternative_route_note": "Source states one construction for each target; future efficient consumers remain gaps, not invented verified OR alternatives.",
                                      "open_source_gap_ids": gapids, "independent_topology_review": "PENDING", "root_closure_review": "PENDING"},
        "lean-graph": {"status": "ACTUAL_IMPORT_AND_LEXICAL_OWNERSHIP_ONLY", "import_edges": [{"from": "module:" + p["path"][:-5].replace("/", "."), "to": "module:" + imp, "kind": "actual-module-import"} for p in targets + providers for imp in p["imports"]],
                       "ownership_edges": [{"from": "module:" + r["module"][:-5].replace("/", "."), "to": ("private-helper:" if r["private"] else "declaration:") + r["name"]} for r in roots],
                       "elaborated_theorem_dependencies": [], "lexical_reference_signals": [], "actual_checked_signatures": "PENDING_DECODER", "compiler_generated_inventory": "NOT_INSPECTED"},
        "compressed-quantum-spine": {"status": "AUTHOR_NAVIGATION_PENDING_PURIFICATION", "groups": [
            {"id": "concept:exact-phase-macro", "expands_to": ["result:one-qubit-macros", "result:monomial-composition", "result:ccz-phase-network", "result:ccx-conjugation"]},
            {"id": "concept:context-multiplexed-rotation", "expands_to": ["result:wire-lift", "result:independent-multiplexor-spec", "result:half-angle-recursion", "result:recursive-evaluation", "result:semantic-multiplexor", "result:exponential-reference-cost"]},
            {"id": "concept:finite-cubic-clean-block", "expands_to": ["result:finite-cubic-table", "result:finite-cubic-program", "result:finite-clean-block", "result:flat-unitary", "result:verified-finite-wrapper"]}],
            "lossless_drilldown": [PREFIX + "author-source-coverage.json", PREFIX + "author-formal-context.json"], "purification": "PENDING", "Exposition_Seal": "PENDING"},
        "functor-hypergraph": {"status": "AUTHOR_CONCEPTUAL_NOT_CERTIFIED_FUNCTOR", "hyperedges": transports, "certified_functor": False, "categorical_identity_composition_certificates": []}}}


def main(args):
    repo, out, original = args.repo.resolve(), args.out.resolve(), args.original.resolve()
    recipe = args.recipe.resolve()
    spec = importlib.util.spec_from_file_location("c31_mechanical_recipe_only", recipe)
    mechanical = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mechanical)
    emit = lambda name, obj: mechanical.emit(out, name, obj)
    raw_emit = lambda name, raw: mechanical.emit_raw(out, name, raw)
    assert out.is_dir()
    assert not any(p.name not in {"author-package-build.py", "verify-author-package.py", *ORIGINAL} for p in out.iterdir()), "Exclusive new metadata only; no overwrite/reseal."
    originals = []
    for name, expected in ORIGINAL.items():
        raw = (original / name).read_bytes()
        assert digest(raw) == expected
        if (out / name).exists():
            assert (out / name).read_bytes() == raw, "Frozen original cannot be replaced."
        else:
            raw_emit(name, raw)
        originals.append(record(out / name, name))
    frozen_source = json.loads((out / "source-freeze.json").read_bytes())
    ambient = mechanical.ambient_files(repo)
    assert len(ambient) == 202
    original_ambient = frozen_source["ambient_source_pins"]
    assert len(original_ambient) == 142
    assert [rec for rec in ambient if rec["path"].startswith("QuantumBlockEncoding/")] == original_ambient, "Production ambient drift: STOP_NO_RESEAL"
    mechanical.assert_current(repo, frozen_source["configuration_and_governance_pins"])
    config = [record(repo / p, p, True) for p in ("lean-toolchain", "lake-manifest.json", "lakefile.lean")]
    targets, roots = [], []
    for path, expected in TARGETS.items():
        rec = record(repo / path, path, True)
        assert rec["sha256"] == expected
        rec["imports"] = mechanical.imports("".join(rec["full_source_lines"]))
        targets.append(rec)
        roots += mechanical.inventory(path, (repo / path).read_bytes())
    assert len(roots) == 87 and sum(not r["private"] for r in roots) == 79 and sum(r["private"] for r in roots) == 8
    assert len({r["name"] for r in roots}) == 87
    providers, queue = {}, [imp for rec in targets for imp in rec["imports"]]
    external = set()
    while queue:
        imp = queue.pop()
        if not imp.startswith("QuantumBlockEncoding."):
            external.add(imp)
            continue
        path = imp.replace(".", "/") + ".lean"
        if path in TARGETS or path in providers:
            continue
        rec = record(repo / path, path, True)
        rec["imports"] = mechanical.imports("".join(rec["full_source_lines"]))
        rec["evidence_boundary"] = "Exact raw local provider bytes; not a new review/admission or compile claim."
        providers[path] = rec
        queue.extend(rec["imports"])
    external_records = []
    for imp in sorted(external):
        path = ".lake/packages/mathlib/" + imp.replace(".", "/") + ".lean" if imp.startswith("Mathlib") else None
        external_records.append({"import": imp, "source": record(repo / path, path) if path and (repo / path).is_file() else None,
                                 "boundary": "Direct external import digest and pinned package manifest; not exhaustive transitive Mathlib source or new compilation evidence."})
    ambient_scope = []
    for rec in targets:
        masked = mechanical.mask_comments("".join(rec["full_source_lines"]))
        ambient_scope.append({"module": rec["path"], "commands": [{"line": i + 1, "exact_text": line} for i, line in enumerate(masked.splitlines()) if re.match(r"^(?:import |namespace |end\b|open |set_option |section\b|noncomputable section|variable |universe |scoped |local |notation |attribute )", line)],
                              "private_named_roots": [r["name"] for r in roots if r["module"] == rec["path"] and r["private"]],
                              "scoped_variables": [], "local_notation": [], "explicit_target_instances": [],
                              "scoped_variable_absence_checked_lexically": True,
                              "option_scope": "Two declaration-local maxHeartbeats=2000000 in PrimitiveMacros; no target-level global option rewrite.",
                              "full_module_raw_bytes_retained": True, "implicit_universes_and_typeclass_synthesis": "Actual elaborated expansion pending decoder."})
    formal = {"schema": "c31-complete-formal-only-input-v1", "status": "FORMAL_ONLY_INPUT_NO_ACCEPTANCE", "author": AUTHOR,
              "target_files": targets, "inventory": [{k: v for k, v in r.items() if k not in ("source_block", "clean_definition_body", "exact_lexical_header")} for r in roots],
              "inventory_count": 87, "public_inventory_count": 79, "private_target_helper_count": 8,
              "source_counts_not_compiler_counts": True, "ambient_scope": ambient_scope,
              "provider_index": [providers[p] for p in sorted(providers)], "external_direct_import_index": external_records,
              "dependency_context": config, "type_authority": "Complete exact target/provider source bytes and lexical roots; no actual elaborated types/axioms/build claimed.",
              "fixed_read_boundary": {"targets": list(TARGETS), "providers": "Exact complete local import closure once by source lines, no redundant base64 arrays; necessary definitions inspectable without unseen project Lean.",
                                      "external": "Pinned toolchain/manifest and direct Mathlib import digests; existing compiled shared substrate reused, not duplicate production code.",
                                      "withheld": "Natural source, lesson identity, source catalog row, assumption map, author topology/coverage, independent reconstructions and verdicts."}}
    emit("author-formal-context.json", formal)
    context_sha = digest((out / "author-formal-context.json").read_bytes())
    emit("author-decoder-packet.json", {"status": "FORMAL_ONLY_INPUT_NO_ACCEPTANCE", "formal_context_path": PREFIX + "author-formal-context.json", "formal_context_sha256": context_sha,
                                        "opaque_context_binding_sha256": context_sha, "target_modules": list(TARGETS), "public_count": 79, "private_count": 8,
                                        "inventory_count": 87, "required_work": "Decode every complete public/private authored root, actual elaborated signature and axiom trust; recursively inspect target/provider bundle semantics. Compiler-generated counts must remain separate.",
                                        "fixed_read_boundary": formal["fixed_read_boundary"], "publication_binding_state": "LATE_OPAQUE_BRIDGE_ONLY_AFTER_INDEPENDENT_RECONSTRUCTION_FREEZE"})
    packet_sha = digest((out / "author-decoder-packet.json").read_bytes())
    source = (out / "source-only.md").read_bytes()
    raw_emit(Path(LESSON).name, source)
    paragraphs = source_paragraphs(source)
    mappings = region_map((out / "author-private-coverage.md").read_bytes())
    assert set(mappings) == {r["name"] for r in roots}
    obligations = []
    for i, root in enumerate(roots, 1):
        mapping = mappings[root["name"]]
        assert mapping["module"] == root["module"] and mapping["source_lines"][0] == root["line"]
        assert mapping["visibility"] == ("private" if root["private"] else "public")
        regions = mapping["source_regions"]
        obligations.append({"id": f"C31-{i:03d}", "name": root["name"], "module": root["module"], "line": root["line"], "private": root["private"], "kind": root["kind"],
                            "source_regions": regions, "source_paragraphs": [p["id"] for p in paragraphs if p["disposition"] == "NODE" and p["source_region"] in regions],
                            "lexical_header_for_audit_only": root["exact_lexical_header"], "binder_audit": parse_binders(root, mechanical),
                            "definition_audit": {"kind": "theorem-not-definition" if root["kind"] in ("theorem", "lemma") else "literal", "noncomputable": root["noncomputable"],
                                                 "scope": "Exact whole-carrier formula/recursive program/proof-carrying constructor; no quotient or uniqueness/choice claim.",
                                                 "exact_source_region": root["source_block"], "sha256": root["source_block_sha256"]},
                            "exact_original_private_record": mapping["parent_original_private_record"], "status": WIP,
                            "generated_declarations_boundary": "Source-authored root only; fields/constructors retained in raw bodies, compiler recursors/equation auxiliaries not counted as authored roots."})
    bundle_specs = {
        "QuantumBlockEncoding/PrimitiveMacros.lean": ["MonomialProgram"],
        "QuantumBlockEncoding/PrimitiveCircuit.lean": ["ExactAngle", "PrimitiveGate", "PrimitiveCircuit", "PrimitiveProgram"],
        "QuantumBlockEncoding/PrimitiveSemantics.lean": ["PrimitiveBasis", "OtherPrimitiveWires", "PrimitiveRefinement"],
        "QuantumBlockEncoding/PrimitiveRefinement.lean": ["PrimitiveProgramRefinement"],
        "QuantumBlockEncoding/BlockEncoding.lean": ["RegisterLayout", "QueryOperatorTarget", "OperatorBlockEncodingCandidate", "VerifiedOperatorBlockEncoding"],
        "QuantumBlockEncoding/Resources.lean": ["Resource"],
    }
    bundles = {}
    for path, names in bundle_specs.items():
        for root in mechanical.inventory(path, (repo / path).read_bytes()):
            if root["lexical_local_name"] in names:
                bundles[root["name"]] = bundles_from(root, path, digest((repo / path).read_bytes()))
    links = {
        "MonomialProgram": ["PrimitiveProgram", "PrimitiveBasis"], "PrimitiveProgramRefinement": ["PrimitiveProgram", "PrimitiveBasis"],
        "PrimitiveProgram": ["PrimitiveCircuit", "ExactAngle"], "PrimitiveCircuit": ["PrimitiveGate"], "PrimitiveGate": ["ExactAngle"],
        "VerifiedOperatorBlockEncoding": ["OperatorBlockEncodingCandidate"], "OperatorBlockEncodingCandidate": ["QueryOperatorTarget", "RegisterLayout", "Resource"],
    }
    for bundle in bundles.values():
        bundle["recursive_expansions"] = ["QuantumBlockEncoding." + key for key in links.get(bundle["name"].split(".")[-1], [])]
    manual = {"MonomialProgram.exact": "evalPrimitiveProgram program = phasePermutationMatrix phase permutation. Input certificates seq/cx/t/tdg use produced semantic equalities; arbitrary phase function not automatically unitary.",
              "PrimitiveProgramRefinement.exact": "evalPrimitiveProgram program = target, exact full global-phase-sensitive equality, not modulo phase.",
              "ExactAngle.constructor_proof_fields": [{"constructor": "twiceArccosRational", "field": "bounded : |(value : Real)| ≤ 1", "classification": "SOURCE", "supplier": "Finite cubicN2Amplitude_abs_le_one in the concrete cubic definition, not a final user theorem assumption."},
                                                        {"constructor": "twiceArccosSqrtRational", "field": "bounded : 0 ≤ (value : Real) ∧ (value : Real) ≤ 1", "classification": "SOURCE", "supplier": "Not used by this concrete cubic angle, included to keep ambient ExactAngle carrier whole."}],
              "PrimitiveGate.cx.distinct": "SOURCE guard control != target; no injectivity requirement among an arbitrary list of controls.",
              "OperatorBlockEncodingCandidate": "isUnitary and blockContainsTarget are arbitrary Prop DATA parameters; layoutMatches proves only layout count consistency. Concrete cubic candidate instantiates actual Matrix.unitaryGroup and clean-entry / normalizer predicates.",
              "VerifiedOperatorBlockEncoding": "unitaryProof : candidate.isUnitary AND blockProof : candidate.blockContainsTarget. Concrete cubic verified wrapper uses cubicN2PrimitiveFlatUnitary_unitary and cubicN2PrimitiveFlatUnitary_cleanBlock, not true metadata.",
              "cubic_target": "operator(r,c)=Rat-to-Complex diagonal (r/4)^3; normalizer1; freeParameters default []; descriptive strings not additional premises.",
              "resource": "PrimitiveProgram.resource=program.circuit.resource; ofCountsWithDepth oneQubitCount twoQubitCount oracle0 pure0 depth; exact-real logical count only.",
              "control_aliasing": "No SOURCE binder wires injective exists; repeated controls yield only context-consistent tuples. Final CCX network has a!=b,a!=t,b!=t; ccz/ccx target blocks and conjugation only require a!=t,b!=t.",
              "private_helpers": "All eight explicit private roots covered; mathematical source-level names, not actual compiler-mangled names. Actual types/axioms pending.",
              "EXCESS": "No newly introduced theorem binder; author provisional classifications only, independent recursive binder audit remains pending."}
    emit("author-binder-definition-audit.json", {"status": WIP, "author": AUTHOR, "whole_module_inventory": [{k: v for k, v in o.items() if k in ("id", "name", "module", "kind", "private", "binder_audit", "definition_audit")} for o in obligations],
                                                   "project_owned_bundle_expansions": bundles, "manual_recursive_semantics": manual, "classification_authority": "AUTHOR_PROVISIONAL_NOT_INDEPENDENT", "original_private_coverage_unchanged": True})
    coverage = {"status": WIP, "author": AUTHOR, "original_source_author": "/root", "historical_formalizer": "UNKNOWN", "source_sha256": ORIGINAL["source-only.md"],
                "source_paragraphs": paragraphs, "whole_module_inventory": obligations, "source_named_roots": 87, "public_roots": 79, "private_helpers": 8,
                "source_region_coverage": "All source bytes partitioned losslessly; every substantive formula/construction/proof paragraph NODE; navigation/provenance only EXCLUDED with reasons.",
                "independent_source_topology": "PENDING", "remaining_boundary": RESIDUAL}
    emit("author-source-coverage.json", coverage)
    views = graph(paragraphs, roots, targets, list(providers.values()))
    emit("author-graph-views.json", views)
    row = {"id": SOURCE_ID, "title": "Exact elementary macros, controlled rotations, and a finite cubic baseline", "authors": "Retrospective natural source /root; metadata " + AUTHOR + "; historical formalizer UNKNOWN",
           "url": "https://github.com/DakeBU/Quantum-Computing-Block-Encoding", "year": 2026, "status": "primary-text-checked",
           "anchor": LESSON + " sections S1–S10; exact source SHA256 " + ORIGINAL["source-only.md"],
           "scope": "Whole PrimitiveMacros, UniformlyControlledRy and CubicAmplitudePrimitive; 87 source-named roots =79 public+8 private, not compiler-generated declaration counts.",
           "formal_status": "AUTHOR/WIP retrospective local recovery only; not independent acceptance, fresh compile, historical pre-proof seal, root admission or PURIFIED."}
    emit("author-source-row-candidate.json", {"status": WIP, "source": row})
    catalog_raw = (repo / "website/research/sources.json").read_bytes()
    catalog = json.loads(catalog_raw)
    assert not any(s["id"] == SOURCE_ID for s in catalog["sources"])
    catalog["sources"].append(row)
    overlay = mechanical.OverlayRoot(repo, {LESSON: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()})
    binding, checker_sha = mechanical.binding_function(repo)
    candidates = []
    for path in TARGETS:
        own = [o for o in obligations if o["module"] == path and not o["private"]]
        contribution = {"baseline": "f2cba045611a0d11c5995c29607569726bf1d6c5", "head": "40d7904", "head_provenance": "Parent-supplied checkpoint context only; this author executed no Git.",
                        "classes": ["reorganisation", "bridge"], "node_ids": ["module:" + path[:-5].replace("/", ".")] + ["declaration:" + o["name"] for o in own],
                        "views": list(views["views"]), "source_graph_sha256": digest((out / "author-graph-views.json").read_bytes()),
                        "coverage_sha256": digest((out / "author-source-coverage.json").read_bytes()), "formal_context_sha256": context_sha, "formal_packet_sha256": packet_sha,
                        "source_graph_authority": "AUTHOR_PROVISIONAL_NOT_INDEPENDENT", "preserved_contract": "Whole source unchanged; source recovery/metadata only; no new mathematical theorem or main admission.", "remaining_boundary": RESIDUAL}
        candidate = {"module": path, "source_id": SOURCE_ID, "source_statement": "Frozen retrospective local source S1–S10; exact phase-preserving H/T/Tdg/CCX, independent context-selected Ry compiler and exponential counts, finite n=2 cubic diagonal clean block. Whole module, private and ambient scope retained.",
                     "source_anchor": LESSON + " sections S1–S10", "lesson_path": LESSON, "declarations": [o["name"] for o in own],
                     "obligation_map": [{"kind": "proof-edge" if o["kind"] in ("theorem", "lemma") else "prerequisite", "source_obligation": o["id"], "declarations": [o["name"]]} for o in own],
                     "assumption_deltas": [{"classification": "same", "source": "Exact full complex phases; chronological gates; actual wire distinctness and possibly repeated controls; finite diagonal n=2 target and exact-real exponential reference counts.",
                                            "formal": "All 87 source-named public/private roots and complete local source context; final CCX stronger separation not inserted into weaker intermediate block identities.", "explanation": "Retrospective source states the actual local mathematics; no proof ingredients moved into an unconditional preparation theorem."},
                                           {"classification": "source-implicit", "source": "Named-wire semantics with explicit LE transport j+4s for finite cubic; generic certificate Prop fields interpreted by concrete instance.", "formal": "Cubic normalizer1, system2/signal1/pure0, real primitive unitary/clean-entry roots, placeholder presentation angles and exact resource ownership retained.", "explanation": "No new finite-bit producer, angle-complete QASM export, scalable state preparation or stronger resource rung inferred."}],
                     "graph_contribution": contribution, "formalizer": AUTHOR + " retrospective metadata author; historical formalizer UNKNOWN", "historical_formalizer": "UNKNOWN", "original_natural_author": "/root",
                     "residual_boundary": RESIDUAL, "decoder_evidence": PREFIX + "decoder-pending/" + Path(path).stem + "-evidence.json", "reviewer_evidence": PREFIX + "reviewer-pending/" + Path(path).stem + "-evidence.json",
                     "evidence_paths_status": "UNATTACHED_NOT_INSPECTED_NOT_FABRICATED", "status": WIP, "statement_seal": {"timing": "RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS", "pre_proof_seal_claim": False},
                     "source_proof_coverage": PREFIX + "author-source-coverage.json", "binder_definition_audit": PREFIX + "author-binder-definition-audit.json", "graph_views": PREFIX + "author-graph-views.json",
                     "formal_context": PREFIX + "author-formal-context.json", "formal_packet": PREFIX + "author-decoder-packet.json", "purification": {"status": "PENDING", "Exposition_Seal": "PENDING"},
                     "independent_acceptance": False, "main_admission": False, "scientific_ROOT": False}
        candidate["binding_sha256"] = binding(overlay, candidate)
        emit("publication-candidate-" + Path(path).stem + ".json", candidate)
        candidates.append({"module": path, "binding_sha256": candidate["binding_sha256"]})
    emit("author-binding-bridge-proposal.json", {"status": WIP, "formal_context_sha256": context_sha, "formal_packet_sha256": packet_sha, "bindings": candidates,
                                                "procedure": "Parent may attach opaque bridge only AFTER distinct formal-only decoder has independently frozen reconstruction. No author-side independent result inspected or accepted.", "accepted": False})
    emit("formal-input-seal.json", {"status": "FORMAL_ONLY_FROZEN_NOT_ACCEPTANCE", "formal_context_sha256": context_sha, "formal_packet_sha256": packet_sha,
                                    "target_bindings": [{k: v for k, v in rec.items() if k in ("path", "sha256", "bytes")} for rec in targets],
                                    "provider_closure_modules": len(providers), "public_roots": 79, "private_helpers": 8, "authored_named_roots": 87,
                                    "whole_ambient_files": 202, "dependency_context": [{k: v for k, v in rec.items() if k in ("path", "sha256", "bytes")} for rec in config]})
    registry_raw = (repo / "website/research/publications.json").read_bytes()
    registry = json.loads(registry_raw)
    assert len(registry["records"]) == 23
    assert all(rec["module"] not in TARGETS for rec in registry["records"])
    strict = frozen_source["configuration_and_governance_pins"] + [rec["source"] for rec in external_records if rec["source"]]
    mechanical.assert_current(repo, ambient + strict)
    assert (repo / "website/research/sources.json").read_bytes() == catalog_raw
    emit("metadata-freeze.json", {"status": WIP, "author": AUTHOR, "original_natural_author": "/root", "historical_formalizer": "UNKNOWN", "original_immutable_inputs": originals,
                                  "new_artifacts": [record(p, p.name) for p in sorted(out.iterdir()) if p.is_file() and p.name not in ORIGINAL],
                                  "whole_ambient_binding_inputs": ambient, "strict_config_and_external_inputs": strict,
                                  "checker_path": "website/scripts/check_research_publications.py", "checker_sha256": checker_sha,
                                  "source_catalog_path": "website/research/sources.json", "source_catalog_sha256": digest(catalog_raw),
                                  "registry_path": "website/research/publications.json", "registry_sha256": digest(registry_raw), "registry_observed_count": 23,
                                  "format_recipe": {"path": "cubic-source-author-c29/author-package-build.py", "sha256": digest(recipe.read_bytes()), "use": "Mechanical serialization/inventory/unchanged binding function only; no old mathematics or independent results ingested."},
                                  "process_memory_ids_consulted": ["QBE-PM-LOW-TOKEN-CONTROL-PLANE", "QBE-PM-VERIFIER-SEMANTIC-LEVEL"],
                                  "new_source_roots": 87, "public_roots": 79, "private_helpers": 8,
                                  "emission": "Exclusive new apply_patch artifacts only; parent source trio untouched; full raw target/provider source lines stored once.",
                                  "independent_evidence_fabricated": False, "production_writes": False, "Lean_executed": False, "Git_executed": False, "network_executed": False,
                                  "acceptance": False, "main_admission": False, "scientific_ROOT": False, "PURIFIED": False, "self_hash_excluded": True})
    emit("outputs-manifest.json", {"status": WIP, "artifacts": [dict(record(p, p.name), planned_canonical_path=LESSON if p.name == Path(LESSON).name else PREFIX + p.name) for p in sorted(out.iterdir()) if p.is_file()],
                                   "planned_prefix": PREFIX, "lesson_path": LESSON, "manifest_self_hash_excluded": True, "independent_acceptance": False, "main_admission": False})
    print(json.dumps({"status": WIP, "formal_context_sha256": context_sha, "formal_packet_sha256": packet_sha, "provider_modules": len(providers), "bindings": candidates,
                      "manifest_sha256": digest((out / "outputs-manifest.json").read_bytes())}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--recipe", required=True, type=Path)
    main(parser.parse_args())
