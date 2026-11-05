"""Read-only C46 C29 prospective baseline. CLI roots only; no gates, Git or Lean."""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_bytes())
def canon(x): return json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def pin(p, logical): return dict(path=logical, sha256=sha(p.read_bytes()), bytes=p.stat().st_size)
ap=argparse.ArgumentParser()
ap.add_argument("--project-root", type=Path, required=True)
ap.add_argument("--prospective-root", type=Path, required=True)
a=ap.parse_args(); project=a.project_root.resolve(); prospect=a.prospective_root.resolve(); overlay=prospect/"overlay"
seal=read(prospect/"seal.json")
if sha((prospect/"seal.json").read_bytes())!="888047e7d9aa187392b5af6f99064db7e53b0e723872775529713ce42ce8e477": raise ValueError("freeze seal drift")
payload=[]
for f in seal["payload"]:
    p=prospect/f["path"]
    if sha(p.read_bytes())!=f["sha256"] or p.stat().st_size!=f["bytes"]: raise ValueError("freeze payload drift")
    payload.append(pin(p, "$PROSPECTIVE/"+f["path"]))
manifest=read(prospect/"overlay-manifest.json")["files"]; overlaypins=[]
for f in manifest:
    p=overlay/f["path"]
    if sha(p.read_bytes())!=f["sha256"] or p.stat().st_size!=f["bytes"]: raise ValueError("overlay file drift")
    overlaypins.append(pin(p,"$OVERLAY/"+f["path"]))
actual_overlay={p.relative_to(overlay).as_posix() for p in overlay.rglob("*") if p.is_file()}
if actual_overlay!={f["path"] for f in manifest}: raise ValueError("overlay membership differs from manifest")
record=read(prospect/"candidate-record-CubicStatePreparation.json")
oldpath=project/"reviews/publication/cubic-source-c29/metadata-v2/publication-candidate-CubicStatePreparation.json"
if sha(oldpath.read_bytes())!="f34ff916d90461dfa32e82078c23fa453f617759f85aa3dc35a957b805119daa": raise ValueError("original C29 record drift")
old=read(oldpath)
keys=("module","source_id","source_statement","source_anchor","lesson_path","declarations","obligation_map","assumption_deltas","graph_contribution","formalizer","residual_boundary")
metadata12=keys+("historical_formalizer",)
metadata_differences=[k for k in metadata12 if canon(old.get(k))!=canon(record.get(k))]
oldrowpath=oldpath.parent/"author-source-row-candidate.json"; oldrow=read(oldrowpath)
sources=read(overlay/"website/research/sources.json"); baseline_sources=read(project/"website/research/sources.json")
rows=sources["sources"]; baseline=baseline_sources["sources"]
row=[r for r in rows if r["id"]==record["source_id"]]
if len(row)!=1: raise ValueError("nonunique C29 source row")
# Frozen old row is wrapped or literal; preserve exact semantics rather than assume schema.
oldrow_value=oldrow.get("source_row", oldrow.get("source", oldrow)) if isinstance(oldrow,dict) else oldrow
lesson=overlay/record["lesson_path"]
lessonhash=sha(lesson.read_bytes())
ambient_dirs=("QuantumBlockEncoding","ABEISTests")
ambient_overlay=sorted(p for d in ambient_dirs for p in (overlay/d).rglob("*.lean"))
ambient_current=sorted(p for d in ambient_dirs for p in (project/d).rglob("*.lean"))
ambient_names_overlay={p.relative_to(overlay).as_posix() for p in ambient_overlay}
ambient_names_current={p.relative_to(project).as_posix() for p in ambient_current}
ambient_changes=[]
for name in sorted(ambient_names_overlay & ambient_names_current):
    x=overlay/name; y=project/name
    if x.read_bytes()!=y.read_bytes():
        ambient_changes.append(dict(path=name,currentSHA256=sha(y.read_bytes()),overlaySHA256=sha(x.read_bytes()),currentBytes=y.stat().st_size,overlayBytes=x.stat().st_size))
