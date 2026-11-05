import hashlib,json,re,unittest
from fractions import Fraction
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

def cutoff(e):
    if e<=0:raise ValueError('Finite diagnostic domain is positive tolerance only')
    inv=1/e;ceiling=-(-inv.numerator//inv.denominator)
    return (max(1,ceiling)-1).bit_length()

class DegreeCheckpoint(unittest.TestCase):
    def test_exact_authored_sources_and_signature(self):
        self.assertEqual(sha((HERE/'AllocatedDegreeBudget.lean').read_bytes()),'26768957c06cbdf32810c9ea8202404b615caaf51539dea9d64984f4539951cd')
        seal=json.loads((HERE/'STATEMENT_SEAL.json').read_bytes())
        self.assertIn(seal['signature']+' := by',(HERE/'AllocatedDegreeBudget.lean').read_text(encoding='utf-8'))
        self.assertEqual(sha((HERE/'sealed-root-signature.txt').read_bytes()),seal['signature_sha256'])
        self.assertIsNone(re.search(r'\b(sorry|admit|unsafe|native_decide|axiom)\b',(HERE/'AllocatedDegreeBudget.lean').read_text(encoding='utf-8')))

    def test_actual_compile_and_exact_own_output_audit(self):
        c=json.loads((HERE/'compile-observation.json').read_bytes())
        a=json.loads((HERE/'audit-observation.json').read_bytes())
        self.assertEqual((c['exit_code'],a['exit_code']),(0,0))
        self.assertEqual(c['source_sha256'],a['source_sha256'])
        self.assertEqual(c['output_sha256'],a['imported_own_output_sha256'])
        self.assertEqual(len(a['four_new_actual_axiom_reports']),4)
        for row in a['four_new_actual_axiom_reports']:
            self.assertEqual(set(row['axioms']),{'propext','Classical.choice','Quot.sound'})
        self.assertTrue(a['selected_own_output_via_actual_deps'])
        self.assertFalse(a['clean_transitive_TCB'])
        self.assertFalse(a['scientific_ROOT'])

    def test_exact_failures_and_large_outputs_preserved(self):
        idx=json.loads((HERE/'observation-index.json').read_bytes());archive=HERE/idx['archive']
        self.assertEqual(sha(archive.read_bytes()),idx['sha256'])
        with ZipFile(archive) as z:
            self.assertEqual(set(z.namelist()),set(idx['members']))
            for n,row in idx['members'].items():
                b=z.read(n);self.assertEqual((len(b),sha(b)),(row['bytes'],row['sha256']))
            self.assertEqual(json.loads(z.read('C148/probe-result.json'))['exit_code'],1)
            self.assertIn(b'Unused tactic linter',z.read('C149/compiler-feedback.txt'))
        self.assertTrue(idx['first_audit_wrapper_parser_failed'])
        self.assertTrue(idx['original_failures_preserved'])
        self.assertFalse(idx['production_verifier_changed'])

    def test_finite_exact_boundary_diagnostics_not_a_family_proof(self):
        for k in [0,1,2,8]:
            for n in [0,1,8,128]:
                for epsilon in [Fraction(1,256),Fraction(1,3),Fraction(1),Fraction(32)]:
                    delta=epsilon/(4*2**(n+1)*(k+1)**2*2**(2*k))
                    M=n+1+2*k+cutoff(epsilon/(4*(k+1)**2))
                    self.assertLessEqual(cutoff(delta),M)
                    self.assertLessEqual(4*cutoff(delta)**2+2*cutoff(delta)+1,4*M*M+2*M+1)
        for e in [Fraction(0),Fraction(-1)]:
            with self.assertRaises(ValueError):cutoff(e)

if __name__=='__main__':unittest.main()
