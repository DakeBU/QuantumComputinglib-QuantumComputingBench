"""Real three-record acceptance, exact role bytes and fail-closed boundaries."""
import copy,hashlib,importlib.util,json,re,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'reviews/publication/sp-extended-c44'
class ActualSPAdmissionTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('unmodified_gate_actual_sp',ROOT/'website/scripts/check_research_publications.py')
        self.gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.gate)
        self.records=json.loads((BASE/'prospective-context.json').read_bytes())['records']
        self.inventory={r['fullName']:r for r in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
    def test_actual_three_records_validate_and_are_in_registry(self):
        registry=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        for record in self.records:
            self.gate.validate_record(ROOT,record,self.inventory)
            self.assertEqual(next(r for r in registry if r['module']==record['module']),record)
    def test_every_final_review_payload_has_original_exact_hash(self):
        with zipfile.ZipFile(BASE/'source-review-final-portable-v1.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(len(z.namelist()),len(seal['payloads'])+1)
            for row in seal['payloads']:
                raw=z.read(row['path'].removeprefix('output:/'))
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
                self.assertEqual(len(raw),row['bytes'])
            for record in self.records:
                name='final-evidence/'+Path(record['reviewer_evidence']).name
                self.assertEqual(z.read(name),(ROOT/record['reviewer_evidence']).read_bytes())
            self.assertEqual(z.read('final-comparison.md'),(BASE/'final-evidence/final-comparison.md').read_bytes())
    def test_missing_actual_reviewer_fails_each_record(self):
        for original in self.records:
            record=copy.deepcopy(original);record['reviewer_evidence']='reviews/publication/sp-extended-c44/mandatory-never-created-reviewer.json'
            self.assertFalse((ROOT/record['reviewer_evidence']).exists())
            with self.assertRaisesRegex(ValueError,'missing evidence file'):
                self.gate.validate_record(ROOT,record,self.inventory)
    def test_swapped_decoder_hash_cannot_pass_a_different_module(self):
        original_load=self.gate.load
        for record in self.records:
            def swapped(root,path):
                obj=copy.deepcopy(original_load(root,path))
                if path==record['reviewer_evidence']:obj['decoder_evidence_sha256']='0'*64
                return obj
            with patch.object(self.gate,'load',side_effect=swapped):
                with self.assertRaisesRegex(ValueError,'exact decoder result'):
                    self.gate.validate_record(ROOT,record,self.inventory)
    def test_portable_successor_contains_no_original_path_bearing_helper(self):
        with zipfile.ZipFile(BASE/'source-review-final-portable-v1.zip') as z:
            for name in z.namelist():
                raw=z.read(name)
                self.assertNotEqual(hashlib.sha256(raw).hexdigest(),'ae47383c8cb28fb1d336bb2291b054721c396f85e110c392188997813b6e8e8c')
                prefixes=tuple((drive+':/'+'Users/').encode() for drive in ('C','D'))+(b'/home/'+b'runner/',)
                for token in prefixes:
                    self.assertNotIn(token.lower(),raw.lower())
                self.assertIsNone(re.search(rb'(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}',raw))
            for helper in ('verify_metadata.py','verify_decoder.py'):
                raw=z.read(helper)
                self.assertIn(b'--repo-root',raw);self.assertIn(b'--workspace-root',raw)
    def test_scope_is_three_bounded_local_owners_not_full_external_algorithms(self):
        counts={Path(r['module']).stem:len(r['declarations']) for r in self.records}
        self.assertEqual(counts,{'StatePreparationBellRoute':17,'StatePreparationPaperEntryCertificates':16,'StatePreparationPaperRoutesCompact':34})
        for record in self.records:
            review=json.loads((ROOT/record['reviewer_evidence']).read_bytes())
            self.assertEqual(set(review['semantic_slots']),{'target','normalization','registers','oracles','ancillas_phases','error_success','resources'})
            self.assertNotEqual(review['identity'],json.loads((ROOT/record['decoder_evidence']).read_bytes())['identity'])
        self.assertFalse(json.loads((BASE/'prospective-context.json').read_bytes())['scientific_ROOT'])
if __name__=='__main__':unittest.main()
