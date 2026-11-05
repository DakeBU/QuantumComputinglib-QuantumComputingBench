"""Evidence integrity and non-promotion tests, not mathematical equivalence."""
import hashlib,json,re,unittest
from pathlib import Path
from zipfile import ZipFile
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
EXP=ROOT/'experiments/uncompute-2610-22367/operation-bridge-c128'
sha=lambda b:hashlib.sha256(b).hexdigest()
class CheckpointTests(unittest.TestCase):
    def test_exact_archives_and_members(self):
        o=json.loads((BASE/'index.json').read_bytes())
        self.assertEqual((o['archive_count'],o['member_count']),(6,88))
        for a in o['archives']:
            self.assertEqual(sha((BASE/a['archive']).read_bytes()),a['sha256'])
            with ZipFile(BASE/a['archive']) as z:
                self.assertEqual(set(z.namelist()),set(a['members']))
                for n,r in a['members'].items():
                    self.assertEqual((sha(z.read(n)),len(z.read(n))),(r['sha256'],r['bytes']))
                self.assertEqual(sha(z.read(a['manifest'])),a['manifest_sha256'])
                self.assertEqual(sha(z.read(a['seal'])),a['seal_sha256'])
    def test_no_host_paths_credentials_or_source_images(self):
        for p in BASE.glob('*.zip'):
            with ZipFile(p) as z:
                for n in z.namelist():
                    self.assertFalse(n.endswith(('.png','.pdf')))
                    s=z.read(n).decode('utf-8-sig')
                    for _ in range(2):s=s.replace('\\\\','\\')
                    self.assertIsNone(re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[/\\]',s),n)
                    self.assertIsNone(re.search(r'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{20,}',s))
    def test_typing_probe_is_not_a_theorem_proof(self):
        o=json.loads((EXP/'signature-only-observation.json').read_bytes())
        raw=(EXP/'StatementProbe.lean').read_bytes()
        self.assertEqual(sha(raw),o['source_sha256'])
        self.assertEqual(o['exit_code'],0)
        self.assertFalse(o['theorem_proof_attempt']);self.assertFalse(o['any_root_proved'])
        self.assertIsNone(re.search(rb'(?m)^theorem\s',raw))
        self.assertEqual(raw.count(b'#check '),7)
    def test_statement_seal_retains_actual_definition_and_review_pins(self):
        o=json.loads((EXP/'STATEMENT_SEAL.json').read_bytes())
        self.assertEqual(o['state'],'STATEMENT_SEALED_NOT_PROVED')
        self.assertEqual(o['actual_definition_source_sha256'],sha((EXP/'StatementProbe.lean').read_bytes()))
        self.assertEqual(o['logical_hypothesis_binders'],[]);self.assertEqual(o['EXCESS'],[])
        self.assertFalse(o['proof_seal']);self.assertFalse(o['source_circuit_admission'])
    def test_historical_preflight_is_exact_but_not_execution(self):
        o=json.loads((ROOT/'reports/lean-433-migration/c122-historical-source-preflight.json').read_bytes())
        self.assertEqual((o['source_vector_count'],o['matched']),(220,220))
        self.assertTrue(all(r['matches'] for r in o['config_checks']))
        self.assertFalse(o['Lean_launched']);self.assertFalse(o['current_head_acceptance'])
    def test_prior_build_association_is_not_redated_or_full_TCB(self):
        o=json.loads((ROOT/'reports/lean-433-migration/c124-prior-full-lean-input-association.json').read_bytes())
        self.assertEqual((o['recorded_inputs'],o['unchanged_inputs']),(211,209))
        self.assertEqual((o['proof_input_count'],o['unchanged_proof_inputs']),(207,207))
        self.assertFalse(o['fresh_compile_run']);self.assertFalse(o['runtime_result_redated'])
        self.assertFalse(o['clean_transitive_rebuild']);self.assertFalse(o['main_admission'])
if __name__=='__main__':unittest.main()
