import Lean

open Lean Elab Command

namespace C31Native

structure RootSpec where
  targetModule : Name
  userName : Name
  privateRoot : Bool
  sourceKind : String
  deriving BEq

def kind : ConstantInfo → String
  | .axiomInfo _ => "axiomInfo"
  | .defnInfo _ => "defnInfo"
  | .thmInfo _ => "thmInfo"
  | .opaqueInfo _ => "opaqueInfo"
  | .quotInfo _ => "quotInfo"
  | .inductInfo _ => "inductInfo"
  | .ctorInfo _ => "ctorInfo"
  | .recInfo _ => "recInfo"

def names (xs : Array Name) : Json := .arr (xs.map fun n => .str n.toString)

def noAccept : List (String × Json) := [
  ("sourceAgreement", .null), ("axiomPolicyPass", .null),
  ("publicationBinding", .null), ("scientificAcceptance", .bool false),
  ("nativeAccepted", .bool false), ("trustClosure", .bool false)]

def emit (tag : String) (row : List (String × Json)) : CommandElabM Unit :=
  IO.println (tag ++ " " ++ (Json.mkObj (row ++ noAccept)).compress)

def requiredEnv (key : String) : CommandElabM String := do
  let some value ← IO.getEnv key | throwError "C31 missing environment binding {key}"
  unless !value.isEmpty do throwError "C31 empty environment binding {key}"
  return value

def typeText (ci : ConstantInfo) : CommandElabM String := do
  let text ← liftTermElabM do return toString (← Meta.ppExpr ci.type)
  if text.contains '⋯' || text.contains '…' then
    throwError "C31 incomplete type pretty print {ci.name}"
  return text

def observation (env : Environment) (target actual : Name) (ci : ConstantInfo)
    (sourceKind : String) : CommandElabM (List (String × Json)) := do
  let some ki := env.toKernelEnv.find? actual
    | throwError "C31 no kernel constant {actual}"
  unless kind ki == kind ci && ki.type == ci.type && ki.levelParams == ci.levelParams do
    throwError "C31 kernel/elaboration disagreement {actual}"
  let typ ← typeText ci
  let axioms ← collectAxioms actual
  let available := (ci.value? (allowOpaque := true)).isSome
  unless available == ci.hasValue (allowOpaque := true) do
    throwError "C31 inconsistent actual value availability {actual}"
  return [
    ("module", .str target.toString), ("actualName", .str actual.toString),
    ("userNameViaActualAPI", .str (privateToUserName actual).toString),
    ("actualPrivate", .bool (isPrivateName actual)), ("actualKind", .str (kind ci)),
    ("kernelRootPresent", .bool true), ("kernelKind", .str (kind ki)),
    ("kernelTypeAndUniversesAgree", .bool true),
    ("universeParameters", names ci.levelParams.toArray),
    ("typePrettyExplicit", .str typ), ("isUnsafe", .bool ci.isUnsafe),
    ("actualHasValueAllowOpaque", .bool available),
    ("valueTextRequested", .bool false), ("valuePrettyExplicitAllowOpaque", .null),
    ("valueObservation", .str (if available then "NOT_REQUESTED_VALUE_AVAILABLE"
      else "NOT_REQUESTED_NO_VALUE_AVAILABLE")),
    ("actualOpaqueInfo", .bool (kind ci == "opaqueInfo")),
    ("actualAxiomInfo", .bool (kind ci == "axiomInfo")),
    ("sourceOpaque", .bool (sourceKind == "opaque")),
    ("axioms", names (axioms.qsort Name.lt)),
    ("selfOccursInAxioms", .bool (axioms.contains actual)),
    ("axiomCollection", .str "ACTUAL_LEAN_COLLECT_AXIOMS_IMPORTED_EXTENSION_AND_LOCAL_BODIES"),
    ("typeTextScope", .str "ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION")]

