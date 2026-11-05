"""Synthetic kernel resource fixtures; only real subprocesses are Python, never Lean."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace

from contextlib import contextmanager
import runner_v4 as adapter
import resource_gate_v4 as gate

PACKAGE = Path(__file__).parent
PROJECT = Path(os.environ.get('C31_TEST_PROJECT',Path.cwd()))
PROFILE = adapter.read(PACKAGE/'ci4-profile.json')
PRIOR3, PRIOR_PACKAGE = adapter.load_ci3(PROJECT,PROFILE)
PRIOR, CI2_PACKAGE = PRIOR3.load_ci2(PROJECT,adapter.read(PRIOR_PACKAGE/'ci3-profile.json'))
gate.bind_common(PRIOR.gate)


@contextmanager
def root_callbacks(prior,revalidate,binding,sampler=None):
    with adapter.self_callbacks(PRIOR3,revalidate,binding):
        with PRIOR3.root_callbacks(prior,lambda:None,{'fixture':'CI3'},sampler=sampler):
            yield
CONTEXT = dict(platform='linux',CI='true',GITHUB_ACTIONS='true',RUNNER_OS='Linux',
    GITHUB_RUN_ID='123456',GITHUB_JOB='SYNTHETIC_CI4_NOT_HARDWARE',GITHUB_SHA='a'*40)
MOUNT = '/sys/fs/cgroup'


def files():
    rows = {'/proc/meminfo':'MemAvailable: 12582912 kB\n', '/proc/self/cgroup':'0::/parent/job\n',
        '/proc/self/mountinfo':'31 20 0:27 / /sys/fs/cgroup rw - cgroup2 cgroup rw\n',
        MOUNT+'/cgroup.controllers':'cpuset cpu io memory pids\n', MOUNT+'/cgroup.procs':'1\n2\n'}
    for name in ('/parent/job','/parent'):
        rows[MOUNT+name+'/memory.max'] = 'max\n'
        rows[MOUNT+name+'/memory.current'] = str(1024*gate.MIB)+'\n'
        rows[MOUNT+name+'/memory.events'] = 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\n'
    return {k:v.encode('ascii') for k,v in rows.items()}


def snapshot(data=None,context=None,namespace=None,permission=None):
    data = files() if data is None else data
    def read(path):
        if permission == path: raise PermissionError(13,'SYNTHETIC_PERMISSION',path)
        if path not in data: raise FileNotFoundError(2,'SYNTHETIC_MISSING',path)
        return data[path]
    def link(path):
        if permission == path: raise PermissionError(13,'SYNTHETIC_PERMISSION',path)
        return ('cgroup:['+str(gate.INIT_CGROUP_INODE)+']') if namespace is None else namespace[path]
    return gate.sample(context=CONTEXT if context is None else context,read_bytes=read,read_link=link)


class RootAPITests(unittest.TestCase):
    def test_PID1_permission_denied_is_never_read_or_fabricated_under_self_only_contract(self):
        calls=[]; data=files()
        def link(path):
            calls.append(path)
            if path=='/proc/1/ns/cgroup': raise PermissionError(13,'FORBIDDEN_PID1_FIXTURE',path)
            return 'cgroup:[4026531835]'
        row=gate.sample(context=CONTEXT,read_bytes=lambda p:data[p],read_link=link)
        self.assertTrue(gate.validate_snapshot(row))
        self.assertEqual(calls,['/proc/self/ns/cgroup'])
        self.assertEqual(len(row['namespaceReads']),1)
        self.assertNotIn('pid1Inode',row['namespaceObservation'])
        self.assertEqual(row['namespaceObservation']['pid1Observation'],
            dict(status='NOT_REQUESTED_NOT_REQUIRED',readRequested=False,value=None))
        row['namespaceObservation']['pid1Inode']=4026531835
        with self.assertRaises(ValueError): gate.validate_snapshot(row)

    def test_missing_self_permission_or_unknown_self_never_uses_PID1_fallback(self):
        data=files()
        for exception in (FileNotFoundError(2,'MISSING_SELF'),PermissionError(13,'DENIED_SELF')):
            calls=[]
            def link(path):
                calls.append(path); raise exception
            row=gate.sample(context=CONTEXT,read_bytes=lambda p:data[p],read_link=link)
            self.assertFalse(row['gatePassed']); self.assertEqual(calls,['/proc/self/ns/cgroup'])
            self.assertEqual(row['failedReadLogicalPath'],'$PROC/self/ns/cgroup')
        for inode in (4026533000,0):
            row=snapshot(namespace={'/proc/self/ns/cgroup':f'cgroup:[{inode}]',
                '/proc/1/ns/cgroup':f'cgroup:[{inode}]'})
            self.assertFalse(row['gatePassed'])

    def test_new_schema_and_policy_reject_old_contract_and_any_fake_PID1(self):
        for field,value in [('schema','C31_CI3_RESOURCE_ROOT_API_V1')]:
            row=snapshot(); row[field]=value
            with self.assertRaises(ValueError): gate.validate_snapshot(row)
        for marker in (dict(status='READ_OK',readRequested=True,value=4026531835),
            dict(status='NOT_REQUESTED_NOT_REQUIRED',readRequested=False,value=4026531835)):
            row=snapshot(); row['namespaceObservation']['pid1Observation']=marker
            with self.assertRaises(ValueError): gate.validate_snapshot(row)

    def test_true_root_nonroot_only_interfaces_absent_is_typed_NA_not_unlimited(self):
        row=snapshot(); self.assertTrue(gate.validate_snapshot(row))
        self.assertEqual(row['effectiveHeadroomBytes'],12288*gate.MIB)
        self.assertEqual(len(row['cgroups']),2); self.assertEqual(len(row['fileReads']),11)
        self.assertFalse(any(r['path'] == MOUNT+'/'+f for r in row['fileReads'] for f in gate.MEMORY_FILES))
        for value in row['rootObservation']['memoryInterfaces'].values():
            self.assertIsNone(value['value']); self.assertFalse(value['readRequested'])
            self.assertFalse(value['unlimitedObserved'])

    def test_finite_parent_and_host_minimum_boundary_and_one_byte_lower(self):
        for group in ('/parent/job','/parent'):
            data=files(); data[MOUNT+group+'/memory.max']=str(8192*gate.MIB).encode()
            self.assertTrue(gate.validate_snapshot(snapshot(data)))
            data[MOUNT+group+'/memory.current']=str(1024*gate.MIB+1).encode()
            row=snapshot(data); self.assertTrue(row['observationComplete']); self.assertFalse(row['gatePassed'])
            with self.assertRaises(ValueError): gate.validate_snapshot(row)
        data=files(); data['/proc/meminfo']=b'MemAvailable: 7340031 kB\n'
        self.assertFalse(snapshot(data)['gatePassed'])

    def test_missing_every_required_OS_file_is_failed_attempt_not_unlimited(self):
        for name in files():
            data=files(); data.pop(name); row=snapshot(data)
            with self.subTest(name=name):
                self.assertFalse(row['observationComplete']); self.assertFalse(row['gatePassed'])
                self.assertEqual(row['failureType'],'FileNotFoundError')
                attempt=row['readAttempts'][-1]
                self.assertEqual(attempt['status'],'READ_ERROR'); self.assertEqual(attempt['path'],name)
                self.assertEqual(row['failedReadLogicalPath'],attempt['logicalPath'])
                root=True if name.startswith(MOUNT+'/cgroup.') else (False if '/memory.' in name else None)
                self.assertIs(row['failedReadAtVerifiedMountRoot'],root)
                with self.assertRaises(ValueError): gate.validate_snapshot(row)

    def test_permission_errors_nonroot_root_and_namespace_always_refused_with_coordinate(self):
        for path in (MOUNT+'/parent/memory.max',MOUNT+'/cgroup.controllers','/proc/self/ns/cgroup'):
            row=snapshot(permission=path)
            self.assertFalse(row['gatePassed']); self.assertEqual(row['failureType'],'PermissionError')
            self.assertEqual(row['readAttempts'][-1]['errno'],13)
            self.assertIsNotNone(row['failedReadLogicalPath'])

    def test_hidden_virtual_unknown_root_only_and_ambiguous_shapes_refused(self):
        cases=[]
        data=files(); data['/proc/self/mountinfo']=b'31 20 0:27 /parent /sys/fs/cgroup rw - cgroup2 cgroup rw\n'; cases.append(data)
        data=files(); data['/proc/self/mountinfo']*=2; cases.append(data)
        data=files(); data['/proc/self/cgroup']=b'0::/\n'; cases.append(data)
        data=files(); data['/proc/self/cgroup']=b'3:memory:/parent/job\n'; cases.append(data)
        data=files(); data['/proc/self/cgroup']=b'0::/a\n0::/b\n'; cases.append(data)
        for data in cases:
            row=snapshot(data); self.assertFalse(row['gatePassed']); self.assertFalse(row['observationComplete'])
        for ns in ('cgroup:[4026533000]','unknown','cgroup:[0]'):
            # Equality to PID1 alone is never proof of initial cgroup namespace.
            self.assertFalse(snapshot(namespace={'/proc/self/ns/cgroup':ns,'/proc/1/ns/cgroup':ns})['gatePassed'])
        # CI4 deliberately does not consult PID1; a different supplied fixture value is irrelevant.
        self.assertTrue(snapshot(namespace={'/proc/self/ns/cgroup':'cgroup:[4026531835]',
            '/proc/1/ns/cgroup':'cgroup:[4026533000]'})['gatePassed'])

    def test_unknown_resource_and_missing_controller_or_event_counter_refused(self):
        mutations=[('/proc/meminfo',b'MemAvailable: unknown kB\n'),
            (MOUNT+'/parent/memory.max',b'unknown'),(MOUNT+'/parent/memory.current',b'-1'),
            (MOUNT+'/parent/memory.events',b'oom 0\n'),
            (MOUNT+'/parent/memory.events',b'oom 0\noom_kill 0\noom_kill 1\n'),
            (MOUNT+'/cgroup.controllers',b'cpu io\n'),(MOUNT+'/cgroup.procs',b'unknown\n')]
        for name,value in mutations:
            data=files(); data[name]=value
            self.assertFalse(snapshot(data)['gatePassed'])

    def test_windows_ci_off_and_missing_identity_refused_before_any_reads(self):
        for k,v in [('platform','win32'),('CI','false'),('GITHUB_ACTIONS',None),('RUNNER_OS','Windows'),
            ('GITHUB_RUN_ID',None),('GITHUB_JOB',''),('GITHUB_SHA',None)]:
            context=dict(CONTEXT); context[k]=v; row=snapshot(context=context)
            self.assertFalse(row['gatePassed']); self.assertEqual(row['readAttempts'],[])

    def test_missing_every_snapshot_group_root_namespace_receipt_and_attempt_field_rejected(self):
        original=snapshot()
        loci=[(),('cgroups',0),('rootObservation',),('namespaceObservation',),
            ('fileReads',0),('namespaceReads',0),('readAttempts',0)]
        for locus in loci:
            target=original
            for key in locus: target=target[key]
            for field in target:
                row=copy.deepcopy(original); target=row
                for key in locus: target=target[key]
                target.pop(field)
                with self.subTest(locus=locus,field=field), self.assertRaises((ValueError,KeyError,TypeError)):
                    gate.validate_snapshot(row)
        for mutation in ('fakeRoot','missingAncestor','forgedGate','badHash'):
            row=snapshot()
            if mutation=='fakeRoot': row['rootObservation']['memoryInterfaces']['memory.max']['value']='max'
            elif mutation=='missingAncestor': row['cgroups'].pop()
            elif mutation=='forgedGate': row['effectiveHeadroomBytes']+=1
            else: row['namespaceReads'][0]['sha256']='a'*64
            with self.assertRaises((ValueError,KeyError)): gate.validate_snapshot(row)


class CallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base,cls.base_package=PRIOR.load_base(PROJECT,adapter.read(CI2_PACKAGE/'ci2-profile.json'))
        old=sys.dont_write_bytecode; sys.dont_write_bytecode=True
        try: cls.api=cls.base.load_shared(PROJECT,adapter.read(cls.base_package/'profile.json'))
        finally: sys.dont_write_bytecode=old

    def test_real_python_pid_exit_timeout_hash_receipts_and_both_pin_callbacks(self):
        for label,code,timeout,expected in [('python-zero','print("CI4_PYTHON_NOT_LEAN")',10,'PROCESS_EXIT_ZERO'),
            ('python-fail','raise SystemExit(7)',10,'PROCESS_NONZERO_UNCLASSIFIED'),
            ('python-timeout','import time; time.sleep(5)',.05,'WRAPPER_TIMEOUT_KILLED_OWN_CHILD')]:
            checks=[]
            with root_callbacks(PRIOR,lambda:checks.append('ci3'),{'test':'SYNTHETIC'},sampler=snapshot):
                cb=PRIOR.BudgetCallback(self.api,lambda:checks.append('ci2'),{})
                with tempfile.TemporaryDirectory(prefix='.ci4-python-fixture-',dir=PACKAGE) as name:
                    private=Path(name); argv=[sys.executable,'-c',code,'--threads=1','--memory=3072']
                    if expected=='PROCESS_EXIT_ZERO': cb(private,label,argv,private,dict(os.environ),timeout)
                    else:
                        with self.assertRaises(self.api.NativeFailure): cb(private,label,argv,private,dict(os.environ),timeout)
                    obs=adapter.read(private/('ci2-'+label+'.observation.json'))
                    self.assertEqual(obs['classification'],expected)
                    self.assertTrue(obs['actualPIDResultReceiptsMatch']); self.assertTrue(obs['actualStreamHashesMatch'])
                    self.assertGreater(obs['nativeResult']['PID'],0); self.assertEqual(checks,['ci3','ci2','ci3','ci2'])
                    self.assertIn('--memory=5120',obs['actualArgv']); self.assertFalse(obs['nativeAccepted'])
                    self.assertIn('ci3Binding',obs['binding'])

    def test_incomplete_low_unknown_and_windows_start_zero_children(self):
        data=files(); data[MOUNT+'/parent/memory.max']=str(8192*gate.MIB).encode()
        data[MOUNT+'/parent/memory.current']=str(1024*gate.MIB+1).encode()
        samplers=[lambda:snapshot(data),lambda:{'gatePassed':True},
            lambda:snapshot(permission=MOUNT+'/parent/memory.max'),
            lambda:snapshot(context=dict(CONTEXT,platform='win32'))]
        for sample in samplers:
            with root_callbacks(PRIOR,lambda:None,{},sampler=sample):
                cb=PRIOR.BudgetCallback(self.api,lambda:None,{})
                calls=[]; cb.native=lambda *a,**k:calls.append(1)
                with tempfile.TemporaryDirectory(prefix='.ci4-python-fixture-',dir=PACKAGE) as name:
                    private=Path(name)
                    with self.assertRaises(PRIOR.PreflightRefused): cb(private,'python-no-start',['lean'],private,dict(os.environ))
                    self.assertEqual(calls,[])

    def test_unknown_postflight_never_green_and_callbacks_restore_on_error(self):
        old_gate,old_callback=PRIOR.gate,PRIOR.BudgetCallback
        samples=iter([snapshot(),{'gatePassed':True}])
        with self.assertRaises(ValueError):
            with root_callbacks(PRIOR,lambda:None,{},sampler=lambda:next(samples)):
                cb=PRIOR.BudgetCallback(self.api,lambda:None,{})
                with tempfile.TemporaryDirectory(prefix='.ci4-python-fixture-',dir=PACKAGE) as name:
                    private=Path(name)
                    cb(private,'python-bad-post',[sys.executable,'-c','print("PYTHON")'],private,dict(os.environ),10)
        self.assertIs(PRIOR.gate,old_gate); self.assertIs(PRIOR.BudgetCallback,old_callback)

    def test_preserved_pins_and_source_vector_and_no_accept(self):
        adapter.pins(PRIOR_PACKAGE,PROFILE['priorFiles'])
        profile=adapter.read(self.base_package/'profile.json')
        self.assertEqual(len(profile['roots']),87); self.assertEqual(len(profile['modules']),3)
        self.assertEqual(sum(r['sourcePrivate'] for r in profile['roots']),8)
        self.api.verify_pins(PROJECT,profile['projectInputs'])
        for k,v in adapter.NO_ACCEPT.items(): self.assertIs(PROFILE[k],v)
        bad=copy.deepcopy(PROFILE); bad['priorFiles']['runner_v3.py']='0'*64
        with self.assertRaises(ValueError): adapter.load_ci3(PROJECT,bad)

    def test_actual_shared_exporter_keeps_raw_hash_and_explicit_logical_derivative(self):
        with tempfile.TemporaryDirectory(prefix='.ci4-python-fixture-',dir=PACKAGE) as name:
            root=Path(name); private=root/'private'; public=root/'public'; private.mkdir(); public.mkdir()
            row=snapshot(permission=MOUNT+'/parent/memory.max')
            self.api.write_json(private/'resource.json',row)
            original=self.api.sha(private/'resource.json')
            self.api.export_public(private,public,{str(root):'$SYNTHETIC_TEMP'})
            derivative=adapter.read(public/'resource.json')
            receipt=adapter.read(public/'raw-derivation-receipts.json')['files'][0]
            self.assertEqual(receipt['rawSHA256'],original)
            self.assertEqual(receipt['publicSHA256'],self.api.sha(public/'resource.json'))
            self.assertNotEqual(receipt['rawSHA256'],receipt['publicSHA256'])
            self.assertEqual(derivative['failedReadLogicalPath'],'$CGROUP_NONROOT_1/memory.max')
            self.assertNotIn(MOUNT,(public/'resource.json').read_text())
            self.assertEqual([r['sha256'] for r in row['fileReads']],
                             [r['sha256'] for r in derivative['fileReads']])

    def test_ci3_pin_callback_error_never_starts_native(self):
        def fail(): raise ValueError('SYNTHETIC_CI4_PIN_DRIFT')
        with root_callbacks(PRIOR,fail,{},sampler=snapshot):
            cb=PRIOR.BudgetCallback(self.api,lambda:None,{})
            calls=[]; cb.native=lambda *a,**k:calls.append(1)
            with tempfile.TemporaryDirectory(prefix='.ci4-python-fixture-',dir=PACKAGE) as name:
                private=Path(name)
                with self.assertRaisesRegex(ValueError,'CI4_PIN_DRIFT'):
                    cb(private,'python-pin-drift',['lean'],private,dict(os.environ))
                self.assertEqual(calls,[]); self.assertEqual(list(private.iterdir()),[])


if __name__=='__main__': unittest.main()
