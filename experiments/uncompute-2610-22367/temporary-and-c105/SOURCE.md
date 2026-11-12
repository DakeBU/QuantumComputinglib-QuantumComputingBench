# Temporary-AND measurement cleanup: a bounded source component

Status: pre-proof mathematical contract, not a source-approved or compiled
result. This component is Methods Eq. (12), physical page 9 of Gu, Kemeny,
Yelin and Lukin, arXiv:2610.22367v1. The page credits measurement-based
uncomputation to Gidney, reference [29]. No novelty is claimed. Primary source:
https://arxiv.org/html/2610.22367v1 ; fixed PDF SHA256
3607f457c3349db74e10b131abadef23a4a2dea0fefa0cf6ac6d0ed9f37fdfd9.
The entire physical page was text-read and visually inspected before this
contract. Source images are private inspection artifacts, not redistributed.

## Exact interface

Let a,b,m,t range over Fin 2; m is the X-measurement record. Let R be any
reference carrier and alpha:R -> Fin 2 -> Fin 2 -> complex be arbitrary.
The premeasurement state has amplitudes alpha(r,a,b) on |r,a,b,a AND b>.
Thus the measured ancilla is the CURRENT AND of the retained controls; this
does not license clearing an arbitrary modified coefficient register.

Use ASPBE's existing exact hadamardMatrix, with entries
H[m,u]=(-1)^(m*u)/sqrt(2). Destructive X measurement is the bra H[m,-]
followed by restoring the measured wire to |0>. Conditional CZ on a,b
has factor c(m,a,b)=-1 only when m=a=b=1, otherwise +1. Define the
unnormalized corrected branch, including the reset wire, by

    B_m(alpha)[r,a,b,t] =
      if t=0 then c(m,a,b) * H[m,a AND b] * alpha(r,a,b) else 0.

The exact root is B_m(alpha)[r,a,b,t] = s *
(if t=0 then alpha(r,a,b) else 0), where s=sqrt(2)/2 is real-positive.
It holds for BOTH outcomes and arbitrary reference amplitudes, preserving
all relative phases. The common positive s is retained, not silently
discarded as a global phase or normalized away. No input normalization is
required for this amplitude identity.

For finite R, let branchMass be the sum of squared complex magnitudes over
all r,a,b,t. A second root is branchMass(m,alpha)=inputMass(alpha)/2.
Normalized input therefore gives probability 1/2 per outcome, and the two
branch masses sum to inputMass. This is a finite-amplitude/Kraus calculation,
not introduction of a second global quantum measurement/channel API.

## Source topology and direct derivation

S1 is the current computed-AND state relation, a local SOURCE locus embodied
by the input embedding. S2 is the actual H basis-entry formula. S3 applies
the X-measurement bra and reset. S4 is outcome-controlled CZ. Their full
AND tail gives S5, the exact corrected branch: the two signs are identical
and square to +1, leaving s independently of r,a,b,m. S6 is s^2=1/2,
derived from the nonnegative real square-root identity. S5 AND S6 AND finite
sum linearity give S7, branchMass=inputMass/2. Normalization is needed ONLY
for its probability corollary. Arbitrary R covers a coherent reference, not
merely real amplitudes or a finite sample of states.

Methods Eq. (11)'s inverse-Toffoli cleanup is an alternative local mechanism,
retained as an OR route but not proved or resource-compared by this packet.
The Toffoli computation, intervening use, physical reset/measurement command
semantics, emitted gadget refinement and a general channel/density interface
are separate suppliers. Eq. (13)'s arbitrary Boolean function and other
Methods/scoring/statistical claims are excluded from THIS bounded theorem,
not declared formalized. No Gaussian coefficient lookup, interleaved phase
fixup, liveness, uniform error, 1583/139 resource point, SP/BE or finite-bit
Hermite root follows.

## Reuse and boundaries

Reuse QuantumBlockEncoding.hadamardMatrix and hadamardMatrix_apply rather
than defining a competing H gate. Mathlib supplies Complex.normSq,
Complex.normSq_mul, Complex.normSq_ofReal and real square-root facts.
Local declaration search found no existing temporary-AND measurement cleanup
root. The external quantum Lean atlas lists measurement APIs as reference/
adapter candidates; none is imported or copied. This narrow amplitude identity
adds no global state/channel foundation. No upstream Gidney proof is assumed:
the displayed local bra/sign algebra is proved directly.

The potential consumer is the cleanup supplier of the value-to-amplitude
route, BE.QueryModel.ValueToAmplitude; its whole compute/rotate/uncompute
chain remains OPEN. Inverse cleanup remains an alternative, and coefficient
MBU requires its ACTUAL live Boolean function rather than assuming it is AND.
No controller, scoring, production Lean or historical log is changed.
