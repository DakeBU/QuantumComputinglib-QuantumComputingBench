"""Offset/reflected successor of the frozen MPS-02 source supplier.

Polynomial injection uses exact rational interval arithmetic and a stored-dyadic
local error budget. It never forms1 minus a tiny coordinate offset. Rational pi
and exp(-1) enclosures have analytic series justifications, not a Lean proof of
this Python program. Exponential cores and QR/normalizer remain uncertified.
No dense amplitude vector or SVD is a construction input.
"""
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
import math
from pathlib import Path
import sys

import numpy as np

HERMITE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERMITE / "mps"))
from mps_core_probe import TT, direct_sum, left_cutoff, pi_interval
from mps_stable_cores import decimal_fraction, interval_injection_tt, subdivision_matrices


def rational_text(value):
    """Lossless decimal or hex rational; avoid Python's decimal-print cap.

    Certificate storage/serialization is charged by operand bit length. This
    conversion does not silently replace a very small error bound by float0.
    """
    try:
        return str(value)
    except ValueError:
        return hex(value.numerator) + "/" + hex(value.denominator)


def read_rational(text):
    if text.startswith(("0x", "-0x")):
        numerator, denominator = text.split("/")
        return Fraction(int(numerator, 0), int(denominator, 0))
    return Fraction(text)


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        if not isinstance(self.lo, Fraction) or not isinstance(self.hi, Fraction):
            raise TypeError("exact Fraction endpoints required")
        if self.lo > self.hi:
            raise ValueError("reversed enclosure")

    def contains(self, value):
        return self.lo <= value <= self.hi


def convex_interval(a: Interval, b: Interval, t: Interval) -> Interval:
    if not 0 <= t.lo <= t.hi <= 1:
        raise ArithmeticError("convex parameter outside[0,1]")
    lower = [(1 - p) * a.lo + p * b.lo for p in (t.lo, t.hi)]
    upper = [(1 - p) * a.hi + p * b.hi for p in (t.lo, t.hi)]
    return Interval(min(lower), max(upper))


def interval_subdivide(coeff, point, counters):
    row, left, right = list(coeff), [coeff[0]], [coeff[-1]]
    while len(row) > 1:
        counters["interval_convex_updates"] += len(row) - 1
        row = [convex_interval(a, b, point) for a, b in zip(row[:-1], row[1:])]
        left.append(row[0])
        right.append(row[-1])
    return left, list(reversed(right))


def exp_minus_one_interval(terms: int) -> Interval:
    """Alternating exp(-1) series: consecutive partial sums enclose the limit.

    Absolute terms1/m! decrease to0 (the first equality causes no issue).
    This fixed scalar is generated, not an oracle callback or Decimal exp.
    """
    if terms < 2:
        raise ValueError("at least2 Taylor terms required")
    partial = sum((Fraction((-1)**m, math.factorial(m)) for m in range(terms)), Fraction())
    following = partial + Fraction((-1)**terms, math.factorial(terms))
    return Interval(min(partial, following), max(partial, following))


def source_base_weights(k):
    """Literal exact rational weights from the frozen positive source formula."""
    degree = 2 * k + 1
    a = [sum((Fraction(math.comb(k + i - m, k), math.factorial(m))
              for m in range(i + 1)), Fraction()) for i in range(k + 1)]
    return [sum((a[i] * Fraction(math.comb(k - i, r - i), math.comb(degree, r))
                 for i in range(k + 1) if i <= r <= k), Fraction())
            for r in range(degree + 1)]


def source_coefficient_intervals(base, exp_interval):
    degree = len(base) - 1
    return [Interval(exp_interval.lo * base[r] + base[degree - r],
                     exp_interval.hi * base[r] + base[degree - r])
            for r in range(degree + 1)]


