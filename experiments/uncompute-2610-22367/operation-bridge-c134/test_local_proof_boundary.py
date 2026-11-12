"""Transport/regression checks, not a replacement for Lean or source review."""
import hashlib,json,re,unittest
from pathlib import Path
from zipfile import ZipFile
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

class LocalProofBoundary(unittest.TestCase):
    def test_actual_source_and_no_placeholders(self):
        raw=(HERE/'OperationBridge.lean').read_bytes()
        self.assertEqual(sha(raw),'2f1150d4c6c48c24e0d62155e94316004efb72ed70ce9d69105ba1a737d64ce3')
        self.assertIsNone(re.search(rb'\b(sorry|admit|axiom|unsafe)\b',raw))
        self.assertTrue(raw.startswith(b'import StatementProbe\n'))
        self.assertEqual(len(re.findall(rb'^theorem ',raw,re.M)),7)

    def test_actual_compile_and_audit_same_output(self):
        c=json.loads((HERE/'compile-observation.json').read_bytes())
        a=json.loads((HERE/'root-audit-observation.json').read_bytes())
        self.assertEqual((c['exit_code'],a['exit_code']),(0,0))
        self.assertFalse(c['timeout'])
        self.assertEqual(c['source_sha256'],a['source_sha256'])
        self.assertEqual(c['olean_sha256'],a['olean_sha256'])
        self.assertEqual(c['olean_sha256'],'57045ea17141c13e38ef3144b0ecfcd7407215f27ccef5ba1d3b6313f2b184b8')
        self.assertTrue(c['exact_single_proof_block_delta_verified'])
        self.assertTrue(c['inherited_compiled_providers'])
        self.assertFalse(c['old_three_attempt_cap_modified'])
        for flag in ['new_source_assumptions','production_changed','independent_review_complete','full_repository_gate','source_admission','scientific_ROOT']:
            self.assertFalse(c[flag])

    def test_exported_axioms_and_sealed_signature(self):
        text=(HERE/'root-types-and-axioms.txt').read_text(encoding='utf-8')
        rows=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text,re.S)
        self.assertEqual(len(rows),7)
        for name,axioms in rows:
            self.assertTrue(name.startswith('ASPBE.Uncompute.MBU.OperationBridge.'))
            self.assertEqual(set(x.strip() for x in axioms.split(',')),{'propext','Classical.choice','Quot.sound'})
        sealed=(HERE.parent/'operation-bridge-c128/sealed-root-signature.txt').read_text(encoding='utf-8').strip()
        source=(HERE/'OperationBridge.lean').read_text(encoding='utf-8')
        self.assertIn(sealed,source)

    def test_original_three_failures_immutable(self):
        idx=json.loads((HERE/'failed-attempts-index.json').read_bytes())
        archive=HERE/idx['archive']
        self.assertEqual(sha(archive.read_bytes()),idx['sha256'])
        self.assertEqual(idx['old_attempt_cap'],3)
        self.assertFalse(idx['old_attempt_cap_modified'])
        with ZipFile(archive) as z:
            self.assertEqual(len(z.namelist()),9)
            for n,item in idx['members'].items():
                b=z.read(n)
                self.assertEqual((len(b),sha(b)),(item['bytes'],item['sha256']))
            for i in range(1,4):
                row=json.loads(z.read(f'attempt-{i}/attempt-{i}.json'))
                self.assertEqual(row['exit_code'],1)
                self.assertIsNone(row['olean_sha256'])
                self.assertEqual(sha(z.read(f'attempt-{i}/OperationBridge.lean')),row['source_sha256'])

    def test_isolated_probe_is_not_whole_root(self):
        row=json.loads((HERE/'controlled-leaf-result.json').read_bytes())
        self.assertEqual(row['exit_code'],0)
        self.assertNotIn('theorem compiledAndCleanupKernel_eq',(HERE/'controlled-leaf-probe.lean').read_text())
        readme=(HERE/'README.md').read_text(encoding='utf-8')
        for boundary in ['NOT_ADMITTED','pending','not a physical','Hermite root','Rollback']:
            self.assertIn(boundary,readme)

if __name__=='__main__':unittest.main()
