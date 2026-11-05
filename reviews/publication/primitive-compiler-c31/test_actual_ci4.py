"""Actual CI4 success retains native self-axioms and ordinary provenance limits."""
import hashlib,importlib.util,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class ActualCI4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'reports/lean-433-migration/c31-actual-ci4-success-native-blockers.json').read_bytes())
        cls.raw=(ROOT/cls.r['archive']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.r['archive']) as z:cls.data={n:z.read(n) for n in z.namelist()}
        cls.load=lambda _,n:json.loads(cls.data[n])
    def test_exact73_members_and_all_original_public_receipt_hashes(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.r['archive_sha256']);self.assertEqual(len(self.data),73)
        self.assertEqual(set(self.data),{r['name'] for r in self.r['members']})
        for row in self.r['members']:
            raw=self.data[row['name']];self.assertEqual(len(raw),row['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))
        receipts=self.load('raw-derivation-receipts.json')['files']
        self.assertEqual(len(receipts),72)
        for row in receipts:self.assertEqual(hashlib.sha256(self.data[row['publicRelativePath']]).hexdigest(),row['publicSHA256'])
    def test_strict_actual_whole_partition_with_three_real_native_axioms(self):
        package=ROOT/'tools/primitive_compiler_native_profile_v1'
        profile=json.loads((package/'profile.json').read_bytes());inputs=self.load('input-bindings.json');cohort=self.load('fresh-target-cohort.json')
        self.assertEqual(inputs['profileSHA256'],hashlib.sha256((package/'profile.json').read_bytes()).hexdigest())
        V=load_module('c31_actual_ci4_validator',package/'validator.py')
        result=V.validate(profile,self.data['30-observe.stdout.raw.sanitized.txt'].decode(),0,timed_out=False,
            profile_sha=inputs['profileSHA256'],cohort_id=cohort['cohortID'],
            expected_oleans={r['module']:r['artifacts'][0]['path'] for r in cohort['targets']})
        self.assertEqual(result,self.load('completeness.json'))
        self.assertEqual((result['roots'],result['private'],result['generated'],result['owned']),(87,8,113,200))
        rows=V.parse(self.data['30-observe.stdout.raw.sanitized.txt'].decode())
        native=[r for r in rows['C31_GENERATED_JSON'] if r['actualKind']=='axiomInfo']
        self.assertEqual(len(native),3)
        for r in native:
            self.assertEqual(r['module'],'QuantumBlockEncoding.CubicAmplitudePrimitive')
            self.assertTrue(r['selfOccursInAxioms']);self.assertIn(r['actualName'],r['axioms'])
            self.assertIn('._native.native_decide.ax_1_1',r['actualName'])
        self.assertEqual(result['observedUnsafe'],0);self.assertEqual(result['observedSelfAxioms'],3)
    def test_eight_actual_processes_and_resource_receipt_chains(self):
        receipts={r['publicRelativePath']:r for r in self.load('raw-derivation-receipts.json')['files']}
        stages=['01-help','02-prefix','11-target','12-target','13-target','21-driver','22-driver','30-observe']
        for stage in stages:
            result=self.load(stage+'.result.json');self.assertGreater(result['PID'],0)
            self.assertEqual(result['exitCode'],0);self.assertFalse(result['timedOut'])
            setup=self.load(stage+'.setup.json');observation=self.load('ci2-'+stage+'.observation.json')
            self.assertEqual(observation['nativeResult'],result);self.assertEqual(observation['actualArgv'],setup['argv'])
            self.assertTrue(observation['actualStreamHashesMatch']);self.assertTrue(observation['actualPIDResultReceiptsMatch'])
            for stream in ('stdout','stderr'):
                self.assertEqual(result[stream+'SHA256'],receipts[stage+'.'+stream+'.raw.sanitized.txt']['rawSHA256'])
            for phase in ('preflight','postflight'):
                name='ci2-'+stage+'.'+phase+'.json';gate=self.load(name)
                self.assertEqual(observation[phase+'SHA256'],receipts[name]['rawSHA256'])
                self.assertTrue(gate['observationComplete']);self.assertTrue(gate['gatePassed'])
                self.assertEqual((gate['budgetMiB'],gate['reserveMiB']),(5120,2048))
                self.assertGreaterEqual(gate['effectiveHeadroomBytes'],7516192768)
                self.assertEqual(gate['namespaceObservation']['selfInode'],4026531835)
                self.assertFalse(gate['namespaceObservation']['pid1Observation']['readRequested'])
                self.assertIsNone(gate['namespaceObservation']['pid1Observation']['value'])
                self.assertEqual(gate['rootObservation']['type'],'DOCUMENTED_TRUE_ROOT_NOT_APPLICABLE_NOT_UNLIMITED')
    def test_frozen_source_bindings_and_no_policy_promotion(self):
        p=ROOT/'tools/primitive_compiler_native_profile_v1';profile=json.loads((p/'profile.json').read_bytes())
        inputs=self.load('input-bindings.json')
        self.assertEqual({r['relativePath']:r['sha256'] for r in inputs['projectInputs']},profile['projectInputs'])
        self.assertEqual(inputs['sharedInstrumentation'],profile['sharedInstrumentation'])
        cohort=self.load('fresh-target-cohort.json')
        for row in cohort['targets']:
            expected=profile['projectInputs'][row['module'].replace('.','/')+'.lean']
            self.assertEqual(row['sourceSHA256Before'],expected);self.assertEqual(row['sourceSHA256After'],expected);self.assertEqual(row['copiedSourceSHA256'],expected)
        copies=self.load('provider-copies.json')['files']
        self.assertEqual({r['module'] for r in copies},set(profile['providers']))
        for row in copies:
            suffix=row['module'].replace('.','/')+'.olean'
            self.assertEqual(row['source'],'$PROJECT/.lake/build/lib/lean/'+suffix)
            self.assertEqual(row['destination'],'$PROJECT/_out/primitive-compiler-native-profile-v1/cohort/'+suffix)
            self.assertRegex(row['sha256'],'^[0-9a-f]{64}$')
        # Project copy hashes are separate receipts, not external-inventory membership.
        self.assertEqual(self.load('provider-inventory.json')['mode'],'ACTUAL_OS_ARTIFACT_INVENTORY_NOT_LOAD_TRACE')
        for obj in (self.r,self.load('result.json')):
            self.assertIsNone(obj['sourceAgreement']);self.assertIsNone(obj['publicationBinding']);self.assertFalse(obj['nativeAccepted'])
        self.assertFalse(self.r['scientific_ROOT']);self.assertFalse(self.r['main_admission'])
if __name__=='__main__':unittest.main()
