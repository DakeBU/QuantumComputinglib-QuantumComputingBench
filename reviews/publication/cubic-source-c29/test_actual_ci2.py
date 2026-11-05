"""Actual frozen CI2 bytes and honest trust boundary; not publication admission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda p: json.loads(p.read_bytes())
sha = lambda raw: hashlib.sha256(raw).hexdigest()


class ActualCI2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = load(ROOT/'reports/lean-433-migration/c29-actual-ci2-runtime.json')
        cls.archive = ROOT/cls.receipt['archive']
        with zipfile.ZipFile(cls.archive) as archive:
            cls.files = {name:archive.read(name) for name in archive.namelist()}

    def test_exact_actual_archive_and_all_38_members(self):
        self.assertEqual(sha(self.archive.read_bytes()),self.receipt['archive_sha256'])
        self.assertEqual(len(self.files),38)
        self.assertEqual(set(self.files),{r['path'] for r in self.receipt['files']})
        for row in self.receipt['files']:
            self.assertEqual(sha(self.files[row['path']]),row['sha256'])
            self.assertEqual(len(self.files[row['path']]),row['bytes'])

    def test_actual_native_exit_codes_and_real_process_handles(self):
        calls = self.receipt['actual_calls']
        self.assertEqual([r['label'] for r in calls],['03-fixture-compile','04-fixture-probe','05-target','06-probe-v4'])
        self.assertEqual(len({r['PID'] for r in calls}),4)
        for call in calls:
            self.assertGreater(call['PID'],0)
            self.assertEqual(call['exitCode'],0)
            self.assertFalse(call['timedOut'])
            observed = json.loads(self.files[call['label']+'.result.json'])
            self.assertEqual(observed['PID'],call['PID'])
            self.assertEqual(observed['stdoutSHA256'],call['stdoutSHA256'])
        self.assertEqual(calls[2]['PID'],7559)

    def test_original_strict_validator_on_actual_ci2_stream(self):
        package = ROOT/'tools/cubic_c29_diagnostic'
        spec = importlib.util.spec_from_file_location('actual_c29_original',package/'validate-output.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        result = module.validate(load(package/'expected-roots.json'),self.files['06-probe-v4.stdout.raw.sanitized.txt'].decode(),0)
        self.assertEqual((result['explicitRoots'],result['privateRoots']),(319,50))

    def test_new_validator_rejects_real_old_metadata_only_stream(self):
        package = ROOT/'tools/cubic_c29_diagnostic'
        spec = importlib.util.spec_from_file_location('actual_c29_v2',package/'validate-output-v2.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with self.assertRaises(ValueError):
            module.validate(load(package/'expected-roots.json'),self.files['06-probe-v4.stdout.raw.sanitized.txt'].decode(),0)

    def test_nine_native_axioms_are_not_hidden_or_auto_whitelisted(self):
        union = self.receipt['explicit_recursive_axiom_union_observed']
        native = [name for name in union if '._native.native_decide.' in name]
        self.assertEqual(len(native),9)
        self.assertEqual(len(union),12)
        links = load(HERE/'runtime-ci2/nine-native-axiom-source-links.json')
        self.assertEqual({r['actualNativeAxiom'] for r in links},set(native))
        source = (ROOT/'QuantumBlockEncoding/CubicStatePreparation.lean').read_text(encoding='utf-8').splitlines()
        for row in links:
            self.assertEqual(source[row['nativeDecideCallsite']['line']-1],row['nativeDecideCallsite']['text'])
            self.assertIsNone(row['axiomPolicyPass'])
            self.assertTrue(row['actualExplicitConsumers'])

    def test_observed_opaque_bodies_do_not_imply_whole_target_axiom_free(self):
        opaque = self.receipt['opaque_observations']
        self.assertEqual(len(opaque),7)
        for row in opaque:
            self.assertEqual(row['actualKind'],'opaqueInfo')
            self.assertTrue(row['actualHasValueAllowOpaque'])
            self.assertEqual(row['axioms'],[])
            self.assertFalse(row['selfOccursInAxioms'])
        packet = load(HERE/'runtime-ci2/runtime-packet.json')
        self.assertFalse(packet['axiomBoundary']['axiomFree'])
        self.assertFalse(packet['wholeTargetTrustClosed'])
        self.assertEqual(packet['generated']['observedCount'],450)

    def test_all_diagnostics_preserve_nonacceptance(self):
        for receipt in (self.receipt,load(HERE/'runtime-ci2/runtime-packet.json'),load(HERE/'ci3-packet.json')):
            for key in ('sourceAgreement','publicationBinding','axiomPolicyPass'):
                self.assertIsNone(receipt[key])
            self.assertFalse(receipt['nativeAccepted'])
            self.assertFalse(receipt['scientific_ROOT'])

    def test_selected_successor_artifacts_and_tool_pins_are_exact(self):
        receipt = load(ROOT/'reports/lean-433-migration/c29-ci3-integration-receipt.json')
        for row in receipt['files']+receipt['exact_selected_audit_artifacts']:
            if row['path'] == 'tools/cubic_c29_diagnostic/runner.py':
                # Historical CI3 receipt stays immutable; verify its preserved predecessor.
                raw = (HERE/'two-signatures-v1/runner-ci3-before-supplement.py.txt').read_bytes()
                current = (ROOT/row['path']).read_bytes()
                successor = load(ROOT/'reports/lean-433-migration/c29-two-signatures-integration.json')
                current_pin = next(r for r in successor['files'] if r['path'] == row['path'])
                self.assertEqual(sha(current),current_pin['sha256'])
                before = "        verify_pins(project, pins['projectInputs'])\n        if any(path.exists() for path in absent_roots):"
                append = ("        # Changed fingerprint: fill only two observed CI3 pretty-signature omissions.\n"
                          "        # The original 319+450 validator/driver and fresh target artifact remain unchanged.\n"
                          "        from supplemental_types_v1 import run_supplemental\n"
                          "        checked_two_types = run_supplemental(package, driver, private, env, lean, output,\n"
                          "                                             native_call, sha, verify_pins, write_json)\n")
                original = raw.decode()
                self.assertEqual(original.count(before),1)
                after = original.replace(before,append+before)
                anchor = "                      generatedActualFields=checked['generatedActualFieldsCollected'],\n"
                self.assertEqual(after.count(anchor),1)
                after = after.replace(anchor,anchor+"                      supplementalTypeTexts=checked_two_types['status'],\n")
                self.assertEqual(current,after.encode())
            else:
                raw = (ROOT/row['path']).read_bytes()
            self.assertEqual(sha(raw),row['sha256'])
            self.assertEqual(len(raw),row['bytes'])
        self.assertEqual(len(receipt['files']),8)
        self.assertEqual(len(receipt['exact_selected_audit_artifacts']),7)
        self.assertFalse(receipt['nativeAccepted'])


if __name__ == '__main__':
    unittest.main()