def offset_parameters(n, a, b, length, pi_bounds):
    """Rational certified parameter enclosures, never subtracting near1 floats.

    Exact source offset endpoints are u=R*A,v=R*B with R=pi*L,
    A=(N-2b)/N,B=(N-2a)/N. The second restriction parameter is
    z=R*(B-A)/(1-R*A), increasing in R on the certified domain.
    """
    count = 1 << n
    if not 0 <= a < b <= count // 2:
        raise ValueError("included middle interval required")
    A, B = Fraction(count - 2 * b, count), Fraction(count - 2 * a, count)
    rlo, rhi = pi_bounds[0] * length, pi_bounds[1] * length
    u = Interval(rlo * A, rhi * A)
    v = Interval(rlo * B, rhi * B)
    if not 0 < rlo <= rhi or not 0 <= u.lo <= u.hi < 1 or v.hi > 1:
        raise ArithmeticError("rational source offset locus not certified")
    parameter = Interval(rlo * (B - A) / (1 - rlo * A),
                         rhi * (B - A) / (1 - rhi * A))
    if not 0 < parameter.lo <= parameter.hi <= 1:
        raise ArithmeticError("rational source restriction parameter not certified")
    return u, v, parameter


def stored_interval_error(value, interval):
    if not math.isfinite(value):
        raise ArithmeticError("coefficient conversion is nonfinite")
    dyadic = Fraction.from_float(value)
    return max(abs(dyadic - interval.lo), abs(dyadic - interval.hi))


def certified_polynomial_injection(n, k, length, a, b, tolerance,
                                   initial_terms=16, max_refinements=5):
    """Return actual float core entries and exact local rational certificates.

    Tolerance is a COEFFICIENT absolute tolerance, not global state epsilon.
    Adaptive retries cannot beat the stored dyadic resolution; failure is honest.
    Scalar enclosure mathematics/Python equivalence remain a separate Lean gap.
    """
    if not isinstance(length, Fraction) or length <= 0 or k < 0 or n < 1:
        raise ValueError("require physical n>=1,k>=0,positive rational L")
    if not isinstance(tolerance, Fraction) or tolerance <= 0:
        raise ValueError("positive exact rational local tolerance required")
    base = source_base_weights(k)
    counters = {"interval_convex_updates": 0, "adaptive_attempts": 0,
                "coordinate_refinements": 0}
    last_error, last_locus_failure = None, None
    for attempt in range(max_refinements):
        terms = initial_terms * 2**attempt
        counters["adaptive_attempts"] += 1
        bounds = pi_interval(terms)
        try:
            u, v, parameter = offset_parameters(n, a, b, length, bounds)
        except ArithmeticError as error:
            # A coarse pi enclosure may cross1 for a genuinely legal active
            # interval. Refine it; an exhausted cap remains an honest failure.
            last_locus_failure = str(error)
            counters["coordinate_refinements"] += 1
            continue
        coefficients = source_coefficient_intervals(base, exp_minus_one_interval(terms))
        # Reflected source polynomial Q(s)=P(1-s), then reverse the restricted
        # coefficients back so j still increases from a to b.
        _, right = interval_subdivide(list(reversed(coefficients)), u, counters)
        restricted, _ = interval_subdivide(right, parameter, counters)
        intervals = list(reversed(restricted))
        values = np.array([float((x.lo + x.hi) / 2) for x in intervals])
        errors = [stored_interval_error(float(value), interval)
                  for value, interval in zip(values, intervals)]
        last_error = max(errors)
        if last_error <= tolerance:
            certificate = {
                "a": a, "b": b, "n": n, "k": k, "L": rational_text(length),
                "terms": terms, "tolerance": rational_text(tolerance),
                "offset_lower_enclosure": [rational_text(u.lo), rational_text(u.hi)],
                "offset_upper_enclosure": [rational_text(v.lo), rational_text(v.hi)],
                "second_parameter_enclosure": [rational_text(parameter.lo), rational_text(parameter.hi)],
                "coefficient_intervals": [[rational_text(x.lo), rational_text(x.hi)] for x in intervals],
                "stored_dyadics": [rational_text(Fraction.from_float(float(x))) for x in values],
                "coefficient_error_bounds": [rational_text(e) for e in errors],
                "maximum_coefficient_error_bound": rational_text(last_error),
                "max_coefficient_endpoint_bits": max(max(q.numerator.bit_length(), q.denominator.bit_length())
                    for interval in intervals for q in (interval.lo, interval.hi)),
                "counters": counters,
                "certificate_scope": "local polynomial coefficients; analytic pi/exp(-1) enclosures and exact Fraction arithmetic, not whole Python/Lean or global state error",
            }
            return values, certificate
    if last_error is None:
        raise ArithmeticError(f"source offset locus not certified after {max_refinements} refinements: {last_locus_failure}")
    raise ArithmeticError(f"local coefficient tolerance not met after {max_refinements} refinements; last bound={rational_text(last_error)}")


