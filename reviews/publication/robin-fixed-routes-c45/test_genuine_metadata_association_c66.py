"""Role-evidence transport and bindings, not mathematical truth by hash."""
import copy,hashlib,json,unittest,zipfile
from pathlib import Path
from website.scripts.check_research_publications import validate_record
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
class GenuineNineAssociationTests(unittest.TestCase):
    def test_exact_stage5_stage6_and_actor_transport_originals(self):
        rows=[('signature-stage5-original8.zip','robin-c47-signature-stage5',8,'40cfd9a24909ff5654b604aac08a471919907f547f88db401c58a2f02ffbe06b','b4c7857170717e6bd36dc7a3d58dfca4cfb640988c60c9365c19efcb2b73c38a'),
          ('metadata-stage6-original21.zip','robin-c47-metadata-stage6',21,'3dab81ab19b355838b453fe33eae897458e036621d82d271004b6d9f56b48ba4','398893644053fbfd4258ba13ed5574931b964a84d9f29d6a59d12d3e4104f0cb'),
          ('metadata-c65-transport-original.zip','robin-c47-metadata-eof-successor-c65',14,'a4e70870a532231dc6358917d6f5d168367d6a7f21506ef01c34b1437fe89f04','d2ca548ef9b4f41707251c18b3b6349b6f2e8c6205e8f2387b45bed74d321ea6')]
        for name,directory,count,seal,manifest in rows:
            with zipfile.ZipFile(BASE/name) as z:
                prefix='W/'+directory+'/'
                self.assertEqual(len(z.namelist()),count)
                self.assertEqual(SHA(z.read('seal.json')),seal);self.assertEqual(SHA(z.read('manifest.json')),manifest)
                self.assertEqual(set(z.namelist()),{n.removeprefix(prefix) for n in json.loads(z.read('publicsafe-allowlist.json'))['files']})
                m=json.loads(z.read('manifest.json'))
                for row in m.get('artifacts',m.get('files',[])):
                    self.assertEqual(SHA(z.read(row['path'].removeprefix(prefix))),row['sha256'])
    def test_actor_report_successor_changes_exactly_one_final_byte(self):
        with zipfile.ZipFile(BASE/'metadata-stage6-original21.zip') as oldz,zipfile.ZipFile(BASE/'metadata-c65-transport-original.zip') as newz:
            old=oldz.read('reviewer-c60-association-report.md');new=newz.read('reviewer-c65-association-report.md')
            self.assertEqual((len(old),len(new)),(7422,7421));self.assertEqual(new+bytes([10]),old)
            self.assertEqual((BASE/'reviewer-c65-association-report.md').read_bytes(),new)
            self.assertFalse(new.endswith(bytes([10,10])))
            self.assertEqual((BASE/'reviewer-c60-association-packet.json').read_bytes(),oldz.read('reviewer-c60-association-packet.json'))
    def test_nine_wrappers_are_actor_originals_and_semantically_unchanged(self):
        with zipfile.ZipFile(BASE/'metadata-stage6-original21.zip') as oldz,zipfile.ZipFile(BASE/'metadata-c65-transport-original.zip') as newz:
            names=[n for n in newz.namelist() if n.endswith('.reviewer-c65.json')];self.assertEqual(len(names),9)
            for name in names:
                raw=newz.read(name);row=json.loads(raw);old=json.loads(oldz.read(name.replace('.reviewer-c65.','.reviewer-c60.')))
                delta={k for k in old if old[k]!=row.get(k)}
                self.assertEqual(delta,{'run_id','artifact_path','artifact_sha256','prospective_reviewer_evidence_path'})
                self.assertEqual(row['identity'],'/root/robin_c47_raw_source_recovery');self.assertTrue(row['anti_anchored'])
                self.assertEqual(row['verdict'],'accepted')
                self.assertEqual((ROOT/row['prospective_reviewer_evidence_path']).read_bytes(),raw)
                for key in ('packet','artifact'):
                    self.assertEqual(SHA((ROOT/row[key+'_path']).read_bytes()),row[key+'_sha256'])
    def test_all_nine_exact_current_records_validate(self):
        registry=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        inventory={d['fullName']:d for d in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
        own=[r for r in registry if r['source_id']=='candidate:aspbe-local-robin-nine-natural-v2']
        self.assertEqual(len(own),9)
        for row in own:validate_record(ROOT,row,inventory)
        self.assertEqual(sum(len(r['declarations']) for r in own),214)
        self.assertEqual(SHA((ROOT/own[0]['lesson_path']).read_bytes()),'10681db8c6f62818bcdd8d6eef787027983b010540e86c547afbaacc34031790')
    def test_modified_scientific_statement_cannot_inherit_accepted_binding(self):
        registry=json.loads((ROOT/'website/research/publications.json').read_bytes())['records']
        row=copy.deepcopy(next(r for r in registry if r['module']=='QuantumBlockEncoding/ModularAdder3.lean'))
        row['source_statement']+=' changed in ordinary negative test'
        inventory={d['fullName']:d for d in json.loads((ROOT/'web/library/declarations.json').read_bytes())['declarations']}
        with self.assertRaisesRegex(ValueError,'binding is stale'):validate_record(ROOT,row,inventory)
if __name__=='__main__':unittest.main()
