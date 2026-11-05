-- SPDX-License-Identifier: Apache-2.0
-- New/modified exact integer transcription; see NOTICE and LICENSE.
-- Definitions ONLY, uncompiled candidate. No proofs or scientific error claim.
import Mathlib.Data.Int.Basic
import GaussianFixedWords

namespace UncomputeGaussian206

def bit (n i : Nat) : Nat := n / 2^i % 2

structure Digit where
  one : Nat
  two : Nat
  sign : Int

def digit (n i : Nat) : Digit :=
  let b0 := if i = 0 then 0 else bit n (2*i-1)
  let b1 := bit n (2*i)
  let b2 := bit n (2*i+1)
  let one := if b0 = b1 then 0 else 1
  let two := if one == 0 && b1 != b2 then 1 else 0
  { one := one, two := two, sign := 1-2*(b2 : Int) }

def address (y : Nat) : Nat := y / 2^25 % 1024
def localD (y : Nat) : Nat := y % 2^25
def localU (D : Nat) : Nat := D / 2^14
def a0 (j : Nat) : Nat := frozenWord j / 2^30 % 2^25
def slopeInitialStored (j : Nat) : Nat := frozenWord j % 2^19
def correctionPattern (j : Nat) : Nat := frozenWord j / 2^19 % 2^11
def correctionSigned (j : Nat) : Int :=
  let q := correctionPattern j
  if q < 2^10 then (q : Int) else (q : Int)-2^11

def truncSigned (z : Int) (shift keep : Nat) : Int :=
  z / (2 : Int)^(shift+keep) * (2 : Int)^keep

def midShift (t : Nat) : Nat := 15-2*t
def midLow (t : Nat) : Nat := max 2 ((9 : Int)-(midShift t : Int)).toNat

def middleRow (j D t : Nat) : Int :=
  let d := 256*correctionSigned j
  let u := digit (localU D) t
  u.sign*((u.one : Int)*truncSigned d (midShift t) (midLow t) +
    (u.two : Int)*truncSigned d (midShift t-1) (midLow t))

def modBits (z : Int) (n : Nat) : Nat := (z % (2 : Int)^n).toNat

def slopeUnbounded (j D : Nat) : Int :=
  4*(slopeInitialStored j : Int) +
    (List.range 6).foldl (fun s t => s+middleRow j D t) 0

def slopeStored (j D : Nat) : Nat :=
  (List.range 6).foldl
    (fun s t => modBits ((s : Int)+middleRow j D t / 4) 19)
    (slopeInitialStored j)

def slopeWord (j D : Nat) : Nat := 4*slopeStored j D
def finalDrop (i : Nat) : Nat := max 6 (2*i+5-18)
def finalShift (i : Nat) : Nat := 21-2*i

def finalRow (F D i : Nat) : Int :=
  let u := digit F i
  let drop := finalDrop i
  let sh := finalShift i
  let t1 := D / 2^(sh+drop) * 2^drop
  let t2 := D / 2^(sh-1+drop) * 2^drop
  u.sign*((u.one : Int)*(t1 : Int) + (u.two : Int)*(t2 : Int) +
    ((u.one+u.two : Nat) : Int)*(2 : Int)^(drop-1))

def finalSum (F D : Nat) : Int :=
  (List.range 9).foldl (fun s r => s+finalRow F D (r+2)) 0

def localIncrement (j D : Nat) : Int :=
  128*(a0 j : Int)-finalSum (slopeWord j D) D

def foldSigned (xs : Int) : Nat :=
  if 0 <= xs then xs.toNat else (-xs-1).toNat

def inDomain (xs : Int) : Prop := -(2 : Int)^35 <= xs ∧ xs < (2 : Int)^35

def increment (xs : Int) : Int :=
  localIncrement (address (foldSigned xs)) (localD (foldSigned xs))

def evaluateSigned (xs : Int) (k : Nat) : Option Nat :=
  letI : Decidable (inDomain xs) :=
    inferInstanceAs (Decidable (-(2 : Int)^35 <= xs ∧ xs < (2 : Int)^35))
  if inDomain xs ∧ k < 2^39 then some (modBits ((k : Int)+increment xs) 39) else none

def decode39 (p : Nat) : Int :=
  if p < 2^38 then (p : Int) else (p : Int)-(2 : Int)^39

def evaluatePattern (p k : Nat) : Option (Nat × Nat) :=
  if p < 2^39 then (evaluateSigned (decode39 p) k).map (fun out => (p,out)) else none

def regime (j : Nat) : Nat := if j < 455 then 0 else if j < 514 then 1 else 2

end UncomputeGaussian206
