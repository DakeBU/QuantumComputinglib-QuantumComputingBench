"""Integrity of a scoped local proof; not source truth or compiler replay."""
import hashlib
import json
import re
import unittest
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
SHA = lambda raw: hashlib.sha256(raw).hexdigest()

class ActiveWalkCheckpointTests(unittest.TestCase):
    def report(self):
        return json.loads((BASE / 'observation.json').read_bytes())

    def test_exact_preproof_signature_is_the_successful_root(self):
        report = self.report()
        source = (BASE / 'WalkRecovery.lean').read_bytes()
        self.assertEqual(SHA(source), report['successful_source_sha256'])
        statement = (BASE / 'statement.md').read_text()
        header = statement.split('```lean\n', 1)[1].split('\n```', 1)[0]
        self.assertIn(header + ' := by', source.decode())
        self.assertIn('invariant_zWalk hp x t', source.decode())
        self.assertIn('rw [zWalk_succ, if_neg hactive]', source.decode())

    def test_failed_attempt_remains_distinct_and_unaccepted(self):
        first, final = self.report()['attempts']
        self.assertEqual(first['exit_code'], 1)
        self.assertIn('unsolved goals', first['diagnostic'])
        self.assertFalse(first['accepted'])
        self.assertNotEqual(first['source_sha256'], final['source_sha256'])
        self.assertEqual(SHA((BASE / 'attempt-1-source.lean').read_bytes()), first['source_sha256'])
        self.assertEqual(final['exit_code'], 0)

    def test_actual_successful_type_and_axiom_output(self):
        text = (BASE / 'actual-success-output.txt').read_text()
        self.assertEqual(SHA(text.encode()), self.report()['success_stdout_sha256'])
        self.assertIn('ASPBE.Uncompute.recover_zWalk_active (p x :', text)
        self.assertIn("depends on axioms: [propext, Classical.choice, Quot.sound]", text)
        self.assertNotIn('sorryAx', text)
        self.assertNotIn('Lean.ofReduceBool', text)

    def test_bounded_actual_runtime_context_and_reserve(self):
        report = self.report()
        self.assertIn('version 4.33.0', report['observed_Lean'])
        for row in report['attempts']:
            self.assertGreater(row['seconds'], 0)
            self.assertEqual(row['limit_MiB'], 1536)
            self.assertEqual(row['reserve_MiB'], 2048)
            self.assertGreaterEqual(row['observed_available_MiB'], 3584)
        self.assertEqual(report['runtime_measurement'], 'local subprocess.run elapsed; not launch-order worker collection time')

    def test_original_review_archives_are_exact_not_resealed(self):
        report = self.report()
        self.assertEqual(len(report['archives']), 5)
        for row in report['archives']:
            path = BASE / row['path']
            self.assertEqual(SHA(path.read_bytes()), row['sha256'])
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()), {m['path'] for m in row['members']})
                for member in row['members']:
                    raw = archive.read(member['path'])
                    self.assertEqual(SHA(raw), member['sha256'])
                    self.assertEqual(len(raw), member['bytes'])

    def test_source_review_and_metadata_warning_do_not_close_formal_admission(self):
        report = self.report()
        self.assertEqual(report['source_topology_status'], 'ACCEPT_WITH_EXISTING_EXPLICIT_BOUNDARIES')
        self.assertEqual(report['upstream_decoder_context_status'], 'ERRATUM_REQUIRED_FOR_CONTEXT_INTERPRETATION')
        self.assertEqual(report['new_bridge_independent_review'], 'IN_PROGRESS_NOT_ACCEPTED')
        self.assertEqual(report['upstream_commit'], '64b5a13aa249f1360846657392e6c66817b26d0f')

    def test_no_scientific_or_runtime_promotion(self):
        report = self.report()
        self.assertEqual(report['status'], 'PROVED_LOCALLY_ISOLATED_NOT_ADMITTED')
        for key in ('production_Lean_changed', 'publication_registry_changed', 'production_controller_changed',
                    'scoring_changed', 'full_paper_formalized', 'quantum_circuit_certificate',
                    'finitebit_resource_certificate', 'Hermite_ROOT', 'scientific_ROOT', 'PURIFIED'):
            self.assertFalse(report[key], key)

    def test_public_payloads_have_no_host_paths_or_credentials(self):
        items = [(p.name, p.read_bytes()) for p in BASE.iterdir() if p.is_file() and p.suffix != '.zip']
        for path in BASE.glob('*.zip'):
            with zipfile.ZipFile(path) as archive:
                items.extend((n, archive.read(n)) for n in archive.namelist())
        for name, raw in items:
            text = raw.decode('utf-8-sig')
            self.assertIsNone(re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|qb261009)', text), name)
            self.assertNotIn('/' + '/'.join(('home', 'runner')) + '/', text, name)
            self.assertIsNone(re.search(r'(?:github_' + 'pat_|gh' + 'p_)[A-Za-z0-9_]{20,}', text), name)

if __name__ == '__main__':
    unittest.main()
