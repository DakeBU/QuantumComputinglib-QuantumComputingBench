"""Uniform local-budget validation; frozen numerical supplier is unchanged.

This optional successor entry does not certify a global state error, source
enclosure or finite-bit runtime. It preserves the constructor's valid returns
and exceptions exactly, while rejecting invalid arguments before computation.
"""
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "offset-source"))
from offset_source import offset_hermite_tt as _frozen_constructor


def offset_hermite_tt_checked(n: int, k: int, length: Fraction,
                             coefficient_tolerance=Fraction(1, 10**14)):
    """Return the original tuple, with no fallback or numerical change.

    coefficient_tolerance is an absolute LOCAL polynomial coefficient budget.
    A successful return is NOT a certificate for an arbitrary global epsilon.
    """
    if type(n) is not int or n < 1 or type(k) is not int or k < 0:
        raise ValueError("require integer physical n>=1 and k>=0")
    if not isinstance(length, Fraction) or length <= 0:
        raise ValueError("positive exact rational L required")
    if not isinstance(coefficient_tolerance, Fraction) or coefficient_tolerance <= 0:
        raise ValueError("positive exact rational local tolerance required")
    return _frozen_constructor(n, k, length, coefficient_tolerance)
