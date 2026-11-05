#!/usr/bin/env python3
"""GHL C30 AUTHOR_WIP_NOT_ADMITTED metadata; no Lean/Git or independent-result read."""
from __future__ import annotations
import argparse, ast, base64, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
WIP = "AUTHOR_WIP_NOT_ADMITTED"
TARGET = "QuantumBlockEncoding/GHL2025.lean"
TARGET_SHA = "2dba31e056b134107b34c7e41c6a5c3a2130c22a2634372d1e9ce794961a4fd4"
PREFIX = "reviews/publication/ghl-source-c30/"
LESSON = "docs/lessons/ghl-global-slot-clean-domain-and-transpose-boundary.md"
SOURCE_ID = "aspbe-local-ghl-global-slot-clean-domain"
BASE, HEAD = "f2cba045611a0d11c5995c29607569726bf1d6c5", "84c4341"
ORIGINAL = {
 "source-only.md":"c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5",
 "author-private-coverage.md":"fbbf35ed0545f73ec310ab9311854ad02b6d684293a9edb4feb38ac3311add37",
 "source-freeze.md":"963dbcd3177f8c8db56e62d13994bf2acf8c2f906491915a1ca1fcb0b7e43ac9"}
RESIDUAL = (
 "Retrospective local whole-source recovery, historical formalizer UNKNOWN. "
 "Full original paper unavailable; edited excerpt corrections not independently source-reviewed. "
 "Finite Nat basis maps and free Coeff syntax evaluated in Rat, not analytic complex unitary semantics. "
 "Global seven-slot clean-domain image injection, explicit post-SWAP candidate and restricted transpose columns "
 "retain n>=3, kappa=7, clog2(kappa)=3 and active source/row restrictions; not full-clean/full-space unitary extension. "
 "Indicator/SWAP finite permutations are not elementary decomposition or Clifford+T resource proofs. "
 "ND/Nf division, bounds, roots, arccos, half-angle and free completion entries remain unresolved. "
 "Single-arccos legacy boundary target differs from doubled-angle edited excerpt; no approved correction imported. "
 "No full seven-matrix normalized block extraction, clean-ancilla/resource closure, ghost-point PDE derivation "
 "or Hamiltonian composition. Metadata flags, strings, constants and record projections are not scientific closure.")
ROOT_RE = re.compile(r"^(?:@\[[^\n]*?\]\s+)?(?P<private>private\s+)?(?P<kind>def|theorem|lemma|structure|abbrev|inductive|opaque|class|instance)\s+(?P<name>[\w'.]+)",re.M)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def jb(obj): return (json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode()
def load_format(reference):
    """Only mechanical helpers; no C29 constants, math tables, build or verify."""
    tree=ast.parse(reference.read_text(encoding="utf-8"))
    selected={"mask_comments","imports","ShadowFile","OverlayRoot","binding_function","ambient_files","assert_current"}
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in selected]
    assert {n.name for n in nodes}==selected
    ns=globals()
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"<author-format-helpers>","exec"),ns)
def emit_raw(out,name,raw):
    path=out/name
    assert path.parent==out and not path.exists(),("EXCLUSIVE_NEW_FILE_REQUIRED",name)
    assert raw.endswith(b"\n") and b"\x00" not in raw
    lines=raw.decode().splitlines()
    chunks,block,length=[],[],0
    for line in lines:
        assert len(line.encode("utf-16-le"))//2<12000,(name,"oversize line")
        if block and length+len(line)>6500:
            chunks.append(block);block=[];length=0
        block.append(line);length+=len(line)+2
    if block: chunks.append(block)
    exe=shutil.which("codex.exe")
    assert exe,"apply_patch unavailable"
    last=None
    for i,chunk in enumerate(chunks):
        if i==0: patch="*** Begin Patch\n*** Add File: "+name+"\n"
        else: patch="*** Begin Patch\n*** Update File: "+name+"\n@@\n "+last+"\n"
        patch+="".join("+"+line+"\n" for line in chunk)
        if i: patch+="*** End of File\n"
        patch+="*** End Patch"
        argv=[exe,"--codex-run-as-apply-patch",patch]
        units=len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2+1
        assert units<30000,(name,i,"WINDOWS_ARGV_BOUND",units)
        run=subprocess.run(argv,cwd=out,capture_output=True,text=True)
        assert run.returncode==0,(name,i,run.stdout,run.stderr)
        last=chunk[-1]
    assert path.read_bytes()==raw,("APPLIED_BYTES_MISMATCH",name)
def emit(out,name,obj): emit_raw(out,name,jb(obj))
def file_record(path,relative,full=False):
    raw=path.read_bytes()
    rec={"path":relative,"sha256":sha(raw),"bytes":len(raw)}
    if full:
        rec["full_source_lines"]=raw.decode().splitlines(keepends=True)
        b=base64.b64encode(raw).decode()
        rec["full_source_utf8_base64_chunks"]=[b[i:i+6000] for i in range(0,len(b),6000)]
        assert "".join(rec["full_source_lines"]).encode()==raw
    return rec
def check_original(author):
    records=[file_record(author/n,n) for n in ORIGINAL]
    assert all(r["sha256"]==ORIGINAL[r["path"]] for r in records),"FROZEN_AUTHOR_INPUT_CHANGED"
    return records
def private_rows(author):
    profiles,rows={},[]
    for line in (author/"author-private-coverage.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "): continue
        c=[v.strip().replace(r"\|","|") for v in re.split(r"(?<!\\)\|",line)[1:-1]]
        if len(c)==10 and re.fullmatch(r"[A-Z]",c[0]):
            profiles[c[0]]={"source_regions":c[1].split("/"),"role":c[2],"semantic_slots":dict(zip(
             ["target","registers","oracles","ancillas","phases","error_success","resources"],c[3:]))}
        if len(c)==8 and re.fullmatch(r"(public|private) (structure|def|theorem|inductive)",c[1]):
            span=re.fullmatch(r"(\d+)–(\d+) / (\d+)–(\d+)",c[2]);assert span
            rows.append({"local_name":c[0],"private":c[1].startswith("private"),
             "kind":c[1].split()[1],"header_start":int(span[1]),"header_end":int(span[2]),
             "line":int(span[3]),"end_line":int(span[4]),
             "frozen_header":c[3].replace("<br>","\n"),"profile":c[6]})
    assert len(rows)==405 and len(profiles)==14
    return rows,profiles
def top_split(text,token):
    stack=[];quoted=False;i=0
    while i<len(text):
        ch=text[i]
        if quoted:
            if ch=="\\": i+=2;continue
            if ch=='"':quoted=False
        elif ch=='"':quoted=True
        elif ch in "({[":stack.append(ch)
        elif ch in ")}]":
            if stack:stack.pop()
        elif not stack and text.startswith(token,i):return text[:i],text[i+len(token):]
        i+=1
    return text,None
def header_body(block,kind):
    masked=mask_comments(block)
    if kind in ("theorem","lemma"):
        hit=re.search(r":=\s*(?:by|rfl)\b",masked)
        if hit:return block[:hit.start()].rstrip(),block[hit.start():]
    before,after=top_split(masked,":=")
    hit=re.search(r"\bwhere\b",masked)
    if hit and (after is None or hit.start()<len(before)):
        return block[:hit.start()].rstrip(),block[hit.start():]
    if after is not None:return block[:len(before)].rstrip(),block[len(before):]
    return block.rstrip(),""
