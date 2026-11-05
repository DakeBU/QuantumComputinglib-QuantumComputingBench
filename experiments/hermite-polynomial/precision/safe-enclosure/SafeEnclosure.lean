import DyadicSupplier
import Mathlib.Data.Rat.Floor
import Mathlib.Data.Nat.Size

/-! Computable safe dyadic angles from finite rational intervals.
The real angle is used only in correctness propositions, never to compute
the output. Sound intervals for actual Hermite source angles are an explicit
missing internal supplier, NOT new assumptions of a closed Source Anchor. -/
namespace QuantumBlockEncoding.SafeEnclosure
open PrimitiveCircuitPerturbation
open scoped Matrix.Norms.L2Operator

def midpoint (lo hi : ℚ) : ℚ := (lo+hi)/2

def nearestNumerator (bits : ℕ) (lo hi : ℚ) : ℤ :=
  Int.floor (midpoint lo hi * (2 : ℚ)^bits + 1/2)

def safeNumerator (bits : ℕ) (lo hi : ℚ) : Option ℤ :=
  if lo ≤ hi ∧ hi-lo ≤ 1/(2 : ℚ)^bits then
    some (nearestNumerator bits lo hi) else none

def safeAngle (bits : ℕ) (lo hi : ℚ) : Option ℚ :=
  (safeNumerator bits lo hi).map (DyadicSupplier.dyadicRat bits)

theorem safeNumerator_eq_some {bits : ℕ} {lo hi : ℚ} {m : ℤ}
    (h : safeNumerator bits lo hi = some m) :
    lo ≤ hi ∧ hi-lo ≤ 1/(2 : ℚ)^bits ∧ m = nearestNumerator bits lo hi := by
  unfold safeNumerator at h
  split_ifs at h with hv
  · exact ⟨hv.1, hv.2, (Option.some.inj h).symm⟩

theorem nearestNumerator_error (bits : ℕ) (lo hi : ℚ) :
    |midpoint lo hi - DyadicSupplier.dyadicRat bits (nearestNumerator bits lo hi)| ≤
      1 / (2*(2 : ℚ)^bits) := by
  have hd : (0 : ℚ) < 2^bits := by positivity
  have low := Int.floor_le (midpoint lo hi * (2 : ℚ)^bits + 1/2)
  have high := (Int.lt_floor_add_one (midpoint lo hi * (2 : ℚ)^bits + 1/2)).le
  unfold DyadicSupplier.dyadicRat nearestNumerator
  apply abs_le.mpr
  constructor <;> field_simp at * <;> nlinarith

theorem safeNumerator_error {bits : ℕ} {lo hi : ℚ} {m : ℤ} {theta : ℝ}
    (h : safeNumerator bits lo hi = some m)
    (lower : (lo : ℝ) ≤ theta) (upper : theta ≤ (hi : ℝ)) :
    |theta - (DyadicSupplier.dyadicRat bits m : ℝ)| ≤ 1/(2 : ℝ)^bits := by
  obtain ⟨ordered, width, hm⟩ := safeNumerator_eq_some h
  subst m
  have near : |((midpoint lo hi : ℚ) : ℝ) -
      (DyadicSupplier.dyadicRat bits (nearestNumerator bits lo hi) : ℝ)| ≤
        1/(2*(2 : ℝ)^bits) := by
    simpa only [Rat.cast_abs, Rat.cast_sub, Rat.cast_div, Rat.cast_mul,
      Rat.cast_pow, Rat.cast_one, Rat.cast_ofNat] using
      (show ((|midpoint lo hi - DyadicSupplier.dyadicRat bits (nearestNumerator bits lo hi)| : ℚ) : ℝ) ≤
        ((1/(2*(2 : ℚ)^bits) : ℚ) : ℝ) from Rat.cast_le.mpr (nearestNumerator_error bits lo hi))
  have wid : (hi : ℝ)-(lo : ℝ) ≤ 1/(2 : ℝ)^bits := by
    simpa only [Rat.cast_sub, Rat.cast_div, Rat.cast_pow, Rat.cast_one, Rat.cast_ofNat]
      using (Rat.cast_le (K := ℝ)).mpr width
  have mid : ((midpoint lo hi : ℚ) : ℝ) = ((lo : ℝ)+(hi : ℝ))/2 := by
    simp [midpoint]
  have center : |theta - ((midpoint lo hi : ℚ) : ℝ)| ≤ 1/(2*(2 : ℝ)^bits) := by
    have half : 2 * (1/(2*(2 : ℝ)^bits)) = 1/(2 : ℝ)^bits := by ring
    rw [mid]
    apply abs_le.mpr
    constructor <;> nlinarith [half]
  calc
    _ ≤ |theta - ((midpoint lo hi : ℚ) : ℝ)| +
      |((midpoint lo hi : ℚ) : ℝ) -
        (DyadicSupplier.dyadicRat bits (nearestNumerator bits lo hi) : ℝ)| :=
      abs_sub_le _ _ _
    _ ≤ 1/(2*(2 : ℝ)^bits) + 1/(2*(2 : ℝ)^bits) := add_le_add center near
    _ = _ := by ring

