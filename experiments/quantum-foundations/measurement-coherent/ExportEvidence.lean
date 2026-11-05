import Lean
import Lean.Util.FoldConsts
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
elab "coherentEvidence" : command => do
  let env ← getEnv
  let roots := #[`QuantumBlockEncoding.MeasurementCoherent.branchIsometry,
    `QuantumBlockEncoding.MeasurementCoherent.branchIsometry_apply,
    `QuantumBlockEncoding.MeasurementCoherent.sum_inner_eq]
  let mut rows : Array Json := #[]
  for root in roots do
    let some ci := env.find? root | throwError "missing required root"
    let some value := ci.value? (allowOpaque := true)
      | throwError "required root has no compiled value"
    let sorted := fun e => (references e).toArray.map Name.toString |>.qsort (· < ·)
    let type ← liftTermElabM <| Meta.ppExpr ci.type
    rows := rows.push <| Json.mkObj [
      ("name", toJson root.toString), ("checked_type", toJson type.pretty),
      ("type_references", toJson (sorted ci.type)),
      ("value_references", toJson (sorted value))]
  let result := Json.mkObj [
    ("schema", "measurement-coherent.compiled-expression-slice.v1"),
    ("lean_version", Lean.versionString),
    ("scope", "Exact roots; direct constant/projection references only, not transitive or minimal support."),
    ("rows", Json.arr rows)]
  logInfo s!"COHERENT_EVIDENCE|{result.compress}"

coherentEvidence
