"""Independent static extractor audit remains distinct from native admission."""
import hashlib
import json
from pathlib import Path
import re
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[3]
class ExtractorAddendumTests(unittest.TestCase):
    def test_exact_six_file_bundle(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-extractor-source-addendum-transport.json').read_bytes())
        data=(ROOT/r['bundle']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),r['bundle_sha256'])
        with zipfile.ZipFile(ROOT/r['bundle']) as z:
            self.assertEqual(len(z.namelist()),6)
            self.assertEqual(set(z.namelist()),{x['name'] for x in r['members']})
            for row in r['members']:
                raw=z.read(row['name'])
                self.assertEqual(len(raw),row['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
                self.assertIsNone(re.search(rb'(?:[A-Za-z]:[\\/](?:Users|qb261009)|/home/runner/|github_pat_|ghp_)',raw))

    def test_provenance_discrepancy_and_native_boundary_preserved(self):
        r=json.loads((ROOT/'reports/lean-433-migration/c29-extractor-source-addendum-transport.json').read_bytes())
        with zipfile.ZipFile(ROOT/r['bundle']) as z:
            s=json.loads(z.read('extractor-source-addendum-v1-seal.json'))
        self.assertEqual(s['inputFiles'],88)
        self.assertEqual(s['discrepancies'][0]['id'],'D1')
        self.assertFalse(s['discrepancies'][0]['exactHistoricalExecutedRunnerByteIdentityEstablished'])
        self.assertFalse(s['boundaries']['nativeAxiomsRemoved'])
        self.assertFalse(s['boundaries']['nativeTCBPolicyAuthorized'])
        for field in ('nativeAccepted','scientific_ROOT','canonicalAdmission','mainCompletion'):
            self.assertFalse(s[field])
        self.assertIsNone(s['sourceAgreement']);self.assertIsNone(s['axiomPolicyPass'])
        self.assertEqual(s['requiredAdditionalDriverSourceReadRequest'],'RESOLVED_AT_PRECISE_IMPLEMENTATION_SOURCE_SCOPE')

if __name__=='__main__':unittest.main()
