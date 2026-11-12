import hashlib
import json
from pathlib import Path
import re
import unittest
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
load = lambda name: json.loads((HERE / name).read_bytes())


class HBICheckpointTests(unittest.TestCase):
    def test_exact_actor_original_archive(self):
        index = load('decoder-index.json')
        self.assertEqual(sha((HERE / index['archive']).read_bytes()), index['sha256'])
        with ZipFile(HERE / index['archive']) as archive:
            self.assertEqual(len(archive.namelist()), 12)
            self.assertEqual(set(archive.namelist()), set(index['members']))
            for name, digest in index['members'].items():
                self.assertEqual(sha(archive.read(name)), digest)
            self.assertEqual(sha(archive.read('seal.json')), 'af0922d26e6f9fe1b403e32143320ea369a17fd42abd446cebb98840ff07e455')

    def inventory(self):
        with ZipFile(HERE / load('decoder-index.json')['archive']) as archive:
            return json.loads(archive.read('declarations.json'))

    def test_complete125_literal_header_body_recomposition(self):
        data = self.inventory()
        parts = [row['header'] + row['body'] for row in data['declarations']]
        self.assertEqual(len(parts), 125)
        self.assertEqual(sha((data['prefix'] + ''.join(parts) + data['suffix']).encode()),
            'cf4fcd8e410b4c103e8e45a569e878404de64e1f2d3775dad0a99004990627f1')
        for row, text in zip(data['declarations'], parts):
            self.assertEqual(sha(text.encode()), row['source_sha256'])

    def test_all_leading_groups_precede_result_or_body(self):
        for row in self.inventory()['declarations']:
            header = row['header'].encode('utf-16-le')
            limit = row['result_colon_relative_utf16']
            if limit is None:
                limit = row['body_relative_utf16']
            for group in row['leading_binder_groups']:
                start, end = group['relative_utf16_start'], group['relative_utf16_end_exclusive']
                self.assertLessEqual(end, limit)
                self.assertEqual(header[start * 2:end * 2].decode('utf-16-le'), group['source'])

    def test_root_has_no_result_subexpressions_as_premises(self):
        root = next(row for row in self.inventory()['declarations'] if row['name'] == 'hermiteKernel_eq_sample')
        self.assertEqual([group['names'] for group in root['leading_binder_groups']],
            [['k', 'n'], ['L'], ['hL'], ['bits'], ['hbits']])
        self.assertEqual(sum(len(group['names']) for row in self.inventory()['declarations']
            for group in row['leading_binder_groups']), 490)

    def test_matched_success_is_focused_and_narrow(self):
        observed = load('focused-compile-observation.json')
        self.assertEqual([row['exit_code'] for row in observed['records']], [0, 0])
        self.assertEqual(observed['limit_MiB'], 3072)
        self.assertEqual(observed['root_axioms'], ['propext', 'Classical.choice', 'Quot.sound'])
        self.assertNotIn('sorryAx', observed['exact_path_free_root_stdout'])
        self.assertEqual(sha(observed['exact_path_free_root_stdout'].encode()), observed['records'][-1]['stdout_sha256'])
        for field in ('full_repository_Lean_gate', 'final_module_admission', 'Hermite_finitebit_ROOT'):
            self.assertFalse(observed[field])

    def test33_current_formal_bindings_not_source_acceptance(self):
        data = load('current-formal-bindings.json')
        self.assertEqual(len(data['files']), 33)
        self.assertTrue(all(row['formal_bytes_equal'] for row in data['files']))
        self.assertEqual(data['target_raw_sha256'], load('focused-compile-observation.json')['source_sha256'])
        self.assertEqual(data['target_formal_sha256'], self.inventory()['formal_sha256'])
        self.assertFalse(data['independent_reviewer_approval'])
        self.assertFalse(data['production_admission'])

    def test_privacy_scan_distinguishes_TeX_from_host_paths(self):
        pattern = rb'(?<![A-Za-z0-9])[A-Za-z]:(?:/|\\(?:Users|qb261009|Windows|Program Files|[A-Za-z0-9_. -]+\\))'
        self.assertIsNone(re.search(pattern, rb'\forall b:\mathrm{Bool}'))
        for value in (b'C:/private/file', b'D:\\Users\\private', b'E:\\scratch\\file'):
            self.assertIsNotNone(re.search(pattern, value))
        index = load('decoder-index.json')
        with ZipFile(HERE / index['archive']) as archive:
            for name in archive.namelist():
                self.assertIsNone(re.search(pattern, archive.read(name)), name)

    def test_fresh_decoder_not_retroactive_old_repair_or_admission(self):
        index = load('decoder-index.json')
        self.assertEqual(index['decoder'], 'hbi_fresh_whole_decoder_c97')
        self.assertEqual(index['formal_source_relative_review'], 'NOT_YET_PERFORMED')
        self.assertFalse(index['old_C67_negative_packet_modified'])
        self.assertFalse(index['final_admission'])


if __name__ == '__main__':
    unittest.main()
