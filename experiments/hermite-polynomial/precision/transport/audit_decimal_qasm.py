"""Independent exact serialization diagnostic, never scientific acceptance.

Plain decimal QASM2 RY/CX only. Binary64 reference angles are interpreted as
exact dyadic rationals; textual decimals as exact decimal rationals. The
audit imports no quantum compiler, core generator, simulator or canonicalizer.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re

NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
RY = re.compile(rf"ry\(({NUMBER})\) q\[(\d+)\];")
CX = re.compile(r"cx q\[(\d+)\],q\[(\d+)\];")


def _wire(value, qubits):
    if type(value) is not int or not 0 <= value < qubits:
        raise ValueError("invalid wire")
    return value


def _reference(row, qubits):
    if not isinstance(row, list) or len(row) != 3:
        raise ValueError("invalid reference instruction")
    if row[0] == "ry":
        if not isinstance(row[1], str):
            raise ValueError("RY reference must be hexadecimal binary64 text")
        try:
            angle = float.fromhex(row[1])
        except ValueError as error:
            raise ValueError("invalid hexadecimal reference") from error
        if not math.isfinite(angle) or angle.hex() != row[1]:
            raise ValueError("noncanonical or nonfinite hexadecimal reference")
        return "ry", Fraction.from_float(angle), _wire(row[2], qubits)
    if row[0] == "cx":
        control, target = _wire(row[1], qubits), _wire(row[2], qubits)
        if control == target:
            raise ValueError("CX control equals target")
        return "cx", control, target
    raise ValueError("unsupported reference gate")


def audit(qasm_path: Path, manifest_path: Path):
    """Return measured transport only; any missing/mismatched input raises."""
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if (not isinstance(manifest, dict)
            or type(manifest.get("schema_version")) is not int
            or manifest["schema_version"] != 1):
        raise ValueError("unsupported reference schema")
    qubits = manifest.get("qubits")
    if type(qubits) is not int or qubits < 1:
        raise ValueError("invalid reference width")
    rows = manifest.get("gates")
    if not isinstance(rows, list):
        raise ValueError("reference gate list missing")
    refs = [_reference(row, qubits) for row in rows]
    decimal_sum, binary_sum = Fraction(), Fraction()
    parser_sum, rotations = Fraction(), 0
    digest = hashlib.sha256()
    # Stream actual saved bytes; preserve exact byte hash including newline.
    with qasm_path.open("rb") as stream:
        expected_header = ["OPENQASM 2.0;", 'include "qelib1.inc";',
                           f"qreg q[{qubits}];"]
        for expected in expected_header:
            raw = stream.readline()
            digest.update(raw)
            if raw.decode("ascii").strip() != expected:
                raise ValueError("unexpected saved QASM header")
        count = 0
        for raw in stream:
            digest.update(raw)
            if count >= len(refs):
                raise ValueError("extra saved instruction")
            line = raw.decode("ascii").strip()
            rotation, cnot = RY.fullmatch(line), CX.fullmatch(line)
            ref = refs[count]
            if rotation:
                token = rotation[1]
                if len(token) > 4096:
                    raise ValueError("literal length exceeds diagnostic budget")
                try:
                    decimal = Decimal(token)
                except InvalidOperation as error:
                    raise ValueError("invalid decimal literal") from error
                if not decimal.is_finite() or abs(decimal.as_tuple().exponent) > 4096:
                    raise ValueError("literal exponent exceeds diagnostic budget")
                text_angle = Fraction(decimal)
                parsed = float(decimal)
                if not math.isfinite(parsed):
                    raise ValueError("nonfinite parsed binary64 angle")
                target = int(rotation[2])
                if ref[0] != "ry" or target != ref[2]:
                    raise ValueError("RY position or physical target changed")
                binary_angle = Fraction.from_float(parsed)
                decimal_sum += abs(text_angle - ref[1])
                binary_sum += abs(binary_angle - ref[1])
                parser_sum += abs(binary_angle - text_angle)
                rotations += 1
            elif cnot:
                instruction = ("cx", int(cnot[1]), int(cnot[2]))
                if instruction != ref:
                    raise ValueError("CX position or physical wires changed")
            else:
                raise ValueError("unsupported saved instruction")
            count += 1
        if count != len(refs):
            raise ValueError("missing saved instruction")
    return {
        "schema_version": 1,
        "status": "SERIALIZATION_ONLY_PASS",
        "semantic_scope": "RY/CX positional transport; no compiler or state acceptance",
        "qubits": qubits, "instructions": count, "ry": rotations,
        "qasm_sha256": digest.hexdigest(),
        "reference_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "exact_decimal_operator_bound": str(decimal_sum / 2),
        "parsed_binary64_operator_bound": str(binary_sum / 2),
        "decimal_to_binary64_operator_bound": str(parser_sum / 2),
        "parsed_angles_exactly_equal_reference": binary_sum == 0,
        "matrix_norm": "Euclidean induced operator norm, conditional on formal RY/CX interpretation",
        "source_refinement_verified": False,
        "full_state_acceptance_verified": False,
        "uniform_numerical_certificate": False,
        "scientific_root_closed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qasm", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.qasm, args.manifest)
    except (OSError, ValueError, UnicodeError, OverflowError) as error:
        # No absolute paths or environment-sensitive exception strings.
        print(json.dumps({"status": "SERIALIZATION_ONLY_FAIL",
                          "reason_class": type(error).__name__,
                          "scientific_root_closed": False}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