def exact_roots(repo,rows):
    raw=(repo/TARGET).read_bytes();assert sha(raw)==TARGET_SHA
    lines=raw.decode().splitlines(keepends=True);assert len(lines)==8474
    roots=[]
    for r in rows:
        block="".join(lines[r["line"]-1:r["end_line"]])
        h="".join(lines[r["header_start"]-1:r["header_end"]]).rstrip()
        shown=re.sub(r"\s*:=\s*(by|rfl)\s*$","",h).strip()
        assert shown==r["frozen_header"],(r["local_name"],"FROZEN_HEADER_DISAGREEMENT")
        hit=ROOT_RE.match(mask_comments(block));assert hit and hit["name"]==r["local_name"]
        code=mask_comments(block)
        assert not re.search(r"^(?:namespace|end|import|open)\b",code,re.M),r["local_name"]
        full=dict(r,name="QuantumBlockEncoding.GHL2025."+r["local_name"],module=TARGET,
         ambient_namespace_stack=["QuantumBlockEncoding","GHL2025"],
         exact_lexical_header_lines=shown.splitlines(),source_block_lines=block.splitlines(keepends=True),
         source_block_sha256=sha(block.encode()),not_elaborated=True)
        _,body=header_body(block,r["kind"]);full["definition_body_lines"]=body.splitlines(keepends=True)
        roots.append(full)
    assert len({r["name"] for r in roots})==405
    matches=list(ROOT_RE.finditer(mask_comments(raw.decode())))
    assert len(matches)==405 and {m["name"] for m in matches}=={r["local_name"] for r in roots}
    return roots
def provider_inventory(relative,raw):
    text=raw.decode();mask=mask_comments(text);matches=list(ROOT_RE.finditer(mask))
    scopes=list(re.finditer(r"^(?:namespace\s+\S+|end(?:\s+\S+)?)\s*$",mask,re.M))
    ambient=list(re.finditer(r"^(?:namespace|end|import|open|section|variable|set_option|universe|scoped|local|attribute)\b[^\n]*",mask,re.M))
    roots=[]
    for i,m in enumerate(matches):
        stack=[]
        for event in scopes:
            if event.start()>=m.start():break
            if event[0].startswith("namespace "):stack.append(event[0].split()[1])
            elif stack:stack.pop()
        candidates=[v.start() for v in ambient if v.start()>m.start()]
        stop=min(([matches[i+1].start()] if i+1<len(matches) else [len(text)])+candidates)
        end=stop
        while end>m.start() and mask[end-1].isspace():end-=1
        block=text[m.start():end]+"\n"
        h,b=header_body(block,m["kind"])
        roots.append({"name":".".join(stack+[m["name"]]),"local_name":m["name"],"kind":m["kind"],
         "private":bool(m["private"]),"module":relative,"ambient_namespace_stack":stack,
         "line":text.count("\n",0,m.start())+1,"end_line":text.count("\n",0,end)+1,
         "exact_lexical_header_lines":h.splitlines(),"source_block_lines":block.splitlines(keepends=True),
         "source_block_sha256":sha(block.encode()),"definition_body_lines":b.splitlines(keepends=True),"not_elaborated":True})
    return roots
def paragraphs(raw):
    text=raw.decode();parts=re.findall(r"[^\n](?:.*?)(?:\n[ \t]*\n+|\Z)|\n+",text,re.S)
    assert "".join(parts)==text
    records=[];offset=0;line=1;region=None
    for i,p in enumerate(parts,1):
        h=re.match(r"## (M\d+)\.",p)
        if h:region=h[1]
        nav=p.lstrip().startswith("#") or not p.strip()
        excluded=nav or region is None
        records.append({"id":f"paragraph:{i:03d}","source_region":region,
         "source_lines":[line,line+p.rstrip("\n").count("\n")],
         "start_utf8_byte":offset,"end_utf8_byte":offset+len(p.encode()),"exact_text":p,"sha256":sha(p.encode()),
         "disposition":"EXCLUDED" if excluded else "NODE",
         "reason":"Navigation/separator/provenance, not an inference." if excluded else None,
         "source_nodes":[] if excluded else [f"source:{i:03d}"],
         "kind":"process-metadata" if region=="M8" else "boundary-and-target-context" if region=="M13" else "local-mathematical-recovery",
         "counts_as_scientific_closure":False if excluded or region in ("M8","M13") else "Only the expressly stated local scope.",
         "authority":WIP})
        offset+=len(p.encode());line+=p.count("\n")
    return records

def binder_groups(root,bundle_index):
    header="\n".join(root["exact_lexical_header_lines"])
    hit=ROOT_RE.match(header);assert hit,root["name"]
    tail=header[hit.end():].lstrip();groups=[]
    while tail and tail[0] in "({[":
        stack=[];end=None
        for i,ch in enumerate(tail):
            if ch in "({[":stack.append(ch)
            elif ch in ")}]":
                stack.pop()
                if not stack:end=i+1;break
        assert end,root["name"]
        g=tail[:end];names=g[1:-1].split(":",1)[0].split()
        typ=g[1:-1].split(":",1)[1].strip() if ":" in g else g
        carrier=bool(re.match(r"^(?:Nat|Rat|Bool|String|Fin|Matrix|[A-Z][\w.]*)(?:\s|\(|$)",typ))
        logical=any(re.match(r"^_?h",n) for n in names) or (not carrier and looks_logical(typ))
        children=bundle_refs(typ,bundle_index)
        groups.append({"exact_lexical_binder":g,"classification":"SOURCE" if logical else "TYPING",
          "source_authority":"Explicit local conditional interface, NOT authenticated original paper premise." if logical else
          "Carrier/value input; nested logical fields in recursive expansion remain SOURCE, never erased.",
          "expanded_project_bundles":children,"recursive_expansion_ids":closure(children,bundle_index),
          "not_checked_type":True})
        tail=tail[end:].lstrip()
    return groups
def looks_logical(typ):
    typ=typ.strip()
    if typ=="Prop" or re.search(r"(?:→|->)\s*Prop\s*$",typ):return False
    return bool(re.search(r"[=≤≥<>≠↔∧∨¬∀]",typ) or
     re.search(r"\b(?:PointwiseEq|Injective|Surjective|Bijective|Nodup)\b",typ) or
     re.search(r"\.(?:isUnitary|blockContainsTarget|blockCorrect|resourceBound|approximationBound)\b",typ))
def bundle_refs(typ,index):
    out=[]
    for name,item in index.items():
        local=item["local_name"]
        if re.search(r"(?<![\w'])"+re.escape(name)+r"(?![\w'])",typ) or re.search(
         r"(?<![\w'.])"+re.escape(local)+r"(?![\w'])",typ):out.append(name)
    return sorted(set(out))
def closure(names,index):
    seen=set();queue=list(names)
    while queue:
        n=queue.pop()
        if n in seen:continue
        seen.add(n)
        if n in index:
            queue+=index[n].get("nested_bundles",[])
    return sorted(seen)
