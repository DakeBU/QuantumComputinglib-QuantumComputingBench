"""Actual source/formal roles and incomplete decoder rejection remain separate."""
import copy,hashlib,json,unittest,zipfile
from pathlib import Path
from website.scripts.check_research_publications import validate_record
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
class SequentialFinalAssociationTests(unittest.TestCase):
    def record_inventory(self):
        records=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        row=next(r for r in records if r['module']=='QuantumBlockEncoding/SequentialPrimitiveAssembly.lean')
        inventory={d['fullName']:d for d in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
        return row,inventory
    def test_actual_whole_formal_and_metadata_originals_remain_exact(self):
        data=[('source-formal-stage4-original12.zip',12,'stage4-seal.json','90bb137aa8939003459b9fcd1c2ade8012333e0f5cd404e131f0ee3777b2401d','c55fe57ba9fcb25c92e9fe11e5903e5b9fedd94b0993283bcc82123b5097cb86'),
              ('metadata-stage5-original11.zip',11,'stage5-seal.json','32c672cb9e21ae6d4a8ef02c8d32da06665c8c5e244bf19986bf5117b47d7b9f','7ae4acdfc3485e597e488730a59a460572017b181719eeaca98b4f39963f733b')]
        for name,count,seal_name,seal_sha,manifest_sha in data:
            with zipfile.ZipFile(BASE/name) as z:
                self.assertEqual(len(z.namelist()),count);self.assertEqual(set(z.namelist()),set(json.loads(z.read('publicsafe-allowlist.json'))['files']))
                self.assertEqual(SHA(z.read(seal_name)),seal_sha);self.assertEqual(SHA(z.read('manifest.json')),manifest_sha)
                for item in json.loads(z.read('manifest.json'))['payloads']:self.assertEqual(SHA(z.read(item['file'])),item['sha256'])
    def test_original_incomplete_decoder_wrapper_is_rejected_not_rewritten(self):
        with zipfile.ZipFile(BASE/'decoder-c53-binding-successor-original6.zip') as z:
            raw=z.read('decoder-binding-wrapper.json')
            self.assertEqual(SHA(raw),'5a2d43c3489acbf35f2d889c87f3bdc5e91afee6f0625cc6afb41f4933f80725')
            self.assertNotIn('reconstruction',json.loads(raw))
            self.assertEqual(raw,(BASE/'decoder-c53-binding-wrapper.json').read_bytes())
        row,inventory=self.record_inventory();row=copy.deepcopy(row)
        row['decoder_evidence']='reviews/publication/sequential-primitive-assembly-c48/decoder-c53-binding-wrapper.json'
        row['reviewer_evidence']='reviews/publication/sequential-primitive-assembly-c48/reviewer-c63-association.json'
        with self.assertRaisesRegex(ValueError,'decoder must retain a source-blind reconstruction'):validate_record(ROOT,row,inventory)
    def test_current_selected_record_passes_unchanged_checker(self):
        row,inventory=self.record_inventory();validate_record(ROOT,row,inventory)
        self.assertEqual(row['binding_sha256'],'b0ceb167ac6eb8f86d0c513a835b96e538219dfa52a3a620880627bd838b0ba9')
        self.assertEqual(row['formalizer'],'UNKNOWN');self.assertEqual(len(row['declarations']),37)
    def test_source_lesson_and_all_obligations_are_preserved(self):
        row,_=self.record_inventory()
        self.assertEqual(SHA((ROOT/row['lesson_path']).read_bytes()),'583cc9333ea977ec6684313749b6f52b49aded53e50456913f065487cada426a')
        self.assertEqual({n for item in row['obligation_map'] for n in item['declarations']},set(row['declarations']))
        self.assertEqual(sum(len(item['declarations']) for item in row['obligation_map']),37)
    def test_original_review_preserves_nonbinding_clean_bond_warning(self):
        with zipfile.ZipFile(BASE/'metadata-stage5-original11.zip') as z:
            wrapper=json.loads(z.read('reviewer-c63-association.json'));report=z.read('reviewer-c63-association-report.md').decode()
            self.assertEqual(set(wrapper['semantic_slots']),{'target','normalization','registers','oracles','ancillas_phases','error_success','resources'})
            self.assertFalse(wrapper['scientific_root_closed']);self.assertFalse(wrapper['PURIFIED'])
            self.assertIn('RAW-DOCSTRING-307',report);self.assertIn('unrepaired',report)
if __name__=='__main__':unittest.main()
