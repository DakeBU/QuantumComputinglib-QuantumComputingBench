import Lake
open Lake DSL

package aspbe where
  version := v!"0.1.0"

require VersoBlueprint from git
  "https://github.com/leanprover/verso-blueprint" @ "v4.33.0"

-- Keep Mathlib last so that its pins win when transitive dependencies overlap.
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.33.0"

@[default_target]
lean_lib QuantumBlockEncoding

lean_lib Tests where
  roots := #[`Tests, `ABEISTests.Basic, `ABEISTests.QBenchIntegration,
    `ABEISTests.GHLHamiltonian]
  globs := #[.one `Tests, .submodules `ABEISTests]

lean_lib ABEISBlueprint

lean_exe blueprintGen where
  root := `ABEISBlueprintMain
  supportInterpreter := true