def bundle_index(roots,provider_roots,hashes):
    idx={}
    for root in roots+provider_roots:
        h="\n".join(root["exact_lexical_header_lines"])
        if root["kind"]!="structure" and not (root["kind"]=="def" and re.search(r":\s*Prop\s*$",h)):continue
        body=mask_comments("".join(root["definition_body_lines"]))
        fields=[]
        matches=list(re.finditer(r"^  (?P<name>[A-Za-z_][\w']*)\s*:",body,re.M)) if root["kind"]=="structure" else []
        for i,m in enumerate(matches):
            stop=matches[i+1].start() if i+1<len(matches) else len(body)
            region=body[m.start():stop]
            region=re.split(r"^deriving\b",region,flags=re.M)[0].rstrip()
            after=region.split(":",1)[1]
            typ,_=top_split(after,":=");typ=typ.strip()
            name=m["name"]
            prop_parameter=typ=="Prop" or bool(re.search(r"(?:→|->)\s*Prop\s*$",typ))
            proof=not prop_parameter and (looks_logical(typ) or name.endswith(("Proof","Proofs","_proof","_eq")) or name in
             {"matrix_eq_eval","layoutMatches","activeEntry_eq","preparedEntry_eq","selectedContribution_eq","branchSum_eq","blockEntry_eq"})
            cls="PROPOSITION_PARAMETER_NOT_TYPING" if prop_parameter else "SOURCE" if proof else "TYPING"
            fields.append({"name":name,"exact_type_lines":typ.splitlines(),"exact_field_region_lines":region.splitlines(),
              "classification":cls,"is_logical_evidence":proof,"is_proposition_parameter":prop_parameter,
              "reason":"Arbitrary proposition/predicate data, not a proof and not mere typing." if prop_parameter else
               "Actual local law/equality/proof field; retained as supplied interface evidence, never source-target closure." if proof else
               "Data field, including Bool/Option/String/ObligationRecord; recursive child fields retained."})
        idx[root["name"]]={"name":root["name"],"local_name":root["local_name"],"kind":root["kind"],
         "provider_path":root["module"],"provider_sha256":hashes[root["module"]],
         "header_lines":root["exact_lexical_header_lines"],"code_lines":[root["line"],root["end_line"]],
         "exact_definition_region_lines":root["source_block_lines"],"field_audit":fields,
         "predicate_body_lines":root["definition_body_lines"] if not matches else [],
         "not_elaborated":True,"authority":WIP}
    for item in idx.values():
        all_refs=[]
        for f in item["field_audit"]:
            f["nested_bundles"]=bundle_refs("\n".join(f["exact_type_lines"]),idx);all_refs+=f["nested_bundles"]
        item["nested_bundles"]=sorted(set(all_refs)-{item["name"]})
    for item in idx.values():
        item["recursive_closure"]=closure(item["nested_bundles"],idx)
    # This is the critical Prop-vs-metadata boundary, checked structurally.
    cleanup=idx["QuantumBlockEncoding.GHL2025.BandedSparseAccessPostSwapCleanup"]
    assert len(cleanup["field_audit"])==11 and all(f["classification"]=="SOURCE" for f in cleanup["field_audit"])
    deriv=idx["QuantumBlockEncoding.GHL2025.DerivativeOracleContract"]
    assert next(f for f in deriv["field_audit"] if f["name"]=="bandwidth_eq")["classification"]=="SOURCE"
    oblig=idx["QuantumBlockEncoding.GHL2025.ObligationRecord"]
    assert [f["name"] for f in oblig["field_audit"]]==["description","source","proved"]
    assert all(not f["is_logical_evidence"] for f in oblig["field_audit"])
    assert len(idx["QuantumBlockEncoding.GHL2025.RobinProofObligations"]["field_audit"])==10
    assert len(idx["QuantumBlockEncoding.Resource"]["field_audit"])==5
    assert all(item["field_audit"] for item in idx.values() if item["kind"]=="structure")
    for item in idx.values():
        for f in item["field_audit"]:
            if "\n".join(f["exact_type_lines"]).strip()=="Prop":
                assert f["classification"]=="PROPOSITION_PARAMETER_NOT_TYPING"
    return idx

