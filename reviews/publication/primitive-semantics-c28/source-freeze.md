# Source freeze and author handoff

## Provenance and scope

Packet identity: `primitive-semantics-author-c28`. Evidence class: retrospective local source reconstruction for the Lean 4.33 migration. Historical formalizer: UNKNOWN. This is the source author, not a distinct decoder/reviewer. No external-paper attribution, pre-proof source provenance, scientific novelty, independent acceptance or fresh compilation is asserted.

Repository snapshot observed by read-only reference queries:

- `HEAD`: `cc25e39022db29ce9f98e77708850ce2dc0b0739`.
- `origin/main`: `f2cba045611a0d11c5995c29607569726bf1d6c5`.
- Fetch/reconciliation ownership: parent; this worker did not fetch, stage, commit, push or modify Git metadata. A read-only status query returned “must be run in a work tree”; the actual source was read and hashed directly. Commit identities are context, not a claim that working bytes equal every file at that commit. The raw-byte hashes below are the binding.

Complete authored target scope (none may be dropped): `QuantumBlockEncoding/ConcreteSemantics.lean`, `QuantumBlockEncoding/PrimitiveSemantics.lean`, `QuantumBlockEncoding/ReversibleClassical.lean`. These three full files were read through EOF, including every proof body and ambient region. SHA-256 is over raw file bytes, without newline normalization. Their final reread hashes agree with the initial freeze.

All file references in this packet are repository-relative or packet-relative. No private machine path is required to interpret the artifacts.

## Frozen actual production inputs

The following is the project-local lexical import closure of the three targets, discovered by recursively following `import QuantumBlockEncoding.…` to existing relative `.lean` files. It binds the actual files rather than claiming all of this closure was semantically audited. Target files were read completely. Necessary provider reading was complete for `PrimitiveCircuit.lean`, `PrimitiveRefinement.lean`, `CircuitSemantics.lean`, `StatePreparation.lean`; targeted provider regions were read in `Core.lean` (finite matrices/grid and coefficient interpretation), `BlockEncodingClassics.lean` (product index and clean block), `Robin/ComplexLCU.lean` (rotation, unitary reindex and permutation infrastructure), `Robin/Hadamard8Verified.lean` (uniform-bit preparation). Other closure files were hashed as ambient context only.

