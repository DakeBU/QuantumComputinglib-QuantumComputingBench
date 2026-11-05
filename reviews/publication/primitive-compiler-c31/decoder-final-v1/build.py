"""Final two-module opaque bridge from own sealed inputs and exact transported ZIP."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path,PurePosixPath
import subprocess
import sys
import zipfile

import validate as check


def read(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(path): return check.sha(path.read_bytes())
def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out: json.dump(value,out,ensure_ascii=False,indent=2); out.write('\n')


def verified_inputs(project,original_addendum):
    packet,artifact=project/check.PACKET,project/check.ARTIFACT
    check.require(digest(packet)==check.PACKET_SHA,'published own source-formal seal drift')
    check.require(digest(artifact)==check.ARTIFACT_SHA,'exact transported addendum ZIP drift')
    seal=read(packet); source_files={}
    for name,expected in seal['artifactBindings'].items():
        path=packet.parent/name
        check.require(digest(path)==expected,'published own packet member drift')
        source_files[(PurePosixPath(check.PACKET).parent/name).as_posix()]=expected
    # These actual files are read inputs for this bridge, not an asserted author packet.
    text=(packet.parent/'formal-only-reconstruction.md').read_text(encoding='utf-8')
    contracts=read(packet.parent/'declaration-contracts.json')['declarations']
    check.require(text and len(contracts)==87,'original whole formal reconstruction missing')
    addendum_seal=read(original_addendum/'seal.json')
    check.require(digest(original_addendum/'seal.json')=='775f7249bcad57053e2622e79f88837220f394375ebb3741d2cc750d5181646d','own original actual addendum seal drift')
    wanted=addendum_seal['publicSafeReviewAllowlist']; members=[]
    with zipfile.ZipFile(artifact) as archive:
        names=[i.filename for i in archive.infolist() if not i.is_dir()]
        check.require(len(names)==11 and len(set(names))==11 and set(names)==set(wanted),'ZIP exact 11-file partition')
        for name in sorted(names):
            rel=PurePosixPath(name); check.require(len(rel.parts)==1 and not rel.is_absolute(),'unsafe ZIP member')
            raw=archive.read(name)
            check.require(raw==(original_addendum/name).read_bytes(),'ZIP is not byte-identical own addendum transport')
            members.append(dict(path=name,sha256=check.sha(raw),bytes=len(raw)))
    report=read(original_addendum/'report.json')
    roots=read(original_addendum/'root-contract-comparisons.json')['roots']
    generated=read(original_addendum/'generated-observations.json')['rows']
    check.require(len(roots)==62 and len(generated)==94 and not report['binderAlignmentIssues'],'own actual addendum completeness')
    check.require([r['name'] for r in report['oldCatalogDefects']]==['QuantumBlockEncoding.hadamardMatrix_apply'],'catalog correction provenance')
    current={}
    for target in seal['targetBindings']:
        if target['module'] in check.LABELS:
            relative=target['module'].replace('.','/')+'.lean'
            check.require(digest(project/relative)==target['rawSHA256'],'unchanged two-module actual source identity')
            current[relative]=target['rawSHA256']
    return seal,source_files,members,report,current


def build(project,original_addendum):
    package=Path(__file__).parent
    source_seal,source_files,members,report,current=verified_inputs(project,original_addendum)
    now=datetime.now(timezone.utc); pid=os.getpid()
    run='c31-formal-decoder/two-module-final-evidence-v1/'+now.strftime('%Y%m%dT%H%M%SZ')+'-pid'+str(pid)
    later=dict(own_actual_formal_CI_read_after_original_seal=True,
        own_runtime_and_kernel_proof_technical_work_after_original_seal=True,
        parent_opaque_labels_received_after_addendum_seal=True,
        author_natural_source_read=False,author_candidate_packet_read=False,source_first_reviewer_result_read=False,
        details='Initial three-module formal reconstruction was sealed before actual CI inspection. Later context was authorized own CI1-CI4 technical/formal observations, original C31 runtime/collector APIs, Linux resource/API and Lean kernel-only technical work, then own two-module actual addendum. Parent later supplied opaque context labels and scheduling facts; no author/source-first review mathematics was read or adopted.')
    common=dict(schema='C31_TWO_MODULE_DECODER_FINAL_EVIDENCE_V1',role='decoder',identity=check.IDENTITY,
        identity_provenance='Actual continuing collaboration task identity; not a fabricated reviewer/formalizer identity',
        run_id=run,run_id_kind='Local decoder-owned generation label using actual UTC and Python generator PID; not a claimed GitHub run/job',
        generated_utc=now.isoformat(),generator_pid=pid,
        packet_path=check.PACKET,packet_sha256=check.PACKET_SHA,
        packet_path_scope='Concrete re-read source-formal seal file indexing the real own decoder packet; its bound reconstruction/contracts were re-read. Historical raw formal inputs are disclosed in bridge.json. Not an author input packet and not a directory hash.',
        artifact_path=check.ARTIFACT,artifact_sha256=check.ARTIFACT_SHA,
        source_blind=True,source_blind_scope='ORIGINAL_FORMAL_ONLY_RECONSTRUCTION_NO_AUTHOR_NATURAL_OR_REVIEWER_CONTEXT',
        later_context_disclosure=later,
        late_opaque_context=dict(label_only=True,recomputed_by_decoder=False,semantic_identity_inferred=False,
            provenance='Parent supplied current-context hashes after its reported source/config/prospective-overlay recomputation; decoder did not inspect that overlay or derive these labels'),
        source_semantic_agreement=None,admission='NOT_PERFORMED_PARENT_AND_DISTINCT_REVIEWER_OWNED')
    descriptions={
        'QuantumBlockEncoding.PrimitiveMacros': 'Original complete formal-only reconstruction covered all three actual modules and their exact phase/order/spectator/wire-alias/resource boundaries, not a sampled theorem. For PrimitiveMacros it reconstructed the exact H/T/Tdg program phases, arbitrary finite-width monomial and CCX matrices, pairwise-distinct literal macro versus only control-target inequalities for block/conjugation results, and full spectator sectors. The own later actual CI4 addendum compared all 43 source roots and 55 generated declarations (98 owned), including complete actual types, universes, implicit/instance Pi inputs, structures and actual recursive axiom observations. Across the two-module addendum all 62 roots and 94 generated declarations were covered. The old hadamardMatrix_apply catalog signature had been truncated at an inner let assignment; the same sealed completeFormalRegion and mathematical reconstruction retained the full proposition. The addendum explicitly recovered that header and compared it with the actual type without changing any old sealed bytes. This is formal reconstruction and actual-evidence comparison, not a source-equivalence verdict for the opaque late label.',
        'QuantumBlockEncoding.UniformlyControlledRy': 'Original complete formal-only reconstruction covered all three actual modules and their exact phase/order/spectator/wire-alias/resource boundaries. For UniformlyControlledRy it reconstructed arbitrary finite qubit/control widths, repeated controls allowed with only control-target inequalities, exact full-context Ry blocks and chronological half-sum/CX/half-difference/CX recursion, and counts 2^k Ry and 2(2^k-1) CX rather than an angle-preparation or finite-bit efficiency claim. The own later actual CI4 addendum compared all 19 source roots (including all eight private roots resolved through actual APIs) and all 39 generated declarations (58 owned), with complete actual types/universes and implicit/instance Pi inputs. Across the two-module addendum all 62 roots and 94 generated declarations were covered. Its explicit hadamardMatrix_apply signature-catalog correction concerns the other module and does not silently edit either old packet. Full statement/binder and source bytes remain separately bound; this is not a source-equivalence verdict for the opaque late label.'}
    index=[]
    for module,label in check.LABELS.items():
        row=dict(common,module=module,binding_sha256=label,reconstruction=descriptions[module])
        check.validate(row)
        name=module.rsplit('.',1)[1]+'.decoder-evidence.json'; write(package/name,row)
        index.append(dict(module=module,role='decoder',identity=check.IDENTITY,run_id=run,
            binding_sha256=label,evidence_file=name,evidence_sha256=digest(package/name)))
    bridge=dict(schema='C31_LATE_OPAQUE_TWO_MODULE_BRIDGE_V1',identity=check.IDENTITY,run_id=run,
        generated_utc=now.isoformat(),generator_pid=pid,
        original_formal_input_scope='Three raw actual Lean modules and necessary formal providers/imports/config/Lean APIs; deterministic comment masking before formal reading, formal string literals kept only as data. No author natural source, author mathematical packets or independent reviewer result.',
        original_source_seal_path=check.PACKET,original_source_seal_sha256=check.PACKET_SHA,
        original_packet_member_bindings=source_files,
        original_target_bindings=source_seal['targetBindings'],current_two_target_hashes_verified=current,
        artifact_path=check.ARTIFACT,artifact_sha256=check.ARTIFACT_SHA,exact_transport_members=members,
        actual_addendum_seal_sha256='775f7249bcad57053e2622e79f88837220f394375ebb3741d2cc750d5181646d',
        actual_addendum_scope=dict(roots=62,generated=94,owned=156,
            modules=[{k:m[k] for k in ('module','sourceRoots','generated','owned','actualRecursiveAxiomUnion','actualNativeNamedDependencies','actualSelfAxioms','actualUnsafe')} for m in report['modules']],
            binder_alignment_issues=report['binderAlignmentIssues'],old_catalog_defects=report['oldCatalogDefects']),
        later_context_disclosure=later,late_opaque_bindings=dict(check.LABELS),
        context_boundary='These are late opaque labels only. No claim that all 202 current inputs or a prospective author overlay were read, recomputed or semantically identified by this decoder. No actual path/hash is fabricated from a label.',
        packet_path_choice='Checker consumes file bytes: use the actually read source-formal-seal.json, not its containing directory. Seal binds the complete own reconstructed packet; historical raw target inputs remain distinguished from that current bridge input.',
        source_semantic_agreement=None,admission='NOT_PERFORMED_PARENT_AND_DISTINCT_REVIEWER_OWNED',
        old_files_changed=False,registry_written=False,local_lean_invocations=0,git_operations=0,network_operations=0,new_agents=0)
    check.no_unsupported_claims(bridge); write(package/'bridge.json',bridge)
    write(package/'index.json',dict(schema='C31_TWO_MODULE_EVIDENCE_INDEX_V1',identity=check.IDENTITY,run_id=run,
        rows=index,bridge_file='bridge.json',bridge_sha256=digest(package/'bridge.json')))
    command=[sys.executable,'-B','-m','unittest','discover','-s',str(package),'-p','test_evidence.py','-v']
    started=datetime.now(timezone.utc).isoformat(); child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    timeout=False
    try: raw,_=child.communicate(timeout=60)
    except subprocess.TimeoutExpired: timeout=True; child.kill(); raw,_=child.communicate()
    text=raw.decode('utf-8').replace(str(package),'$FINAL_EVIDENCE_PACKAGE')
    write(package/'python-tests.json',dict(kind='ACTUAL_PYTHON_READONLY_BINDING_AND_NEGATIVE_SCHEMA_TESTS_NO_LEAN',
        PID=child.pid,exitCode=child.returncode,timed_out=timeout,started_utc=started,
        finished_utc=datetime.now(timezone.utc).isoformat(),raw_stdout_sha256=check.sha(raw),stdout_sanitized=text))
    print(text)
    check.require(child.returncode==0 and not timeout,'Python test failure')
    verified_inputs(project,original_addendum)
    allow=['README.md','validate.py','build.py','test_evidence.py','PrimitiveMacros.decoder-evidence.json',
        'UniformlyControlledRy.decoder-evidence.json','bridge.json','index.json','python-tests.json','bindings.json','seal.json']
    files={p.name:digest(p) for p in package.iterdir() if p.is_file() and p.name not in ('bindings.json','seal.json')}
    check.require(set(files)==set(allow)-{'bindings.json','seal.json'},'exact final package partition')
    write(package/'bindings.json',dict(files=files))
    write(package/'seal.json',dict(state='DECODER_FINAL_TWO_MODULE_OPAQUE_BRIDGE_SEALED_NOT_ADMISSION',
        identity=check.IDENTITY,run_id=run,generated_utc=now.isoformat(),manifest_sha256=digest(package/'bindings.json'),
        evidence_sha256={r['module']:r['evidence_sha256'] for r in index},bridge_sha256=digest(package/'bridge.json'),
        packet_sha256=check.PACKET_SHA,artifact_sha256=check.ARTIFACT_SHA,public_safe_allowlist=allow,
        old_files_changed=False,registry_written=False,local_lean_invocations=0,git_operations=0,network_operations=0,
        source_semantic_agreement=None,admission='NOT_PERFORMED_PARENT_AND_DISTINCT_REVIEWER_OWNED'))
    print(json.dumps(dict(identity=check.IDENTITY,run_id=run,evidence={r['module']:r['evidence_sha256'] for r in index},
        manifest_sha256=digest(package/'bindings.json'),bridge_sha256=digest(package/'bridge.json'),
        seal_sha256=digest(package/'seal.json'),files=len(allow))))


if __name__=='__main__': build(*map(lambda s:Path(s).resolve(),sys.argv[1:3]))