SUPPLEMENT = """## M14. Canonical bulk guard clarification — source-bound successor v2

This supplement clarifies the historical row-dependent candidate in M4. It does not rewrite the original frozen source or any implementation. In that section, “bulk” means exactly the canonical n-only predicate 2 ≤ r ≤ N−3, where N=2^n and subtraction is natural-number subtraction. It is not the arbitrary-parameter interval [K₁,K₂] used by the generic classifier discussion in M1/M2.

The forward candidate tests the canonical bulk predicate first, then row 0, then row 1, then row N−2, then row N−1, then its fallback. Within those regions its slot bounds are respectively 5,3,4,4,3; an unused slot returns the input row.

The reverse candidate tests row 0 first, row 1 second, then the canonical bulk predicate, then row N−2, then row N−1, then its fallback. Its outputs in that order are target, target, target+2−row, target−(N−4), target−(N−3), and target. This actual precedence matters on the total natural-number carrier, especially at small grids.

The recovered forward/reverse roundtrip is only the stated canonical-family result for n≥3, sparse index s<8, and input row i<N. No arbitrary K₁,K₂ version is claimed. These are the existing local formula and theorem guards, not added paper assumptions or a repaired Lean target.

Provenance: after the original source-only freeze, the parent supplied one explicitly authorized limited independent-phase clarification request concerning the meaning of bulk. The author received that specific feedback but read no reviewer/decoder file or other independent result. The two implementation definitions and the roundtrip header were directly rechecked before writing this supplement. The original source SHA-256 remains c774ecaf66c3d3c9586c41f7441b416ee77bfd54a3314e1d9ee66ff7151db6f5; the prospective lesson appends this visibly versioned supplement rather than pretending it was present initially.
"""
def graph_views(pars,roots,target,providers):
    pn=[{"id":p["source_nodes"][0],"kind":p["kind"],"paragraph_id":p["id"],
      "source_region":p["source_region"],"sha256":p["sha256"],"status":WIP}
      for p in pars if p["disposition"]=="NODE"]
    premises={
     "finite-syntax":"Finite entry functions; free Coeff syntax; arbitrary Rat environment; list products act right-to-left.",
     "active-domain":"n>=3 AND kappa=7 AND clog2(kappa)=3 AND finite source AND padded-clean input AND sparse slot<7.",
     "other-active":"Every compared transpose output row lies in the same padded-clean slot<7 subset; full row set is NOT supplied.",
     "bounded-splice":"Written address v<2^n; finite base index when a finite output is claimed; width compatibility when sparse reconstruction is used.",
     "canonical-row-model":"N=2^n; fixed bulk 2<=row<=N-3; forward/reverse branch precedence exactly M14; n>=3,s<8,i<N for roundtrip.",
     "supplied-preimage":"Given post=SWAP(image(source)) AND post=image(pre) AND clean(pre) AND address(pre)<2^n; early interface only."}
    nodes=pn+[{"id":"premise:"+k,"kind":"explicit-local-condition","formula":v,"status":WIP}
              for k,v in premises.items()]
    steps=[
     ("carriers",["premise:finite-syntax"],"Literal finite matrices, coefficient evaluation and zero/one/two-path sums.",["M0"]),
     ("layout-data",[],"Literal signal/workspace/normalizer/resource metadata, not a block certificate.",["M1","M2"]),
     ("global-slots",[],"Seven fixed offsets and reverse-slot table, literal total fallback preserved.",["M3"]),
     ("modular-roundtrip",["result:global-slots","premise:active-domain"],"Reverse address returns row; active offset uniqueness and same-row slot injectivity.",["M3"]),
     ("row-model",["premise:canonical-row-model"],"Historical row-local roundtrip/range only; unused-slot collision; not an active oracle.",["M4","M14"]),
     ("splice",["result:carriers","premise:bounded-splice"],"Low/high preservation, written address extraction, finite range, overwrite and reconstruction.",["M5","M11"]),
     ("clean-reconstruct",["result:splice","premise:active-domain"],"Padded-clean OD value equals extracted slot shifted by n-clog2(kappa).",["M11"]),
     ("image-injection",["result:splice","result:clean-reconstruct","result:modular-roundtrip","premise:active-domain"],"Equal full images on active clean subset imply equal finite source indices.",["M11"]),
     ("coefficient-data",[],"Literal global/row-local rational-symbol tables; not ghost-point PDE derivation.",["M6"]),
     ("rotation-skeleton",["result:coefficient-data"],"Controlled symbolic two-by-two matrix only; inverse/normalizer/trig identities unresolved.",["M7"]),
     ("function-skeleton",["result:carriers"],"Specified normalized-symbol clean branch, zero other clean rows and free completion entries.",["M9"]),
     ("swap-permutation",["result:carriers"],"Bit-mask exchange preserves difference, cancels twice and yields finite permutation matrix.",["M10"]),
     ("indicator-permutation",["result:carriers"],"Row preservation makes toggle condition invariant; in-range involution gives finite permutation.",["M10"]),
     ("post-registers",["result:splice","result:swap-permutation"],"Post-SWAP row is global address; OD block is old row, with explicit bounds.",["M10","M12"]),
     ("transpose-matrix",["result:carriers","result:splice"],"Literal transpose-style zero/one entries governed by the same image; no inverse claim.",["M5"]),
     ("conditional-witness",["premise:supplied-preimage","result:splice"],"Package supplied preimage with transpose entry and register checks; no existence supplied here.",["M12"]),
     ("candidate",["result:post-registers","result:modular-roundtrip","result:splice","premise:active-domain"],"Construct finite padded-clean reverse-slot preimage whose forward image is post.",["M12"]),
     ("candidate-active",["result:candidate","result:global-slots","premise:active-domain"],"Reverse slot remains <7, so constructed preimage is active.",["M12"]),
     ("unique-preimage",["result:candidate-active","result:image-injection","premise:active-domain","premise:other-active"],"Any active preimage of same post equals the candidate.",["M12"]),
     ("restricted-transpose",["result:unique-preimage","result:candidate","result:transpose-matrix","premise:active-domain","premise:other-active"],
       "Literal transpose column is 1 at candidate and 0 at every OTHER ACTIVE row; no outside-row statement.",["M12"]),
     ("metadata-guards",[],"Record defaults, absent images, scope/permission/citation/resource flags and labels only.",["M8","M13"])]
    edges=[]
    for key,tails,formula,regions in steps:
        nid="result:"+key
        nodes.append({"id":nid,"kind":"local-construction-or-data","formula":formula,"source_regions":regions,
         "source_paragraphs":[p["id"] for p in pars if p["disposition"]=="NODE" and p["source_region"] in regions],
         "status":WIP,"not_compiler_evidence":True})
        edges.append({"id":"construction:"+key,"logic":"AND","tails":tails,"heads":[nid],"status":WIP,
         "empty_tail_meaning":"Literal definition/accounting, NOT physical existence or unconditional resource closure." if not tails else None})
    gaps={
     "ORIGINAL-PAPER":"Original full source and its full proof topology/fidelity unavailable; external theorem transcripts not authenticated.",
     "ANGLE-CORRECTION":"Legacy single-arccos and edited doubled-angle targets differ; no independently approved source correction imported.",
     "ANALYTIC-ND-NF":"Nonzero normalizers, inverse/division, coefficient bounds, abs-square, roots, arccos/half-angle and unitary identities.",
     "FUNCTION-PRODUCER":"Actual piecewise-polynomial coherent amplitude oracle and orthogonal/system-preserving completion, not independent symbol entries.",
     "FULL-CLEAN-DOMAIN":"Address image and transpose action over all padded-clean encoded slots, including out-of-active values.",
     "FULL-SPACE-UNITARY":"Reversible completion on all columns/rows; restricted injection and transpose columns are insufficient.",
     "FULL-BLOCK-EXTRACTION":"Actual full seven-matrix product, preparation/unpreparation and all success/signal/workspace projections.",
     "PRIMITIVE-COST":"Gate-level oracle construction, controls, connectivity/depth, precision, finite-bit synthesis and preprocessing costs.",
     "PDE-GHOST":"Source-faithful ghost-point elimination, scaling and complete Robin derivative bridge.",
     "HAMILTONIAN-COMPOSITION":"One-/multi-dimensional Hamiltonian and downstream simulation contracts are metadata here, not certified consumers."}
    gapids=["SOURCE_GAP-"+k for k in gaps]
    nodes += [{"id":"SOURCE_GAP-"+k,"kind":"SOURCE_GAP","formula":v,"status":"OPEN","author_state":WIP} for k,v in gaps.items()]
    cases=[
     {"id":"modular-wrap","kind":"CASE_SPLIT","guards":["a+i<N","N<=a+i<2N"],"join":"EXHAUSTIVE_CASES_NOT_CONSTRUCTION_OR"},
     {"id":"canonical-forward","kind":"CASE_SPLIT","guards":["2<=i<=N-3","else i=0","else i=1","else i=N-2","else i=N-1","else fallback"],"precedence":"AS_WRITTEN","join":"EXHAUSTIVE_CASES_NOT_CONSTRUCTION_OR"},
     {"id":"canonical-reverse","kind":"CASE_SPLIT","guards":["row=0","else row=1","else 2<=row<=N-3","else row=N-2","else row=N-1","else fallback"],"precedence":"AS_WRITTEN","join":"EXHAUSTIVE_CASES_NOT_CONSTRUCTION_OR"},
     {"id":"slot-domain","kind":"CASE_SPLIT","guards":["active slot<7","encoded value 7 or off-active input"],"meaning":"Different theorem domains, not two sufficient oracle constructions."},
     {"id":"rotation-sector","kind":"CASE_SPLIT","guards":["indicator=1 bulk enabled","indicator=0 boundary enabled"],"meaning":"Matrix definition sectors, no unitary producer."},
     {"id":"function-workspace","kind":"CASE_SPLIT","guards":["input workspace clean and selected output","input clean and other clean output","completion row or nonclean input"],"meaning":"Literal skeleton branches."}]
    transport=[
     ("active-image-to-restricted-transpose",["result:image-injection","result:candidate-active","result:candidate","result:transpose-matrix","premise:active-domain","premise:other-active"],
      ["result:restricted-transpose"],"Injective active image plus active preimage gives its restricted transpose coordinates.",
      "Same finite basis, same literal image, same fixed post, both active restrictions; excludes outside rows."),
     ("bounded-splice-to-post-registers",["result:swap-permutation","result:splice","premise:bounded-splice"],["result:post-registers"],
      "Bounded address splice plus register exchange gives the two post-register equalities, not full oracle unitarity.",
      "Exact zero/one entries and stated slice order; no circuit hardware or resource theorem.")]
    lg={"status":WIP,"authority":"ACTUAL_IMPORT_AND_LEXICAL_OWNERSHIP_ONLY",
     "target_import_edges":[{"from":"module:QuantumBlockEncoding.GHL2025","to":"module:"+i,"kind":"actual-module-import"} for i in target["imports"]],
     "provider_import_edges":[{"from":"module:"+p["path"][:-5].replace("/","."),"to":"module:"+i,"kind":"actual-module-import"} for p in providers for i in p["imports"]],
     "ownership_edges":[{"from":"module:QuantumBlockEncoding.GHL2025","to":("private-helper:" if r["private"] else "declaration:")+r["name"],
      "kind":"private-source-owner" if r["private"] else "public-source-owner"} for r in roots],
     "elaborated_theorem_dependencies":[],"lexical_reference_signal":"Not exported as theorem dependence.","private_helpers":2}
    return {"status":WIP,"authority":"AUTHOR_LOCAL_RETROSPECTIVE_NOT_ORIGINAL_PAPER_TOPOLOGY",
     "views":{"source-construction-graph":{"nodes":nodes,"AND_hyperedges":edges,"case_splits":cases,
       "construction_OR_routes":[],"construction_OR_note":"No alternative sufficient physical route is supplied by this module. CASE_SPLITs are not construction OR.",
       "open_source_gap_ids":gapids,"gap_status":"Every unresolved node explicitly OPEN"},
      "lean-graph":lg,
      "compressed-quantum-spine":{"status":WIP,"groups":[
       {"id":"concept:finite-symbolic-carriers","expands_to":["result:carriers","result:layout-data"]},
       {"id":"concept:global-slot-register-semantics","expands_to":["result:global-slots","result:modular-roundtrip","result:splice","result:clean-reconstruct","result:image-injection"]},
       {"id":"concept:basis-permutation-providers","expands_to":["result:swap-permutation","result:indicator-permutation"]},
       {"id":"concept:restricted-inverse-on-range","expands_to":["result:candidate","result:candidate-active","result:unique-preimage","result:restricted-transpose"]},
       {"id":"concept:unresolved-amplitude-skeletons","expands_to":["result:rotation-skeleton","result:function-skeleton"]}],
       "lossless_drilldown":[PREFIX+"author-source-coverage.json",PREFIX+"author-formal-context.json"],
       "purification":"PENDING","Exposition_Seal":"PENDING","remaining_gap_ids":gapids},
      "functor-hypergraph":{"status":WIP,"certified_transport":False,"hyperedges":[
       {"id":"transport:"+key,"logic":"AND","tails":tails,"heads":heads,"formula":formula,
        "hypothesis_map":boundary,"conclusion_map":"Exactly the local finite coordinates/register relation, not full consumers.",
        "failure_boundary":RESIDUAL,"independent_review":"PENDING","categorical_certificate":False}
       for key,tails,heads,formula,boundary in transport]}}}

