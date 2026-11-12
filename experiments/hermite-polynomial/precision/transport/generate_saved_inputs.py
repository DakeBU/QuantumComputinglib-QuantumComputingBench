"""Generate finite source-instance saved transport inputs; NOT a certificate.

This invokes the existing floating compiler. The reference manifest captures
its actual binary64 instructions, not the exact Lean compiler. Independent
auditing and saved-circuit source replay are separate commands.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from unittest import mock

MPS = Path(__file__).resolve().parents[2] / "mps"
sys.path.insert(0, str(MPS))
from mps_core_probe import TT
from mps_stable_cores import stable_hermite_tt
from mps_ry_compiler import compile_mps


def generate(n, k, length, output):
    output.mkdir(parents=True, exist_ok=True)
    with mock.patch.object(TT, "small_dense_diagnostic",
                           side_effect=AssertionError("dense constructor forbidden")):
        raw, source_metadata = stable_hermite_tt(n, k, Fraction(length))
        plan = compile_mps(raw)
        gates = list(plan.gates())
        rows = [[g[0], g[1].hex(), g[2]] if g[0] == "ry" else list(g)
                for g in gates]
        plan.write_qasm2(output / "saved.qasm")
    reference = {
        "schema_version": 1, "qubits": n + plan.ancillas, "gates": rows,
        "provenance": "Actual existing floating compiler gate iteration",
        "n": n, "k": k, "L": length,
        "exact_Lean_producer_refinement": False,
    }
    (output / "reference.json").write_text(json.dumps(reference, indent=2) + "\n",
                                            encoding="utf-8")
    return {
        "status": "FINITE_SOURCE_TRANSPORT_INPUTS_GENERATED",
        "n": n, "k": k, "L": length, "instructions": len(rows),
        "resource_counts": plan.resource_counts,
        "source_metadata": source_metadata,
        "dense_constructor_forbidden": True,
        "qasm_sha256": hashlib.sha256((output / "saved.qasm").read_bytes()).hexdigest(),
        "reference_sha256": hashlib.sha256((output / "reference.json").read_bytes()).hexdigest(),
        "exact_Lean_producer_refinement": False,
        "scientific_root_closed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--L", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.n, args.k, args.L, args.output), indent=2))


if __name__ == "__main__":
    main()
