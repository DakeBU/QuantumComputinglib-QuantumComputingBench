"""Replay actual terminal artifacts, including failure and negative guards."""
import copy,hashlib,importlib.util,json,re,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
def capture(name):
    report=json.loads((ROOT/'reports/lean-433-migration'/name).read_bytes())
    raw=(ROOT/report['archive']).read_bytes()
    with zipfile.ZipFile(ROOT/report['archive']) as z:
        assert len(z.namelist())==len(set(z.namelist()))
        files={n:z.read(n) for n in z.namelist()}
    return report,raw,files
class ActualTerminalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k,cls.kr,cls.kf=capture('c31-kernel-v3-actual-success.json')
        cls.c,cls.cr,cls.cf=capture('c34-ci3-actual-memory-failure.json')
        cls.v=module('c35_original_validator',ROOT/'tools/primitive_compiler_native_profile_v1/validator.py')
        cls.comp=module('c35_original_compare',ROOT/'tools/c31_kernel_proof_v1/compare.py')
    def test_exact_transport_and_all_public_derivation_receipts(self):
        for report,raw,files,count in [(self.k,self.kr,self.kf,79),(self.c,self.cr,self.cf,41)]:
            self.assertEqual(hashlib.sha256(raw).hexdigest(),report['archive_sha256'])
            self.assertEqual(len(files),count)
            self.assertEqual(set(files),{r['name'] for r in report['members']})
            for row in report['members']:
                value=files[row['name']]
                self.assertEqual((len(value),hashlib.sha256(value).hexdigest()),(row['bytes'],row['sha256']))
                self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',value))
            receipt_name=next(n for n in files if n.endswith('raw-derivation-receipts.json'))
            prefix=receipt_name[:-len('raw-derivation-receipts.json')]
            receipts=json.loads(files[receipt_name])['files']
            for row in receipts:
                self.assertEqual(hashlib.sha256(files[prefix+row['publicRelativePath']]).hexdigest(),row['publicSHA256'])
    def kernel_records(self):
        return self.v.parse(self.kf['30-observe.stdout.raw.sanitized.txt'].decode())
    def test_strict_whole_current_observation_and_old_baseline(self):
        p=ROOT/'tools/c31_kernel_proof_v1'
        profile=json.loads((p/'profile.json').read_bytes())
        inputs=json.loads(self.kf['input-bindings.json']);cohort=json.loads(self.kf['fresh-target-cohort.json'])
        self.assertEqual(inputs['profileSHA256'],hashlib.sha256((p/'profile.json').read_bytes()).hexdigest())
        result=self.v.validate(profile,self.kf['30-observe.stdout.raw.sanitized.txt'].decode(),0,timed_out=False,
            profile_sha=inputs['profileSHA256'],cohort_id=cohort['cohortID'],
            expected_oleans={r['module']:r['artifacts'][0]['path'] for r in cohort['targets']})
        self.assertEqual(result,json.loads(self.kf['completeness.json']))
        self.assertEqual((result['roots'],result['private'],result['generated'],result['owned']),(87,8,113,200))
        self.assertEqual(result['observedAxiomUnion'],['Classical.choice','Quot.sound','propext'])
        self.assertEqual((result['observedUnsafe'],result['observedSelfAxioms']),(0,0))
        old_report=json.loads((ROOT/'reports/lean-433-migration/c31-actual-ci4-success-native-blockers.json').read_bytes())
        with zipfile.ZipFile(ROOT/old_report['archive']) as z: old=self.v.parse(z.read('30-observe.stdout.raw.sanitized.txt').decode())
        baseline=json.loads((p/'baseline.json').read_bytes())
        self.assertEqual(self.comp.normalized(old),baseline['rows'])
        self.assertEqual(self.comp.compare(baseline,self.kernel_records()),json.loads(self.kf['whole-owned-comparison.json']))
    def test_independent_all_row_native_removal_and_signature_comparison(self):
        rows=self.kernel_records();all_new=rows['C31_ROOT_JSON']+rows['C31_GENERATED_JSON']
        p=ROOT/'tools/c31_kernel_proof_v1';old=json.loads((p/'baseline.json').read_bytes())
        oldmap={(r['family'],r['module'],r['identity']):r for r in old['rows']}
        newmap={(tag,r['module'],r.get('sourceUserName',r['actualName'])):r
                for tag in self.comp.TAGS for r in rows[tag]}
        removed=set(old['targetNativeAxioms']);survivors=set(oldmap)&set(newmap)
        self.assertEqual(len(survivors),197)
        self.assertEqual({oldmap[k]['actualName'] for k in set(oldmap)-set(newmap)},removed)
        changed=0
        for key in survivors:
            a,b=oldmap[key],newmap[key]
            self.assertEqual(self.comp.digest({f:b[f] for f in self.comp.SIG}),a['signatureSHA256'])
            self.assertEqual(set(b['axioms']),set(a['axioms'])-removed)
            changed+=bool(set(a['axioms'])&removed)
        self.assertEqual(changed,21)
        additions=[newmap[k] for k in set(newmap)-set(oldmap)]
        self.assertEqual(len(additions),3)
        for row in additions:
            self.assertEqual(row['actualKind'],'thmInfo');self.assertFalse(row['isUnsafe'])
        for row in all_new:
            self.assertNotEqual(row['actualKind'],'axiomInfo');self.assertFalse(row['selfOccursInAxioms'])
            self.assertFalse(row['isUnsafe']);self.assertFalse(set(row['axioms'])&removed)
    def test_actual_eight_children_resource_chain_and_helper_copy(self):
        files=self.kf;receipts={r['publicRelativePath']:r for r in json.loads(files['raw-derivation-receipts.json'])['files']}
        for stage in ['01-help','02-prefix','11-target','12-target','13-target','21-driver','22-driver','30-observe']:
            r=json.loads(files[stage+'.result.json']);s=json.loads(files[stage+'.setup.json'])
            o=json.loads(files['ci2-'+stage+'.observation.json'])
            self.assertGreater(r['PID'],0);self.assertEqual(r['exitCode'],0);self.assertFalse(r['timedOut'])
            self.assertEqual(o['nativeResult'],r);self.assertEqual(o['actualArgv'],s['argv'])
            self.assertTrue(o['actualStreamHashesMatch']);self.assertTrue(o['actualPIDResultReceiptsMatch'])
            for stream in ['stdout','stderr']:
                self.assertEqual(r[stream+'SHA256'],receipts[stage+'.'+stream+'.raw.sanitized.txt']['rawSHA256'])
            for phase in ['preflight','postflight']:
                gate=json.loads(files['ci2-'+stage+'.'+phase+'.json'])
                self.assertTrue(gate['gatePassed']);self.assertTrue(gate['observationComplete'])
                self.assertEqual((gate['budgetMiB'],gate['reserveMiB']),(5120,2048))
        helper=json.loads(files['shared-helper-copy.json'])
        expected=hashlib.sha256((ROOT/'tools/cubic_c29_diagnostic/runner.py').read_bytes()).hexdigest()
        for field in ['sha256','sourceSHA256Before','sourceSHA256After','destinationSHA256','executingAPISourceSHA256']:
            self.assertEqual(helper[field],expected)
        self.assertFalse(helper['copiedHelperExecuted'])
        e=json.loads(files['executing-code-bindings.json'])
        self.assertEqual(e['entry']['sourceSHA256'],hashlib.sha256((ROOT/'tools/c31_kernel_proof_v3/entry.py').read_bytes()).hexdigest())
        self.assertFalse(e['OSAttestation']);self.assertFalse(e['codeObjectAttestation'])
    def test_observation_and_comparison_fail_closed_under_tamper(self):
        text=self.kf['30-observe.stdout.raw.sanitized.txt'].decode()
        with self.assertRaises(ValueError):self.v.parse(text+'unrecognized output\n')
        rows=copy.deepcopy(self.kernel_records());rows['C31_ROOT_JSON'][0]['typePrettyExplicit']+=' changed'
        baseline=json.loads((ROOT/'tools/c31_kernel_proof_v1/baseline.json').read_bytes())
        self.assertTrue(self.comp.compare(baseline,rows)['issues'])
        rows=copy.deepcopy(self.kernel_records());rows['C31_ROOT_JSON'][0]['axioms'].append('unapproved_axiom')
        self.assertTrue(self.comp.compare(baseline,rows)['issues'])
    def test_real_compiler_discovery_then_lean_memory_exception_not_math(self):
        p='real-preparation-native-c34-implement-v2/public/'
        d=json.loads(self.cf[p+'compiler-discovery.json'])
        self.assertTrue(d['closureComplete']);self.assertEqual(d['candidateCount'],220)
        self.assertEqual((len(d['projectClosure']),len(d['providers'])),(37,34))
        for stage in ['01-prefix','02-help','03-parser-compile','04-parser-observe']:
            self.assertEqual(json.loads(self.cf[p+stage+'.result.json'])['exitCode'],0)
        r=json.loads(self.cf[p+'11-target.result.json']);s=json.loads(self.cf[p+'11-target.setup.json'])
        self.assertEqual(r['exitCode'],-6);self.assertFalse(r['timedOut'])
        self.assertIn('--memory=3072',s['argv']);self.assertIn('--threads=1',s['argv'])
        self.assertEqual(s['argv'][-1],'QuantumBlockEncoding/RealAmplitudePreparation.lean')
        self.assertIn(b'lean::memory_exception',self.cf[p+'11-target.stderr.raw.sanitized.txt'])
        self.assertNotIn(p+'12-target.result.json',self.cf);self.assertNotIn(p+'30-observe.result.json',self.cf)
        self.assertEqual(json.loads(self.cf['c34-native-ci3/public/python-result.json'])['exitCode'],0)
        self.assertFalse(json.loads(self.cf[p+'result.json'])['scientificAcceptance'])
    def test_no_root_or_main_promotion_from_diagnostics(self):
        for report in [self.k,self.c]:
            for key in ['nativeAccepted','scientific_ROOT','main_admission','production_sources_changed','historical_evidence_changed']:
                self.assertFalse(report[key])
            self.assertIsNone(report['sourceAgreement']);self.assertIsNone(report['publicationBinding'])
if __name__=='__main__':unittest.main()
