# Reuse the normalized source bridge; correct the public-LE adapter

IMPORTANT CORRECTION: the frozen C341 analysis incorrectly says the actual
exponential input is -p^2. The literal Hermite source is exp(p) for p<-1,
the Hermite polynomial for -1<=p<=0, and exp(-p) for p>0. Middle expMidpoint
uses fixed -1. All those exponential inputs are nonpositive, so the existing
enclosure domain and error budget remain unchanged. See the separately
hash-bound explicit-source-correction.json. Original erroneous analysis,
manifest and seal remain byte-exact; their mistake is not hidden or edited.
Hash integrity alone is not semantic correctness.

Existing normalized_original_error already gives epsilon/2 for positive
rational L,epsilon and the SAME sourceDelta. The central norm floor comes
from coordinate p=0 at index N/2, NOT index0. The next useful interface is
literal producer -> public-LE vector -> existing allocatedVector. wordIndex
is LSB-first; sampleEquiv adds reverseBasis and cannot be substituted on the
same Word without a bridge. Its two-bit symbolic mismatch is not a failure
of the already-proved source/circuit theorem or an executed benchmark.

Actual arbitrary-Real-L input representation remains OPEN. So do actual
rounding, norm evaluation, finite QR/isometry/absorption, angles/synthesis,
phase/clean workspace, total classical/native costs and family acceptance.
Do not transfer the old exact chain's bond or ideal-real gate budget to this
new producer. Source analysis/author context only, with incidental legacy
metadata exposure disclosed. Not independent review, new compilation or ROOT.
