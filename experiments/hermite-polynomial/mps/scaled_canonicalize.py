"""Experimental scaled float64 right canonicalization; not a certificate.

The old backend is deliberately unchanged. Positive rescalings are removed
before QR and residual absorption and recorded as a binary mantissa/exponent.
No dense state, SVD, tolerance pruning, or numerical-rank decision is used.
The normalized TT keeps signed amplitudes and MSB contraction / LSB labels.

QR and contraction still round, tiny entries may underflow, and exact zero
by cancellation is not decidable here. The normalizer is an approximate
floating-point product, not an exact source norm or a uniform error theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from mps_core_probe import TT


@dataclass(frozen=True)
class ScaledNorm:
    """Approximate positive norm = mantissa * 2**exponent, without expansion."""

    mantissa: float
    exponent: int

    def __post_init__(self):
        if not math.isfinite(self.mantissa) or not 0.5 <= self.mantissa < 1:
            raise ValueError("normalizer mantissa must be finite in [0.5,1)")
        if type(self.exponent) is not int:
            raise ValueError("normalizer exponent must be an integer")

    @property
    def log_norm(self) -> float:
        return math.log(self.mantissa) + self.exponent * math.log(2)

    @property
    def log2_norm(self) -> float:
        return math.log2(self.mantissa) + self.exponent

    def to_float(self) -> float:
        """Explicit optional conversion; fail if float64 cannot represent it."""
        try:
            value = math.ldexp(self.mantissa, self.exponent)
        except OverflowError as error:
            raise ArithmeticError("normalizer exceeds float64 range") from error
        if not math.isfinite(value) or value <= 0:
            raise ArithmeticError("normalizer is outside positive float64 range")
        return value


class _ScaleProduct:
    def __init__(self):
        self.mantissa, self.exponent = 0.5, 1  # Exactly one initially.

    def include(self, factor: float):
        if not math.isfinite(factor) or factor <= 0:
            raise ArithmeticError("nonpositive or nonfinite normalization scale")
        mantissa, exponent = math.frexp(factor)
        product, adjustment = math.frexp(self.mantissa * mantissa)
        self.mantissa = product
        self.exponent += exponent + adjustment

    def result(self) -> ScaledNorm:
        return ScaledNorm(self.mantissa, self.exponent)


def _rescale(array: np.ndarray, scales: _ScaleProduct) -> np.ndarray:
    if not np.all(np.isfinite(array)):
        raise ArithmeticError("nonfinite core or QR intermediate")
    if not array.size:
        raise ArithmeticError("zero-sized bond has no normalized state")
    scale = float(np.max(np.abs(array)))
    if scale == 0:
        raise ArithmeticError("stored-zero tensor has no normalized state")
    scales.include(scale)
    return array / scale


def scaled_right_canonicalize(tt: TT) -> tuple[TT, ScaledNorm]:
    """Return an approximate normalized TT and an unexpanded positive norm.

    Each core is initially max-scaled. At every right-to-left step, the
    QR residual is max-scaled BEFORE absorption; the absorbed preceding core
    is scaled again. All factors are positive, so signs are not discarded.
    The reduced-QR dimensions are min(left, 2*right), NOT a certified rank.
    Rank-deficient rows are retained; no singular-value cutoff is introduced.
    Caller data is copied. Only small core matrices are materialized.
    """
    scales = _ScaleProduct()
    cores = []
    for original in tt.cores:
        if np.iscomplexobj(original):
            raise ValueError("real cores required")
        try:
            core = np.array(original, dtype=np.float64, copy=True)
        except (ValueError, TypeError, OverflowError) as error:
            raise ValueError("float64-convertible real cores required") from error
        cores.append(_rescale(core, scales))

    for offset in range(tt.n - 1, 0, -1):
        left, _, right = cores[offset].shape
        q, residual = np.linalg.qr(cores[offset].reshape(left, 2 * right).T,
                                   mode="reduced")
        if not np.all(np.isfinite(q)):
            raise ArithmeticError("nonfinite QR factor")
        cores[offset] = q.T.reshape(q.shape[1], 2, right)
        residual = _rescale(residual, scales)
        absorbed = np.einsum("abc,cd->abd", cores[offset - 1], residual.T)
        cores[offset - 1] = _rescale(absorbed, scales)

    # The head has bounded entries after rescaling. hypot also avoids a naive
    # square-and-sum overflow/underflow if this implementation is reused.
    head_norm = math.hypot(*(float(value) for value in cores[0].flat))
    if not math.isfinite(head_norm) or head_norm <= 0:
        raise ArithmeticError("no finite positive scaled head norm")
    scales.include(head_norm)
    cores[0] = cores[0] / head_norm
    return TT(cores), scales.result()
