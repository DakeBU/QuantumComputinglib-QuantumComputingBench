"""Reproducible fixed-cap supplier failure, not a theorem impossibility."""
from fractions import Fraction
import json
from pathlib import Path
import sys
import unittest

PRECISION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRECISION / "offset-entry-v2"))
from checked_entry import offset_hermite_tt_checked
from offset_source import offset_hermite_tt
from mps_core_probe import ceil_fraction, left_cutoff, pi_interval


def adversarial_length():
    low, high = pi_interval(512)
    return Fraction(2) / (low + high)


def exact_attempt_records(length):
    records = []
    for terms in range(8, 513, 8):
        lo, hi = pi_interval(terms)
        assert lo < 1 / length < hi
        lower = Fraction(2) - Fraction(2) / (lo * length)
        upper = Fraction(2) - Fraction(2) / (hi * length)
        clamp = lambda x: max(0, min(2, ceil_fraction(x)))
        records.append({"terms": terms, "lower_negative": lower < 0,
                        "upper_positive": upper > 0,
                        "clamped_ceil": [clamp(lower), clamp(upper)]})
    return records


class CutoffCapTests(unittest.TestCase):
    def test_legal_positive_rational_has_exact_straddling_at_every_attempt(self):
        length = adversarial_length()
        self.assertGreater(length, 0)
        records = exact_attempt_records(length)
        self.assertEqual(len(records), 64)
        self.assertTrue(all(r["lower_negative"] and r["upper_positive"] and
                            r["clamped_ceil"] == [0, 1] for r in records))

    def test_actual_frozen_cutoff_fails_closed(self):
        with self.assertRaisesRegex(ArithmeticError, "did not separate the cutoff"):
            left_cutoff(2, adversarial_length())

    def test_actual_old_and_checked_entries_propagate_failure(self):
        for constructor in (offset_hermite_tt, offset_hermite_tt_checked):
            with self.subTest(constructor=constructor.__name__):
                with self.assertRaisesRegex(ArithmeticError, "did not separate the cutoff"):
                    constructor(2, 0, adversarial_length())


def witness():
    length = adversarial_length()
    record = {"task": "SP-HERMITE-POLY-002", "n": 2, "k": 0,
              "L_rule": "2/(pi_low(512)+pi_high(512))",
              "L_input_bits": [length.numerator.bit_length(), length.denominator.bit_length()],
              "attempts": exact_attempt_records(length),
              "classification": "IMPLEMENTATION_FAILED",
              "scope": "Fixed512-term executable cutoff supplier; not a mathematical Hermite impossibility",
              "global_epsilon_certificate": False}
    try:
        left_cutoff(2, length)
    except ArithmeticError as error:
        record["actual_exception"] = str(error)
    else:
        raise AssertionError("Frozen fixed-cap failure unexpectedly changed")
    return record


if __name__ == "__main__":
    if "--witness" in sys.argv:
        print(json.dumps(witness(), indent=2))
    else:
        unittest.main()
