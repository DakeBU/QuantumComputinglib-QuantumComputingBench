import Lean
import Lean.Util.FoldConsts
import QuantumBlockEncoding.MeasurementProbability

/-! Fixed-slice compiled-expression observation, not a verifier or a claim of
minimal mathematical support. Type and proof references remain separate. -/
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
elab "measurementIntakeGraph" : command => do
  let env ← getEnv
  let roots := #[`QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq,
    `QuantumBlockEncoding.MeasurementProbability.outcome_probability_mem_Icc]
  let mut rows : Array Json := #[]
  for root in roots do
    let some ci := env.find? root | throwError "missing required root"
    let some value := ci.value? (allowOpaque := true)
      | throwError "required root has no compiled proof value"
    let sorted := fun e => (references e).toArray.map Name.toString |>.qsort (· < ·)
    rows := rows.push <| Json.mkObj [
      ("name", toJson root.toString), ("type_references", toJson (sorted ci.type)),
      ("proof_references", toJson (sorted value))]
  let result := Json.mkObj [
    ("schema", "measurement.compiled_expression_slice.v1"),
    ("lean_version", Lean.versionString),
    ("scope", "Two exact roots; direct constant and projection-structure references, not transitive closure, minimal support or whole-library graph."),
    ("rows", Json.arr rows)]
  logInfo s!"MEASUREMENT_GRAPH|{result.compress}"

measurementIntakeGraph