def offset_hermite_tt(n: int, k: int, length: Fraction,
                      coefficient_tolerance=Fraction(1, 10**14)):
    """Actual successor raw TT, sharing frozen cutoff/core/assembly mechanisms."""
    if not isinstance(length, Fraction) or length <= 0 or k < 0 or n < 1:
        raise ValueError("require physical n>=1,k>=0,positive rational L")
    cutoff, cutoff_terms = left_cutoff(n, length)
    degree, count = 2 * k + 1, 1 << n
    digits = math.ceil(n * math.log10(2)) + 90
    certificates = []
    with localcontext() as context:
        context.prec = digits
        terms = max(cutoff_terms, math.ceil((digits + 10) / math.log10(25)))
        pi_low, pi_high = pi_interval(terms)
        radius = decimal_fraction((pi_low + pi_high) / 2) * decimal_fraction(length)
        step = 2 * radius / Decimal(count)
        subdivisions = subdivision_matrices(degree)

        def polynomial_inject(a, b):
            values, certificate = certified_polynomial_injection(
                n, k, length, a, b, coefficient_tolerance, initial_terms=max(16, cutoff_terms))
            certificates.append(certificate)
            return values

        middle, middle_blocks = interval_injection_tt(
            n, cutoff, count // 2, degree + 1,
            lambda offset, bit: subdivisions[bit], polynomial_inject)

        def exponential_inject(a, b):
            # This frozen-style exponential supplier is intentionally NOT
            # covered by the polynomial coefficient certificate.
            last = radius * (Decimal(2 * (b - 1)) / Decimal(count) - 1)
            return np.array([float(last.exp())])

        def left_free(offset, bit):
            value = 1. if bit else float((-step * Decimal(1 << (n - 1 - offset))).exp())
            return np.array([[value]])

        left, left_blocks = interval_injection_tt(n, 0, cutoff, 1, left_free, exponential_inject)
        right_cores = [np.array([0., 1.]).reshape(1, 2, 1)]
        for offset in range(1, n):
            right_cores.append(np.array([1., float((-step * Decimal(1 << (n - 1 - offset))).exp())])
                               .reshape(1, 2, 1))
        raw = direct_sum([(1, left), (1, middle), (1, TT(right_cores))])
    return raw, {
        "candidate": "MPS-02-OFFSET-INTERVAL-SUCCESSOR", "n": n, "k": k, "L": rational_text(length),
        "L_input_bits": [length.numerator.bit_length(), length.denominator.bit_length()],
        "left_cutoff": cutoff, "cutoff_pi_terms": cutoff_terms,
        "nonpolynomial_decimal_digits": digits,
        "bond_bound": 2 * k + 6, "max_bond": raw.max_bond, "core_scalars": raw.scalar_count,
        "middle_dyadic_injections": middle_blocks, "left_dyadic_injections": left_blocks,
        "polynomial_certificates": certificates,
        "dense_constructor_input": False, "dense_svd_used": False,
        "global_epsilon_certificate": False,
        "remaining": ["pi/exp analytic membership and Python refinement in Lean", "cutoff bounded separation",
                      "float subdivision/exponential errors", "QR and absorption", "normalizer and circuit serialization"],
    }
