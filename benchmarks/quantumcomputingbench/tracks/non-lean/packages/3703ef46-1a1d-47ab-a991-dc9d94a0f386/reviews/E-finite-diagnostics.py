"""Small independent diagnostics for E1/E2, not a proof or residual certifier.

Uses exact rational arithmetic for the scalar residual search and ordinary
floating-point arithmetic for small complex-vector/matrix spot checks.
No model, Lean, circuit compiler, external service, or package installation.
"""
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path

import numpy as np


def scalar_residual_search():
    gains = list(map(Fraction, [0, 1, 4])) + [Fraction(1, 4)]
    approximations = list(map(Fraction, [-2, -1, 0, 1, 2, 4]))
    count = 0
    violations = []
    false_certificates = []
    for n in (2, 3):
        for gs in product(gains, repeat=n):
            for prefix in product(approximations, repeat=n):
                es = prefix + (Fraction(1),)
                eps = [abs(es[j] - gs[j] * es[j + 1]) for j in range(n)]
                beta = Fraction(0)
                weight = Fraction(1)
                for j in range(n):
                    beta += weight * eps[j]
                    weight *= gs[j]
                mass = weight
                count += 1
                if abs(es[0] - mass) > beta:
                    violations.append([n, str(gs), str(es)])
                if mass == 0 and es[0] - sum(eps) > 0:
                    if len(false_certificates) < 8:
                        false_certificates.append({
                            "n": n, "gains": list(map(str, gs)),
                            "approximate_environments": list(map(str, es)),
                            "residual_certificates": list(map(str, eps)),
                            "true_mass": str(mass), "weighted_beta": str(beta),
                            "false_naive_lower_bound": str(es[0] - sum(eps)),
                        })
    assert not violations
    assert false_certificates
    return {"arithmetic": "exact Fraction", "cases": count,
            "bound_violations": violations,
            "unweighted_false_positive_witnesses": false_certificates}


def geometry_search():
    count = active = extended = 0
    violations = []
    for qn, tn, pn in product(range(21), range(21), range(25)):
        q = qn / 20
        theta = math.pi * tn / 20
        phase = 2 * math.pi * pn / 24
        clean = np.array([q * np.exp(1j * phase) * math.cos(theta),
                          q * math.sin(theta)], dtype=complex)
        omega = np.concatenate([clean, [math.sqrt(max(0, 1 - q * q)), 0]])
        target = np.array([1, 0, 0, 0], dtype=complex)
        dist = float(np.linalg.norm(omega - target))
        count += 1
        if dist < 1 - 1e-12:
            active += 1
        if dist < math.sqrt(2) - 1e-12:
            extended += 1
            assert q > 0
            accepted_dist = float(np.linalg.norm(clean / q - target[:2]))
            if q * q + 1e-12 < (1 - dist * dist / 2) ** 2 or accepted_dist > dist + 1e-12:
                violations.append([qn, tn, pn])
    assert not violations
    return {"arithmetic": "floating-point finite vector checks", "cases": count,
            "cases_with_full_distance_less_than_one": active,
            "cases_with_full_distance_less_than_sqrt_two": extended,
            "violations": violations,
            "nonunit_output_counterexample": {
                "target": [1, 0], "output": [0.5, 0.5],
                "full_distance_squared": 0.5,
                "normalized_distance_squared": 2 - math.sqrt(2),
                "interpretation": "Dropping full-output unit norm can invalidate conditional contraction."
            }}


def completion(first):
    columns = [np.asarray(first, dtype=complex)]
    for basis in np.eye(len(first), dtype=complex):
        v = basis.copy()
        for col in columns:
            v -= col * np.vdot(col, v)
        norm = np.linalg.norm(v)
        if norm > 1e-10:
            columns.append(v / norm)
        if len(columns) == len(first):
            break
    return np.column_stack(columns)


def unitary_perturbation(rng, n, scale):
    m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = (m + m.conj().T) / 2
    vals, vecs = np.linalg.eigh(h)
    vals = vals / max(1, np.max(np.abs(vals)))
    return (vecs * np.exp(1j * scale * vals)) @ vecs.conj().T


