"""Bounded C46 formal-input delta; never reads natural/reviewer/context catalogs.

All artifact files are emitted as an apply_patch payload, not written by this
program. Original decoder packets/artifacts are hashed, not semantically reread.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time
import unittest

IDENTITY='/root/primitive_compiler_formal_decoder_c31'
CONTROL='d5e11bb5c6bc01f7f152a76d354a7b65637ca4fe913d66e877cd7785749d5547'
MANIFEST='d466e117dc401f7de4037e8c1da93d8a2965787c430e3a59df1820b438683e56'
PRIOR_SEAL='5bac711b87c61f30b20c3b66d43ee957bcdc9721ffd20dfdb247f3b016f01bc1'
PRIOR_MANIFEST='732036b718c9b02495a71add5cd818c8509abbaaab3bd67cf5dba999ff0fb834'
SOURCE_SEAL='0fd3e599c0532c6e308dbb87b26b420f939886d9d39de89c419692946f40cd68'
CUBIC_RECONSTRUCTION='457b369bcb1c98933f144551eb1ee82fcfb20d032437aa5b2536120a4d3c4309'
ASSESSMENT_PATH='reviews/publication/paired-kernel-c46/decoder-c31-current/delta-assessment.json'
BASE_PATH='reviews/publication/paired-kernel-c46/decoder-c31-current/'
CHANGED={
 'QuantumBlockEncoding/CubicStatePreparation.lean':('d125f8c239bca1c15e6e4fa6e788df6dd8984394630cb2dcc9be8946c4cbcb55','6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44'),
 'QuantumBlockEncoding/CubicAmplitudePrimitive.lean':('48c9a4a1c47c925c93493eede21eb7b492d23d2cb7dadf254782e4485c349cb3','952e2b359796ef695a1b1c1a376d40a80affbc679f503f94227ea0c775a6cd48')}
NO_ACCEPT=dict(sourceAgreement=None,axiomPolicyPass=None,publicationBinding=None,nativeAccepted=False,scientificAcceptance=False,trustClosure=False)


def require(x,msg):
    if not x:raise ValueError(msg)
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def unique(pairs):
    obj={}
    for k,v in pairs:
        require(k not in obj,'duplicate JSON key');obj[k]=v
    return obj
def parse(x):return json.loads(x,object_pairs_hook=unique)
def read(p):return parse(p.read_bytes())
def safe_path(value):
    p=Path(value);require(not p.is_absolute() and '..' not in p.parts and '\\' not in value,'unsafe logical path');return p
def formal_path(value):
    return ((value.endswith('.lean') and (value.startswith(('QuantumBlockEncoding/','ABEISTests/')) or value in ('QuantumBlockEncoding.lean','lakefile.lean')))
            or value in ('lean-toolchain','lake-manifest.json'))


def masked(raw):
    """Same nested-comment recipe as my pinned C38 replay; strings remain data."""
    out=bytearray(raw);i=depth=0;line=string=escape=False
    while i<len(raw):
        pair=raw[i:i+2]
        if line:
            if raw[i] in (10,13):line=False
            else:out[i]=32
            i+=1;continue
        if depth:
            if pair==b'/-':out[i:i+2]=b'  ';depth+=1;i+=2
            elif pair==b'-/':out[i:i+2]=b'  ';depth-=1;i+=2
            else:
                if raw[i] not in (10,13):out[i]=32
                i+=1
            continue
        if string:
            if escape:escape=False
            elif raw[i]==92:escape=True
            elif raw[i]==34:string=False
            i+=1;continue
        if pair==b'--':out[i:i+2]=b'  ';line=True;i+=2
        elif pair==b'/-':out[i:i+2]=b'  ';depth=1;i+=2
        else:
            if raw[i]==34:string=True
            i+=1
    require(not depth and not string,'unterminated formal lexical region');return bytes(out)


def imports(raw):
    names=[]
    for line in masked(raw).decode('utf-8-sig').splitlines():
        s=line.strip()
        if not s or s in ('module','prelude'):continue
        m=re.fullmatch(r'(?:public\s+)?import\s+([A-Za-z0-9_.]+(?:\s+[A-Za-z0-9_.]+)*)',s)
        if m:names.extend(m[1].split());continue
        require(not re.match(r'^(?:public\s+)?import\b',s),'unsupported import syntax')
        break
    require(len(names)==len(set(names)),'duplicate import');return names


def graph(source):
    local={};external={}
    for path,raw in source.items():
        if not path.endswith('.lean'):continue
        local[path]=[];external[path]=[]
        for name in imports(raw):
            target=name.replace('.','/')+'.lean'
            if target in source:local[path].append(target)
            else:
                require(not (name=='QuantumBlockEncoding' or name.startswith(('QuantumBlockEncoding.','ABEISTests.'))),'missing project import: '+name)
                external[path].append(name)
    return local,external


def closure(local,start):
    require(start in local,'missing module');seen=set();pending=[start]
    while pending:
        item=pending.pop()
        if item in seen:continue
        seen.add(item);pending.extend(local[item])
    return sorted(seen)


def proof_delta(old,new,special=None):
    matches=list(re.finditer(rb'\bnative_decide\b',masked(old)));result=old;sites=[]
    for m in reversed(matches):
        line=old[:m.start()].count(b'\n')+1
        token=b'exact Rat.sub_self' if line==special else b'decide +kernel'
        result=result[:m.start()]+token+result[m.end():]
        sites.append(dict(line=line,start=m.start(),end=m.end(),oldToken='native_decide',newToken=token.decode()))
    require(result==new,'not exact proof-token-only delta');return list(reversed(sites))


def verify_seal(directory,manifest_name,seal_name,pin,manifest_pin):
    require(sha((directory/seal_name).read_bytes())==pin,'prior own seal')
    require(sha((directory/manifest_name).read_bytes())==manifest_pin,'prior own manifest')
    m=read(directory/manifest_name);s=read(directory/seal_name)
    require(s['manifestSHA256']==manifest_pin,'prior seal binding')
    for name,p in m['files'].items():require(sha((directory/safe_path(name)).read_bytes())==p,'prior sealed file: '+name)
    return m,s


def assess(workspace,project):
    work=workspace/'hermite-export-work'
    control_path=work/'paired-kernel-c46-formal-only-control/control.json'
    require(sha(control_path.read_bytes())==CONTROL,'control pin')
    c=read(control_path);require(c['snapshot']=='$WORK/paired-kernel-c46-prospective/overlay' and c['snapshot_manifest']=='$WORK/paired-kernel-c46-prospective/overlay-manifest.json','control snapshot paths')
    require(c['snapshot_manifest_sha256']==MANIFEST,'control manifest pin')
    manifest_path=work/'paired-kernel-c46-prospective/overlay-manifest.json';require(sha(manifest_path.read_bytes())==MANIFEST,'overlay manifest bytes')
    all_rows=read(manifest_path)['files'];require(len(all_rows)==len({r['path'] for r in all_rows}),'manifest duplicates')
    rows=[r for r in all_rows if formal_path(r['path'])]
    overlay=work/'paired-kernel-c46-prospective/overlay';current={};old={};pins={};differences=[]
    for row in rows:
        name=row['path'];path=safe_path(name);raw=(overlay/path).read_bytes();before=(project/path).read_bytes()
        require(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'formal snapshot file pin')
        current[name]=raw;old[name]=before;pins[name]=dict(originalSHA256=sha(before),overlaySHA256=sha(raw),bytes=len(raw))
        if before!=raw:differences.append(name)
    require(set(differences)==set(CHANGED),'unexpected changed formal/config file')
    require(len(rows)==206 and sum(n.startswith('QuantumBlockEncoding/') for n in current)==142 and sum(n.startswith('ABEISTests/') for n in current)==60,'formal vector size')
    proof={}
    for name,(original,candidate) in CHANGED.items():
        require(sha(old[name])==original and sha(current[name])==candidate,'pair exact raw pins')
        proof[name]=proof_delta(old[name],current[name],2465 if name.endswith('CubicStatePreparation.lean') else None)
    require(sorted(map(len,proof.values()))==[3,9],'proof-token counts')
    original_graph,original_external=graph(old);final_graph,final_external=graph(current)
    require(original_graph==final_graph and original_external==final_external,'formal import header delta')
    prior=workspace/'.c29-c31-joint-actual-decoder-c38'
    prior_manifest,prior_seal=verify_seal(prior,'final-bindings-v2.json','final-seal-v2.json',PRIOR_SEAL,PRIOR_MANIFEST)
    prior_delta=read(prior/'source-delta.json');summary=read(prior/'summary.json');technical=read(prior/'technical-chain.json')
    for name,wanted in prior_delta['originalProjectInputs'].items():require(sha(old[name])==wanted,'prior original31 input drift')
    for name,wanted in prior_delta['shadowProjectInputs'].items():require(sha(current[name])==wanted,'prior joint31 candidate input drift')
    require(len(prior_delta['shadowProjectInputs'])==31,'prior source/config vector size')
    for target in technical['cohort']['targets']:
        path=target['module'].replace('.','/')+'.lean'
        require(target['sourceSHA256Before']==target['sourceSHA256After']==target['copiedSourceSHA256']==sha(current[path]),'old actual cohort/source does not match overlay')
    # Original C31 separate-candidate inputs have only CSP different from final pair.
    prior31=workspace/'.c31-kernel-v3-actual-decoder-addendum-v1'
    own_kernel_m,own_kernel_s=verify_seal(prior31,'bindings.json','seal.json',
        'b8473c295a0e9552589a175cbc018353e5bb664df2fa016a5d2fe6f6002ccf5f','73761459f5dd7f59b70beaf7c92758d04f6b97cbda39be7373c4eedd17812901')
    require(sha((prior31/'Cubic-reconstruction.md').read_bytes())==CUBIC_RECONSTRUCTION,'own complete25-root reconstruction')
    packet=project/'reviews/publication/primitive-compiler-c31/decoder-c31/source-formal-seal.json'
    require(sha(packet.read_bytes())==SOURCE_SEAL,'original source-only seal')
    kernel_profile=read(workspace/'.c31-kernel-proof-v1-staging/profile.json')
    require(sha((workspace/'.c31-kernel-proof-v1-staging/profile.json').read_bytes())=='e3e46b04819500acc83eaadfd34ad5185ea79b3d778f26e7b5624d84377850e7','prior kernel profile')
    c31_different=[name for name,value in kernel_profile['projectInputs'].items() if value!=sha(current[name])]
    require(c31_different==['QuantumBlockEncoding/CubicStatePreparation.lean'],'old separate-candidate context delta')
    require(summary['ownedRows']==968 and summary['observedAxiomUnion']==['Classical.choice','Quot.sound','propext'],'prior actual formal observation boundary')
    list37=c['old37'];require(len(list37)==37 and len({x['module'] for x in list37})==37,'old37 identity partition')
    lineage={};closures={};expected={r['module']:r['import_closure'] for r in c['import_impact']}
    for row in list37:
        module=row['module'];cl=closure(final_graph,module)
        require(not set(cl)&set(CHANGED),'changed module in original record closure: '+module)
        require(cl==closure(original_graph,module),'old/final closure drift')
        require(all(old[n]==current[n] for n in cl),'closure formal byte delta')
        raw=(project/safe_path(row['old_decoder_path'])).read_bytes();require(sha(raw)==row['old_decoder_sha256'],'original decoder evidence pin')
        dec=parse(raw);require(dec['role']=='decoder' and dec['identity'] and dec['run_id'] and dec['source_blind'] is True and dec['reconstruction'],'original decoder lineage missing')
        require(dec['binding_sha256']==row['original_binding'],'original opaque binding mismatch')
        for label in ('packet','artifact'):
            path=row['old_'+label+'_path'];pin=row['old_'+label+'_sha256']
            require(dec[label+'_path']==path and dec[label+'_sha256']==pin,'original packet/artifact evidence link')
            require(sha((project/safe_path(path)).read_bytes())==pin,'original packet/artifact bytes')
        require(cl==expected[module],'computed closure differs from control cross-check')
        closures[module]=dict(importClosure=cl,formalClosureSHA256={n:sha(current[n]) for n in cl},
                              externalImports=sorted({i for n in cl for i in final_external[n]}),
                              excludesBothChangedModules=True,allClosureBytesUnchanged=True,computedBeforeComparingControl=True)
        lineage[module]=dict(control=row,originalEvidence=dec,evidenceSHA256=sha(raw),packetAndArtifactRehashedWithoutSemanticReread=True)
    # Rehash actual opened formal inputs at the end; no docs/catalog bytes opened.
    for name in current:
        require((overlay/name).read_bytes()==current[name] and (project/name).read_bytes()==old[name],'formal before/after drift')
    require(sha(control_path.read_bytes())==CONTROL and sha(manifest_path.read_bytes())==MANIFEST,'late control drift')
    return dict(control=c,pins=pins,proof=proof,closures=closures,lineage=lineage,
                graph=final_graph,external=final_external,priorSummary=summary,priorTechnical=technical,
                priorManifest=prior_manifest,priorKernelManifest=own_kernel_m,
                prior31Inputs=prior_delta['shadowProjectInputs'],separate31ChangedInput=c31_different,
                ignoredNonformalManifestEntries=len(all_rows)-len(rows))


def artifacts(result,run_id):
    shared=dict(schema='C46_C31_CURRENT_FORMAL_DELTA_ASSESSMENT_V1',role='decoder',identity=IDENTITY,run_id=run_id,
        direction='formal-proof-epoch-delta-and-no-import-carryforward',controlSHA256=CONTROL,overlayManifestSHA256=MANIFEST,
        formalInputVector=result['pins'],formalCounts=dict(productionModules=142,testModules=60,rootAggregator=1,lakefile=1,otherConfigs=2),
        changedFormalModules=list(CHANGED),unchangedFormalConfigCount=204,proofOnlySites=result['proof'],
        allOtherSourceBytesUnchangedIncludingStatementsBindersDataDefinitions=True,all31PriorJointSourceConfigPinsMatch=True,
        formalBaselineKind='Exact current local read-only working-tree bytes, not Git committed blob bytes or an attested CI checkout',
        rootAggregatorRawSHA256=result['pins']['QuantumBlockEncoding.lean']['overlaySHA256'],
        rootAggregatorCommittedLinuxRawIdentityClaim=False,
        oldSeparateC31CandidateContextDiffersOnlyAt=result['separate31ChangedInput'],
        independentlyEnumeratedNoImportCarryforwardCount=len(result['closures']),noImportCarryforward=result['closures'],
        completeGraph=result['graph'],externalImports=result['external'],
        originalSourceOnlySeal=SOURCE_SEAL,ownWholeCubicReconstructionSHA256=CUBIC_RECONSTRUCTION,
        priorOwnJointOuterSeal=PRIOR_SEAL,priorOwnJointManifest=PRIOR_MANIFEST,
        retainedActualCohort=result['priorTechnical']['cohort'],retainedActualSummary=result['priorSummary'],
        observedAxioms=['Classical.choice','Quot.sound','propext'],axiomFree=False,
        currentInstalledBuild='PENDING_NOT_RUN_HERE',oldCohortIsNotNewInstalledBuild=True,
        newLocalLeanInvocations=0,newNativeProbes=0,freshWholeModuleSemanticRereads=0,
        claimScope='My own complete Cubic reconstruction and reviewed actual evidence plus current exact formal-input delta;37 other records preserve their original identities and restrictions, not37 newly authored decodes',
        excludedReads=['prospective/context.json','prospective/candidate-record*.json','overlay sources.json','overlay docs','natural/author/reviewer packages','registry'],
        manifestNonformalEntriesNotOpened=result['ignoredNonformalManifestEntries'],
        controlDiffWasNotUsedForProofRecognition=True,
        lateOpaqueBindingScope='Supplied labels only; no author metadata formula, source correspondence or semantic equivalence inferred from labels',
        importBoundary='Explicit source import graph, not theorem dependency, load trace, metaprogram noninterference, or a clean-transitive binary build',
        trustBoundary='Prior24 inherited project providers and external libraries remain;96CSP value omissions and no ordinary C31 value printing retained;not a new allTCB/body policy',
        instrumentationAuthorshipDisclosed=True,freshSourceBlindRun=False,**NO_ACCEPT)
    data={'delta-assessment.json':shared,'lineage.json':result['lineage']}
    artifact_sha=sha((json.dumps(shared,ensure_ascii=False,indent=2)+'\n').encode())
    for module,entry in result['lineage'].items():
        old=entry['originalEvidence'];row=entry['control'];name=Path(row['new_decoder_logical_path']).name
        data['final-decoders/'+name]=dict(schema='C46_RETAINED_DECODER_CURRENT_INPUT_DELTA_V1',role='decoder',identity=IDENTITY,run_id=run_id,
            module=module,binding_sha256=row['prospective_binding'],intended_repository_evidence_path=row['new_decoder_logical_path'],
            packet_path=row['old_packet_path'],packet_sha256=row['old_packet_sha256'],
            packet_path_scope='Retained original decoder input packet; rehashed, not a fresh whole semantic read by current delta checker',
            artifact_path=ASSESSMENT_PATH,artifact_sha256=artifact_sha,
            source_blind=True,source_blind_scope='Only the retained original mathematical reconstruction under its genuine original identity; this current wrapper is an input-delta continuation, not a fresh source-blind decoding',
            fresh_source_blind_run=False,new_full_semantic_read=False,
            reconstruction=dict(kind='UNCHANGED_ORIGINAL_RECONSTRUCTION_WITH_CURRENT_FORMAL_DELTA',
                original_identity=old['identity'],original_run_id=old['run_id'],original_reconstruction=old['reconstruction'],
                original_evidence_path=row['old_decoder_path'],original_evidence_sha256=row['old_decoder_sha256'],
                original_artifact_path=row['old_artifact_path'],original_artifact_sha256=row['old_artifact_sha256'],
                original_packet_path=row['old_packet_path'],original_packet_sha256=row['old_packet_sha256'],
                original_binding_sha256=row['original_binding'],allOriginalLimitsAndCaveatsRetainedByExactEvidence=True,
                current_delta='Exact source/import closure unchanged and excludes the changed proof pair; original semantic result reused without upgrade'),
            original_lineage_path=BASE_PATH+'lineage.json',original_lineage_sha256=sha((json.dumps(result['lineage'],ensure_ascii=False,indent=2)+'\n').encode()),
            explicit_import_closure=result['closures'][module],opaque_binding_recomputed=False,
            finalInstalledBuildPending=True,current_context_assessment='SUPPORTED_ONLY_WITH_STATED_DELTA_AND_REUSE_LIMITS',**NO_ACCEPT)
    cubic=next(r for r in result['control']['new2'] if r['module'].endswith('/CubicAmplitudePrimitive.lean'))
    data['final-decoders/CubicAmplitudePrimitive.json']=dict(schema='C46_OWN_C31_CUBIC_CURRENT_DECODER_V1',role='decoder',identity=IDENTITY,run_id=run_id,
        module=cubic['module'],binding_sha256=cubic['prospective_binding'],intended_repository_evidence_path=cubic['new_decoder_logical_path'],
        packet_path='reviews/publication/primitive-compiler-c31/decoder-c31/source-formal-seal.json',packet_sha256=SOURCE_SEAL,
        artifact_path=ASSESSMENT_PATH,artifact_sha256=artifact_sha,
        source_blind=True,source_blind_scope='Original complete formal-only reconstruction retained; later own actual technical evidence and current proof-only/input delta disclosed, not a fresh blind reset',
        fresh_source_blind_run=False,new_full_semantic_read=False,
        reconstruction='My original whole3-module/87-root formal-only reconstruction and my subsequent whole25-declaration Cubic reconstruction are retained exactly. The concrete system has wires0/1 little-endian, signal2, encode(s,j)=j+4s, amplitudes(j/4)^3 for j in Fin4, and full unitary[[D,-S],[S,D]]. Relative phases, all input sectors, control/target alias conditions, signal failure branch, zero additional pure ancillas, syntactic versus physical resource limits, and finite2-system-qubit scope remain unchanged. The exact3proof-token candidate has25actual roots plus19generated; prior separatelyactual and jointsame-cohort types/universes/kinds/privacy/valueavailability agree. Removed3selfnative axioms do not recur; standardpropext/Classical.choice/Quot.sound are observed, not axiom-freedom. Current overlay candidate bytes952e and provider6ee match my prior joint31input vector exactly; no finalinstalledbuild was run here.',
        original_complete_reconstruction=dict(sourceSealSHA256=SOURCE_SEAL,wholeCubicSHA256=CUBIC_RECONSTRUCTION,
            actualKernelV3SealSHA256='b8473c295a0e9552589a175cbc018353e5bb664df2fa016a5d2fe6f6002ccf5f',jointOuterSealSHA256=PRIOR_SEAL),
        actualCandidateSourceSHA256=CHANGED[cubic['module']][1],actualProviderCandidateSHA256=CHANGED['QuantumBlockEncoding/CubicStatePreparation.lean'][1],
        actualOldJointCohort=result['priorTechnical']['cohort']['cohortID'],finalInstalledBuildPending=True,
        observedStandardAxioms=['Classical.choice','Quot.sound','propext'],axiomFree=False,
        opaque_binding_recomputed=False,noCSPWholeSemanticDecoderClaim=True,allEarlierProviderAndBodyObservationLimitsRetained=True,**NO_ACCEPT)
    return data


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workspace',type=Path,required=True);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--emit-patch',action='store_true')
    a=ap.parse_args();home=Path(__file__).resolve().parent
    require(not (home/'seal.json').exists(),'already sealed; no overwrite')
    start=datetime.now(timezone.utc).isoformat();began=time.monotonic();r=assess(a.workspace,a.project)
    run_id='c46-c31-current-delta-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-pid'+str(os.getpid())
    data=artifacts(r,run_id)
    import test_assessment
    log=io.StringIO();suite=unittest.defaultTestLoader.loadTestsFromModule(test_assessment)
    outcome=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    require(outcome.wasSuccessful(),'negative tests failed')
    data['python-tests.json']=dict(PID=os.getpid(),startedUTC=start,finishedUTC=datetime.now(timezone.utc).isoformat(),wallSeconds=time.monotonic()-began,
        run_id=run_id,tests=outcome.testsRun,failures=len(outcome.failures),errors=len(outcome.errors),actualPythonInterpreterSHA256=sha(Path(sys.executable).read_bytes()),
        log=log.getvalue(),logSHA256=sha(log.getvalue().encode()),sourcePins={n:sha((home/n).read_bytes()) for n in ('assessment.py','test_assessment.py')},
        localLeanInvocations=0,**NO_ACCEPT)
    output_root=home
    data['handoff-map.json']=dict(artifact_files={n:BASE_PATH+n for n in data if not n.startswith('final-decoders/')},
        wrappers={n:r['intended_repository_evidence_path'] for n,r in data.items() if n.startswith('final-decoders/')},
        parentCopiesExactBytes=True,CSPFinalWrapperNotAuthoredHere=True,**NO_ACCEPT)
    public=['assessment.py','test_assessment.py','HANDOFF.md']+list(data)+['allowlist.json','bindings.json','seal.json']
    data['allowlist.json']=dict(members=public,excluded=['__pycache__/**'],noImplicitGlobPublication=True,**NO_ACCEPT)
    encoded={n:(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode() for n,v in data.items()}
    pins={n:sha((home/n).read_bytes()) for n in ('assessment.py','test_assessment.py','HANDOFF.md')};pins.update({n:sha(v) for n,v in encoded.items()})
    data['bindings.json']=dict(files=pins,controlSHA256=CONTROL,overlayManifestSHA256=MANIFEST,run_id=run_id,**NO_ACCEPT)
    manifest_raw=(json.dumps(data['bindings.json'],ensure_ascii=False,indent=2)+'\n').encode();encoded['bindings.json']=manifest_raw
    data['seal.json']=dict(schema='C46_C31_CURRENT_FORMAL_DELTA_SEAL_V1',manifestSHA256=sha(manifest_raw),allowlistSHA256=sha(encoded['allowlist.json']),
                          pythonReceiptSHA256=sha(encoded['python-tests.json']),identity=IDENTITY,run_id=run_id,**NO_ACCEPT)
    encoded['seal.json']=(json.dumps(data['seal.json'],ensure_ascii=False,indent=2)+'\n').encode()
    for name,raw in encoded.items():
        require(not re.search(rb'[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+[\\/]',raw),'host path in generated artifact')
        require(not (home/name).exists(),'refuse existing output '+name)
    if a.emit_patch:
        patch=['*** Begin Patch']
        for name,raw in encoded.items():
            patch.append('*** Add File: '+(output_root/name).as_posix())
            patch.extend('+'+line for line in raw.decode().splitlines())
        patch.append('*** End Patch');sys.stdout.buffer.write(('\n'.join(patch)+'\n').encode())
    else:print(json.dumps(dict(run_id=run_id,summary=dict(wrapperCount=38,carryforward37=len(r['closures']),formalFiles=len(r['pins'])),testCount=outcome.testsRun)))


if __name__=='__main__':main()
