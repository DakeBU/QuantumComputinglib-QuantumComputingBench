"""Consumer sealed regressions; finite diagnostics never formal acceptance."""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from saved_action import (MeasuredWork, Interval, finite_trig, outward, terminal_readout,
    action_chain, literal_embedding, literal_residual, validate_chain, parse_saved,
    stage_surrogates, audit_fixture, independent_saved_replay, physical_word, amplitude,
    LimitReached, CAPS, load_fixture)
from generate_fixture import generate
from mps_core_probe import TT
from qr_residual import sqrt_upper

FIXTURE = HERE / 'fixture-n3-k1-L1'


def exact_poly(x, degree, sine):
    # Independent literal factorial/power sum, not producer's recurrence.
    import math
    return sum((F((-1)**((i-1)//2 if sine else i//2), math.factorial(i)) * x**i
                for i in range(degree+1) if i % 2 == (1 if sine else 0)), F())


class SavedActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.qchain, cls.dchain = audit_fixture(FIXTURE)
        cls.manifest = json.loads((FIXTURE/'manifest.json').read_text())
        cls.qasm = (FIXTURE/'saved.qasm').read_bytes()
        cls.gates, _ = parse_saved(cls.qasm, cls.manifest, MeasuredWork())

    def test_actual_same_return_saved_plan_full_action(self):
        p = json.loads((FIXTURE/'producer.json').read_text())
        self.assertEqual(p['compile_mps_calls'], 1)
        self.assertEqual(p['certified_scaled_return_calls'], 1)
        self.assertTrue(p['same_returned_object_compiler_input'])
        self.assertTrue(p['C_D_unchanged_by_compiler_byte_check'])
        self.assertEqual(p['observed_calls']['compiler_repeated_right_canonicalize'], 1)
        self.assertEqual(p['observed_calls']['complete_isometry'], 3)
        self.assertEqual(self.result['instructions'], 456)
        self.assertEqual(self.result['full_terminal_bond_labels'], 4)
        self.assertEqual(len(self.qchain), 5)
        self.assertEqual([s['count'] for s in self.result['stages']], [184, 168, 104])
        self.assertLess(self.result['candidate_bound_float_diagnostic'], 1e-11)
        self.assertFalse(self.result['target_renormalized'])
        self.assertEqual(self.result['formalGate'], 'OPEN')
        self.assertEqual(self.result['executableRoot'], 'OPEN')

    def test_primary_consumer_has_no_dense_state_input(self):
        with mock.patch.object(TT, 'small_dense_diagnostic', side_effect=AssertionError('no dense')):
            result, _, _ = audit_fixture(FIXTURE)
        self.assertFalse(result['dense_constructor_or_checker_input'])
        self.assertEqual(result['work']['peak_local_matrix_entries'], 64)
        self.assertEqual(result['work']['visited_core_pairs'], 15)

    def test_independent_qiskit_saved_parser_replay(self):
        r = independent_saved_replay(FIXTURE, self.qchain, self.dchain)
        self.assertLess(r['saved_to_literal_D_euclidean_diagnostic'], 1e-11)
        self.assertLess(r['saved_to_surrogate_euclidean_diagnostic'], 1e-11)
        self.assertFalse(r['phase_alignment'])
        # Exact local crossGram agrees with tiny word enumeration as a diagnostic.
        dense_q = sum(((amplitude(self.qchain, physical_word(i, 3, 2)) -
                       amplitude(self.dchain, physical_word(i, 3, 2)))**2 for i in range(32)), F())
        self.assertEqual(dense_q, F(self.result['literal_residual']['residual_squared']))

    def test_deterministic_normal_producer_fixture_bytes(self):
        with tempfile.TemporaryDirectory() as t:
            output = Path(t)/'fresh'
            generated = generate(output)
            self.assertEqual(generated['fixture_sha256'], self.result['fixture_sha256'])
            with self.assertRaisesRegex(ValueError, 'refuse overwriting'):
                generate(output)

    def test_missing_extra_and_hash_mutants_fail_closed(self):
        for mutant in ('missing', 'extra', 'hash'):
            with self.subTest(mutant=mutant), tempfile.TemporaryDirectory() as t:
                p = Path(t)/'copy'
                shutil.copytree(FIXTURE, p)
                if mutant == 'missing':
                    (p/'returned.json').unlink()
                elif mutant == 'extra':
                    (p/'unclaimed.json').write_text('{}')
                else:
                    (p/'saved.qasm').write_bytes(self.qasm + b'\n')
                with self.assertRaises(ValueError):
                    load_fixture(p, MeasuredWork())

    def test_parser_instruction_and_angle_mutants(self):
        first_ry = next(i for i, g in enumerate(self.gates) if g[0] == 'ry')
        lines = self.qasm.decode().splitlines()
        mutants = [lines[:-1], lines + ['ry(0) q[0];']]
        for token in ('NaN', 'pi', '1e999', '0.0'):
            changed = lines.copy()
            wire = self.gates[first_ry][2]
            changed[3+first_ry] = f'ry({token}) q[{wire}];'
            mutants.append(changed)
        for altered in mutants:
            qasm = ('\n'.join(altered)+'\n').encode()
            manifest = copy.deepcopy(self.manifest)
            manifest['qasm_sha256'] = hashlib.sha256(qasm).hexdigest()
            with self.assertRaises(ValueError):
                parse_saved(qasm, manifest, MeasuredWork())

    def test_bad_stage_spans_readout_and_wires_rejected(self):
        for mutant in ('start', 'count', 'reuse', 'missing', 'a'):
            m = copy.deepcopy(self.manifest)
            if mutant == 'start': m['stage_spans'][1]['start'] += 1
            elif mutant == 'count': m['stage_spans'][0]['count'] += 1
            elif mutant == 'reuse': m['stage_spans'][1]['data_wire'] = 2
            elif mutant == 'missing': m['stage_spans'].pop()
            elif mutant == 'a': m['ancillas'] = 5
            with self.subTest(mutant=mutant), self.assertRaises(ValueError):
                parse_saved(self.qasm, m, MeasuredWork())
        # Valid plan-shaped manifest with a wrong physical data wire rejects chronology.
        m = copy.deepcopy(self.manifest)
        lines = self.qasm.decode().splitlines()
        i = next(i for i,g in enumerate(self.gates) if g[0]=='ry')
        m['gates'][i][2] = 0
        binary = float.fromhex(m['gates'][i][1])
        lines[3+i] = f'ry({binary:.17g}) q[0];'
        qasm = ('\n'.join(lines)+'\n').encode()
        m['qasm_sha256'] = hashlib.sha256(qasm).hexdigest()
        with self.assertRaisesRegex(ValueError, 'cross-stage'):
            parse_saved(qasm, m, MeasuredWork())

    def test_valid_rebound_action_mutants_change_residual(self):
        # Intentional semantic adversaries, not acceptance of modified provenance.
        for mutant in ('angle', 'sign', 'order'):
            gates = self.gates.copy()
            i = next(i for i,g in enumerate(gates) if g[0]=='ry' and g[1])
            if mutant == 'angle': gates[i] = ('ry', gates[i][1]+F(1,2), gates[i][2])
            elif mutant == 'sign': gates[i] = ('ry', -gates[i][1], gates[i][2])
            else:
                count = self.manifest['stage_spans'][0]['count']
                gates[:count] = list(reversed(gates[:count]))
            w = MeasuredWork()
            centers, _, _ = stage_surrogates(gates, self.manifest, w)
            chain = action_chain(centers, 2, w)
            residual = literal_residual(chain, self.dchain, w)
            with self.subTest(mutant=mutant):
                self.assertGreater(float(F(residual['residual_upper'])), 1e-5)

    def test_all_terminal_labels_endian_and_ancilla_excitation(self):
        tail = terminal_readout(2)
        for label in range(4):
            head = [[[F(label==j) for j in range(4)], [F() for _ in range(4)]]]
            chain = [head] + tail
            validate_chain(chain, MeasuredWork())
            for b in range(4):
                self.assertEqual(amplitude(chain, [0,(b>>1)&1,b&1]), F(label==b))
        self.assertEqual(terminal_readout(0), [])
        # Ancilla MSB/LSB swap preserves dimensions but changes the literal action.
        centers, _, _ = stage_surrogates(self.gates, self.manifest, MeasuredWork())
        moved = copy.deepcopy(centers)
        # Flip terminal low ancilla on final stage, retain every B sector.
        moved[-1] = [centers[-1][i ^ 1] for i in range(8)]
        w = MeasuredWork()
        chain = action_chain(moved, 2, w)
        residual = literal_residual(chain, self.dchain, w)
        self.assertGreater(float(F(residual['residual_upper'])), 1.4)
        garbage = sum((amplitude(chain, physical_word(i,3,2))**2 for i in range(8,32)), F())
        self.assertGreater(float(garbage), .99)
        # A dimension-valid swapped terminal readout is a semantic error.
        wrong_tail = terminal_readout(2)
        wrong_tail[0] = [[[F() for _ in range(2)] for _ in range(2)] for _ in range(4)]
        for label in range(4):
            wrong_tail[0][label][label % 2][label // 2] = F(1)
        wrong_readout = chain[:3] + wrong_tail
        validate_chain(wrong_readout,MeasuredWork())
        self.assertGreater(float(F(literal_residual(chain,wrong_readout,MeasuredWork())['residual_upper'])),1.4)
        # Naive global-MSB-first reading is NOT the data-first phi bijection.
        word = [int(x) for x in '10101']
        self.assertNotEqual(float(amplitude(self.qchain, word)), float(amplitude(self.qchain, physical_word(int('10101',2),3,2))))
        # A complete routing bond is mandatory; terminal projection cannot validate.
        projected = copy.deepcopy(self.qchain[:3])
        with self.assertRaisesRegex(ValueError, 'scalar terminal'):
            validate_chain(projected, MeasuredWork())

    def test_literal_target_not_renormalized_and_signed(self):
        unnormalized = [[[[F(2)], [F()]]]]
        unit = [[[[F(1)], [F()]]]]
        r = literal_residual(unit, unnormalized, MeasuredWork())
        self.assertEqual(F(r['literal_D_gram']), 4)
        self.assertEqual(F(r['residual_squared']), 1)
        negative = [[[[F(-1)], [F()]]]]
        self.assertEqual(F(literal_residual(unit, negative, MeasuredWork())['residual_squared']), 4)

    def test_zero_deficient_tall_and_invalid_rational_cores(self):
        zero = [[[[F()], [F()]]]]
        self.assertEqual(F(literal_residual(zero, zero, MeasuredWork())['residual_squared']), 0)
        tall = [ [[[F(1),F(0),F(0)], [F(0),F(0),F(0)]]],
                 [[[F(1)],[F(0)]], [[F(0)],[F(0)]], [[F(0)],[F(0)]]] ]
        self.assertEqual(F(literal_residual(tall,tall,MeasuredWork())['residual_squared']),0)
        for chain in ([], [[[[1],[0]]]], [[[[F(1),F(0)],[F(0)]]]], tall[:1]):
            with self.assertRaises((ValueError, TypeError)):
                validate_chain(chain, MeasuredWork())

    def test_empty_stage_and_no_ancillas(self):
        manifest = {'schema_version':1,'n':1,'ancillas':0,'stage_spans':[{'start':0,'count':0,'data_wire':0}]}
        w = MeasuredWork()
        centers, stages, sigma = stage_surrogates([], manifest, w)
        chain = action_chain(centers,0,w)
        self.assertEqual(amplitude(chain,[0]),1)
        self.assertEqual(amplitude(chain,[1]),0)
        self.assertEqual(sigma,0)
        self.assertEqual(stages[0]['count'],0)

    def test_sigma_product_not_unjustified_sum(self):
        etas = [F(s['eta']) for s in self.result['stages']]
        product = F(1)
        for eta in etas: product *= 1+eta
        self.assertEqual(F(self.result['sigma_product_bound']),product-1)
        self.assertGreater(product-1,sum(etas,F()))
        # Two nonunitary factors need the cross term: 1.1^2-1=.21>.2.
        self.assertGreater((1+F(1,10))**2-1,2*F(1,10))

    def test_taylor_membership_algorithm_and_caps(self):
        import math
        for x in (F(0),F(1,3),F(-8),F(8),F(19,10)):
            sine, cosine, radius = finite_trig(x,MeasuredWork())
            self.assertEqual(radius,abs(x)**97/math.factorial(97))
            for enclosure,is_sine in ((sine,True),(cosine,False)):
                lowpoly = exact_poly(x,96,is_sine)
                self.assertLessEqual(enclosure.lo, lowpoly-radius)
                self.assertGreaterEqual(enclosure.hi, lowpoly+radius)
                # Independent higher-order rational polynomial discriminator only.
                self.assertLessEqual(enclosure.lo, exact_poly(x,128,is_sine))
                self.assertGreaterEqual(enclosure.hi, exact_poly(x,128,is_sine))
        for x, degree, bits in ((F(9),96,80),(F(1),129,80),(F(1),96,81)):
            with self.assertRaises(LimitReached): finite_trig(x,MeasuredWork(),degree,bits)
        enclosure = outward(Interval(F(-1,3),F(2,3)),MeasuredWork())
        self.assertLessEqual(enclosure.lo,F(-1,3))
        self.assertGreaterEqual(enclosure.hi,F(2,3))

    def test_directed_sqrt_zero_ties_nonsquares(self):
        for q in (F(0),F(1),F(1,4),F(2),F(1,10**50)):
            r,_=sqrt_upper(q,80,MeasuredWork())
            self.assertGreaterEqual(r*r,q)
            if r: self.assertLess((r-F(1,2**80))**2,q)


if __name__=='__main__':
    unittest.main()
