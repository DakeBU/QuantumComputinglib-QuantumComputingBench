import Fixture
import Lean

/- Diagnostic candidate only. NOT RUN by decoder; no mathematical acceptance.
   The hosting process must bind raw source, fresh output and provider hashes.
   QBE_EXPECT_FRESH_OLEAN must name the exact fresh target artifact. -/

open Lean Elab Command

set_option pp.universes true
set_option pp.fullNames true
set_option pp.privateNames true
set_option pp.explicit true
set_option pp.notation false
set_option pp.proofs true
set_option pp.funBinderTypes true
set_option pp.piBinderTypes true

namespace CubicBlindDiagnosticCandidate

structure RootSpec where
  userName : Name
  privateRoot : Bool
  sourceKind : String

def expectedRoots : Array RootSpec := #[
  { userName := `Fixture.supplied, privateRoot := false, sourceKind := "axiom" },
  { userName := `Fixture.exposed, privateRoot := false, sourceKind := "def" },
  { userName := `Fixture.hidden, privateRoot := true, sourceKind := "theorem" },
  { userName := `Fixture.sealed, privateRoot := false, sourceKind := "opaque" },
  { userName := `Fixture.Pair, privateRoot := false, sourceKind := "structure" }
]
def constantKind : ConstantInfo → String
  | .axiomInfo _ => "axiomInfo"
  | .defnInfo _ => "defnInfo"
  | .thmInfo _ => "thmInfo"
  | .opaqueInfo _ => "opaqueInfo"
  | .quotInfo _ => "quotInfo"
  | .inductInfo _ => "inductInfo"
  | .ctorInfo _ => "ctorInfo"
  | .recInfo _ => "recInfo"

def jsonNames (ns : Array Name) : Json :=
  .arr (ns.map fun n => .str n.toString)

def opaqueObservation (sourceKind : String) (ci : ConstantInfo) : String :=
  if sourceKind != "opaque" then "NOT_SOURCE_OPAQUE"
  else match ci with
    | .axiomInfo _ => "SOURCE_OPAQUE_ACTUAL_AXIOM_INFO"
    | .opaqueInfo _ => "SOURCE_OPAQUE_ACTUAL_OPAQUE_INFO"
    | _ => "SOURCE_OPAQUE_OTHER_ACTUAL_KIND_REQUIRES_REVIEW"

def exactTypeText (ci : ConstantInfo) : CommandElabM String :=
  liftTermElabM do
    return toString (← Meta.ppExpr ci.type)

def exactValueText (ci : ConstantInfo) : CommandElabM Json := do
  match ci.value? (allowOpaque := true) with
  | none => return .null
  | some value =>
    liftTermElabM do
      return .str (toString (← Meta.ppExpr value))

def emit (tag : String) (value : Json) : CommandElabM Unit := do
  IO.println (tag ++ " " ++ value.compress)

run_cmd do
  let target := `Fixture
  let some expectedPathString ← IO.getEnv "QBE_EXPECT_FRESH_OLEAN"
    | throwError "C29_FAIL: missing QBE_EXPECT_FRESH_OLEAN"
  let actualPath ← findOLean target
  let actualRealPath ← IO.FS.realPath actualPath
  let expectedRealPath ← IO.FS.realPath (System.FilePath.mk expectedPathString)
  unless actualRealPath == expectedRealPath do
    throwError "C29_FAIL: fresh target olean not first in actual search path"

  let env := (← getEnv).setExporting false
  withEnv env do
    let some targetIdx := env.getModuleIdx? target
      | throwError "C29_FAIL: target module absent from imported environment"
    let owned := env.constants.toList.filter fun pair =>
      env.getModuleIdxFor? pair.1 == some targetIdx
    unless expectedRoots.size == 5 do
      throwError "C29_FAIL: expected explicit root vector is not 5"
    unless (expectedRoots.filter fun r => r.privateRoot).size == 1 do
      throwError "C29_FAIL: expected private root vector is not 1"
    unless (expectedRoots.filter fun r => r.sourceKind == "opaque").size == 1 do
      throwError "C29_FAIL: source opaque vector is not 1"
    unless (expectedRoots.filter fun r => r.sourceKind == "structure").size == 1 do
      throwError "C29_FAIL: source structure vector is not 1"

    -- Resolve ALL roots before emitting any root-completion claim.
    -- No construction, parsing or guessing of numeric private name components.
    let mut resolved : Array (RootSpec × Name × ConstantInfo) := #[]
    let mut seenActual : Array Name := #[]
    let mut seenUsers : Array Name := #[]
    for spec in expectedRoots do
      if seenUsers.contains spec.userName then
        throwError "C29_FAIL: duplicated source user name {spec.userName}"
      let choices := owned.filter fun pair =>
        if spec.privateRoot then
          isPrivateName pair.1 && privateToUserName? pair.1 == some spec.userName
        else
          !isPrivateName pair.1 && pair.1 == spec.userName
      match choices with
      | [(actual, ci)] =>
        if seenActual.contains actual then
          throwError "C29_FAIL: actual name reused across explicit roots {actual}"
        let some kernelInfo := env.toKernelEnv.find? actual
          | throwError "C29_FAIL: resolved root missing from checked kernel environment {actual}"
        unless constantKind kernelInfo == constantKind ci do
          throwError "C29_FAIL: kernel/elaboration ConstantInfo kind mismatch {actual}"
        seenActual := seenActual.push actual
        seenUsers := seenUsers.push spec.userName
        resolved := resolved.push (spec, actual, ci)
      | [] => throwError "C29_FAIL: missing explicit root {spec.userName}"
      | _ => throwError "C29_FAIL: ambiguous explicit root {spec.userName}"

    let mut projectionOwners : Array (Name × Name) := #[]
    let mut structureNames : Array Name := #[]
    let mut structureRows : Array Json := #[]
    for (spec, actual, ci) in resolved do
      if spec.sourceKind == "structure" then
        let some sinfo := getStructureInfo? env actual
          | throwError "C29_FAIL: source structure lacks actual StructureInfo {actual}"
        let .inductInfo iv := ci
          | throwError "C29_FAIL: source structure is not actual inductInfo {actual}"
        structureNames := structureNames.push actual
        let mut fields : Array Json := #[]
        for field in sinfo.fieldInfo do
          let some fieldInfo := env.find? field.projFn
            | throwError "C29_FAIL: structure projection absent {field.projFn}"
          unless env.getModuleIdxFor? field.projFn == some targetIdx do
            throwError "C29_FAIL: structure projection belongs to unexpected module {field.projFn}"
          projectionOwners := projectionOwners.push (field.projFn, actual)
          fields := fields.push (Json.mkObj [
            ("fieldName", .str field.fieldName.toString),
            ("projection", .str field.projFn.toString),
            ("actualKind", .str (constantKind fieldInfo))])
        structureRows := structureRows.push (Json.mkObj [
          ("sourceUserName", .str spec.userName.toString),
          ("actualName", .str actual.toString),
          ("constructors", jsonNames iv.ctors.toArray),
          ("fields", .arr fields)])

    emit "C29_BINDING_JSON" (Json.mkObj [
      ("targetModule", .str target.toString),
      ("actualResolvedOleanPath", .str actualRealPath.toString),
      ("freshOleanPathComparisonPassed", .bool true),
      ("expectedNamedRoots", toJson expectedRoots.size),
      ("observedTargetOwnedConstants", toJson owned.length),
      ("sourceOpaqueCount", toJson (expectedRoots.filter fun r => r.sourceKind == "opaque").size),
      ("actualStructures", .arr structureRows),
      ("sourceAgreement", .null), ("nativeAccepted", .bool false)])

    let mut ordinal := 0
    for (spec, actual, ci) in resolved do
      ordinal := ordinal + 1
      let typeText ← exactTypeText ci
      let axioms ← collectAxioms actual
      -- This is the same public collector used by builtin #print axioms.
      -- Never infer an empty array from a missing name or a lexical opaque tag.
      emit "C29_ROOT_JSON" (Json.mkObj [
        ("ordinal", toJson ordinal),
        ("sourceUserName", .str spec.userName.toString),
        ("sourcePrivate", .bool spec.privateRoot),
        ("sourceKind", .str spec.sourceKind),
        ("actualName", .str actual.toString),
        ("actualPrivate", .bool (isPrivateName actual)),
        ("actualKind", .str (constantKind ci)),
        ("opaqueClassification", .str (opaqueObservation spec.sourceKind ci)),
        ("kernelRootPresent", .bool true),
        ("universeParameters", jsonNames ci.levelParams.toArray),
        ("typePrettyExplicit", .str typeText),
        ("actualHasValueAllowOpaque", .bool (ci.hasValue (allowOpaque := true))),
        ("isUnsafe", .bool ci.isUnsafe),
        ("axioms", jsonNames (axioms.qsort Name.lt)),
        ("selfOccursInAxioms", .bool (axioms.contains actual)),
        ("sourceAgreement", .null), ("nativeAccepted", .bool false)])

    let mut generatedCount := 0
    for (name, ci) in owned do
      unless seenActual.contains name do
        generatedCount := generatedCount + 1
        let mut association := "OTHER_TARGET_OWNED_GENERATED_RESIDUAL"
        let mut parents : Array Name := #[]
        for (projection, owner) in projectionOwners do
          if name == projection then
            association := "STRUCTURE_FIELD_PROJECTION_METADATA"
            parents := parents.push owner
        match ci with
        | .ctorInfo v =>
          if structureNames.contains v.induct then
            association := "STRUCTURE_CONSTRUCTOR_METADATA"
            parents := parents.push v.induct
        | .recInfo v =>
          for owner in v.all do
            if structureNames.contains owner then
              association := "STRUCTURE_RECURSOR_METADATA"
              parents := parents.push owner
        | _ => pure ()
        let some kernelInfo := env.toKernelEnv.find? name
          | throwError "C29_FAIL: generated constant absent from kernel environment {name}"
        unless constantKind kernelInfo == constantKind ci do
          throwError "C29_FAIL: generated kernel/elaboration kind mismatch {name}"
        let typeText ← exactTypeText ci
        let valueText ← exactValueText ci
        let axioms ← collectAxioms name
        emit "C29_GENERATED_JSON" (Json.mkObj [
          ("actualName", .str name.toString),
          ("userNameViaActualAPI", .str (privateToUserName name).toString),
          ("actualPrivate", .bool (isPrivateName name)),
          ("actualKind", .str (constantKind ci)),
          ("kernelRootPresent", .bool true),
          ("universeParameters", jsonNames ci.levelParams.toArray),
          ("typePrettyExplicit", .str typeText),
          ("actualHasValueAllowOpaque", .bool (ci.hasValue (allowOpaque := true))),
          ("valuePrettyExplicitAllowOpaque", valueText),
          ("valueTextScope", .str "ACTUAL_META_PPEXPR_NOT_LOSSLESS_EXPR_SERIALIZATION"),
          ("isUnsafe", .bool ci.isUnsafe),
          ("opaqueClassification", .str (if constantKind ci == "opaqueInfo" then
            "GENERATED_ACTUAL_OPAQUE_INFO" else "GENERATED_NOT_OPAQUE_INFO")),
          ("axioms", jsonNames (axioms.qsort Name.lt)),
          ("selfOccursInAxioms", .bool (axioms.contains name)),
          ("axiomPolicyPass", .null), ("sourceAgreement", .null),
          ("publicationBinding", .null), ("nativeAccepted", .bool false),
          ("classification", .str association),
          ("structureParents", jsonNames parents),
          ("includedIn319ExplicitRootCount", .bool false),
          ("typeAxiomAuditScope", .str "ACTUAL_GENERATED_TYPE_VALUE_AXIOMS_POLICY_UNASSESSED")])

    emit "C29_SUMMARY_JSON" (Json.mkObj [
      ("status", .str "RUNTIME_DIAGNOSTIC_COMPLETE_NOT_SCIENTIFIC_ACCEPTANCE"),
      ("explicitRootsCompleted", toJson ordinal),
      ("explicitPrivateCompleted", toJson (resolved.filter fun r => r.1.privateRoot).size),
      ("generatedTargetOwnedConstants", toJson generatedCount),
      ("observedTargetOwnedConstants", toJson owned.length),
      ("actualStructureCount", toJson structureNames.size),
      ("generatedTypeValueAxiomAuditCompleted", toJson generatedCount),
      ("generatedAuditSchema", .str "C29_GENERATED_AUDIT_V2"),
      ("allExplicitNamesResolvedUniquely", .bool true),
      ("axiomPolicyPass", .null), ("sourceAgreement", .null),
      ("publicationBinding", .null), ("nativeAccepted", .bool false)])

end CubicBlindDiagnosticCandidate
