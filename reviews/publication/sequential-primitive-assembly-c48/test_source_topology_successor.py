"""Genuine source-topology successor acceptance does not approve formal code."""
import hashlib,json,unittest,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
SHA=lambda b:hashlib.sha256(b).hexdigest()
class SourceTopologySuccessorTests(unittest.TestCase):
    def test_exact_seven_files_manifest_and_limited_source_only_verdict(self):
        with zipfile.ZipFile(BASE/'source-topology-stage3-successor-public7.zip') as z:
            self.assertEqual(len(z.namelist()),7)
            self.assertEqual(set(z.namelist()),set(json.loads(z.read('publicsafe-allowlist.json'))['files']))
            self.assertEqual(SHA(z.read('stage3-source-seal.json')),'930811a0c6d9e78c84261b14df4cadb47ac53729debff569e34f36f36c4ee42f')
            self.assertEqual(SHA(z.read('manifest.json')),'d3d301fe80c6acc435e66f2cb82cbdccd8c8bbe8b01a14926ad2eb59c0cbc5d0')
            manifest=json.loads(z.read('manifest.json'))
            for row in manifest['payloads']:self.assertEqual(SHA(z.read(row['file'])),row['sha256'])
            report=z.read('successor-review.md').decode()
            self.assertIn('ACCEPTED_SOURCE_TOPOLOGY_ONLY',report)
            self.assertIn('Formal comparison is not entered',' '.join(report.split()))
            self.assertIn('old graph and its adverse Stage 2',report)
if __name__=='__main__':unittest.main()
