#!/usr/bin/env python3
"""Deterministic serialization of an AUTHOR/WIP packet; never admission.

Arguments choose the read-only repository and this existing author directory.
No Git, Lean, cache, independent-result, registry-write or acceptance API is used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PREFIX = "reviews/publication/hermite-substrate-c27/"
LESSON = "docs/lessons/hermite-regularity-cuts-and-stored-kernels.md"
SOURCE_ID = "aspbe-local-hermite-substrate"
HEAD = "cc25e39022db29ce9f98e77708850ce2dc0b0739"
BASE = "f2cba045611a0d11c5995c29607569726bf1d6c5"
WIP = "AUTHOR_WIP_NOT_ADMITTED"
EXPECTED = {
    "HermiteSmoothness": "fd345e839442cb2355a475d2dfa8a16e50cd33d59a1e7e05acbbba228f813004",
    "HermiteTransferCores": "bdcdde7754a59d67870a5b0d9e169d9ef20b7fbe161e2ce719b310cdb6a938ec",
    "HermiteBinaryCutoff": "728f7afa19181bbd3fe6e8d2d3eb66ea1862b01932afef0be8a50cd557a7a212",
    "StoredHermiteChildGeometry": "8315b9e37fd060decf3b8ba41ef4101a9b4e21baafc35b61b0fe6bddeb7588f2",
    "StoredHermiteKernelTable": "a0fd513ed0e1d7a826080660871103b492329c6577e7aec6d0cfedfc2d49bc12",
}
SHORT = dict(zip(EXPECTED, ("smoothness", "transfer", "binary-cutoff", "child-geometry", "kernel-table")))
SOURCE_HASH = "b971e269ccf4f89dde39ba87eb385a9c6d200acb97d570738f2b5bbac85784fd"
ROOT_RE = re.compile(r"^(?P<private>private\s+)?(?:noncomputable\s+)?(?:@\[[^\n]*?\]\s+)?(?P<kind>def|theorem|structure|abbrev|instance)\s+(?P<name>[\w']+)", re.M)
PROOF_NAMES = {"hf", "hg", "hv", "hd", "hjet", "hj", "hp", "hL", "hlo", "hhi", "hl", "hw", "hs", "hm", "hc", "hr", "h", "correct"}
SUPPLIED_NAMES = {"parent", "level", "span", "cut", "midpoint", "fields", "f"}
SECTION_ROOTS = {
 "HermiteSmoothness": {
  "splice":[2], "hasDerivAt_ite_of_eq":[2], "hasDerivAt_splice":[2], "deriv_splice":[2],
  "contDiff_splice":[3], "iteratedDeriv_exp":[3], "iteratedDeriv_exp_neg":[3],
  "contDiff_right_splice":[1,3], "right_splice_eventuallyEq":[3], "contDiff_double_splice":[3],
  "smoothInitial_eq_double_splice":[1,3], "smoothInitial_contDiff":[1,3]},
 "HermiteTransferCores": {},
 "HermiteBinaryCutoff": {"below":[6],"search":[6],"search_cost":[6],"half_span":[6],"middle_point":[5,6],"search_value":[5,6],"compute":[6],"root_span":[5,6],"compute_value":[5,6],"compute_cost":[6],"compute_comparisons":[6],"compute_field_operations":[6]},
 "StoredHermiteChildGeometry": {
  "Flags":[8],"flags":[7,8],"flags_full":[7,8],"flags_partial":[7,8],"flags_cost":[8],
  "Child":[8],"ChildRun":[6,8],"child":[8],"child_first":[8],"child_lower":[8],"child_upper":[8],
  "child_flags":[7,8],"child_cost":[8],"child_integerAdditions":[8],"child_refines":[7,8],
  "children":[9],"children_value":[9],"children_cost":[9],"children_integerAdditions":[9],
  "children_total_cost":[9],"Refines":[8,9],"children_refines":[9],"children_certified":[8,9],"child_index_word_bound":[9]},
 "StoredHermiteKernelTable": {"Fields":[10],"blockView":[11],"storedBlock":[11],"storedBlock_value":[11],"decode":[10,11],"entry":[11],"entry_value":[11],"assemble":[12],"assemble_value":[12],"tick_le_one":[6,12],"storedBlock_cost_le":[11],"entry_cost_le":[11],"assemble_cost_le":[12],"assemble_total_cost_le":[12],"SourceCorrect":[13],"blockView_source":[13,14],"assemble_source":[13,14]}}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def emit(out: Path, name: str, data) -> None:
    (out/name).write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())

def load(out: Path, name: str):
    return json.loads((out/name).read_bytes())

def file_record(path: Path, relative: str, full: bool = False):
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    result = {"path": relative, "sha256": sha(raw), "bytes": len(raw)}
    if full:
        result.update(full_source_lines=text.splitlines(keepends=True), full_source_utf8_bytes=list(raw))
        assert "".join(result["full_source_lines"]).encode() == raw
    return result

def imports(text: str):
    return re.findall(r"^import\s+(\S+)\s*$", text, re.M)

def module_path(name: str):
    return name.replace(".", "/") + ".lean"

def inventory(path: str, raw: bytes):
    text = raw.decode()
    ns = re.search(r"^namespace\s+(\S+)", text, re.M).group(1)
    roots = []
    for index, match in enumerate(ROOT_RE.finditer(text)):
        roots.append({"name": ns+"."+match["name"], "module": path,
                      "kind": match["kind"], "line": text.count("\n",0,match.start())+1,
                      "private": bool(match["private"]), "lexical_local_name": match["name"],
                      "start_offset": match.start()})
    for i, root in enumerate(roots):
        end = roots[i+1]["start_offset"] if i+1<len(roots) else len(text)
        block = text[root["start_offset"]:end]
        header = re.split(r"\s:=|\swhere\b",block,maxsplit=1)[0]
        root["lexical_header"] = header.rstrip()
        root["body_sha256"] = sha(block.encode())
    return roots

def audit_binders(root):
    """Lexical binder groups only; never described as elaborated signatures."""
    text=root["lexical_header"]
    match=ROOT_RE.match(text)
    tail=text[match.end():].lstrip()
    result=[]
    while tail and tail[0] in "({[":
        stack=[]; end=None
        for i,c in enumerate(tail):
            if c in "({[": stack.append(c)
            elif c in ")}]":
                if not stack: break
                stack.pop()
                if not stack: end=i+1; break
        assert end is not None, root["name"]
        group=tail[:end]
        content=group[1:-1]
        names=content.split(":",1)[0].split() if ":" in content else []
        is_proof=any(n in PROOF_NAMES for n in names)
        is_data=("StoredHermite" in root["module"] and any(n in SUPPLIED_NAMES for n in names))
        cls="SOURCE" if is_proof or is_data else "TYPING"
        reason=("Substantive stated analytic/algebraic/invariant/cache/supplier premise; not mere type formation."
                if is_proof else "Supplied materialized data or cached input; no uncharged source production is inferred."
                if is_data else "Carrier, dimension, point, index or literal formula parameter; no hidden correctness promise.")
        result.append({"exact_lexical_binder":group,"classification":cls,"reason":reason})
        tail=tail[end:].lstrip()
    return result

def exact_definition(repo, relative, local):
    text=(repo/relative).read_bytes().decode()
    match=re.search(r"^(?:noncomputable )?(?:def|abbrev|structure) "+re.escape(local)+r"\b[\s\S]*?(?=\n\n|\Z)",text,re.M)
    assert match,(relative,local)
    return {"provider_path":relative,"provider_sha256":sha((repo/relative).read_bytes()),"exact_lexical_definition":match[0],"scope":"Literal project-owned bundle expansion; signature elaboration remains a separate gate."}

def paragraphs(raw):
    text=raw.decode()
    pieces=re.findall(r"[^\n](?:.*?)(?:\n[ \t]*\n+|\Z)|\n+",text,re.S)
    assert "".join(pieces)==text
    result=[]; offset=0; line=1; section=None
    for i,piece in enumerate(pieces):
        heading=re.match(r"## (S\d+)\.",piece)
        if heading: section=heading[1]
        navigation=piece.lstrip().startswith("#") or not piece.strip()
        pbytes=piece.encode()
        item={"id":f"paragraph:{i+1:03d}","source_lines":[line,line+piece.rstrip("\n").count("\n")],
              "section":section,"start_utf8_byte":offset,"end_utf8_byte":offset+len(pbytes),
              "exact_text":piece,"sha256":sha(pbytes),
              "disposition":"EXCLUDED" if navigation else "NODE",
              "reason":"title/section navigation or blank separator" if navigation else None,
              "source_nodes":[] if navigation else [f"source:{i+1:03d}"],
              "disposition_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT"}
        result.append(item);offset+=len(pbytes);line+=piece.count("\n")
    return result

def source_graph(pars, targets, roots):
    nodes=[{"id":p["source_nodes"][0],"kind":"source-paragraph","paragraph_id":p["id"],"section":p["section"],"sha256":p["sha256"],"status":"AUTHOR_PROVISIONAL"} for p in pars if p["disposition"]=="NODE"]
    inputs={
      "poly-formula":"Finite a(k,r), A_k, B_k and P_k formulas; arbitrary natural k.",
      "common-slopes":"Two real functions have common derivative d and equal values at x; arbitrary decidable selector.",
      "splice-data":"Both real branches are differentiable everywhere, with equal values AND equal derivatives at the cut.",
      "glue-data":"Both branches globally C^k and all jets j=0..k agree at the cut.",
      "degree":"q is a supplied real polynomial with natDegree(q)≤d.",
      "grid-positive":"n≥0, L>0, h=πL/2^n and affine origin -πL.",
      "search-invariant":"start≤C≤start+2^r, lower=p_start, span=h*2^r.",
      "raw-search-data":"Arbitrary natural r,start and supplied real lower/span; exact-real compare primitive.",
      "cache-parent":"parent.first=s_(r+1).",
      "cache-lower":"parent.lower=origin+grid*parent.first.",
      "cache-width":"level.width=grid*2^r.",
      "cache-span":"supplied span=2^r.",
      "cache-midpoint":"supplied midpoint=2^n.",
      "word-legal":"cut≤2^n and r≤n; single-word integer model.",
      "stored-records":"Two supplied materialized seven-field records, not matrix entry callbacks.",
      "supplier-1":"For each bit, leftPartial is exact Partial(0,C,first,2^r).",
      "supplier-2":"For each bit, leftInjection is Full-guarded exp(last included point), zero if disabled.",
      "supplier-3":"For each bit, leftFree is the specified bounded-tail expression.",
      "supplier-4":"For each bit, middlePartial is exact Partial(C,2^n,first,2^r).",
      "supplier-5":"For each bit and coefficient, middleInjection is Full-guarded literal restriction, zero if disabled.",
      "supplier-6":"For each bit and indices, shared stored matrix equals the finite subdivision expression.",
      "supplier-7":"For each bit, rightCore has root guard r=n, otherwise the specified right-tail factor.",
      "fixed-layout":"D=2k+6 with explicit boundary/coefficient tags and bit*D+outgoing flattening.",
      "charged-storage":"Materialize each entry once, then two read/write passes per entry and row reference; eight counter components.",
      "restriction-literal":"Finite Bernstein β and de Casteljau restriction with total division; affine interpretation separately needs u≠1."}
    nodes += [{"id":"premise:"+k,"kind":"stated-local-input","formula":v,"classification":"SOURCE","not_a_produced_output":True,"status":"AUTHOR_PROVISIONAL"} for k,v in inputs.items()]
    defs=[
      ("polynomial-jets",["premise:poly-formula"],"Degree≤2k+1, both endpoint jets for every j≤k, positivity and uniqueness.",[1]),
      ("selector-derivative",["premise:common-slopes"],"Arbitrary-selector derivative from common difference-quotient limits.",[2]),
      ("splice-derivative",["result:selector-derivative","premise:splice-data"],"Threshold derivative splice using local branch equality away from cut.",[2]),
      ("finite-glue",["premise:glue-data","result:splice-derivative"],"C^k splice by induction, including k=0.",[3]),
      ("right-glue",["result:polynomial-jets","result:finite-glue"],"P_k/right exponential globally C^k; polynomial agreement on neighborhood of -1.",[3]),
      ("literal-smooth",["result:right-glue","result:polynomial-jets","result:finite-glue"],"Second join at -1 equals literal ≤0 middle function, globally C^k.",[1,3]),
      ("translation-update",[],"Binomial matrix row v_d(x)T_d(w)=v_d(x+w); triangular zeros, for every d,x,w without a polynomial degree premise.",[4]),
      ("translation-eval",["premise:degree","result:translation-update"],"Finite successive row contraction equals q(origin+sum weights), including empty list.",[4]),
      ("hermite-transfer",["result:translation-eval","result:polynomial-jets"],"Specialize q=P_k and d=2k+1, dimension 2k+2.",[4]),
      ("cut-laws",["premise:grid-positive"],"C in [0,2^n]; strict threshold cut and midpoint membership laws.",[5]),
      ("search-correct",["premise:grid-positive","premise:search-invariant","result:cut-laws"],"Exact search value=C by closed interval invariant, endpoint and one-cell cases included.",[6]),
      ("search-cost",["premise:raw-search-data"],"Exact vector 2r field+(r+1) compare for all data.",[6]),
      ("root-cut",["premise:grid-positive","result:cut-laws","result:search-correct","result:search-cost"],"The same initialized run returns C with 2n+2 field,n+1 compare.",[6]),
      ("flags",[],"Four literal integer comparisons and two writes produce Full/Partial flags when last=first+size.",[7,8]),
      ("child-literal",["result:flags"],"Actual child formulas; 3F+9C+7R+11W and two separate integer additions.",[8]),
      ("child-refinement",["result:child-literal"]+["premise:cache-"+x for x in ("parent","lower","width","span","midpoint")],"All seven child value/flag equalities, no coordinate output assumed.",[7,8]),
      ("pair-same-run",["result:child-literal","result:child-refinement","premise:charged-storage"]+["premise:cache-"+x for x in ("parent","lower","width","span","midpoint")],"Both children in false/true order, source refinement, total70 and integer additions4 in the same run. Costs themselves do not require cache coherence.",[9]),
      ("word-bound",["premise:cache-parent","premise:cache-span","premise:word-legal","result:child-literal"],"first+span<2^(n+2); this is a width requirement, not bitcost.",[9]),
      ("block-reader",["premise:stored-records","premise:fixed-layout"],"Exact tagged block semantics with reads/Bool selection/8 dispatch comparisons, two 8-comparison index decodes.",[10,11]),
      ("table-same-run",["result:block-reader","premise:charged-storage","premise:fixed-layout"],"Exact two-slice table from same materializing run; each counter≤72D²,total≤576D².",[12]),
      ("source-formulas",["premise:restriction-literal"],"Literal Full-guarded injections, finite Bernstein S_b, free tails and right root guard.",[13]),
      ("conditional-kernel",["premise:stored-records","premise:fixed-layout","result:source-formulas","result:table-same-run"]+["premise:supplier-"+str(i) for i in range(1,8)],"Exact local source-kernel equality for returned table; all seven suppliers for both bits are AND prerequisites.",[13,14])]
    edges=[]
    for key,tails,conclusion,sections in defs:
        nid="result:"+key
        associated=[p["id"] for p in pars if p["disposition"]=="NODE" and p["section"] in ["S"+str(s) for s in sections]]
        nodes.append({"id":nid,"kind":"mathematical-construction-step","formula":conclusion,"source_paragraphs":associated,"status":"AUTHOR_PROVISIONAL"})
        edges.append({"id":"construction:"+key,"logic":"AND","tails":tails,"heads":[nid],"empty_tail_meaning":"literal finite definition/calculation, not a consumer assumption" if not tails else None,"status":"AUTHOR_PROVISIONAL","tail_scope":"Local statement premises and constructed dependencies are distinct; complete listed tails are jointly required."})
    gaps=[
      ("SOURCE_GAP-SUPPLIER-PRODUCTION","Generate/cache all supplied parent/span/midpoint and seven field records, with source-correctness AND complete cost, not just receive them."),
      ("SOURCE_GAP-INTEGER-BITCOST","Natural powers, schedule/index arithmetic, casts and arbitrary-integer/word implementation costs omitted by selected counters."),
      ("SOURCE_GAP-FINITE-REAL-COMPARISON","Finite encodings, separation at exact thresholds, and numerical comparison/error analysis."),
      ("SOURCE_GAP-REPRESENTATION-BRIDGE","Identify monomial translation with Bernstein restricted stored blocks through an explicit adapter, not dimension equality."),
      ("SOURCE_GAP-COMPLETE-RAW-CHAIN","Produce every raw source chain core and its boundaries, normalization and all-word target equality from the costed suppliers."),
      ("SOURCE_GAP-QUANTUM-CONSUMER","Unitary/isometry/circuit/oracle realization, register cleanup, resource and finite-angle synthesis semantics remain external consumers.")]
    nodes += [{"id":k,"kind":"SOURCE_GAP","formula":v,"status":"OPEN_STRONGER_CONSUMER_NOT_REFUTATION"} for k,v in gaps]
    return {
      "status":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT_TOPOLOGY",
      "shared_modules":[t["path"] for t in targets],
      "views":{
       "source-construction-graph":{"status":"AUTHOR_PROVISIONAL","derived_from":"Frozen source-only mathematics; no decoder/reviewer topology consulted.","nodes":nodes,"AND_hyperedges":edges,
          "lanes":[{"id":"A","sections":["S1","S2","S3","S4"],"scope":"regularity and monomial transfer"},{"id":"B","sections":["S5","S6","S7","S8","S9","S10","S11","S12","S13","S14"],"scope":"exact cut and conditional stored suppliers"}],
          "guarded_OR_cases":[
            {"id":"finite-glue-order","join":"OR","guards":["k=0","k is a positive successor"],"routes":["Matching values give continuity, no differentiability required","C^(j+1) gives differentiability; differentiate splice, shift jet orders, apply induction"],"both_routes_required":False,"exhaustive":True,"note":"The generic derivative lemma is a conditional theorem used only on the successor branch; it does not turn C^0 inputs into differentiable functions."},
            {"id":"search-halves","join":"OR","guards":["middle<-1","not middle<-1"],"routes":["upper half with shifted start","lower half with same start"],"both_routes_required":False,"exhaustive":True,"same_branch-independent_cost":True},
            {"id":"one-cell","join":"OR","guards":["lower<-1","not lower<-1"],"routes":["return start+1","return start"],"both_routes_required":False,"exhaustive":True},
            {"id":"child-selection","join":"OR","guards":["bit=false","bit=true"],"routes":["offset=(0,0)","offset=(1,span)"],"both_routes_required":False,"exhaustive":True,"pair_producer_note":"The pair calls each branch once; a single-child statement does not require both guards."},
            {"id":"block-tag-cases","join":"OR","guards":["left boundary/boundary","left boundary/free","left free/free","middle boundary/boundary","middle boundary/coefficient","middle coefficient/coefficient","right/right","all remaining tag pairs"],"routes":["read flag/select","read left injection","read left free","read flag/select","read vector/ref/scalar","read matrix/ref/row/scalar","read right scalar","literal zero"],"both_routes_required":False,"exhaustive":True},
            {"id":"supplier-injection-guards","join":"OR","guards":["Full target child","not Full target child"],"routes":["supplied literal injection","supplied numerical zero"],"both_routes_required":False,"exhaustive":True,"note":"Both guard implications belong to each single equality; do not erase disabled-zero data."}],
          "alternative_end_to_end_OR_routes":[],"open_source_gap_ids":[k for k,_ in gaps],"source_hypothesis_policy":"A downstream desired table equality is never a supplier clause. Cache/field promises are genuine conditional inputs; degree and endpoint results for the actual P_k are produced prerequisites, not new smoothness assumptions."},
       "lean-graph":{"status":"ACTUAL_IMPORT_AND_LEXICAL_OWNERSHIP_ONLY",
          "target_import_edges":[{"from":"module:"+t["path"][:-5].replace("/","."),"to":"module:"+i,"kind":"actual-module-import"} for t in targets for i in t["imports"]],
          "ownership_edges":[{"from":"module:"+r["module"][:-5].replace("/","."),"to":("private-lexical:" if r["private"] else "declaration:")+r["name"],"kind":"private-lexical-owner" if r["private"] else "public-lexical-inventory-owner"} for r in roots],
          "provider_import_index":PREFIX+"author-formal-context.json#provider_index","elaborated_theorem_dependencies":[],"not_claimed":"Lexical ownership and import closure do not extract compiler proof-term dependencies or prove fresh elaboration."},
       "compressed-quantum-spine":{"status":"AUTHOR_NAVIGATION_ONLY_PENDING_PURIFICATION","groups":[
          {"id":"concept:hermite-finite-order-source","expands_to":["result:polynomial-jets","result:literal-smooth","result:hermite-transfer"]},
          {"id":"concept:exact-real-cut-and-conditional-geometry","expands_to":["result:cut-laws","result:root-cut","result:child-refinement","result:pair-same-run","result:word-bound"]},
          {"id":"concept:conditional-stored-kernel-table","expands_to":["result:block-reader","result:table-same-run","result:source-formulas","result:conditional-kernel"]}],
          "lossless_drilldown":[PREFIX+"author-source-coverage.json",PREFIX+"author-formal-context.json"],"purification":"PENDING","Exposition_Seal":"PENDING"},
       "functor-hypergraph":{"status":"AUTHOR_CONCEPTUAL_NOT_CERTIFIED_FUNCTOR","certified_transport":False,"hyperedges":[
          {"id":"transport:polynomial-affine-features","logic":"AND","tails":["premise:degree","result:translation-update","result:translation-eval"],"heads":["result:hermite-transfer"],"formula":"q(a+sum w) from monomial features and coefficient contraction; P_k only after its actual degree result.","hypothesis_map":"degree bound and explicit weights preserved","conclusion_map":"scalar evaluation, not quantum state or cost","failure_boundary":"wrong degree truncates coefficients; no numerical stability or preprocessing follows","independent_review":"PENDING"},
          {"id":"transport:stored-record-to-source-block","logic":"AND","tails":["premise:stored-records","premise:fixed-layout"]+["premise:supplier-"+str(i) for i in range(1,8)]+["result:table-same-run"],"heads":["result:conditional-kernel"],"formula":"Materialized two-bit-slice blocks equal the specified local kernel, under every field supplier clause.","hypothesis_map":"all seven equalities for both bits, disabled zeros and root guard retained","conclusion_map":"same returned stored table, eight operation counters preserved","failure_boundary":"not a field generator, whole chain, finite-bit routine or coherent oracle","independent_review":"PENDING"}],"source_graph_authority":"AUTHOR_PROVISIONAL","not_claimed":"No typed categorical object/morphism maps or identity/composition certificates; conceptual routes are not compiler dependency edges."}}}

class ShadowFile:
    def __init__(self, canonical, data): self.canonical=canonical; self.data=data
    def resolve(self): return self.canonical.resolve()
    def is_file(self): return True
    def read_bytes(self): return self.data
    def read_text(self, encoding="utf-8"): return self.data.decode(encoding)

class OverlayRoot:
    """Read-only virtual files for the unchanged checker's binding function."""
    def __init__(self, repo, overlay): self.repo=repo; self.overlay=overlay
    def __fspath__(self): return str(self.repo)
    def resolve(self): return self.repo.resolve()
    def __truediv__(self, name):
        name=str(name)
        return ShadowFile(self.repo/name,self.overlay[name]) if name in self.overlay else self.repo/name

