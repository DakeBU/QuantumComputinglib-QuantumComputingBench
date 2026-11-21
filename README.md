# QuantumComputinglib · QuantumComputingBench

**A connected library of quantum mathematics, checked proofs, and questions for learning and evaluating AI.**

QuantumComputinglib explains quantum constructions, formalizes their mathematics in Lean, and connects reusable ideas through graphs. QuantumComputingBench turns this knowledge into training and evaluation tasks for specialized models.

[Website](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/) · [Bench repository](benchmarks/quantumcomputingbench/) · [Contribute](CONTRIBUTING.md)

## Explore

| | What you will find |
| --- | --- |
| [Lean libs & textbooks](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/library/) | Search declarations, or [read the mathematics](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/learning/). |
| [Lean Graph](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/lean-graph/) | Inspect library structure and formal proof dependencies where verified. |
| [Functor Hypergraph](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/functor-hypergraph/) | See how mathematical mechanisms can be combined, with their required assumptions. |
| [QuantumComputingBench](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/) | Practice, train and evaluate quantum mathematics through two complementary tracks. |

## See what we do

Suppose we want to prepare a quantum state. ASPBE (Automatic State Preparation and Block Encoding) searches for circuits and checks successful candidates: the unitary must map the all-zero input to the requested normalized state. In a matrix representation, this means its first column must be the target vector.

```math
U|0^n\rangle=|\psi\rangle.
```

<p align="center"><img src="docs/assets/state_preparation_first_column.svg" alt="The first column of a unitary matrix is the state prepared from the all-zero input" width="760"></p>

[Try the one-qubit example](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/reading-guide/) · [See verified constructions](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/example-cases/) · [Build your own task](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/task-builder/)

## QuantumComputingBench

| Mode | Ability evaluated |
| --- | --- |
| **Non-agentic Mathematical QA** | Knowledge, derivations, assumptions and proofs without tools. |
| **Agentic Lean-assisted QA** | Interactive mathematical proof using Lean and verifier feedback. |

Both tracks are grounded in the Lean Graph and Functor Hypergraph. Dependency reasoning and optional graph-given proof planning are shared capabilities, not another dataset. Whole-domain coverage is currently in development; public answers are not hidden test data. [Run or download tasks](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/run/) · [Benchmark standard](benchmarks/quantumcomputingbench/BENCHMARK_STANDARD.md) · [Contributor goals](benchmarks/quantumcomputingbench/CONTRIBUTOR_GOALS.md)

## News

- **18 November 2026.** [Lean course v6](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/quantumcomputingbench/run/course-v6/) reaches 25 shared mathematical cores, adding orientation and wire-order proofs.
- **21 October 2026.** [QuantumComputingBench starts](benchmarks/quantumcomputingbench/), a graph-grounded benchmark for specialized mathematical models.
- **10 September 2026.** A [smooth-state preparation result](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/example-cases/hermite-smooth-state-preparation/) gives a linear logical gate bound for fixed polynomial degree under exact-real assumptions; finite-bit compilation remains open.
- **14 August 2026.** The selected [Robin block-encoding construction](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/case-studies/robin/) reduces its audited branch from 49 to 30 $T^{\dagger 3}$ gates and 52 to 32 CNOTs under the same register contract.

[Full project history and technical guide](PROJECT_GUIDE.md) · [Current research agenda](https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/math-2-0/)

## Build and contribute

Use [the local build guide](PROJECT_GUIDE.md#lean-library) for the pinned Lean toolchain, tests and site. Follow [the repository agent goal](benchmarks/quantumcomputingbench/AGENT_GOAL.md) and the [continuation goals](benchmarks/quantumcomputingbench/CONTRIBUTOR_GOALS.md) for benchmark contributions.

## Citation

```bibtex
@misc{aspbe2026,
  author = {Bu, Dake and Huang, Xiajie and Lv, Outongyi and Liu, Nana and Nitanda, Atsushi and Wong, Hau-san and Zhang, Qingfu},
  title = {{ASPBE: Automatic State Preparation and Block Encoding for Quantum Computing}},
  year = {2026},
  note = {QuantumComputinglib and project source: \url{https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench}}
}
```

[MIT license](LICENSE) · [Third-party licenses and reuse](LICENSES/REUSE.md) · [Attribution](docs/attribution.md)
