"""Offline profiles cannot discover providers or silently authorize generation."""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import digest, read_json, write_json
from qcb_operator_profile import (
    profile_schema,
    profile_template,
    read_operator_profile,
    validate_operator_profile,
)
from test_proof_session import task

spec = importlib.util.spec_from_file_location("qcb_evaluate_cli_test", B / "scripts/evaluate_agentic.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


def completed_profile():
    config = profile_template()
    config["adapter"] = {"id": "qcb_nonexistent_adapter:create", "revision_sha256": "a" * 64}
    config["model"] = {"id": "unit-test/no-endpoint", "revision": "b" * 40, "chat_template_sha256": "c" * 64}
    return config


class OperatorProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qcb-profile-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def invoke(self, *arguments):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(sys, "argv", ["evaluate_agentic.py", *map(str, arguments)]), redirect_stdout(output), redirect_stderr(errors):
            code = cli.main()
        return code, output.getvalue(), errors.getvalue()

    def test_template_requires_actual_metadata_and_does_not_fake_hashes(self):
        template = profile_template()
        self.assertEqual(template["model"], {"id": None, "revision": None, "chat_template_sha256": None})
        self.assertLessEqual(template["limits"]["max_calls"], 8)
        with self.assertRaises(ValueError):
            validate_operator_profile(template)
        template["limits"]["max_calls"] = 32
        self.assertEqual(profile_template()["limits"]["max_calls"], 8)
        self.assertEqual(validate_operator_profile(completed_profile()), completed_profile())

    def test_schema_and_runtime_cross_field_checks_are_both_required(self):
        for change in (lambda c: c["limits"].update(max_calls=33),
                       lambda c: c["model"].update(revision="main"),
                       lambda c: c["adapter"].update(id="not-an-import-reference")):
            config = completed_profile()
            change(config)
            with self.assertRaises(ValueError):
                validate_operator_profile(config)
        for change in (lambda c: c["session_limits"].update(wall_seconds=300),
                       lambda c: c["limits"].update(max_call_endpoint_cost_usd=1),
                       lambda c: c["limits"].update(max_calls=1.0)):
            config = completed_profile()
            change(config)
            self.assertEqual(list(Draft202012Validator(profile_schema()).iter_errors(config)), [])
            with self.assertRaises(ValueError):
                validate_operator_profile(config)

    def test_unknown_credential_field_is_rejected_without_echoing_value(self):
        config = completed_profile()
        config["api_key"] = "PRIVATE_CREDENTIAL_CANARY"
        with self.assertRaises(ValueError) as error:
            validate_operator_profile(config)
        self.assertNotIn("PRIVATE_CREDENTIAL_CANARY", str(error.exception))

    def test_profile_file_size_ceiling_precedes_parsing(self):
        path = self.directory / "oversized.json"
        path.write_text(" " * 65537)
        with self.assertRaisesRegex(ValueError, "64 KiB"):
            read_operator_profile(path)

    def test_offline_commands_never_load_task_registry_or_construct_provider(self):
        profile = self.directory / "profile.json"
        with patch.object(cli, "load_registry", side_effect=AssertionError("offline command read the task corpus")), \
                patch.object(cli, "run_episode", side_effect=AssertionError("offline command ran an episode")):
            code, output, _ = self.invoke("schema")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["type"], "object")
            code, output, _ = self.invoke("profile-template", "--purpose", "explanation_only", "--output", profile)
            self.assertEqual(code, 0)
            self.assertFalse(json.loads(output)["profile_ready_to_run"])
            self.assertEqual(read_json(profile)["condition"]["exposure"], "closed_book")
            path = self.directory / "complete.json"
            write_json(path, completed_profile())
            code, output, _ = self.invoke("validate-config", "--config", path)
            self.assertEqual(code, 0)
            result = json.loads(output)
            self.assertTrue(result["valid"])
            self.assertEqual(result["model_calls"], 0)
            self.assertFalse(result["candidate_execution_enabled"])

    def test_conflicting_flags_and_reused_output_fail_without_side_effects(self):
        path = self.directory / "preserved.json"
        path.write_text("preserve this exact content")
        code, _, _ = self.invoke("profile-template", "--output", path)
        self.assertEqual(code, 1)
        self.assertEqual(path.read_text(), "preserve this exact content")
        for args in (("schema", "--authorize-model"), ("validate", "--authorize-model"),
                     ("profile-template", "--purpose", "explanation_only", "--exposure", "approved_interface", "--output", self.directory / "new.json")):
            with patch.object(cli, "load_registry", side_effect=AssertionError("invalid arguments reached registry")):
                self.assertEqual(self.invoke(*args)[0], 1)
        self.assertFalse((self.directory / "new.json").exists())

    def test_formal_plan_and_authorized_run_do_not_import_nonexistent_adapter(self):
        fixed = task()
        view = {"task": fixed, "entry": {"task_hash": digest(fixed), "view_id": "software-test-only",
                                        "allowed_modes": ["root_only", "proof_dag"],
                                        "allowed_exposures": ["closed_book", "approved_interface"]},
                "registry_digest": "d" * 64, "reference_lineage": {}}
        config_path = self.directory / "operator.json"
        write_json(config_path, completed_profile())
        for command, flags, expected_code, expected_status in (("plan", [], 0, "dry_run"),
                                                               ("run", ["--authorize-model"], 2, "ENV_BLOCKED")):
            with patch.object(cli, "load_registry", return_value=({"software-test-only": deepcopy(view)}, {})), \
                    patch.object(cli.importlib, "import_module", side_effect=AssertionError("adapter import before execution gate")):
                code, output, _ = self.invoke(command, "--view", "software-test-only", "--config", config_path,
                                             "--episode-dir", self.directory / "never-created", "--adapter", "qcb_nonexistent_adapter:create", *flags)
            self.assertEqual(code, expected_code)
            result = json.loads(output)
            self.assertEqual(result["status"], expected_status)
            self.assertEqual(result["provider_calls"], 0)
            self.assertFalse(result["provider_constructed"])
            self.assertFalse(result["episode_directory_created"])
            self.assertFalse((self.directory / "never-created").exists())
            if command == "run":
                self.assertIn("isolated", result["reason"])


if __name__ == "__main__":
    unittest.main()
