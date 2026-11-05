"""Exact transport tests, not Hermite family acceptance."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

from audit_decimal_qasm import audit

MPS = Path(__file__).resolve().parents[2] / "mps"


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.qasm = self.root / "saved.qasm"
        self.manifest = self.root / "reference.json"

    def fixture(self, gates, body, qubits=2):
        self.manifest.write_text(json.dumps(
            {"schema_version": 1, "qubits": qubits, "gates": gates}), encoding="utf-8")
        self.qasm.write_text('OPENQASM 2.0;\ninclude "qelib1.inc";\n'
                             + f"qreg q[{qubits}];\n" + body, encoding="ascii")

    def test_decimal_is_not_the_binary_reference(self):
        self.fixture([["ry", (0.1).hex(), 0]], "ry(0.1) q[0];\n")
        result = audit(self.qasm, self.manifest)
        self.assertNotEqual(result["exact_decimal_operator_bound"], "0")
        self.assertEqual(result["parsed_binary64_operator_bound"], "0")
        self.assertFalse(result["scientific_root_closed"])

    def test_negative_and_subnormal_reference(self):
        angles = [-0.0, -0.375, float.fromhex("0x0.0000000000001p-1022")]
        self.fixture([["ry", x.hex(), 0] for x in angles],
                     "".join(f"ry({x:.17g}) q[0];\n" for x in angles))
        self.assertTrue(audit(self.qasm, self.manifest)
                        ["parsed_angles_exactly_equal_reference"])

    def test_actual_existing_writer_and_independent_auditor(self):
        sys.path.insert(0, str(MPS))
        from mps_ry_compiler import MPSPlan
        plan = MPSPlan(2, 1, [[(0, 1, .123)], [(0, 2, -.37)]],
                       0.0, 1.0, [1, 1, 1])
        gates = list(plan.gates())
        refs = [[g[0], g[1].hex(), g[2]] if g[0] == "ry" else list(g)
                for g in gates]
        self.manifest.write_text(json.dumps(
            {"schema_version": 1, "qubits": 3, "gates": refs}), encoding="utf-8")
        plan.write_qasm2(self.qasm)
        result = audit(self.qasm, self.manifest)
        self.assertEqual(result["instructions"], len(gates))
        self.assertEqual(result["status"], "SERIALIZATION_ONLY_PASS")
        self.assertEqual(result["parsed_binary64_operator_bound"], "0")

    def test_missing_files_never_pass(self):
        with self.assertRaises(FileNotFoundError):
            audit(self.qasm, self.manifest)
        self.fixture([], "")
        self.qasm.unlink()
        with self.assertRaises(FileNotFoundError):
            audit(self.qasm, self.manifest)

    def test_changed_physical_target_rejected(self):
        self.fixture([["ry", (0.1).hex(), 0]], "ry(0.1) q[1];\n")
        with self.assertRaises(ValueError):
            audit(self.qasm, self.manifest)

    def test_order_and_cx_wires_rejected(self):
        gates = [["ry", (0.1).hex(), 0], ["cx", 0, 1]]
        for body in ["cx q[0],q[1];\nry(0.1) q[0];\n",
                     "ry(0.1) q[0];\ncx q[1],q[0];\n"]:
            self.fixture(gates, body)
            with self.assertRaises(ValueError):
                audit(self.qasm, self.manifest)

    def test_missing_and_extra_gates_rejected(self):
        for gates, body in [([["ry", (0.1).hex(), 0]], ""),
                            ([], "ry(0.1) q[0];\n")]:
            self.fixture(gates, body)
            with self.assertRaises(ValueError):
                audit(self.qasm, self.manifest)

    def test_nonfinite_and_unsupported_literals_rejected(self):
        for token in ["nan", "inf", "1e999", "pi/2"]:
            self.fixture([["ry", (0.1).hex(), 0]], f"ry({token}) q[0];\n")
            with self.assertRaises(ValueError):
                audit(self.qasm, self.manifest)

    def test_invalid_reference_manifest_rejected(self):
        for gates in [[["cx", 0, 0]], [["ry", "inf", 0]],
                      [["ry", (0.1).hex(), True]], [["h", 0, 1]]]:
            self.fixture(gates, "")
            with self.assertRaises(ValueError):
                audit(self.qasm, self.manifest)

    def test_schema_version_has_exact_integer_type(self):
        for version in [True, False, 1.0, "1", None, 0, 2]:
            self.fixture([], "")
            data = json.loads(self.manifest.read_text(encoding="utf-8"))
            data["schema_version"] = version
            self.manifest.write_text(json.dumps(data), encoding="utf-8")
            with self.subTest(version=version, type=type(version).__name__):
                with self.assertRaises(ValueError):
                    audit(self.qasm, self.manifest)

    def test_same_wire_angle_permutation_reports_error_not_identity(self):
        self.fixture([["ry", (0.25).hex(), 0], ["ry", (-0.5).hex(), 0]],
                     "ry(-0.5) q[0];\nry(0.25) q[0];\n")
        result = audit(self.qasm, self.manifest)
        self.assertEqual(result["parsed_binary64_operator_bound"], "3/4")
        self.assertEqual(result["status"], "SERIALIZATION_ONLY_PASS")
        self.assertFalse(result["parsed_angles_exactly_equal_reference"])
        self.assertFalse(result["scientific_root_closed"])

    def test_empty_identity_is_transport_only(self):
        self.fixture([], "")
        result = audit(self.qasm, self.manifest)
        self.assertEqual(result["parsed_binary64_operator_bound"], "0")
        self.assertFalse(result["full_state_acceptance_verified"])


if __name__ == "__main__":
    unittest.main()
