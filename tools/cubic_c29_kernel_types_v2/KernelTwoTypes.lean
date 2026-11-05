import QuantumBlockEncoding.CubicStatePreparation
import Lean

/- Narrow diagnostic supplement for two observed kernel-candidate pretty-type omissions.
   No values, axiom policy or scientific acceptance are emitted. -/
open Lean Elab Command

set_option pp.universes true
set_option pp.fullNames true
set_option pp.privateNames true
set_option pp.explicit true
set_option pp.notation false
set_option pp.proofs true
set_option pp.funBinderTypes true
set_option pp.piBinderTypes true
set_option pp.deepTerms true
set_option pp.maxSteps 2000000
set_option maxRecDepth 10000

namespace CubicKernelTwoSignatureSupplementV2

def exactNames : Array Name := #[
  `QuantumBlockEncoding.CubicDiagonalOracle.linearDiagonalFourSquareBranchVector_unit._proof_1_1,
  `QuantumBlockEncoding.CubicDiagonalOracle.cubicDiagonalFourSquareBranchVector_unit._proof_1_1
]

def emit (tag : String) (row : Json) : CommandElabM Unit :=
  IO.println (tag ++ " " ++ row.compress)

def jsonNames (names : Array Name) : Json :=
  .arr (names.map fun name => .str name.toString)

def exactTypeText (info : ConstantInfo) : CommandElabM String :=
  liftTermElabM do
    return toString (← Meta.ppExpr info.type)

run_cmd do
  let target := `QuantumBlockEncoding.CubicStatePreparation
  let some expectedString ← IO.getEnv "QBE_EXPECT_FRESH_OLEAN"
    | throwError "C29_TWO_FAIL: missing expected fresh olean"
  let actualPath ← IO.FS.realPath (← findOLean target)
  let expectedPath ← IO.FS.realPath (System.FilePath.mk expectedString)
  unless actualPath == expectedPath do
    throwError "C29_TWO_FAIL: actual import is not the same fresh target artifact"
  let env := (← getEnv).setExporting false
  withEnv env do
    let some targetIdx := env.getModuleIdx? target
      | throwError "C29_TWO_FAIL: target module absent"
    let owned := env.constants.toList.filter fun pair =>
      env.getModuleIdxFor? pair.1 == some targetIdx
    emit "C29_TWO_BINDING_JSON" (Json.mkObj [
      ("schema", .str "C29_TWO_SIGNATURES_V1"),
      ("targetModule", .str target.toString),
      ("actualResolvedOleanPath", .str actualPath.toString),
      ("freshOleanPathComparisonPassed", .bool true),
      ("expectedNames", jsonNames exactNames),
      ("ppDeepTerms", .bool true), ("ppMaxSteps", toJson (2000000 : Nat)),
      ("maxRecDepth", toJson (10000 : Nat)),
      ("sourceAgreement", .null), ("publicationBinding", .null),
      ("axiomPolicyPass", .null), ("nativeAccepted", .bool false)])
    let mut ordinal := 0
    for name in exactNames do
      let choices := owned.filter fun pair => pair.1 == name
      match choices with
      | [(actual, info)] =>
        let some kernelInfo := env.toKernelEnv.find? actual
          | throwError "C29_TWO_FAIL: target signature absent from checked kernel env {actual}"
        let .thmInfo _ := kernelInfo
          | throwError "C29_TWO_FAIL: actual checked kind is not thmInfo {actual}"
        let .thmInfo _ := info
          | throwError "C29_TWO_FAIL: elaboration kind is not thmInfo {actual}"
        let text ← exactTypeText kernelInfo
        let axioms ← collectAxioms actual
        ordinal := ordinal + 1
        emit "C29_TWO_TYPE_JSON" (Json.mkObj [
          ("ordinal", toJson ordinal), ("actualName", .str actual.toString),
          ("actualKind", .str "thmInfo"), ("kernelRootPresent", .bool true),
          ("universeParameters", jsonNames kernelInfo.levelParams.toArray),
          ("typePrettyExplicit", .str text),
          ("isUnsafe", .bool kernelInfo.isUnsafe),
          ("axioms", jsonNames (axioms.qsort Name.lt)),
          ("selfOccursInAxioms", .bool (axioms.contains actual)),
          ("valuesPrinted", .bool false),
          ("sourceAgreement", .null), ("publicationBinding", .null),
          ("axiomPolicyPass", .null), ("nativeAccepted", .bool false)])
      | [] => throwError "C29_TWO_FAIL: exact observed generated name missing {name}"
      | _ => throwError "C29_TWO_FAIL: exact observed generated name ambiguous {name}"
    emit "C29_TWO_SUMMARY_JSON" (Json.mkObj [
      ("schema", .str "C29_TWO_SIGNATURES_V1"),
      ("completed", toJson ordinal), ("valuesPrinted", .bool false),
      ("scope", .str "TWO_PRETTY_SIGNATURES_ONLY_NOT_AXIOM_POLICY"),
      ("sourceAgreement", .null), ("publicationBinding", .null),
      ("axiomPolicyPass", .null), ("nativeAccepted", .bool false)])

end CubicKernelTwoSignatureSupplementV2