| Relative file | Lines | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `QuantumBlockEncoding/BlockEncoding.lean` | 255 | 8443 | `fe06f75a29822e28ccdbfedfb0b0e87f90872620fae7aed359085fad8fae64b4` |
| `QuantumBlockEncoding/BlockEncodingClassics.lean` | 891 | 34134 | `94ac6632924df0a49b1ebd99bb5d9ed69b2ea463ec527033f38bd73deeb1346a` |
| `QuantumBlockEncoding/Circuit.lean` | 89 | 2532 | `286c7b579f75891cb34f01d13e84a5f00e6b509a480efaaef9472a58a67a0f94` |
| `QuantumBlockEncoding/CircuitSemantics.lean` | 814 | 33102 | `761ac3a98ea5a82ad5030e280e3810821081d10cec3d0a0a1d3c2add3fcd4666` |
| `QuantumBlockEncoding/ConcreteSemantics.lean` | 297 | 12631 | `4b4e1c3612ea2d4eed3a2d5dbfec39ffae81263fd9ceb521c1a59231f786caa1` |
| `QuantumBlockEncoding/Core.lean` | 243 | 7357 | `c7e76d91c7fcfd844177f99c0399a3465a7d8360d3a522acb5d4c4e2f8277894` |
| `QuantumBlockEncoding/Examples/RobinHeat.lean` | 88 | 2922 | `f2b2691ecc6300705a1dd319fa4386562e2b267e806ff905b66d81303b6645ff` |
| `QuantumBlockEncoding/GHL2025.lean` | 8474 | 383342 | `2dba31e056b134107b34c7e41c6a5c3a2130c22a2634372d1e9ce794961a4fd4` |
| `QuantumBlockEncoding/PrimitiveCircuit.lean` | 229 | 8337 | `d5019ef58ce1ce65664d2a40979cdd652ca691c94743532c59dfe18cf2036d4c` |
| `QuantumBlockEncoding/PrimitiveRefinement.lean` | 38 | 1528 | `d285b747ebe189b9e9b381cdbd3c16bd23edb0b9706b2099bb679a5ad230279e` |
| `QuantumBlockEncoding/PrimitiveSemantics.lean` | 493 | 20422 | `a68955f9dbe0e951c2751fcd14c535c28da7c8bcac75787b0005808b951f28de` |
| `QuantumBlockEncoding/Resources.lean` | 152 | 4784 | `d7d939aa5e74965a28a3835750aa7ca5fa27aeeb0ef14ad1f5555cbf6279e09d` |
| `QuantumBlockEncoding/ReversibleClassical.lean` | 83 | 3422 | `7662d42a2afae784dc14d669a462baecf5fa18ac8165c64e35c006be3517c26d` |
| `QuantumBlockEncoding/Robin/ComplexLCU.lean` | 401 | 16680 | `aa51d33a6ca788b17879e1d88030b525f4f035c97d74588636ccf25f8c04b843` |
| `QuantumBlockEncoding/Robin/ComplexLCUProjection.lean` | 222 | 9587 | `fa0b84ce5c819184f190b81b4d259e12f725e6196cd37147984fab76fe4ec340` |
| `QuantumBlockEncoding/Robin/EvolvedCandidates.lean` | 100 | 4416 | `93875b1775a857e70ea3447a892cf245b0d4a77a0dcb0ec3310c85bdf55e5268` |
| `QuantumBlockEncoding/Robin/FixedN3Data.lean` | 54 | 2066 | `5d9cd56041be0af97ad2385aae2714f6ad05331a4df91ffc0704c2e983b453b8` |
| `QuantumBlockEncoding/Robin/Hadamard8Verified.lean` | 120 | 4818 | `138b0ecf4a43b888d43d7e4d7682218139725644695952c0f3eb8d99663acfd4` |
| `QuantumBlockEncoding/Robin/SourceBaseline.lean` | 92 | 3410 | `cc3aa711cb2bc5c4dfb308719e77ac299539d9a1f97f7b45002b4a11cc9a5722` |
| `QuantumBlockEncoding/Robin/WeightedPermutation.lean` | 111 | 4450 | `c5c4ab73bd9a1d97f3672bfcb4ef374b9c832afec2935df378408283d2756eaf` |
| `QuantumBlockEncoding/RobinEvolution.lean` | 212 | 7897 | `8673572458ff260cf35d6cfce60ffcc52b5b2be721671b3171919e32d0b73a37` |
| `QuantumBlockEncoding/RobinMatrix.lean` | 26985 | 1294042 | `1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835` |
| `QuantumBlockEncoding/StatePreparation.lean` | 105 | 3928 | `2585a3b5ef2a58a0f7fb33664552e9166373cec2815eddf2542c9db66cb5f52f` |

## Toolchain, package configuration and complete manifest revision set

`lean-toolchain` content: `leanprover/lean4:v4.33.0`. SHA-256: `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b`.

`lakefile.lean` SHA-256: `f6637c3a2467fdeee6b2de72505d0581c4a49793388197bd8e9e7df3f5817fc1`. Package `aspbe` version `0.1.0`; direct requirements are VersoBlueprint and Mathlib at `v4.33.0`, Mathlib listed last. This records configuration, not an executed build.

`lake-manifest.json` SHA-256: `510171e8214a2ac5e00f16c1bf92ad474d2de42c4cd2dc2b3d411272f7b58763`. Manifest version `1.2.0`, `packagesDir = .lake/packages`, `lakeDir = .lake`, `fixedToolchain = false`.