def supplyCircuit (bits : ℕ) : PrimitiveCircuit qubits → List (ℚ×ℚ) →
    Option (PrimitiveCircuit qubits)
  | [], [] => some []
  | [], _::_ => none
  | .ry target _::rest, (lo,hi)::intervals => do
      let m ← safeNumerator bits lo hi
      let tail ← supplyCircuit bits rest intervals
      pure (.ry target (.rational (DyadicSupplier.dyadicRat bits m)) :: tail)
  | .ry _ _::_, [] => none
  | .x target::rest, intervals =>
      (supplyCircuit bits rest intervals).map (.x target :: ·)
  | .rz target angle::rest, intervals =>
      (supplyCircuit bits rest intervals).map (.rz target angle :: ·)
  | .cx c t h::rest, intervals =>
      (supplyCircuit bits rest intervals).map (.cx c t h :: ·)

/-- Explicit internal supplier condition. No exact-real computation occurs in
this recursive consumer: it only states what an upstream enclosure must prove. -/
def Sound : PrimitiveCircuit qubits → List (ℚ×ℚ) → Prop
  | [], [] => True
  | [], _::_ => False
  | .ry _ angle::rest, (lo,hi)::intervals =>
      (lo : ℝ) ≤ angle.eval ∧ angle.eval ≤ (hi : ℝ) ∧ Sound rest intervals
  | .ry _ _::_, [] => False
  | .x _::rest, intervals | .rz _ _::rest, intervals | .cx _ _ _::rest, intervals =>
      Sound rest intervals

private theorem supplyCircuit_ry_some {bits : ℕ} {target : Fin qubits} {angle : ExactAngle}
    {rest : PrimitiveCircuit qubits} {lo hi : ℚ} {intervals : List (ℚ×ℚ)}
    {returned : PrimitiveCircuit qubits}
    (h : supplyCircuit bits (.ry target angle::rest) ((lo,hi)::intervals) = some returned) :
    ∃ m tail, safeNumerator bits lo hi = some m ∧
      supplyCircuit bits rest intervals = some tail ∧
      returned = .ry target (.rational (DyadicSupplier.dyadicRat bits m))::tail := by
  change (safeNumerator bits lo hi).bind (fun m =>
    (supplyCircuit bits rest intervals).bind (fun tail =>
      some (.ry target (.rational (DyadicSupplier.dyadicRat bits m))::tail))) = some returned at h
  obtain ⟨m,hs,hrest⟩ := Option.bind_eq_some_iff.mp h
  obtain ⟨tail,ht,he⟩ := Option.bind_eq_some_iff.mp hrest
  exact ⟨m,tail,hs,ht,(Option.some.inj he).symm⟩

theorem supplyCircuit_aligned {bits : ℕ} {exact returned : PrimitiveCircuit qubits}
    {intervals : List (ℚ×ℚ)} (sound : Sound exact intervals)
    (success : supplyCircuit bits exact intervals = some returned) :
    Aligned (1/(2 : ℝ)^bits) exact returned := by
  induction exact generalizing returned intervals with
  | nil =>
      cases intervals with
      | nil => simp only [supplyCircuit, Option.some.injEq] at success; subst returned; exact .nil
      | cons e es => simp [supplyCircuit] at success
  | cons g rest ih =>
      cases g with
      | ry target angle =>
          cases intervals with
          | nil => simp [supplyCircuit] at success
          | cons e es =>
              obtain ⟨lo,hi⟩ := e
              obtain ⟨m,tail,hs,ht,rfl⟩ := supplyCircuit_ry_some success
              exact .cons (.ry target angle _
                (safeNumerator_error hs sound.1 sound.2.1)) (ih sound.2.2 ht)
      | x target =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          exact .cons (.unchanged _) (ih sound ht)
      | rz target angle =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          exact .cons (.unchanged _) (ih sound ht)
      | cx c t h =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          exact .cons (.unchanged _) (ih sound ht)

