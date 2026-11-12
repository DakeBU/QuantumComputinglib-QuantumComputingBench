import RadiusStability

noncomputable section
namespace QuantumBlockEncoding.ExperimentalRadiusStability
open HermitePolynomial

example : sourceLipschitzConstant 0 = 8 := by
  norm_num [sourceLipschitzConstant, ExperimentalCoefficientRange.coarseBound]

example : |smoothInitial 0 (-2)-smoothInitial 0 1| ≤ 24 := by
  have h := smoothInitial_lipschitz 0 (-2) 1
  norm_num [sourceLipschitzConstant, ExperimentalCoefficientRange.coarseBound] at h ⊢
  exact h

example : |smoothInitial 128 (-3/2)-smoothInitial 128 (-1/2)| ≤ sourceLipschitzConstant 128 := by
  simpa only [show |(-3/2 : ℝ)-(-1/2)|=1 by norm_num, mul_one]
    using smoothInitial_lipschitz 128 (-3/2) (-1/2)

example (R : ℝ) : radiusGrid 0 R ⟨1, by norm_num [gridSize]⟩ = 0 := by
  norm_num [radiusGrid, gridSize]

example :
    ‖NormedSpace.normalize (radiusVector 0 0 ((1/10^100 : ℚ) : ℝ))-
      ExperimentalNormalizationStability.targetVector 0 0 (1/10^100)‖ ≤
      2*Real.sqrt (gridSize (0+1) : ℝ)*sourceLipschitzConstant 0*
        |((1/10^100 : ℚ) : ℝ)-Real.pi*(1/10^100)| := by
  exact normalized_radius_error 0 0 (1/10^100) (by positivity) (1/10^100) (by positivity)

example :
    ‖NormedSpace.normalize (radiusVector 64 12 ((3217 : ℚ) : ℝ))-
      ExperimentalNormalizationStability.targetVector 64 12 1024‖ ≤
      2*Real.sqrt (gridSize (12+1) : ℝ)*sourceLipschitzConstant 64*
        |((3217 : ℚ) : ℝ)-Real.pi*1024| := by
  exact normalized_radius_error 64 12 1024 (by norm_num) 3217 (by norm_num)

end QuantumBlockEncoding.ExperimentalRadiusStability
