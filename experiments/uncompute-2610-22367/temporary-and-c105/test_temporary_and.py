"""Integrity and finite sign regressions; not a Lean replay or source admission."""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import re
import unittest

BASE = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()

class TemporaryAndTests(unittest.TestCase):
    def observation(self):
        return json.loads((BASE/'compile-observations.json').read_bytes())

    def test_frozen_contract_precedes_actual_sources(self):
        obs = self.observation()
        self.assertEqual(sha((BASE/'SOURCE.md').read_bytes()), obs['source_contract_sha256'])
        self.assertEqual(sha((BASE/'STATEMENT_SEAL.json').read_bytes()), obs['statement_seal_sha256'])
        self.assertFalse(json.loads((BASE/'STATEMENT_SEAL.json').read_bytes())['proof_body_existed_at_seal'])

    def test_both_sealed_root_headers_are_literal_current_headers(self):
        seal = json.loads((BASE/'STATEMENT_SEAL.json').read_bytes())
        source = (BASE/'TemporaryAnd.lean').read_text()
        normalize = lambda s: re.sub(r'\s+', '', s.replace('Complex','ℂ').replace('->','→'))
        for key in ['amplitude_root','mass_root']:
            header = seal[key]
            name = header.split('theorem ',1)[1].split(' ',1)[0]
            actual = 'theorem '+source.split('theorem '+name,1)[1].split(' := by',1)[0]
            actual = actual.replace('theorem ', 'theorem '+name,1)
            self.assertEqual(normalize(header), normalize(actual))

    def test_actual_sources_times_axioms_and_memory_boundary(self):
        obs = self.observation()
        self.assertEqual(sha((BASE/'TemporaryAnd.lean').read_bytes()),obs['attempts'][1]['source_sha256'])
        self.assertEqual(sha((BASE/'attempt-1-source.lean').read_bytes()),obs['attempts'][0]['source_sha256'])
        self.assertNotEqual(obs['attempts'][0]['source_sha256'],obs['attempts'][1]['source_sha256'])
        for row in obs['attempts']:
            self.assertEqual(row['exit_code'],0)
            self.assertFalse(row['timeout'])
            self.assertGreater(row['seconds'],0)
            self.assertGreaterEqual(row['available_MiB'],5120)
            self.assertEqual(row['memory_cap_MiB'],3072)
            self.assertEqual(row['threads'],1)
        text=obs['actual_current_type_and_axiom_stdout']
        self.assertEqual(text.count('depends on axioms: [propext, Classical.choice, Quot.sound]'),3)
        self.assertNotIn('sorryAx',text)
        self.assertNotIn('Lean.ofReduceBool',text)

    def test_exact_sign_cancellation_for_all_outcomes_and_controls(self):
        for m,a,b in itertools.product(range(2),repeat=3):
            measured_sign=(-1)**(m*(a&b))
            cz_sign=-1 if m==a==b==1 else 1
            self.assertEqual(measured_sign*cz_sign,1)

    def test_complex_reference_coherence_and_branch_mass_proxy(self):
        amplitudes=[complex(r+2*a-b,2*r-a+3*b) for r,a,b in itertools.product(range(3),range(2),range(2))]
        mass=sum(Fraction(int(z.real)**2+int(z.imag)**2) for z in amplitudes)
        for m in range(2):
            corrected=[]
            for r,a,b in itertools.product(range(3),range(2),range(2)):
                z=amplitudes[r*4+a*2+b]
                corrected.append(z*((-1)**(m*(a&b)))*(-1 if m==a==b==1 else 1))
            self.assertEqual(corrected,amplitudes)
            branch_mass=sum(Fraction(int(z.real)**2+int(z.imag)**2,2) for z in corrected)
            self.assertEqual(branch_mass,mass/2)

    def test_omitting_correction_does_not_preserve_coherence(self):
        uncorrected=[(-1)**(a&b) for a,b in itertools.product(range(2),repeat=2)]
        self.assertNotEqual(uncorrected,[1,1,1,1])
        self.assertEqual(uncorrected,[1,1,1,-1])

    def test_arbitrary_modified_workspace_is_not_covered(self):
        # m=1,a=b=0, but measured bit1 rather than current AND0.
        self.assertEqual((-1)**1 * 1,-1)
        self.assertNotEqual((-1)**1 * 1,1)

    def test_no_promotion_or_host_path_leakage(self):
        obs=self.observation()
        for key in ['production_Lean_changed','source_admission','independent_review_complete',
                    'Gaussian_or_SP_BE_or_Hermite_ROOT','full_repository_gate','PURIFIED']:
            self.assertFalse(obs[key],key)
        for path in BASE.iterdir():
            if path.is_file():
                raw=path.read_bytes()
                self.assertIsNone(re.search(rb'(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|qb261009)',raw),path.name)
                self.assertNotIn(b'/' + b'/'.join([b'home', b'runner']) + b'/',raw,path.name)
                self.assertIsNone(re.search(rb'(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}',raw),path.name)

if __name__=='__main__':
    unittest.main()