def matrix_search():
    rng = np.random.default_rng(20261106)
    cases = 0
    maxima = {k: 0.0 for k in (
        "sandwich_identity_error", "exact_target_identity_error",
        "completion_invariance_error", "unitarity_defect",
        "error_bound_excess", "coefficient_bound_excess", "phase_bound_excess")}
    nontrivial = 0
    for selector, system, trial in product((1, 2, 3), (1, 2), range(30)):
        c = rng.normal(size=selector) + 1j * rng.normal(size=selector)
        if selector > 1 and trial % 3 == 0:
            c[-1] = 0
        alpha = sum(abs(c))
        left = np.sqrt(abs(c) / alpha).astype(complex)
        phase = np.ones(selector, dtype=complex)
        np.divide(c, abs(c), out=phase, where=(abs(c) != 0))
        right = phase * left
        scale = (0.0, 0.01, 0.08, 0.2, 0.5)[trial % 5]
        ql = unitary_perturbation(rng, selector, scale) @ completion(left)
        qr = unitary_perturbation(rng, selector, scale) @ completion(right)
        lt, rt = ql[:, 0], qr[:, 0]
        us = [unitary_perturbation(rng, system, 2) for _ in range(selector)]
        s = np.zeros((selector * system, selector * system), dtype=complex)
        for j, u in enumerate(us):
            s[j * system:(j + 1) * system, j * system:(j + 1) * system] = u
        st = unitary_perturbation(rng, selector * system, scale) @ s
        w = np.kron(ql.conj().T, np.eye(system)) @ st @ np.kron(qr, np.eye(system))
        block = w[:system, :system]
        cl = np.kron(lt.reshape(-1, 1), np.eye(system))
        cr = np.kron(rt.reshape(-1, 1), np.eye(system))
        target = sum(cj * uj for cj, uj in zip(c, us)) / alpha
        ideal = np.kron(left.conj().reshape(1, -1), np.eye(system)) @ s @ np.kron(right.reshape(-1, 1), np.eye(system))
        dl, dr = np.linalg.norm(lt - left), np.linalg.norm(rt - right)
        eta = np.linalg.norm(st - s, 2)
        budget = dl + dr + eta
        nontrivial += int(budget < 2)
        maxima["sandwich_identity_error"] = max(maxima["sandwich_identity_error"], float(np.linalg.norm(block - cl.conj().T @ st @ cr, 2)))
        maxima["exact_target_identity_error"] = max(maxima["exact_target_identity_error"], float(np.linalg.norm(ideal - target, 2)))
        maxima["unitarity_defect"] = max(maxima["unitarity_defect"], float(np.linalg.norm(w.conj().T @ w - np.eye(selector * system), 2)))
        maxima["error_bound_excess"] = max(maxima["error_bound_excess"], float(np.linalg.norm(block - target, 2) - min(2, budget)))
        coeff_error = sum(abs(np.conj(lt) * rt - c / alpha))
        maxima["coefficient_bound_excess"] = max(maxima["coefficient_bound_excess"], float(coeff_error - dl - dr))
        if selector > 1:
            diagonal = np.eye(selector, dtype=complex)
            diagonal[-1, -1] = -1
            qlp, qrp = ql @ diagonal, qr @ diagonal
            wp = np.kron(qlp.conj().T, np.eye(system)) @ st @ np.kron(qrp, np.eye(system))
            maxima["completion_invariance_error"] = max(maxima["completion_invariance_error"], float(np.linalg.norm(wp[:system, :system] - block, 2)))
            assert abs(np.linalg.norm(ql - qlp, 2) - 2) < 1e-10
        theta_l, theta_r = 0.37, -0.63
        zeta = np.exp(1j * (theta_r - theta_l))
        bphase = zeta * block
        shifted_bound = min(2, budget + abs(1 - zeta) * np.linalg.norm(target, 2))
        maxima["phase_bound_excess"] = max(maxima["phase_bound_excess"], float(np.linalg.norm(target - bphase, 2) - shifted_bound))
        cases += 1
    assert all(value < 1e-10 for value in maxima.values()), maxima
    return {"arithmetic": "floating-point finite matrix checks, tolerance 1e-10",
            "seed": 20261106, "cases": cases,
            "dimensions": "selector 1,2,3; system 1,2; largest matrix 6 by 6",
            "cases_with_uncapped_error_budget_below_two": nontrivial,
            "maxima": maxima}


if __name__ == "__main__":
    report = {"reviewer_actual_identity": "/root/batch2_review_composition",
              "scope": "Finite diagnostics only; no arbitrary-dimension proof, certified numerical residuals, resource theorem, or Lean compilation.",
              "scalar_residual_search": scalar_residual_search(),
              "conditional_geometry_search": geometry_search(),
              "lcu_matrix_search": matrix_search()}
    output = Path(__file__).with_name("E-finite-diagnostics.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
