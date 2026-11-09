"""Finite discriminators and binding checks, not mathematical or Lean admission."""
from pathlib import Path
from collections import Counter
import cmath
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / "HARNESS.md").is_file())


def mcx(controls, target, scratch):
    if len(controls) == 1:
        return [("cx", controls[0], target)]
    if len(controls) == 2:
        return [("ccx", *controls, target)]
    chain = [("ccx", controls[0], controls[1], scratch[0])]
    for index in range(1, len(controls) - 2):
        chain.append(("ccx", scratch[index - 1], controls[index + 1], scratch[index]))
    return chain + [("ccx", scratch[len(controls) - 3], controls[-1], target)] + list(reversed(chain))


def adder(m):
    # Q occupies 0..m-1, Y occupies m..2m-1, A follows.
    scratch = list(range(2 * m, 2 * m + max(m - 2, 0)))
    gates = []
    for j in range(m):
        for i in range(m - 1, j - 1, -1):
            gates += mcx([j] + list(range(m + j, m + i)), m + i, scratch)
    return gates


def apply_gates(bits, gates):
    for gate in gates:
        if all(bits[c] for c in gate[1:-1]):
            bits[gate[-1]] ^= 1


def vector_norm(v):
    return math.sqrt(sum(abs(z) ** 2 for z in v))


def inner(u, v):
    return sum(a.conjugate() * b for a, b in zip(u, v))


def rank_one_phase(v, s, delta):
    coef = inner(s, v)
    return [x + delta * coef * y for x, y in zip(v, s)]


