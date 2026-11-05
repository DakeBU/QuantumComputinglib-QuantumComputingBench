"""Offline task/response boundaries; fixtures are not model or Lean runs."""
import hashlib
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path, PurePosixPath
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_bench_runtime import (
    _source_roots,
    _task,
    bundle,
    export_records,
    prepare_run,
    public_index,
    read_jsonl,
    response_template,
    review_pack,
    review_template,
    score,
    smoke,
    verify_downloads,
    write_downloads,
    write_jsonl,
)
from qcb_core import digest


def registry_fixture():
    tasks = []
    rubric = [{"id": "c1", "criterion": "Give a valid mathematical argument.", "weight": 2}]
    for i, decision in enumerate(("holds", "refuted")):
        tasks.append(_task("semantic", "case" + str(i), ["core-1"], "test_public", "Question",
                           {"question": "Does the statement hold?", "response_format": {"decision": "holds|refuted"}},
                           {"target_nodes": ["node-1"]}, {"answer": "REFERENCE_NOT_A_PROMPT", "decision": decision, "rubric": rubric},
                           pair_id="PAIR_PRIVATE", contract_hashes={"core-1": "contract"}))
    tasks.append(_task("nonlean", "nl", ["core-2"], "train", "NL", {"question": "Explain."}, {},
                       {"answer": "OTHER_PRIVATE_REFERENCE", "rubric": rubric}))
    tasks.append(_task("lean", "lean", ["core-2"], "train", "Lean", {"question": "Prove it.", "imports": ["Example"]}, {},
                       {"rubric": [], "proof_export_available": False}))
    return {"registry_hash": digest({"tasks": tasks, "sources": {"snapshot": "s"}, "runtime_sources": {"verifier.py": "1" * 64}}), "source_commit": "f" * 40, "source_identities": {"snapshot": "s"},
            "runtime_sources": {"verifier.py": "1" * 64}, "tasks": tasks, "summary": {"task_views": 4}}