def build(repo,author,out,reference):
    originals=check_original(author)
    assert out.is_dir()
    source=(author/"source-only.md").read_bytes()
    supplement=SUPPLEMENT.encode()
    lesson=source+b"\n"+supplement
    rows,profiles=private_rows(author)
    roots=exact_roots(repo,rows)
    assert sum(not r["private"] for r in roots)==403
    target=file_record(repo/TARGET,TARGET,True)
    target["imports"]=imports((repo/TARGET).read_text(encoding="utf-8"))
    ambient=ambient_files(repo)
    assert len(ambient)==202,("AMBIENT_SET_CHANGED_STOP",len(ambient))
    config=[file_record(repo/p,p,True) for p in ("lean-toolchain","lake-manifest.json","lakefile.lean")]
    providers={};queue=list(target["imports"])
    while queue:
        imp=queue.pop()
        if not imp.startswith("QuantumBlockEncoding."):continue
        rel=imp.replace(".","/")+".lean"
        if rel==TARGET or rel in providers:continue
        rec=file_record(repo/rel,rel,True)
        rec["imports"]=imports((repo/rel).read_text(encoding="utf-8"))
        rec["reading_evidence"]="Author whole provider source read before source freeze; no independent provider review/build."
        providers[rel]=rec;queue+=rec["imports"]
    assert set(providers)=={"QuantumBlockEncoding/Core.lean","QuantumBlockEncoding/Resources.lean",
      "QuantumBlockEncoding/Circuit.lean","QuantumBlockEncoding/BlockEncoding.lean","QuantumBlockEncoding/CircuitSemantics.lean"}
    checker_rel="website/scripts/check_research_publications.py"
    checker=file_record(repo/checker_rel,checker_rel)
    binding,checker_sha=binding_function(repo);assert checker_sha==checker["sha256"]
    cat_rel,reg_rel="website/research/sources.json","website/research/publications.json"
    catalog_raw=(repo/cat_rel).read_bytes();registry_raw=(repo/reg_rel).read_bytes()
    reg_count=len(json.loads(registry_raw)["records"]);assert reg_count==23
    strict=ambient+[{"path":c["path"],"sha256":c["sha256"],"bytes":c["bytes"]} for c in config]+[
      checker,file_record(repo/cat_rel,cat_rel),file_record(repo/reg_rel,reg_rel)]
    if (repo/"Tests.lean").is_file():strict.append(file_record(repo/"Tests.lean","Tests.lean"))
    assert_current(repo,strict)
    proots=[r for rel in providers for r in provider_inventory(rel,(repo/rel).read_bytes())]
    hashes={TARGET:TARGET_SHA}|{p:r["sha256"] for p,r in providers.items()}
    bundles=bundle_index(roots,proots,hashes)
    masked=mask_comments((repo/TARGET).read_text(encoding="utf-8"))
    commands=[{"line":i+1,"exact_text":line} for i,line in enumerate(masked.splitlines())
      if re.match(r"^(?:import |namespace |end\b|open |section\b|variable |set_option |universe |local |scoped |attribute )",line)]
    assert [c["line"] for c in commands]==[1,2,13,14,16,8473,8474]
    scope={"module":TARGET,"commands":commands,"namespace_stack_for_all_roots":["QuantumBlockEncoding","GHL2025"],
     "private_named_roots":[r["name"] for r in roots if r["private"]],"target_global_variables":[],
     "target_local_notation":[],"explicit_instances":[],"full_source_bytes_retained":True,
     "type_authority":"Lexical raw syntax only; no checked types/elaboration or compiler success inferred."}
    neutral=[{k:r[k] for k in ("name","module","kind","private","line","end_line","ambient_namespace_stack",
       "exact_lexical_header_lines","source_block_sha256","not_elaborated")} for r in roots]
    formal={"status":WIP,"packet_kind":"FORMAL_ONLY_INPUT_NO_ACCEPTANCE","target_files":[target],"inventory":neutral,
      "inventory_count":405,"public_inventory_count":403,"private_target_helper_count":2,"explicit_structure_count":38,
      "ambient_scope":[scope],"provider_index":[providers[p] for p in sorted(providers)],
      "dependency_context":config,"whole_ambient_binding_inputs":ambient,
      "external_direct_import_index":[{"module":"Std","boundary":"Library import; no raw Std source/elaborated theorem review provided."}],
      "type_authority":"Exact raw UTF8 lines/base64, imports, lexical names/headers/ambient, NOT elaborated theorem types.",
      "fixed_read_boundary":{"target":"One whole module, all 8474 lines and every private/public/ambient byte.",
       "providers":"Exact five local modules under raw hashes; complete raw source provided.",
       "ambient":"202 production and ABEISTests Lean files bound by path/raw hash; hash binding is not reading/review credit.",
       "withheld":"No authored natural source, assumption alignment, source graph, lesson, feedback or independent result."}}
    emit(out,"author-formal-context.json",formal)
    context_sha=sha((out/"author-formal-context.json").read_bytes())
    packet={"status":WIP,"packet_kind":"FORMAL_ONLY","formal_context_path":PREFIX+"author-formal-context.json",
      "formal_context_sha256":context_sha,"opaque_context_binding_sha256":context_sha,
      "target_modules":[TARGET],"inventory_count":405,"public_count":403,"private_count":2,
      "required_work":"Read complete formal source/ambient and necessary provider definitions. Reconstruct all actual local statements, proof fields and data boundaries independently. Lexical inventory is not checked type evidence.",
      "publication_binding_state":"LATE_BRIDGE_ONLY_AFTER_INDEPENDENT_FORMAL_RECONSTRUCTION_FREEZE",
      "withheld":"Authored natural reconstruction, correspondence, graph and all independent result files."}
    emit(out,"author-decoder-packet.json",packet)
    emit(out,"formal-input-seal.json",{"status":WIP,"packet_kind":"FORMAL_ONLY_INPUT_SEAL",
      "formal_context_sha256":context_sha,"formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
      "target_bindings":[{k:target[k] for k in ("path","sha256","bytes")}],
      "provider_bindings":[{k:r[k] for k in ("path","sha256","bytes")} for r in providers.values()],
      "ambient_binding_count":202,"dependency_context":[{k:r[k] for k in ("path","sha256","bytes")} for r in config],
      "not_acceptance":True})
    emit_raw(out,"source-clarification-v2.md",supplement)
    emit_raw(out,"ghl-global-slot-clean-domain-and-transpose-boundary.md",lesson)
    pars=paragraphs(lesson)
    obligations=[]
    for i,r in enumerate(roots,1):
        prof=profiles[r["profile"]];regions=prof["source_regions"][:]
        if r["profile"]=="L":regions.append("M14")
        bs=binder_groups(r,bundles)
        refs=sorted(set(n for b in bs for n in b["recursive_expansion_ids"]))
        obligations.append({"id":f"C30-{i:03d}","status":WIP,"name":r["name"],"kind":r["kind"],
         "private":r["private"],"module":TARGET,"source_lines":[r["line"],r["end_line"]],
         "header_lines":[r["header_start"],r["header_end"]],"exact_lexical_header_lines":r["exact_lexical_header_lines"],
         "source_block_sha256":r["source_block_sha256"],"source_regions":regions,
         "source_paragraphs":[p["id"] for p in pars if p["disposition"]=="NODE" and p["source_region"] in regions],
         "semantic_slots":prof["semantic_slots"],"local_role":prof["role"],
         "scientific_closure":"METADATA_NOT_SCIENTIFIC" if r["profile"] in ("D","C","Z") else "ONLY_EXACT_LOCAL_STATEMENT",
         "binder_audit":bs,"recursive_bundle_expansions":refs,
         "definition_audit":{"kind":"theorem-not-definition" if r["kind"]=="theorem" else "literal",
          "noncomputable":False,"choice_or_quotient":False,"opaque":False,
          "exact_definition_region_lines":r["source_block_lines"] if r["kind"] in ("structure","inductive") else [],
          "full_raw_definition_available_in_formal_context":True,
          "fallback_policy":"Literal off-active defaults not source-prescribed valid-domain semantics; free completion not chosen unitary."},
         "original_paper_binder_status":"UNAUTHENTICATED; SOURCE classification here means explicit local interface only.",
         "output_logic":"Every conjunction/iff/quantified conclusion retained verbatim, not inserted as proof premises."})
    assert all(o["source_paragraphs"] for o in obligations)
    graph=graph_views(pars,roots,target,list(providers.values()))
    graph["source_version"]={"original_source_sha256":ORIGINAL["source-only.md"],
      "clarification_sha256":sha(supplement),"lesson_sha256":sha(lesson),"feedback_received":True,
      "independent_result_files_read":False}
    coverage={"status":WIP,"role":"AUTHOR_NOT_INDEPENDENT_REVIEWER","source_path":LESSON,"source_sha256":sha(lesson),
      "source_bytes":len(lesson),"source_components":[
       {"path":"$AUTHOR/final/source-only.md","sha256":ORIGINAL["source-only.md"],"unchanged":True},
       {"path":PREFIX+"source-clarification-v2.md","sha256":sha(supplement),"appended_separator_utf8":"0a"}],
      "source_paragraphs":pars,"reconstruction":"Concatenate every exact_text without added separators for exact prospective lesson bytes.",
      "whole_module_inventory":obligations,"public_target_roots":403,"private_target_helpers":2,"explicit_structure_count":38,
      "ambient_scope":[scope],"full_formal_context_sha256":context_sha,"project_owned_bundle_expansions":bundles,
      "open_source_gap_ids":graph["views"]["source-construction-graph"]["open_source_gap_ids"],
      "frozen_manual_nested_contract_audit_lines":(author/"author-private-coverage.md").read_text(encoding="utf-8").split(
       "## Binder audit semantics and complete contract expansion\n",1)[1].split("## Shared seven-slot profiles",1)[0].splitlines(),
      "remaining_boundary":RESIDUAL,"topology_authority":"AUTHOR_WIP_LOCAL_RECOVERY_NOT_ORIGINAL_PAPER"}
    emit(out,"author-source-coverage.json",coverage)
    emit(out,"author-binder-definition-audit.json",{"status":WIP,"whole_module_inventory":[
      {k:o[k] for k in ("id","name","private","binder_audit","recursive_bundle_expansions","definition_audit","exact_lexical_header_lines")}
      for o in obligations],"project_owned_bundle_expansions":bundles,
      "classification_policy":"SOURCE only explicit local logical premise/proof field; TYPING outer objects retain nested SOURCE. Prop parameters are never TYPING or proofs.",
      "original_paper_status":"UNAUTHENTICATED; no EXCESS-free paper Anchor asserted.",
      "original_trio_unchanged":True})
    graph["coverage_sha256"]=sha((out/"author-source-coverage.json").read_bytes())
    emit(out,"author-graph-views.json",graph)
    source_row={"id":SOURCE_ID,"title":"Global sparse slots, clean-domain preimages and restricted transpose columns",
      "authors":"Historical formalizer UNKNOWN; retrospective local AUTHOR-curator ghl-source-author-c30",
      "url":"https://github.com/DakeBU/Quantum-Computing-Block-Encoding","year":2026,"status":"primary-text-checked",
      "anchor":LESSON+" M0-M14; prospective lesson SHA256 "+sha(lesson),
      "scope":"Exactly one whole legacy local module;405 lexical command roots,403 public+2 private. Local source v2 clarifies canonical fixed bulk and priority, without source-paper correction.",
      "formal_status":WIP+"; original full paper unavailable; no compilation, independent acceptance, pre-proof provenance or novelty."}
    emit(out,"author-source-row-candidate.json",{"status":WIP,"source":source_row,
      "primary_text_meaning":"The authored local retrospective source, NOT the unavailable original paper.",
      "source_components":coverage["source_components"],"received_limited_feedback":True})
    catalog=json.loads(catalog_raw)
    assert not any(s["id"]==SOURCE_ID for s in catalog["sources"]),"SOURCE_ID_ALREADY_PRESENT_STOP"
    catalog["sources"].append(source_row)
    overlay=OverlayRoot(repo,{LESSON:lesson,cat_rel:json.dumps(catalog,ensure_ascii=False).encode()})
    public=[o for o in obligations if not o["private"]]
    contribution={"baseline":BASE,"head":HEAD,"head_provenance":"Parent-supplied context only, no Git executed.",
      "classes":["reorganisation","bridge"],"node_ids":["module:QuantumBlockEncoding.GHL2025"]+
       [("private-helper:" if o["private"] else "declaration:")+o["name"] for o in obligations]+
       graph["views"]["source-construction-graph"]["open_source_gap_ids"],
      "views":list(graph["views"]),"source_graph_sha256":sha((out/"author-graph-views.json").read_bytes()),
      "coverage_sha256":sha((out/"author-source-coverage.json").read_bytes()),"formal_context_sha256":context_sha,
      "preserved_contract":"Whole source/ambient/runtime unchanged; author-only recovery/metadata plus visibly versioned canonical-bulk clarification.",
      "remaining_boundary":RESIDUAL,"authority":WIP}
    candidate={"status":WIP,"module":TARGET,"source_id":SOURCE_ID,"source_anchor":LESSON+" M0-M14",
      "source_statement":"Retrospective local whole-source M0-M14; actual global-slot modular/register/preimage/restricted transpose mathematics, fixed canonical historical row model, finite basis permutations and unresolved amplitude/metadata boundaries.",
      "lesson_path":LESSON,"declarations":[o["name"] for o in public],
      "obligation_map":[{"kind":"proof-edge" if o["kind"]=="theorem" else "prerequisite","source_obligation":o["id"],"declarations":[o["name"]]} for o in public],
      "assumption_deltas":[
       {"classification":"same","source":"Explicit local restricted domains, free coefficient syntax, actual record/metadata and proof field distinctions.",
        "formal":"All 405 exact raw lexical headers and recursive law/Prop fields preserved.",
        "explanation":"No helper hypothesis is promoted to final block-encoding closure."},
       {"classification":"same","source":"M14 source-bound successor specifies fixed 2<=row<=N-3 and actual forward/reverse priority, not generic K1,K2.",
        "formal":"Original n-only definitions and roundtrip binder hn>=3,hs<8,hi<N unchanged.",
        "explanation":"Limited authorized clarification appended visibly after original natural freeze; old trio not overwritten."},
       {"classification":"unresolved","source":"Full original paper and reviewed single-/double-angle correction not available.",
        "formal":"Legacy single-arccos records, unresolved ND/Nf and full-space oracles remain actual code boundaries.",
        "explanation":"No source-fidelity acceptance, approved correction or admission can be inferred."}],
      "graph_contribution":contribution,"formalizer":"ghl-source-author-c30 retrospective AUTHOR; historical formalizer UNKNOWN",
      "historical_formalizer":"UNKNOWN","residual_boundary":RESIDUAL,
      "decoder_evidence":PREFIX+"decoder-pending/GHL2025-evidence.json",
      "reviewer_evidence":PREFIX+"reviewer-pending/GHL2025-evidence.json",
      "evidence_paths_status":"UNATTACHED_NO_AUTHORED_INDEPENDENT_EVIDENCE",
      "source_proof_coverage":PREFIX+"author-source-coverage.json","binder_definition_audit":PREFIX+"author-binder-definition-audit.json",
      "graph_views":PREFIX+"author-graph-views.json","formal_context":PREFIX+"author-formal-context.json",
      "formal_packet":PREFIX+"author-decoder-packet.json",
      "statement_seal":{"timing":"RETROSPECTIVE_LOCAL_WITH_VISIBLE_V2_CLARIFICATION","pre_proof_seal_claim":False},
      "purification":{"status":"PENDING","Exposition_Seal":"PENDING"},
      "independent_acceptance":False,"main_admission":False,"scientific_ROOT":False}
    assert_current(repo,strict)
    candidate["binding_sha256"]=binding(overlay,candidate)
    emit(out,"publication-candidate-GHL2025.json",candidate)
    emit(out,"author-binding-bridge-proposal.json",{"status":WIP,"formal_context_sha256":context_sha,
      "formal_packet_sha256":sha((out/"author-decoder-packet.json").read_bytes()),
      "bindings":[{"module":TARGET,"binding_sha256":candidate["binding_sha256"]}],
      "procedure":"After independently frozen formal reconstruction, parent may add actual-scope later bridge; no author acceptance.",
      "limited_source_phase_feedback_received":True,"feedback_scope":"Only canonical M4 bulk/branch priority, as disclosed by M14.",
      "independent_result_files_read":False,"accepted":False})
    assert_current(repo,strict);check_original(author)
    names=sorted(p.name for p in out.iterdir() if p.is_file())
    emit(out,"metadata-freeze.json",{"status":WIP,"base":BASE,"head":HEAD,"original_immutable_inputs":originals,
      "new_artifacts":[file_record(out/n,n) for n in names],"whole_ambient_binding_inputs":ambient,
      "strict_inputs":strict,"checker_path":checker_rel,"checker_sha256":checker_sha,
      "binding_recipe":{"function":"binding_digest","function_unchanged":True,"overlay_paths":[LESSON,cat_rel],
       "entrypoints_NOT_called":["validate_record","check","main"],"output_is_acceptance":False},
      "registry_observed_count":reg_count,"registry_sha256":sha(registry_raw),"source_catalog_sha256":sha(catalog_raw),
      "source_version":{"base_sha256":sha(source),"supplement_sha256":sha(supplement),"lesson_sha256":sha(lesson)},
      "feedback_disclosure":"M14 responds solely to explicitly authorized limited parent-supplied independent-phase note; no reviewer/decoder files read.",
      "format_reference":{"path":"$AUTHOR/../../cubic-source-author-c29/author-package-build.py",
       "sha256":sha(reference.read_bytes()),"use":"Only selected mechanical AST helpers; no Cubic mathematics/constants or results imported."},
      "source_inventory_counts":{"public":403,"private":2,"structures":38,"all":405},
      "emission":"Exclusive new files through bounded apply_patch; Windows argv measured below30000; partial files retained on failure.",
      "serialization_successor":"v3; prior private artifacts retained; where delimiter selected before field defaults; JSON decoded before path scan.",
      "prior_private_serialization_manifest":"$AUTHOR/final/metadata/outputs-manifest.json",
      "all_artifacts_WIP":True,"production_writes":False,"Lean_executed":False,"Git_executed":False,"acceptance":False})
    report=verify(repo,author,out,False)
    emit(out,"mechanical-selftest.json",report)
    outputs=[]
    for p in sorted(out.iterdir()):
        if not p.is_file():continue
        rec=file_record(p,p.name)
        rec["planned_canonical_path"]=LESSON if p.name=="ghl-global-slot-clean-domain-and-transpose-boundary.md" else PREFIX+p.name
        outputs.append(rec)
    emit(out,"outputs-manifest.json",{"status":WIP,"artifacts":outputs,"manifest_self_hash_excluded":True,
      "planned_prefix":PREFIX,"lesson_path":LESSON,"source_version":candidate["source_anchor"],
      "independent_acceptance":False,"main_admission":False,"scientific_ROOT":False,
      "recovery":"No existing output overwritten; preserve partial files on failure; verify is read-only."})
    print(json.dumps(verify(repo,author,out,True),ensure_ascii=False,indent=2))

