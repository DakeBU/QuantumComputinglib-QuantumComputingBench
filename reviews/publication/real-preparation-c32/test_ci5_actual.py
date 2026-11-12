"""Replay actual CI5 observations; Python checks are not independent source review."""
import copy,hashlib,json,types,unittest,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
PIN='56e379105b69b19e42ec0a20c1567203f6cb96d1fddbe768fa0c9f4844e62492'
BASE='real-preparation-native-c34-implement-v2/public/'
LABELS=['01-prefix','02-help','03-parser-compile','04-parser-observe','11-target','12-target','13-target','21-driver','22-driver','30-observe']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def archive(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names))
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and chr(92) not in n for n in names)
        return {n:z.read(n) for n in names}
def get(files,name):return json.loads(files[BASE+name])
def validator():
    p=ROOT/'tools/real_preparation_native_c34_ci5/public-runtime-package.zip'
    with zipfile.ZipFile(p) as z:
        m=types.ModuleType('c39_pinned_stream_validator')
        exec(compile(z.read('validator.py'),'$SEALED_CI5/validator.py','exec'),m.__dict__)
        return m,json.loads(z.read('profile.json')),sha(z.read('profile.json'))
def replay(files,override=None):
    v,profile,pin=validator();cohort=get(files,'target-cohort.json')
    wanted={r['module']:r['artifacts'][0]['path'] for r in cohort['targets']}
    result=get(files,'30-observe.result.json')
    raw=files[BASE+'30-observe.stdout.raw.sanitized.txt'].decode() if override is None else override
    return v.validate(profile,raw,result['exitCode'],timed_out=result['timedOut'],profile_sha=pin,cohort_id=cohort['cohortID'],expected_oleans=wanted)
