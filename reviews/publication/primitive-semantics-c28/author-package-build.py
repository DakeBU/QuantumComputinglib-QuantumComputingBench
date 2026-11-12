#!/usr/bin/env python3
"""C28 author-only deterministic publication serialization, never admission.

Format/overlay technique follows c27; all mathematical mappings are c28-only.
No Git, Lean, independent-result read, cache write or registry write.
Build refuses to overwrite any existing output; --verify is read-only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PREFIX = "reviews/publication/primitive-semantics-c28/"
LESSON = "docs/lessons/concrete-primitive-and-reversible-semantics.md"
SOURCE_ID = "aspbe-local-concrete-primitive-reversible-semantics"
HEAD = "cc25e39022db29ce9f98e77708850ce2dc0b0739"
BASE = "f2cba045611a0d11c5995c29607569726bf1d6c5"
WIP = "AUTHOR_WIP_NOT_ADMITTED"
EXPECTED = {
    "ConcreteSemantics": ("4b4e1c3612ea2d4eed3a2d5dbfec39ffae81263fd9ceb521c1a59231f786caa1", 25),
    "PrimitiveSemantics": ("a68955f9dbe0e951c2751fcd14c535c28da7c8bcac75787b0005808b951f28de", 55),
    "ReversibleClassical": ("7662d42a2afae784dc14d669a462baecf5fa18ac8165c64e35c006be3517c26d", 8),
}
ORIGINAL = {
    "source-only.md": "696a9dce55a0ab9af6139b96ed8ba619fa0b946a0519bbe740cbdc58666e44b5",
    "author-private-coverage.md": "1c42f8d0190581e416e25c897d1ce8f581f8da995742b5c62e9977f9a2afc59a",
    "source-freeze.md": "fa3168c2e7c199144674a983ac63c2db3faac124d35aecc3c64dff8032b649ff",
}
ROOT_RE = re.compile(r"^(?:@\[[^\n]*?\]\s+)?(?P<private>private\s+)?(?:noncomputable\s+)?(?P<kind>def|theorem|structure|abbrev|inductive|instance)\s+(?P<name>[\w'.]+)", re.M)
PROOF_NAMES = {"_lower", "_upper", "distinct", "unitary", "c0_ne_c1", "c0_ne_target", "c1_ne_target"}
RESIDUAL = (
    "Retrospective local mathematics only; historical formalizer UNKNOWN. Target normalization is an arbitrary stored Prop, not automatically squared norm one. "
    "Presentation circuit/schedule/resource/auxiliary data are not linked to matrix denotation or charged implementation. Named-wire assignments have no certified integer-endian bridge here. "
    "Half angles, signed entries, chronological later-on-left order and exact global phase, including zero wires, are retained; RY(pi/2) is not H. "
    "CCX belongs to reversible proof IR, not the final four primitives; compilation and costs need a separate consumer bridge. No finite-bit angle/runtime, measurement/success, ancilla cleanup or hardware/resource theorem is inferred."
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def dump_bytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode()

def emit(out, name, data):
    # Exclusive creation, including after a partial failed build.
    with (out / name).open("xb") as handle:
        handle.write(dump_bytes(data))

def file_record(path, relative, full=False):
    raw = path.read_bytes()
    rec = {"path": relative, "sha256": sha(raw), "bytes": len(raw)}
    if full:
        rec.update(full_source_lines=raw.decode().splitlines(keepends=True), full_source_utf8_bytes=list(raw))
        assert "".join(rec["full_source_lines"]).encode() == raw
    return rec

def imports(text):
    return re.findall(r"^import\s+(\S+)\s*$", text, re.M)

def module_path(name):
    return name.replace(".", "/") + ".lean"

def outside_definition_split(text):
    """Keep binder defaults intact: only a top-level := or where ends header."""
    stack = []
    for i, ch in enumerate(text):
        if ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if stack:
                stack.pop()
        elif not stack:
            if text.startswith(":=", i):
                return text[:i].rstrip(), text[i:]
            if text.startswith("where", i) and (i == 0 or text[i-1].isspace()) and (i+5 == len(text) or text[i+5].isspace()):
                return text[:i].rstrip(), text[i:]
    return text.rstrip(), ""

def inventory(path, raw):
    text = raw.decode()
    events = []
    for match in re.finditer(r"^(namespace\s+\S+|end(?:\s+\S+)?)\s*$", text, re.M):
        events.append((match.start(), "scope", match.group(1)))
    matches = list(ROOT_RE.finditer(text))
    for match in matches:
        events.append((match.start(), "root", match))
    scopes = []
    roots = []
    for pos, kind, item in sorted(events, key=lambda e: e[0]):
        if kind == "scope":
            if item.startswith("namespace "):
                scopes.append(item.split()[1])
            elif scopes:
                scopes.pop()
            continue
        local = item["name"]
        roots.append({
            "name": ".".join(scopes + [local]), "module": path, "kind": item["kind"],
            "line": text.count("\n", 0, pos) + 1, "private": bool(item["private"]),
            "lexical_local_name": local, "start_offset": pos,
            "ambient_namespace_stack": list(scopes),
        })
    for idx, root in enumerate(roots):
        end = roots[idx+1]["start_offset"] if idx+1 < len(roots) else len(text)
        block = text[root["start_offset"]:end]
        header, body = outside_definition_split(block)
        root.update(lexical_header=header, lexical_block=block, body_sha256=sha(block.encode()))
        root["generated_member_scope"] = (
            "Record constructor/projections and their full fields in the preserved body; compiler recursors/equation auxiliaries are infrastructure, not additional authored roots."
            if root["kind"] in ("structure", "inductive") else None
        )
    return roots

def binder_audit(root):
    match = ROOT_RE.match(root["lexical_header"])
    tail = root["lexical_header"][match.end():].lstrip()
    result = []
    while tail and tail[0] in "({[":
        stack = []
        end = None
        for i, ch in enumerate(tail):
            if ch in "({[":
                stack.append(ch)
            elif ch in ")}]":
                stack.pop()
                if not stack:
                    end = i+1
                    break
        assert end, root["name"]
        group = tail[:end]
        names = group[1:-1].split(":", 1)[0].split()
        proof = bool(set(names) & PROOF_NAMES)
        bundles = []
        for token in ("ComplexStatePreparationCertificate", "ComplexUnitaryGate", "StatePreparationTarget", "PrimitiveGate", "PrimitiveCircuit", "PrimitiveProgram", "ReversibleGate", "ReversibleProgram", "OtherPrimitiveWires"):
            if re.search(r"\b" + token + r"\b", group):
                bundles.append(token)
        if "≃" in group:
            bundles.append("Equiv")
        result.append({
            "exact_lexical_binder": group, "classification": "SOURCE" if proof else "TYPING",
            "reason": "Substantive stated coefficient bound, wire separation or matrix unitarity premise; never mere finite carrier formation."
            if proof else "Carrier/algebra/index/scalar/function/object parameter. Any nested logical evidence is expanded separately, not erased by this outer data label.",
            "expanded_bundle_names": bundles,
            "nested_evidence_policy": "See exact project-owned bundle bodies and nested SOURCE clauses; a typed supplied object is not a produced correctness theorem." if bundles else None,
        })
        tail = tail[end:].lstrip()
    return result

def paragraphs(raw):
    text = raw.decode()
    pieces = re.findall(r"[^\n](?:.*?)(?:\n[ \t]*\n+|\Z)|\n+", text, re.S)
    assert "".join(pieces) == text
    result = []
    offset, line, section = 0, 1, None
    for idx, piece in enumerate(pieces, 1):
        heading = re.match(r"## (\d+)\.", piece)
        if heading:
            section = int(heading[1])
        nav = piece.lstrip().startswith("#") or not piece.strip()
        pbytes = piece.encode()
        result.append({
            "id": f"paragraph:{idx:03d}", "section": section, "source_lines": [line, line+piece.rstrip("\n").count("\n")],
            "start_utf8_byte": offset, "end_utf8_byte": offset+len(pbytes), "exact_text": piece, "sha256": sha(pbytes),
            "disposition": "EXCLUDED" if nav else "NODE", "reason": "Navigation heading or blank separator only." if nav else None,
            "source_nodes": [] if nav else [f"source:{idx:03d}"], "disposition_authority": "AUTHOR_PROVISIONAL_NOT_INDEPENDENT",
        })
        offset += len(pbytes)
        line += piece.count("\n")
    return result

def map_private_rows(text):
    result = {}
    for line in text.splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) == 4 and re.fullmatch(r"\d+", cells[0]) and cells[1].startswith(chr(96)):
            name = cells[1].strip(chr(96))
            result[name] = {"binder_note": cells[2], "mathematics": cells[3]}
    return result

def sections_for(module, name):
    if module.endswith("/ConcreteSemantics.lean"):
        return [1, 2] if name in ("FiniteMatrix", "StateVector") else [3] if name in (
            "ProductRegisterMatrix", "flatToProductRegister", "productRegisterBlockProjection",
            "productRegisterBlockProjection_flatToProductRegister", "productIndex_val_eq_signalSystemBlockRowIndex",
            "signalSystemBlockProjection_eq_cleanBlockProduct", "cleanBasisActionAmplitude",
            "cleanBasisActionAmplitude_eq_signalSystemBlockProjection", "pointwiseProjection_iff_cleanBasisAction") else [2]
    if module.endswith("/ReversibleClassical.lean"):
        return [7]
    if name.startswith(("standardRy", "standardRz", "star_complex", "conj_complex", "complex_ofReal")) or name in ("xMatrix", "xMatrix_conjugates_standardRy"):
        return [4]
    return [6] if name.startswith(("evalPrimitiveCircuit", "evalGlobalPhase", "evalPrimitiveProgram")) or name == "PrimitiveRefinement" else [5]

def extract_bundle(repo, relative, local):
    raw = (repo/relative).read_bytes()
    own = inventory(relative, raw)
    candidates = [r for r in own if r["lexical_local_name"] == local]
    assert len(candidates) == 1, (relative, local)
    root = candidates[0]
    return {
        "provider_path": relative, "provider_sha256": sha(raw), "name": root["name"],
        "exact_lexical_header": root["lexical_header"], "exact_definition_region": root["lexical_block"],
        "classification": "literal", "not_elaborated": True,
    }

class ShadowFile:
    def __init__(self, canonical, data):
        self.canonical, self.data = canonical, data
    def resolve(self):
        return self.canonical.resolve()
    def is_file(self):
        return True
    def read_bytes(self):
        return self.data
    def read_text(self, encoding="utf-8"):
        return self.data.decode(encoding)

class OverlayRoot:
    """Only two prospective data files; all production reads stay real."""
    def __init__(self, repo, overlay):
        self.repo, self.overlay = repo, overlay
    def __fspath__(self):
        return str(self.repo)
    def resolve(self):
        return self.repo.resolve()
    def __truediv__(self, name):
        name = str(name)
        return ShadowFile(self.repo/name, self.overlay[name]) if name in self.overlay else self.repo/name

def binding_function(repo):
    path = "website/scripts/check_research_publications.py"
    code = (repo/path).read_bytes()
    namespace = {"__file__": str(repo/path), "__name__": "author_readonly_binding"}
    exec(compile(code, namespace["__file__"], "exec"), namespace)
    return namespace["binding_digest"], sha(code)

def graph_views(pars, targets, roots):
    nodes = [{"id": p["source_nodes"][0], "kind": "source-paragraph", "paragraph_id": p["id"], "section": p["section"], "sha256": p["sha256"], "status": "AUTHOR_PROVISIONAL"} for p in pars if p["disposition"] == "NODE"]
    premises = {
        "finite-carriers": "Natural dimensions, finite indices and appropriate scalar algebra; no blanket positivity or nonzero assumption.",
        "certificate-N": "A supplied target stores arbitrary N:Prop AND supplied evidence of N; not inferred norm-one.",
        "certificate-U": "Supplied concrete gate has actual complex matrix unitarity evidence.",
        "certificate-action": "Supplied certificate evidence U e_0 = target amplitudes.",
        "presentation-data": "Arbitrary supplied circuit, schedule, resource and auxiliary count; no denotation/cost linkage.",
        "flattening": "Signal high, system low: (a,i) maps to a*d+i; same selected signal at input and output.",
        "coefficient-domain": "The stated loader equality retains -1<=c<=1; half-angle cancellation itself does not use it.",
        "generic-gate-unitary": "The arbitrary one-qubit input G satisfies standard complex unitarity.",
        "wire-CX": "Control differs from target for CX involution/equivalence and typed CX instruction.",
        "wire-CCX": "Each CCX control differs from target for its action-equivalence theorem; instruction syntax additionally requires controls distinct.",
        "typed-primitive": "X/RY/RZ/CX only, exact angle syntax and nested bounded-arccos evidence, with arbitrary-real angle permitted.",
        "phase": "Declared real-valued global phase is interpreted as exp(i phi), not quotiented out.",
    }
    nodes += [{"id": "premise:"+key, "kind": "SOURCE" if key not in ("finite-carriers", "flattening", "phase", "presentation-data") else "literal-context", "formula": value, "status": "AUTHOR_PROVISIONAL", "not_a_produced_output": True} for key, value in premises.items()]
    steps = [
        ("basis", ["premise:finite-carriers"], "Delta basis and finite action select one column; complex two-term linearity, no distinct-index premise.", [1,2]),
        ("first-column", ["result:basis"], "Pointwise first-column equality iff zero-ket action; all qubit counts.", [2]),
        ("certificate", ["result:first-column","premise:certificate-N","premise:certificate-U","premise:certificate-action","premise:presentation-data"], "Repackage existing evidence; metadata is not a circuit implementation theorem.", [2]),
        ("product-view", ["premise:finite-carriers","premise:flattening"], "Rectangular flat/product projection agrees; rational clean-block restriction agrees.", [3]),
        ("clean-action", ["result:basis","result:product-view"], "Clean basis input/output amplitude equals block entry; pointwise iff without unitarity.", [3]),
        ("RY", [], "Literal half-angle signed real rotation; zero/add/neg/X-conjugation and trig unitarity.", [4]),
        ("loader", ["result:RY","premise:coefficient-domain"], "RY(2 arccos c)=amplitude rotation; intended interval retained, not newly required for arbitrary angles.", [4]),
        ("uniform", ["result:RY"], "RY(pi/2)=[[sqrt2/2,-sqrt2/2],[sqrt2/2,sqrt2/2]], not H.", [4]),
        ("RZ", [], "Literal +/- half-angle diagonal phases; unitarity and negative-angle dagger.", [4]),
        ("X-equivalence", [], "Bit flip updates only target and is self inverse.", [5]),
        ("CX-equivalence", ["result:X-equivalence","premise:wire-CX"], "Control is preserved and conditional double flip cancels.", [5]),
        ("wire-split", [], "Target/rest split and inverse with exact other-wire coordinates; no endian flattening.", [5]),
        ("lift", ["result:wire-split"], "Literal G tensor identity transported along split, exact entry and dagger laws.", [5]),
        ("lift-unitary", ["result:lift","premise:generic-gate-unitary"], "Conditional generic lift preserves supplied unitarity.", [5]),
        ("permutation", [], "Q_sigma entry convention; adjoint Q_inverse; permutation unitarity.", [5]),
        ("gate-unitary", ["premise:typed-primitive","result:RY","result:RZ","result:X-equivalence","result:CX-equivalence","result:permutation","result:lift"], "All four constructor denotations are unitary; rotation input unitarity is produced, not assumed.", [5]),
        ("gate-dagger", ["result:RY","result:RZ","result:permutation","result:lift","result:X-equivalence","result:CX-equivalence"], "Each instruction dagger denotes exact matrix adjoint.", [5]),
        ("circuit", ["result:gate-unitary","result:gate-dagger"], "Chronological recursion yields unitarity, append later-on-left and reverse-adjoint theorem.", [6]),
        ("phase-unitary", ["premise:phase"], "Scalar conjugate products both one; negative phase is conjugate.", [6]),
        ("program", ["result:circuit","result:phase-unitary"], "Exact global-phase program identity, sequential multiplication, unitarity and dagger.", [6]),
        ("refinement", ["result:circuit"], "Circuit equality record is exact, not phase quotient; no arbitrary phase can be appended.", [6]),
        ("CCX-equivalence", ["result:X-equivalence","premise:wire-CCX"], "Double-one controlled update is involutive; only control-target separation is needed for this semantic theorem.", [7]),
        ("reversible", ["result:X-equivalence","result:CX-equivalence","result:CCX-equivalence"], "Typed proof instructions evaluate to basis equivalences; list executes head then tail, no primitive compilation implied.", [7]),
    ]
    edges = []
    for key, tails, formula, secs in steps:
        nid = "result:"+key
        nodes.append({"id": nid, "kind": "mathematical-construction-step", "formula": formula, "source_paragraphs": [p["id"] for p in pars if p["disposition"]=="NODE" and p["section"] in secs], "status": "AUTHOR_PROVISIONAL"})
        edges.append({"id":"construction:"+key,"logic":"AND","tails":tails,"heads":[nid],"status":"AUTHOR_PROVISIONAL","empty_tail_meaning":"Literal formula and finite/trigonometric calculation, not a consumer assumption." if not tails else None,"scope":"All tails jointly required for the named combined result; guarded constructor subcases are not simultaneously executed."})
    gaps = {
        "NORMALIZATION": "Derive a specified analytic norm-one proposition, rather than merely retain an arbitrary stored normalization Prop.",
        "PRESENTATION-DENOTATION": "Connect supplied state-preparation circuit/schedule/auxiliary metadata to the certified matrix and actual ancilla behavior.",
        "NAMED-WIRE-ENDIAN": "Supply an explicit certified equivalence to a chosen integer bit order before claiming flat physical ordering.",
        "CCX-FOUR-PRIMITIVE": "Compile proof-only CCX into X/RY/RZ/CX with exact phase-sensitive denotation and cost.",
        "RESOURCES-FINITE-BIT": "Cost angle evaluation/synthesis, preprocessing, connectivity/depth and implementation precision; metadata alone supplies none.",
        "SYMBOLIC-ENV-UNITARITY": "Supply semantic constraints on any symbolic rational environment and a separate actual unitarity proof.",
        "SUCCESS-CLEANUP": "Specify and prove other output sectors, cleanup, success probability or normalization if a downstream consumer needs them.",
    }
    gapids = ["SOURCE_GAP-"+key for key in gaps]
    nodes += [{"id":"SOURCE_GAP-"+key,"kind":"SOURCE_GAP","formula":value,"status":"OPEN_STRONGER_CONSUMER_NOT_REFUTATION"} for key,value in gaps.items()]
    guarded = [
        {"id":"delta-coordinate","guards":["row=index","row!=index"],"routes":["one","zero"]},
        {"id":"RY-RZ-entries","guards":["row/column=(0,0)","(0,1)","(1,0)","(1,1)"],"routes":["specified first diagonal","signed sine or zero","signed sine or zero","specified second diagonal"]},
        {"id":"CX-action","guards":["control bit=0","control bit!=0"],"routes":["unchanged","target flip"],"condition":"involution requires control!=target"},
        {"id":"lift-entry","guards":["other-wire restrictions equal","other-wire restrictions unequal"],"routes":["one-qubit entry","zero"]},
        {"id":"primitive-constructor","guards":["X","RY","RZ","CX"],"routes":["X permutation","lift Y","lift Z","CX permutation"]},
        {"id":"list-recursion","guards":["empty","head::tail"],"routes":["identity","head then tail; tail matrix on left"]},
        {"id":"CCX-action","guards":["both control bits=1","not both control bits=1"],"routes":["target flip","unchanged"],"condition":"both controls differ from target; syntax also separates controls"},
        {"id":"reversible-constructor","guards":["X","CX","CCX"],"routes":["single flip equivalence","controlled flip equivalence","doubly controlled flip equivalence"]},
        {"id":"empty-dimensions","guards":["qubits=0","qubits>0"],"routes":["one basis assignment, no instructions, program phase remains","named wires may exist; CX/CCX still require their inequalities"]},
    ]
    for item in guarded:
        item.update(join="OR",exhaustive=True,both_routes_required=False,status="AUTHOR_PROVISIONAL")
    return {
        "status":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT_TOPOLOGY",
        "views":{
            "source-construction-graph":{"status":"AUTHOR_PROVISIONAL","derived_from":"Frozen c28 mathematical source and author's own prior coverage, not decoder/reviewer input.","nodes":nodes,"AND_hyperedges":edges,"guarded_OR_cases":guarded,"open_source_gap_ids":gapids,
                "conditional_theorem_scope":"CX-equivalence, CCX-equivalence, coefficient-loader and generic lift nodes are conditional theorem interfaces with local binders. Their premises are not global requirements on unrelated constructors or every register.",
                "constructor_local_discharge":[
                    {"consumer":"result:gate-unitary","guard":"gate is CX","supplied_by":"Actual CX constructor distinctness field","not_added_to_other_cases":True},
                    {"consumer":"result:gate-unitary","guard":"gate is RY or RZ","supplied_by":"Explicit rotation-unitarity theorem; generic lift input unitarity is produced internally","not_public_premise":True},
                    {"consumer":"result:gate-dagger","guard":"gate is X or CX","supplied_by":"Appropriate involutive basis equivalence; CX field only in CX branch","not_added_to_rotations":True},
                    {"consumer":"result:reversible","guard":"instruction is CX or CCX","supplied_by":"Actual instruction constructor inequalities; CCX action theorem uses the two control-target fields","control_control_proof_not_required_by_action_theorem":True},
                ]},
            "lean-graph":{"status":"ACTUAL_IMPORT_AND_LEXICAL_OWNERSHIP_ONLY","target_import_edges":[{"from":"module:"+t["path"][:-5].replace("/","."),"to":"module:"+imp,"kind":"actual-module-import"} for t in targets for imp in t["imports"]],"ownership_edges":[{"from":"module:"+r["module"][:-5].replace("/","."),"to":"declaration:"+r["name"],"kind":"public-lexical-inventory-owner"} for r in roots],"elaborated_theorem_dependencies":[],"provider_import_index":PREFIX+"author-formal-context.json#provider_index","not_claimed":"No theorem-level proof-term dependency extraction or fresh elaboration."},
            "compressed-quantum-spine":{"status":"AUTHOR_NAVIGATION_ONLY_PENDING_PURIFICATION","groups":[{"id":"concept:finite-state-action","expands_to":["result:basis","result:first-column","result:certificate"]},{"id":"concept:clean-product-action","expands_to":["result:product-view","result:clean-action"]},{"id":"concept:exact-named-wire-primitive-semantics","expands_to":["result:RY","result:RZ","result:lift","result:gate-unitary","result:gate-dagger"]},{"id":"concept:chronological-phase-sensitive-programs","expands_to":["result:circuit","result:phase-unitary","result:program","result:refinement"]},{"id":"concept:reversible-proof-execution","expands_to":["result:CCX-equivalence","result:reversible"]}],"lossless_drilldown":[PREFIX+"author-source-coverage.json",PREFIX+"author-formal-context.json"],"purification":"PENDING","Exposition_Seal":"PENDING"},
            "functor-hypergraph":{"status":"AUTHOR_CONCEPTUAL_NOT_CERTIFIED_FUNCTOR","certified_transport":False,"hyperedges":[
                {"id":"transport:clean-basis-to-block","logic":"AND","tails":["result:basis","result:product-view"],"heads":["result:clean-action"],"formula":"clean output amplitude on each clean basis input equals projected matrix entry","hypothesis_map":"same signal index and high-signal/low-system embedding retained","conclusion_map":"pointwise exact block equality, no probability/normalizer added","failure_boundary":"A register permutation or integer-endian interpretation needs its own bridge.","independent_review":"PENDING"},
                {"id":"transport:named-wire-unitary-lift","logic":"AND","tails":["result:wire-split","premise:generic-gate-unitary","result:lift"],"heads":["result:lift-unitary"],"formula":"G unitary implies transported G tensor I unitary","hypothesis_map":"actual supplied one-qubit unitarity AND exact split bijection","conclusion_map":"same named-wire matrix, not a resource certificate","failure_boundary":"No generic G unitarity without its premise; no unnamed endian map.","independent_review":"PENDING"},
                {"id":"transport:phase-sensitive-program","logic":"AND","tails":["result:circuit","result:phase-unitary"],"heads":["result:program"],"formula":"exact chronological circuit matrix times exp(i phi)","hypothesis_map":"declared exact angle semantics, no phase quotient","conclusion_map":"unitary and dagger laws preserve exact global phase","failure_boundary":"A bare circuit refinement does not certify an arbitrarily phased program; no numerical export bound.","independent_review":"PENDING"}
            ],"not_claimed":"No categorical object/morphism laws, quantum synthesis advancement or automatic implication from a conceptual edge."},
        },
    }

def build(repo, out):
    assert out.is_dir()
    sealed = []
    for name, expected in ORIGINAL.items():
        item = file_record(out/name,name)
        assert item["sha256"] == expected, name
        sealed.append(item)
    source = (out/"source-only.md").read_bytes()
    targets, roots, ambient = [], [], []
    queue, closure = [], {}
    for short, (expected, count) in EXPECTED.items():
        relative = "QuantumBlockEncoding/"+short+".lean"
        raw = (repo/relative).read_bytes()
        assert sha(raw)==expected, relative
        rec = file_record(repo/relative,relative,True)
        rec["imports"] = imports(raw.decode())
        own = inventory(relative,raw)
        assert len(own)==count and not any(r["private"] for r in own), (short,len(own))
        targets.append(rec)
        roots += own
        queue += rec["imports"]
        commands = [{"line":idx+1,"exact_text":line} for idx,line in enumerate(raw.decode().splitlines(keepends=True)) if re.match(r"^(?:import |namespace |end\b|open |section\b|noncomputable section|set_option |variable |scoped |local |notation |instance )",line)]
        ambient.append({"module":relative,"commands":commands,"private_named_roots":[],"explicit_instances":[],"attributes_in_full_source":True,"full_source_bytes_retained":True,"implicit_binders":"Universe and autoimplicit parameters retained by exact lexical input; no elaborated signature claim.","noncomputable_policy":"Exact mathematical semantics, not a computability or runtime promise."})
    assert len(roots)==88 and len({r["name"] for r in roots})==88
    targetpaths = {t["path"] for t in targets}
    while queue:
        imp = queue.pop()
        if not imp.startswith("QuantumBlockEncoding."):
            continue
        relative = module_path(imp)
        if relative in targetpaths or relative in closure:
            continue
        raw = (repo/relative).read_bytes()
        rec = file_record(repo/relative,relative)
        rec.update(imports=imports(raw.decode()),permission="Read exact provider only after hash verification; context only, no whole-provider review credit.")
        closure[relative] = rec
        queue += rec["imports"]
    formal = {
        "status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","target_files":targets,
        "inventory":[{k:v for k,v in r.items() if k not in ("start_offset","lexical_header","lexical_block","body_sha256")} for r in roots],
        "inventory_count":88,"public_roots_per_module":{key:value[1] for key,value in EXPECTED.items()},"private_target_helper_count":0,
        "ambient_scope":ambient,"provider_index":[closure[k] for k in sorted(closure)],
        "dependency_context":[file_record(repo/p,p,True) for p in ("lean-toolchain","lake-manifest.json","lakefile.lean")],
        "type_authority":"Exact full byte/line arrays and lexical inventory, not elaborated types or successful Lean execution.",
        "fixed_read_boundary":{"targets":"Exactly three complete modules, all ambient bytes, 88 public lexical roots including inline attributes, abbrev and inductive; generated constructor/field infrastructure is retained inside source.","providers":"Exact local import closure indexed by relative path, hashes and imports; external source bounded by toolchain/manifest.","external":"Changed or unavailable bytes require resealing, not floating retrieval.","not_claimed":"No author desired conclusion, source identity, graph or previous outcome is supplied as a decoding guide."},
    }
    emit(out,"author-formal-context.json",formal)
    context_hash = sha((out/"author-formal-context.json").read_bytes())
    packet = {"status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","formal_context_path":PREFIX+"author-formal-context.json","formal_context_sha256":context_hash,"opaque_context_binding_sha256":context_hash,"target_modules":[t["path"] for t in targets],"inventory_count":88,"private_count":0,"required_work":"Read all complete formal target bytes and ambient commands, reconstruct every authored declaration and recursively inspect necessary provider definitions under their hashes. Distinguish exact lexical input from checked types. No author outcome is supplied.","fixed_read_boundary":formal["fixed_read_boundary"],"publication_binding_state":"LATE_BRIDGE_REQUIRED_AFTER_INDEPENDENT_FORMAL_RECONSTRUCTION_FREEZE","withheld":"Natural-language source/identity/lesson, author obligations and assumption audit, source topology, prior reconstruction and review conclusions."}
    emit(out,"author-decoder-packet.json",packet)
    with (out/"concrete-primitive-and-reversible-semantics.md").open("xb") as handle:
        handle.write(source)
    pars = paragraphs(source)
    descriptions = map_private_rows((out/"author-private-coverage.md").read_text(encoding="utf-8"))
    obligations = []
    for idx, root in enumerate(roots,1):
        local = root["lexical_local_name"]
        lookup = ".".join(root["name"].split(".")[2:]) if root["module"].endswith("/ConcreteSemantics.lean") else local
        assert lookup in descriptions, (root["name"],lookup)
        sec = sections_for(root["module"],local)
        audit = binder_audit(root)
        block = root["lexical_block"]
        members = None
        if root["kind"] in ("structure","inductive"):
            body = outside_definition_split(block)[1]
            members = body.split("\n\n",1)[0]
        obligations.append({
            "id":f"C28-{idx:03d}","name":root["name"],"module":root["module"],"line":root["line"],"kind":root["kind"],"private":root["private"],"status":WIP,
            "source_sections":sec,"source_paragraphs":[p["id"] for p in pars if p["section"] in sec and p["disposition"]=="NODE"],
            "source_obligation":descriptions[lookup]["mathematics"],"original_private_binder_note":descriptions[lookup]["binder_note"],
            "role":"mathematical-proof-edge" if root["kind"]=="theorem" else "literal-interface",
            "binder_audit":audit,"logical_inputs":[b for b in audit if b["classification"]=="SOURCE"],"typing_data_binders":[b for b in audit if b["classification"]=="TYPING"],
            "lexical_header_for_audit_only":root["lexical_header"],"output_logic":"All conclusion components/iff directions remain outputs, never moved into premises.",
            "definition_audit":{"kind":"theorem-not-definition" if root["kind"]=="theorem" else "literal","characterized_choice":False,"quotient_representative":False,"expanded_structure_or_inductive_members":members,"all_source_cases_retained":True},
            "proof_region_sha256":root["body_sha256"],"author_only":True,
        })
    bundle_specs = [
        ("QuantumBlockEncoding/StatePreparation.lean",["StatePreparationTarget","FirstColumnMatches","StatePreparationCandidate","VerifiedStatePreparation"]),
        ("QuantumBlockEncoding/PrimitiveCircuit.lean",["ExactAngle","PrimitiveGate","PrimitiveCircuit","PrimitiveProgram"]),
        ("QuantumBlockEncoding/ConcreteSemantics.lean",["ComplexUnitaryGate","ComplexStatePreparationCertificate","OtherPrimitiveWires"][:2]),
        ("QuantumBlockEncoding/PrimitiveSemantics.lean",["PrimitiveBasis","OtherPrimitiveWires","PrimitiveRefinement"]),
        ("QuantumBlockEncoding/ReversibleClassical.lean",["ReversibleGate","ReversibleProgram"]),
    ]
    bundles = {name:extract_bundle(repo,relative,name) for relative,names in bundle_specs for name in names}
    nested = {
        "StatePreparationTarget":{"normalization":"TYPING proposition parameter N, not a specified norm equation; no proof stored here.","amplitudes":"TYPING amplitude data","source":"TYPING metadata string"},
        "StatePreparationCandidate":{"isUnitary":"TYPING arbitrary proposition parameter; the concrete adapter selects actual matrix unitarity.","circuit_schedule_resource_auxiliary":"TYPING supplied metadata, not denotation/resource correctness"},
        "VerifiedStatePreparation":{"normalizationProof":"SOURCE evidence of candidate.target.normalization","unitaryProof":"SOURCE evidence of candidate.isUnitary","preparationProof":"SOURCE first-column equality; the adapter produces it from action"},
        "ComplexUnitaryGate":{"unitary":"SOURCE actual standard complex matrix unitarity"},
        "ComplexStatePreparationCertificate":{"target":"Expand StatePreparationTarget; N remains arbitrary","gate":"Expand ComplexUnitaryGate, including SOURCE unitarity","normalizationProof":"SOURCE evidence of target N","preparationProof":"SOURCE exact U e_0 = amplitudes"},
        "ExactAngle":{"bounded-arccos":"SOURCE |q|<=1","bounded-sqrt-arccos":"SOURCE 0<=q AND q<=1","all-other-constructors":"TYPING real expression data; real constructor has no numerical export promise"},
        "PrimitiveGate":{"cx.distinct":"SOURCE control!=target","rotation.angle":"Recursive ExactAngle evidence; no unitarity assumption on an instruction"},
        "PrimitiveCircuit":{"element":"Recursive PrimitiveGate constraints for each actual list element"},
        "PrimitiveProgram":{"circuit":"Recursive primitive constraints","globalPhase":"ExactAngle semantics with all nested domain evidence; global phase not discarded"},
        "ReversibleGate":{"cx.distinct":"SOURCE control!=target","ccx.c0_ne_c1":"SOURCE control0!=control1 at instruction syntax only","ccx.c0_ne_target":"SOURCE control0!=target","ccx.c1_ne_target":"SOURCE control1!=target"},
        "ReversibleProgram":{"element":"Recursive ReversibleGate constraints"},
        "OtherPrimitiveWires":{"property":"TYPING exclusion from target in subtype carrier; no extra top-level circuit premise"},
        "PrimitiveRefinement":{"exact":"SOURCE equality E(circuit)=target, not equality up to phase"},
        "Equiv":{"left_inv_right_inv":"SOURCE mutually inverse functions inside supplied equivalence data; no surjectivity theorem silently assumed from a raw function"},
    }
    graph = graph_views(pars,targets,roots)
    gapids = graph["views"]["source-construction-graph"]["open_source_gap_ids"]
    coverage = {
        "status":WIP,"role":"AUTHOR_CURATOR_NOT_INDEPENDENT_REVIEWER","source_path":LESSON,"source_sha256":ORIGINAL["source-only.md"],"source_bytes":len(source),
        "source_paragraphs":pars,"reconstruction":"Concatenate exact_text without separators to recover every original UTF-8 byte, including final newline.",
        "whole_module_inventory":obligations,"canonical_inventory_roots":88,"public_roots_per_module":formal["public_roots_per_module"],"private_target_helpers":0,"additional_top_level_named_instances":0,
        "ambient_scope":ambient,"full_target_source_context_sha256":context_hash,"project_owned_bundle_expansions":bundles,"nested_logical_field_audit":nested,
        "source_seal_timing":"RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS; historical formalizer UNKNOWN",
        "logical_input_policy":"Every explicit logical binder and recursive bundle proof remains SOURCE; outer carriers/objects and exact arithmetic instances are TYPING. Proved gate/circuit/program unitarity and adjoint conclusions remain produced outputs, never added hypotheses.",
        "definition_policy":"All literal definitions, no choice/quotient replacement, no zero fallback on an omitted valid locus.",
        "generated_declarations":"Constructor/field source is expanded in obligation records and bundles; compiler recursors/noConfusion/equation auxiliaries are EXCLUDED as generated infrastructure, not authored public roots.",
        "topology_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT","open_source_gap_ids":gapids,"remaining_boundary":RESIDUAL,
    }
    emit(out,"author-source-coverage.json",coverage)
    audit = {"status":WIP,"whole_module_inventory":[{"id":o["id"],"name":o["name"],"binder_audit":o["binder_audit"],"definition_audit":o["definition_audit"],"lexical_header_for_audit_only":o["lexical_header_for_audit_only"]} for o in obligations],"project_owned_bundle_expansions":bundles,"nested_logical_field_audit":nested,"classification_authority":"AUTHOR_PROVISIONAL, not a verdict. No STANDING/RULED/EXCESS is silently introduced.","original_private_coverage_unchanged":True,"refinement_note":"An outer equivalence/certificate/instruction parameter is data; its recursively stored logical evidence is separately SOURCE, not erased as mere typing."}
    emit(out,"author-binder-definition-audit.json",audit)
    graph["coverage_sha256"] = sha((out/"author-source-coverage.json").read_bytes())
    emit(out,"author-graph-views.json",graph)
    source_row = {
        "id":SOURCE_ID,"title":"Finite state action, exact primitive circuits, and reversible address logic",
        "authors":"Historical formalizer UNKNOWN; retrospective local AUTHOR-curator primitive-semantics-author-c28",
        "url":"https://github.com/DakeBU/Quantum-Computing-Block-Encoding","year":2026,"status":"primary-text-checked",
        "anchor":LESSON+" sections 1-8; immutable source UTF-8 SHA256 "+ORIGINAL["source-only.md"],
        "scope":"Three complete actual modules, 88 authored public lexical roots (25/55/8), all ambient bytes, no private named roots. Finite action/projection, exact phase-sensitive primitive semantics and reversible proof execution.",
        "formal_status":"AUTHOR/WIP retrospective source only; no independent acceptance, historical identity assertion, pre-proof provenance, novelty, fresh build, main admission or PURIFIED claim.",
    }
    emit(out,"author-source-row-candidate.json",{"status":WIP,"source":source_row,"immutability":"Prospective source-row data for read-only overlay; parent must not silently change the row once a binding is frozen."})
    catalog_raw = (repo/"website/research/sources.json").read_bytes()
    catalog = json.loads(catalog_raw)
    assert not any(s["id"]==SOURCE_ID for s in catalog["sources"]), "Existing source ID: reconcile without replacement."
    catalog["sources"].append(source_row)
    overlay = OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind, checker_hash = binding_function(repo)
    registry_raw = (repo/"website/research/publications.json").read_bytes()
    registry_count = len(json.loads(registry_raw)["records"])
    bindings = []
    for short in EXPECTED:
        relative = "QuantumBlockEncoding/"+short+".lean"
        own = [o for o in obligations if o["module"]==relative]
        contribution = {
            "baseline":BASE,"head":HEAD,"head_provenance":"Parent-supplied reference context; this continuation did not invoke Git.",
            "classes":["reorganisation","bridge"],"node_ids":["module:QuantumBlockEncoding."+short]+["declaration:"+o["name"] for o in own]+gapids,
            "views":["source-construction-graph","lean-graph","compressed-quantum-spine","functor-hypergraph"],
            "source_graph_sha256":sha((out/"author-graph-views.json").read_bytes()),"coverage_sha256":sha((out/"author-source-coverage.json").read_bytes()),
            "formal_context_sha256":context_hash,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
            "source_graph_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT",
            "preserved_contract":"Three whole production sources unchanged; metadata/source correspondence only, not a new mathematical result or canonical admission.",
            "remaining_boundary":RESIDUAL,
        }
        rec = {
            "module":relative,"source_id":SOURCE_ID,
            "source_statement":"Frozen retrospective local mathematical source sections 1-8, losslessly covered, with complete actual ambient/declarations and explicit conditional unitarity, evidence, metadata, phase/order, empty-carrier and consumer boundaries.",
            "source_anchor":LESSON+" sections 1-8","lesson_path":LESSON,"declarations":[o["name"] for o in own],
            "obligation_map":[{"kind":"proof-edge" if o["kind"]=="theorem" else "prerequisite","source_obligation":o["id"],"declarations":[o["name"]]} for o in own],
            "assumption_deltas":[
                {"classification":"same","source":"Stated coefficient interval, valid-wire inequalities, conditional input-matrix unitarity, and supplied certificate N/unitarity/action evidence.","formal":"All exact lexical logical binders and nested evidence-bearing records retained in author audit.","explanation":"Author proposal only; output gate/circuit/program unitarity is derived and is not inserted as a theorem premise."},
                {"classification":"source-implicit","source":"Natural finite dimensions, scalar algebra and exact real expressions; arbitrary normalization proposition and unconstrained presentation metadata are explicit.","formal":"Function-valued matrix carrier, full ambient imports, named-wire functions and high-signal/low-system product indices preserved.","explanation":"No analytic normalization, metadata implementation, endian identification, finite-bit cost, CCX compiler or phase quotient is inferred."},
            ],
            "graph_contribution":contribution,"formalizer":"primitive-semantics-author-c28 retrospective AUTHOR-curator; historical formalizer UNKNOWN",
            "historical_formalizer":"UNKNOWN","residual_boundary":RESIDUAL,
            "decoder_evidence":PREFIX+"decoder-pending/"+short+"-evidence.json","reviewer_evidence":PREFIX+"reviewer-pending/"+short+"-evidence.json",
            "evidence_paths_status":{"decoder":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE","reviewer":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE"},
            "status":WIP,"statement_seal":{"timing":"RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS","pre_proof_seal_claim":False},
            "source_proof_coverage":PREFIX+"author-source-coverage.json","binder_definition_audit":PREFIX+"author-binder-definition-audit.json",
            "graph_views":PREFIX+"author-graph-views.json","formal_context":PREFIX+"author-formal-context.json","formal_packet":PREFIX+"author-decoder-packet.json",
            "purification":{"status":"PENDING","Exposition_Seal":"PENDING"},"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,
        }
        rec["binding_sha256"] = bind(overlay,rec)
        emit(out,"publication-candidate-"+short+".json",rec)
        bindings.append({"module":relative,"binding_sha256":rec["binding_sha256"]})
    emit(out,"author-binding-bridge-proposal.json",{
        "status":WIP,"formal_context_sha256":context_hash,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),"bindings":bindings,
        "procedure":"Only after a fresh independently frozen formal-only reconstruction may the parent compare target/provider/dependency bytes and add a later opaque binding bridge. Author has read no decoder/reviewer output and supplies no acceptance.",
        "independent_input_binding_inspected":False,"decoder_reconstruction_inspected":False,"reviewer_result_inspected":False,"accepted":False,
    })
    emit(out,"formal-input-seal.json",{
        "status":"FORMAL_ONLY_FROZEN_NOT_ACCEPTANCE","formal_context_sha256":context_hash,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
        "target_bindings":[{k:t[k] for k in ("path","sha256","bytes")} for t in targets],"provider_index_sha256":sha(json.dumps(formal["provider_index"],sort_keys=True,ensure_ascii=False).encode()),
        "dependency_context":[{k:t[k] for k in ("path","sha256","bytes")} for t in formal["dependency_context"]],"public_roots":88,"private_helpers":0,
        "note":"Opaque formal-only input seal; no source row or author verdict is evidence.",
    })
    new_names = sorted(p.name for p in out.iterdir() if p.is_file() and p.name not in ORIGINAL)
    ambient_bindings = [file_record(path,path.relative_to(repo).as_posix()) for directory in ("QuantumBlockEncoding","ABEISTests") for path in sorted((repo/directory).rglob("*.lean"))]
    emit(out,"metadata-freeze.json",{
        "status":WIP,"head":HEAD,"base":BASE,"original_immutable_inputs":sealed,"new_artifacts":[file_record(out/name,name) for name in new_names],
        "whole_ambient_binding_inputs":ambient_bindings,"checker_path":"website/scripts/check_research_publications.py","checker_sha256":checker_hash,
        "binding_recipe":{"function":"binding_digest","function_unchanged":True,"fields":["module","source_id","source_statement","source_anchor","lesson_path","declarations","obligation_map","assumption_deltas","graph_contribution","formalizer","residual_boundary"],"virtual_data_overlay":[LESSON,"website/research/sources.json"],"method":"Unchanged trusted binding_digest called against read-only prospective lesson/source-row overlay; validate_record/check/main never called."},
        "registry_observed_count":registry_count,"registry_sha256":sha(registry_raw),"original_source_catalog_sha256":sha(catalog_raw),
        "format_reference":{"path":"hermite-substrate-author-c27r/author-package-build.py","use":"Mechanical serialization and unchanged-checker overlay pattern only; no mathematical content or independent outcome reused."},
        "all_artifacts_WIP":True,"independent_evidence_fabricated":False,"production_writes":False,"Lean_executed":False,"Git_executed_in_this_continuation":False,"acceptance":False,"freeze_self_hash_excluded":True,
    })
    report = verify(repo,out,manifest=False)
    emit(out,"mechanical-selftest.json",report)
    names = sorted([p.name for p in out.iterdir() if p.is_file()])
    artifacts = []
    for name in names:
        item = file_record(out/name,name)
        item["planned_canonical_path"] = LESSON if name=="concrete-primitive-and-reversible-semantics.md" else PREFIX+name
        artifacts.append(item)
    emit(out,"outputs-manifest.json",{
        "status":WIP,"artifacts":artifacts,"mechanical_selftest":report,"manifest_self_hash_excluded":True,"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,
        "recovery":"All artifacts are ordinary relative files. Original three byte bindings and deterministic generator are retained; source paragraph concatenation recovers the exact lesson, formal target/dependency arrays recover their frozen input bytes. Never overwrite other author packets on replay.",
        "planned_prefix":PREFIX,"lesson_path":LESSON,"all_output_paths_relative":True,
    })
    print(json.dumps(verify(repo,out,manifest=True),ensure_ascii=False,indent=2))

def verify(repo,out,manifest=True):
    load = lambda name: json.loads((out/name).read_bytes())
    frozen = load("metadata-freeze.json")
    for item in frozen["original_immutable_inputs"]+frozen["new_artifacts"]:
        data = (out/item["path"]).read_bytes()
        assert sha(data)==item["sha256"] and len(data)==item["bytes"], item["path"]
    for item in frozen["whole_ambient_binding_inputs"]:
        data = (repo/item["path"]).read_bytes()
        assert sha(data)==item["sha256"] and len(data)==item["bytes"], item["path"]
    formal, packet = load("author-formal-context.json"), load("author-decoder-packet.json")
    context_hash = sha((out/"author-formal-context.json").read_bytes())
    assert context_hash==packet["formal_context_sha256"]
    for item in formal["target_files"]+formal["dependency_context"]:
        data = bytes(item["full_source_utf8_bytes"])
        assert data=="".join(item["full_source_lines"]).encode()==(repo/item["path"]).read_bytes()
        assert sha(data)==item["sha256"]
    providers = {item["path"]:item for item in formal["provider_index"]}
    targets = {item["path"] for item in formal["target_files"]}
    for item in formal["target_files"]+formal["provider_index"]:
        data = (repo/item["path"]).read_bytes()
        assert sha(data)==item["sha256"] and imports(data.decode())==item["imports"]
        for imp in item["imports"]:
            if imp.startswith("QuantumBlockEncoding."):
                assert module_path(imp) in targets|providers.keys()
    roots = formal["inventory"]
    assert len(roots)==88 and not any(r["private"] for r in roots)
    cov = load("author-source-coverage.json")
    source = (out/"source-only.md").read_bytes()
    assert source==(out/"concrete-primitive-and-reversible-semantics.md").read_bytes()
    assert sha(source)==ORIGINAL["source-only.md"]
    assert "".join(p["exact_text"] for p in cov["source_paragraphs"]).encode()==source
    for p in cov["source_paragraphs"]:
        assert source[p["start_utf8_byte"]:p["end_utf8_byte"]]==p["exact_text"].encode()
        assert sha(p["exact_text"].encode())==p["sha256"]
        assert p["disposition"] in ("NODE","EXCLUDED") and (p["source_nodes"] or p["reason"])
    obligations = cov["whole_module_inventory"]
    assert {o["name"] for o in obligations}=={r["name"] for r in roots}
    assert all(o["source_paragraphs"] for o in obligations)
    assert all(b["classification"] in ("SOURCE","TYPING") for o in obligations for b in o["binder_audit"])
    graph = load("author-graph-views.json")
    sg = graph["views"]["source-construction-graph"]
    ids = {node["id"] for node in sg["nodes"]}
    assert len(ids)==len(sg["nodes"])
    for edge in sg["AND_hyperedges"]+graph["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"]=="AND" and set(edge["tails"]+edge["heads"])<=ids
    assert len(graph["views"]["lean-graph"]["ownership_edges"])==88
    for forbidden in (SOURCE_ID,LESSON,"source-construction-graph","publication_binding_sha256","source-only.md"):
        assert forbidden not in (out/"author-decoder-packet.json").read_text(encoding="utf-8")
    catalog = json.loads((repo/"website/research/sources.json").read_bytes())
    assert not any(s["id"]==SOURCE_ID for s in catalog["sources"])
    catalog["sources"].append(load("author-source-row-candidate.json")["source"])
    overlay = OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind, checker_hash = binding_function(repo)
    assert checker_hash==frozen["checker_sha256"]
    replay = []
    for short,(_,count) in EXPECTED.items():
        rec = load("publication-candidate-"+short+".json")
        own = {o["name"] for o in obligations if o["module"]==rec["module"]}
        assert len(own)==count and len(rec["declarations"])==count and set(rec["declarations"])==own
        assert {n for o in rec["obligation_map"] for n in o["declarations"]}==own
        assert rec["status"]==WIP and not rec["independent_acceptance"] and not rec["main_admission"]
        assert bind(overlay,rec)==rec["binding_sha256"]
        replay.append({"module":rec["module"],"binding_sha256":rec["binding_sha256"]})
    if manifest:
        man = load("outputs-manifest.json")
        for item in man["artifacts"]:
            data = (out/item["path"]).read_bytes()
            assert sha(data)==item["sha256"] and len(data)==item["bytes"], item["path"]
            assert not re.search(r"(?:[A-Za-z]:[\\/]|^/|\\)",item["planned_canonical_path"])
    return {
        "status":"MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION","whole_target_modules":3,"public_roots":88,"public_per_module":[25,55,8],"private_named_roots":0,
        "lossless_source_paragraphs":len(cov["source_paragraphs"]),"source_AND_edges":len(sg["AND_hyperedges"]),"open_SOURCE_GAPs":len(sg["open_source_gap_ids"]),
        "provider_closure_modules":len(providers),"binding_replayed_with_unchanged_checker":replay,"registry_observed_count":frozen["registry_observed_count"],
        "validate_record_called":False,"Lean_executed":False,"independent_evidence_fabricated":False,"main_admission":False,"scientific_ROOT":False,"PURIFIED":False,"manifest_verified":manifest,
    }

if __name__=="__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--verify",action="store_true")
    args = ap.parse_args()
    if args.verify:
        print(json.dumps(verify(args.repo.resolve(),args.out.resolve()),ensure_ascii=False,indent=2))
    else:
        build(args.repo.resolve(),args.out.resolve())
