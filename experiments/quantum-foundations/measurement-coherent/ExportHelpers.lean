import Lean
import QuantumBlockEncoding.MeasurementCoherent

open Lean

private partial def references (e : Expr) (s : NameSet := {}) : NameSet :=
  match e with
  | .const n _ => s.insert n
  | .proj n _ body => references body (s.insert n)
  | .app f a => references a (references f s)
  | .lam _ t b _ | .forallE _ t b _ => references b (references t s)
  | .letE _ t v b _ => references b (references v (references t s))
  | .mdata _ b => references b s
  | _ => s

open Lean Elab Command in
elab "coherentHelperEvidence" : command => do
  let env ← getEnv
  let publicRoots := #[`QuantumBlockEncoding.MeasurementCoherent.branchIsometry,
    `QuantumBlockEncoding.MeasurementCoherent.branchIsometry_apply,
    `QuantumBlockEncoding.MeasurementCoherent.sum_inner_eq]
  let helperPrefix := "QuantumBlockEncoding.MeasurementCoherent.branchIsometry."
  let mut pending := publicRoots
  let mut seen : NameSet := {}
  let mut rows : Array Json := #[]
  while !pending.isEmpty do
    let root := pending.back!
    pending := pending.pop
    if seen.contains root then continue
    if rows.size ≥ 64 then throwError "bounded helper expansion exceeded"
    seen := seen.insert root
    let some ci := env.find? root | throwError "missing requested compiled constant"
    let some value := ci.value? (allowOpaque := true)
      | throwError "required compiled value unavailable"
    let refs := references value
    for child in refs.toArray do
      if child.toString.startsWith helperPrefix && !seen.contains child then
        pending := pending.push child
    let sorted := fun e => (references e).toArray.map Name.toString |>.qsort (· < ·)
    let type ← liftTermElabM <| Meta.ppExpr ci.type
    rows := rows.push <| Json.mkObj [
      ("name", toJson root.toString), ("checked_type", toJson type.pretty),
      ("generated_helper", toJson (root.toString.startsWith helperPrefix)),
      ("type_references", toJson (sorted ci.type)),
      ("value_references", toJson (sorted value))]
  let result := Json.mkObj [
    ("schema", "measurement-coherent.bounded-helper-expression-slice.v2"),
    ("lean_version", Lean.versionString),
    ("public_roots", toJson (publicRoots.map Name.toString)),
    ("scope", "Direct references at three public roots and their reachable generated branchIsometry helpers only; not whole-library transitive or minimal support."),
    ("rows", Json.arr rows)]
  logInfo s!"COHERENT_HELPERS|{result.compress}"

coherentHelperEvidence
