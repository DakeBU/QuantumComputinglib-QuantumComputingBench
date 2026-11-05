"""Replay real type-only output, preserving all stronger unproved boundaries."""
import hashlib,importlib.util,json,re,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class ActualKernelTwoTypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c29-kernel-two-types-v2-actual.json').read_bytes())
        cls.raw=(ROOT/cls.r['archive']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.r['archive']) as z:cls.data={n:z.read(n) for n in z.namelist()}
    def test_exact_original39_public_members_and_raw_derivations(self):
        r=self.r;self.assertEqual(hashlib.sha256(self.raw).hexdigest(),r['archive_sha256']);self.assertEqual(len(self.data),39)
        self.assertEqual(set(self.data),{x['name'] for x in r['members']})
        for row in r['members']:
            raw=self.data[row['name']];self.assertEqual(len(raw),row['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))
        receipts=0
        for name,raw in self.data.items():
            if name.endswith('/raw-derivation-receipts.json'):
                prefix=name.rsplit('/',1)[0]+'/'
                for row in json.loads(raw)['files']:
                    self.assertEqual(hashlib.sha256(self.data[prefix+row['publicRelativePath']]).hexdigest(),row['publicSHA256']);receipts+=1
        self.assertEqual(receipts,36)
    def test_strict_actual_two_types_same_fresh_no_omission(self):
        p=ROOT/'tools/cubic_c29_kernel_types_v2';R=module('actual_kernel_type_entry',p/'run.py');V=module('actual_kernel_type_validator',p/'validate_two_types.py')
        old='cubic-c29-kernel-only-v1/public/';new='cubic-c29-kernel-types-v2/public/'
        binding=json.loads(self.data[new+'input-bindings.json']);fresh=json.loads(self.data[old+'fresh-candidate-artifacts.json'])
        result=R.checked_stream(V,self.data[new+'05-two-kernel-types.stdout.raw.sanitized.txt'].decode(),0,Path(fresh['files'][0]['path']))
        observed=json.loads(self.data[new+'two-kernel-types.json'])
        for key,value in result.items():self.assertEqual(observed[key],value)
        self.assertEqual([len(r['typePrettyExplicit']) for r in result['signatures']],self.r['type_text_characters'])
        self.assertEqual(binding['targetFreshOleanSHA256'],fresh['files'][0]['sha256'])
        self.assertEqual(binding['collectorSourceSHA256'],binding['collectorDestinationSHA256'])
        for key,relative in [('actualEntrySHA256','run.py'),('collectorSourceSHA256','KernelTwoTypes.lean'),('validatorSHA256','validate_two_types.py')]:
            self.assertEqual(binding[key],hashlib.sha256((p/relative).read_bytes()).hexdigest())
        before=json.loads(self.data[old+'04-full-kernel-candidate-probe.setup.json'])['selectedEnvironment']
        after=json.loads(self.data[new+'05-two-kernel-types.setup.json'])['selectedEnvironment']
        self.assertEqual(before,after)
    def test_current_full_kernel_stream_not_assumed_from_prior_job(self):
        with tempfile.TemporaryDirectory(prefix='c29-actual-replay-') as temporary:
            package=Path(temporary)
            with zipfile.ZipFile(ROOT/'tools/cubic_c29_kernel_ci1/public-runtime-package.zip') as z:
                for name in z.namelist():
                    self.assertNotIn('..',Path(name).parts);self.assertFalse(Path(name).is_absolute())
                    destination=package/name;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(z.read(name))
            K=module('actual_new_cohort_kernel_replay',package/'kernel_only.py')
            result=K.validate_changed(json.loads((package/'vendor/expected-roots.json').read_bytes()),
                self.data['cubic-c29-kernel-only-v1/public/04-full-kernel-candidate-probe.stdout.raw.sanitized.txt'].decode(),0,
                json.loads((package/'baseline-observations.json').read_bytes()),package)
        self.assertEqual((result['explicitRoots'],result['generatedObserved']),(319,449))
        self.assertEqual(len(result['removedNativeAxiomsAbsent']),9);self.assertEqual(len(result['additionalGeneratedTheorems']),8)
    def test_actual_processes_and_no_scientific_promotion(self):
        r=self.r
        for row in r['calls']:
            self.assertGreater(row['PID'],0);self.assertEqual(row['exitCode'],0);self.assertFalse(row['timedOut'])
            self.assertEqual((row['memoryMiB'],row['threads']),(3072,1))
        self.assertEqual(r['prior_proof_value_omissions_still_open'],96)
        for field in ('nativeAccepted','scientific_ROOT','main_admission','PURIFIED','losslessExpr','production_Lean_changed'):
            self.assertFalse(r[field])
        self.assertIsNone(r['sourceAgreement']);self.assertIsNone(r['publicationBinding'])
if __name__=='__main__':unittest.main()
