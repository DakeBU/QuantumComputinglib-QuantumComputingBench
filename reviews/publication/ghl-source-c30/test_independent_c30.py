"""Frozen independent WIP evidence integrity; never compiler or semantic acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
load = lambda path: json.loads(path.read_bytes())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()


class IndependentC30Tests(unittest.TestCase):
    def test_exact_independent_transports_and_distinct_roles(self):
        receipt = load(HERE/'parent-independent-transport-c30.json')
        self.assertEqual(len(receipt['reviewer_files']), 7)
        self.assertEqual(len(receipt['decoder_files']), 9)
        self.assertNotEqual(receipt['reviewer_identity'], receipt['decoder_identity'])
        self.assertNotEqual(receipt['original_author_identity'], receipt['reviewer_identity'])
        self.assertFalse(receipt['native_acceptance'])
        self.assertIsNone(receipt['sourceAgreement'])
        for row in receipt['reviewer_files'] + receipt['decoder_files']:
            self.assertEqual(sha(ROOT/row['path']), row['sha256'])
            self.assertEqual((ROOT/row['path']).stat().st_size, row['bytes'])

    def test_source_first_chronology_is_preserved(self):
        first = load(HERE/'reviewer-c30/phase1-seal.json')
        supplement = load(HERE/'reviewer-c30/phase1-addendum-seal.json')
        static = load(HERE/'reviewer-c30/phase2-static-seal.json')
        self.assertFalse(first['scope']['implementation_read'])
        self.assertFalse(first['scope']['phase2_authorized'])
        self.assertFalse(supplement['authorization']['formal_comparison_authorized'])
        self.assertTrue(static['source_first_order_preserved'])
        self.assertFalse(static['acceptance_boundary']['elaborated_types_or_kernel_proof_terms_observed'])
        for row in static['immutable_prior_review_records']:
            self.assertEqual(sha(HERE/'reviewer-c30'/row['path'].removeprefix('$REVIEWER/')), row['sha256'])

    def test_static_graph_finding_is_exact_and_not_math_refutation(self):
        static = load(HERE/'reviewer-c30/phase2-static-seal.json')
        finding = static['finding']
        self.assertEqual(finding['id'], 'STATIC-GRAPH-01')
        self.assertFalse(finding['actual_arithmetic_theorems_refuted'])
        self.assertFalse(finding['Lean_or_source_mathematical_statement_repair_requested'])
        repairs = {row['edge_id']: row['add_explicit_tail'] for row in finding['repairs']}
        self.assertEqual(repairs, {
            'construction:conditional-witness': 'result:transpose-matrix',
            'construction:swap-permutation': 'result:layout-data',
            'construction:indicator-permutation': 'result:layout-data',
        })

    def test_formal_source_reconstruction_is_not_compiled_evidence(self):
        frozen = load(HERE/'decoder-c30/phase1formal-freeze.json')
        pending = load(HERE/'decoder-c30/compile-type-axiom-pending.json')
        self.assertEqual(frozen['allExplicitDeclarations'], 405)
        self.assertEqual(frozen['privateDeclarations'], 2)
        self.assertEqual(frozen['leanInvocationCount'], 0)
        self.assertEqual(pending['leanInvocationCount'], 0)
        for key in ('compiledSignatures', 'recursiveAxiomClosure', 'privateNameResolution'):
            self.assertIsNone(pending[key])
        self.assertIsNone(frozen['sourceAgreement'])
        self.assertIsNone(frozen['publicationBinding'])
        self.assertFalse(frozen['publicationAccepted'])

    def test_integer_collision_is_finite_diagnostic_not_lean_proof(self):
        diagnostic = load(HERE/'decoder-c30/exact-integer-reconstruction-diagnostic.json')
        n = diagnostic['p']['n']
        kappa = diagnostic['p']['kappa']
        self.assertEqual((n, kappa), (3, 7))
        size = 2**n
        low = 2**(1+n)
        high = 2**(1+2*n)
        offsets = [size-2, size-1, 0, 1, 2, size-3, 3]
        def image(index):
            row = index//2 % size
            slot = index//low % size
            address = ((offsets[slot] if slot < 7 else 0) + row) % size
            return index % low + address*low + index//high*high
        self.assertEqual(diagnostic['distinctCleanSources'], [32, 112])
        self.assertEqual([image(j) for j in diagnostic['distinctCleanSources']], [0, 0])
        self.assertEqual(diagnostic['globalSourceMembership'], [True, False])
        self.assertIn('NOT Lean certified', diagnostic['layer'])


if __name__ == '__main__':
    unittest.main()
