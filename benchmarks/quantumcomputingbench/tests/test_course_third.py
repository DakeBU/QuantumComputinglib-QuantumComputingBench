"""Independent third-cohort software regressions, without Lean or model calls.

Mock decoders, reviewers and verifier replies have no mathematical authority.
The actual fixture, canonical item payloads and blind input packets are read.
"""
import ast
import asyncio
import io
import json
import runpy
import subprocess
import sys
import unittest
from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
sys.path[:0] = [str(B / "src"), str(B / "scripts")]
import lean_course as driver
import lean_course_v2 as previous
import lean_course_v3 as third_driver
import qcb_course_batch as batch
import qcb_course_third as third
import qcb_graph_course_pilot as pilot
from qcb_core import digest, read_json
from qcb_lean_course import coverage, export_course
from qcb_proof_session import ProofSession, bound_reply, proof_sha


def reseal_mock(packet, docs):
    comparison = docs["comparison.json"]
    comparison["candidate_batch_digest"] = digest(packet)
    for group in comparison["packet_digests"]:
        context = docs[group + "-decoder-input.json"]
        decoder = docs[group + "-decoder.json"]
        decoder["packet_digest"] = digest(context)
        comparison["packet_digests"][group] = digest(context)
        comparison["decoder_digests"][group] = digest(decoder)
    inputs = docs["comparison-input.json"]
    for key in ("candidate_batch_digest", "packet_digests", "decoder_digests"):
        inputs[key] = deepcopy(comparison[key])
    comparison["comparison_input_digest"] = digest(inputs)


def mock_documents(packet, cases, items, *, evidence_dir=third.EVIDENCE, fixture=third.FIXTURE):
    """Hash-consistent routing fixture; never independent semantic evidence."""
    groups = {c["semantic_evidence"]["group"] for c in cases}
    docs = {g + "-decoder-input.json": read_json(evidence_dir / (g + "-decoder-input.json")) for g in groups}
    for group in groups:
        docs[group + "-decoder.json"] = {
            "schema_version": "qcb.curriculum_blind_decode.v1", "source_blind": True,
            "decoder_identity": "software-mock-decoder-" + group,
            "views": [{"anonymous_id": v["anonymous_id"],
                       "reconstructed_statement": "SOFTWARE MOCK ONLY; no mathematical reconstruction."}
                      for v in docs[group + "-decoder-input.json"]["views"]]}
    comparison = {"schema_version": "qcb.course_semantic_comparison.v1", "source_blind": False,
                  "reviewer": "software-mock-source-comparator", "views": [],
                  "packet_digests": dict.fromkeys(groups), "decoder_digests": dict.fromkeys(groups)}
    inputs = {"schema_version": "qcb.course_semantic_comparison_input.v2", "views": []}
    for case in cases:
        core = case["task"]["core_id"]
        evidence = case["semantic_evidence"]
        group, anonymous = evidence["group"], evidence["anonymous_id"]
        context = docs[group + "-decoder-input.json"]
        formal = next(v for v in context["views"] if v["anonymous_id"] == anonymous)
        decoded = next(v for v in docs[group + "-decoder.json"]["views"] if v["anonymous_id"] == anonymous)
        labels = {"core_id": core, "task_hash": digest(case["task"]),
                  "formal_context_digest": digest(formal["formal_context"]),
                  "source_item_digest": case["source_item_digest"]}
        comparison["views"].append({**labels, "verdict": "accept", "reasoning": "SOFTWARE MOCK ONLY.",
                                     "whole_question_coverage": {"software_mock": "No semantic assessment."}})
        inputs["views"].append({**labels, "source_semantics": {k: deepcopy(items[core][k]) for k in
                                ("question", "reference_answer", "assumptions", "conventions")},
                                "retrieval_interfaces": deepcopy(case["task"]["interfaces"]), "formal_view": deepcopy(formal),
                                "ambient_context": {k: deepcopy(v) for k, v in context.items() if k != "views"},
                                "source_blind_decode": deepcopy(decoded)})
    docs.update({"comparison.json": comparison, "comparison-input.json": inputs,
                 fixture.name: deepcopy(packet)})
    reseal_mock(packet, docs)
    return docs


class CourseThirdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read_json(third.FIXTURE)
        cls.bundle = pilot.load_catalog()
        cls.cases, cls.identity, cls.catalog, cls.graph = pilot.load_candidates(
            require_semantics=False, fixture=third.FIXTURE, evidence_dir=third.EVIDENCE,
            expected_cores=third.EXPECTED, excluded_authors=third.AUTHORS)
        cls.docs = mock_documents(cls.packet, cls.cases, cls.bundle[1])

    def candidate_check(self, docs=None):
        docs = self.docs if docs is None else docs
        def reader(path):
            return deepcopy(docs[Path(path).name])
        with ExitStack() as stack:
            stack.enter_context(patch.object(pilot, "read_json", side_effect=reader))
            stack.enter_context(patch.object(batch, "read_json", side_effect=reader))
            stack.enter_context(patch.object(batch, "_canonical_items", return_value=self.bundle[1]))
            stack.enter_context(patch.object(pilot, "load_catalog", return_value=self.bundle))
            return third.candidates()

    def test_actual_five_core_fixture_and_mock_binding_baseline(self):
        cases, identity, _, _ = self.candidate_check()
        self.assertEqual({c["task"]["core_id"] for c in cases},
                         {"qcb-core-be-110", "qcb-core-be-111", "qcb-core-be-102", "qcb-core-sp-101", "qcb-core-sp-104"})
        self.assertEqual(len(cases), 5)
        self.assertEqual(sum(len(c["references"]) for c in cases), 21)
        self.assertEqual(identity["fixture_digest"], digest(self.packet))

    def test_actual_new_and_preceding_review_inputs_are_sanitized_canonical_projections(self):
        for fixture, evidence in ((third.FIXTURE, third.EVIDENCE),
                                  (third.preceding.FIXTURE, third.EVIDENCE / "legacy-v2")):
            packet = read_json(fixture)
            inputs = read_json(evidence / "comparison-input.json")
            cases = {c["task"]["core_id"]: c for c in packet["cases"]}
            self.assertEqual(inputs["schema_version"], "qcb.course_semantic_comparison_input.v2")
            self.assertEqual(inputs["candidate_batch_digest"], digest(packet))
            self.assertEqual({r["core_id"] for r in inputs["views"]}, set(cases))
            self.assertEqual(len(inputs["views"]), len(cases))
            for row in inputs["views"]:
                with self.subTest(fixture=fixture.name, core=row["core_id"]):
                    item = self.bundle[1][row["core_id"]]
                    self.assertEqual(set(row["source_semantics"]), {"question", "reference_answer", "assumptions", "conventions"})
                    self.assertEqual(row["source_semantics"], {k: item[k] for k in ("question", "reference_answer", "assumptions", "conventions")})
                    self.assertNotIn("source_item", row)
                    self.assertEqual(row["source_item_digest"], digest(item))
                    self.assertEqual(row["retrieval_interfaces"], cases[row["core_id"]]["task"]["interfaces"])
                    self.assertEqual(row["task_hash"], digest(cases[row["core_id"]]["task"]))

    def test_source_qa_payload_cannot_be_substituted_even_with_fresh_input_digest(self):
        for field in ("question", "reference_answer", "assumptions", "conventions"):
            docs = deepcopy(self.docs)
            row = docs["comparison-input.json"]["views"][0]
            row["source_semantics"][field] = "SOFTWARE MOCK ATTACK"
            reseal_mock(self.packet, docs)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "actual canonical"):
                self.candidate_check(docs)

    def test_sanitized_input_rejects_rehashed_review_metadata_at_every_source_level(self):
        for level in ("input", "row", "source_semantics"):
            docs = deepcopy(self.docs)
            inputs = docs["comparison-input.json"]
            row = inputs["views"][0]
            target = inputs if level == "input" else row if level == "row" else row["source_semantics"]
            target["reviews"] = [{"reviewer": "SOFTWARE MOCK PRIOR REVIEW", "verdict": "accept"}]
            reseal_mock(self.packet, docs)
            with self.subTest(level=level), self.assertRaisesRegex(ValueError, "extra metadata|actual canonical"):
                self.candidate_check(docs)

    def test_canonical_body_hash_is_independent_of_a_forged_label(self):
        for alter_body in (False, True):
            docs = deepcopy(self.docs)
            cases = deepcopy(self.cases)
            core = cases[0]["task"]["core_id"]
            row = next(v for v in docs["comparison-input.json"]["views"] if v["core_id"] == core)
            impostor = deepcopy(self.bundle[1][core]); impostor["question"] = "SOFTWARE MOCK CANONICAL IMPOSTOR"
            cases[0]["source_item_digest"] = digest(impostor)
            row["source_item_digest"] = digest(impostor)
            if alter_body:
                row["source_semantics"]["question"] = impostor["question"]
            reseal_mock(self.packet, docs)
            with self.subTest(alter_body=alter_body), patch.object(batch, "read_json", side_effect=lambda p: deepcopy(docs[Path(p).name])), \
                    patch.object(batch, "_canonical_items", return_value=self.bundle[1]), self.assertRaisesRegex(ValueError, "actual canonical"):
                batch.bind_review_input(third.FIXTURE, third.EVIDENCE, cases, require_sanitized=True)

    def test_legacy_full_item_stays_readable_but_cannot_pass_a_sanitized_gate(self):
        docs = deepcopy(self.docs)
        docs["comparison-input.json"]["schema_version"] = "qcb.course_semantic_comparison_input.v1"
        for row in docs["comparison-input.json"]["views"]:
            row["source_item"] = deepcopy(self.bundle[1][row["core_id"]])
            del row["source_semantics"]; del row["retrieval_interfaces"]
        reseal_mock(self.packet, docs)
        with patch.object(batch, "read_json", side_effect=lambda p: deepcopy(docs[Path(p).name])):
            batch.bind_review_input(third.FIXTURE, third.EVIDENCE, self.cases)
            with self.assertRaisesRegex(ValueError, "actual comparison input"):
                batch.bind_review_input(third.FIXTURE, third.EVIDENCE, self.cases, require_sanitized=True)
        with self.assertRaisesRegex(ValueError, "actual comparison input"):
            self.candidate_check(docs)

    def test_exact_interface_body_and_full_scope_are_bound_not_only_task_hash(self):
        for attack in ("type", "name", "module", "source_node_id", "missing", "extra"):
            docs = deepcopy(self.docs)
            entries = docs["comparison-input.json"]["views"][0]["retrieval_interfaces"]
            if attack == "missing":
                entries.pop()
            elif attack == "extra":
                entries.append(deepcopy(entries[0]))
            else:
                entries[0][attack] = "SOFTWARE MOCK INTERFACE SUBSTITUTION"
            reseal_mock(self.packet, docs)
            with self.subTest(attack=attack), self.assertRaisesRegex(ValueError, "actual canonical"):
                self.candidate_check(docs)

    def test_actual_13_scoped_declarations_are_retrievable_and_closed_book_blocks(self):
        self.assertEqual([len(c["task"]["interfaces"]) for c in self.cases], [3, 3, 3, 3, 1])
        for case in self.cases:
            task = case["task"]
            approved = ProofSession(task, exposure="approved_interface")
            closed = ProofSession(task, exposure="closed_book")
            self.assertNotIn("interfaces", approved.agent_input()["task"])
            self.assertNotIn("interfaces", closed.agent_input()["task"])
            for entry in task["interfaces"]:
                with self.subTest(core=task["core_id"], declaration=entry["name"]):
                    self.assertEqual(set(entry), {"name", "type", "module", "source_node_id"})
                    node = self.graph[entry["source_node_id"]]
                    self.assertEqual(node["kind"], "declaration")
                    self.assertEqual(node["inventory_status"], "Compiled")
                    self.assertFalse(node["open_obligation"])
                    self.assertEqual(node["source"], entry["module"].replace(".", "/") + ".lean")
                    reply = asyncio.run(approved.act({"kind": "search", "state_id": approved.state_id, "query": entry["name"]}))
                    self.assertEqual(reply["status"], "returned")
                    self.assertIn(entry, reply["entries"])
                    self.assertTrue(all(e in task["interfaces"] for e in reply["entries"]))
                    blocked = asyncio.run(closed.act({"kind": "search", "state_id": closed.state_id, "query": entry["name"]}))
                    self.assertEqual(blocked["status"], "blocked")
                    self.assertEqual(blocked["failure_class"], "API_BLOCKED")
                    self.assertNotIn("entries", blocked)

    def test_resealed_actual_ambient_or_reconstruction_cannot_reuse_another_review_input(self):
        for which in ("ambient", "reconstruction", "formal_node"):
            docs = deepcopy(self.docs)
            group = self.cases[0]["semantic_evidence"]["group"]
            if which == "ambient":
                docs[group + "-decoder-input.json"]["ambient_definitions"] = []
            elif which == "reconstruction":
                docs[group + "-decoder.json"]["views"][0]["reconstructed_statement"] = "CHANGED SOFTWARE MOCK"
            else:
                docs[group + "-decoder-input.json"]["views"][0]["nodes"] = []
            reseal_mock(self.packet, docs)
            with self.subTest(which=which), self.assertRaisesRegex(ValueError, "substituted"):
                self.candidate_check(docs)

    def test_cohort_cannot_be_shrunk_duplicated_or_replace_a_canonical_core(self):
        for which in ("shrink", "duplicate", "replace"):
            docs = deepcopy(self.docs)
            cases = docs[third.FIXTURE.name]["cases"]
            if which == "shrink":
                cases.pop()
            elif which == "duplicate":
                cases[-1] = deepcopy(cases[0])
            else:
                cases[-1]["task"]["core_id"] = "qcb-core-sp-120"
            reseal_mock(docs[third.FIXTURE.name], docs)
            with self.subTest(which=which), self.assertRaisesRegex(ValueError, "exact sealed"):
                self.candidate_check(docs)

    def test_resealed_invalid_schemas_roles_and_coverage_are_rejected(self):
        group = self.cases[0]["semantic_evidence"]["group"]
        attacks = {
            "comparison_schema": lambda d: d["comparison.json"].update(schema_version="unsupported"),
            "input_schema": lambda d: d["comparison-input.json"].update(schema_version="unsupported"),
            "decoder_schema": lambda d: d[group + "-decoder.json"].update(schema_version="unsupported"),
            "blind_role": lambda d: d[group + "-decoder.json"].update(source_blind=False),
            "author_decoder": lambda d: d[group + "-decoder.json"].update(decoder_identity=third.AUTHORS[0]),
            "same_roles": lambda d: d[group + "-decoder.json"].update(decoder_identity=d["comparison.json"]["reviewer"]),
            "missing_review": lambda d: d["comparison-input.json"]["views"].pop(),
            "duplicate_review": lambda d: d["comparison-input.json"]["views"].__setitem__(1, deepcopy(d["comparison-input.json"]["views"][0])),
            "missing_decoder": lambda d: d[group + "-decoder.json"]["views"].pop(),
        }
        for name, attack in attacks.items():
            docs = deepcopy(self.docs); attack(docs); reseal_mock(self.packet, docs)
            with self.subTest(attack=name), self.assertRaises(ValueError):
                self.candidate_check(docs)

    def test_malformed_bound_input_has_a_typed_rejection(self):
        for value in (None, False, "not an input", [], {"views": None}):
            docs = deepcopy(self.docs); docs["comparison-input.json"] = value
            docs["comparison.json"]["comparison_input_digest"] = digest(value)
            with self.subTest(value=value), patch.object(batch, "read_json", side_effect=lambda p: deepcopy(docs[Path(p).name])), self.assertRaises(ValueError):
                batch.bind_review_input(third.FIXTURE, third.EVIDENCE, self.cases)

    def mock_receipt(self):
        wrong = {proof_sha(c["negative_controls"]["wrong_target"]) for c in self.cases}
        sorry = {proof_sha(c["negative_controls"]["sorry_axiom"]) for c in self.cases}
        serial = iter(range(1, 1000))
        class SoftwareMockVerifier:
            execution_class = "trusted_local_authored_reference"
            isolated = False
            def __init__(self, task, allowlist, build_root):
                self.replays = []
            async def verify(self, request):
                proof = proof_sha(request["proof"])
                negative = proof in wrong | sorry
                return bound_reply(request, status="compile_error" if negative else "verified",
                                   execution_id=f"{next(serial):032x}", kernel_checked=not negative,
                                   axioms=["sorryAx"] if proof in sorry else [])
        raw = []
        with patch.object(driver, "AuthoredReferenceVerifier", SoftwareMockVerifier), redirect_stdout(io.StringIO()):
            report = asyncio.run(driver.check_references(self.cases, self.identity, "unused-software-mock", raw,
                                                        "f" * 40, profile=third.PROFILE))
        report["pipeline_source_hashes_lf"] = {p: digest({"software_mock": p}) for p in third.PIPELINE_PATHS}
        report["receipt_digest"] = digest(report)
        return report, raw

    def test_mock_driver_profile_covers_all_46_checks_and_keeps_controls_separate(self):
        report, raw = self.mock_receipt()
        self.assertTrue(report["passed"])
        self.assertEqual(report["authored_reference_profile"],
                         {"batch_wall_seconds": 2700, "session_wall_seconds": 600, "check_seconds": 120, "control_wall_seconds": 180})
        self.assertEqual(len(raw), 15)
        self.assertEqual(sum(r["session"]["metrics"]["verifier_calls"] for r in raw), 46)
        self.assertFalse(report["standalone_controls_are_completed_protocol_sessions"])
        self.assertFalse(report["model_performance_measured"])
        self.assertEqual(report["model_calls"], 0)
        for record in raw:
            self.assertEqual(record["session"]["limits"]["check_seconds"], 120)
            self.assertEqual(record["session"]["limits"]["wall_seconds"], 600 if record["condition"] == "provided_dag_repair" else 180)

    def test_qualification_rejects_resealed_receipt_drift_before_git_lineage(self):
        good, _ = self.mock_receipt()
        attacks = {
            "smaller_profile": lambda r: r["authored_reference_profile"].update(session_wall_seconds=450),
            "missing_pipeline": lambda r: r["pipeline_source_hashes_lf"].pop(next(iter(r["pipeline_source_hashes_lf"]))),
            "extra_pipeline": lambda r: r["pipeline_source_hashes_lf"].update(untrusted="a"*64),
            "missing_core": lambda r: r["results"].pop(),
            "duplicate_core": lambda r: r["results"].__setitem__(1, deepcopy(r["results"][0])),
            "claimed_model_measurement": lambda r: r.update(model_performance_measured=True),
            "malformed_results": lambda r: r.update(results=None),
        }
        for name, attack in attacks.items():
            report = deepcopy(good); attack(report); report.pop("receipt_digest"); report["receipt_digest"] = digest(report)
            with self.subTest(attack=name), patch.object(batch, "read_json", return_value=report), \
                    patch.object(batch, "_source_lineage", side_effect=AssertionError("invalid receipt reached lineage")), self.assertRaises(ValueError):
                batch.qualify_candidate_batch(self.cases, self.identity, Path("unused"), third.PROFILE, third.PIPELINE_PATHS)
        with patch.object(batch, "read_json", return_value=good), patch.object(batch, "_source_lineage", return_value={"software_mock": True}):
            views, status = batch.qualify_candidate_batch(self.cases, self.identity, Path("unused"), third.PROFILE, third.PIPELINE_PATHS)
        self.assertEqual(len(views), 5)
        self.assertEqual(status["new_mathematical_cores"], 0)
        self.assertFalse(status["model_performance_measured"])

    def test_script_entrypoint_wires_the_third_loaders_and_profile(self):
        with patch.object(driver, "main", return_value=0) as main, self.assertRaises(SystemExit) as done:
            runpy.run_path(str(B / "scripts/lean_course_v3.py"), run_name="__main__")
        self.assertEqual(done.exception.code, 0)
        self.assertIs(main.call_args.kwargs["source_loader"], third.candidates)
        self.assertIs(main.call_args.kwargs["pipeline_loader"], third.pipeline_identity)
        self.assertEqual(main.call_args.kwargs["reference_profile"], third.PROFILE)

    def test_declared_pipeline_equals_static_local_import_closure_plus_fixed_data(self):
        files = [*(B / "src").glob("*.py"), *(B / "scripts").glob("*.py"), R / "website/scripts/proof_inputs.py"]
        modules = {p.stem: p for p in files}
        seen, pending = set(), ["lean_course_v3"]
        while pending:
            name = pending.pop()
            if name in seen:
                continue
            seen.add(name)
            for node in ast.walk(ast.parse(modules[name].read_text(encoding="utf-8-sig"))):
                imported = ([a.name for a in node.names] if isinstance(node, ast.Import) else
                            [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                pending.extend(n.split(".")[0] for n in imported if n.split(".")[0] in modules)
        actual = {modules[n].relative_to(R).as_posix() for n in seen}
        self.assertEqual(len(actual), 31)
        self.assertEqual({p for p in third.PIPELINE_PATHS if p.endswith(".py")}, actual)
        data = {p for p in third.PIPELINE_PATHS if not p.endswith(".py")}
        self.assertEqual(data, {third.FIXTURE.relative_to(R).as_posix(), third.PLAN.relative_to(R).as_posix(),
                              third.preceding.FIXTURE.relative_to(R).as_posix(),
                              *(str(third.EVIDENCE.relative_to(R).as_posix()) + "/" + n for n in
                                ("comparison.json", "comparison-input.json", "permutation-decoder-input.json", "permutation-decoder.json",
                                 "jet-decoder-input.json", "jet-decoder.json", "oracle-decoder-input.json", "oracle-decoder.json")),
                              *(str(third.EVIDENCE.relative_to(R).as_posix()) + "/legacy-v2/" + n for n in
                                ("comparison.json", "comparison-input.json", "lcu-decoder-input.json", "lcu-decoder.json",
                                 "conditioning-decoder-input.json", "conditioning-decoder.json"))})
        self.assertEqual(len(data), 17)

    def test_preceding_alignment_is_mandatory_before_any_historical_qualification(self):
        with patch.object(third_driver, "check_preceding_alignment", side_effect=ValueError("SOFTWARE MOCK missing fresh alignment")), \
                patch.object(third_driver.previous, "load_course", side_effect=AssertionError("unreviewed history reached reader")), \
                patch.object(third_driver, "qualified", side_effect=AssertionError("unreviewed history reached third qualification")), \
                self.assertRaisesRegex(ValueError, "missing fresh alignment"):
            third_driver.load_course()

    def test_preceding_supplement_accepts_only_bound_sanitized_mock_input(self):
        prior = third.preceding
        with patch.object(pilot, "load_catalog", return_value=self.bundle):
            selected = pilot.load_candidates(require_semantics=False, fixture=prior.FIXTURE,
                                            evidence_dir=prior.EVIDENCE, expected_cores=prior.EXPECTED)
        packet = read_json(prior.FIXTURE)
        baseline = mock_documents(packet, selected[0], self.bundle[1],
                                  evidence_dir=third.EVIDENCE / "legacy-v2", fixture=prior.FIXTURE)
        for attack in (None, "unsanitized", "source_body", "interface_body"):
            docs = deepcopy(baseline)
            if attack == "unsanitized":
                docs["comparison-input.json"]["schema_version"] = "qcb.course_semantic_comparison_input.v1"
            elif attack == "source_body":
                docs["comparison-input.json"]["views"][0]["source_semantics"]["question"] = "SOFTWARE MOCK SOURCE SUBSTITUTION"
            elif attack == "interface_body":
                docs["comparison-input.json"]["views"][0]["retrieval_interfaces"] = [{"software_mock": "unbound interface"}]
            reseal_mock(packet, docs)
            reader = lambda p: deepcopy(docs[Path(p).name])
            with self.subTest(attack=attack), patch.object(prior, "candidates", return_value=selected), \
                    patch.object(third, "read_json", side_effect=reader), patch.object(pilot, "read_json", side_effect=reader), \
                    patch.object(batch, "read_json", side_effect=reader), patch.object(batch, "_canonical_items", return_value=self.bundle[1]):
                if attack is None:
                    third.check_preceding_alignment()
                else:
                    with self.assertRaises(ValueError):
                        third.check_preceding_alignment()

    def test_cumulative_exports_preserve_13_historical_views_and_hide_all_authored_proofs(self):
        earlier = previous.load_course()
        before = digest(earlier)
        new = {c["view_id"]: {"task": deepcopy(c["task"])} for c in self.cases}
        with patch.object(third_driver, "check_preceding_alignment") as alignment, \
                patch.object(third_driver.previous, "load_course", return_value=earlier), \
                patch.object(third_driver, "qualified", return_value=(new, {"software_mock_only": True}, self.catalog, self.graph)):
            plan, views, catalog, graph, report = third_driver.load_course()
        alignment.assert_called_once_with()
        self.assertEqual(digest(earlier), before)
        self.assertEqual(len(earlier[1]), 13)
        old_status = earlier[4]["reference_qualification"]
        for status in (old_status["second_cohort"], old_status["previous_course"]["new_companions"]):
            self.assertFalse(status["reference_lineage"]["recorded_pipeline_matches_current_sources"])
            self.assertFalse(status["reference_lineage"]["reference_replayed_during_registry_validation"])
        self.assertEqual(len(views), 18)
        self.assertEqual(report["distinct_shared_cores"], 18)
        for key, value in earlier[1].items():
            self.assertEqual(views[key], value)
        self.assertEqual(coverage(plan, views, catalog, graph)["new_mathematical_cores"], 0)
        proofs = {p for c in self.cases for k in ("references", "controls", "negative_controls") for p in c[k].values()}
        forbidden = {"references", "reference_answer", "controls", "negative_controls", "allowed_proofs", "source_binder_audit"}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(value.keys() & forbidden)
                for child in value.values(): inspect(child)
            elif isinstance(value, list):
                for child in value: inspect(child)
        for mode in ("root_only", "proof_dag"):
            for exposure in ("closed_book", "approved_interface"):
                with self.subTest(mode=mode, exposure=exposure):
                    exported = export_course(plan, views, catalog, graph, mode=mode, exposure=exposure)
                    self.assertEqual(len(exported["tasks"]), 18)
                    inspect(exported)
                    for row in exported["tasks"]:
                        dumped = json.dumps(row["input"], ensure_ascii=False)
                        self.assertTrue(all(json.dumps(p, ensure_ascii=False)[1:-1] not in dumped for p in proofs))

    def test_historical_course_receipt_bytes_retain_their_git_record(self):
        for cohort in ("v1", "v2"):
            path = B / "reports" / ("lean-course-" + cohort) / "reference-checks.json"
            pinned = subprocess.check_output(["git", "show", "HEAD:" + path.relative_to(R).as_posix()], cwd=R, timeout=10)
            with self.subTest(cohort=cohort):
                self.assertEqual(path.read_bytes().replace(b"\r\n", b"\n"), pinned.replace(b"\r\n", b"\n"))

    def test_cumulative_reader_rejects_overwriting_an_earlier_view(self):
        key = self.cases[0]["view_id"]
        with patch.object(third_driver, "check_preceding_alignment"), \
                patch.object(third_driver.previous, "load_course", return_value=(None, {key: {}}, None, None, {})), \
                patch.object(third_driver, "qualified", return_value=({key: {}}, {}, self.catalog, self.graph)), \
                self.assertRaisesRegex(ValueError, "overwrite historical"):
            third_driver.load_course()


if __name__ == "__main__":
    unittest.main()
