"""Packet integrity regressions; passing is not publication or compiler admission."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOAD = lambda path: json.loads(path.read_text(encoding='utf-8'))
SHA = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


class StagingIntegrityTests(unittest.TestCase):
    def test_lossless_formula_coverage_and_old_negative(self):
        latest = LOAD(HERE / 'parent-source-coverage-v4.json')
        source = ROOT / latest['source_path']
        blocks = latest['source_paragraphs']
        self.assertEqual(len(blocks), 42)
        self.assertEqual('\n\n'.join(r['exact_text'] for r in blocks).encode(), source.read_bytes())
        for row in blocks:
            self.assertEqual(hashlib.sha256(row['exact_text'].encode()).hexdigest(), row['sha256'])
        failed = LOAD(HERE / 'parent-source-coverage-v2.json')
        self.assertEqual(len(failed['source_paragraphs']), 34)
        self.assertNotEqual('\n\n'.join(r['exact_text'] for r in failed['source_paragraphs']).encode(), source.read_bytes())

    def test_actual_witness_premises_and_open_gaps(self):
        graph = LOAD(HERE / 'parent-graph-views-v3.json')['views']['source-construction-graph']
        nodes = {r['id']: r for r in graph['nodes']}
        edges = {r['heads'][0]: r for r in graph['hyperedges']}
        self.assertEqual(len(edges), 20)
        for edge in edges.values():
            self.assertEqual(edge['logic'], 'AND')
            self.assertTrue(set(edge['tails'] + edge['heads']) <= set(nodes))
        for number in (2, 8, 9, 10, 20):
            self.assertIn('premise:F-separated-through-I', edges[f'source:S{number}']['tails'])
        for number in (8, 10):
            self.assertIn('premise:G-separated-through-J', edges[f'source:S{number}']['tails'])
        gaps = {r['id'] for r in nodes.values() if r['kind'] == 'SOURCE_GAP'}
        self.assertEqual(len(gaps), 3)
        self.assertEqual({r['to'] for r in graph['source_gap_links']}, gaps)
        for name in gaps:
            self.assertEqual(nodes[name]['status'], 'OPEN')
            self.assertFalse(nodes[name]['mathematical_proof_node'])
        old = LOAD(HERE / 'author-graph-views.json')['views']['source-construction-graph']
        rank = next(e for e in old['hyperedges'] if e['heads'] == ['source:S2'])
        self.assertNotIn('premise:F-separated-through-I', rank['tails'])

    def test_formal_context_display_repair(self):
        old = LOAD(HERE / 'author-formal-context.json')
        new = LOAD(HERE / 'author-formal-context-v2.json')
        self.assertEqual(old['files'], new['files'])
        self.assertEqual([r['source_exact'] for r in old['declarations']], [r['source_exact'] for r in new['declarations']])
        for row in new['declarations']:
            body = row['definition_or_proof_source']
            self.assertTrue(row['source_exact'].endswith(body))
            self.assertEqual(row['source_exact'][:-len(body)].rstrip(), row['statement_source'])
        for row in new['files']:
            self.assertEqual(''.join(row['full_source_lines']).encode(), (ROOT / row['path']).read_bytes())

    def test_independent_frozen_decoder_and_later_bridge(self):
        base = HERE / 'decoder-c24'
        self.assertEqual(SHA(base / 'freeze.json'), 'f6f012795dac69f04b009d8299e00a488b8b7ebde5334f4704d66b63b9842050')
        for row in LOAD(base / 'freeze.json')['artifacts']:
            self.assertEqual(SHA(base / row['path']), row['sha256'])
        self.assertEqual(SHA(base / 'later-binding-bridge-v5.json'), '197fe44da53e7328181c3080364fb7244cb279fde09f0f1c871f7be4607c4964')
        bridge = LOAD(base / 'later-binding-bridge-v5.json')
        self.assertEqual(set(bridge['changed_fields']), {'binding_sha256', 'supersedes'})
        for version in (4, 5):
            self.assertEqual(SHA(ROOT / bridge[f'packet_v{version}_path']), bridge[f'packet_v{version}_sha256'])
        packet = LOAD(HERE / 'author-decoder-packet-v5.json')
        self.assertEqual(SHA(ROOT / packet['formal_context_path']), packet['formal_context_sha256'])
        self.assertEqual(bridge['opaque_binding'], packet['binding_sha256'])

    def test_frozen_reviewer_and_attested_transports_are_present(self):
        registry = LOAD(ROOT / 'website/research/publications.json')['records']
        record = next(r for r in registry if r['module'] == 'QuantumBlockEncoding/HermiteCutRank.lean')
        link = record['wrapper_transport_attestation']
        attestation = ROOT / link['path']
        self.assertEqual(SHA(attestation), link['sha256'])
        self.assertEqual(link['sha256'], '5a892157463f96cf711d12b75b39e718e4003d327dc06a38564d4e00964e5df8')
        att = LOAD(attestation)
        self.assertEqual(att['verdict'], 'accepted')
        for key in ('parent_wrapper_bindings', 'canonical_reviewer_originals',
                    'canonical_decoder_originals_and_bridges', 'canonical_packet_history'):
            for name, expected in att[key].items():
                self.assertEqual(SHA(ROOT / name), expected, name)
        frozen = HERE / 'reviewer-c24/freeze.json'
        self.assertEqual(SHA(frozen), '5aa82c2c56dd2376d0d8b6e68609b9b468c55e74d40b29edd38df448c1f8aef3')
        for row in LOAD(frozen)['artifacts']:
            self.assertEqual(SHA(frozen.parent / row['path']), row['sha256'])
        self.assertEqual(record['binding_sha256'], att['binding_sha256'])
        self.assertFalse(record['main_admission'])
        self.assertFalse(record['scientific_ROOT'])

    def test_prospective_binding_and_existing_canonical_records(self):
        sys.path.insert(0, str(ROOT))
        from website.scripts import check_research_publications as checker
        current = checker.load
        row = LOAD(HERE / 'author-source-row-candidate.json')['source']
        def prospective(root, name):
            data = current(root, name)
            if name == 'website/research/sources.json':
                present = [r for r in data['sources'] if r['id'] == row['id']]
                if present:
                    self.assertEqual(present, [row])
                else:
                    data['sources'].append(row)
            return data
        with patch.object(checker, 'load', prospective):
            record = LOAD(HERE / 'publication-candidate-v4.json')
            self.assertEqual(checker.binding_digest(ROOT, record), record['binding_sha256'])
        self.assertEqual(record['binding_sha256'], '3b82211ff24790ab53188f090ce383142cad2d7df706943309071d56605b1296')
        inventory = {r['fullName']: r for r in LOAD(ROOT / 'web/library/declarations.json')['declarations']}
        for record in LOAD(ROOT / 'website/research/publications.json')['records']:
            checker.validate_record(ROOT, record, inventory)


if __name__ == '__main__':
    unittest.main()