class CI5ActualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.f=archive(HERE/'c34-ci5-actual-success-public.zip')
    def test_exact_archive_and_every_public_derivative(self):
        self.assertEqual(sha((HERE/'c34-ci5-actual-success-public.zip').read_bytes()),PIN)
        self.assertEqual(len(self.f),106)
        rows=get(self.f,'raw-derivation-receipts.json')['files']
        names=[r['publicRelativePath'] for r in rows]
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual({BASE+n for n in names},{n for n in self.f if n.startswith(BASE)}-{BASE+'raw-derivation-receipts.json'})
        for r in rows:self.assertEqual(sha(self.f[BASE+r['publicRelativePath']]),r['publicSHA256'])
        self.assertFalse(any(n.endswith(('.olean','.dll','.so','.ir')) for n in self.f))
    def test_ten_actual_serial_children_and_each_headroom_gate(self):
        self.assertEqual({n[len(BASE):-len('.result.json')] for n in self.f if n.startswith(BASE) and n.endswith('.result.json')},set(LABELS))
        previous=None;pids=[]
        for label in LABELS:
            r=get(self.f,label+'.result.json');start=get(self.f,label+'.started.json')
            o=get(self.f,'ci2-'+label+'.observation.json');pre=get(self.f,'ci2-'+label+'.preflight.json');post=get(self.f,'ci2-'+label+'.postflight.json')
            self.assertEqual((r['exitCode'],r['timedOut']),(0,False));self.assertEqual(r['PID'],start['PID']);self.assertGreater(r['PID'],0);pids.append(r['PID'])
            self.assertEqual(o['nativeResult'],r);self.assertTrue(o['actualPIDResultReceiptsMatch']);self.assertTrue(o['actualStreamHashesMatch'])
            self.assertIn('--memory=5120',o['actualArgv']);self.assertIn('--threads=1',o['actualArgv'])
            self.assertTrue(pre['gatePassed']);self.assertGreaterEqual(pre['effectiveHeadroomBytes'],7168*1024**2);self.assertIsNotNone(post['effectiveHeadroomBytes'])
            if previous is not None:self.assertLessEqual(previous,r['startedUTC'])
            previous=r['finishedUTC']
        self.assertEqual(len(set(pids)),10)
    def test_three_actual_fresh_targets_and_provider_exclusion(self):
        c=get(self.f,'target-cohort.json');v,p,pin=validator()
        self.assertEqual([x['module'] for x in c['targets']],[x['module'] for x in p['modules']])
        targets={x['module'] for x in c['targets']}
        for x in c['targets']:
            self.assertEqual(x['nativeResult']['exitCode'],0);self.assertFalse(x['nativeResult']['timedOut'])
            self.assertIn('/cohort/',x['artifacts'][0]['path']);self.assertEqual(len(x['artifacts'][0]['sha256']),64)
        # Complete actual collector bindings independently bind every target to the cohort output.
        rs=v.parse(self.f[BASE+'30-observe.stdout.raw.sanitized.txt'].decode())
        expected={x['module']:x['artifacts'][0]['path'] for x in c['targets']}
        for b in rs['C34_BINDING_JSON']:
            self.assertEqual(b['cohortID'],c['cohortID']);self.assertEqual(b['resolvedOleanPath'],expected[b['module']])
        copies=get(self.f,'provider-copies.json')['files']
        self.assertFalse(targets & {x['module'] for x in copies if 'module' in x})
    def test_full_raw_partition_and_observed_axiom_boundary(self):
        x=replay(self.f);self.assertEqual(x,get(self.f,'completeness.json'))
        self.assertEqual((x['roots'],x['private'],x['generated'],x['owned']),(57,4,47,104))
        for k in ('observedUnsafe','observedSelfAxioms','observedKernelElaborationUnsafeDifferences','observedKernelElaborationValueAvailabilityDifferences','observedKernelElaborationValueExprDifferences'):self.assertEqual(x[k],0)
        self.assertEqual(x['observedAxiomUnion'],['Classical.choice','Quot.sound','propext'])
        self.assertFalse(x['nativeAccepted']);self.assertIsNone(x['sourceAgreement'])
    def test_partial_root_and_elliptical_signature_fail_closed(self):
        v,p,pin=validator();raw=self.f[BASE+'30-observe.stdout.raw.sanitized.txt'].decode()
        lines=raw.splitlines();at=next(i for i,s in enumerate(lines) if s.startswith('C34_ROOT_JSON '))
        with self.assertRaises(ValueError):replay(self.f,'\n'.join(lines[:at]+lines[at+1:])+'\n')
        tag,_,value=lines[at].partition(' ');row=json.loads(value);row['typePrettyExplicit']='Nat -> ⋯'
        lines[at]=tag+' '+json.dumps(row)
        with self.assertRaises(ValueError):replay(self.f,'\n'.join(lines)+'\n')
    def test_wrong_cohort_and_timeout_fail_closed(self):
        f=dict(self.f);c=get(f,'target-cohort.json');c['cohortID']='wrong';f[BASE+'target-cohort.json']=json.dumps(c).encode()
        with self.assertRaises(ValueError):replay(f)
        f=dict(self.f);r=get(f,'30-observe.result.json');r['timedOut']=True;f[BASE+'30-observe.result.json']=json.dumps(r).encode()
        with self.assertRaises(ValueError):replay(f)
    def test_success_does_not_grant_publication_or_root(self):
        x=get(self.f,'result.json')
        for k in ('cleanTransitive','actualLoadTrace','nativeTCBReviewed','scientificAcceptance','nativeAccepted','trustClosure'):self.assertIs(x[k],False)
        for k in ('sourceAgreement','axiomPolicyPass','publicationBinding'):self.assertIsNone(x[k])
        for label in ('launcher-result.json','python-result.json'):
            r=json.loads(self.f['c34-native-ci5/public/'+label]);self.assertEqual(r['exitCode'],0);self.assertFalse(r['scientific_ROOT'])
if __name__=='__main__':unittest.main()