def verify(repo,author,out,manifest=True):
    """Read-only integrity/replay; no publication acceptance function."""
    read=lambda n:json.loads((out/n).read_bytes())
    frozen=read("metadata-freeze.json")
    check_original(author)
    for rec in frozen["new_artifacts"]:
        raw=(out/rec["path"]).read_bytes()
        assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"],rec["path"]
    assert_current(repo,frozen["strict_inputs"])
    formal=read("author-formal-context.json");packet=read("author-decoder-packet.json")
    context_sha=sha((out/"author-formal-context.json").read_bytes())
    assert context_sha==packet["formal_context_sha256"]
    assert len(formal["inventory"])==405 and sum(not r["private"] for r in formal["inventory"])==403
    assert sum(r["kind"]=="structure" for r in formal["inventory"])==38
    assert [c["line"] for c in formal["ambient_scope"][0]["commands"]]==[1,2,13,14,16,8473,8474]
    assert len(formal["provider_index"])==5 and len(formal["whole_ambient_binding_inputs"])==202
    for rec in formal["target_files"]+formal["provider_index"]+formal["dependency_context"]:
        raw=base64.b64decode("".join(rec["full_source_utf8_base64_chunks"]))
        assert raw=="".join(rec["full_source_lines"]).encode()==(repo/rec["path"]).read_bytes()
        assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"]
    available={r["path"] for r in formal["provider_index"]}|{TARGET}
    for rec in formal["target_files"]+formal["provider_index"]:
        raw=(repo/rec["path"]).read_bytes()
        assert imports(raw.decode())==rec["imports"]
        assert all(i.replace(".","/")+".lean" in available for i in rec["imports"] if i.startswith("QuantumBlockEncoding."))
    packet_text=(out/"author-decoder-packet.json").read_text(encoding="utf-8")
    for bad in (SOURCE_ID,LESSON,"source-clarification-v2.md","source-only.md","source-construction-graph"):
        assert bad not in packet_text,("NATURAL_LEAK_IN_FORMAL_PACKET",bad)
    coverage=read("author-source-coverage.json")
    lesson=(out/"ghl-global-slot-clean-domain-and-transpose-boundary.md").read_bytes()
    supplement=(out/"source-clarification-v2.md").read_bytes()
    assert lesson==(author/"source-only.md").read_bytes()+b"\n"+supplement
    assert sha(lesson)==coverage["source_sha256"]
    pars=coverage["source_paragraphs"]
    assert "".join(p["exact_text"] for p in pars).encode()==lesson
    for p in pars:
        assert lesson[p["start_utf8_byte"]:p["end_utf8_byte"]]==p["exact_text"].encode()
        assert sha(p["exact_text"].encode())==p["sha256"]
        assert p["disposition"] in ("NODE","EXCLUDED") and (p["source_nodes"] or p["reason"])
    obligations=coverage["whole_module_inventory"]
    assert {o["name"] for o in obligations}=={r["name"] for r in formal["inventory"]}
    assert all(o["source_paragraphs"] for o in obligations)
    idx=coverage["project_owned_bundle_expansions"]
    cleanup=idx["QuantumBlockEncoding.GHL2025.BandedSparseAccessPostSwapCleanup"]
    assert len(cleanup["field_audit"])==11 and all(f["classification"]=="SOURCE" for f in cleanup["field_audit"])
    for bundle in idx.values():
        assert not any(re.match(r"^(namespace|end|import|open)\b",line) for line in bundle["exact_definition_region_lines"])
        for f in bundle["field_audit"]:
            typ="\n".join(f["exact_type_lines"])
            assert not any(re.match(r"^(namespace|end|import|open)\b",line) for line in f["exact_field_region_lines"])
            if typ.strip()=="Prop":assert f["classification"]=="PROPOSITION_PARAMETER_NOT_TYPING"
    graph=read("author-graph-views.json");sg=graph["views"]["source-construction-graph"]
    ids={n["id"] for n in sg["nodes"]};assert len(ids)==len(sg["nodes"])
    for edge in sg["AND_hyperedges"]+graph["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"]=="AND" and set(edge["tails"]+edge["heads"])<=ids
    assert all(n["status"]=="OPEN" for n in sg["nodes"] if n["kind"]=="SOURCE_GAP")
    assert all(c["kind"]=="CASE_SPLIT" for c in sg["case_splits"])
    assert sg["construction_OR_routes"]==[]
    assert len(graph["views"]["lean-graph"]["ownership_edges"])==405
    row=read("author-source-row-candidate.json")["source"]
    catalog=json.loads((repo/"website/research/sources.json").read_bytes())
    existing=[s for s in catalog["sources"] if s["id"]==SOURCE_ID]
    assert not existing or existing==[row],"EXISTING_SOURCE_ROW_DIFFERS"
    if not existing:catalog["sources"].append(row)
    overlay=OverlayRoot(repo,{LESSON:lesson,"website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    binding,checker_sha=binding_function(repo);assert checker_sha==frozen["checker_sha256"]
    candidate=read("publication-candidate-GHL2025.json")
    assert candidate["status"]==WIP and not candidate["main_admission"] and not candidate["independent_acceptance"]
    public={r["name"] for r in formal["inventory"] if not r["private"]}
    assert len(candidate["declarations"])==403 and set(candidate["declarations"])==public
    assert {n for edge in candidate["obligation_map"] for n in edge["declarations"]}==public
    assert binding(overlay,candidate)==candidate["binding_sha256"]
    if manifest:
        man=read("outputs-manifest.json")
        for rec in man["artifacts"]:
            raw=(out/rec["path"]).read_bytes()
            assert sha(raw)==rec["sha256"] and len(raw)==rec["bytes"],rec["path"]
            assert not re.search(r"(?:[A-Za-z]:[\\/]|^/|\\)",rec["planned_canonical_path"])
        assert man["status"]==WIP and not man["main_admission"]
    # Only new text artifacts: no machine prefix in public payloads.
    for path in out.iterdir():
        if path.is_file() and path.suffix in (".json",".md",".py"):
            obj=json.loads(path.read_bytes()) if path.suffix==".json" else path.read_text(encoding="utf-8")
            def leaf_strings(value):
                if isinstance(value,str):yield value
                elif isinstance(value,dict):
                    for k,v in value.items():
                        yield str(k)
                        yield from leaf_strings(v)
                elif isinstance(value,list):
                    for v in value:yield from leaf_strings(v)
            assert not any(re.search(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]",s) for s in leaf_strings(obj)),("MACHINE_PREFIX",path.name)
    return {"status":WIP,"mechanical_integrity":"PASS_NOT_ADMISSION","read_only_verify":True,
      "whole_target_modules":1,"public_roots":403,"private_named_helpers":2,"structures":38,
      "schema_extraction":"where before field defaults; all structure fields retained",
      "project_bundle_count":len(idx),"logical_proof_fields":sum(f["is_logical_evidence"] for b in idx.values() for f in b["field_audit"]),
      "proposition_parameter_fields":sum(f["is_proposition_parameter"] for b in idx.values() for f in b["field_audit"]),
      "lossless_source_paragraphs":len(pars),"source_AND_edges":len(sg["AND_hyperedges"]),
      "case_splits_not_construction_OR":len(sg["case_splits"]),"open_SOURCE_GAPs":len(sg["open_source_gap_ids"]),
      "provider_closure_modules":5,"whole_ambient_binding_inputs":202,"registry_observed_count":frozen["registry_observed_count"],
      "binding_replayed_with_unchanged_checker":candidate["binding_sha256"],"lesson_sha256":sha(lesson),
      "canonical_bulk_supplement_sha256":sha(supplement),"source_version_feedback_affected":True,
      "validate_record_called":False,"check_or_main_called":False,"Lean_executed":False,"Git_executed":False,
      "independent_result_files_read":False,"independent_evidence_fabricated":False,
      "main_admission":False,"scientific_ROOT":False,"PURIFIED":False,"manifest_verified":manifest}
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,required=True);p.add_argument("--author",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--reference",type=Path,required=True)
    p.add_argument("--verify",action="store_true");a=p.parse_args()
    load_format(a.reference)
    if a.verify:print(json.dumps(verify(a.repo.resolve(),a.author.resolve(),a.out.resolve()),ensure_ascii=False,indent=2))
    else:build(a.repo.resolve(),a.author.resolve(),a.out.resolve(),a.reference.resolve())