/-- Erase only RY angle payloads; all constructors, ordered wire arguments,
and the complete non-RY gate (including RZ angle) remain visible. -/
def eraseRyAngle : PrimitiveGate qubits → PrimitiveGate qubits
  | .ry target _ => .ry target (.rational 0)
  | gate => gate

theorem supplyCircuit_chronology {bits : ℕ} {exact returned : PrimitiveCircuit qubits}
    {intervals : List (ℚ×ℚ)} (success : supplyCircuit bits exact intervals = some returned) :
    returned.map eraseRyAngle = exact.map eraseRyAngle := by
  induction exact generalizing returned intervals with
  | nil =>
      cases intervals with
      | nil => simp only [supplyCircuit, Option.some.injEq] at success; subst returned; rfl
      | cons e es => simp [supplyCircuit] at success
  | cons g rest ih =>
      cases g with
      | ry target angle =>
          cases intervals with
          | nil => simp [supplyCircuit] at success
          | cons e es =>
              obtain ⟨lo,hi⟩ := e
              obtain ⟨m,tail,hs,ht,rfl⟩ := supplyCircuit_ry_some success
              simp only [List.map_cons]; rw [ih ht]; rfl
      | x target =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]
      | rz target angle =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]
      | cx c t h =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]

def footprint (g : PrimitiveGate qubits) : ℕ×ℕ×Finset (Fin qubits) :=
  (g.oneQubitCount,g.twoQubitCount,g.touched)

theorem supplyCircuit_footprints {bits : ℕ} {exact returned : PrimitiveCircuit qubits}
    {intervals : List (ℚ×ℚ)} (success : supplyCircuit bits exact intervals = some returned) :
    returned.map footprint = exact.map footprint := by
  induction exact generalizing returned intervals with
  | nil =>
      cases intervals with
      | nil => simp only [supplyCircuit, Option.some.injEq] at success; subst returned; rfl
      | cons e es => simp [supplyCircuit] at success
  | cons g rest ih =>
      cases g with
      | ry target angle =>
          cases intervals with
          | nil => simp [supplyCircuit] at success
          | cons e es =>
              obtain ⟨lo,hi⟩ := e
              obtain ⟨m,tail,hs,ht,rfl⟩ := supplyCircuit_ry_some success
              simp only [List.map_cons]
              rw [ih ht]
              rfl
      | x target =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]
      | rz target angle =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]
      | cx c t h =>
          obtain ⟨tail,ht,he⟩ := Option.map_eq_some_iff.mp success
          subst returned
          simp only [List.map_cons]; rw [ih ht]

theorem supplyCircuit_length {bits : ℕ} {exact returned : PrimitiveCircuit qubits}
    {intervals : List (ℚ×ℚ)} (success : supplyCircuit bits exact intervals = some returned) :
    returned.length = exact.length := by
  simpa using congrArg List.length (supplyCircuit_footprints success)

theorem footprints_resource {a b : PrimitiveCircuit qubits}
    (shape : a.map footprint = b.map footprint) : a.resource = b.resource := by
  have one : a.oneQubitCount = b.oneQubitCount := by
    simpa only [PrimitiveCircuit.oneQubitCount, List.foldl_map, footprint] using
      congrArg (fun c : List (ℕ×ℕ×Finset (Fin qubits)) => c.foldl (fun t g => t+g.1) 0) shape
  have two : a.twoQubitCount = b.twoQubitCount := by
    simpa only [PrimitiveCircuit.twoQubitCount, List.foldl_map, footprint] using
      congrArg (fun c : List (ℕ×ℕ×Finset (Fin qubits)) => c.foldl (fun t g => t+g.2.1) 0) shape
  have wires : a.wireDepths = b.wireDepths := by
    have hw := congrArg (fun c : List (ℕ×ℕ×Finset (Fin qubits)) => c.foldl
      (fun d g => let layer := g.2.2.sup d
                  fun w => if w∈g.2.2 then layer+1 else d w) (fun _ => 0)) shape
    simp only [List.foldl_map] at hw
    exact hw
  simp only [PrimitiveCircuit.resource, PrimitiveCircuit.depth, one, two, wires]

theorem supplyCircuit_resource {bits : ℕ} {exact returned : PrimitiveCircuit qubits}
    {intervals : List (ℚ×ℚ)} (success : supplyCircuit bits exact intervals = some returned) :
    returned.resource = exact.resource :=
  footprints_resource (supplyCircuit_footprints success)