def run():
    report = {"schema_version": "qcb.finite_discriminator_report.v1", "author": "/root/batch2_phase", "evidence_level": "finite_exact_boolean_and_floating_point_screens_only", "lean_run": False, "model_run": False, "admission_claim": False}
    rows = []
    for m in range(1, 8):
        gates = adder(m)
        counts = Counter(g[0] for g in gates)
        expected_t = m * (m - 1) * (2 * m - 1) // 6
        assert counts["cx"] == m and counts["ccx"] == expected_t
        cases = 0
        for q in range(1 << m):
            for y in range(1 << m):
                bits = [(q >> i) & 1 for i in range(m)] + [(y >> i) & 1 for i in range(m)] + [0] * max(m - 2, 0)
                apply_gates(bits, gates)
                q_out = sum(bits[i] << i for i in range(m))
                y_out = sum(bits[m + i] << i for i in range(m))
                assert q_out == q and y_out == (q + y) % (1 << m)
                assert not any(bits[2 * m:])
                cases += 1
        max_phase_residual = 0.0
        M = 1 << m
        gradient = [cmath.exp(2j * math.pi * y / M) / math.sqrt(M) for y in range(M)]
        for q in range(M):
            translated = [gradient[(z - q) % M] for z in range(M)]
            expected = [cmath.exp(-2j * math.pi * q / M) * z for z in gradient]
            residual = vector_norm([a - b for a, b in zip(translated, expected)])
            max_phase_residual = max(max_phase_residual, residual)
            assert residual < 5e-14
        rows.append({"m": m, "basis_cases": cases, "cnot": counts["cx"], "toffoli": counts["ccx"], "scratch": max(m - 2, 0), "maximum_fourier_residual": max_phase_residual})
    report["P1_adder_and_phase_screens"] = rows
    sharpness = []
    for eps in ([0.0], [0.0, 0.0], [0.1], [3.0], [0.1, 0.2, 0.0], [0.0, 3.0, 0.2], [0.2] * 16):
        r = vector_norm(eps)
        kappa = min(2.0, r)
        if r == 0:
            sharpness.append({"eps": list(eps), "bound": 0.0, "zero_case": True})
            continue
        s = [complex(x / r) for x in eps]
        delta = cmath.exp(2j * math.asin(kappa / 2)) - 1
        columns = []
        for j in range(len(eps)):
            e = [complex(i == j) for i in range(len(eps))]
            v = rank_one_phase(e, s, delta)
            err = vector_norm([a - b for a, b in zip(v, e)])
            assert err <= eps[j] + 2e-14
            columns.append(v)
        for j, a in enumerate(columns):
            for k, b in enumerate(columns):
                assert abs(inner(a, b) - (j == k)) < 2e-14
        vs = rank_one_phase(s, s, delta)
        assert abs(vector_norm([a - b for a, b in zip(vs, s)]) - kappa) < 2e-14
        sharpness.append({"eps": list(eps), "r": r, "bound_attained": kappa, "unitary_gram_residual_below": 2e-14})
    report["P2_unitary_tolerance_screens"] = sharpness
    interference = []
    for N in (2, 3, 4, 16, 64):
        s = [complex(1 / math.sqrt(N))] * N
        t = [complex(1 / math.sqrt(2)), complex(-1 / math.sqrt(2))] + [0j] * (N - 2)
        h = [(a + b) / math.sqrt(2) for a, b in zip(s, t)]
        k = rank_one_phase(h, s, -2)
        assert abs(inner(h, k)) < 2e-14
        assert abs(vector_norm([a - b for a, b in zip(h, k)]) - math.sqrt(2)) < 2e-14
        interference.append({"N": N, "column_error": 2 / math.sqrt(N), "operator_error": 2, "overlap_abs": abs(inner(h, k)), "vector_distance": vector_norm([a - b for a, b in zip(h, k)])})
    report["P2_interference_screens"] = interference
    snapshot = json.loads((REPO / "benchmarks/quantumcomputingbench/manifests/release-v3/snapshot.json").read_text())
    node_ids = {n["id"] for n in snapshot["nodes"]}
    bindings = []
    for slot in ("P1", "P2"):
        qpath = ROOT / "questions" / f"{slot}.json"
        apath = ROOT / "qa" / f"{slot}.json"
        q = json.loads(qpath.read_text())
        a = json.loads(apath.read_text())
        for field in ("core_id", "title", "question", "assumptions", "conventions", "source_refs", "target_nodes", "supporting_nodes"):
            assert q[field] == a[field], (slot, field)
        assert a["admission"] == "candidate_not_counted" and a["dedup_review_required"] is True
        assert sum(r["weight"] for r in a["rubric"]) == 10
        assert set(a["target_nodes"] + a["supporting_nodes"]) <= node_ids
        seen = {i["id"] for i in a["reasoning_map"]["inputs"]}
        for s in a["reasoning_map"]["steps"]:
            assert set(s["required_inputs"]) <= seen, (slot, s["id"])
            seen.add(s["id"])
        for source in a["source_refs"]:
            raw = (REPO / source["path"]).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == source["raw_sha256"]
            assert source["sha256"] == snapshot["input_hashes"][source["path"]]
        qhash = hashlib.sha256(qpath.read_bytes()).hexdigest()
        assert qhash == a["provenance"]["question_only_sha256"]
        bindings.append({"slot": slot, "question_sha256": qhash, "payload_sha256": hashlib.sha256(apath.read_bytes()).hexdigest(), "question_contract_equal": True, "rubric_total": 10, "source_hashes_match": True, "nodes_present_in_frozen_snapshot": True, "reasoning_map_backward_reference_check": True})
    report["binding_checks"] = bindings
    report["limitations"] = ["Exhaustive arithmetic checks cover widths 1 through 7 only; the arbitrary-width proof is the natural-language derivation, not this diagnostic.", "Floating-point screens test signs and representative examples only, not universal symbolic mathematics or a compiled circuit.", "Successful structural/source bindings do not establish independent review, semantic novelty, source fidelity of the new theorem, formal acceptance or split clearance."]
    out = ROOT / "evidence" / "phase-finite-checks.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"adder_widths": [1, 7], "basis_cases": sum(x["basis_cases"] for x in rows), "bindings": bindings, "report": str(out.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    run()
