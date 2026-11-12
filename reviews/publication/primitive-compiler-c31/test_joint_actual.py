"""Actual same-cohort observations; finite diagnostics never grant source/main acceptance."""
import copy,hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('parent_actual_joint_compare',ROOT/'tools/c29_c31_joint_kernel_v1/joint_compare.py')
J=importlib.util.module_from_spec(spec);spec.loader.exec_module(J)
SHA='c540fc35303cf5c7f865d90cd4b3fbca3b3ef840bd926c743657e606e85b5d51'
def archive(path):
    with zipfile.ZipFile(path) as z:return {n:z.read(n) for n in z.namelist()}
def read(f,n):return J.parse(f[n])
def compare(f):
    a=archive(ROOT/'reviews/publication/cubic-source-c29/kernel-two-types-v2-actual-public.zip')
    b=archive(ROOT/'reviews/publication/primitive-compiler-c31/kernel-v3-actual-success-public.zip')
    old=J.strict(a[J.CSP_FULL].decode(),J.CSP_TAGS);new=J.strict(f['40-csp-probe.stdout.raw.sanitized.txt'].decode(),J.CSP_TAGS)
    ar,ag=J.common_rows(old,J.CSP_TAGS[1],J.CSP_TAGS[2]);br,bg=J.common_rows(new,J.CSP_TAGS[1],J.CSP_TAGS[2])
    J.require(len(ar)==len(br)==319,'CSP319 root coverage')
    at=J.overlay_two(old,J.strict(a[J.CSP_TWO].decode(),J.TWO_TAGS));bt=J.overlay_two(new,J.strict(f['41-csp-two-types.stdout.raw.sanitized.txt'].decode(),J.TWO_TAGS))
    J.require(old[J.CSP_TAGS[0]][0]['actualStructures']==new[J.CSP_TAGS[0]][0]['actualStructures'],'CSP structure drift')
    return J.relational(ar,ag,br,bg,at,bt),J.compare_c31(b[J.C31_STREAM].decode(),f[J.C31_STREAM].decode())
class JointActualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=HERE/'joint-csp-cubic-actual-success-public.zip';cls.f=archive(cls.path)
    def test_archive_and_every_original_public_derivative_receipt(self):
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(),SHA)
        rows=read(self.f,'raw-derivation-receipts.json')['files']
        self.assertEqual(len({r['publicRelativePath'] for r in rows}),len(rows))
        self.assertEqual({r['publicRelativePath'] for r in rows},set(self.f)-{'raw-derivation-receipts.json'})
        for r in rows:self.assertEqual(J.sha(self.f[r['publicRelativePath']]),r['publicSHA256'])
        for n in self.f:self.assertFalse(n.endswith(('.olean','.ir','.so','.dll')))
    def test_eleven_actual_children_have_pid_exit_timeout_and_gated_budget(self):
        labels=['01-help','02-prefix','10-csp-target','11-target','12-target','13-target','21-driver','22-driver','30-observe','40-csp-probe','41-csp-two-types']
        observed={n[:-len('.result.json')] for n in self.f if n.endswith('.result.json')}
        self.assertEqual(set(labels),observed)
        for label in labels:
            result=read(self.f,label+'.result.json');start=read(self.f,label+'.started.json')
            obs=read(self.f,'ci2-'+label+'.observation.json');pre=read(self.f,'ci2-'+label+'.preflight.json')
            post=read(self.f,'ci2-'+label+'.postflight.json')
            self.assertGreater(result['PID'],0);self.assertEqual(result['PID'],start['PID'])
            self.assertEqual(result['exitCode'],0);self.assertFalse(result['timedOut'])
            self.assertEqual(obs['nativeResult'],result);self.assertTrue(obs['actualStreamHashesMatch']);self.assertTrue(obs['actualPIDResultReceiptsMatch'])
            self.assertEqual(obs['classification'],'PROCESS_EXIT_ZERO');self.assertIn('--memory=5120',obs['actualArgv']);self.assertIn('--threads=1',obs['actualArgv'])
            self.assertGreaterEqual(pre['effectiveHeadroomBytes'],7168*1024**2)
            self.assertIs(pre['gatePassed'],True);self.assertIsNotNone(post['effectiveHeadroomBytes'])
    def test_fresh_four_target_chronology_and_both_probes_same_cohort(self):
        cohort=read(self.f,'joint-four-target-cohort.json');csp=cohort['targets'][0]
        self.assertEqual(cohort['compileOrder'],['QuantumBlockEncoding.CubicStatePreparation','QuantumBlockEncoding.PrimitiveMacros','QuantumBlockEncoding.UniformlyControlledRy','QuantumBlockEncoding.CubicAmplitudePrimitive'])
        self.assertEqual(csp['sourceSHA256Before'],csp['sourceSHA256After']);self.assertEqual(csp['sourceSHA256Before'],'6ee53311b5d6e18c46afb3e068341689acb86f1bdbc425e774705e81c9142f44')
        self.assertEqual(csp['cohortID'],cohort['cohortID']);self.assertFalse(csp['sourceArtifactInherited'])
        for p in ('40-csp-probe.stdout.raw.sanitized.txt','41-csp-two-types.stdout.raw.sanitized.txt'):
            tag,_,payload=self.f[p].decode().splitlines()[0].partition(' ');row=J.parse(payload)
            self.assertEqual(row['actualResolvedOleanPath'],csp['freshOlean'])
        self.assertEqual(cohort['bothCSPProbesSameFreshOlean'],csp['freshOlean'])
        previous=read(self.f,'10-csp-target.result.json')['finishedUTC']
        for label in ('11-target','12-target','13-target'):
            r=read(self.f,label+'.result.json');self.assertLessEqual(previous,r['startedUTC']);previous=r['finishedUTC']
    def test_raw_observation_relational_replay_preserves_signatures_and_only_loses_axioms(self):
        csp,c31=compare(self.f)
        self.assertEqual((csp['explicitRoots'],csp['generatedObserved']),(319,449))
        self.assertEqual((c31['explicitRoots'],c31['generatedObserved']),(87,113))
        for result in (csp,c31):
            self.assertTrue(result['allBaselineSignaturesPreserved']);self.assertTrue(result['perRowAxiomsOnlyDecrease'])
            self.assertEqual(result['newGenerated'],[]);self.assertFalse(result['nativeAccepted']);self.assertIsNone(result['sourceAgreement'])
    def test_signature_drift_and_axiom_increase_fail_closed(self):
        f=dict(self.f);rows=J.strict(f[J.C31_STREAM].decode(),J.C31_TAGS)
        for key,value in [('typePrettyExplicit','Nat'),('axioms',['Unexpected.unproved'])]:
            bad=copy.deepcopy(rows);bad[J.C31_TAGS[1]][0][key]=value
            f[J.C31_STREAM]=('\n'.join(t+' '+json.dumps(r) for t in J.C31_TAGS for r in bad[t])+'\n').encode()
            with self.assertRaises(ValueError):compare(f)
    def test_missing_or_elliptical_two_type_supplement_fails_closed(self):
        f=dict(self.f);key='41-csp-two-types.stdout.raw.sanitized.txt'
        f[key]=b''
        with self.assertRaises(ValueError):compare(f)
        two=J.strict(self.f[key].decode(),J.TWO_TAGS);two[J.TWO_TAGS[1]][0]['typePrettyExplicit']='Nat -> ...'
        f[key]=('\n'.join(t+' '+json.dumps(r) for t in J.TWO_TAGS for r in two[t])+'\n').encode()
        with self.assertRaises(ValueError):compare(f)
if __name__=='__main__':unittest.main()
