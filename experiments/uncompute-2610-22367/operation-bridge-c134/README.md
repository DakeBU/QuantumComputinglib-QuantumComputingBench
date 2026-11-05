# Actual operator bridge — proved locally, not admitted

Status: `PROVED_LOCALLY_IN_INHERITED_CONTEXT_NOT_ADMITTED`.

This is an experimental finite-dimensional linear-algebra bridge for temporary
AND cleanup, not a physical measurement/reset implementation or an SP/BE root.
It refines the ideal branch calculation on page 9, equations (11)–(13), of
Gu, Kemeny, Yelin and Lukin, *Discovering state-of-the-art quantum circuits with
large language models*, arXiv:2610.22367v1. The pinned PDF SHA256 is
`3607f457c3349db74e10b131abadef23a4a2dea0fefa0cf6ac6d0ed9f37fdfd9`.

## Exact statement and scope

Let J insert a zero target into the two-bit data carrier, U be the existing
primitive evaluator's actual three-wire CCX program, K_m the full-carrier
X-basis bra, and C_m the conditional CZ on the retained data. The sealed root is

    J C_m K_m U J = (sqrt(2)/2) J, for each m in Fin 2.

Multiplication acts right to left. The two data bits are preserved; J after
the bra gives a reset-shaped linear map, not a theorem about hardware reset.
Both outcomes are retained, including their exact phases. There is no
intervening consumer operation; arbitrary use of the computed AND is not
covered. The source Statement Seal and typed operator definitions remain in
`../operation-bridge-c128/`, unchanged.

Seven exported theorems prove actual CCX graph action on zero-target input,
J and C_m isometries, all-carrier Kraus completeness for K_m, equality to the
earlier scalar branch helper, the displayed kernel identity, and half of input
mass in each branch. Complex amplitudes with an arbitrary untouched reference
label are allowed; the mass theorem additionally requires a finite reference
carrier. Normalized conditional states and Born semantics are not silently
inserted into these unnormalized linear identities.

## Actual observations, not proposed outcomes

The whole module compiled with Lean 4.33.0: exit 0, 66.828 seconds, 3072 MiB
limit, one compiler thread. A separate import of that exact output checked all
seven exported types and printed their axioms: exit 0, 26.031 seconds. Each
lists exactly `propext`, `Classical.choice`, `Quot.sound`. Output/source hashes
and inherited-provider limitations are in the observation JSON files. Existing
provider binaries were inherited; this is not a fresh transitive TCB build or
a proof that every provider binary equals its current source.

Three earlier failed implementations and their original feedback survive
byte-for-byte in `failed-attempts-original.zip`. Their fixed three-attempt cap
was not increased. A separately diagnosed finite-sum alignment probe passed
before the single-block integration. Failed compilation was an implementation
failure, not a counterexample to the statement.

Fresh whole-formal source-blind decoding and independent source comparison
are still pending at this checkpoint. No Proof Seal, publication admission,
full library/Tests gate, full site gate, physical adaptive-instrument theorem,
gate/ancilla/finite-bit resource claim, arbitrary-use theorem, SP/BE closure,
Hermite root, or PURIFIED reader status is claimed.

## Reproduction boundary

Use the repository's Lean 4.33.0 dependency context, with required provider
modules actually built. In a newly created exclusive staging directory, place
the exact `TemporaryAnd.lean` from `../temporary-and-c105/`,
`StatementProbe.lean` from `../operation-bridge-c128/`, and this directory's
`OperationBridge.lean` and `RootAudit.lean`. Set `LEAN_PATH` to the staging
directory while retaining the lake environment's dependency paths. Compile
these first three modules in order, serially, using
`lake env lean -M3072 -j1 --root=STAGE -o STAGE/Module.olean STAGE/Module.lean`,
then compile `RootAudit.lean` against those outputs. `STAGE` and `Module` are
placeholders, not stored local paths. Missing files, missing dependencies,
nonzero exit or mismatched hashes are failures, never green acceptance.

The exact public observation originals are preserved in
`../../../reviews/publication/migration-checkpoints-c135/public-observations-original.zip`.
Flat text files use explicitly recorded LF transport derivatives; see that
directory's `observation-transports.json`. Original hashes are not retroedited.

Rollback: remove this additive experimental checkpoint. It changes no
production primitive, verifier, target, scoring, acceptance or historical log.
