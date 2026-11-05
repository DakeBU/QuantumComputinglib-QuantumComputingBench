"""Synthetic comparison fixtures, exact-byte source tests and real Python children. No Lean."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

import compare
import proof_patch
import runtime

PACKAGE=Path(__file__).parent
PROJECT=Path(os.environ.get('C31_TEST_PROJECT',Path.cwd())).resolve()
CONFIG=runtime.read(PACKAGE/'kernel-profile.json')
CI4,CI2,BASE,P1,ORIGINAL,API=runtime.load_runtime(PROJECT,CONFIG)
GATE=CI4.gate4


def synthetic_records():
    records={t:[] for t in ('C31_ROOT_JSON','C31_GENERATED_JSON','C31_BINDING_JSON')}
    defaults=dict(actualKind='thmInfo',kernelKind='thmInfo',actualPrivate=False,
        kernelRootPresent=True,kernelTypeAndUniversesAgree=True,universeParameters=[],typePrettyExplicit='True',
        typeTextScope='ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION',isUnsafe=False,
        actualHasValueAllowOpaque=True,actualOpaqueInfo=False,actualAxiomInfo=False,sourceOpaque=False,
        valueTextRequested=False,valueObservation='NOT_REQUESTED_VALUE_AVAILABLE',valuePrettyExplicitAllowOpaque=None,
        selfOccursInAxioms=False)
    axioms=runtime.read(PACKAGE/'baseline.json')['targetNativeAxioms']
    for spec in ORIGINAL['roots']:
        name=spec['sourceUserName']
        records['C31_ROOT_JSON'].append(dict(defaults,module=spec['module'],actualName=name,
            userNameViaActualAPI=name,sourceUserName=name,axioms=['propext']+axioms))
    for i,name in enumerate(axioms):
        records['C31_GENERATED_JSON'].append(dict(defaults,module='QuantumBlockEncoding.CubicAmplitudePrimitive',
            actualName=name,userNameViaActualAPI=name,actualKind='axiomInfo',kernelKind='axiomInfo',
            actualAxiomInfo=True,actualHasValueAllowOpaque=False,selfOccursInAxioms=True,axioms=[name]))
    ordinary='Synthetic.generated'
    records['C31_GENERATED_JSON'].append(dict(defaults,module='QuantumBlockEncoding.CubicAmplitudePrimitive',
        actualName=ordinary,userNameViaActualAPI=ordinary,axioms=['propext']+axioms))
    structures={m['module']:[] for m in ORIGINAL['modules']}
    records['C31_BINDING_JSON']=[dict(module=k,structures=v) for k,v in structures.items()]
    baseline=dict(rows=compare.normalized(records),targetNativeAxioms=axioms,structures=structures)
    candidate=copy.deepcopy(records)
    candidate['C31_GENERATED_JSON']=[r for r in candidate['C31_GENERATED_JSON'] if r['actualName'] not in axioms]
    for tag in compare.TAGS:
        for r in candidate[tag]: r['axioms']=[a for a in r['axioms'] if a not in axioms]
    return baseline,records,candidate


def snapshot():
    values={'/proc/meminfo':b'MemAvailable: 12582912 kB\n','/proc/self/cgroup':b'0::/job\n',
        '/proc/self/mountinfo':b'31 20 0:27 / /sys/fs/cgroup rw - cgroup2 cgroup rw\n',
        '/sys/fs/cgroup/cgroup.controllers':b'memory cpu\n','/sys/fs/cgroup/cgroup.procs':b'1\n',
        '/sys/fs/cgroup/job/memory.max':str(10240*GATE.MIB).encode(),
        '/sys/fs/cgroup/job/memory.current':str(1024*GATE.MIB).encode(),
        '/sys/fs/cgroup/job/memory.events':b'oom 0\noom_kill 0\n'}
    return GATE.sample(context=dict(platform='linux',CI='true',GITHUB_ACTIONS='true',RUNNER_OS='Linux',
        GITHUB_RUN_ID='123',GITHUB_JOB='SYNTHETIC_NOT_HARDWARE',GITHUB_SHA='a'*40),
        read_bytes=lambda p:values[p],read_link=lambda p:'cgroup:[4026531835]')


class SourceTests(unittest.TestCase):
    def test_exact_three_tokens_inverse_and_statements_other_bytes(self):
        raw=(PROJECT/proof_patch.RELATIVE).read_bytes(); wanted,sites=proof_patch.candidate(raw)
        self.assertEqual(wanted,(PACKAGE/'candidate'/proof_patch.RELATIVE).read_bytes())
        self.assertEqual([s['originalLine'] for s in sites],[40,93,100])
        self.assertEqual(len(wanted)-len(raw),3)
        with self.assertRaises(ValueError): proof_patch.candidate(raw+b' ')

    def test_profile_only_exact_two_raw_hash_occurrences_change(self):
        raw=(PACKAGE/'original-profile.json').read_bytes(); new=runtime.sha(PACKAGE/'candidate'/proof_patch.RELATIVE)
        self.assertEqual(raw.replace(proof_patch.ORIGINAL_SHA.encode(),new.encode()),(PACKAGE/'profile.json').read_bytes())
        derived=runtime.read(PACKAGE/'profile.json')
        self.assertTrue(proof_patch.validate_derivation(ORIGINAL,derived,new))
        for field,value in [('roots',[]),('nativeAccepted',True),('ppMaxSteps',1),('generatedCountBaseline',197)]:
            bad=copy.deepcopy(derived); bad[field]=value
            with self.assertRaises(ValueError): proof_patch.validate_derivation(ORIGINAL,bad,new)

    def test_actual_baseline_all_200_not_candidate_count_requirement(self):
        baseline=runtime.read(PACKAGE/'baseline.json')
        self.assertEqual(len(baseline['rows']),baseline['observedOwned'])
        self.assertEqual(sum(r['family']=='C31_ROOT_JSON' for r in baseline['rows']),87)
        self.assertEqual(len(baseline['targetNativeAxioms']),3)
        self.assertIsNone(CONFIG['baselineCandidateGeneratedCount'])
        self.assertEqual(len(ORIGINAL['projectInputs']),31)

    def test_real_source_workspace_preparation_no_lean_or_provider_build(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as directory:
            root=Path(directory); work=root/'workspace'; package=root/'runtime-input'
            # Only provider copying is stubbed in this Python-only preparation test.
            fake=SimpleNamespace(copy_providers=lambda *args:[])
            rows,providers,files=runtime.prepare(PROJECT,PACKAGE,work,package,runtime.read(PACKAGE/'profile.json'),fake,API)
            self.assertEqual(len(rows),31); self.assertEqual(providers,[])
            self.assertEqual(runtime.sha(work/proof_patch.RELATIVE),CONFIG['candidateTargetSHA256'])
            self.assertEqual(runtime.sha(PROJECT/proof_patch.RELATIVE),proof_patch.ORIGINAL_SHA)
            runtime.verify(work,runtime.read(PACKAGE/'profile.json')['projectInputs'])
            self.assertEqual(runtime.read(package/'profile.json')['roots'],ORIGINAL['roots'])


class ComparisonTests(unittest.TestCase):
    def test_complete_synthetic_success_all_old_rows_and_extra_removals_reported(self):
        baseline,_,candidate=synthetic_records(); result=compare.compare(baseline,candidate)
        self.assertEqual(result['issues'],[]); self.assertEqual(result['oldRowsCompared'],len(baseline['rows']))
        candidate['C31_ROOT_JSON'][0]['axioms']=[]
        result=compare.compare(baseline,candidate)
        self.assertEqual(result['issues'],[])
        self.assertEqual(result['perOldRow'][0]['extraRemovedBeyondNative3'],['propext'])
        self.assertFalse(result['nativeAccepted']); self.assertIsNone(result['axiomPolicyPass'])

    def test_remaining_native_axiom_or_ref_new_axiom_and_unsafe_refused(self):
        for mutation in ('nativeName','nativeRef','newAxiom','unsafe','selfAxiom'):
            baseline,old,candidate=synthetic_records()
            if mutation=='nativeName': candidate['C31_GENERATED_JSON'].append(old['C31_GENERATED_JSON'][0])
            elif mutation=='nativeRef': candidate['C31_ROOT_JSON'][0]['axioms'].append(baseline['targetNativeAxioms'][0])
            elif mutation=='newAxiom': candidate['C31_ROOT_JSON'][0]['axioms'].append('Synthetic.new_axiom')
            elif mutation=='unsafe': candidate['C31_ROOT_JSON'][0]['isUnsafe']=True
            else: candidate['C31_ROOT_JSON'][0]['selfOccursInAxioms']=True
            self.assertTrue(compare.compare(baseline,candidate)['issues'])

    def test_each_root_surviving_generated_type_and_structure_metadata_checked(self):
        for family,index in [('C31_ROOT_JSON',0),('C31_ROOT_JSON',86),('C31_GENERATED_JSON',0)]:
            baseline,_,candidate=synthetic_records(); candidate[family][index]['typePrettyExplicit']='False'
            self.assertTrue(compare.compare(baseline,candidate)['issues'])
        baseline,_,candidate=synthetic_records(); candidate['C31_BINDING_JSON'][0]['structures']=[{'fake':True}]
        self.assertTrue(compare.compare(baseline,candidate)['issues'])

    def test_missing_duplicate_root_fail_and_generated_add_remove_dynamic(self):
        baseline,_,candidate=synthetic_records()
        for mutation in ('missing','duplicate'):
            bad=copy.deepcopy(candidate)
            if mutation=='missing': bad['C31_ROOT_JSON'].pop()
            else: bad['C31_ROOT_JSON'].append(copy.deepcopy(bad['C31_ROOT_JSON'][0]))
            with self.assertRaises(ValueError): compare.compare(baseline,bad)
        extra=copy.deepcopy(candidate['C31_GENERATED_JSON'][0]); extra.update(actualName='Synthetic.NEW',userNameViaActualAPI='Synthetic.NEW')
        candidate['C31_GENERATED_JSON'].append(extra)
        result=compare.compare(baseline,candidate); self.assertEqual(result['issues'],[])
        self.assertEqual(len(result['newGeneratedRows']),1)
        candidate['C31_GENERATED_JSON'][-1]['axioms'].append('Synthetic.unexpected_imported_axiom')
        self.assertTrue(compare.compare(baseline,candidate)['issues'])


class InstrumentationTests(unittest.TestCase):
    def test_deadline_clamps_every_child_and_exhaustion_refuses(self):
        clock=[100.0]; deadline=runtime.Deadline(clock=lambda:clock[0]); seen=[]
        bounded=deadline.native(lambda *args,**kwargs:seen.append(kwargs['timeout']))
        clock[0]+=2095; bounded(None,None,None,None,None,timeout=900); self.assertEqual(seen,[5.0])
        clock[0]+=5
        with self.assertRaises(RuntimeError): bounded(None,None,None,None,None,timeout=900)
        self.assertEqual(seen,[5.0])

    def test_environment_removes_original_build_fallback_and_rejects_other_local_roots(self):
        with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as directory:
            project=Path(directory)/'project'; work=Path(directory)/'work'
            roots=[project,project/'.lake/build/lib/lean',project/'.lake/packages/lib']
            env=runtime.external_environment(project,work,{'LEAN_PATH':os.pathsep.join(map(str,roots))})
            self.assertEqual(env['LEAN_PATH'].split(os.pathsep),[str(work/'.lake/build/lib/lean'),str(roots[-1])])
            with self.assertRaises(ValueError): runtime.external_environment(project,work,{'LEAN_PATH':str(project/'bad-fallback')})

    def test_callback_rollback_all_hooks_and_environment(self):
        original=dict(os.environ); old_gate=CI2.gate; old_load=BASE.load_shared; old_native=API.native_call; old_write=API.write_json
        callback=SimpleNamespace(write_json=lambda *args:None)
        with self.assertRaises(RuntimeError):
            with runtime.reused_callbacks(BASE,CI2,GATE,API,callback,dict(original,C31_TEST_MARKER='SYNTHETIC')):
                self.assertIs(API.native_call,callback); self.assertIs(CI2.gate,GATE)
                raise RuntimeError('SYNTHETIC_ROLLBACK')
        self.assertEqual(dict(os.environ),original); self.assertIs(CI2.gate,old_gate)
        self.assertIs(BASE.load_shared,old_load); self.assertIs(API.native_call,old_native); self.assertIs(API.write_json,old_write)

    def test_actual_python_children_same_finite_callback_pid_exit_hash_timeout(self):
        for label,code,timeout,expected in [('python-zero','print("KERNEL_SUCCESSOR_PYTHON_ONLY")',10,'PROCESS_EXIT_ZERO'),
            ('python-nonzero','raise SystemExit(7)',10,'PROCESS_NONZERO_UNCLASSIFIED'),
            ('python-timeout','import time; time.sleep(5)',.05,'WRAPPER_TIMEOUT_KILLED_OWN_CHILD')]:
            checks=[]; callback=CI2.BudgetCallback(API,lambda:checks.append(1),{'scope':'SYNTHETIC_NO_LEAN'},sampler=snapshot)
            callback.native=runtime.Deadline().native(callback.native)
            with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as directory:
                private=Path(directory)
                with runtime.reused_callbacks(BASE,CI2,GATE,API,callback,dict(os.environ)):
                    argv=[sys.executable,'-c',code,'--memory=3072','--threads=1']
                    if expected=='PROCESS_EXIT_ZERO': callback(private,label,argv,private,dict(os.environ),timeout)
                    else:
                        with self.assertRaises(API.NativeFailure): callback(private,label,argv,private,dict(os.environ),timeout)
                row=runtime.read(private/('ci2-'+label+'.observation.json'))
                self.assertEqual(row['classification'],expected); self.assertTrue(row['actualStreamHashesMatch'])
                self.assertTrue(row['actualPIDResultReceiptsMatch']); self.assertIn('--memory=5120',row['actualArgv'])
                self.assertEqual(len(checks),2)

    def test_windows_unknown_low_gate_and_pin_drift_start_zero_children(self):
        for sample in (lambda:{'gatePassed':True},lambda:dict(snapshot(),gatePassed=False),
            lambda:GATE.sample(context={'platform':'win32'})):
            callback=CI2.BudgetCallback(API,lambda:None,{},sampler=sample); calls=[]
            callback.native=lambda *a,**k:calls.append(1)
            with tempfile.TemporaryDirectory(prefix='.fixture-',dir=PACKAGE) as directory:
                private=Path(directory)
                with runtime.reused_callbacks(BASE,CI2,GATE,API,callback,dict(os.environ)):
                    with self.assertRaises(CI2.PreflightRefused): callback(private,'python-no-start',['lean'],private,dict(os.environ))
                self.assertEqual(calls,[])
        bad=copy.deepcopy(CONFIG); name=next(iter(bad['runtimePackages']))
        bad['runtimePackages'][name]['runner.py']='0'*64
        with self.assertRaises(ValueError): runtime.load_runtime(PROJECT,bad)


if __name__=='__main__': unittest.main()
