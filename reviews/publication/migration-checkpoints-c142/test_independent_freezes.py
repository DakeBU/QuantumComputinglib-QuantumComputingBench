import base64,hashlib,json,re,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

class IndependentFreezes(unittest.TestCase):
    def test_exact_twentyfour_members(self):
        index=json.loads((HERE/'index.json').read_bytes());count=0
        for row in index['packets']:
            archive=HERE/row['archive']
            self.assertEqual(sha(archive.read_bytes()),row['archive_sha256'])
            with ZipFile(archive) as z:
                self.assertEqual(set(z.namelist()),set(row['members']))
                for name,item in row['members'].items():
                    raw=z.read(name);count+=1
                    self.assertEqual((len(raw),sha(raw)),(item['bytes'],item['sha256']))
                    self.assertIsNone(re.search(rb'(?<![A-Za-z0-9])[A-Za-z]:[\\/]',raw))
                self.assertEqual(sha(z.read('manifest.json')),row['manifest_sha256'])
                self.assertEqual(sha(z.read('seal.json')),row['seal_sha256'])
        self.assertEqual(count,24)
        self.assertFalse(index['source_admission'])
        self.assertFalse(index['original_decoder_allowlist_changed'])

    def test_core_reconstructions_and_identity_are_distinct(self):
        with ZipFile(HERE/'operation-c137-blind-decoder-original.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['decoder_task'],'/root/operation_formal_blind_decoder_c137')
            self.assertEqual(sha(base64.b64decode(z.read('exact/OperationBridge.lean.base64'))),'2f1150d4c6c48c24e0d62155e94316004efb72ed70ce9d69105ba1a737d64ce3')
            declarations=json.loads(z.read('exact-declarations.json'))['files']
            target=next(row for row in declarations if row['path']=='OperationBridge.lean')
            self.assertEqual(len(target['declarations']),19)
        with ZipFile(HERE/'operation-c138-own-formal-review-original.zip') as z:
            seal=json.loads(z.read('seal.json'))
            self.assertEqual(seal['reviewer'],'temporary_and_operation_statement_review_c120')
            self.assertEqual(seal['status'],'OWN_FORMAL_ONLY_FROZEN_STOPPED_BEFORE_ACTUAL_DECODER')

    def test_parent_rehash_is_not_admission(self):
        row=json.loads((HERE/'parent-freeze-rehash.json').read_bytes())
        self.assertEqual(row['formal_input_members'],30)
        self.assertEqual(sum(p['payloads'] for p in row['verified_packets']),20)
        self.assertEqual(row['exact_core_restorations'],3)
        self.assertFalse(row['compilation_or_source_admission'])
        self.assertFalse(row['scientific_ROOT'])

if __name__=='__main__':unittest.main()
