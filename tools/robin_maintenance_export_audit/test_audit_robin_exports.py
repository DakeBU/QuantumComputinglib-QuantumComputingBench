"""Only mocked subprocesses. Synthetic observations are NOT Lean results."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import audit_robin_exports as audit

BASE = Path(__file__).parent
CASE_PAIRS = (
    "QuantumBlockEncoding.Examples.RobinHeat.OneTermRobinBlockEncodingProofRoute",
    "QuantumBlockEncoding.Examples.RobinHeat.oneTermRobinBlockEncodingProofRoute",
    "QuantumBlockEncoding.Examples.RobinHeat.RobinOracleComposition",
    "QuantumBlockEncoding.Examples.RobinHeat.robinOracleComposition",
)


def mock_observation(probe):
    """Read the genuinely written probe; fabricate output ONLY inside the mock."""
    output = []
    for line in probe.read_text(encoding="utf-8").splitlines():
        if line.startswith('#eval IO.println "'):
            output.append(line[len('#eval IO.println "'):-1])
        elif line.startswith("#check "):
            output.append(line[7:] + " : Nat")
        elif line.startswith("#print axioms "):
            name = line[len("#print axioms "):]
            # Exercise both modern generated native axioms and other additions.
            axioms = ("propext, Classical.choice, Quot.sound" if not name.endswith("robinOracleComposition")
                      else "propext, _private.Example.0._native.native_decide.ax_1, extraAxiom")
            output.append(f"'{name}' depends on axioms: [{axioms}]")
    return ("\n".join(output) + "\n").encode()


class AuditTests(unittest.TestCase):
    def setUp(self):
        # Every real fixture byte is confined to this new package and cleaned up.
        scratch = BASE / "test-tmp"
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="fixture-", dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.out = self.root / "_out/audit"
        self.names = list(CASE_PAIRS) + [f"Fixture.name{i}" for i in range(391)]
        self.rows = [dict(source=audit.MODULE, fullName=n, kind="def", line=i + 1,
                          experimental=True, openProof=False) for i, n in enumerate(self.names)]
        self.put(audit.MODULE, b"-- synthetic source, never compiled\n")
        self.put(audit.CATALOG, json.dumps(dict(declarations=self.rows)).encode())
        self.put("lean-toolchain", b"leanprover/lean4:v4.33.0\n")
        self.put("lakefile.lean", b"-- synthetic config\n")
        self.put("lake-manifest.json", b"{}\n")
        self.put(audit.OLEAN, b"synthetic olean, never loaded\n")
        self.binary = self.put("fake-prefix/bin/lean", b"synthetic binary, never executed\n")
        self.receipt_path = "_out/full/result.json"
        self.receipt = dict(full_Lean_Tests_success=True, input_bytes_unchanged=True,
                            Lean_version="Lean (version 4.33.0, synthetic test fixture)",
                            Lean_binary_sha256=audit.pin(self.binary)["sha256"],
                            inputs={p: audit.pin(self.root / p)["sha256"]
                                    for p in (audit.MODULE, *audit.CONFIGS)})
        self.put(self.receipt_path, json.dumps(self.receipt).encode())
        self.pin_patch = patch.object(audit, "EXPECTED_SOURCE_SHA256", audit.pin(self.root / audit.MODULE)["sha256"])
        self.pin_patch.start()
        self.addCleanup(self.pin_patch.stop)

    def put(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def fake_run(self, args, **kwargs):
        self.assertTrue(kwargs["capture_output"])
        self.assertEqual(kwargs["cwd"], self.root)
        self.assertGreater(kwargs["timeout"], 0)
        if args[-1] == "--print-prefix":
            stdout = (str(self.binary.parent.parent) + "\n").encode()
        elif args[-1] == "--version":
            stdout = (self.receipt["Lean_version"] + "\n").encode()
        elif "--deps" in args:
            stdout = (str(self.root / audit.OLEAN) + "\n").encode()
        else:
            self.assertEqual(args[:6], ["lake", "env", "lean", "-M1536", "-j1", args[-1]])
            stdout = mock_observation(self.root / args[-1])
        return subprocess.CompletedProcess(args, 0, stdout, b"")

    def run_audit(self, runner=None):
        with patch.object(audit.subprocess, "run", side_effect=runner or self.fake_run) as mocked:
            result = audit.audit(self.root, "_out/audit", self.receipt_path, 3)
        self.assertEqual(json.loads((self.out / "report.json").read_bytes()), result)
        return result, mocked

    def assert_failed(self, runner=None):
        result, mocked = self.run_audit(runner)
        self.assertIs(result["success"], False)
        self.assertEqual(result["status"], "failed")
        return result, mocked

    def test_mocked_complete_case_sensitive_coverage_and_raw_pins(self):
        result, mocked = self.run_audit()
        self.assertTrue(result["success"])
        self.assertEqual(mocked.call_count, 4)
        self.assertEqual(result["case_sensitive_unique_names"], 395)
        self.assertEqual([x["row"]["fullName"] for x in result["observations"][:4]], list(CASE_PAIRS))
        native = result["observations"][3]
        self.assertEqual(native["classification"], "additional-with-native-name-marker")
        self.assertIn("extraAxiom", native["additional_axioms"])
        self.assertEqual(len(native["native_name_markers"]), 1)
        for command in result["commands"]:
            self.assertEqual(audit.pin(self.out / command["stdout"]), command["stdout_pin"])
            self.assertEqual(audit.pin(self.out / command["stderr"]), command["stderr_pin"])

    def test_missing_required_file_never_runs_a_command(self):
        (self.root / "lake-manifest.json").unlink()
        _, mocked = self.assert_failed()
        mocked.assert_not_called()

    def test_missing_one_catalog_name(self):
        self.put(audit.CATALOG, json.dumps(dict(declarations=self.rows[:-1])).encode())
        _, mocked = self.assert_failed()
        mocked.assert_not_called()

    def test_true_exact_duplicate_is_not_a_case_pair(self):
        self.rows[-1]["fullName"] = self.rows[0]["fullName"]
        self.put(audit.CATALOG, json.dumps(dict(declarations=self.rows)).encode())
        result, _ = self.assert_failed()
        self.assertIn("exact duplicate", result["failure_reason"])

    def test_catalog_flag_is_not_silently_ignored(self):
        self.rows[0]["openProof"] = True
        self.put(audit.CATALOG, json.dumps(dict(declarations=self.rows)).encode())
        self.assert_failed()

    def test_stale_green_is_invalidated_before_validation(self):
        old = b'{"success":true,"old":"historical bytes"}\n'
        self.put("_out/audit/report.json", old)
        (self.root / audit.MODULE).unlink()
        self.assert_failed()
        archived = self.out / "history" / ("report-" + audit.digest(old) + ".json")
        self.assertEqual(archived.read_bytes(), old)

    def test_stale_green_is_invalidated_before_commands(self):
        self.put("_out/audit/report.json", b'{"success":true}\n')
        def check_then_fail(args, **kwargs):
            self.assertFalse(json.loads((self.out / "report.json").read_bytes())["success"])
            return subprocess.CompletedProcess(args, 1, b"full raw stdout\n", b"full raw stderr\n")
        result, _ = self.assert_failed(check_then_fail)
        entry = result["commands"][0]
        self.assertEqual((self.out / entry["stdout"]).read_bytes(), b"full raw stdout\n")
        self.assertEqual((self.out / entry["stderr"]).read_bytes(), b"full raw stderr\n")

    def test_tampered_source_pin_even_with_updated_receipt(self):
        self.put(audit.MODULE, b"-- changed source\n")
        self.receipt["inputs"][audit.MODULE] = audit.pin(self.root / audit.MODULE)["sha256"]
        self.put(self.receipt_path, json.dumps(self.receipt).encode())
        self.assert_failed()

    def test_no_subprocess_result(self):
        self.assert_failed(lambda *args, **kwargs: None)

    def test_success_exit_without_observations_cannot_green(self):
        def runner(args, **kwargs):
            result = self.fake_run(args, **kwargs)
            if "-M1536" in args:
                result.stdout = b""
            return result
        self.assert_failed(runner)

    def test_missing_signature_or_axiom_or_marker_cannot_green(self):
        for defect in ("signature", "axiom", "marker", "case"):
            with self.subTest(defect=defect):
                def runner(args, **kwargs):
                    result = self.fake_run(args, **kwargs)
                    if "-M1536" in args:
                        name = CASE_PAIRS[0].encode()
                        if defect == "signature":
                            result.stdout = result.stdout.replace(name + b" : Nat", b"", 1)
                        elif defect == "axiom":
                            result.stdout = re.sub(rb"'[^']+' depends on axioms: \[[^\]]+\]", b"", result.stdout, count=1)
                        elif defect == "marker":
                            result.stdout = result.stdout.replace(b"0000|END", b"0000|MISSING", 1)
                        else:
                            result.stdout = result.stdout.replace(name + b" : Nat", CASE_PAIRS[1].encode() + b" : Nat", 1)
                    return result
                self.assert_failed(runner)

    def test_wrong_dependency_binary_does_not_green(self):
        def runner(args, **kwargs):
            result = self.fake_run(args, **kwargs)
            if "--deps" in args:
                result.stdout = b"old-cache/QuantumBlockEncoding/RobinMatrix.olean\n"
            return result
        self.assert_failed(runner)

    def test_changed_source_or_olean_during_command(self):
        for path in (audit.MODULE, audit.OLEAN):
            with self.subTest(path=path):
                original = (self.root / path).read_bytes()
                def runner(args, **kwargs):
                    result = self.fake_run(args, **kwargs)
                    if "-M1536" in args:
                        self.put(path, original + b"tampered")
                    return result
                self.assert_failed(runner)
                self.put(path, original)

    def test_timeout_keeps_partial_raw_bytes(self):
        def runner(args, **kwargs):
            raise subprocess.TimeoutExpired(args, 3, output=b"partial stdout", stderr=b"partial stderr")
        result, _ = self.assert_failed(runner)
        entry = result["commands"][0]
        self.assertTrue(entry["timeout"])
        self.assertEqual((self.out / entry["stdout"]).read_bytes(), b"partial stdout")
        self.assertEqual((self.out / entry["stderr"]).read_bytes(), b"partial stderr")

    def test_failed_full_build_receipt(self):
        self.receipt["full_Lean_Tests_success"] = False
        self.put(self.receipt_path, json.dumps(self.receipt).encode())
        _, mocked = self.assert_failed()
        mocked.assert_not_called()

    def test_stale_full_build_input(self):
        self.put("lakefile.lean", b"-- stale config\n")
        self.assert_failed()

    def test_wrong_toolchain_binary(self):
        self.binary.write_bytes(b"changed fake binary")
        self.assert_failed()

    def test_unknown_print_format_fails_closed(self):
        rows = [dict(fullName="A.name")]
        raw = b"C368|n|0000|CHECK\nA.name : Nat\nC368|n|0000|AXIOMS\nunknown output\nC368|n|0000|END\n"
        with self.assertRaises(audit.AuditError):
            audit.parse_observations(raw, rows, "n")

    def test_parameter_binders_before_result_colon(self):
        for signature in (
            'A.name (rowIdx colIdx : Nat) (entries : List Entry) : Coeff',
            'A.name.{u_1} {rows cols : Nat}\n  (mat : Matrix rows cols Coeff) [Inhabited Coeff] : Rat',
            'A.name ⦃n : Nat⦄ (h : (n = n)) : True',
            'A.name (h : symbol "[(" = symbol "[(") : True',
            'A.name : Nat',
        ):
            with self.subTest(signature=signature):
                self.assertTrue(audit.exact_signature(signature, 'A.name'))

    def test_signature_prefix_rejects_malformed_or_wrong_case(self):
        for signature in ('A.Name (n : Nat) : Nat', 'A.name_extra : Nat',
                          'A.name (n : Nat)', 'A.name (n : Nat] : Nat',
                          'A.name (n : Nat : Nat', 'A.name (n : Nat) :',
                          'A.name unknown : Nat', 'A.name (h : "unterminated) : Nat'):
            with self.subTest(signature=signature):
                self.assertFalse(audit.exact_signature(signature, 'A.name'))

    def test_binder_signature_still_requires_all_ordered_axiom_markers(self):
        prefix='C368|n|0000|CHECK\nA.name (x : Nat) : Nat\nC368|n|0000|AXIOMS\n'
        suffix="'A.name' does not depend on any axioms\nC368|n|0000|END\n"
        raw=(prefix+suffix).encode()
        self.assertEqual(audit.parse_observations(raw,[dict(fullName='A.name')],'n')[0]['signature'],
                         'A.name (x : Nat) : Nat')
        for defective in (raw.replace(b'0000|END', b'0000|MISSING'),
                          raw.replace(b"'A.name'", b"'A.Name'"),
                          raw.replace(b' : Nat\nC368|n|0000|AXIOMS', b'\nC368|n|0000|AXIOMS')):
            with self.subTest(defective=defective):
                with self.assertRaises(audit.AuditError):
                    audit.parse_observations(defective,[dict(fullName='A.name')],'n')

    def test_actual_terminal_dagger_axioms_are_preserved_and_disclosed(self):
        plain='Fixture.theorem._native.native_decide.ax_1_1'
        dagger=plain+'✝'
        raw=("C368|n|0000|CHECK\nA.name (n : Nat) : Nat\nC368|n|0000|AXIOMS\n"
             + "'A.name' depends on axioms: [propext, " + plain + ', ' + dagger + "]\n"
             + "C368|n|0000|END\n").encode()
        result=audit.parse_observations(raw,[dict(fullName='A.name')],'n')[0]
        self.assertEqual(result['axioms'],['propext',plain,dagger])
        self.assertEqual(result['additional_axioms'],[plain,dagger])
        self.assertEqual(result['native_name_markers'],[plain,dagger])
        self.assertEqual(result['classification'],'additional-with-native-name-marker')
        for bad in (plain+'✝✝', plain+'💥', 'Fixture.✝name'):
            with self.subTest(bad=bad):
                self.assertIsNone(audit.AXIOM_NAME.fullmatch(bad))

    def test_actual_observed_axiom_line_grammar_and_synthetic_no_axioms(self):
        # The first axiom line is copied from a past actual Lean4.33 C346 stdout.
        # Signatures/markers and the second no-axioms block below are SYNTHETIC.
        names = ["HermiteSourceSuffix.actualSuffix", "Fixture.noAxioms"]
        raw = ("C368|n|0000|CHECK\nHermiteSourceSuffix.actualSuffix : Prop\nC368|n|0000|AXIOMS\n"
               "'HermiteSourceSuffix.actualSuffix' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
               "C368|n|0000|END\nC368|n|0001|CHECK\nFixture.noAxioms : Nat\nC368|n|0001|AXIOMS\n"
               "'Fixture.noAxioms' does not depend on any axioms\nC368|n|0001|END\n").encode()
        result = audit.parse_observations(raw, [dict(fullName=n) for n in names], "n")
        self.assertEqual([x["classification"] for x in result], ["ordinary-only", "no-axioms"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
