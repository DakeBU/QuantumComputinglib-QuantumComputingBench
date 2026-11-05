#!/usr/bin/env python3
"""Versioned AUTHOR metadata-only F1/F2/F3 successor; no old file replacement.

Logical replay: python build-metadata-v3.py --repo REPOSITORY_ROOT --old
AUTHOR_PACKAGE_DIRECTORY --reviewer STATIC_REVIEW_DIRECTORY --recipe
AUTHOR_SERIALIZATION_RECIPE --out METADATA_V3_DIRECTORY
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
AUTHOR = "/root/primitive_compiler_metadata_c31"
PREFIX = "reviews/publication/primitive-compiler-c31/metadata-v3/"
WIP = "AUTHOR_METADATA_V3_WIP_NOT_ADMITTED"
REVIEW = {"phase2-static-report.md": "da7c6a36d1a45b57d0dc1d8a204656ed97a93a24f5e628b028bbe6e3e9fe05c5",
          "phase2-static-seal.json": "88227580b575d7952bb1ba0b7817a05374d9194d98c4f8166db3046b0dea0f64"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def rec(path, logical):
    raw = path.read_bytes()
    return {"path": logical, "sha256": sha(raw), "bytes": len(raw)}


# Authored from the unchanged natural text, not the reviewer's Nxx mapping.
# Each anchor is an exact substring of its paragraph; no reviewer node is used.
ATOM_PLAN = {
 "chronology": (4, "For gates listed in temporal order", "times that product.", "Chronological gate evaluation and exp(i phase) program denotation."),
 "angle-standing": (4, "An exact angle is symbolic", "approximation algorithm.", "Exact-angle mathematical evaluation; no numerical oracle or finite-bit promise."),
 "standard-matrices": (5, "Use the standard matrices", "\\]", "Standard half-angle Ry, Rz and X with exact complex phase."),
 "lift": (6, "Splitting off a target wire", "used below.", "Fixed-context lifting, multiplication and scalar transport."),
 "H-definition": (8, "H=i", "R_z(\\pi),", "Literal H=i Ry(pi/2) Rz(pi)."),
 "P-definition": (8, "P(\\theta)=", "R_z(\\theta).", "Literal phase-compensated phase gate P(theta)."),
 "H-entries": (8, "H=\\frac", "\\end{pmatrix},", "Exact Hadamard entries sqrt(2)/2 and their signs."),
 "P-entries": (8, "P(\\theta)=\\operatorname", "e^{i\\theta}).", "Diagonal entries 1 and exp(i theta)."),
 "H-program": (8, "The exact H program lists", "phase π/2.", "Temporal Rz then Ry and phase pi/2."),
 "T-programs": (8, "The exact T and inverse-T programs", "respectively.", "T and inverse-T: signed Rz and global phases separately retained."),
 "macro-evaluation": (8, "Temporal composition and the lifting identities", "matrix equalities.", "Full-register exact macro evaluation, not probability equivalence."),
 "monomial-definition": (10, "On a finite index set", "automatically a unitary matrix.", "Arbitrary complex monomial phase and permutation; no unit-modulus premise."),
 "monomial-product": (10, "If a left program executes", "without an appeal to a simulator.", "Chronological phase/permutation composition and unique surviving summand."),
 "cx-monomial": (11, "A controlled-X is such a matrix", "controlled-flip permutation.", "CX phase-one monomial identity."),
 "phase-monomial": (11, "A phase P(θ) on target t", "when it is one.", "Lifted phase gate as identity-permutation monomial."),
 "monomial-record": (11, "A proof-carrying monomial program stores", "equality of their matrices.", "All four MonomialProgram fields, including actual evaluation equality."),
 "monomial-seq": (11, "Its sequential constructor derives", "oracle contract holds.", "Produced exact equality from both input witnesses and monomial multiplication."),
 "middle-list": (13, "Take three pairwise distinct wires", "CX_{a,b}.\n\\]", "Literal 13-step pairwise-distinct phase network."),
 "middle-permutation": (13, "The four flips of t restore t", "permutation is identity.", "Target/control flips restore the complete basis assignment."),
 "middle-exponent": (13, "For initial bits a,b,t", "-(b\\oplus a).\n\\]", "Accumulated exponent E, retaining exact T/Tdg phases."),
 "E-local-OR": (13, "Checking the eight bit triples", "gives E=4abt.", "Source-local alternative proofs of E=4abt: exhaustive eight cases OR XOR polynomial expansion."),
 "ccz-phase": (13, "The middle matrix is therefore diagonal", "exact T and inverse-T programs.", "CCZ sign only on all-one triple, all macro phases included."),
 "ccx-composition": (14, "Conjugate that middle program", "H program on t.", "Literal H-middle-H chronology."),
 "target-blocks": (14, "For each fixed other-wire assignment", "identity otherwise.", "Active target block Z, inactive target block identity."),
 "H-identities": (14, "Direct two-by-two multiplication", "H²=I and HZH=X.", "Two exact 2x2 conjugation identities, not phase quotients."),
 "ccx-equality": (14, "Block-diagonal multiplication then gives", "on all basis states.", "Whole exact controlled-controlled-X permutation matrix."),
 "refinement": (14, "The program and its proof-carrying refinement", "controlled-X primitives.", "Proof-carrying primitive refinement, not merely a logical label."),
 "weaker-guards": (15, "Some intermediate block identities", "every intermediate identity.", "Two target inequalities for block/conjugation lemmas, three pairwise guards for final network."),
 "control-assignment": (17, "For any assignment x", "two-dimensional block.", "Read actual physical context along the control-wire map."),
 "control-domain": (17, "Let w map n control positions", "n-bit control tuple.", "All source-specified control/target/table data and only target-avoidance guard; noninjective controls allowed."),
 "consistent-tuples": (18, "With repeated control wires", "independently occur.", "Only consistent tuples arise from physical contexts; no injectivity hypothesis."),
 "zero-block": (18, "For zero controls", "single Ry gate.", "Unique empty-tuple specification equals lifted Ry."),
 "cx-block": (18, "A controlled-X similarly", "target/context splitting.", "Controlled-X context block is I or X, established entrywise."),
 "angle-split": (20, "For a nonempty tuple split", "\n\\]", "Prepend head bit and exact half-sum/half-difference tables."),
 "compiler-list": (20, "Execute recursively the tail-controlled", "recursion is well-typed.", "Chronological alpha,CX,delta,CX recursive construction and inherited target avoidance."),
 "recursive-denotation": (20, "A separate recursive matrix formula", "that recursive formula.", "Separate recursive matrix definition and emitted-list evaluation induction."),
 "direct-semantic": (21, "To establish the independent specification", "map is unnecessary.", "Direct fixed-context semantic induction, both head cases and exact Ry/X identities; not a call to recursive-denotation theorem."),
 "count-formulas": (23, "Let r(n) and c(n)", "c(n)=2(2^n-1).\n\\]", "Separate emitted-list count recurrences and their exponential solutions."),
 "five-counts": (23, "At five controls", "32 and 62.", "Specialization of Ry/CX count conjunction to five control positions."),
 "oracle-zero": (23, "The emitted primitive language", "count is zero.", "Resource definition has no opaque oracle instruction; no efficiency inference."),
 "finite-wires": (25, "Now fix exactly two little-endian", "wire 2.", "System control wires0,1 and signal wire2, finite width only."),
 "finite-index-table": (25, "If the system bits are b0,b1", "27/64\\}.\n\\]", "j=b0+2b1 and the four rational cubic amplitudes."),
 "finite-bound": (25, "These four rational values", "lie in [0,1].", "Four-input rational range proof, not sample-inferred arbitrary-n bound."),
 "finite-angle": (25, "Select the exact standard-Ry angle", "wire 2 as target.", "Construct exact arccos angle with bound supplied internally and compile two controls."),
 "finite-phase": (25, "The program's explicit global phase", "is zero.", "Literal zero global phase of the finite program."),
 "finite-matrix": (26, "The compiler theorem gives", "controlled block diagonal.", "Finite emitted program has the independent controlled-Ry matrix."),
 "encoding": (28, "Encode (s,j)", "floor(j/2) mod 2, s).", "Literal named-wire signal/system encoding."),
 "encoding-identities": (28, "Extracting the two controls", "their signal values.", "Control decoding recovers j and context equality iff system indices agree."),
 "clean-entry": (28, "These finite encoding identities", "state-loading operator.", "Exact clean-signal cubic DIAGONAL entry formula, not rank-one state loading."),
 "primitive-unitarity": (28, "The ambient matrix is genuinely unitary", "unitary on the system.", "Program evaluation is unitary independently of its clean-block identity."),
 "LE-equivalence": (29, "The separately proved little-endian", "flat integer j+4s.", "Explicit named-wire to flat LE basis adapter."),
 "flat-transport": (29, "Reindexing the whole unitary", "transports the clean entries.", "Separate reindex preservation of unitarity and inverse-law transport of entries."),
 "target-layout": (29, "The operator target has normalizer one", "additional pure workspace.", "Literal normalizer1/system2/signal1/pure0 target/layout data."),
 "wrapper-proofs": (29, "The verified wrapper is supplied", "Boolean metadata flag.", "Concrete unitary AND clean-entry producer theorems instantiate actual candidate predicates."),
 "presentation": (30, "The human circuit presentation", "QASM emitter.", "Gate/wire presentation discards exact angle values; no executable refinement."),
 "resource-ownership": (30, "The resource row is definitionally", "field is zero.", "Resource ownership and oracle zero are separate from wrapper correctness and list-count theorems."),
 "finite-counts": (30, "The generic reference formulas", "six controlled-X gates.", "Mathematical reference specialization 4 Ry/6 CX; no new named compiled root."),
 "consumer-boundaries": (30, "Neither the presentation wrapper", "executable acceptance theorem.", "No normalized SP, success/amplification, finite-bit synthesis or family executable consequence."),
 "private-providers": (33, "Private helpers for prepending", "external source results.", "Internal helper role, not independent external source credit."),
 "open-consumers": (34, "Open consumers are", "stronger goals.", "All stronger scientific/implementation consumers stay open."),
}


# Exactly 87 primary source links, individually authored from statement roles.
# The tuple order is the already frozen authored-root order, not compiler output.
ROOT_LINKS = [
 ("H-definition",), ("P-definition",), ("H-entries",), ("P-entries",),
 ("H-program",), ("T-programs",), ("T-programs",), ("chronology", "H-program"),
 ("lift",), ("lift",), ("macro-evaluation", "H-program"), ("macro-evaluation", "T-programs"), ("macro-evaluation", "T-programs"),
 ("monomial-definition",), ("monomial-product",), ("cx-monomial",), ("phase-monomial", "lift"),
 ("cx-monomial", "chronology"), ("cx-monomial",), ("phase-monomial", "T-programs"), ("phase-monomial", "T-programs"),
 ("monomial-record",), ("monomial-seq",), ("cx-monomial", "monomial-record"), ("phase-monomial", "T-programs"), ("phase-monomial", "T-programs"),
 ("middle-list",), ("ccx-composition",), ("middle-permutation",), ("middle-exponent", "E-local-OR", "ccz-phase"),
 ("ccz-phase",), ("middle-permutation", "ccz-phase"), ("target-blocks",), ("H-identities",), ("H-identities",),
 ("lift",), ("target-blocks", "weaker-guards"), ("target-blocks", "weaker-guards"), ("ccx-equality", "weaker-guards"),
 ("ccx-equality", "weaker-guards"), ("H-identities", "ccx-equality", "weaker-guards"), ("ccx-equality", "weaker-guards"), ("refinement", "ccx-equality"),
 ("angle-split", "private-providers"), ("angle-split", "private-providers"), ("angle-split", "private-providers"),
 ("control-assignment",), ("control-domain", "control-assignment"), ("control-assignment", "lift"),
 ("lift", "zero-block"), ("zero-block",), ("cx-block",), ("cx-block",), ("cx-block",),
 ("compiler-list", "control-domain"), ("recursive-denotation", "control-domain"), ("recursive-denotation",), ("direct-semantic",),
 ("count-formulas",), ("count-formulas",), ("oracle-zero",), ("five-counts",),
 ("finite-wires",), ("finite-wires",), ("finite-index-table",), ("finite-bound",), ("finite-angle", "finite-bound"),
 ("finite-angle", "finite-wires"), ("finite-phase",), ("finite-matrix",), ("finite-matrix", "finite-phase"),
 ("encoding",), ("encoding",), ("encoding-identities",), ("encoding-identities",), ("clean-entry", "encoding-identities"),
 ("LE-equivalence", "flat-transport"), ("primitive-unitarity", "flat-transport"), ("LE-equivalence", "encoding"),
 ("clean-entry", "flat-transport"), ("clean-entry", "target-layout"), ("presentation",), ("resource-ownership",),
 ("target-layout", "wrapper-proofs", "presentation", "resource-ownership"), ("wrapper-proofs",), ("resource-ownership",), ("resource-ownership",),
]


def source_atoms(paragraphs):
    result = {}
    for name, (number, start, ending, meaning) in ATOM_PLAN.items():
        paragraph = paragraphs[number - 1]
        assert paragraph["id"] == f"paragraph:{number:03d}" and paragraph["disposition"] == "NODE"
        text = paragraph["exact_text"]
        begin = text.index(start)
        end = text.index(ending, begin) + len(ending)
        quote = text[begin:end]
        absolute = paragraph["start_utf8_byte"] + len(text[:begin].encode())
        result[name] = {"id": "natural:" + name, "source_paragraph": paragraph["id"], "source_region": paragraph["source_region"],
                        "exact_quote": quote, "sha256": sha(quote.encode()), "start_utf8_byte": absolute,
                        "end_utf8_byte": absolute + len(quote.encode()), "mathematical_role": meaning,
                        "authority": "AUTHOR_RELINKING_FROM_UNCHANGED_NATURAL_SOURCE_NOT_INDEPENDENT_REVIEW"}
    return result


def pi_binders(old):
    result = copy.deepcopy(old[:1])
    data = [
        ("controls", "(controls : Nat)", "TYPING", "Source-specified number of control positions, not count of distinct physical controls."),
        ("wires", "(wires : Fin controls → Fin qubits)", "TYPING", "Source-specified map of control positions to physical wires; not assumed injective."),
        ("target", "(target : Fin qubits)", "TYPING", "Source-specified target wire in the finite carrier."),
        ("target-avoidance", "(∀ control, wires control ≠ target)", "SOURCE", "Actual anonymous Pi proof argument, target avoidance at every control position. No control-control injectivity premise."),
        ("angles", "(PrimitiveBasis controls → ExactAngle)", "TYPING", "Actual anonymous Pi table-data argument; audit label angles does not invent a Lean binder name."),
    ]
    for label, syntax, classification, reason in data:
        result.append({"audit_label": label, "exact_lexical_binder": syntax, "syntax_origin": "RESULT_TYPE_DEPENDENT_PI_AFTER_COLON",
                       "classification": classification, "source_data_role": "SOURCE_SPECIFIED_DATA_WITH_TYPING_ROLE" if classification == "TYPING" else "SOURCE_LOGICAL_GUARD",
                       "reason": reason, "standing_source_semantics": "ExactAngle.eval uses the standard mathematical real/half-angle convention, not a numerical access assumption." if label == "angles" else None,
                       "actual_elaborated_type": "NOT_INSPECTED"})
    return result


def make_graph(old_graph, atoms):
    graph = copy.deepcopy(old_graph)
    graph["status"] = WIP
    sg = {"status": "AUTHOR_SOURCE_TOPOLOGY_V3_PENDING_DISTINCT_REVIEW", "nodes": [], "AND_hyperedges": [],
          "guarded_exhaustive_cases": [], "local_alternative_proofs": [], "full_compiler_alternative_routes": [],
          "source_narrative_order_not_implication": ["claim:recursive-evaluation", "claim:semantic-compiler"],
          "independent_review_of_v3": "PENDING", "elaborated_dependencies_claimed": False}
    for atom in atoms.values():
        sg["nodes"].append({"id": atom["id"], "kind": "natural-source-atom", "paragraph": atom["source_paragraph"], "sha256": atom["sha256"]})
    # Preserve disposition nodes for all substantive source paragraphs, even
    # topology summaries/open boundaries that are not standalone Lean roots.
    sg["nodes"] += [copy.deepcopy(n) for n in old_graph["views"]["source-construction-graph"]["nodes"] if n["kind"] == "source-mathematics"]
    def node(name, meaning, kind="source-claim", status="AUTHOR_PROVISIONAL"):
        identifier = "claim:" + name
        sg["nodes"].append({"id": identifier, "kind": kind, "meaning": meaning, "status": status})
        return identifier
    def edge(name, tails, head, source, layer="source-construction"):
        sg["AND_hyperedges"].append({"id": "and:" + name, "logic": "AND", "tails": tails, "heads": [head],
                                     "source_atoms": ["natural:" + s for s in source], "layer": layer,
                                     "authority": "AUTHOR_STATIC_METADATA_NOT_KERNEL_DEPENDENCY"})
    def inputs(name, meaning):
        return node(name, meaning, "local-proof-schema-input-not-public-theorem-binder")
    lift = node("wire-lift", "Fixed non-target contexts, lifted multiplication/scalar identities.")
    edge("wire-lift", ["natural:lift"], lift, ["lift"])
    macros = node("exact-macros", "Exact H/T/Tdg full-register matrices including their program phases.")
    edge("exact-macros", [lift, "natural:chronology", "natural:standard-matrices", "natural:H-program", "natural:T-programs", "natural:H-definition", "natural:P-definition", "natural:H-entries", "natural:P-entries"], macros, ["macro-evaluation"])
    monomial = node("monomial-product", "Finite unique-summand chronological product for arbitrary complex phases.")
    edge("monomial-product", ["natural:monomial-definition", "natural:monomial-product"], monomial, ["monomial-product"])
    middle_perm = node("middle-permutation", "The literal middle network restores all bits.")
    edge("middle-permutation", ["natural:middle-list", "natural:middle-permutation"], middle_perm, ["middle-permutation"])
    exponent = node("phase-exponent", "E=4abt for bits a,b,t; local arithmetic identity only.")
    route8 = inputs("eight-bit-case-check", "All eight source bit cases establish E=4abt; visible implementation route, not newly executed.")
    route_xor = inputs("xor-expansion-proof", "Use x xor y=x+y-2xy to expand E; source-described local proof option, not a compiled alternative compiler.")
    common = ["natural:middle-exponent", "natural:E-local-OR"]
    edge("phase-exponent-eight-cases", common + [route8], exponent, ["E-local-OR"], "local-source-proof-route")
    edge("phase-exponent-xor", common + [route_xor], exponent, ["E-local-OR"], "local-source-proof-route")
    sg["local_alternative_proofs"].append({"id": "local-OR:E=4abt", "logic": "OR_OF_SUFFICIENT_LOCAL_PROOF_ROUTES", "common_head": exponent,
                                           "route_hyperedges": ["and:phase-exponent-eight-cases", "and:phase-exponent-xor"],
                                           "implementation_route": "and:phase-exponent-eight-cases", "compiled_alternative_construction": False,
                                           "xor_status": "SOURCE_DESCRIBED_OPTION_NOT_NATIVE_OR_KERNEL_ACCEPTED"})
    ccz = node("exact-ccz", "Exact middle CCZ diagonal including all T/Tdg phases.")
    edge("exact-ccz", [macros, monomial, middle_perm, exponent, "natural:middle-list", "natural:monomial-record", "natural:monomial-seq", "natural:ccz-phase"], ccz, ["middle-list", "ccz-phase"])
    ccx = node("exact-ccx", "Exact H-middle-H primitive CCX and supplied refinement.")
    edge("exact-ccx", [ccz, macros, lift, "natural:target-blocks", "natural:H-identities", "natural:ccx-composition", "natural:weaker-guards", "natural:refinement"], ccx, ["ccx-equality", "refinement"])
    spec = node("independent-spec", "Context-selected Ry with target avoidance only; repeated controls permitted.")
    edge("independent-spec", [lift, "natural:control-domain", "natural:control-assignment", "natural:consistent-tuples"], spec, ["control-domain", "control-assignment"])
    compiler = node("compiler-definition", "One Ry at zero; tail(alpha),CX,tail(delta),CX otherwise.", "literal-construction")
    edge("compiler-definition", ["natural:zero-block", "natural:angle-split", "natural:compiler-list", "natural:control-domain", "natural:angle-standing"], compiler, ["compiler-list"])
    recursive_formula = node("recursive-matrix-definition", "Separate reverse-chronological recursive matrix expression.", "literal-definition")
    edge("recursive-matrix-definition", ["natural:recursive-denotation", "natural:angle-split", "natural:chronology"], recursive_formula, ["recursive-denotation"])
    append = inputs("circuit-append-law", "Chronological append evaluation and zero/singleton evaluation.")
    eval_ih = inputs("recursive-eval-IH-pair", "Both tail recursive-denotation induction hypotheses, for alpha and delta; local induction schema.")
    recursive_eval = node("recursive-evaluation", "C31-057: emitted list evaluates to recursive matrix formula.")
    edge("recursive-evaluation", [compiler, recursive_formula, append, eval_ih], recursive_eval, ["recursive-denotation"])
    zero = node("zero-control-block", "Unique empty tuple yields lifted Ry.")
    edge("zero-control-block", [lift, "natural:zero-block"], zero, ["zero-block"])
    cx_block = node("cx-context-block", "CX context I/X and flip-bit entry, no same-wire gate.")
    edge("cx-context-block", [lift, "natural:cx-block", "natural:control-domain"], cx_block, ["cx-block"])
    angle_eval = inputs("exact-half-angle-evaluation", "ExactAngle evaluation of alpha/delta is (theta0 +/- theta1)/2.")
    ry_add = inputs("Ry-addition", "Standard Ry matrices compose by addition at the half-angle convention.")
    x_conj = inputs("X-Ry-X", "X Ry(delta) X=Ry(-delta), exact complex equality.")
    block_products = inputs("reindex-block-product-laws", "Reindex and blockDiagonal multiplication preserve complete fixed contexts.")
    assignments = inputs("head-tail-assignment-reconstruction", "Prepending actual head bit to tail assignment reconstructs full control tuple, also for correlated/repeated wires.")
    semantic_ih = inputs("semantic-tail-IH-pair", "Both tail independent-specification induction hypotheses for alpha and delta; not recursive-denotation IH.")
    head0 = inputs("head-zero-branch", "Under head=0, Ry(delta)Ry(alpha)=Ry(theta0).")
    head1 = inputs("head-one-branch", "Under head=1, XRy(delta)XRy(alpha)=Ry(theta1).")
    semantic = node("semantic-compiler", "C31-058: direct independent-spec induction, not a use of C31-057.")
    edge("semantic-compiler-direct", [spec, compiler, append, zero, cx_block, angle_eval, ry_add, x_conj, block_products, assignments, semantic_ih, head0, head1], semantic, ["direct-semantic"])
    sg["guarded_exhaustive_cases"].append({"id": "cases:head-bit", "semantics": "EXHAUSTIVE_CASES_ALL_BRANCHES_REQUIRED", "guards": ["head=0", "head=1"],
                                           "required_branch_ids": [head0, head1], "consuming_hyperedge": "and:semantic-compiler-direct", "alternative_constructions": False})
    sg["guarded_exhaustive_cases"].append({"id": "cases:context-and-dimension", "semantics": "EXHAUSTIVE_CASES_ALL_BRANCHES_REQUIRED", "guards": ["contexts equal / unequal", "controls=0 / successor"],
                                           "required_branch_explanations": ["Within-context 2x2 identity AND cross-context zero entries", "Zero-control base AND successor induction"], "alternative_constructions": False})
    count_data = inputs("list-count-definitions-and-additivity", "Ry/CX singleton/base/append counters of emitted list.")
    count_ih = inputs("tail-count-IH-pairs", "Separate Ry and CX tail count IH pairs with elementary arithmetic; not a semantic correctness premise.")
    ry_count = node("Ry-count", "2^n emitted Ry gates.")
    cx_count = node("CX-count", "2(2^n-1) emitted CX gates.")
    for name, result in (("Ry-count", ry_count), ("CX-count", cx_count)):
        edge(name, [compiler, count_data, count_ih, "natural:count-formulas"], result, ["count-formulas"])
    resource_def = inputs("primitive-resource-definition", "Program resource is circuit resource, oracle field literally zero; no correctness/efficiency theorem required.")
    oracle = node("oracle-zero", "Zero opaque calls from primitive resource definition.")
    edge("oracle-zero", [resource_def, "natural:oracle-zero"], oracle, ["oracle-zero"])
    five = node("five-control-counts", "Reference counts32/62 at five controls.")
    edge("five-control-counts", [ry_count, cx_count, "natural:five-counts"], five, ["five-counts"])
    table = node("finite-table-and-bound", "Four cubic rationals on n=2 and their actual bound, not arbitrary-n inference.")
    edge("finite-table-and-bound", ["natural:finite-index-table", "natural:finite-bound"], table, ["finite-index-table", "finite-bound"])
    finite_program = node("finite-program-definition", "Control wires0,1, target2, actual exact arccos angle and zero phase.", "literal-construction")
    edge("finite-program-definition", [table, "natural:finite-wires", "natural:finite-angle", "natural:finite-phase"], finite_program, ["finite-angle", "finite-phase"])
    finite_matrix = node("finite-program-matrix", "Finite program evaluates to independent controlled-Ry matrix.")
    edge("finite-program-matrix", [finite_program, semantic, "natural:chronology", "natural:finite-phase"], finite_matrix, ["finite-matrix"])
    encoded = node("encoding-identities", "Signal output, control index and context iff identities on encoded(s,j).")
    edge("encoding-identities", ["natural:encoding", "natural:encoding-identities"], encoded, ["encoding-identities"])
    arccos = inputs("Ry-arccos-clean-entry-and-casts", "Actual Ry-to-amplitudeRotation identity AND arccos clean entry with internally supplied finite bound AND rational/real/complex casts.")
    spec_entry = inputs("independent-spec-entry-law", "Equal-context selected target entry and unequal-context zero.")
    named_clean = node("named-wire-clean-entries", "Clean signal-zero entries equal finite cubic diagonal.")
    edge("named-wire-clean-entries", [finite_matrix, encoded, table, arccos, spec_entry, "natural:clean-entry"], named_clean, ["clean-entry"])
    flat_def = node("flat-matrix-definition", "Forward little-endian reindex of the evaluated primitive program.", "literal-definition")
    edge("flat-matrix-definition", [finite_program, "natural:LE-equivalence", "natural:flat-transport"], flat_def, ["LE-equivalence", "flat-transport"])
    program_unitary = inputs("primitive-program-unitarity", "Actual unitary primitive evaluation + chronological list and exact phase-unitarity provider, independently of clean-entry formula.")
    reindex_unitary = inputs("reindex-unitarity-law", "Reindex preservation of Matrix.unitaryGroup membership.")
    flat_unitary = node("flat-unitarity", "Actual reindexed whole program is unitary; does not require named/flat clean entries.")
    edge("flat-unitarity", [flat_def, program_unitary, reindex_unitary], flat_unitary, ["primitive-unitarity", "flat-transport"])
    clean_index = inputs("clean-index-and-LE-inverse-laws", "Forward image of signal-zero encoding and actual LE inverse cancellation; no assumed endianness.")
    flat_clean = node("flat-clean-entries", "Flat clean-sector entries equal the finite cubic diagonal.")
    edge("flat-clean-entries", [flat_def, named_clean, clean_index], flat_clean, ["clean-entry", "LE-equivalence", "flat-transport"])
    target = node("concrete-target-normalizer-layout", "Literal D2/normalizer1/system2/signal1/pure0.", "literal-data")
    edge("concrete-target-normalizer-layout", ["natural:target-layout", "natural:clean-entry"], target, ["target-layout"])
    predicates = inputs("concrete-candidate-predicates", "This candidate's isUnitary is actual Matrix.unitaryGroup membership AND blockContainsTarget is exact clean entries divided by its normalizer. Generic Prop fields remain arbitrary data.")
    wrapper = node("verified-wrapper-correctness", "Concrete unitaryProof AND blockProof supplied by actual unitary and clean-entry theorems; no list-count theorem required.")
    edge("verified-wrapper-correctness", [predicates, target, flat_unitary, flat_clean], wrapper, ["wrapper-proofs"])
    presentation = node("presentation-data", "Gate/wire presentation with discarded angles; not an executable refinement.", "literal-data")
    edge("presentation-data", [finite_program, "natural:presentation"], presentation, ["presentation"])
    resource = node("resource-ownership", "Program/circuit resource equality by definitions, independent of wrapper proof.")
    edge("resource-ownership", [finite_program, resource_def, "natural:resource-ownership"], resource, ["resource-ownership"])
    finite_counts = node("finite-reference-counts", "Source-level specialization4 Ry/6 CX; not a newly compiled theorem.")
    edge("finite-reference-counts", [ry_count, cx_count, finite_program, "natural:finite-counts"], finite_counts, ["finite-counts"])
    sg["candidate_definition_data_links_not_correctness_proof_tails"] = [presentation, resource, target, flat_def]
    sg["open_source_gap_ids"] = old_graph["views"]["source-construction-graph"]["open_source_gap_ids"]
    for n in old_graph["views"]["source-construction-graph"]["nodes"]:
        if n["id"] in sg["open_source_gap_ids"]:
            sg["nodes"].append(copy.deepcopy(n))
    graph["views"]["source-construction-graph"] = sg
    graph["views"]["lean-graph"]["actual_static_source_traces"] = {
        "direct_independent_semantic_root": "C31-058", "recursive_denotation_root": "C31-057", "direct_semantic_calls_recursive_root": False,
        "flat_unitarity_root": "C31-078", "named_clean_root": "C31-076", "flat_clean_root": "C31-080", "verified_root": "C31-085",
        "counts_not_wrapper_proof_inputs": ["C31-059", "C31-060", "C31-062"], "resource_ownership_root": "C31-087",
        "not_elaborated_dependency_graph": True}
    spine = graph["views"]["compressed-quantum-spine"]
    spine["groups"] = [
        {"id": "concept:exact-phase-macro", "expands_to": [macros, monomial, ccz, ccx]},
        {"id": "concept:context-multiplexed-rotation", "expands_to": [spec, compiler, recursive_formula, recursive_eval, semantic]},
        {"id": "concept:reference-resources", "expands_to": [ry_count, cx_count, oracle, five, resource, finite_counts, presentation]},
        {"id": "concept:finite-cubic-clean-block", "expands_to": [table, finite_program, finite_matrix, named_clean, flat_def, flat_unitary, flat_clean, target, wrapper]}]
    spine["lossless_drilldown"] = [PREFIX + "author-source-coverage.json", "reviews/publication/primitive-compiler-c31/author-formal-context.json"]
    functor = graph["views"]["functor-hypergraph"]
    functor["hyperedges"] = []
    for edge_id in ("and:exact-ccz", "and:semantic-compiler-direct", "and:verified-wrapper-correctness"):
        e = next(e for e in sg["AND_hyperedges"] if e["id"] == edge_id)
        functor["hyperedges"].append({"id": "transport:" + edge_id[4:], "logic": "AND", "tails": e["tails"], "heads": e["heads"],
                                     "source_hyperedge": edge_id, "formula": "Only the precisely matched complete source-tail construction; no independently sufficient split arrows.",
                                     "hypothesis_map": "All listed source-data, standing algebra and local proof-schema requirements retained at their actual evidence layer; not extra public theorem binders.",
                                     "conclusion_map": "Exactly the named source-level local result, no stronger scientific consumer.",
                                     "failure_boundary": "No certified categorical functor, finite-bit/executable family, normalized SP or main admission.",
                                     "independent_review": "PENDING_V3", "certified": False})
    return graph


def main(args):
    old, out, repo, reviewer = args.old.resolve(), args.out.resolve(), args.repo.resolve(), args.reviewer.resolve()
    assert out.parent == old and out.name == "metadata-v3"
    assert {p.name for p in out.iterdir()} == {"build-metadata-v3.py", "audit-metadata-v3.py"}, "Exclusive fresh successor; no overwrite."
    recipe = module(args.recipe.resolve(), "c31_mechanical_recipe_only")
    audit_module = module(out / "audit-metadata-v3.py", "c31_new_static_metadata_audit")
    emit = lambda name, obj: recipe.emit(out, name, obj)
    raw_emit = lambda name, raw: recipe.emit_raw(out, name, raw)
    snapshot = [rec(p, p.relative_to(old).as_posix()) for p in sorted(old.rglob("*")) if p.is_file() and out not in p.parents]
    for name, expected in REVIEW.items():
        assert sha((reviewer / name).read_bytes()) == expected
    old_cov = read_json(old / "author-source-coverage.json")
    old_audit = read_json(old / "author-binder-definition-audit.json")
    old_graph = read_json(old / "author-graph-views.json")
    coverage, binder = copy.deepcopy(old_cov), copy.deepcopy(old_audit)
    assert len(ROOT_LINKS) == 87
    source = (old / "source-only.md").read_bytes()
    assert sha(source) == "5907262565b6202fec61b189c42d942cb84d6215223a0da4211d63b92d3ad168"
    atoms = source_atoms(coverage["source_paragraphs"])
    binder_by_id = {o["id"]: o for o in binder["whole_module_inventory"]}
    changes = []
    for index, (o, names) in enumerate(zip(coverage["whole_module_inventory"], ROOT_LINKS), 1):
        assert o["id"] == f"C31-{index:03d}"
        old_links = {"source_regions": o["source_regions"], "source_paragraphs": o["source_paragraphs"]}
        selected = [atoms[name] for name in names]
        o["source_regions"] = list(dict.fromkeys(a["source_region"] for a in selected))
        o["source_paragraphs"] = list(dict.fromkeys(a["source_paragraph"] for a in selected))
        o["source_links"] = [{"natural_atom": a["id"], "source_paragraph": a["source_paragraph"], "source_sha256": a["sha256"],
                              "role": "source-claim-or-literal-construction" if i == 0 else "source-semantic-context-or-local-provider-role",
                              "declaration_specific_role": o["name"].split(".")[-1] + ": " + a["mathematical_role"],
                              "reviewer_Nxx_mapping_used_as_source": False} for i, a in enumerate(selected)]
        o["legacy_lexical_header_authority"] = "NONAUTHORITATIVE_LEXICAL_HINT_MAY_INCLUDE_OR_TRUNCATE_BODY; exact whole source remains authority, no signature digest."
        o["status"] = WIP
        o["source_link_precision_version"] = 3
        if index in (55, 56):
            o["binder_audit"] = pi_binders(o["binder_audit"])
            field = binder_by_id[o["id"]]
            field["binder_audit"] = copy.deepcopy(o["binder_audit"])
            exact = o["definition_audit"]["exact_source_region"]
            type_region = exact[:exact.index("\n  | 0,")]
            o["complete_lexical_dependent_type_region"] = type_region
            field["complete_lexical_dependent_type_region"] = type_region
            o["standing_semantics_not_extra_parameter"] = {"classification": "STANDING", "meaning": "ExactAngle mathematical real evaluation and standard Ry half-angle convention.", "source_atoms": ["natural:angle-standing", "natural:standard-matrices"], "computational_access_assumed": False}
            field["standing_semantics_not_extra_parameter"] = copy.deepcopy(o["standing_semantics_not_extra_parameter"])
        changes.append({"id": o["id"], "name": o["name"], "old_module_wide_links": old_links,
                        "new_source_regions": o["source_regions"], "new_source_paragraphs": o["source_paragraphs"], "new_natural_atoms": [a["id"] for a in selected],
                        "rationale": "; ".join(a["mathematical_role"] for a in selected), "binder_Pi_repair": index in (55, 56)})
    coverage.update(status=WIP, metadata_version=3, author=AUTHOR, source_atoms=list(atoms.values()),
                    source_link_policy="Individually authored exact natural-source excerpts for all87 roots, not a copy of reviewer Nxx mappings. Whole34-paragraph lossless partition is unchanged; topology-only/open paragraphs remain source nodes even when no declaration claims them.",
                    predecessor_sha256=sha((old / "author-source-coverage.json").read_bytes()), independent_source_topology="PENDING_V3")
    binder.update(status=WIP, metadata_version=3, author=AUTHOR, predecessor_sha256=sha((old / "author-binder-definition-audit.json").read_bytes()))
    binder["classification_authority"] = "AUTHOR_CORRECTION_AFTER_AUTHORIZED_STATIC_REPORT_NOT_INDEPENDENT_ACCEPTANCE"
    graph = make_graph(old_graph, atoms)
    graph["metadata_version"] = 3
    graph["predecessor_sha256"] = sha((old / "author-graph-views.json").read_bytes())
    emit("author-source-coverage.json", coverage)
    emit("author-binder-definition-audit.json", binder)
    emit("author-graph-views.json", graph)
    emit("source-link-diff.json", {"status": WIP, "source_unchanged_sha256": sha(source), "review_mapping_not_copied": True, "all87_individually_relinked": changes})
    diff_lines = ["C31 metadata-v3 author correction after authorized STATIC report", "", "Only F1/F2/F3 metadata corrected; no source, Lean, history, scoring or old verifier altered.",
                  "F1: C31-055/056 now list leading qubits plus controls/wires/target/target-avoidance SOURCE proof/angle table Pi inputs. Exact-angle evaluation is STANDING semantics, not extra numeric access. No control-map injectivity premise.",
                  "F2: Every row below names exact excerpts in the unchanged natural source; paragraph partition remains byte-lossless. Reviewer Nxx mappings were not used as source links. Old lexical headers remain nonauthoritative, not exact elaborated signatures.",
                  "F3: Direct semantic induction differs from recursive denotation; flat unitarity differs from clean entries; wrapper proof differs from resource/presentation/count data. Exhaustive cases require both branches. E=4abt keeps a source-local eight-case OR XOR proof, not an independently compiled alternative construction.",
                  "F4/F5 retained: Generic arbitrary Prop fields are weaker than this concrete actual unitary/clean-entry instance; native scripts are not executed/accepted, finite-bit and executable-family claims remain open.", "", "Per-root natural-source relinking:"]
    diff_lines += [r["id"] + " " + r["name"] + " -> " + ",".join(r["new_natural_atoms"]) + "; " + r["rationale"] for r in changes]
    diff_lines += ["", "Review status: this is the original metadata author's successor, not the independent reviewer's acceptance. New independent v3 review and all formal/native gates remain pending.",
                   "Logical audit command: python audit-metadata-v3.py --package METADATA_V3_DIRECTORY --old AUTHOR_PACKAGE_DIRECTORY --repo REPOSITORY_ROOT", ""]
    raw_emit("reviewer-readable-diff.txt", "\n".join(diff_lines).encode())
    audit = audit_module.audit_metadata(coverage, binder, graph, source)
    negative = audit_module.negative_tests(coverage, binder, graph, source)
    emit("author-static-tests.json", {"status": "AUTHOR_STATIC_METADATA_TESTS_NOT_INDEPENDENT_REVIEW", "positive": audit, "negative_mutation_tests": negative,
                                      "source_and_Lean_unchanged": True, "Lean_executed": False, "native_or_decoder_evidence_read": False, "independent_acceptance": False})
    old_row = read_json(old / "author-source-row-candidate.json")["source"]
    catalog_raw = (repo / "website/research/sources.json").read_bytes()
    catalog = json.loads(catalog_raw)
    existing = [row for row in catalog["sources"] if row["id"] == old_row["id"]]
    assert not existing or existing == [old_row], "Existing source row differs; stop, no reseal."
    if not existing:
        catalog["sources"].append(old_row)
    lesson = read_json(old / "publication-candidate-PrimitiveMacros.json")["lesson_path"]
    overlay = recipe.OverlayRoot(repo, {lesson: source, "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()})
    binding, checker_sha = recipe.binding_function(repo)
    old_freeze = read_json(old / "metadata-freeze.json")
    assert checker_sha == old_freeze["checker_sha256"]
    recipe.assert_current(repo, old_freeze["whole_ambient_binding_inputs"] + old_freeze["strict_config_and_external_inputs"])
    prospective = []
    derivatives = []
    for name in ("author-source-coverage.json", "author-binder-definition-audit.json", "author-graph-views.json"):
        derivatives.append({"kind": "VERSIONED_METADATA_CORRECTION_NOT_BYTE_ALIAS", "original_file": name, "original_sha256": sha((old / name).read_bytes()),
                            "successor_file": name, "successor_sha256": sha((out / name).read_bytes()), "change_scope": ["F1", "F2", "F3"], "same_bytes_claim": False})
    for path in ("PrimitiveMacros", "UniformlyControlledRy", "CubicAmplitudePrimitive"):
        name = "publication-candidate-" + path + ".json"
        original = read_json(old / name)
        candidate = copy.deepcopy(original)
        contribution = candidate["graph_contribution"]
        contribution.update(source_graph_sha256=sha((out / "author-graph-views.json").read_bytes()), coverage_sha256=sha((out / "author-source-coverage.json").read_bytes()),
                            binder_audit_sha256=sha((out / "author-binder-definition-audit.json").read_bytes()), metadata_version=3,
                            static_review_trigger_report_sha256=REVIEW["phase2-static-report.md"],
                            v3_review_status="PENDING_DISTINCT_REVIEW_NO_PRIOR_VERDICT_INHERITED")
        contribution["node_ids"] += ["natural:" + key for key in atoms]
        candidate.update(status=WIP, metadata_version=3, prior_binding_sha256=original["binding_sha256"], independent_acceptance=False,
                         source_proof_coverage=PREFIX + "author-source-coverage.json", binder_definition_audit=PREFIX + "author-binder-definition-audit.json",
                         graph_views=PREFIX + "author-graph-views.json", author_correction_scope=["F1", "F2", "F3"],
                         predecessor_candidate_sha256=sha((old / name).read_bytes()))
        candidate["evidence_paths_status"] = "UNATTACHED_PENDING_V3_REVIEW; NO_OLD_ACCEPTANCE_INHERITED"
        candidate["binding_sha256"] = binding(overlay, candidate)
        emit(name, candidate)
        prospective.append({"module": candidate["module"], "prior_binding_sha256": original["binding_sha256"], "new_prospective_binding_sha256": candidate["binding_sha256"], "accepted": False})
        derivatives.append({"kind": "VERSIONED_PUBLICATION_CANDIDATE_NOT_BYTE_ALIAS", "original_file": name, "original_sha256": sha((old / name).read_bytes()),
                            "successor_file": name, "successor_sha256": sha((out / name).read_bytes()), "change_scope": ["F1", "F2", "F3", "NEW_PROSPECTIVE_BINDING"], "same_bytes_claim": False})
    emit("prospective-bindings.json", {"status": WIP, "author": AUTHOR, "bindings": prospective,
                                       "formal_context_unchanged_sha256": "a0b798f1e74b084274a44061514f7944ea6b694c13af2b8f718a27ea7b0ac408",
                                       "formal_packet_unchanged_sha256": "819f8413afb69daab2e282c863900b198f32feae93d57ec3df5cc8c1179f5fde",
                                       "late_bridge_policy": "No independently frozen reconstruction or verdict is read or silently rebound; any later opaque bridge requires a separate authorized step.", "acceptance": False})
    emit("derivative-allowlist.json", {"status": "VERSIONED_METADATA_DERIVATIVES_EXPLICITLY_NOT_ORIGINAL_ALIASES", "derivatives": derivatives,
                                       "natural_source_byte_changes": False, "production_Lean_changes": False, "old_bindings_remain_immutable": True})
    raw_emit("handoff-v3.txt", (
        "C31 metadata-v3 AUTHOR/WIP handoff\n\n"
        "Author /root/primitive_compiler_metadata_c31; original natural author /root; historical formalizer UNKNOWN. Authorized static report and seal were completely read; no decoder/CI/runtime result was consumed.\n"
        "F1 repaired only two metadata binder lists (055/056) by explicit dependent Pi enumeration. F2 relinks all87 authored roots to precise quoted natural-source atoms while retaining all34 unchanged source paragraphs. F3 separates denotation/semantic induction, unitary/clean entries, correctness/resource data, all-branches-required cases and source-local proof OR. No control injectivity, new theorem, changed phase, changed cost tier or actual signature digest is introduced.\n"
        "Existing generic Prop vs concrete Matrix.unitaryGroup/clean-entry semantics, actual exact-real exponential counts, finite n=2 scope, native-acceptance unknown, finite-bit/executable-family boundaries remain unchanged.\n"
        "Reviewable differences: reviewer-readable-diff.txt and source-link-diff.json. Fresh author-positive and mutation-negative static checks: author-static-tests.json. New bindings are prospective only: prospective-bindings.json. Distinct v3 review and all actual signature/axiom/native/integration/publication gates remain pending. No MAIN/ROOT/PURIFIED claim.\n"
        "Public safety: use public-allowlist.json and derivative-allowlist.json only. Regenerated metadata has distinct old/new hashes and is never an alias. Exact original source/formal references retain their old hashes. All commands use logical placeholders; no host path is authored here. Public privacy/static checks do not verify withheld private history or replace original verifier evidence.\n"
        "Failure class: original metadata IMPLEMENTATION_FAILED (incomplete audit/link granularity), corrected only at metadata layer. Mathematical refutation NONE. Salvage: original raw source/context retained exactly. Process-memory policy remains low-token deterministic static audit and verifier-layer separation; no children or route-comparison claim. Purification/Exposition Seal PENDING.\n"
        "Replay: python audit-metadata-v3.py --package METADATA_V3_DIRECTORY --old AUTHOR_PACKAGE_DIRECTORY --repo REPOSITORY_ROOT\n"
        "STOP after versioned private handoff; public-safe classification is not authorization to publish/admit.\n"
    ).encode())
    # Every artifact emitted in this version is public-safe as content, but the
    # package remains a private WIP until a separately authorized transport.
    for pin in snapshot:
        assert rec(old / pin["path"], pin["path"]) == pin, "Old artifact changed."
    emit("metadata-v3-seal.json", {"status": WIP, "author": AUTHOR, "authorized_static_review_pins": REVIEW,
                                  "old_artifact_hashes_preserved": snapshot,
                                  "source_sha256_unchanged": sha(source), "whole_ambient_source_pins": old_freeze["whole_ambient_binding_inputs"],
                                  "config_and_external_pins": old_freeze["strict_config_and_external_inputs"],
                                  "new_artifact_pins": [rec(p, p.name) for p in sorted(out.iterdir()) if p.is_file()],
                                  "source_catalog_snapshot_sha256": sha(catalog_raw), "checker_sha256": checker_sha,
                                  "no_Lean_Git_network_canonical_writes": True, "independent_acceptance": False, "self_hash_excluded": True})
    exact = ["source-only.md", "author-private-coverage.md", "source-freeze.json", "author-formal-context.json", "author-source-row-candidate.json"]
    public = {"status": "PUBLICSAFE_CONTENT_ALLOWLIST_PRIVATE_WIP_NOT_PUBLICATION_AUTHORITY", "new_original_artifacts": [rec(p, p.name) for p in sorted(out.iterdir()) if p.is_file() and p.name not in {r["successor_file"] for r in derivatives}],
              "versioned_derivatives": [rec(out / d["successor_file"], d["successor_file"]) for d in derivatives],
              "derivative_receipt": "derivative-allowlist.json", "exact_original_references": [dict(rec(old / name, "../" + name), kind="EXACT_REFERENCE_UNCHANGED") for name in exact],
              "private_original_handoff_not_referenced": True, "not_standalone_verification_of_all_historical_private_artifacts": True,
              "allowlist_self_hash_excluded": True, "host_paths_authorized": False, "independent_acceptance": False}
    emit("public-allowlist.json", public)
    print(json.dumps(audit_module.verify_package(out, old, repo), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("repo", "old", "reviewer", "recipe", "out"):
        parser.add_argument("--" + flag, type=Path, required=True)
    main(parser.parse_args())
