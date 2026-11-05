"""Exact-dyadic, non-enumerating certificate of the actual scaled QR return.

The certificate targets the original STORED raw TT, not ideal source values.
No numerical QR stability/orthogonality premise or dense input is used. The
actual approximate scale product is interpreted literally; its drift is not
replaced by the exact product of factors. Python-to-Lean and source/gate
refinement remain separate obligations.
"""
from dataclasses import dataclass
from fractions import Fraction
import math
from pathlib import Path
import sys

import numpy as np

MPS = Path(__file__).resolve().parents[2] / "mps"
sys.path.insert(0, str(MPS))
from scaled_canonicalize import ScaledNorm, scaled_right_canonicalize


def rational_text(value):
    try:
        return str(value)
    except ValueError:
        return hex(value.numerator) + "/" + hex(value.denominator)


def read_rational(text):
    if text.startswith(("0x", "-0x")):
        a, b = text.split("/")
        return Fraction(int(a, 0), int(b, 0))
    return Fraction(text)


@dataclass
class Work:
    rational_additions: int = 0
    rational_multiplications: int = 0
    rational_divisions: int = 0
    decoded_scalars: int = 0
    max_numerator_bits: int = 0
    max_denominator_bits: int = 0
    stored_core_scalars: int = 0
    peak_environment_scalars: int = 1
    matrix_output_allocations: int = 0
    environment_output_allocations: int = 0
    transpose_index_cell_copies: int = 0
    visited_core_pairs: int = 0
    max_unreduced_numerator_bits_bound: int = 0
    max_unreduced_denominator_bits_bound: int = 0

    def unreduced(self, numerator_bits, denominator_bits):
        # Conservative pre-GCD product/sum bounds, not just reduced outputs.
        # This does not claim a complete trace of Python's Fraction internals.
        self.max_unreduced_numerator_bits_bound = max(
            self.max_unreduced_numerator_bits_bound, numerator_bits)
        self.max_unreduced_denominator_bits_bound = max(
            self.max_unreduced_denominator_bits_bound, denominator_bits)

    def note(self, value):
        self.max_numerator_bits = max(self.max_numerator_bits, abs(value.numerator).bit_length())
        self.max_denominator_bits = max(self.max_denominator_bits, value.denominator.bit_length())
        return value

    def add(self, a, b):
        self.rational_additions += 1
        self.unreduced(max(abs(a.numerator).bit_length() + b.denominator.bit_length(),
                           abs(b.numerator).bit_length() + a.denominator.bit_length()) + 1,
                       a.denominator.bit_length() + b.denominator.bit_length())
        return self.note(a + b)

    def mul(self, a, b):
        self.rational_multiplications += 1
        self.unreduced(abs(a.numerator).bit_length() + abs(b.numerator).bit_length(),
                       a.denominator.bit_length() + b.denominator.bit_length())
        return self.note(a * b)

    def div(self, a, b):
        self.rational_divisions += 1
        self.unreduced(abs(a.numerator).bit_length() + b.denominator.bit_length(),
                       a.denominator.bit_length() + abs(b.numerator).bit_length())
        return self.note(a / b)


def stored_cores(tt, work):
    """Decode each actual binary64 exactly; no array coercion changes input."""
    if not tt.cores:
        raise ValueError("nonempty stored TT required")
    result = []
    previous = 1
    for offset, core in enumerate(tt.cores):
        if not isinstance(core, np.ndarray) or core.dtype != np.dtype(np.float64):
            raise ValueError("actual real float64 stored cores required")
        if core.ndim != 3 or core.shape[1] != 2 or min(core.shape) <= 0:
            raise ValueError("positive compatible binary core dimensions required")
        if core.shape[0] != previous:
            raise ValueError("stored bond mismatch")
        if not np.all(np.isfinite(core)):
            raise ArithmeticError("nonfinite stored core")
        left, _, right = core.shape
        decoded = [[[work.note(Fraction.from_float(float(core[a, bit, b])))
                     for b in range(right)] for bit in range(2)] for a in range(left)]
        work.decoded_scalars += core.size
        work.stored_core_scalars += core.size
        result.append(decoded)
        previous = right
    if previous != 1:
        raise ValueError("scalar terminal boundary required")
    return result