def ValidIntervals (bits : ℕ) (intervals : List (ℚ×ℚ)) : Prop :=
  ∀ e ∈ intervals, e.1 ≤ e.2 ∧ e.2-e.1 ≤ 1/(2 : ℚ)^bits

/-- Finite data validity and arity alone imply a successful return. This does
not ask a refinement loop to decide any exact-real floor bin. -/
theorem supplyCircuit_complete (bits : ℕ) (exact : PrimitiveCircuit qubits)
    (intervals : List (ℚ×ℚ)) (count : intervals.length = exact.ryCount)
    (valid : ValidIntervals bits intervals) :
    ∃ returned, supplyCircuit bits exact intervals = some returned := by
  induction exact generalizing intervals with
  | nil =>
      have hz : intervals.length=0 := by simpa [PrimitiveCircuit.ryCount] using count
      cases intervals with
      | nil => exact ⟨[],rfl⟩
      | cons e es => simp at hz
  | cons g rest ih =>
      cases g with
      | ry target angle =>
          cases intervals with
          | nil => simp [PrimitiveCircuit.ryCount] at count
          | cons e es =>
              obtain ⟨lo,hi⟩ := e
              have hv := valid (lo,hi) (by simp)
              have hcount : es.length=PrimitiveCircuit.ryCount rest := by
                simpa [PrimitiveCircuit.ryCount] using count
              have hvalid : ValidIntervals bits es := fun e he => valid e (by simp [he])
              obtain ⟨tail,ht⟩ := ih es hcount hvalid
              have hs : safeNumerator bits lo hi = some (nearestNumerator bits lo hi) :=
                if_pos hv
              exact ⟨.ry target (.rational (DyadicSupplier.dyadicRat bits
                (nearestNumerator bits lo hi)))::tail, by
                  simp [supplyCircuit, hs, ht]⟩
      | x target =>
          have hcount : intervals.length=PrimitiveCircuit.ryCount rest := by
            simpa [PrimitiveCircuit.ryCount] using count
          obtain ⟨tail,ht⟩ := ih intervals hcount valid
          exact ⟨.x target::tail, by simp [supplyCircuit,ht]⟩
      | rz target angle =>
          have hcount : intervals.length=PrimitiveCircuit.ryCount rest := by
            simpa [PrimitiveCircuit.ryCount] using count
          obtain ⟨tail,ht⟩ := ih intervals hcount valid
          exact ⟨.rz target angle::tail, by simp [supplyCircuit,ht]⟩
      | cx c t h =>
          have hcount : intervals.length=PrimitiveCircuit.ryCount rest := by
            simpa [PrimitiveCircuit.ryCount] using count
          obtain ⟨tail,ht⟩ := ih intervals hcount valid
          exact ⟨.cx c t h::tail, by simp [supplyCircuit,ht]⟩

/-- This bounds the integer output magnitude, not arithmetic runtime. -/
theorem nearestNumerator_magnitude (bits : ℕ) (lo hi : ℚ) :
    |(nearestNumerator bits lo hi : ℚ)| ≤
      |midpoint lo hi| * (2 : ℚ)^bits + 1/2 := by
  have low := Int.floor_le (midpoint lo hi * (2 : ℚ)^bits + 1/2)
  have high := (Int.lt_floor_add_one (midpoint lo hi * (2 : ℚ)^bits + 1/2)).le
  have ha := (abs_le.mp (le_refl |midpoint lo hi|))
  have hd : (0 : ℚ) ≤ 2^bits := by positivity
  have hlow := mul_le_mul_of_nonneg_right ha.1 hd
  have hhigh := mul_le_mul_of_nonneg_right ha.2 hd
  unfold nearestNumerator
  apply abs_le.mpr
  constructor <;> linarith

private theorem abs_rat_le_num (q : ℚ) : |q| ≤ (q.num.natAbs : ℚ) := by
  have hd : (1 : ℚ) ≤ q.den := by exact_mod_cast q.den_pos
  nth_rw 1 [← q.num_div_den]
  rw [abs_div, abs_of_nonneg (by positivity : (0 : ℚ) ≤ q.den)]
  have hn : |(q.num : ℚ)| = (q.num.natAbs : ℚ) := by simp
  rw [hn]
  exact div_le_self (by positivity) hd

