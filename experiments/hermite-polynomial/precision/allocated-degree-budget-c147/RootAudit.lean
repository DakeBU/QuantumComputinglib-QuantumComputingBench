import AllocatedDegreeBudget

/-! Audit commands only. A successful future execution must be recorded
against the exact source and provider bytes; this text is not a verdict. -/

set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
set_option pp.proofs true

#check HermiteFiniteExp.tailCutoff
#print HermiteFiniteExp.tailCutoff
#check HermiteFiniteExpDegree.sourceDegree
#print HermiteFiniteExpDegree.sourceDegree
#check HermiteFiniteExpDegree.degree
#print HermiteFiniteExpDegree.degree
#check HermiteFiniteExpDegree.halfDegree
#print HermiteFiniteExpDegree.halfDegree
#check HermitePiecewiseSourceBudget.sourceDelta
#print HermitePiecewiseSourceBudget.sourceDelta
#check HermiteFiniteMiddleSource.amplificationQ
#print HermiteFiniteMiddleSource.amplificationQ

#check Nat.ceil_le
#check Nat.ceil_pos
#check Nat.le_ceil
#check Nat.clog_le_iff_le_pow
#check Nat.le_pow_clog
#check HermiteFiniteExpDegree.degree_formula
#print axioms HermiteFiniteExpDegree.degree_formula

#check HermiteAllocatedDegreeBudget.tailCutoff_div_pow_two_le
#print HermiteAllocatedDegreeBudget.tailCutoff_div_pow_two_le
#print axioms HermiteAllocatedDegreeBudget.tailCutoff_div_pow_two_le
#check HermiteAllocatedDegreeBudget.sourceDelta_factorization
#print HermiteAllocatedDegreeBudget.sourceDelta_factorization
#print axioms HermiteAllocatedDegreeBudget.sourceDelta_factorization
#check HermiteAllocatedDegreeBudget.allocated_tailCutoff_le
#print HermiteAllocatedDegreeBudget.allocated_tailCutoff_le
#print axioms HermiteAllocatedDegreeBudget.allocated_tailCutoff_le
#check HermiteAllocatedDegreeBudget.allocated_sourceDegree_le
#print HermiteAllocatedDegreeBudget.allocated_sourceDegree_le
#print axioms HermiteAllocatedDegreeBudget.allocated_sourceDegree_le
