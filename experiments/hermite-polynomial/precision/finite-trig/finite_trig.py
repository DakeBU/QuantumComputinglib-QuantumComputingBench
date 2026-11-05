"""Exact finite rational Taylor enclosures; no float/transcendental oracle.

The formulas are proved in FiniteTrig.lean. This implementation's Python-to-Lean
refinement is NOT yet proved. A degree cap failure does not refute mathematics.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import factorial
import re


class LimitReached(RuntimeError):
    pass


@dataclass(frozen=True)
class Enclosure:
    argument: Fraction
    degree: int
    sin_center: Fraction
    cos_center: Fraction
    radius: Fraction

    @property
    def sin_bounds(self):
        return self.sin_center - self.radius, self.sin_center + self.radius

    @property
    def cos_bounds(self):
        return self.cos_center - self.radius, self.cos_center + self.radius

    @property
    def width(self):
        return 2 * self.radius


def _rational(value, name):
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be an exact Fraction, not float")
    return value


def exact_decimal(token: str, *, max_chars: int = 4096) -> Fraction:
    """Strict textual decimal semantics, not parsed-binary64 semantics."""
    if not isinstance(token, str):
        raise TypeError("decimal token must be str")
    if len(token) > max_chars:
        raise LimitReached("decimal text cap reached")
    if re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", token) is None:
        raise ValueError("malformed finite decimal token")
    # Charge/reject absurd exponents before Fraction could allocate huge powers.
    exponent = re.search(r"[eE]([+-]?[0-9]+)$", token)
    if exponent and abs(int(exponent.group(1))) > max_chars:
        raise LimitReached("decimal exponent cap reached")
    return Fraction(token)


def at_degree(q: Fraction, n: int) -> Enclosure:
    _rational(q, "q")
    if type(n) is not int or n < 0:
        raise ValueError("degree must be a nonnegative int")
    sin_center = Fraction(0)
    cos_center = Fraction(0)
    term = Fraction(1)
    for i in range(n + 1):
        residue = i % 4
        if residue == 0:
            cos_center += term
        elif residue == 1:
            sin_center += term
        elif residue == 2:
            cos_center -= term
        else:
            sin_center -= term
        term *= q / (i + 1)
    return Enclosure(q, n, sin_center, cos_center, abs(term))


def enclose(q: Fraction, max_width: Fraction, *, max_degree: int = 128) -> Enclosure:
    """First degree 0..cap with exact width <= request, else honest failure."""
    _rational(q, "q")
    _rational(max_width, "max_width")
    if max_width < 0:
        raise ValueError("max_width must be nonnegative")
    if type(max_degree) is not int or max_degree < 0:
        raise ValueError("max_degree must be a nonnegative int")
    sin_center, cos_center, term = Fraction(0), Fraction(0), Fraction(1)
    for n in range(max_degree + 1):
        residue = n % 4
        if residue == 0:
            cos_center += term
        elif residue == 1:
            sin_center += term
        elif residue == 2:
            cos_center -= term
        else:
            sin_center -= term
        term *= q / (n + 1)
        radius = abs(term)
        if 2 * radius <= max_width:
            return Enclosure(q, n, sin_center, cos_center, radius)
    raise LimitReached("Taylor degree cap reached without requested width")


def dyadic_outward(bounds, bits: int = 80):
    """Pure outward rounding. Its enlarged width must be budgeted by consumer."""
    if type(bits) is not int or bits < 0:
        raise ValueError("bits must be a nonnegative int")
    lo, hi = bounds
    _rational(lo, "lower endpoint")
    _rational(hi, "upper endpoint")
    scale = 1 << bits
    lower = (lo.numerator * scale) // lo.denominator
    upper = -((-hi.numerator * scale) // hi.denominator)
    return Fraction(lower, scale), Fraction(upper, scale)


def operand_bits(value: Fraction):
    return max(abs(value.numerator).bit_length(), value.denominator.bit_length())