def matrix_product(a, b, work):
    rows, inner, columns = len(a), len(b), len(b[0])
    if any(len(row) != inner for row in a):
        raise ValueError("matrix dimension mismatch")
    result = []
    work.matrix_output_allocations += rows * columns
    for i in range(rows):
        row = []
        for j in range(columns):
            total = Fraction(0)
            for k in range(inner):
                total = work.add(total, work.mul(a[i][k], b[k][j]))
            row.append(total)
        result.append(row)
    return result


def cross_gram(c, d, work):
    """Literal two-product local recurrence, streaming one small environment."""
    if len(c) != len(d):
        raise ValueError("same physical core count required")
    environment = [[Fraction(1)]]
    for a, b in zip(reversed(c), reversed(d)):
        parts = []
        for bit in range(2):
            left = [row[bit] for row in a]
            right_transpose = [list(row) for row in zip(*(row[bit] for row in b))]
            work.transpose_index_cell_copies += len(b) * len(b[0][bit])
            parts.append(matrix_product(matrix_product(left, environment, work),
                                        right_transpose, work))
        environment = [[work.add(x, y) for x, y in zip(first, second)]
                       for first, second in zip(*parts)]
        work.environment_output_allocations += len(environment) * len(environment[0])
        work.peak_environment_scalars = max(work.peak_environment_scalars,
                                            len(environment) * len(environment[0]))
        work.visited_core_pairs += 1
    if len(environment) != 1 or len(environment[0]) != 1:
        raise ValueError("scalar initial boundary required")
    return environment[0][0]


def exact_scale(normalizer, work):
    if not isinstance(normalizer, ScaledNorm):
        raise TypeError("actual ScaledNorm record required")
    mantissa = work.note(Fraction.from_float(normalizer.mantissa))
    exponent = normalizer.exponent
    power = Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)
    return work.mul(mantissa, work.note(power))


