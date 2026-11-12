"""Positive/negative Python only; synthetic olean fixtures are never Lean evidence."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import entry as E
import joint_compare as J

PACKAGE=Path(__file__).parent.resolve()
PROJECT=Path(os.environ['C31_JOINT_TEST_PROJECT']).resolve()


class JointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (cls.profile,cls.derived,cls.guard,cls.runtime,cls.ci4,cls.ci2,cls.base,cls.p1,
            cls.api,cls.csp_data,cls.cubic,cls.delta)=E.setup(PROJECT,PACKAGE)
        cls.csp=E.archive(PROJECT/cls.profile['cspBaselineArchive'],cls.profile['archives'][cls.profile['cspBaselineArchive']])
        cls.c31=E.archive(PROJECT/cls.profile['c31BaselineArchive'],cls.profile['archives'][cls.profile['c31BaselineArchive']])
        cls.temp=tempfile.TemporaryDirectory(prefix='.validators-',dir=PACKAGE); folder=Path(cls.temp.name)
        for name in ('validate-output.py','validate-output-v2.py','expected-roots.json'):
            E.write_bytes(folder/name,cls.csp_data['vendor/'+name])
        cls.original=E.load('joint_test_original',folder/'validate-output.py')
        cls.fields=E.load('joint_test_fields',folder/'validate-output-v2.py')
        cls.expected=E.read(folder/'expected-roots.json')
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def csp_compare(self,full=None,two=None):
        original=self.csp[J.CSP_FULL].decode(); supplement=self.csp[J.CSP_TWO].decode()
        return J.compare_csp(original,supplement,original if full is None else full,supplement if two is None else two,
            self.expected,self.original,self.fields)
    def text(self,records,tags):
        return '\n'.join(t+' '+json.dumps(row) for t in tags for row in records[t])+'\n'

    def test_archive_exact_candidates_and_single31_input_overlay(self):
        self.assertEqual(len(self.csp_data),10); self.assertEqual(len(self.derived['projectInputs']),31)
        self.assertEqual(J.sha(self.csp_data['candidate/CubicStatePreparation.lean']),E.NEW_CSP)
        self.assertEqual(J.sha(self.cubic),E.NEW_CUBIC)
        self.assertNotIn(J.CSP,self.derived['providers']); self.assertEqual(len(self.derived['providers']),24)
        self.assertEqual(self.profile['compileOrder'][0],J.CSP)
        self.assertIsNone(self.profile['expectedJointGeneratedCount'])

    def test_actual_candidate_baselines_replay_not_joint_success(self):
        J.receipt_partition(self.csp,'cubic-c29-kernel-only-v1/public/')
        J.receipt_partition(self.csp,'cubic-c29-kernel-types-v2/public/')
        J.receipt_partition(self.c31,'')
        csp=self.csp_compare(); c31=J.compare_c31(self.c31[J.C31_STREAM].decode(),self.c31[J.C31_STREAM].decode())
        self.assertEqual((csp['explicitRoots'],csp['generatedObserved']),(319,449))
        self.assertEqual((c31['explicitRoots'],c31['generatedObserved']),(87,113))
        self.assertEqual(csp['oldGeneratedValueTextOmissions'],96)
        self.assertEqual(csp['newGeneratedValueTextOmissions'],96)
        self.assertFalse(csp['nativeAccepted']); self.assertFalse(c31['nativeAccepted'])

    def test_csp_exact_proof_delta_wrong_source_and_nonproof_edit_rejected(self):
        original=self.csp_data['original/CubicStatePreparation.lean']; candidate=self.csp_data['candidate/CubicStatePreparation.lean']
        self.assertEqual(E.verify_csp_delta(original,candidate)['proofTokenEdits'],9)
        for badold,badnew in ((original+b' ',candidate),(original,candidate+b' ')):
            with self.assertRaises(ValueError): E.verify_csp_delta(badold,badnew)

    def test_cache_rejection_for_each_of_four_targets_and_each_sidecar(self):
        with tempfile.TemporaryDirectory(prefix='.cache-',dir=PACKAGE) as name:
            root=Path(name)
            for module in self.profile['compileOrder']:
                for suffix in self.api.SIDECARS:
                    file=root/(module.replace('.','/')+suffix); file.parent.mkdir(parents=True,exist_ok=True); file.write_bytes(b'SYNTHETIC_OLD_TARGET')
                    with self.assertRaises(ValueError): E.reject_target_cache([root],self.profile['compileOrder'],self.api)
                    file.unlink()
            E.reject_target_cache([root],self.profile['compileOrder'],self.api)

    def test_real31_source_prepare_two_candidates_no_target_provider_seed(self):
        calls=[]
        def no_binary_copy(project,seed,profile,api): calls.append(list(profile['providers'])); return []
        with tempfile.TemporaryDirectory(prefix='.prepare-',dir=PACKAGE) as name:
            root=Path(name); rows,seed,files,helper=E.prepare(PROJECT,root/'work',root/'view',self.derived,self.p1,self.api,
                SimpleNamespace(copy_providers=no_binary_copy),self.guard,self.csp_data['candidate/CubicStatePreparation.lean'],self.cubic)
            self.assertEqual(len(rows),31); self.assertEqual(E.sha(root/'work'/E.CSP),E.NEW_CSP)
            self.assertEqual(E.sha(root/'work'/E.CUBIC),E.NEW_CUBIC)
            self.assertEqual(calls,[self.derived['providers']]); self.assertFalse(set(calls[0])&set(self.profile['compileOrder']))
            self.base.recheck_rows(seed,self.api); self.api.verify_pins(root/'work',self.derived['projectInputs'])
            self.assertFalse(helper['copiedHelperExecuted'])

    def test_single_insertion_same_cohort_source_and_output_binding(self):
        with tempfile.TemporaryDirectory(prefix='.insert-',dir=PACKAGE) as name:
            work=Path(name)/'work'; work.mkdir(); inner=work/self.base.OUT_REL
            for d in ('private','cohort','source','driver'): (inner/d).mkdir(parents=True,exist_ok=True)
            E.write_bytes(work/E.CSP,self.csp_data['candidate/CubicStatePreparation.lean'])
            self.api.write_json(inner/'private/provider-inventory.json',dict(leanBinary=sys.executable,leanBinarySHA256=E.sha(Path(sys.executable))))
            env=dict(LEAN_PATH=os.pathsep.join(str(inner/x) for x in ('cohort','driver')),profileSHA256='a'*64,cohortID='SYNTHETIC_SHARED_COHORT')
            path=inner/'private/runtime-environment.json'; self.api.write_json(path,env); calls=[]
            def fake_compile(private,label,argv,cwd,environment,timeout):
                calls.append((label,argv,cwd,environment)); output=Path(argv[argv.index('-o')+1]); E.write_bytes(output,b'SYNTHETIC_NOT_A_LEAN_ARTIFACT')
                return dict(PID=12345,exitCode=0,timedOut=False,scope='SYNTHETIC_TEST_ONLY')
            joint=E.JointCSP(work,self.base,self.api,fake_compile,self.derived); joint.compile(path,env)
            self.assertEqual(calls[0][0],'10-csp-target'); self.assertEqual(joint.receipt['cohortID'],'SYNTHETIC_SHARED_COHORT')
            self.assertEqual(calls[0][3]['C31_COHORT_ID'],joint.receipt['cohortID'])
            self.assertEqual(joint.receipt['sourceSHA256Before'],E.NEW_CSP)
            self.base.recheck_rows(joint.rows,self.api)
            with self.assertRaises(ValueError): joint.compile(path,env)

    def test_insertion_write_precedes_compile_and_restores_callback(self):
        order=[]; original=lambda p,v:order.append('written'); cb=SimpleNamespace(write_json=original)
        joint=SimpleNamespace(compile=lambda p,v:order.append('compile'))
        with self.assertRaises(RuntimeError):
            with E.insertion(cb,joint): cb.write_json(Path('fixture'),{}); raise RuntimeError('SYNTHETIC_ROLLBACK')
        self.assertEqual(order,['written','compile']); self.assertIs(cb.write_json,original)

    def test_foreign_cohort_root_or_same_source_different_fresh_artifact_rejected(self):
        root=PACKAGE/'SYNTHETIC_cohort'; path=str(root/E.CSP.replace('.lean','.olean'))
        csp=dict(cohortID='SYNTHETIC_A',freshOlean=path)
        three=dict(cohortID='SYNTHETIC_A',targets=[dict(cohortID='SYNTHETIC_A',artifacts=[dict(path=str(root/'QuantumBlockEncoding/PrimitiveMacros.olean'))])])
        full={J.CSP_TAGS[0]:[dict(actualResolvedOleanPath=path)]}; two={J.TWO_TAGS[0]:[dict(actualResolvedOleanPath=path)]}
        E.joint_bindings(csp,three,full,two)
        bad=copy.deepcopy(three); bad['cohortID']='SYNTHETIC_B'
        with self.assertRaises(ValueError): E.joint_bindings(csp,bad,full,two)
        for key in ('full','two'):
            foreign=copy.deepcopy(full if key=='full' else two)
            foreign[J.CSP_TAGS[0] if key=='full' else J.TWO_TAGS[0]][0]['actualResolvedOleanPath']=str(PACKAGE/'old-cache.olean')
            with self.assertRaises(ValueError): E.joint_bindings(csp,three,foreign if key=='full' else full,foreign if key=='two' else two)

    def test_missing_duplicate_or_unknown_CSP_records_rejected(self):
        records=J.strict(self.csp[J.CSP_FULL].decode(),J.CSP_TAGS)
        bad=copy.deepcopy(records); bad[J.CSP_TAGS[2]].pop()
        with self.assertRaises(ValueError): self.csp_compare(self.text(bad,J.CSP_TAGS))
        bad=copy.deepcopy(records); bad[J.CSP_TAGS[2]].append(bad[J.CSP_TAGS[2]][0])
        with self.assertRaises(ValueError): self.csp_compare(self.text(bad,J.CSP_TAGS))
        with self.assertRaises(ValueError): self.csp_compare('UNKNOWN {}\n')

    def test_two_type_omission_or_missing_supplement_never_passes(self):
        two=J.strict(self.csp[J.CSP_TWO].decode(),J.TWO_TAGS)
        bad=copy.deepcopy(two); bad[J.TWO_TAGS[1]][0]['typePrettyExplicit']='Nat → ⋯'
        with self.assertRaises(ValueError): self.csp_compare(two=self.text(bad,J.TWO_TAGS))
        bad=copy.deepcopy(two); bad[J.TWO_TAGS[1]].pop()
        with self.assertRaises(ValueError): self.csp_compare(two=self.text(bad,J.TWO_TAGS))

    def test_perrow_axiom_increase_and_signature_drift_rejected(self):
        records=J.strict(self.c31[J.C31_STREAM].decode(),J.C31_TAGS)
        for key,value in [('axioms',['Unexpected.foreign_axiom']),('typePrettyExplicit','Nat')]:
            bad=copy.deepcopy(records); bad[J.C31_TAGS[1]][0][key]=value
            with self.assertRaises(ValueError): J.compare_c31(self.c31[J.C31_STREAM].decode(),self.text(bad,J.C31_TAGS))

    def test_CSP_private_kind_or_structure_drift_rejected(self):
        records=J.strict(self.csp[J.CSP_FULL].decode(),J.CSP_TAGS)
        for change in ('private','kind','structure'):
            bad=copy.deepcopy(records)
            if change=='private': bad[J.CSP_TAGS[1]][0]['actualPrivate']=True
            elif change=='kind': bad[J.CSP_TAGS[1]][0]['actualKind']='opaqueInfo'
            else: bad[J.CSP_TAGS[0]][0]['actualStructures'][0]['fields'].pop()
            with self.assertRaises(ValueError): self.csp_compare(self.text(bad,J.CSP_TAGS))

    def test_dynamic_CSP_generated_count_not_guessed_and_new_axiom_rejected(self):
        records=J.strict(self.csp[J.CSP_FULL].decode(),J.CSP_TAGS); bad=copy.deepcopy(records)
        row=copy.deepcopy(next(r for r in bad[J.CSP_TAGS[2]] if r['actualKind']=='thmInfo' and not any(x in r['typePrettyExplicit'] for x in ('⋯','…'))))
        row['actualName']=row['userNameViaActualAPI']='Synthetic.NewFullyObservedProof'
        bad[J.CSP_TAGS[2]].append(row)
        bad[J.CSP_TAGS[0]][0]['observedTargetOwnedConstants']+=1
        for key in ('generatedTargetOwnedConstants','observedTargetOwnedConstants','generatedTypeValueAxiomAuditCompleted'): bad[J.CSP_TAGS[3]][0][key]+=1
        result=self.csp_compare(self.text(bad,J.CSP_TAGS))
        self.assertEqual(result['generatedObserved'],450); self.assertEqual(result['newGenerated'][0]['actualName'],row['actualName'])
        self.assertIsNone(result['axiomPolicyPass'])
        bad=copy.deepcopy(records); bad[J.CSP_TAGS[1]][0]['axioms']=['Unexpected.foreign_axiom']
        with self.assertRaises(ValueError): self.csp_compare(self.text(bad,J.CSP_TAGS))

    def test_archive_byte_pin_and_duplicate_JSON_key_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix='.archive-',dir=PACKAGE) as name:
            path=Path(name)/'bad.zip'; path.write_bytes(b'NOT_AN_AUTHORIZED_ARCHIVE')
            with self.assertRaises(ValueError): E.archive(path,self.profile['archives'][self.profile['cspArchive']])
        with self.assertRaises(ValueError): J.parse('{"actualName":"a","actualName":"b"}')

    def test_v3_guard_binds_true_new_entry_not_old_v3(self):
        base=PROJECT/'tools/c31_kernel_proof_v1'; files=E.read(PROJECT/'tools/c31_kernel_proof_v3/profile.json')['baseFiles']
        new=str(PACKAGE/'entry.py')
        record=self.guard.execution_record(PACKAGE,base,files,self.runtime,new,new,new,E.sha(PACKAGE/'entry.py'))
        self.assertEqual(record['entry']['actualFile'],new)
        with self.assertRaises(ValueError): self.guard.execution_record(PACKAGE,base,files,self.runtime,new,str(PROJECT/'tools/c31_kernel_proof_v3/entry.py'),new,E.sha(PACKAGE/'entry.py'))

    def snapshot(self,low=False):
        gate=self.ci4.gate4; mount='/sys/fs/cgroup'
        data={'/proc/meminfo':b'MemAvailable: 12582912 kB\n','/proc/self/cgroup':b'0::/parent/job\n',
            '/proc/self/mountinfo':b'31 20 0:27 / /sys/fs/cgroup rw - cgroup2 cgroup rw\n',
            mount+'/cgroup.controllers':b'cpu memory pids\n',mount+'/cgroup.procs':b'1\n2\n'}
        for p in ('/parent/job','/parent'):
            data[mount+p+'/memory.max']=b'max\n'; data[mount+p+'/memory.current']=b'1073741824\n'
            data[mount+p+'/memory.events']=b'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n'
        if low: data['/proc/meminfo']=b'MemAvailable: 7340031 kB\n'
        context=dict(platform='linux',CI='true',GITHUB_ACTIONS='true',RUNNER_OS='Linux',GITHUB_RUN_ID='123456',GITHUB_JOB='SYNTHETIC_PYTHON_ONLY',GITHUB_SHA='a'*40)
        return gate.sample(context=context,read_bytes=lambda p:data[p],read_link=lambda p:'cgroup:[4026531835]')

    def test_actual_Python_child_keeps_gate_PID_hash_timeout_and_5120_adapter(self):
        checks=[]; callback=self.ci2.BudgetCallback(self.api,lambda:checks.append(True),{'scope':'SYNTHETIC_PYTHON_NOT_LEAN'},sampler=self.snapshot)
        callback.native=self.runtime.Deadline().native(callback.native)
        with tempfile.TemporaryDirectory(prefix='.python-',dir=PACKAGE) as name:
            private=Path(name)
            with self.runtime.reused_callbacks(self.base,self.ci2,self.ci4.gate4,self.api,callback,dict(os.environ)):
                result=self.api.native_call(private,'python-only',[sys.executable,'-c','print("joint-fixture")','--memory=3072','--threads=1'],PACKAGE,dict(os.environ),timeout=30)
            self.assertEqual(result['exitCode'],0); self.assertGreater(result['PID'],0)
            row=E.read(private/'ci2-python-only.observation.json'); self.assertIn('--memory=5120',row['actualArgv'])
            self.assertTrue(row['actualStreamHashesMatch']); self.assertTrue(row['actualPIDResultReceiptsMatch'])
            self.assertEqual(row['classification'],'PROCESS_EXIT_ZERO')
        self.assertGreaterEqual(len(checks),2)

    def test_low_memory_zero_child_and_Windows_context_rejected(self):
        callback=self.ci2.BudgetCallback(self.api,lambda:None,{'scope':'SYNTHETIC_ZERO_CHILD'},sampler=lambda:self.snapshot(True))
        called=[]; callback.native=lambda *a,**k:called.append(True)
        with tempfile.TemporaryDirectory(prefix='.gate-',dir=PACKAGE) as name:
            with self.runtime.reused_callbacks(self.base,self.ci2,self.ci4.gate4,self.api,callback,dict(os.environ)):
                with self.assertRaises(self.ci2.PreflightRefused): self.api.native_call(Path(name),'no-child',['lean','--memory=3072','--threads=1'],PACKAGE,dict(os.environ))
        self.assertFalse(called)
        with self.assertRaises(ValueError): self.ci4.gate4.context_check(dict(platform='win32',CI='true',GITHUB_ACTIONS='true',RUNNER_OS='Linux'))


if __name__=='__main__': unittest.main()
