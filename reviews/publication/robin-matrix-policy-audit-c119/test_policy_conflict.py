"""Ensure the observed policy conflict stays explicit, not silently bypassed."""
import hashlib,json,runpy,sys,unittest
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT))
from website.scripts.check_research_publications import validate_record

class ExperimentalPublicationBoundaryTests(unittest.TestCase):
    def test_fresh_filename_flag_matches_actual_inventory(self):
        w=runpy.run_path(str(ROOT/'scripts/generate-aspbe-catalog.py'),run_name='test_no_main')
        g=w['load_generator']();w['register_public_modules'](g)
        fresh,_=g.collect()
        rows=[d for d in fresh if d.source=='QuantumBlockEncoding/RobinMatrix.lean']
        self.assertEqual(len(rows),395)
        self.assertTrue(all(d.experimental and not d.open_proof for d in rows))
    def test_unchanged_source_assimilation_guard_rejects_synthetic_record(self):
        rows=json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']
        inv={r['fullName']:r for r in rows}
        names=[r['fullName'] for r in rows if r.get('source')=='QuantumBlockEncoding/RobinMatrix.lean']
        keys=('source_id','source_statement','source_anchor','lesson_path','obligation_map',
            'assumption_deltas','graph_contribution','formalizer','residual_boundary',
            'binding_sha256','decoder_evidence','reviewer_evidence')
        fixture={k:'SYNTHETIC_POLICY_PROBE_NOT_A_REVIEW' for k in keys}
        fixture.update(module='QuantumBlockEncoding/RobinMatrix.lean',declarations=names)
        with self.assertRaisesRegex(ValueError,'unfinished/experimental source cannot enter'):
            validate_record(ROOT,fixture,inv)
    def test_diagnostic_does_not_implement_or_claim_an_acceptance(self):
        p=ROOT/'reports/lean-433-migration/c119-robin-policy-conflict.json'
        r=json.loads(p.read_bytes())
        self.assertEqual(hashlib.sha256((ROOT/r['checker']).read_bytes()).hexdigest(),r['checker_sha256'])
        for key in ('source_assimilated','maintenance_lane_implemented','production_changed',
                    'verifier_changed','scoring_changed','scientific_target_changed','main_merged'):
            self.assertFalse(r[key])

if __name__=='__main__':unittest.main()
