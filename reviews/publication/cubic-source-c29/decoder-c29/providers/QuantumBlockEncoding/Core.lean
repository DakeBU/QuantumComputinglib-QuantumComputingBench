import Std

   
                                    

                                                                              
                                                                                
                                                                               
                                                                   
  

namespace QuantumBlockEncoding

                                                  
abbrev Matrix (rows cols : Nat) (α : Type u) := Fin rows -> Fin cols -> α

namespace Matrix

                                              
def PointwiseEq {rows cols : Nat} {α : Type u}
    (a b : Matrix rows cols α) : Prop :=
  ∀ i j, a i j = b i j

                              
def zero (rows cols : Nat) (α : Type u) [OfNat α 0] : Matrix rows cols α :=
  fun _ _ => 0

                                  
def identity (n : Nat) (α : Type u) [OfNat α 0] [OfNat α 1] :
    Matrix n n α :=
  fun i j => if i = j then 1 else 0

                                                                                   
def mul {rows mid cols : Nat} {α : Type u}
    [OfNat α 0] [HAdd α α α] [HMul α α α]
    (a : Matrix rows mid α) (b : Matrix mid cols α) :
    Matrix rows cols α :=
  fun i j =>
    (List.finRange mid).foldl (fun acc k => acc + a i k * b k j) 0

end Matrix

                                                      
def gridSize (n : Nat) : Nat := 2 ^ n

   
                                                  

                                                                        
                        
  
def clog2 (m : Nat) : Nat :=
  if m <= 1 then 0 else Nat.log2 (m - 1) + 1

@[simp] theorem gridSize_zero : gridSize 0 = 1 := rfl

@[simp] theorem clog2_zero : clog2 0 = 0 := by
  simp [clog2]

@[simp] theorem clog2_one : clog2 1 = 0 := by
  simp [clog2]

                                                                           
theorem log2_pred_two_pow_succ (n : Nat) :
    Nat.log2 (2 ^ (n + 1) - 1) = n := by
  let x := 2 ^ (n + 1) - 1
  have hx : x ≠ 0 := by
    have h : 1 ≤ x := by
      induction n with
      | zero => decide
      | succ n _ =>
          dsimp [x]
          rw [Nat.pow_succ]
          rw [Nat.pow_succ]
          omega
    omega
  have hle : n ≤ Nat.log2 x := by
    rw [Nat.le_log2 hx]
    dsimp [x]
    induction n with
    | zero => simp
    | succ n _ =>
        rw [Nat.pow_succ]
        rw [Nat.pow_succ]
        omega
  have hlt : Nat.log2 x < n + 1 := by
    rw [Nat.log2_lt hx]
    dsimp [x]
    have h : 0 < 2 ^ (n + 1) := Nat.pow_pos (by decide : 0 < 2)
    omega
  exact Nat.le_antisymm (Nat.lt_succ_iff.mp hlt) hle

                                                 
@[simp] theorem clog2_gridSize (n : Nat) : clog2 (gridSize n) = n := by
  cases n with
  | zero => rfl
  | succ n =>
      simpa [Nat.succ_eq_add_one] using
        (show clog2 (gridSize (n + 1)) = n + 1 by
          simp [clog2, gridSize, log2_pred_two_pow_succ])

                                                   
inductive BoundaryKind where
  | periodic
  | robin
  | dirichlet
  | neumann
deriving Repr, DecidableEq

                                          
structure Stencil where
  derivativeOrder : Nat
  accuracyOrder : Nat
  leftRadius : Nat
  rightRadius : Nat
deriving Repr, DecidableEq

namespace Stencil

                                                                                  
def width (s : Stencil) : Nat :=
  s.leftRadius + s.rightRadius + 1

@[simp] theorem width_eq (s : Stencil) :
    s.width = s.leftRadius + s.rightRadius + 1 := rfl

end Stencil

   
                                                                             
                                                                          
                                                                   
  
structure BulkWindow where
  lower : Nat
  upper : Nat
deriving Repr, DecidableEq

namespace BulkWindow

                                                                                   
def paperBoundaryLines (w : BulkWindow) (n : Nat) : Nat :=
  w.lower + gridSize n - w.upper

end BulkWindow

                                                                       
inductive Coeff where
  | rat (q : Rat)
  | symbol (name : String)
  | add (a b : Coeff)
  | mul (a b : Coeff)
  | neg (a : Coeff)
deriving Repr, DecidableEq

namespace Coeff

instance : OfNat Coeff n where
  ofNat := Coeff.rat (OfNat.ofNat n)

instance : Neg Coeff where
  neg := Coeff.neg

instance : HAdd Coeff Coeff Coeff where
  hAdd := Coeff.add

instance : HMul Coeff Coeff Coeff where
  hMul := Coeff.mul

def sub (a b : Coeff) : Coeff := a + (-b)

instance : HSub Coeff Coeff Coeff where
  hSub := sub

                                                                            
def evalWith (env : String → Rat) : Coeff → Rat
  | rat q => q
  | symbol name => env name
  | add a b => evalWith env a + evalWith env b
  | mul a b => evalWith env a * evalWith env b
  | neg a => -(evalWith env a)

@[simp] theorem evalWith_rat (env : String → Rat) (q : Rat) :
    evalWith env (rat q) = q := rfl

@[simp] theorem evalWith_symbol (env : String → Rat) (name : String) :
    evalWith env (symbol name) = env name := rfl

@[simp] theorem evalWith_add (env : String → Rat) (a b : Coeff) :
    evalWith env (add a b) = evalWith env a + evalWith env b := rfl

@[simp] theorem evalWith_mul (env : String → Rat) (a b : Coeff) :
    evalWith env (mul a b) = evalWith env a * evalWith env b := rfl

@[simp] theorem evalWith_neg (env : String → Rat) (a : Coeff) :
    evalWith env (neg a) = -(evalWith env a) := rfl

                                                                   
theorem rat_zero : Coeff.rat 0 = Coeff.rat 0 := rfl

                                                                 
@[simp] theorem evalWith_rat_zero (env : String → Rat) :
    evalWith env (Coeff.rat 0) = (0 : Rat) := rfl

                                                                 
@[simp] theorem evalWith_rat_one (env : String → Rat) :
    evalWith env (Coeff.rat 1) = (1 : Rat) := rfl

                                                                         
theorem evalWith_rat_add (env : String → Rat) (a b : Rat) :
    evalWith env (Coeff.add (Coeff.rat a) (Coeff.rat b)) = a + b := by
  simp

                                                                         
theorem evalWith_rat_mul (env : String → Rat) (a b : Rat) :
    evalWith env (Coeff.mul (Coeff.rat a) (Coeff.rat b)) = a * b := by
  simp

                                                        
theorem evalWith_rat_neg (env : String → Rat) (a : Rat) :
    evalWith env (Coeff.neg (Coeff.rat a)) = -a := by
  simp

                                                                                    
theorem evalWith_eq_zero_of_rat_zero (env : String → Rat) :
    evalWith env (Coeff.rat 0) = (0 : Rat) := rfl

                                                                                    
theorem evalWith_eq_one_of_rat_one (env : String → Rat) :
    evalWith env (Coeff.rat 1) = (1 : Rat) := rfl

def divNat (a : Coeff) (n : Nat) : Coeff :=
  a * Coeff.rat ((1 : Rat) / n)

end Coeff

                                                             
structure StencilEntry where
  offset : Int
  coeff : Coeff
deriving Repr, DecidableEq

end QuantumBlockEncoding
