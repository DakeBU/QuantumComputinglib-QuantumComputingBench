"""Metadata transport is not formal correspondence or scientific acceptance."""
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
class MetadataV2TransportTests(unittest.TestCase):
    def test_exact42_members_and_seal_not_admission(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c32-metadata-v2-transport.json').read_bytes())
        self.assertEqual(hashlib.sha256((ROOT/r['archive']).read_bytes()).hexdigest(),r['archive_sha256'])
        with zipfile.ZipFile(ROOT/r['archive']) as z:
            self.assertEqual(len(z.namelist()),42)
            self.assertEqual(set(z.namelist()),{m['name'] for m in r['members']})
            for m in r['members']:
                raw=z.read(m['name']);self.assertEqual(len(raw),m['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(),m['sha256'])
        self.assertFalse(r['nativeAccepted']);self.assertFalse(r['main_admission'])
        self.assertIsNone(r['sourceAgreement']);self.assertEqual(r['validate_record_calls'],0)

    def test_parent_integrity_and_isolation_is_not_native_or_review(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c32-metadata-v2-transport.json').read_bytes())
        p=r['parent_replay'];self.assertEqual(p['exit_code'],0);self.assertTrue(p['all_pass'])
        self.assertEqual((p['integrity_checks'],p['inherited_strategies'],p['source_isolation_tests']),(62,13,9))
        self.assertEqual(r['actual_native_calls'],0);self.assertFalse(r['scientific_ROOT']);self.assertFalse(r['PURIFIED'])

if __name__=='__main__':unittest.main()
