"""Exact static decoder evidence and its deliberately open acceptance boundary."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()

class StaticTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads((ROOT/'reports/lean-433-migration/c32-static-decoder-transport.json').read_bytes())
        cls.raw=(ROOT/cls.receipt['bundle']).read_bytes()
        with zipfile.ZipFile(ROOT/cls.receipt['bundle']) as z:
            cls.names=z.namelist();cls.files={n:z.read(n) for n in cls.names}

    def test_exact_eleven_original_members_and_seal(self):
        self.assertEqual(sha(self.raw),self.receipt['bundle_sha256'])
        self.assertEqual(len(self.names),11)
        self.assertEqual(len(set(self.names)),11)
        self.assertEqual(set(self.names),{r['member'] for r in self.receipt['members']})
        for row in self.receipt['members']:
            self.assertEqual(sha(self.files[row['member']]),row['sha256'])
            self.assertEqual(len(self.files[row['member']]),row['bytes'])
        seal=json.loads(self.files['seal.json'])
        freeze=json.loads(self.files['freeze.json'])
        self.assertEqual(sha(self.files['seal.json']),freeze['seal_sha256'])
        self.assertEqual(freeze['seal_sha256'],'e36ee8c1f2a996b9f859042329a675966ee419c0646b225c2faf2e5b08c1e809')
        for row in seal['artifacts']:
            if row['publicsafe']:
                self.assertEqual(sha(self.files[row['path']]),row['sha256'])

    def test_exact_allowlist_no_private_script_or_host_path(self):
        allow=json.loads(self.files['publicsafe-allowlist.json'])
        self.assertEqual(set(self.names),set(allow['allowed']))
        self.assertEqual(len(allow['excluded']),3)
        self.assertTrue(all(r['path'] not in self.names for r in allow['excluded']))
        for name,data in self.files.items():
            self.assertNotIn('/',name);self.assertNotIn('\\',name)
            for forbidden in (b'C:\\Users\\',b'C:/Users/',b'D:\\Users\\',b'D:/Users/',b'/home/runner/',b'github_pat_',b'ghp_'):
                self.assertNotIn(forbidden,data)

    def test_current_three_target_and_three_config_pins(self):
        context=json.loads(self.files['context-binding.json'])
        self.assertEqual(len(context['target_modules']),3)
        self.assertEqual([r['declarations'] for r in context['target_modules']],[45,7,5])
        pins=context['target_modules']+context['toolchain_and_manifest']
        self.assertEqual(len(pins),6)
        for row in pins:
            data=(ROOT/row['path']).read_bytes()
            self.assertEqual((sha(data),len(data)),(row['sha256'],row['bytes']))
        self.assertEqual(sha(self.files['formal-context.md']),context['input_packet']['sha256'])

    def test_current_supplement_pins_are_ranges_not_whole_file_read_claims(self):
        rows=json.loads(self.files['supplemental-bindings.json'])
        self.assertEqual(len(rows),7)
        for row in rows:
            data=(ROOT/row['path']).read_bytes()
            self.assertEqual((sha(data),len(data)),(row['whole_file_sha256'],row['whole_file_bytes']))
            self.assertGreaterEqual(row['start_line'],1)
            self.assertLessEqual(row['end_line'],len(data.decode().splitlines()))
            self.assertIn('does not imply whole file read',row['claim'])

    def test_complete_static_inventory_with_explicit_non_native_status(self):
        rows=json.loads(self.files['inventory.json'])
        self.assertEqual(len(rows),57)
        self.assertEqual(len({r['id'] for r in rows}),57)
        self.assertEqual(sum(r['kind']=='def' for r in rows),13)
        self.assertEqual(sum(r['kind']=='theorem' for r in rows),44)
        self.assertEqual(sum(r['visibility'].startswith('private source declaration') for r in rows),4)
        for row in rows:
            self.assertEqual(row['elaboration_status'],'not run')
            self.assertTrue(row['statement_source'])
            self.assertTrue(row['proof_or_body_source_and_trailing_comments'])
            self.assertIn(row['semantic_record'].split('#')[1].encode(),self.files['reconstruction.md'])

    def test_no_implicit_source_agreement_or_family_certificate(self):
        r=self.receipt
        for key in ('nativeAccepted','scientific_ROOT','main_admission','purified'):
            self.assertFalse(r[key])
        for key in ('sourceAgreement','publicationBinding','axiomPolicyPass'):
            self.assertIsNone(r[key])
        self.assertIn('not yet rebased',r['natural_successor_boundary'])
        self.assertEqual(json.loads(self.files['seal.json'])['state'],'STATIC_FROZEN_NOT_KERNEL_ACCEPTED')

if __name__=='__main__':unittest.main()