theorem nearestNumerator_natAbs_bound (bits : ℕ) (lo hi : ℚ) :
    (nearestNumerator bits lo hi).natAbs ≤
      (lo.num.natAbs+hi.num.natAbs+1) * 2^bits := by
  have hmid : |midpoint lo hi| ≤ |lo|+|hi| := by
    unfold midpoint
    rw [abs_div]
    norm_num
    have ha := abs_add_le lo hi
    have hp : 0 ≤ |lo|+|hi| := by positivity
    linarith
  have hr := nearestNumerator_magnitude bits lo hi
  have hl := abs_rat_le_num lo
  have hh := abs_rat_le_num hi
  have hd : (1 : ℚ) ≤ 2^bits := one_le_pow₀ (by norm_num)
  have hb : |(nearestNumerator bits lo hi : ℚ)| ≤
      ((lo.num.natAbs : ℚ)+(hi.num.natAbs : ℚ)+1) * (2 : ℚ)^bits := by
    nlinarith
  have habs : |(nearestNumerator bits lo hi : ℚ)| =
      ((nearestNumerator bits lo hi).natAbs : ℚ) := by simp
  rw [habs] at hb
  exact_mod_cast hb

/-- Binary width of the unreduced grid denominator, an output storage bound. -/
theorem gridDenominator_bits (bits : ℕ) : Nat.size (2^bits) = bits+1 := Nat.size_pow

theorem numerator_bits_bound (bits : ℕ) (lo hi : ℚ) :
    Nat.size (nearestNumerator bits lo hi).natAbs ≤
      Nat.size (lo.num.natAbs+hi.num.natAbs+1) + bits := by
  apply Nat.size_le.mpr
  apply (nearestNumerator_natAbs_bound bits lo hi).trans_lt
  calc
    _ < 2^(Nat.size (lo.num.natAbs+hi.num.natAbs+1)) * 2^bits :=
      Nat.mul_lt_mul_of_pos_right (Nat.lt_size_self _) (by positivity)
    _ = _ := by rw [pow_add]

/-- Conditional INTERNAL consumer of the actual full cached source list.
Its soundness premise is the required missing enclosure-producer interface. -/
theorem hermite_internal_state_error (k n : ℕ) (L : ℝ) (hL : 0<L) (bits : ℕ)
    (intervals : List (ℚ×ℚ))
    (returned : PrimitiveCircuit ((n+1)+HermiteFiniteChain.bondQubits k))
    (sound : Sound (StagedGlobalAssembly.compile k n L hL).run.value intervals)
    (success : supplyCircuit bits (StagedGlobalAssembly.compile k n L hL).run.value intervals =
      some returned) :
    ‖DyadicSupplier.column (evalPrimitiveCircuit returned) - DyadicSupplier.target k n L‖ ≤
      DyadicSupplier.errorCoefficient k n / (2 : ℝ)^bits := by
  have alignment := supplyCircuit_aligned sound success
  have bound := aligned_eval_distance_le (by positivity) alignment
  have count : ((StagedGlobalAssembly.compile k n L hL).run.value.length : ℝ) ≤
      48 * ((n+1 : ℕ) : ℝ) * ((2*k+6 : ℕ) : ℝ)^3 := by
    exact_mod_cast StagedGlobalAssembly.compile_gateCount_polynomial k n L hL
  rw [← DyadicSupplier.exact_column_target k n L hL]
  apply (DyadicSupplier.column_error _ _).trans
  apply bound.trans
  calc
    _ ≤ (48 * ((n+1 : ℕ) : ℝ) * ((2*k+6 : ℕ) : ℝ)^3) *
      (1/(2 : ℝ)^bits)/2 := by gcongr
    _ = _ := by unfold DyadicSupplier.errorCoefficient; ring

theorem hermite_internal_epsilon (k n : ℕ) (L : ℝ) (hL : 0<L)
    {epsilon : ℝ} (he : 0<epsilon) (intervals : List (ℚ×ℚ))
    (returned : PrimitiveCircuit ((n+1)+HermiteFiniteChain.bondQubits k))
    (sound : Sound (StagedGlobalAssembly.compile k n L hL).run.value intervals)
    (success : supplyCircuit (DyadicSupplier.bitsFor k n epsilon)
      (StagedGlobalAssembly.compile k n L hL).run.value intervals = some returned) :
    ‖DyadicSupplier.column (evalPrimitiveCircuit returned) - DyadicSupplier.target k n L‖ ≤
      epsilon :=
  (hermite_internal_state_error k n L hL _ intervals returned sound success).trans
    (DyadicSupplier.bitsFor_error k n he)

