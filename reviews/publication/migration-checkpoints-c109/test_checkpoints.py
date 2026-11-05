"""Exact checkpoint integrity; never source truth, kernel replay or admission."""
import hashlib
import json
from pathlib import Path
import unittest
from zipfile import ZipFile

BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()

class ReviewCheckpointTests(unittest.TestCase):
    def index(self): return json.loads((BASE/'index.json').read_bytes())

    def test_exact_original_archives_and_members(self):
        index=self.index()
        self.assertEqual(len(index['archives']),11)
        self.assertEqual(sum(len(r['members']) for r in index['archives']),106)
        for row in index['archives']:
            data=(BASE/row['archive']).read_bytes()
            self.assertEqual(sha(data),row['sha256'])
            with ZipFile(BASE/row['archive']) as z:
                self.assertEqual(set(z.namelist()),set(row['members']))
                for name,member in row['members'].items():
                    raw=z.read(name)
                    self.assertEqual(sha(raw),member['sha256'])
                    self.assertEqual(len(raw),member['bytes'])

    def test_old_partial_and_whole_decoder_freezes_are_distinct(self):
        with ZipFile(BASE/'robin-c98-whole-formal-decoder-original.zip') as z:
            old=json.loads(z.read('seal.json'))
            self.assertEqual(old['status'],'INCOMPLETE_FROZEN_BEFORE_SOURCE_RELEASE')
        with ZipFile(BASE/'robin-c98-whole-formal-continuation2-original.zip') as z:
            new=json.loads(z.read('seal.json'))
            self.assertEqual(new['state'],'FROZEN_BEFORE_SOURCE_RELEASE')
            self.assertTrue(new['coverage']['complete'])
            self.assertEqual(new['coverage']['lines'],[1,26985])
            self.assertFalse(new['source_release'])
            self.assertFalse(new['lean_execution'])

    def test_actual_whole_inventory_parent_recomposition_scope(self):
        rows=self.index()['C98_independent_text_recomposition']
        self.assertEqual(len(rows),8)
        self.assertTrue(all(r['recompose_exact'] for r in rows))
        target=next(r for r in rows if r['path']=='QuantumBlockEncoding/RobinMatrix.lean')
        self.assertEqual(target['commands'],688)
        self.assertEqual(target['sha256'],'17735bc5f3a1d42fa16d9cf55d33237af432178b19c6946cc2294d7d41e61de8')

    def test_gaussian_successor_accepts_only_exposed_source_obligations(self):
        with ZipFile(BASE/'uncompute-c96-gaussian-successor-review-original.zip') as z:
            seal=json.loads(z.read('SEAL.json'))
            self.assertEqual(seal['independent_verdict'],'ACCEPTED_FOR_BOUNDED_T1_T5_SOURCE_TOPOLOGY_REPAIR_ONLY')
            self.assertEqual(seal['remaining_T1_T5_defects'],[])
            self.assertFalse(seal['source_circuit_refuted_or_route_retired'])
        index=self.index()
        self.assertFalse(index['source_or_runtime_or_publication_admission'])
        self.assertFalse(index['scientific_ROOT'])
        self.assertFalse(index['PURIFIED'])

    def test_hbi_source_and_own_formal_frozen_before_actual_decoder_comparison(self):
        with ZipFile(BASE/'hbi-c100-decoder-comparison-original.zip') as z:
            seal=json.loads(z.read('COMPARISON_SEAL.json'))
            self.assertTrue(seal['chronology']['own_formal_freeze_precedes_actual_decoder_release'])
            self.assertTrue(seal['chronology']['source_and_own_interpretations_not_amended_after_decoder'])
            self.assertEqual(seal['actual_comparison']['all_target_declarations_compared'],125)
            self.assertEqual(seal['actual_comparison']['leading_named_binders'],490)
            self.assertFalse(seal['actual_comparison']['source_graph_approved'])

if __name__=='__main__': unittest.main()