def sqrt_upper(q, bits, work):
    """Directed exact rational upper bound, including exact zero/ties."""
    if q < 0 or type(bits) is not int or bits < 0:
        raise ValueError("nonnegative squared residual and integer bits required")
    denominator = 1 << bits
    numerator = q.numerator * denominator * denominator
    ceiling = -((-numerator) // q.denominator)
    integer = math.isqrt(ceiling)
    if integer * integer < ceiling:
        integer += 1
    result = work.note(Fraction(integer, denominator))
    if work.mul(result, result) < q:
        raise AssertionError("directed square-root bound violated")
    # Integer operands preceding Fraction reduction are distinct cost data.
    return result, {"integer_operand_bits": max(numerator.bit_length(),
                    q.denominator.bit_length(), ceiling.bit_length()),
                    "grid_bits": bits, "output_numerator_bits": integer.bit_length()}


def certify_pair(raw, output, normalizer, certificate_bits=80):
    """Certify these exact supplied stored objects; never replace their data.

    This entry also permits adversarial returns to test acceptance. It does
    not assert that an arbitrary pair came from the frozen canonicalizer.
    """
    if type(certificate_bits) is not int or certificate_bits < 0:
        raise ValueError("nonnegative integer certificate precision required")
    work = Work()
    c, d = stored_cores(raw, work), stored_cores(output, work)
    if len(c) != len(d):
        raise ValueError("same physical core count required")
    before_add, before_mul = work.rational_additions, work.rational_multiplications
    raw_gram = cross_gram(c, c, work)
    output_gram = cross_gram(d, d, work)
    cross = cross_gram(c, d, work)
    contraction_additions = work.rational_additions - before_add
    contraction_multiplications = work.rational_multiplications - before_mul
    if raw_gram <= 0:
        raise ArithmeticError("stored raw TT is zero; normalization target undefined")
    scale = exact_scale(normalizer, work)
    inverse = work.div(Fraction(1), scale)
    ratio_squared = work.mul(work.mul(inverse, inverse), raw_gram)
    residual_squared = work.add(work.add(output_gram,
        -work.mul(work.mul(Fraction(2), inverse), cross)), ratio_squared)
    if residual_squared < 0:
        raise AssertionError("exact cross-Gram squared residual is negative")
    residual, integer_work = sqrt_upper(residual_squared, certificate_bits, work)
    tau = abs(work.add(ratio_squared, Fraction(-1)))
    bound = work.add(residual, tau)
    max_bond = max(raw.max_bond, output.max_bond)
    field_budget = 27 * raw.n * max_bond**3
    if contraction_additions + contraction_multiplications > field_budget:
        raise AssertionError("actual contraction count exceeds declared cubic bound")
    certificate = {
        "n": raw.n, "raw_max_bond": raw.max_bond, "output_max_bond": output.max_bond,
        "actual_normalizer_mantissa": rational_text(Fraction.from_float(normalizer.mantissa)),
        "actual_normalizer_exponent": normalizer.exponent,
        "actual_normalizer": rational_text(scale),
        "raw_gram": rational_text(raw_gram), "output_gram": rational_text(output_gram),
        "cross_gram": rational_text(cross),
        "residual_squared": rational_text(residual_squared),
        "residual_upper": rational_text(residual),
        "scaled_raw_norm_squared": rational_text(ratio_squared),
        "normalizer_ratio_error_upper": rational_text(tau),
        "normalized_stored_TT_error_upper": rational_text(bound),
        "work": {**vars(work), "contraction_additions": contraction_additions,
                 "contraction_multiplications": contraction_multiplications,
                 "contraction_field_budget": field_budget,
                 "normalizer_exponent_abs": abs(normalizer.exponent),
                 "integer_sqrt": integer_work,
                 "scalar_assembly_additions": work.rational_additions - contraction_additions,
                 "scalar_assembly_multiplications": work.rational_multiplications - contraction_multiplications,
                 "scalar_assembly_divisions": work.rational_divisions,
                 "normalizer_float_decodes": 2,
                 "scalar_comparison_sign_abs_and_bit_checks": "also performed; not included in rational field count",
                 "certificate_text_serialization": "lossless strings; integer decimal/hex conversion work separate"},
        "dense_constructor_or_checker_input": False,
        "certificate_scope": "actual output vs normalized original stored TT; exact rational arithmetic with literal cross-Gram semantics, not ideal source/circuit or whole Python-Lean refinement",
        "global_source_epsilon_certificate": False,
    }
    return certificate


def certify_scaled_canonicalize(raw, certificate_bits=80):
    """Call the frozen producer once and certify the SAME returned TT/scale."""
    # Validate stored input before the actual call; conversion error is not
    # silently merged into the stored-source target.
    if type(certificate_bits) is not int or certificate_bits < 0:
        raise ValueError("nonnegative integer certificate precision required")
    validation_work = Work()
    stored_cores(raw, validation_work)
    output, normalizer = scaled_right_canonicalize(raw)
    certificate = certify_pair(raw, output, normalizer, certificate_bits)
    certificate["work"]["prevalidation_decoded_scalars"] = validation_work.decoded_scalars
    certificate["work"]["total_decoded_scalars_including_prevalidation"] = (
        validation_work.decoded_scalars + certificate["work"]["decoded_scalars"])
    certificate["work"]["input_validation_passes"] = 2
    certificate["work"]["output_validation_passes"] = 1
    certificate["work"]["work_scope"] = (
        "exact certificate arithmetic, copies and prevalidation; frozen QR work is separate. "
        "Reduced Fraction bit maxima and conservative pre-GCD bounds are distinguished; "
        "no complete Python-integer/GCD runtime trace is claimed.")
    certificate["producer"] = "frozen scaled_right_canonicalize; exactly one call"
    return output, normalizer, certificate
