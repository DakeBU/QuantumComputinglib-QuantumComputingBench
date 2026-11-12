-- SPDX-License-Identifier: Apache-2.0
-- Consumer candidate: bind the actual imported theorem to the exact C229 type.
import GaussianConstancyProof

open UncomputeGaussian206

#check localIncrement_block128_constancy
#check (localIncrement_block128_constancy :
  ∀ (j D : Nat), j < 1024 → D < 2^25 →
    localIncrement j D = localIncrement j (128*(D/128)))

example : ∀ (j D : Nat), j < 1024 → D < 2^25 →
    localIncrement j D = localIncrement j (128*(D/128)) :=
  localIncrement_block128_constancy

#print localIncrement_block128_constancy
#print axioms localIncrement_block128_constancy
