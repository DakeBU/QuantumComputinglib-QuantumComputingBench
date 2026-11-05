# AxQM: pinned shared-foundation intake

Repository: https://github.com/Axiomatic-AI/AxQM
Paper: https://arxiv.org/abs/2609.05157v1
Inspected independent branch: `2ccf167efca86eb5164f1df8cedb72b84626b479`.
Upstream toolchain is Lean4.30.0-rc1 with a Mathlib fork; not a local dependency.
Credit Axiomatic AI, Winston Yin, Frank Koppens and the other paper authors.
Apache-2.0/NOTICE applies to upstream code/data; textbook rights remain separate.

Public tasks contain holes and reference solutions are private. Task/source
metadata are not local proof memory. Upstream reported task-dependency edges
must not be drawn as locally checked proof-term implications.

## First local preparatory fragment

See [the exact package](../../experiments/quantum-foundations/measurement-completeness/README.md).
It independently proves the pure-vector completeness/norm-mass substrate using
Mathlib, with no new state/channel/measurement type. Two exact Lean roots:

- `QuantumBlockEncoding.MeasurementProbability.sum_norm_sq_eq`;
- `QuantumBlockEncoding.MeasurementProbability.outcome_probability_mem_Icc`.

Their source, import, full types, checked smoke use, source pins, runtime evidence,
source-blind reconstruction and distinct semantic review live in that package.
State is `proved_locally_preparatory_fragment`, NOT production import availability,
main admission or PURIFIED. A genuine non-wrapper downstream consumer remains
open. Source/Mathlib retrieval is bounded, not a novelty/nonexistence proof.

Existing Born/effect stability at contribution `0bf8979ab4600d458288aa2c19eb95b065e2799a`
is prior distinct work. Reuse it rather than creating a parallel probability API.
The current QA proposal adds only partial support for existing public-test cores
plan-201/202. No new core, changed split, whole-question Lean view or gold label.

Next dependency-ready work: a real POVM/branch consumer on the canonical operator
API, then the pure-state rank-one/trace correspondence. Mixed-state updates,
instruments, dilation, tensor conventions and resource/circuit realization remain
separate obligations. OpenAI Math and the other recorded QIT libraries must share
the resulting reviewed semantic adapter, not acquire independent foundations.


## Coherent branch consumer checkpoint

The [coherent-branch package](../../experiments/quantum-foundations/measurement-coherent/README.md)
now consumes the preceding norm-mass theorem in the actual map
`MeasurementCoherent.branchIsometry`, using Mathlib's existing finite Hilbert
product and `LinearIsometry`. It proves the literal coordinate action and full
complex-overlap identity through that isometry; no second measurement/state API
is introduced. This closes the preparatory packet's internal non-wrapper-use
gap, not the separate production-textbook-consumer/admission obligation.

Exact source, pre-proof seal, independent source-blind reconstruction, distinct
static semantic acceptance, actual Lean4.33 consumers/signatures/axioms and a
bounded compiler-helper dependency observation are pinned in that package.
The portable fixed-source replay passes independently of the author's runner;
its initial dependency-parser failure remains preserved alongside the correction.
Status is still **proved_locally preparatory**, not production Graph/main/QA gold
or PURIFIED. Existing public-test plan-201/202 contracts and splits are unchanged;
the square-root/POVM, register, normalized block and mixed-state obligations
are not closed by this interface.