class BenchRuntimeTests(unittest.TestCase):
    def test_standalone_grader_at_container_filesystem_root_has_no_repo_requirement(self):
        base, root = _source_roots(PurePosixPath("/grader/qcb_bench_runtime.py"))
        self.assertEqual(str(base), "/")
        self.assertEqual(str(root), "/")

    def setUp(self):
        self.registry = registry_fixture()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def prepare(self, **kw):
        return prepare_run(self.registry, self.root / "run", **kw)

    def oracle(self, manifest):
        tasks = [t for t in self.registry["tasks"] if t["track"] == "semantic"]
        rows = response_template(tasks, manifest["run_id"])
        for row, task in zip(rows, tasks):
            row.update(status="answered", answer={"decision": task["reference"]["decision"], "explanation": "An alternative valid derivation."})
        return rows

    def test_gold_independent_task_hash_and_separate_index(self):
        a = _task("semantic", "a", ["c"], "train", "T", {"question": "P?"}, {}, {"decision": "holds"}, pair_id="p")
        b = _task("semantic", "a", ["c"], "train", "T", {"question": "P?"}, {}, {"decision": "refuted"}, pair_id="other")
        self.assertEqual(a["task_hash"], b["task_hash"])
        self.assertNotEqual(digest(a), digest(b))
        text = json.dumps(public_index(self.registry))
        self.assertNotIn("REFERENCE_NOT_A_PROMPT", text)
        self.assertNotIn("PAIR_PRIVATE", text)

    def test_eval_export_has_only_inputs_and_training_cannot_cross_split(self):
        rows = export_records(self.registry, split="test_public")
        self.assertEqual(len(rows), 2)
        self.assertEqual(set(rows[0]), {"schema_version", "task_id", "task_hash", "input"})
        train = export_records(self.registry, purpose="training")
        self.assertEqual(len(train), 1)
        self.assertEqual(train[0]["split"], "train")
        self.assertIn("reference", train[0])
        self.assertEqual([m["role"] for m in train[0]["messages"]], ["user", "assistant"])
        self.assertEqual(json.loads(train[0]["messages"][1]["content"]), {"explanation": "OTHER_PRIVATE_REFERENCE"})
        for kw in ({"split": "test_public"}, {"split": "dev"}, {"track": "lean"},
                   {"task_ids": [self.registry["tasks"][0]["task_id"]]}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                export_records(self.registry, purpose="training", **kw)

    def test_prepared_agent_folder_excludes_gold_and_operator_metadata(self):
        manifest = self.prepare()
        text = (self.root / "run/input/tasks.jsonl").read_text()
        self.assertNotIn("REFERENCE_NOT_A_PROMPT", text)
        self.assertNotIn("PAIR_PRIVATE", text)
        self.assertNotIn("core-1", text)
        self.assertFalse(manifest["model_generation_authorized"])
        self.assertEqual(manifest["budget"]["max_model_calls"], 0)
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_lean_closed_book_rejected_before_creating_run(self):
        with self.assertRaises(ValueError):
            self.prepare(split="train", track="lean")
        self.assertFalse((self.root / "run").exists())

    def test_oracle_wrong_abstained_blocked_missing_are_distinct(self):
        manifest = self.prepare()
        oracle = self.oracle(manifest)
        report = score(self.registry, manifest, oracle)
        self.assertEqual(report["decision_accuracy_over_planned"], 1)
        self.assertEqual(report["pair_joint_accuracy_over_selected_pairs"], 1)
        wrong = deepcopy(oracle)
        wrong[0]["answer"]["decision"] = "refuted"
        self.assertEqual(score(self.registry, manifest, wrong)["decision_accuracy_over_planned"], .5)
        self.assertEqual(score(self.registry, manifest, wrong)["pair_joint_accuracy_over_selected_pairs"], 0)
        for state in ("abstained", "env_blocked", "not_run", "budget_exhausted"):
            row = deepcopy(oracle[0])
            row.update(status=state, answer=None)
            report = score(self.registry, manifest, [row])
            self.assertEqual(report["outcomes"], {state: 1, "missing": 1})
            self.assertIsNone(report["decision_accuracy_on_answered"])
            self.assertEqual(report["decision_accuracy_over_planned"], 0)

    def test_self_scores_unknown_duplicates_and_stale_bindings_fail(self):
        manifest = self.prepare()
        rows = self.oracle(manifest)
        mutations = [("task_id", "unknown"), ("task_hash", "0" * 64), ("run_id", "other"),
                     ("status", "correct"), ("score", 1)]
        for field, value in mutations:
            altered = deepcopy(rows)
            altered[0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                score(self.registry, manifest, altered)
        with self.assertRaises(ValueError):
            score(self.registry, manifest, rows + rows[:1])
        changed = deepcopy(self.registry)
        changed["tasks"][0]["reference"]["decision"] = "refuted"
        with self.assertRaises(ValueError):
            score(changed, manifest, rows)

    def test_irrelevant_cli_flags_are_rejected_before_registry_loading(self):
        for args in (("doctor", "--purpose", "reference"), ("validate", "--reviews", "unused"),
                     ("review-pack", "--reviews", "unused")):
            result = subprocess.run([sys.executable, str(B / "scripts/bench.py"), *args], capture_output=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn(b"does not apply", result.stderr)

    def test_rehashed_untyped_or_invented_manifest_provenance_is_rejected(self):
        manifest = self.prepare()
        original = self.oracle(manifest)
        for field, value in (("run_id", None), ("run_id", ""), ("source_commit", "INVENTED_SOURCE_COMMIT"),
                             ("source_commit", "0" * 40), ("source_tree_dirty", "false"), ("source_tree_dirty", True)):
            altered = deepcopy(manifest)
            rows = deepcopy(original)
            altered[field] = value
            if field == "run_id":
                for row in rows:
                    row["run_id"] = value
            altered["manifest_hash"] = digest({k: v for k, v in altered.items() if k != "manifest_hash"})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                score(self.registry, altered, rows)
        self.registry["source_tree_dirty"] = True
        altered = deepcopy(manifest)
        altered["source_tree_dirty"] = False
        altered["manifest_hash"] = digest({k: v for k, v in altered.items() if k != "manifest_hash"})
        with self.assertRaises(ValueError):
            score(self.registry, altered, original)

    def test_alternative_explanation_ungraded_until_complete_bound_review(self):
        manifest = self.prepare()
        rows = self.oracle(manifest)
        self.assertIsNone(score(self.registry, manifest, rows)["aggregate_semantic_score"])
        reviews = review_template(self.registry["tasks"][:2], rows)
        for review in reviews:
            review["reviewer"] = {"identity": "reviewer", "kind": "human", "method": "Inspected the actual argument."}
            for criterion in review["criteria"]:
                criterion["met"] = True
        report = score(self.registry, manifest, rows, reviews)
        self.assertEqual(report["aggregate_semantic_score"], 1)
        self.assertFalse(report["model_identity_authenticated"])
        self.assertEqual(report["rows"][0]["response_hash"], digest(rows[0]))
        self.assertEqual(report["rows"][0]["review_hash"], digest(reviews[0]))
        self.assertEqual(report["rows"][0]["reviewer"], reviews[0]["reviewer"])
        self.assertFalse(report["rows"][0]["review_identity_authenticated"])
        rows[0]["answer"]["explanation"] = "Changed after review."
        with self.assertRaises(ValueError):
            score(self.registry, manifest, rows, reviews)

    def test_criteria_weight_null_and_partial_review_cannot_inflate_score(self):
        manifest = self.prepare()
        rows = self.oracle(manifest)
        original = review_template(self.registry["tasks"][:2], rows)
        for review in original:
            review["reviewer"] = {"identity": "r", "kind": "ai", "method": "Read the response."}
            review["criteria"][0]["met"] = True
        for key, value in (("weight", 999), ("met", None), ("met", 1), ("criterion", "A trivial replacement.")):
            reviews = deepcopy(original)
            reviews[0]["criteria"][0][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                score(self.registry, manifest, rows, reviews)
        self.assertIsNone(score(self.registry, manifest, rows, original[:1])["aggregate_semantic_score"])

    def test_review_pack_joins_actual_argument_and_reference_without_changing_student_input(self):
        manifest = self.prepare()
        responses = self.oracle(manifest)
        responses[0]["answer"]["explanation"] = '<script>alert("data only")</script> Alternative argument.'
        student_path = self.root / "run/input/tasks.jsonl"
        student_bytes = student_path.read_bytes()
        output = self.root / "review"
        summary = review_pack(self.registry, manifest, responses, output, run_directory=self.root / "run")
        cases = read_jsonl(output / "cases.jsonl")
        reviews = read_jsonl(output / "reviews.template.jsonl")
        self.assertEqual(summary["review_records"], 2)
        self.assertEqual(summary["review_states"], {"needs_rubric_review": 2})
        self.assertFalse(summary["ready_to_score"])
        self.assertTrue(summary["contains_reference_answers"])
        self.assertEqual(cases[0]["input"], self.registry["tasks"][0]["input"])
        self.assertEqual(cases[0]["response"], responses[0])
        self.assertEqual(cases[0]["reference"], self.registry["tasks"][0]["reference"])
        self.assertEqual(cases[0]["response_hash"], digest(responses[0]))
        self.assertEqual(cases[0]["review_template"], reviews[0])
        self.assertIsNone(cases[0]["semantic_rubric_score"])
        self.assertEqual(student_path.read_bytes(), student_bytes)
        self.assertNotIn("REFERENCE_NOT_A_PROMPT", student_path.read_text())
        self.assertNotIn("<script>", (output / "README.md").read_text())
        for filename, expected in summary["files"].items():
            self.assertEqual(hashlib.sha256((output / filename).read_bytes()).hexdigest(), expected)
        with self.assertRaises(ValueError):
            score(self.registry, manifest, responses, reviews)
        for review in reviews:
            review["reviewer"] = {"identity": "reviewer", "kind": "human", "method": "Inspected each case."}
            for criterion in review["criteria"]:
                criterion["met"] = True
        self.assertEqual(score(self.registry, manifest, responses, reviews)["aggregate_semantic_score"], 1)
        with self.assertRaises(FileExistsError):
            review_pack(self.registry, manifest, responses, output, run_directory=self.root / "run")

    def test_review_pack_retains_unanswered_cases_and_has_no_invented_reviews(self):
        manifest = self.prepare(split=None, track=None, task_ids=[t["task_id"] for t in self.registry["tasks"][:3]])
        responses = self.oracle(manifest)
        responses[0].update(status="abstained", answer=None)
        responses[1].update(status="env_blocked", answer=None)
        summary = review_pack(self.registry, manifest, responses, self.root / "review", run_directory=self.root / "run")
        cases = read_jsonl(self.root / "review/cases.jsonl")
        self.assertEqual([c["status"] for c in cases], ["abstained", "env_blocked", "missing"])
        self.assertEqual(summary["outcomes"], {"abstained": 1, "env_blocked": 1, "missing": 1})
        self.assertEqual(summary["review_records"], 0)
        self.assertTrue(all(c["review_state"] == "no_answer_to_review" and c["review_template"] is None for c in cases))
        self.assertIsNone(cases[-1]["response"])
        self.assertIsNone(cases[-1]["response_hash"])
        self.assertEqual(read_jsonl(self.root / "review/reviews.template.jsonl"), [])

    def test_nonlean_review_pack_scores_only_completed_argument_review(self):
        manifest = self.prepare(split="train", track="nonlean")
        responses = response_template(self.registry["tasks"][2:3], manifest["run_id"])
        responses[0].update(status="answered", answer={"explanation": "A derivation using a different valid route."})
        review_pack(self.registry, manifest, responses, self.root / "review", run_directory=self.root / "run")
        case = read_jsonl(self.root / "review/cases.jsonl")[0]
        self.assertEqual(case["track"], "nonlean")
        self.assertEqual(case["review_state"], "needs_rubric_review")
        self.assertIsNone(case["decision_correct"])
        self.assertIsNone(score(self.registry, manifest, responses)["aggregate_semantic_score"])
        reviews = read_jsonl(self.root / "review/reviews.template.jsonl")
        reviews[0]["reviewer"] = {"identity": "r", "kind": "human", "method": "Checked the alternative derivation."}
        reviews[0]["criteria"][0]["met"] = True
        result = score(self.registry, manifest, responses, reviews)
        self.assertEqual(result["semantic_scores_by_track"], {"nonlean": 1})
        self.assertIsNone(result["decision_accuracy_over_planned"])
        self.assertIsNone(result["formal_proof_score"])

    def test_review_pack_rejects_bad_bindings_and_student_output_paths_before_writing(self):
        manifest = self.prepare()
        responses = self.oracle(manifest)
        for relative in ("input/review", "output/review", "operator/review"):
            output = self.root / "run" / relative
            with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, "outside"):
                review_pack(self.registry, manifest, responses, output, run_directory=self.root / "run")
            self.assertFalse(output.exists())
        # A portable bundle exposes the sibling environment directory as a
        # student build context, so it cannot receive operator review material.
        (self.root / "task.json").write_text('{}')
        output = self.root / "environment/workspace/review"
        with self.assertRaisesRegex(ValueError, "outside"):
            review_pack(self.registry, manifest, responses, output, run_directory=self.root / "run")
        self.assertFalse(output.exists())
        responses[0]["task_hash"] = "0" * 64
        with self.assertRaises(ValueError):
            review_pack(self.registry, manifest, responses, self.root / "bad-review", run_directory=self.root / "run")
        self.assertFalse((self.root / "bad-review").exists())

    def test_review_pack_keeps_submitted_lean_text_ungraded(self):
        manifest = self.prepare(split="train", track="lean", exposure="approved_interface")
        responses = response_template(self.registry["tasks"][-1:], manifest["run_id"])
        responses[0].update(status="answered", answer={"proof": "by run_tac IO.println \"UNTRUSTED\""})
        summary = review_pack(self.registry, manifest, responses, self.root / "review", run_directory=self.root / "run")
        case = read_jsonl(self.root / "review/cases.jsonl")[0]
        self.assertEqual(summary["review_records"], 0)
        self.assertEqual(case["response"], responses[0])
        self.assertEqual(case["review_state"], "formal_verifier_required")
        self.assertEqual(case["formal_execution"], "ENV_BLOCKED")
        self.assertIsNone(case["formal_proof_score"])
        self.assertIsNone(case["semantic_rubric_score"])

    def test_review_pack_cli_and_completed_review_scoring_round_trip(self):
        manifest = self.prepare()
        response_path = self.root / "responses.jsonl"
        write_jsonl(response_path, self.oracle(manifest))
        cli = runpy.run_path(str(B / "scripts/bench.py"))["main"]
        common = ["--manifest", str(self.root / "run/manifest.json"), "--responses", str(response_path)]
        with patch.dict(cli.__globals__, {"build_registry": lambda: self.registry}):
            stdout = StringIO()
            with patch.object(sys, "argv", ["bench.py", "review-pack", *common, "--output", str(self.root / "review")]), redirect_stdout(stdout):
                self.assertEqual(cli(), 0)
            self.assertEqual(json.loads(stdout.getvalue())["review_records"], 2)
            reviews = read_jsonl(self.root / "review/reviews.template.jsonl")
            for review in reviews:
                review["reviewer"] = {"identity": "reviewer", "kind": "human", "method": "Checked mathematical criteria."}
                for criterion in review["criteria"]:
                    criterion["met"] = True
            completed_path = self.root / "review/reviews.completed.jsonl"
            write_jsonl(completed_path, reviews)
            stdout = StringIO()
            with patch.object(sys, "argv", ["bench.py", "score", *common, "--reviews", str(completed_path)]), redirect_stdout(stdout):
                self.assertEqual(cli(), 0)
            scored = json.loads(stdout.getvalue())
            self.assertEqual(scored["aggregate_semantic_score"], 1)
            self.assertEqual(scored["semantic_review_coverage"], 2)
            self.assertFalse(scored["model_performance_measured"])

    def test_formal_text_is_never_executed_or_promoted(self):
        manifest = self.prepare(split="train", track="lean", exposure="approved_interface")
        rows = response_template(self.registry["tasks"][-1:], manifest["run_id"])
        rows[0].update(status="answered", answer={"proof": "by run_tac IO.println \"UNTRUSTED\""})
        report = score(self.registry, manifest, rows)
        self.assertIsNone(report["formal_proof_score"])
        self.assertEqual(report["rows"][0]["formal_execution"], "ENV_BLOCKED")
        altered = deepcopy(manifest)
        altered["exposure"] = "closed_book"
        altered["manifest_hash"] = digest({k: v for k, v in altered.items() if k != "manifest_hash"})
        with self.assertRaises(ValueError):
            score(self.registry, altered, rows)
        altered["exposure"] = "open_library"
        altered["manifest_hash"] = digest({k: v for k, v in altered.items() if k != "manifest_hash"})
        with self.assertRaises(ValueError):
            score(self.registry, altered, rows)

    def test_portable_bundle_has_no_reference_in_agent_context_and_standalone_grader(self):
        directory = self.root / "bundle"
        bundle(self.registry, directory)
        public = "".join(p.read_text() for p in (directory / "environment").rglob("*") if p.is_file())
        self.assertNotIn("REFERENCE_NOT_A_PROMPT", public)
        self.assertNotIn("PAIR_PRIVATE", public)
        self.assertIn("COPY workspace/", public)
        oracle = subprocess.check_output([sys.executable, str(directory / "solution/oracle.py")])
        response = directory / "run/output/oracle.jsonl"
        response.write_bytes(oracle)
        graded = subprocess.check_output([sys.executable, str(directory / "grader/grade.py"), str(response)])
        self.assertEqual(json.loads(graded)["decision_accuracy_over_planned"], 1)
        none = subprocess.check_output([sys.executable, str(directory / "grader/grade.py"), str(directory / "run/output/responses.template.jsonl")])
        self.assertEqual(json.loads(none)["decision_accuracy_over_planned"], 0)

    def test_synthetic_smoke_and_downloads_preserve_split_and_evidence(self):
        report = smoke(self.registry, self.root / "smoke")
        self.assertTrue(report["passed"])
        self.assertEqual(report["model_calls"], 0)
        self.assertEqual(report["container_calls"], 0)
        self.assertTrue(report["standalone_oracle_and_grader_passed"])
        self.assertTrue(report["tampered_response_rejected"])
        self.assertEqual(report["reports"]["wrong"]["decision_accuracy_over_planned"], 0)
        self.assertEqual(report["reports"]["wrong"]["pair_joint_accuracy_over_selected_pairs"], 0)

    def test_download_validator_checks_projection_not_only_rehashed_manifest(self):
        registry = deepcopy(self.registry)
        registry["tasks"].append(_task("nonlean", "dev", ["core-3"], "dev", "Development", {"question": "P?"}, {}, {"answer": "DEV_GOLD", "rubric": []}))
        registry["registry_hash"] = digest({"tasks": registry["tasks"], "sources": registry["source_identities"], "runtime_sources": registry["runtime_sources"]})
        directory = self.root / "downloads"
        write_downloads(directory, registry)
        self.assertTrue(verify_downloads(directory, registry)["passed"])
        rows = read_jsonl(directory / "eval-prompts.jsonl")
        rows[0]["reference"] = "A leaked reference."
        (directory / "eval-prompts.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
        with self.assertRaises(ValueError):
            verify_downloads(directory, registry)


if __name__ == "__main__":
    unittest.main()
