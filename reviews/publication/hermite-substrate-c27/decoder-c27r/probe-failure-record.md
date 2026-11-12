# Retained probe failure

Class: IMPLEMENTATION_FAILED (diagnostic command compatibility), not mathematical refutation.

The first ProbeHermiteBinaryCutoff call exited 1 after 19.658029317855835 seconds. Its final command was `#print prefix _private.QuantumBlockEncoding.HermiteBinaryCutoff`. Lean 4.33 rejected `prefix` as an unexpected token after `#print`, followed by an unexpected-identifier error. The nine public root checks and axiom prints preceding this syntax error are not counted as a successful probe invocation.

The corrected probe enumerates matching private names from the loaded environment. It retains all nine original root checks/axiom prints and must independently exit 0. A subsequent probe will check the four discovered fully qualified private declarations directly.

The failed invocation's command, source/setup hashes, exit and wall time remain in the private call ledger. The first stdout file was reused by the corrected probe, so its full partial output is not retained; the error above and tool output are the surviving failure evidence. Later attempts receive separate versioned stdout/stderr logs. No actual-source proof compilation failed or was restarted.

The first supplemental ProbePrivateRoots call exited 1 after 20.623497486114502 seconds. It tried to spell internal private names with numeric name component `.0` directly in Lean surface syntax; the parser treated that component as numeral/field syntax and rejected the commands. The full versioned log is retained. The successor constructs identifiers from the actual environment Name values, then invokes the actual `#check`/`#print axioms` command elaborators; it asserts exactly four matching private roots. This is another diagnostic-assembly implementation failure, not a failed proof.

The second supplemental ProbePrivateRoots call exited 1 after 19.150057554244995 seconds. Lean inferred the unannotated mutable match counter as MessageData from the final error message, producing missing OfNat/BEq/HAdd instances. The next version explicitly annotates that counter as Nat and uses a qualified error logger. No proof theorem was altered; both failed supplemental full logs are retained.