| Package | Repository | Exact manifest revision |
| --- | --- | --- |
| mathlib | `leanprover-community/mathlib4` | `db584cd6d46c92f209a44c0f1c829460d327499d` |
| VersoBlueprint | `leanprover/verso-blueprint` | `e0d667222e8222ac4bfd74780f69a2e89cd4655f` |
| plausible | `leanprover-community/plausible` | `b7eb3304aeae834b12dda98993a37f6a41f6f0bb` |
| LeanSearchClient | `leanprover-community/LeanSearchClient` | `5f4d51b81cbd3f6b32b156bfad9056621a040404` |
| importGraph | `leanprover-community/import-graph` | `16f02aa7642864af59f1ff0e384a015994db9118` |
| proofwidgets | `leanprover-community/ProofWidgets4` | `4be2e3d5087eeb272cf5a8853b8f9dd025ef5957` |
| aesop | `leanprover-community/aesop` | `3448c0bcc5ce01b2d1546e483ec3620e32df3d0e` |
| Qq | `leanprover-community/quote4` | `92c15be17b7caf78c2ad767ec40f89052d908d81` |
| batteries | `leanprover-community/batteries` | `4488d40d070b9700d4d5a6aa342f0d40c31b2a2d` |
| verso-slides | `leanprover/verso-slides` | `ddea15f92035c6de1d76e3afa5476f7ab3de955d` |
| verso | `leanprover/verso` | `36664a0ebe032ef3f9e72a8ed0d7be9b14af17d2` |
| Cli | `leanprover/lean4-cli` | `6130a47896ce867c6a4a55373441e59e565bad0f` |
| illuminate | `leanprover/illuminate` | `6bc815869cba1f19515715dc6b47795acd521f1c` |
| MD4Lean | `acmepjz/md4lean` | `31907cc18f48a95384f99cee5582c00fb39e0f67` |
| subverso | `leanprover/subverso` | `3a75ede05278806fd3249bb0c97a6fb5777a4f7d` |

These are manifest pins, not verification of installed package trees, fetched Git objects, generated `.olean` contents or a successful compiler execution. No dependency cache was written.

## Packet artifact bindings

| Packet-relative artifact | SHA-256 |
| --- | --- |
| `source-only.md` | `696a9dce55a0ab9af6139b96ed8ba619fa0b946a0519bbe740cbdc58666e44b5` |
| `author-private-coverage.md` | `1c42f8d0190581e416e25c897d1ce8f581f8da995742b5c62e9977f9a2afc59a` |

This freeze file does not contain its own recursively defined hash. Its final hash is returned in the handoff. Text checks found balanced inline/display mathematical delimiters, no local-path leakage or implementation names in the public source, and lexical-name coverage of every authored target declaration in the private map. These checks are not independent mathematical review.

## Short handoff

Objective/frontier: author-source restoration for the entire finite-action/primitive-semantics/reversible-classical dependency family. Mathematical delta: one natural-language mathematical source contract preserving half-angle and signed RY/RZ entries, later-on-left chronological products, exact global phase, arbitrary stored normalization proposition, unlinked presentation/resource metadata, signal-high/system-low flattening, named-wire basis without invented integer endianness, empty carriers and zero-wire phase, conditional generic lifting versus derived primitive unitarity, and proof-only CCX with syntax/semantic distinctness differences.

Only the three packet files were created. Production source, Git, caches and dependencies were untouched. No Lean/build/test command was run, by explicit task boundary. No decoder/reviewer/older verdict artifact was inspected, no agent was spawned, no independent accepted verdict was authored. Failure class NONE for this source recovery; mirror status-query limitation noted above. No failed proof fragment requires salvage. No external process memory was treated as mathematical authority.

Next permitted step: parent coordinates fresh source-first readers with only the public mathematical source and later anti-anchored comparison against the exact frozen whole modules. Private coverage and this freeze are author evidence, not substitutes for those readers. Any changed target source/import/private helper/ambient scope, toolchain or manifest invalidates the relevant binding; rehash and re-review rather than inheriting this packet silently. Independent topology review, decoder/reviewer records, publication metadata, build gates, Proof Seal, purification and Exposition Seal remain outside this author task.
