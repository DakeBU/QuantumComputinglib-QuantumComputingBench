# C324: final width-cap definition unfolding only

C322 source exit1/22.157s, zero accepted own output, consumer NOT run. Empty
list cases were resolved; four remaining final denominator clauses compare
hd at S+1 or S to an unexpanded operationWidth. Add ONLY operationWidth, the
same local S definition and Nat.add_zero to those four simp-only calls.
All arithmetic helpers, raw integer lists, witness/guard/carry definitions,
public/private statements and exact consumer stay unchanged. This is a
definition-level tactic repair, not an added bound or scientific assumption.

C310/C318 and C321/C322 immutable failures remain. C323 discloses C321's
inherited stale outputs metadata; current manifest separately binds fresh
outputs and ancestor inputs explicitly. No historical bytes are rewritten.
No width/root acceptance is asserted before new source/own-consumer gate.
No native/GCD/scratch/CPU/Sites/producer-wide/quantum/cleanup/export credit.
