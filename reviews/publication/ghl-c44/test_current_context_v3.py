"""Current-v3 bindings and immutable decoder transport; no source verdict proxy."""
import copy,hashlib,importlib.util,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'reviews/publication/ghl-c44'
class CurrentV3Tests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('unchanged_current_gate',ROOT/'website/scripts/check_research_publications.py')
        self.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.gate)
        self.context=json.loads((BASE/'prospective-context-v3.json').read_bytes())
        self.record=self.context['record']
        self.inventory={r['fullName']:r for r in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
    def test_current_v3_exact_binding_and_graph(self):
        self.assertEqual(self.record['binding_sha256'],self.gate.binding_digest(ROOT,self.record))
        graph=self.record['graph_contribution']
        self.assertEqual(graph['graph_context_sha256'],hashlib.sha256((ROOT/graph['graph_context']).read_bytes()).hexdigest())
        self.assertFalse(self.context['publication_acceptance'])
    def test_actual_decoder_exact_current_identity_and_reconstruction(self):
        raw=(ROOT/self.record['decoder_evidence']).read_bytes(); d=json.loads(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'9d42f27e2955ea0e6c2ac6a92f11775ab5daed69890437a4bef55290ea323255')
        self.assertEqual(d['binding_sha256'],self.record['binding_sha256'])
        self.assertIs(d['source_blind'],True);self.assertIs(d['source_identity_blind'],False)
        self.assertTrue(d['reconstruction'])
        for key in ('packet','artifact'):
            self.assertEqual(d[key+'_sha256'],hashlib.sha256((ROOT/d[key+'_path']).read_bytes()).hexdigest())
    def test_decoder_capsule_preserves_actual_sealed_bytes(self):
        with zipfile.ZipFile(BASE/'decoder-context-v3-final.zip') as z:
            seal=json.loads(z.read('seal.json'))
            for row in seal['sealed_outputs']:
                self.assertEqual(hashlib.sha256(z.read(row['path'])).hexdigest(),row['sha256'])
            self.assertEqual(z.read('GHL2025-decoder-context-v3.json'),(ROOT/self.record['decoder_evidence']).read_bytes())
    def test_absent_reviewer_cannot_be_green(self):
        record=copy.deepcopy(self.record)
        record['reviewer_evidence']='reviews/publication/ghl-c44/mandatory-never-created-current-reviewer.json'
        self.assertFalse((ROOT/record['reviewer_evidence']).exists())
        with self.assertRaisesRegex(ValueError,'missing evidence file'):
            self.gate.validate_record(ROOT,record,self.inventory)
    def test_negative_stage4_remains_bound_not_overwritten(self):
        negative=self.context['metadata_v2_negative_review']
        self.assertEqual(hashlib.sha256((ROOT/negative['path']).read_bytes()).hexdigest(),negative['sha256'])
        with zipfile.ZipFile(ROOT/negative['path']) as z:
            self.assertEqual(hashlib.sha256(z.read('seal.json')).hexdigest(),'53c7a3b42aaef88e01c1aeb716555e4287aa81b430e2a90c00913c9d8aa74b36')
    def test_actual_accepted_local_record_passes_original_gate(self):
        self.gate.validate_record(ROOT,self.record,self.inventory)
        registry=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        self.assertEqual(next(r for r in registry if r['module']==self.record['module']),self.record)
    def test_dropping_one_public_declaration_fails_closed(self):
        record=copy.deepcopy(self.record);record['declarations']=record['declarations'][:-1]
        with self.assertRaisesRegex(ValueError,'whole changed-module inventory'):
            self.gate.validate_record(ROOT,record,self.inventory)
    def test_actual_review_cannot_be_reused_for_changed_decoder(self):
        from unittest.mock import patch
        original_load=self.gate.load
        def changed(root,path):
            value=copy.deepcopy(original_load(root,path))
            if path==self.record['reviewer_evidence']:value['decoder_evidence_sha256']='0'*64
            return value
        with patch.object(self.gate,'load',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'exact decoder result'):
                self.gate.validate_record(ROOT,self.record,self.inventory)
    def test_new_comparison_is_the_reviewers_actual_artifact(self):
        with zipfile.ZipFile(BASE/'source-review-final-v3.zip') as z:
            reviewer=json.loads(z.read('GHL2025-reviewer-context-v3.json'))
            self.assertEqual(z.read('final-comparison.md'),(ROOT/reviewer['artifact_path']).read_bytes())
            self.assertEqual(z.read('GHL2025-reviewer-context-v3.json'),(ROOT/self.record['reviewer_evidence']).read_bytes())
            self.assertEqual(set(reviewer['semantic_slots']),{'target','normalization','registers','oracles','ancillas_phases','error_success','resources'})
if __name__=='__main__':unittest.main()
