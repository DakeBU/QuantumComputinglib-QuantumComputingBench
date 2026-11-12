"""Bounded header repair integrity; never a substitute for source review or Lean."""
import ast,hashlib,json,re,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class SignatureSuccessorTests(unittest.TestCase):
    def newer(self):return zipfile.ZipFile(BASE/'decoder-c57-original23.zip')
    def extractor(self,z):
        tree=ast.parse(z.read('repair_signature_annex.py').decode())
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('tokens','exact_header','unit_tests')]
        self.assertEqual(len(nodes),3)
        scope=dict(re=re)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'<bounded-header-extractor>','exec'),scope)
        return scope
    def test_exact_23_files_and_21_payload_hashes(self):
        with self.newer() as z:
            self.assertEqual(len(z.namelist()),23)
            self.assertEqual(SHA(z.read('seal.json')),'799ad3b94ab03f9dbc7430b3b8870baaab55c28be6161194d7a09120fe3a9de9')
            self.assertEqual(SHA(z.read('manifest.json')),'f4293044679ce2237044e367cd2378a3856483afa905498a15a95a4524d8a783')
            manifest=json.loads(z.read('manifest.json'))
            self.assertEqual(set(z.namelist()),set(manifest['publicsafeAllowlist']))
            self.assertEqual(set(z.namelist()),set(json.loads(z.read('publicsafe-allowlist.json'))['files']))
            self.assertEqual(len(manifest['artifacts']),21)
            for row in manifest['artifacts']:self.assertEqual(SHA(z.read(row['file'])),row['sha256'])
    def test_replay_all_15_bounded_extractor_cases(self):
        with self.newer() as z:self.assertEqual(len(self.extractor(z)['unit_tests']()),15)
    def test_all_215_headers_reextract_and_every_old_field_is_retained(self):
        with self.newer() as z,zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as oldz:
            old=json.loads(oldz.read('declaration-inventory.json'))
            new=json.loads(z.read('declaration-inventory-c57.json'))
            self.assertEqual(new['providers'],old['providers'])
            self.assertEqual(len(new['targets']),len(old['targets']))
            count=changed=0;extract=self.extractor(z)['exact_header']
            for a,b in zip(old['targets'],new['targets']):
                self.assertEqual({k:v for k,v in a.items() if k!='declarations'},{k:v for k,v in b.items() if k!='declarations'})
                self.assertEqual(len(a['declarations']),len(b['declarations']))
                for before,after in zip(a['declarations'],b['declarations']):
                    self.assertEqual({k:after[k] for k in before},before)
                    header,boundary=extract(before['sourceCapture'])
                    self.assertEqual(header,after['exactSourceHeader']);self.assertEqual(boundary,after['exactSourceHeaderBoundary'])
                    count+=1;changed+=header!=before['sourceSignature']
            self.assertEqual((count,changed),(215,18))
    def test_exact_18_match_actual_review_and_original_negative_is_retained(self):
        with self.newer() as z,zipfile.ZipFile(BASE/'source-formal-stage4-original16.zip') as review:
            delta=json.loads(z.read('annex-delta-c57.json'))
            differences=json.loads(review.read('signature-annex-findings.json'))['differences']
            expected={(r['path'].split('formal-only/')[-1],r['name']):r for r in differences}
            self.assertEqual((delta['actualHeaderDifferences'],delta['whereDifferences'],delta['equationDifferences']),(18,12,6))
            self.assertEqual(len(delta['changes']),18)
            for row in delta['changes']:
                r=expected.pop((row['path'].split('formal-only/')[-1],row['name']))
                self.assertEqual(row['exactSourceHeader'],r['actualSourceHeader'])
                self.assertEqual(row['oldSourceSignature'],r['C49Signature'])
                self.assertEqual(row['boundary'],r['boundary'])
            self.assertEqual(expected,{})
            self.assertEqual(json.loads(review.read('typed-findings.json'))['findings'][0]['status'],'OPEN_IN_PINNED_C49_ANNEX')
    def test_reconstruction_inverse_is_exact_and_flat_artifacts_are_original(self):
        with self.newer() as z,zipfile.ZipFile(BASE/'decoder-c49-publicsafe-original19.zip') as oldz:
            delta=json.loads(z.read('annex-delta-c57.json'));text=z.read('reconstruction.md').decode()
            note=delta['reconstructionAddedLineage'];self.assertTrue(text.endswith(note));text=text[:-len(note)]
            self.assertEqual(len(delta['reconstructionDescriptionReplacements']),3)
            for row in reversed(delta['reconstructionDescriptionReplacements']):
                self.assertEqual(text.count(row['new']),1);text=text.replace(row['new'],row['old'])
            self.assertEqual(text.encode(),oldz.read('reconstruction.md'))
            self.assertEqual(z.read('packet.json'),(BASE/'decoder-c57-packet.json').read_bytes())
            self.assertEqual(z.read('reconstruction.md'),(BASE/'decoder-c57-reconstruction.md').read_bytes())
    def test_nine_actual_decoder_wrappers_match_opaque_control_and_payloads(self):
        with self.newer() as z:
            control=json.loads(z.read('opaque-control.json'))
            bindings={r['module']:r['binding_sha256'] for r in control['bindings']}
            names=[n for n in z.namelist() if n.endswith('.decoder-c57.json')]
            self.assertEqual(len(names),9)
            root=BASE.parents[2]
            for name in names:
                raw=z.read(name);row=json.loads(raw)
                self.assertEqual(row['role'],'decoder');self.assertTrue(row['source_blind'])
                self.assertEqual(row['identity'],'/root/robin_c49_current_formal_decoder')
                self.assertEqual(row['binding_sha256'],bindings.pop(row['module']))
                self.assertEqual(SHA((root/row['packet_path']).read_bytes()),row['packet_sha256'])
                self.assertEqual(SHA((root/row['artifact_path']).read_bytes()),row['artifact_sha256'])
                self.assertEqual((BASE/'decoder-c57'/name).read_bytes(),raw)
            self.assertEqual(bindings,{})
if __name__=='__main__':unittest.main()
