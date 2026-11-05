import hashlib,json,re,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

class Discriminator(unittest.TestCase):
    def test_actual_source_and_transcript(self):
        p=json.loads((HERE/'result.json').read_bytes())
        self.assertEqual(sha((HERE/'MiddleDiscriminator.lean').read_bytes()),p['source_sha256'])
        out=(HERE/'feedback.txt').read_bytes();self.assertEqual(sha(out),p['stdout_sha256'])
        markers=dict(re.findall(r'^(GENERIC_COUNT|ACTUAL_COUNT|GENERIC_PASS|ACTUAL_PASS)=(.*)$',out.decode(),re.M))
        self.assertEqual(markers,{'GENERIC_COUNT':'1120','ACTUAL_COUNT':'336','GENERIC_PASS':'true','ACTUAL_PASS':'true'})
        self.assertNotIn(b'COUNTEREXAMPLE=',out)
        self.assertEqual(p['exit_code'],0);self.assertFalse(p['timeout'])
    def test_exact_finite_domain_is_not_a_symbolic_proof(self):
        p=json.loads((HERE/'result.json').read_bytes())
        self.assertEqual(p['state'],'FINITE_DISCRIMINATOR_PASS')
        self.assertFalse(p['symbolic_family_proof']);self.assertFalse(p['scientific_ROOT'])
        self.assertFalse(p['three_arm_comparison']);self.assertIsNone(p['strategy_superiority'])
        self.assertEqual(p['source_contract_seal'],'e4be7acce67f288b8b70755da16c4f0c40bba589cd40454b45111547b2c5ee5a')
        self.assertEqual(p['selected_provider_sha256'],'77547431cc9e4759adcd8c25f6a3e57622da492bdb31ac36f2061ab06e50d473')
    def test_unobserved_costs_remain_unknown(self):
        p=json.loads((HERE/'result.json').read_bytes())
        for k in ['model_calls','tokens','CPU_seconds','peak_memory']:self.assertIsNone(p[k])
        self.assertGreater(p['parent_subprocess_wall_seconds'],0)
        source=(HERE/'MiddleDiscriminator.lean').read_text(encoding='utf-8')
        self.assertIn('#eval do',source)
        self.assertIsNone(re.search(r'^\s*(theorem|lemma|axiom)\b',source,re.M))

if __name__=='__main__':unittest.main()