/-- Actual successful return is supplied by the finite-data validator, not an
extra premise. Source-specific sound/valid enclosure generation remains the
explicit INTERNAL prerequisite; this is not a public source closure theorem. -/
theorem hermite_internal_supplier (k n : ℕ) (L : ℝ) (hL : 0<L)
    {epsilon : ℝ} (he : 0<epsilon) (intervals : List (ℚ×ℚ))
    (count : intervals.length =
      PrimitiveCircuit.ryCount (StagedGlobalAssembly.compile k n L hL).run.value)
    (valid : ValidIntervals (DyadicSupplier.bitsFor k n epsilon) intervals)
    (sound : Sound (StagedGlobalAssembly.compile k n L hL).run.value intervals) :
    ∃ returned,
      supplyCircuit (DyadicSupplier.bitsFor k n epsilon)
        (StagedGlobalAssembly.compile k n L hL).run.value intervals = some returned ∧
      returned.resource = (StagedGlobalAssembly.compile k n L hL).run.value.resource ∧
      returned.map eraseRyAngle =
        (StagedGlobalAssembly.compile k n L hL).run.value.map eraseRyAngle ∧
      ‖DyadicSupplier.column (evalPrimitiveCircuit returned) - DyadicSupplier.target k n L‖ ≤
        epsilon := by
  obtain ⟨returned,success⟩ := supplyCircuit_complete _ _ intervals count valid
  exact ⟨returned,success,supplyCircuit_resource success,supplyCircuit_chronology success,
    hermite_internal_epsilon k n L hL he intervals returned sound success⟩

namespace Tests
def physical : PrimitiveCircuit 2 :=
  [.ry 1 (.rational (1/10)), .cx 1 0 (by decide), .ry 0 (.rational (-1/10))]

#eval (supplyCircuit 3 physical [(1/10,1/10),(-1/10,-1/10)]).map
  (fun c => c.map (fun g => match g with
    | .ry t (.rational a) => ("ry",t.val,a)
    | .cx c t _ => ("cx",c.val,(t.val : ℚ))
    | _ => ("unsupported",0,0)))
#eval (supplyCircuit 3 physical []).isNone
#eval (supplyCircuit 3 physical [(1/10,1/10),(-1/10,-1/10),(0,0)]).isNone
#eval (supplyCircuit 3 physical [(0,1),(-1/10,-1/10)]).isNone
#eval safeNumerator 3 (-1/10) (-1/10)
#eval safeNumerator 3 (1/10) (1/10)
#eval safeNumerator 2 (-1/8) (-1/8)
#eval safeNumerator 2 (1/8) (1/8)
#eval safeNumerator 3 (-1/32) (1/32)
#eval safeNumerator 3 (7/32) (9/32)
#eval safeNumerator 3 1 0
#eval safeNumerator 3 0 1
#eval decide (safeNumerator 3 (-1/10) (-1/10) = some (-1))
#eval decide (safeNumerator 3 (1/10) (1/10) = some 1)
#eval decide (safeNumerator 2 (-1/8) (-1/8) = some 0)
#eval decide (safeNumerator 2 (1/8) (1/8) = some 1)
#eval decide (safeNumerator 3 (-1/32) (1/32) = some 0)
#eval decide (safeNumerator 3 (7/32) (9/32) = some 2)
#eval decide (safeNumerator 3 1 0 = none)
#eval decide (safeNumerator 3 0 1 = none)
example : safeNumerator 3 (-1/10) (-1/10) = some (-1) := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 3 (1/10) (1/10) = some 1 := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 2 (-1/8) (-1/8) = some 0 := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 2 (1/8) (1/8) = some 1 := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 3 (-1/32) (1/32) = some 0 := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 3 (7/32) (9/32) = some 2 := by
  norm_num [safeNumerator, nearestNumerator, midpoint]
example : safeNumerator 3 1 0 = none := by norm_num [safeNumerator]
example : safeNumerator 3 0 1 = none := by norm_num [safeNumerator]
end Tests

#print axioms nearestNumerator_error
#print axioms safeNumerator_error
#print axioms supplyCircuit_aligned
#print axioms supplyCircuit_resource
#print axioms supplyCircuit_chronology
#print axioms supplyCircuit_complete
#print axioms nearestNumerator_natAbs_bound
#print axioms numerator_bits_bound
#print axioms hermite_internal_state_error
#print axioms hermite_internal_epsilon
#print axioms hermite_internal_supplier
end QuantumBlockEncoding.SafeEnclosure
