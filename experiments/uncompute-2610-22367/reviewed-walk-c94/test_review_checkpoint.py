"""Evidence regressions; no compiler, simulator, network or acceptance writes."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from zipfile import ZipFile
from formal_redaction import verify

HERE = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
load = lambda name: json.loads((HERE / name).read_bytes())


class ReviewCheckpointTests(unittest.TestCase):
    def test_exact_archives_and_all_original_members(self):
        index = load('packet-index.json')
        self.assertEqual(len(index['archives']), 7)
        self.assertEqual(sum(len(row['members']) for row in index['archives']), 51)
        for row in index['archives']:
            self.assertEqual(sha((HERE / row['archive']).read_bytes()), row['sha256'])
            with ZipFile(HERE / row['archive']) as archive:
                self.assertEqual(set(archive.namelist()), set(row['members']))
                for name, digest in row['members'].items():
                    self.assertEqual(sha(archive.read(name)), digest)

    def test_all_published_text_is_host_path_and_token_free(self):
        forbidden = rb'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]{20,}'
        for path in HERE.iterdir():
            if path.is_file() and path.suffix != '.zip':
                self.assertIsNone(re.search(forbidden, path.read_bytes()), path.name)
        for row in load('packet-index.json')['archives']:
            with ZipFile(HERE / row['archive']) as archive:
                for name in archive.namelist():
                    self.assertIsNone(re.search(forbidden, archive.read(name)), name)

    def test_file_specific_raw_to_formal_derivation(self):
        observed = load('execution-observation.json')
        with ZipFile(HERE / 'reviewed-formal-inputs-original.zip') as formal, ZipFile(
                HERE.parent / 'upstream-divsteps-inputs-64b5a13-original.zip') as upstream:
            for row in observed['source_mask_bindings']:
                path = row['path']
                raw = ((HERE.parent / 'active-walk-c88/WalkRecovery.lean').read_bytes()
                       if path == 'WalkRecovery.lean' else upstream.read('lean/divsteps/' + path))
                self.assertEqual(sha(raw), row['raw_sha256'])
                self.assertEqual(sha(formal.read(path)), row['formal_sha256'])
                self.assertEqual(verify(raw, formal.read(path))['comment_regions'], row['comment_regions'])

    def test_exact_formal_inventory(self):
        with ZipFile(HERE / 'reviewed-formal-inputs-original.zip') as archive:
            original = json.loads(archive.read('formal-inputs.json'))
            self.assertEqual(len(original['files']), 7)
            for row in original['files']:
                self.assertEqual(sha(archive.read(row['path'])), row['formal_sha256'])

    def test_success_is_narrow_and_failed_attempt_remains_failed(self):
        observed = load('execution-observation.json')
        self.assertEqual([row['exit_code'] for row in observed['records']], [0, 0, 0, 0])
        self.assertEqual(observed['root_axioms'], ['propext', 'Classical.choice', 'Quot.sound'])
        self.assertFalse(observed['local_publication_admission'])
        self.assertFalse(observed['full_repository_Lean_gate'])
        self.assertFalse(observed['quantum_circuit_or_finitebit_resource_certificate'])
        self.assertFalse(observed['clean_transitive_Mathlib_or_TCB_build'])
        self.assertEqual(observed['initial_C88_failure']['exit_code'], 1)
        self.assertTrue(observed['initial_C88_failure']['sorryAx_in_failed_output'])

    def test_exact_source_free_root_stdout(self):
        observed = load('execution-observation.json')
        raw = (HERE.parent / 'active-walk-c88/actual-success-output.txt').read_bytes()
        self.assertEqual(sha(raw), observed['root_stdout_sha256'])
        self.assertEqual(raw.decode(), observed['exact_root_stdout'])
        self.assertNotIn('sorryAx', observed['exact_root_stdout'])

    def test_genuine_distinct_review_stages_and_no_final_admission(self):
        with ZipFile(HERE / 'uncompute-c87-bridge-execution-binding-original.zip') as archive:
            seal = json.loads(archive.read('seal.json'))
            self.assertEqual(seal['actual_agent'], '/root/uncompute_appendix_topology_c87')
            self.assertEqual(seal['file_specific_correspondence_verdict'], 'PASS_EXACT_AUTHORIZED_GIT_RAW_MASK_STAGE_BINDINGS')
            self.assertFalse(seal['final_publication_or_admission_approval'])
            self.assertFalse(seal['historical_C91_initial_empty_cache_independently_witnessed'])
        with ZipFile(HERE / 'formal-bridge-c89-decoder-original.zip') as archive:
            decoder = json.loads(archive.read('manifest.json'))
            self.assertNotEqual(seal['actual_agent'], decoder['decoder_identity'])

    def test_gaussian_remains_source_only_and_unreviewed(self):
        with ZipFile(HERE / 'uncompute-c92-gaussian-source-first-original.zip') as archive:
            manifest = json.loads(archive.read('MANIFEST.json'))
            self.assertEqual(manifest['status'], 'SOURCE_ONLY_FROZEN_UNREVIEWED')
            self.assertEqual(manifest['independent_review'], 'PENDING')
            self.assertEqual(manifest['proof_or_resource_certification'], 'NONE')

    def test_migration_discriminator_preserves_both_failures(self):
        report = json.loads((HERE.parents[2] / 'reports/lean-433-migration/c95-main-hbi-compatibility-discriminator.json').read_bytes())
        self.assertEqual([row['exit_code'] for row in report['attempts']], [3221226505, 1])
        self.assertEqual([row['limit_MiB'] for row in report['attempts']], [1536, 3072])
        self.assertEqual([row['line'] for row in report['second_error_locations']], [302, 560, 767, 806, 903, 984])
        self.assertTrue(report['unchanged_source_between_attempts'])

    def test_migration_discriminator_is_not_full_main_or_math_obstruction(self):
        report = json.loads((HERE.parents[2] / 'reports/lean-433-migration/c95-main-hbi-compatibility-discriminator.json').read_bytes())
        self.assertIn('contribution Lean4.33 caches', report['dependency_context'])
        for field in ('full_repository_Lean_gate', 'main_migration_complete',
                      'scientific_obstruction', 'production_admission', 'production_sources_changed'):
            self.assertFalse(report[field])


if __name__ == '__main__':
    unittest.main()
