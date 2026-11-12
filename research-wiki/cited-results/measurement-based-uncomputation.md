# Measurement-based uncomputation: bounded intake

| Result id | Source | Statement used | QBE status | Lean target | Used by | Reviewer note |
| --- | --- | --- | --- | --- | --- | --- |
| UNCOMPUTE-TEMP-AND-LOCAL | [Gu, Kemeny, Yelin and Lukin, arXiv:2610.22367v1](https://arxiv.org/html/2610.22367v1), Methods physical page 9, Eq. (12) | Current AND ancilla, destructive X measurement/reset, conditional CZ: both corrected branches preserve arbitrary retained complex amplitudes up to positive factor sqrt(2)/2; branch masses are half input mass. | obligation; isolated local component compiled, not canonically admitted | `ASPBE.Uncompute.MBU.correctedTemporaryAndBranch_eq`, `correctedTemporaryAndBranch_mass` in [temporary-and-c105](../../experiments/uncompute-2610-22367/temporary-and-c105/README.md) | Candidate cleanup supplier for value-to-amplitude and kickmix digestion; no certified downstream consumer yet | Direct local bra/sign algebra, not the whole Gaussian cleanup, arbitrary modified coefficient, channel API, resource result or SP/BE certificate. Source/formal independent reviews remain pending. |
| GIDNEY-TEMP-AND-PROVENANCE | [C. Gidney, *Halving the cost of quantum addition*, Quantum 2, 74 (2018), arXiv:1709.06648](https://arxiv.org/abs/1709.06648), cited as reference [29] by Gu et al. | Historical attribution for temporary-AND MBU. | paper-cited | No upstream-paper theorem/adaptor admitted by this intake | Attribution only | Bibliography verified in Gu et al. physical page 12; full Gidney paper not audited here. The local proof does not assume an unproved external theorem. |

The candidate uses the existing `QuantumBlockEncoding.hadamardMatrix` rather
than introducing a duplicate gate. It lives outside production Lean and is
explicitly `proved_locally`, pending the existing publication protocol. It
does not justify replacing inverse uncompute in any scientific target without
the exact current-function/phase/cleanup bridge and same-tier resource audit.