def binding_function(repo):
    namespace={"__file__":str(repo/"website/scripts/check_research_publications.py"),"__name__":"author_readonly_binding"}
    code=(repo/"website/scripts/check_research_publications.py").read_bytes()
    exec(compile(code,namespace["__file__"],"exec"),namespace)
    return namespace["binding_digest"],sha(code)

def build(repo, out):
    assert out.is_dir()
    sealed={name:file_record(out/name,name) for name in ("source-only.md","author-private-coverage.md","source-freeze.md","handoff.md")}
    source=(out/"source-only.md").read_bytes()
    assert sha(source)==SOURCE_HASH
    targets=[]; roots=[]; ambient=[]; closure={}; queue=[]
    for short,expected in EXPECTED.items():
        path="QuantumBlockEncoding/"+short+".lean"
        raw=(repo/path).read_bytes(); assert sha(raw)==expected, path
        rec=file_record(repo/path,path,True); rec["imports"]=imports(raw.decode()); targets.append(rec)
        local_roots=inventory(path,raw);roots+=local_roots;queue+=rec["imports"]
        commands=[{"line":i+1,"exact_text":line} for i,line in enumerate(raw.decode().splitlines(keepends=True)) if re.match(r"^(?:import |namespace |end\b|open |noncomputable section|set_option |variable |scoped |local |notation )",line)]
        ambient.append({"module":path,"commands":commands,"private_helpers":[r["name"] for r in local_roots if r["private"]],"additional_named_instances":[],"all_source_bytes_retained":True})
    target_paths={t["path"] for t in targets}
    while queue:
        name=queue.pop()
        if not name.startswith("QuantumBlockEncoding."): continue
        path=module_path(name)
        if path in target_paths or path in closure: continue
        data=(repo/path).read_bytes()
        rec=file_record(repo/path,path);rec["imports"]=imports(data.decode())
        rec["permission"]="Read exact provider path only after matching hash; context-only, no new whole-provider review or theorem dependency claim."
        closure[path]=rec;queue+=rec["imports"]
    assert len(roots)==75 and sum(not r["private"] for r in roots)==71
    formal={"status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","target_files":targets,
      "inventory":[{k:v for k,v in r.items() if k not in ("start_offset","lexical_header","body_sha256")} for r in roots],
      "inventory_count":71,"private_target_helper_count":4,"ambient_scope":ambient,
      "provider_index":[closure[k] for k in sorted(closure)],
      "type_authority":"Full byte arrays and line arrays are exact lexical input, not elaborated signatures. Fresh checked types require the separate authorized formal process.",
      "dependency_context":[file_record(repo/p,p,True) for p in ("lean-toolchain","lake-manifest.json")],
      "fixed_read_boundary":{"targets":"Exactly five complete target byte arrays, all ambient scope and all 71 public/4 private lexical roots.","providers":"Complete actual local-import closure indexed by exact relative paths/hashes/imports; external library source follows the dependency manifest.","external":"Missing or changed bytes require a resealed request, not floating retrieval.","not_claimed":"No source identity, lesson, desired verdict, author obligations or graph are supplied. Import indexing is not elaborated proof-term analysis."}}
    emit(out,"author-formal-context.json",formal)
    context_hash=sha((out/"author-formal-context.json").read_bytes())
    packet={"status":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","formal_context_path":PREFIX+"author-formal-context.json","formal_context_sha256":context_hash,"opaque_context_binding_sha256":context_hash,"target_modules":[t["path"] for t in targets],"inventory_count":71,"additional_top_level_named_instance_or_private_count":4,"required_work":"Read complete target byte arrays/ambient scope and each 71 public and 4 private lexical root. Independently reconstruct mathematical meanings and exact checked types. Verify provider hashes before reading permitted provider files. No author outcome or acceptance is supplied.","fixed_read_boundary":formal["fixed_read_boundary"],"publication_binding_state":"LATE_BRIDGE_REQUIRED_AFTER_INDEPENDENT_FORMAL_RECONSTRUCTION_FREEZE","withheld":"Natural-language source/identity/lesson, author obligations and assumption audit, source topology, any earlier reconstruction or review outcome."}
    emit(out,"author-decoder-packet.json",packet)
    (out/"hermite-regularity-cuts-and-stored-kernels.md").write_bytes(source)
    pars=paragraphs(source)
    private_text=(out/"author-private-coverage.md").read_text(encoding="utf-8")
    descriptions={}
    module=None
    for line in private_text.splitlines():
        m=re.match(r"### (\w+):",line)
        if m:module=m[1]
        m=re.match(r"\| (\d+) (?:private )?(\w+) \| (.*?) \|$",line)
        if m and module:descriptions[(module,m[2])]=m[3]
    obligations=[]
    for idx,r in enumerate(roots):
        m=r["module"].split("/")[-1][:-5];name=r["lexical_local_name"]
        sections=SECTION_ROOTS[m].get(name,[4] if m=="HermiteTransferCores" else [])
        assert sections,(m,name)
        binders=audit_binders(r)
        field_expansion=None
        if name in ("Flags","Child","ChildRun","Fields","SourceCorrect"):
            text=(repo/r["module"]).read_bytes().decode()
            pos=r["start_offset"];following=[x["start_offset"] for x in roots if x["module"]==r["module"] and x["start_offset"]>pos]
            field_expansion=text[pos:min(following) if following else len(text)].split("where",1)[1].strip()
        obligations.append({"id":f"HS-{idx+1:02d}","name":r["name"],"module":r["module"],"line":r["line"],"kind":r["kind"],"private":r["private"],"status":WIP,"author_only":True,
          "source_sections":["S"+str(s) for s in sections],"source_paragraphs":[p["id"] for p in pars if p["section"] in ["S"+str(s) for s in sections] and p["disposition"]=="NODE"],
          "source_obligation":descriptions[(m,name)],"role":"internal-bookkeeping" if r["private"] else "literal-interface" if r["kind"]!="theorem" else "mathematical-proof-edge",
          "binder_audit":binders,"logical_inputs":[b for b in binders if b["classification"]=="SOURCE"],"typing_data_binders":[b for b in binders if b["classification"]=="TYPING"],
          "lexical_header_for_audit_only":r["lexical_header"],"output_logic":"AND; all conclusion components remain outputs, never premises",
          "output_conjuncts":[descriptions[(m,name)]],
          "definition_audit":{"kind":"theorem-not-definition" if r["kind"]=="theorem" else "literal","characterized_choice":False,"quotient_representative":False,"expanded_structure_fields":field_expansion,"field_classification":"SOURCE supplier equalities, all seven clauses are substantive" if name=="SourceCorrect" else "literal stored payload / type fields; no implicit semantic promise" if field_expansion else None},
          "no_excess_or_ruling_claim":"Author proposal only; exact source and later independent comparison decide fidelity."})
    graph=source_graph(pars,targets,roots)
    gapids=graph["views"]["source-construction-graph"]["open_source_gap_ids"]
    coverage={"status":WIP,"role":"AUTHOR_CURATOR_NOT_INDEPENDENT_REVIEWER","source_path":LESSON,"source_sha256":SOURCE_HASH,"source_bytes":len(source),"paragraph_count":len(pars),"reconstruction":"Concatenate exact_text with no added separators; preserve every byte, indent and final LF.","source_paragraphs":pars,"whole_module_inventory":obligations,"canonical_inventory_roots":71,"additional_top_level_named_instances":0,"private_target_helpers":4,"ambient_scope":ambient,"full_target_source_context_sha256":context_hash,"logical_input_policy":"Cache equalities, degree/differentiability/jet promises, L>0 and invariant inequalities and SourceCorrect clauses remain substantive SOURCE premises of conditional statements. Actual source-polynomial jets/degree and target outputs remain produced dependencies.","source_explanation_note":"Provider and explanatory mathematics is included as context with exact paragraph disposition, not falsely counted as new named target roots.","source_topology_authority":"AUTHOR_PROVISIONAL; independent source-only topology not consulted or claimed.","open_source_gap_ids":gapids,"source_seal_timing":"RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS; historical formalizer UNKNOWN; original source bytes unchanged.","procedural_status":"No independent comparison, accepted verdict, main admission, ROOT or PURIFIED claim."}
    coverage["project_owned_bundle_expansions"]={
       name:exact_definition(repo,relative,name) for relative,names in (
         ("QuantumBlockEncoding/HermiteBoundaryInjection.lean",("Full","Outside","Partial","affinePoint","selectedChild","boundarySchedule")),
         ("QuantumBlockEncoding/StoredBinaryCoordinates.lean",("Point",)),
         ("QuantumBlockEncoding/StoredHermiteGeometry.lean",("TailLevel",)),
         ("QuantumBlockEncoding/StoredHermiteChildGeometry.lean",("Refines","ChildRun","Child")),
         ("QuantumBlockEncoding/StoredHermiteKernelTable.lean",("SourceCorrect","Fields"))) for name in names}
    for r in obligations:
        body=r["lexical_header_for_audit_only"]
        r["expanded_project_owned_input_bundles"]=[name for name in coverage["project_owned_bundle_expansions"] if re.search(r"\b"+name+r"\b",body)]
        if r["name"].endswith((".child_refines",".children_refines",".children_certified")):
            r["output_conjuncts"]=["returned first equals selected child index","returned lower equals affine coordinate at first","returned upper equals affine coordinate at first+2^r","leftFull equals exact Full predicate","leftPartial equals exact Partial predicate","middleFull equals exact Full predicate","middlePartial equals exact Partial predicate"]
            if r["name"].endswith(".children_certified"):
                r["output_conjuncts"]=["For each of BOTH bits: "+x for x in r["output_conjuncts"]]+["sum of this same run's eight counters =70","this same result's separate integerAdditions=4"]
        if r["name"].endswith((".blockView_source",".assemble_source")):
            r["output_conjuncts"]=["Exact local source-kernel equality for arbitrary incoming/outgoing states in the actual returned block/table; never a SourceCorrect input clause."]
    emit(out,"author-source-coverage.json",coverage)
    graph["coverage_sha256"]=sha((out/"author-source-coverage.json").read_bytes())
    emit(out,"author-graph-views.json",graph)
    source_row={"id":SOURCE_ID,"title":"Hermite bridges, exact cuts, and stored local blocks","authors":"Historical formalizer UNKNOWN; retrospective local AUTHOR-curator hermite-substrate-author-c27r","url":"https://github.com/DakeBU/Quantum-Computing-Block-Encoding","year":2026,"status":"primary-text-checked","anchor":LESSON+" S1-S14; original UTF-8 SHA256 "+SOURCE_HASH,"scope":"Five complete fixed modules; 71 public lexical roots and four private helpers, all ambient byte scope. Exact finite-order regularity, formula transfer, exact-real comparison cut and explicitly conditional stored geometry/kernel tables.","formal_status":"AUTHOR/WIP; retrospective local source, no independent source-to-formal acceptance, pre-proof chronology, historical independence, novelty, finite-bit computation, scientific ROOT, main admission or PURIFIED claim."}
    emit(out,"author-source-row-candidate.json",{"status":WIP,"source":source_row,"immutability":"Frozen candidate source row for later data-overlay binding; do not silently edit after independent packets bind it."})
    bind,checker_hash=binding_function(repo)
    source_catalog=json.loads((repo/"website/research/sources.json").read_bytes())
    assert not any(s["id"]==SOURCE_ID for s in source_catalog["sources"]), "Source ID already exists; reconcile instead of silently replacing it."
    source_catalog["sources"].append(source_row)
    overlay=OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(source_catalog,ensure_ascii=False).encode()})
    residual="Exact classical/algebraic prerequisites only. Supplied caches and materialized field records remain conditional inputs; generation/casts/powers/index arithmetic and arbitrary integer bitcost, finite-real threshold separation/error, monomial/Bernstein bridge, complete costed raw chain and normalization, coherent quantum oracles/circuits/gate resources and scientific/PDE scaling remain outside this packet."
    bindings=[]
    for m in EXPECTED:
        mod="QuantumBlockEncoding/"+m+".lean"; own=[r for r in obligations if r["module"]==mod and not r["private"]]
        contribution={"baseline":BASE,"head":HEAD,"head_provenance":"Parent-supplied current checkout context; worker did not run Git.","classes":["reorganisation","bridge"],"node_ids":["module:QuantumBlockEncoding."+m]+["declaration:"+r["name"] for r in own]+gapids,"views":["source-construction-graph","lean-graph","compressed-quantum-spine","functor-hypergraph"],"source_graph_sha256":sha((out/"author-graph-views.json").read_bytes()),"coverage_sha256":sha((out/"author-source-coverage.json").read_bytes()),"formal_context_sha256":context_hash,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),"source_graph_authority":"AUTHOR_PROVISIONAL_NOT_INDEPENDENT","preserved_contract":"Five whole-module bytes unchanged, no new production theorem; retrospective source/metadata correspondence proposal only.","remaining_boundary":residual}
        rec={"module":mod,"source_id":SOURCE_ID,"source_statement":"Frozen retrospective local source S1-S14 in full, with exhaustive lossless paragraphs, each public/private root and explicit conditional data/cost boundaries. Independent comparison is pending.","source_anchor":LESSON+" S1-S14","lesson_path":LESSON,"declarations":[r["name"] for r in own],"obligation_map":[{"kind":"proof-edge" if r["kind"]=="theorem" else "prerequisite","source_obligation":r["id"],"declarations":[r["name"]]} for r in own],"assumption_deltas":[{"classification":"same","source":"Per-result exact premises in source S1-S14, including finite jets/degree/positive-grid invariant or explicitly conditional supplied caches and fields.","formal":"All logical binders and supplier bundles individually retained in author coverage. Whole lexical context, including private roots, is fixed in formal context.","explanation":"Author proposal only. No source-polynomial output or assembled-kernel equality is assumed as a root premise."},{"classification":"source-implicit","source":"Finite carriers, exact real arithmetic and total division; n is residual-width parameter of n+1 sample digits, d=2k+1 is a polynomial degree.","formal":"Literal carrier/index/option/sum/vector definitions and complete ambient scope retained; all stored records are supplied materialized data, not semantic callbacks.","explanation":"No arbitrary-integer bitcost, finite-real decision algorithm or whole source generation is hidden in typing."}],"graph_contribution":contribution,"formalizer":"hermite-substrate-author-c27r retrospective AUTHOR-curator; historical formalizer UNKNOWN","historical_formalizer":"UNKNOWN","residual_boundary":residual,"decoder_evidence":PREFIX+"decoder-pending/"+SHORT[m]+"-evidence.json","reviewer_evidence":PREFIX+"reviewer-pending/"+SHORT[m]+"-evidence.json","evidence_paths_status":{"decoder":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE","reviewer":"UNATTACHED_NOT_INSPECTED_NO_AUTHORED_EVIDENCE"},"status":WIP,"statement_seal":{"timing":"RETROSPECTIVE_LOCAL_AFTER_PREEXISTING_PROOFS","pre_proof_seal_claim":False},"source_proof_coverage":PREFIX+"author-source-coverage.json","graph_views":PREFIX+"author-graph-views.json","formal_context":PREFIX+"author-formal-context.json","formal_packet":PREFIX+"author-decoder-packet.json","purification":{"status":"PENDING","Exposition_Seal":"PENDING"},"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False}
        rec["binding_sha256"]=bind(overlay,rec)
        emit(out,"publication-candidate-"+SHORT[m]+".json",rec)
        bindings.append({"module":mod,"binding_sha256":rec["binding_sha256"]})
    # No independent packet is read or named as evidence by this proposal.
    emit(out,"author-binding-bridge-proposal.json",{"status":WIP,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),"formal_context_sha256":context_hash,"bindings":bindings,"procedure":"After independently frozen formal-only reconstruction, parent may attest exact target/provider/dependency input equality and bridge opaque formal context to the prospective author bindings. This author has not read the reconstruction and does not assert equality to another packet.","independent_input_binding_inspected":False,"decoder_reconstruction_inspected":False,"reviewer_result_inspected":False,"accepted":False})
    emit(out,"formal-input-seal.json",{"status":"FORMAL_ONLY_FROZEN_NOT_ACCEPTANCE","formal_context_sha256":context_hash,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),"target_bindings":[{k:v for k,v in t.items() if k in ("path","sha256","bytes")} for t in targets],"provider_index_sha256":sha(json.dumps(formal["provider_index"],sort_keys=True,ensure_ascii=False).encode()),"dependency_context":[{k:v for k,v in d.items() if k in ("path","sha256","bytes")} for d in formal["dependency_context"]],"public_roots":71,"private_helpers":4,"note":"Opaque formal-only input binding; no source identity or author graph included."})
    core_names=[p.name for p in out.iterdir() if p.name in ("author-package-build.py","author-publication-selftest.py") or p.name in ("author-formal-context.json","author-decoder-packet.json","author-source-coverage.json","author-graph-views.json","author-source-row-candidate.json","author-binding-bridge-proposal.json","formal-input-seal.json","hermite-regularity-cuts-and-stored-kernels.md") or p.name.startswith("publication-candidate-")]
    ambient_bindings=[file_record(p,p.relative_to(repo).as_posix()) for directory in ("QuantumBlockEncoding","ABEISTests") for p in sorted((repo/directory).rglob("*.lean"))]
    emit(out,"metadata-freeze.json",{"status":WIP,"head":HEAD,"head_provenance":"Parent-supplied; no Git verification executed by author worker.","original_immutable_inputs":list(sealed.values()),"source_row_candidate_sha256":sha((out/"author-source-row-candidate.json").read_bytes()),"new_artifacts":[file_record(out/p,p) for p in sorted(core_names)],"whole_ambient_binding_inputs":ambient_bindings,"checker_path":"website/scripts/check_research_publications.py","checker_sha256":checker_hash,"binding_method":"Unchanged trusted binding_digest function invoked on a read-only virtual lesson/source-catalog data overlay; validate_record and main never invoked.","all_artifacts_WIP":True,"independent_evidence_fabricated":False,"production_writes":False,"Lean_executed":False,"graph_authority":"AUTHOR_PROVISIONAL","acceptance":False,"freeze_self_hash_excluded":True})
    result=verify(repo,out,manifest=False)
    emit(out,"mechanical-selftest.json",result)
    manifest_names=sorted(core_names+list(sealed)+["metadata-freeze.json","mechanical-selftest.json"])
    artifacts=[]
    for name in manifest_names:
        item=file_record(out/name,name)
        item["planned_canonical_path"]=LESSON if name=="hermite-regularity-cuts-and-stored-kernels.md" else PREFIX+name
        artifacts.append(item)
    emit(out,"outputs-manifest.json",{"status":WIP,"artifacts":artifacts,"mechanical_selftest":result,"manifest_self_hash_excluded":True,"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,"all_output_paths_relative":True})
    final=verify(repo,out,manifest=True)
    # Report does not bind the manifest hash, so it can truthfully record the
    # completed manifest test without a self-referential checksum cycle.
    emit(out,"mechanical-selftest.json",final)
    for item in artifacts:
        if item["path"]=="mechanical-selftest.json":
            item.update(file_record(out/item["path"],item["path"]))
    emit(out,"outputs-manifest.json",{"status":WIP,"artifacts":artifacts,"mechanical_selftest":final,"manifest_self_hash_excluded":True,"independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,"all_output_paths_relative":True})
    print(json.dumps(verify(repo,out,manifest=True),ensure_ascii=False,indent=2))

def verify(repo,out,manifest=True):
    frozen=load(out,"metadata-freeze.json")
    for a in frozen["original_immutable_inputs"]+frozen["new_artifacts"]:
        raw=(out/a["path"]).read_bytes();assert sha(raw)==a["sha256"] and len(raw)==a["bytes"],a["path"]
    for a in frozen["whole_ambient_binding_inputs"]:
        raw=(repo/a["path"]).read_bytes();assert sha(raw)==a["sha256"] and len(raw)==a["bytes"],a["path"]
    formal=load(out,"author-formal-context.json")
    packet=load(out,"author-decoder-packet.json")
    context_hash=sha((out/"author-formal-context.json").read_bytes())
    assert packet["formal_context_sha256"]==context_hash
    for rec in formal["target_files"]+formal["dependency_context"]:
        data=bytes(rec["full_source_utf8_bytes"])
        assert data=="".join(rec["full_source_lines"]).encode()
        assert data==(repo/rec["path"]).read_bytes() and sha(data)==rec["sha256"]
    indexed={p["path"]:p for p in formal["provider_index"]}
    targetpaths={p["path"] for p in formal["target_files"]}
    for rec in formal["target_files"]+formal["provider_index"]:
        data=(repo/rec["path"]).read_bytes();assert sha(data)==rec["sha256"]
        assert imports(data.decode())==rec["imports"]
        for imp in rec["imports"]:
            if imp.startswith("QuantumBlockEncoding."):assert module_path(imp) in indexed or module_path(imp) in targetpaths
    allroots=formal["inventory"];pub=[r for r in allroots if not r["private"]];priv=[r for r in allroots if r["private"]]
    assert len(allroots)==75 and len(pub)==71 and len(priv)==4
    cov=load(out,"author-source-coverage.json");source=(out/"source-only.md").read_bytes()
    assert source==(out/"hermite-regularity-cuts-and-stored-kernels.md").read_bytes()
    reconstructed="".join(p["exact_text"] for p in cov["source_paragraphs"]).encode()
    assert reconstructed==source and sha(source)==SOURCE_HASH
    for p in cov["source_paragraphs"]:
        assert source[p["start_utf8_byte"]:p["end_utf8_byte"]]==p["exact_text"].encode()
        assert sha(p["exact_text"].encode())==p["sha256"]
        assert p["disposition"] in ("NODE","EXCLUDED") and (p["source_nodes"] or p["reason"])
    assert {r["name"] for r in cov["whole_module_inventory"]}=={r["name"] for r in allroots}
    assert all(r["source_paragraphs"] and r["definition_audit"] is not None for r in cov["whole_module_inventory"])
    assert all(b["classification"] in ("SOURCE","TYPING") for r in cov["whole_module_inventory"] for b in r["binder_audit"])
    graph=load(out,"author-graph-views.json");sg=graph["views"]["source-construction-graph"]
    nodeids={n["id"] for n in sg["nodes"]};assert len(nodeids)==len(sg["nodes"])
    for e in sg["AND_hyperedges"]:assert e["logic"]=="AND" and set(e["tails"]+e["heads"])<=nodeids
    for view in (graph["views"]["functor-hypergraph"],):
        for e in view["hyperedges"]:assert e["logic"]=="AND" and set(e["tails"]+e["heads"])<=nodeids
    assert all(n["status"]=="OPEN_STRONGER_CONSUMER_NOT_REFUTATION" for n in sg["nodes"] if n["kind"]=="SOURCE_GAP")
    assert len(graph["views"]["lean-graph"]["ownership_edges"])==75
    for forbidden in (SOURCE_ID,LESSON,"source-construction-graph","publication_binding_sha256"):
        assert forbidden not in (out/"author-decoder-packet.json").read_text(encoding="utf-8")
    source_row=load(out,"author-source-row-candidate.json")["source"]
    catalog=json.loads((repo/"website/research/sources.json").read_bytes());assert not any(s["id"]==SOURCE_ID for s in catalog["sources"])
    catalog["sources"].append(source_row)
    overlay=OverlayRoot(repo,{LESSON:source,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind,checker_hash=binding_function(repo);assert checker_hash==frozen["checker_sha256"]
    replay=[]
    for m in EXPECTED:
        rec=load(out,"publication-candidate-"+SHORT[m]+".json")
        assert rec["status"]==WIP and rec["main_admission"] is False
        own={r["name"] for r in pub if r["module"]==rec["module"]}
        assert set(rec["declarations"])==own
        assert {n for o in rec["obligation_map"] for n in o["declarations"]}==own
        assert bind(overlay,rec)==rec["binding_sha256"]
        replay.append({"module":rec["module"],"binding_sha256":rec["binding_sha256"]})
    if manifest:
        man=load(out,"outputs-manifest.json")
        for a in man["artifacts"]:
            data=(out/a["path"]).read_bytes();assert sha(data)==a["sha256"] and len(data)==a["bytes"]
            assert not re.search(r"(?:[A-Za-z]:[\\/]|^/|\\)",a["planned_canonical_path"])
    return {"status":"MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION","source_bytes":len(source),"lossless_paragraphs":len(cov["source_paragraphs"]),"whole_target_modules":5,"public_roots":71,"private_helpers":4,"provider_closure_modules":len(indexed),"source_AND_edges":len(sg["AND_hyperedges"]),"open_SOURCE_GAPs":len(sg["open_source_gap_ids"]),"target_import_edges":len(graph["views"]["lean-graph"]["target_import_edges"]),"ownership_edges":75,"binding_replayed_with_unchanged_checker":replay,"validate_record_called":False,"Lean_executed":False,"independent_evidence_fabricated":False,"main_admission":False,"scientific_ROOT":False,"PURIFIED":False,"manifest_verified":manifest}

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args();build(args.repo.resolve(),args.out.resolve())
