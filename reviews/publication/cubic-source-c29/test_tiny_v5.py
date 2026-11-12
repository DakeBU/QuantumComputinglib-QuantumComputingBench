"""Actual small Lean fixture provenance; never evidence of full Cubic closure."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent/'tiny-v5-api'
load = lambda name: json.loads((HERE/name).read_bytes())


class TinyV5Tests(unittest.TestCase):
    def test_raw_and_derived_stream_hashes_are_distinctly_bound(self):
        rows = load('raw-derivation-receipts.json')['files']
        for row in rows:
            raw = (HERE/row['publicRelativePath']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['publicSHA256'])
        result = load('02-fixture-probe-v5.result.json')
        row = next(r for r in rows if r['publicRelativePath']=='02-fixture-probe-v5.stdout.raw.sanitized.txt')
        self.assertEqual(result['stdoutSHA256'], row['rawSHA256'])
        self.assertEqual(row['rawSHA256'], '380ea92b791875a3bc7ebd27b5d1cd45f6931f02944ddb14141c5a8453f08cd4')
        self.assertNotEqual(row['rawSHA256'], row['publicSHA256'])

    def test_actual_fixture_native_success_remains_scoped(self):
        for label, pid in [('01-fixture-compile', 1616), ('02-fixture-probe-v5', 48944)]:
            result = load(label+'.result.json')
            self.assertEqual(result['PID'], pid)
            self.assertEqual(result['exitCode'], 0)
            self.assertFalse(result['timedOut'])
        summary = load('summary.private.json')
        self.assertEqual(summary['LeanInvocations'], 2)
        self.assertFalse(summary['actualCubicCompile'])
        self.assertFalse(summary['actual319Signatures'])
        self.assertFalse(summary['nativeAccepted'])
        self.assertIsNone(summary['sourceAgreement'])

    def test_real_axiom_private_and_opaque_observations_are_retained(self):
        stream = (HERE/'02-fixture-probe-v5.stdout.raw.sanitized.txt').read_text(encoding='utf-8')
        rows = [json.loads(line.split(' ',1)[1]) for line in stream.splitlines() if line.startswith('C29_ROOT_JSON ')]
        self.assertEqual(len(rows), 5)
        by_name = {row['sourceUserName']: row for row in rows}
        self.assertEqual(by_name['Fixture.supplied']['actualKind'], 'axiomInfo')
        self.assertIn('Fixture.supplied', by_name['Fixture.supplied']['axioms'])
        self.assertTrue(by_name['Fixture.hidden']['actualPrivate'])
        self.assertIn('Fixture.supplied', by_name['Fixture.hidden']['axioms'])
        self.assertEqual(by_name['Fixture.sealed']['actualKind'], 'opaqueInfo')
        self.assertTrue(by_name['Fixture.sealed']['actualHasValueAllowOpaque'])
        self.assertTrue(all(not row['nativeAccepted'] for row in rows))


if __name__ == '__main__':
    unittest.main()