deltas=[]
for name in ("CubicStatePreparation","CubicAmplitudePrimitive"):
    rel="QuantumBlockEncoding/"+name+".lean"
    original=(project/rel).read_bytes(); candidate=(overlay/rel).read_bytes()
    lines=original.split(b"\n"); edits=[]; offset=0; patched=[]
    for i,line in enumerate(lines,1):
        if b"native_decide" in line:
            if line.count(b"native_decide")!=1: raise ValueError("multiple native tokens")
            replacement=b"exact Rat.sub_self" if name=="CubicStatePreparation" and i==2465 else b"decide +kernel"
            edits.append(dict(line=i,byteOffset=offset+line.index(b"native_decide"),old="native_decide",replacement=replacement.decode()))
            line=line.replace(b"native_decide",replacement)
        patched.append(line); offset+=len(lines[i-1])+1
    reconstructed=b"\n".join(patched)
    deltas.append(dict(module=rel,edits=edits,editCount=len(edits),allOtherBytesIdentical=reconstructed==candidate,
                       currentSHA256=sha(original),candidateSHA256=sha(candidate),sourceSignaturesDefinitionsResourcesUnchanged=reconstructed==candidate))
checker=project/"website/scripts/check_research_publications.py"
if sha(checker.read_bytes())!="f8f6d7232376b5bc19a480b7e0ef549a5fafa8d66017e07482f7e6999962f8ad": raise ValueError("original checker drift")
spec=importlib.util.spec_from_file_location("c46_original_publication_checker_readonly",checker)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
computed=module.binding_digest(overlay,record) # Only original pure formula; never check()/Git.
providers=[]
for n in ("Core","Resources","Circuit","BlockEncoding","BlockEncodingClassics"):
    rel="QuantumBlockEncoding/"+n+".lean"; q=project/rel; p=overlay/rel
    providers.append(dict(path=rel,sha256=sha(p.read_bytes()),sameCurrentBytes=p.read_bytes()==q.read_bytes()))
result=dict(schema="C46_C29_ORIGINAL_REVIEWER_BASELINE_V1",freezePayloadPins=payload,overlayPins=overlaypins,
            overlayManifestCount=len(manifest),ambientCount=len(ambient_overlay),
            ambientMembershipUnchanged=ambient_names_overlay==ambient_names_current,ambientOpaqueByteChanges=ambient_changes,
            recordPin=pin(prospect/"candidate-record-CubicStatePreparation.json","$PROSPECTIVE/candidate-record-CubicStatePreparation.json"),
            oldRecordPin=pin(oldpath,"$PROJECT/reviews/publication/cubic-source-c29/metadata-v2/publication-candidate-CubicStatePreparation.json"),
            oldSourceRowPin=pin(oldrowpath,"$PROJECT/reviews/publication/cubic-source-c29/metadata-v2/author-source-row-candidate.json"),
            metadata12Compared=list(metadata12),metadata12Differences=metadata_differences,
            oldSourceCount=len(baseline),newSourceCount=len(rows),
            oldSourceRowsUnchanged=rows[:len(baseline)]==baseline,
            sourceRowsDeltaExactlyOne=len(rows)==len(baseline)+1 and row[0]==rows[-1],
            C29SourceRow=row[0],C29SourceRowEqualsOldCandidate=row[0]==oldrow_value,
            lessonPin=pin(lesson,"$OVERLAY/"+record["lesson_path"]),
            lessonEqualsOriginalNaturalSource=lessonhash=="e3e594b40b44bd474a4c98cf61c052b5f2a42ec8082de8d6164bd4f1e1df3dc7",
            exactProofDeltas=deltas,providers=providers,
            checkerPin=pin(checker,"$PROJECT/website/scripts/check_research_publications.py"),
            originalPureCheckerBindingComputed=computed,prospectiveRecordBinding=record["binding_sha256"],
            bindingMatches=computed==record["binding_sha256"],publicDeclarations=len(record["declarations"]),
            originalHistoricalFormalizer=record.get("historical_formalizer"),
            pendingInstalledGate=record.get("proof_context_successor"),
            sourceStatement=record["source_statement"],residualBoundary=record["residual_boundary"],
            assumptionDeltas=record["assumption_deltas"],sourceAgreement=None,nativeAccepted=False,scientific_ROOT=False)
print(json.dumps(result,ensure_ascii=False,separators=(",",":")))