def collect (targets : Array Name) (roots : Array RootSpec) : CommandElabM Unit := do
  let profileSHA ← requiredEnv "C31_PROFILE_SHA256"
  let cohortID ← requiredEnv "C31_COHORT_ID"
  let freshRoot ← requiredEnv "C31_FRESH_ROOT"
  let opts ← getOptions
  unless pp.deepTerms.get opts && pp.proofs.get opts && pp.explicit.get opts &&
      pp.universes.get opts && pp.fullNames.get opts && pp.privateNames.get opts &&
      !pp.notation.get opts && pp.funBinderTypes.get opts && pp.piBinderTypes.get opts do
    throwError "C31 incomplete pp options"
  unless pp.maxSteps.get opts == 2000000 && maxRecDepth.get opts == 10000 do
    throwError "C31 wrong bounded pp limits"
  unless targets.size > 0 && roots.size > 0 do throwError "C31 empty profile"
  let env := (← getEnv).setExporting false
  withEnv env do
    let mut seenModules : Array Name := #[]
    let mut globalActual : Array Name := #[]
    let mut explicitCount := 0
    let mut privateCount := 0
    let mut generatedCount := 0
    let mut ownedCount := 0
    for target in targets do
      if seenModules.contains target then throwError "C31 duplicate target module"
      seenModules := seenModules.push target
      let expectedPath := (System.FilePath.mk freshRoot) /
        (target.toString.replace "." "/" ++ ".olean")
      let actualPath ← findOLean target
      let realActual ← IO.FS.realPath actualPath
      let realExpected ← IO.FS.realPath expectedPath
      unless realActual == realExpected do throwError "C31 fresh cohort lookup mismatch {target}"
      let some idx := env.getModuleIdx? target | throwError "C31 missing target module {target}"
      let owned := (env.constants.toList.filter fun p =>
        env.getModuleIdxFor? p.1 == some idx).toArray.qsort fun a b => Name.lt a.1 b.1
      let specs := roots.filter fun r => r.targetModule == target
      unless owned.size > 0 && specs.size > 0 do throwError "C31 empty module inventory"
      let mut resolved : Array (RootSpec × Name × ConstantInfo) := #[]
      let mut seenUsers : Array Name := #[]
      let mut explicitNames : Array Name := #[]
      for spec in specs do
        if seenUsers.contains spec.userName then throwError "C31 duplicate source root"
        seenUsers := seenUsers.push spec.userName
        let choices := owned.filter fun p =>
          if spec.privateRoot then isPrivateName p.1 && privateToUserName? p.1 == some spec.userName
          else !isPrivateName p.1 && p.1 == spec.userName
        unless choices.size == 1 do throwError "C31 missing or ambiguous source root {spec.userName}"
        let (actual, ci) := choices[0]!
        if globalActual.contains actual then throwError "C31 actual root collision {actual}"
        globalActual := globalActual.push actual
        explicitNames := explicitNames.push actual
        resolved := resolved.push (spec, actual, ci)
      let mut structures : Array Json := #[]
      for (actual, _) in owned do
        if let some si := getStructureInfo? env actual then
          let some (.inductInfo iv) := env.find? actual
            | throwError "C31 structure not inductive {actual}"
          let mut fields : Array Json := #[]
          for field in si.fieldInfo do
            unless env.getModuleIdxFor? field.projFn == some idx do
              throwError "C31 field ownership mismatch {field.projFn}"
            let some fi := env.find? field.projFn | throwError "C31 missing field projection"
            fields := fields.push (Json.mkObj [
              ("fieldName", .str field.fieldName.toString),
              ("projection", .str field.projFn.toString), ("actualKind", .str (kind fi))])
          structures := structures.push (Json.mkObj [
            ("actualName", .str actual.toString), ("constructors", names iv.ctors.toArray),
            ("fieldNames", names si.fieldNames), ("fields", .arr fields)])
      emit "C31_BINDING_JSON" [
        ("module", .str target.toString), ("profileSHA256", .str profileSHA),
        ("cohortID", .str cohortID), ("resolvedOleanPath", .str realActual.toString),
        ("freshOleanPathComparisonPassed", .bool true),
        ("ownershipMethod", .str "ENVIRONMENT_MODULE_INDEX_NOT_NAME_PREFIX"),
        ("ownedNames", names (owned.map Prod.fst)), ("ownedCount", toJson owned.size),
        ("expectedRoots", toJson specs.size), ("structures", .arr structures),
        ("ppDeepTerms", .bool true), ("ppMaxSteps", toJson (2000000 : Nat)),
        ("maxRecDepth", toJson (10000 : Nat))]
      for (spec, actual, ci) in resolved do
        explicitCount := explicitCount + 1
        if spec.privateRoot then privateCount := privateCount + 1
        let row ← observation env target actual ci spec.sourceKind
        emit "C31_ROOT_JSON" (row ++ [
          ("moduleOrdinal", toJson (specs.toList.idxOf spec + 1)),
          ("sourceUserName", .str spec.userName.toString),
          ("sourcePrivate", .bool spec.privateRoot), ("sourceKind", .str spec.sourceKind)])
      for (actual, ci) in owned do
        unless explicitNames.contains actual do
          if globalActual.contains actual then throwError "C31 generated identity collision"
          globalActual := globalActual.push actual
          generatedCount := generatedCount + 1
          emit "C31_GENERATED_JSON" ((← observation env target actual ci "GENERATED") ++
            [("includedInExplicitRootCount", .bool false)])
      ownedCount := ownedCount + owned.size
    unless explicitCount == roots.size && globalActual.size == ownedCount do
      throwError "C31 incomplete ownership partition"
    emit "C31_SUMMARY_JSON" [
      ("status", .str "FORMAL_DIAGNOSTIC_COMPLETE_NOT_ACCEPTANCE"),
      ("profileSHA256", .str profileSHA), ("cohortID", .str cohortID),
      ("modulesCompleted", toJson targets.size), ("rootsCompleted", toJson explicitCount),
      ("privateCompleted", toJson privateCount), ("generatedCompleted", toJson generatedCount),
      ("ownedCompleted", toJson ownedCount), ("allNamesResolvedUniquely", .bool true)]

end C31Native
