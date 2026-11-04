"""Engineered protocol tests only: no model, training, Lean or actual gains.

The mocked trusted-verifier branch below tests arithmetic/authorization routing.
Its records and judgments are invented, not an attested scientific experiment.
"""
import hashlib
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))

from qcb_core import digest
from qcb_learning_design import (
    CELLS,
    analyze_experiment,
    canonical_messages,
    canonical_prompt_policy,
    experiment_template,
    profile_template,
    review_input,
    validate_experiment,
)
from qcb_learning_validity import stage_a_input


def cohort():
    probes = []
    for number in range(4):
        split = "train" if number == 0 else "test_public"
        probes.append({"probe_id": str(UUID(int=number+1)), "pair_id": str(UUID(int=100+number//2)),
                       "cluster_id": "mechanism-" + str(number//2), "parent_core_ids": ["core-" + str(number)],
                       "parent_contracts": {"core-" + str(number): digest(number)},
                       "canonical_relation": "diagnostic_contract_candidate", "split": split,
                       "question": "SOFTWARE FIXTURE: assess the stated proposition.", "assumptions": [], "conventions": [],
                       "formal_context": {"imports": ["Mathlib"], "proposition": "True"},
                       "gold": {"decision": "holds" if number % 2 == 0 else "refuted", "reference_proof": "by trivial",
                                "answer": "Invented test expectations, not mathematical review.",
                                "rubric": [{"id": "reason", "criterion": "Give a valid mechanism.", "weight": 1},
                                           {"id": "boundary", "criterion": "Preserve the boundary.", "weight": 3}]},
                       "source_nodes": ["declaration:Fixture.placeholder"], "reasoning_kind": "assumption_diagnosis",
                       "difficulty": {"band": "D2", "rationale": "Software fixture only.",
                                      "status": "provisional_author_mathematical_assessment", "measured_model_difficulty": None},
                       "author_identity": "fixture-author", "formal_coverage": "decision_polarity_only"})
    return {"probes": probes, "blind_test": False, "model_performance_measured": False}


def registered(packet, *, kind="weight_update"):
    registration = experiment_template(packet)
    registration["operator_identity"] = "fixture-operator"
    registration["intervention"].update(kind=kind, training_core_ids=["core-0"], material_sha256=digest("train only"),
                                         planned_optimizer_steps=2 if kind == "weight_update" else None)
    if kind == "in_context":
        lesson = "SOFTWARE FIXTURE lesson: preserve the normalization α and the register order.\n"
        registration["intervention"].update(lesson_text=lesson, material_sha256=hashlib.sha256(lesson.encode("utf-8")).hexdigest())
    base = profile_template()
    base.update(model_id="fixture-test-model", checkpoint_revision=digest("base"), chat_template_sha256=digest("chat"),
                tokenizer_sha256=digest("tokenizer"), adapter_sha256=digest("adapter"), architecture_sha256=digest("architecture"),
                runtime_sha256=digest("runtime"), parameter_count=123456, dtype="bfloat16", quantization="none")
    base["sampling"]["thinking_mode"] = "disabled"
    registration["profiles"] = {cell: deepcopy(base) for cell in CELLS}
    if kind == "weight_update":
        registration["profiles"]["update_post"]["checkpoint_revision"] = digest("updated")
    else:
        registration["profiles"]["update_post"]["lesson_prefix_sha256"] = registration["intervention"]["material_sha256"]
    return registration


def measurements(registration, packet, *, evidence="synthetic_fixture"):
    records = []
    for cell in CELLS:
        profile = registration["profiles"][cell]
        for probe in packet["probes"]:
            answer = {"decision": probe["gold"]["decision"], "explanation": "SOFTWARE FIXTURE: not an actual model answer."}
            # Cluster 0 improves by one; cluster 1 improves by one half.
            score = 0 if cell == "update_pre" else 1 if cell == "update_post" else 0.25
            if probe["cluster_id"] == "mechanism-1" and cell == "update_post":
                score = 0.5
            review = {"schema_version": "qcb.learning_semantic_review.v1", "probe_id": probe["probe_id"],
                      "answer_digest": digest(answer), "rubric_digest": digest(probe["gold"]["rubric"]),
                      "reviewer": {"identity": "fixture-independent-reviewer", "kind": "human", "method": "Invented marks for software tests."},
                      "respondent_identity": profile["model_id"], "blinded_packet_digest": digest(review_input(probe, answer)),
                      "blinding": {"arm_hidden": True, "phase_hidden": True, "model_hidden": True, "formal_result_hidden": True},
                      "criteria": [{"id": c["id"], "score": score, "reason": "Invented criterion expectation."} for c in probe["gold"]["rubric"]],
                      "semantic_fidelity": "faithful", "reasoning": "SOFTWARE FIXTURE ONLY."}
            identity = cell + ":" + probe["probe_id"]
            messages = canonical_messages(registration, probe, cell=cell)
            records.append({"schema_version": "qcb.learning_measurement.v1", "measurement_id": identity,
                            "registration_digest": digest(registration), "cohort_digest": digest(packet),
                            "cell": cell, "probe_id": probe["probe_id"], "profile_digest": digest(profile),
                            "execution_class": evidence, "generation_status": "answered", "answer": answer,
                            "answer_digest": digest(answer), "semantic_review": review,
                            "session": {"id": identity, "fresh_context": True, "assessment_feedback_received": False,
                                        "input_digest": digest(stage_a_input(probe)), "messages": messages, "prompt_digest": digest(messages)},
                            "usage": {"calls": 1, "input_tokens": 100, "output_tokens": 50, "wall_seconds": 1, "endpoint_cost_usd": 0}})
    return records


def attestation(registration, packet, records):
    return {"schema_version": "qcb.learning_operator_attestation.v1", "registration_digest": digest(registration),
            "cohort_digest": digest(packet), "operator_identity": registration["operator_identity"],
            "measurement_digests": [digest(r) for r in records],
            "review_digests": sorted({digest(r["semantic_review"]) for r in records if r["semantic_review"] is not None}),
            "prompt_execution_receipts": [
                {"measurement_digest": digest(r), "prompt_digest": r["session"]["prompt_digest"],
                 "rendered_input_sha256": digest(["SOFTWARE MOCK RENDER", r["session"]["messages"]]),
                 "rendered_token_ids_sha256": digest(["SOFTWARE MOCK TOKENS", r["session"]["messages"]]),
                 "transcript_sha256": digest(["SOFTWARE MOCK TRANSCRIPT", r]),
                 "evidence_reference": "Software-only rendering fixture; no actual token stream exists."}
                for r in records if r["generation_status"] in {"answered", "abstained"}
                or r["usage"] is not None and r["usage"]["calls"] > 0],
            "intervention_receipt": {"kind": registration["intervention"]["kind"],
                                     "base_checkpoint_revision": registration["profiles"]["update_pre"]["checkpoint_revision"],
                                     "post_checkpoint_revision": registration["profiles"]["update_post"]["checkpoint_revision"],
                                     "material_sha256": registration["intervention"]["material_sha256"], "completed": True,
                                     "optimizer_steps": registration["intervention"]["planned_optimizer_steps"],
                                     "evidence_reference": "Software test only; no training occurred."},
            "claims": {"actual_model_execution_observed": True, "checkpoint_identities_checked": True,
                       "architecture_runtime_precision_and_size_checked": True,
                       "actual_prompt_transcripts_match_canonical_messages_checked": True,
                       "rendered_tokens_match_registered_template_and_policy_checked": True,
                       "registration_precedes_assessment_checked": True, "fresh_context_and_no_feedback_checked": True,
                       "reviews_blinded_and_independent_checked": True, "cohort_gold_and_rubrics_reviewed_checked": True,
                       "training_excludes_dev_test_answers_checked": True,
                       "assessment_records_excluded_from_training_checked": True},
            "evidence_reference": "Mock authentication routing fixture; not actual evidence.", "signature": "not-a-real-signature"}


class LearningDesignTests(unittest.TestCase):
    def setUp(self):
        self.packet = cohort()
        self.registration = registered(self.packet)
        self.records = measurements(self.registration, self.packet)

    def test_default_draft_is_not_ready_and_empty_measurements_have_no_gains(self):
        draft = experiment_template(self.packet)
        checked = validate_experiment(draft, self.packet)
        self.assertEqual(checked["status"], "NOT_READY")
        report = analyze_experiment(draft, self.packet, [])
        self.assertIsNone(report["learning_gain"])
        self.assertFalse(report["declared_resource_profiles_matched"])
        self.assertEqual(report["generation_outcomes"], {"not_submitted": 16})

    def test_valid_registration_does_not_establish_execution(self):
        checked = validate_experiment(self.registration, self.packet)
        self.assertEqual(checked["status"], "REGISTERED")
        self.assertFalse(checked["model_performance_measured"])
        self.assertIsNone(checked["learning_gain"])

    def test_template_binds_implemented_prompt_policy_and_defaults_to_zero_endpoint_spend(self):
        template = profile_template()
        self.assertEqual(template["prompt_policy_sha256"], digest(canonical_prompt_policy()))
        self.assertEqual(template["resources"]["max_endpoint_cost_usd"], 0)
        for key in ("architecture_sha256", "runtime_sha256", "parameter_count", "dtype", "quantization"):
            self.assertIsNone(template[key])

    def test_canonical_weight_prompts_are_identical_and_controller_metadata_stays_outside(self):
        probe = self.packet["probes"][0]
        prompts = [canonical_messages(self.registration, probe, cell=cell) for cell in CELLS]
        self.assertTrue(all(messages == prompts[0] for messages in prompts))
        self.assertEqual(len(prompts[0]), 2)
        user = json.loads(prompts[0][-1]["content"])
        self.assertEqual(set(user), {"question", "assumptions", "conventions", "response_format"})
        self.assertNotIn(probe["probe_id"], json.dumps(prompts[0]))
        exposed = stage_a_input(probe)
        exposed.update(state_id="secret state", arm="update", phase="post", model="secret model", gold={"decision": "holds"})
        with patch("qcb_learning_design.stage_a_input", return_value=exposed):
            self.assertEqual(canonical_messages(self.registration, probe, cell="update_post"), prompts[0])

    def test_contextual_prompt_has_exact_literal_lesson_only_in_update_post(self):
        registration = registered(self.packet, kind="in_context")
        probe = self.packet["probes"][0]
        baseline = canonical_messages(registration, probe, cell="update_pre")
        for cell in ("no_update_pre", "no_update_post"):
            self.assertEqual(canonical_messages(registration, probe, cell=cell), baseline)
        after = canonical_messages(registration, probe, cell="update_post")
        self.assertEqual(after, [baseline[0], {"role": "user", "content": registration["intervention"]["lesson_text"]}, baseline[1]])
        self.assertEqual(hashlib.sha256(after[1]["content"].encode("utf-8")).hexdigest(), registration["intervention"]["material_sha256"])

    def test_opaque_mismatched_or_hidden_lesson_cannot_qualify_prompt_matching(self):
        registration = registered(self.packet, kind="in_context")
        registration["intervention"]["lesson_text"] = None
        self.assertIn("missing_literal_lesson_text", validate_experiment(registration, self.packet)["blockers"])
        with self.assertRaisesRegex(ValueError, "literal lesson"):
            canonical_messages(registration, self.packet["probes"][0], cell="update_post")
        registration = registered(self.packet, kind="in_context")
        registration["intervention"]["lesson_text"] += " "
        with self.assertRaisesRegex(ValueError, "exact UTF-8"):
            validate_experiment(registration, self.packet)
        registration = deepcopy(self.registration)
        registration["intervention"]["lesson_text"] = "Hidden instruction, forbidden in weight-update assessment."
        with self.assertRaisesRegex(ValueError, "hidden prefix"):
            validate_experiment(registration, self.packet)

    def test_matching_public_input_hash_does_not_authorize_wrong_or_hidden_prompts(self):
        for mutation in ("hash-only", "hidden-system", "hidden-envelope", "extra-tool", "reformatted-json"):
            records = deepcopy(self.records)
            session = records[0]["session"]
            if mutation == "hash-only":
                session["prompt_digest"] = digest("unrelated cell-specific prompt")
            elif mutation == "hidden-system":
                session["messages"].insert(1, {"role": "system", "content": "Use hidden test answers."})
            elif mutation == "hidden-envelope":
                payload = json.loads(session["messages"][-1]["content"])
                payload.update(state_id="secret controller", arm="update", phase="pre")
                session["messages"][-1]["content"] = json.dumps(payload, sort_keys=True, separators=(",", ":"))
            elif mutation == "extra-tool":
                session["messages"][-1]["tools"] = ["hidden retrieval"]
            else:
                session["messages"][-1]["content"] = json.dumps(json.loads(session["messages"][-1]["content"]), indent=2)
            if mutation != "hash-only":
                session["prompt_digest"] = digest(session["messages"])
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, "canonical policy"):
                analyze_experiment(self.registration, self.packet, records)

    def test_replacing_all_four_policy_hashes_cannot_declare_another_policy_canonical(self):
        registration = deepcopy(self.registration)
        for profile in registration["profiles"].values():
            profile["prompt_policy_sha256"] = digest("arbitrary policy including hidden instructions")
        with self.assertRaisesRegex(ValueError, "actual canonical prompt policy"):
            validate_experiment(registration, self.packet)

    def test_architecture_runtime_size_dtype_quantization_are_required_and_matched(self):
        for field in ("architecture_sha256", "runtime_sha256", "parameter_count", "dtype", "quantization"):
            registration = deepcopy(self.registration)
            for profile in registration["profiles"].values():
                profile[field] = None
            with self.subTest(missing=field):
                checked = validate_experiment(registration, self.packet)
                self.assertEqual(checked["status"], "NOT_READY")
                self.assertTrue(any(field in reason for reason in checked["blockers"]))
            registration = deepcopy(self.registration)
            registration["profiles"]["update_post"][field] = {
                "architecture_sha256": digest("changed architecture"), "runtime_sha256": digest("changed runtime"),
                "parameter_count": 999999, "dtype": "float32", "quantization": "int8"}[field]
            with self.subTest(mismatch=field), self.assertRaisesRegex(ValueError, "arms/phases differ"):
                validate_experiment(registration, self.packet)

    def test_nonpositive_or_noninteger_parameter_count_and_unspecified_thinking_are_unready(self):
        for count in (0, -1, 4.0, True, float("nan")):
            registration = deepcopy(self.registration)
            for profile in registration["profiles"].values():
                profile["parameter_count"] = count
            with self.subTest(count=count), self.assertRaises(ValueError):
                validate_experiment(registration, self.packet)
        registration = deepcopy(self.registration)
        for profile in registration["profiles"].values():
            profile["sampling"]["thinking_mode"] = "unspecified"
        checked = validate_experiment(registration, self.packet)
        self.assertEqual(checked["status"], "NOT_READY")
        self.assertTrue(any("sampling.thinking_mode" in reason for reason in checked["blockers"]))

    def test_contrasts_are_not_parallel_forms_and_train_aliases_not_heldout(self):
        for scope in ("fresh_instance_transfer", "family_transfer", "composition_transfer"):
            with self.subTest(scope=scope):
                draft = experiment_template(self.packet, scope=scope)
                self.assertNotIn(self.packet["probes"][0]["probe_id"], draft["assessment"]["probe_ids"])
                self.assertEqual(validate_experiment(draft, self.packet)["status"], "NOT_READY")
                draft["assessment"]["probe_ids"].append(self.packet["probes"][0]["probe_id"])
                with self.assertRaisesRegex(ValueError, "train aliases"):
                    validate_experiment(draft, self.packet)
        draft = experiment_template(self.packet, scope="fresh_instance_transfer")
        draft["assessment"]["parallel_form_review_digest"] = digest("invented approval")
        with self.assertRaisesRegex(ValueError, "no independently reviewed"):
            validate_experiment(draft, self.packet)

    def test_mismatched_arm_checkpoint_template_sampling_and_budget_rejected(self):
        for field in ("checkpoint_revision", "chat_template_sha256", "tokenizer_sha256", "adapter_sha256", "prompt_policy_sha256"):
            with self.subTest(field=field):
                edited = deepcopy(self.registration)
                edited["profiles"]["no_update_post"][field] = digest("changed")
                with self.assertRaises(ValueError):
                    validate_experiment(edited, self.packet)
        for group, field in (("sampling", "temperature"), ("resources", "max_output_tokens")):
            edited = deepcopy(self.registration)
            edited["profiles"]["update_post"][group][field] = 1
            with self.assertRaises(ValueError):
                validate_experiment(edited, self.packet)

    def test_no_update_and_in_context_weight_semantics(self):
        contextual = registered(self.packet, kind="in_context")
        self.assertEqual(validate_experiment(contextual, self.packet)["status"], "REGISTERED")
        contextual["profiles"]["update_post"]["checkpoint_revision"] = digest("different weights")
        with self.assertRaisesRegex(ValueError, "contextual learning"):
            validate_experiment(contextual, self.packet)
        unchanged = deepcopy(self.registration)
        unchanged["profiles"]["update_post"]["checkpoint_revision"] = unchanged["profiles"]["update_pre"]["checkpoint_revision"]
        with self.assertRaisesRegex(ValueError, "different artifact"):
            validate_experiment(unchanged, self.packet)

    def test_training_on_test_or_unknown_alias_is_rejected(self):
        for core in ("core-1", "unknown-core"):
            edited = deepcopy(self.registration)
            edited["intervention"]["training_core_ids"] = [core]
            with self.assertRaisesRegex(ValueError, "known train"):
                validate_experiment(edited, self.packet)

    def test_synthetic_fixture_never_becomes_actual_model_gain_even_with_trust_hook(self):
        evidence = attestation(self.registration, self.packet, self.records)
        result = analyze_experiment(self.registration, self.packet, self.records,
                                    operator_attestation=evidence, attestation_verifier=lambda _: True)
        self.assertIsNone(result["learning_gain"])
        self.assertFalse(result["model_performance_measured"])
        self.assertIn("non_model_or_missing_observation_provenance", result["blockers"])
        self.assertFalse(result["probe_count_is_independent_sample_size"])

    def test_signed_looking_json_and_unattested_scores_cannot_award_gain(self):
        records = measurements(self.registration, self.packet, evidence="operator_model_observation")
        evidence = attestation(self.registration, self.packet, records)
        for kwargs in ({}, {"operator_attestation": evidence},
                       {"operator_attestation": evidence, "attestation_verifier": lambda _: False},
                       {"operator_attestation": evidence, "attestation_verifier": lambda _: "true"}):
            with self.subTest(kwargs=sorted(kwargs)):
                result = analyze_experiment(self.registration, self.packet, records, **kwargs)
                self.assertIsNone(result["learning_gain"])
                self.assertFalse(result["model_performance_measured"])

    def test_mock_authenticated_branch_computes_cluster_macro_did_only(self):
        # Pure software branch test with invented records. No scientific result.
        records = measurements(self.registration, self.packet, evidence="operator_model_observation")
        evidence = attestation(self.registration, self.packet, records)
        result = analyze_experiment(self.registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda supplied: supplied == evidence)
        self.assertAlmostEqual(result["learning_gain"], 0.75)
        self.assertEqual(result["cluster_count"], 2)
        self.assertTrue(result["too_few_clusters_for_inference"])
        self.assertIsNone(result["p_value"])
        self.assertIsNone(result["confidence_interval"])
        self.assertFalse(result["learning_claim_supported"])
        self.assertFalse(result["heldout_transfer_established"])

    def test_shared_parent_cores_merge_mechanism_clusters(self):
        packet = deepcopy(self.packet)
        # Both public-test, so a shared core legitimately connects mechanisms.
        packet["probes"][2]["parent_core_ids"] = ["core-1"]
        packet["probes"][2]["parent_contracts"] = {"core-1": digest(1)}
        registration = registered(packet)
        result = analyze_experiment(registration, packet, [])
        self.assertEqual(result["cluster_count"], 1)

    def test_missing_wrong_env_blocked_and_not_run_are_distinct(self):
        records = deepcopy(self.records)
        records.pop()
        wrong = records[0]
        wrong["answer"]["decision"] = "refuted"
        wrong["answer_digest"] = digest(wrong["answer"])
        wrong["semantic_review"] = None
        for row, outcome in zip(records[1:3], ("env_blocked", "not_run")):
            row.update(generation_status=outcome, answer=None, answer_digest=None, semantic_review=None, usage=None)
        result = analyze_experiment(self.registration, self.packet, records)
        self.assertEqual(result["generation_outcomes"]["not_submitted"], 1)
        self.assertEqual(result["generation_outcomes"]["env_blocked"], 1)
        self.assertEqual(result["generation_outcomes"]["not_run"], 1)
        self.assertFalse(next(r for r in result["rows"] if r["measurement_digest"] == digest(wrong))["decision_correct"])
        self.assertEqual(result["decision_outcomes"]["answered_wrong"], 1)
        self.assertIsNone(result["learning_gain"])
        self.assertIn("incomplete_four_cell_semantic_matrix", result["blockers"])

    def test_one_missing_cell_blocks_even_verified_complete_case_selection(self):
        records = measurements(self.registration, self.packet, evidence="operator_model_observation")[:-1]
        evidence = attestation(self.registration, self.packet, records)
        result = analyze_experiment(self.registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)
        self.assertEqual(result["complete_four_cell_probe_count"], 3)
        self.assertEqual(result["cluster_contrasts"], [])
        self.assertIsNone(result["learning_gain"])

    def test_forged_self_author_unblinded_and_stale_reviews_fail(self):
        for mutation in ("self", "author", "unblinded", "stale-answer", "stale-rubric", "summary-grade"):
            with self.subTest(mutation=mutation):
                records = deepcopy(self.records)
                review = records[0]["semantic_review"]
                if mutation == "self":
                    review["reviewer"]["identity"] = review["respondent_identity"]
                elif mutation == "author":
                    review["reviewer"]["identity"] = "fixture-author"
                elif mutation == "unblinded":
                    review["blinding"]["arm_hidden"] = False
                elif mutation == "stale-answer":
                    review["answer_digest"] = digest("different answer")
                elif mutation == "stale-rubric":
                    review["rubric_digest"] = digest("different rubric")
                else:
                    records[0]["score"] = 1
                with self.assertRaises(ValueError):
                    analyze_experiment(self.registration, self.packet, records)

    def test_wrong_polarity_cannot_get_semantic_credit_from_forged_high_marks(self):
        records = deepcopy(self.records)
        row = records[0]
        probe = self.packet["probes"][0]
        row["answer"]["decision"] = "refuted"
        row["answer_digest"] = digest(row["answer"])
        review = row["semantic_review"]
        review["answer_digest"] = row["answer_digest"]
        review["blinded_packet_digest"] = digest(review_input(probe, row["answer"]))
        for criterion in review["criteria"]:
            criterion["score"] = 1
        result = analyze_experiment(self.registration, self.packet, records)
        self.assertEqual(result["rows"][0]["supplied_partial_mark_unauthenticated"], 1)
        self.assertEqual(result["rows"][0]["supplied_semantic_mark_unauthenticated"], 0)

    def test_duplicate_reused_session_wrong_profile_and_bad_usage_rejected(self):
        for mutation in ("duplicate", "session", "profile", "usage", "feedback", "nan"):
            records = deepcopy(self.records)
            if mutation == "duplicate":
                records[-1] = deepcopy(records[0])
            elif mutation == "session":
                records[1]["session"]["id"] = records[0]["session"]["id"]
            elif mutation == "profile":
                records[0]["profile_digest"] = digest("different profile")
            elif mutation == "feedback":
                records[0]["session"]["assessment_feedback_received"] = True
            else:
                records[0]["usage"]["output_tokens"] = float("nan") if mutation == "nan" else 999999
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                analyze_experiment(self.registration, self.packet, records)

    def test_attestation_wrong_records_receipt_and_truthy_booleans_rejected(self):
        for mutation in ("record", "receipt", "claim", "integer-boolean", "float-steps"):
            evidence = attestation(self.registration, self.packet, self.records)
            if mutation == "record":
                evidence["measurement_digests"][0] = digest("a different episode")
            elif mutation == "receipt":
                evidence["intervention_receipt"]["completed"] = False
            elif mutation == "claim":
                evidence["claims"]["actual_model_execution_observed"] = "true"
            elif mutation == "integer-boolean":
                evidence["claims"]["actual_model_execution_observed"] = 1
            else:
                evidence["intervention_receipt"]["optimizer_steps"] = 2.0
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                analyze_experiment(self.registration, self.packet, self.records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)

    def test_actual_prompt_execution_requires_more_than_matching_declared_message_hashes(self):
        records = measurements(self.registration, self.packet, evidence="operator_model_observation")
        for mutation in ("missing-receipts", "wrong-messages", "wrong-measurement", "missing-rendering", "unchecked-transcripts"):
            evidence = attestation(self.registration, self.packet, records)
            if mutation == "missing-receipts":
                evidence["prompt_execution_receipts"] = []
            elif mutation == "wrong-messages":
                evidence["prompt_execution_receipts"][0]["prompt_digest"] = digest("different messages")
            elif mutation == "wrong-measurement":
                evidence["prompt_execution_receipts"][0]["measurement_digest"] = digest("different run")
            elif mutation == "missing-rendering":
                evidence["prompt_execution_receipts"][0].pop("rendered_token_ids_sha256")
            else:
                evidence["claims"]["actual_prompt_transcripts_match_canonical_messages_checked"] = False
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                analyze_experiment(self.registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)
        result = analyze_experiment(self.registration, self.packet, records,
                                    operator_attestation=attestation(self.registration, self.packet, records))
        self.assertTrue(result["canonical_declared_messages_validated"])
        self.assertEqual(result["actual_prompt_execution_basis"], "not_authenticated")
        self.assertFalse(result["rendered_tokens_independently_authenticated_by_this_module"])
        self.assertIsNone(result["learning_gain"])

    def test_review_projection_omits_arm_phase_model_and_formal_gold(self):
        projection = review_input(self.packet["probes"][0], self.records[0]["answer"])
        self.assertEqual(set(projection), {"input", "answer", "rubric"})
        self.assertNotIn("formal_context", projection["input"])
        self.assertNotIn("gold", projection["input"])
        self.assertNotIn("model_id", projection)

    def test_same_retest_improvement_in_control_is_not_a_positive_did(self):
        records = measurements(self.registration, self.packet, evidence="operator_model_observation")
        for record in records:
            for criterion in record["semantic_review"]["criteria"]:
                criterion["score"] = 1 if record["cell"].endswith("post") else 0
        evidence = attestation(self.registration, self.packet, records)
        result = analyze_experiment(self.registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)
        self.assertEqual(result["learning_gain"], 0)
        self.assertFalse(result["learning_claim_supported"])

    def test_unequal_probe_counts_do_not_reweight_the_independent_cluster_mean(self):
        registration = deepcopy(self.registration)
        registration["assessment"]["probe_ids"].remove(self.packet["probes"][1]["probe_id"])
        records = [r for r in measurements(registration, self.packet, evidence="operator_model_observation")
                   if r["probe_id"] in registration["assessment"]["probe_ids"]]
        evidence = attestation(registration, self.packet, records)
        result = analyze_experiment(registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)
        self.assertAlmostEqual(result["learning_gain"], 0.75)
        self.assertEqual(sorted(len(g["probe_ids"]) for g in result["clusters"]), [1, 2])

    def test_uncertain_review_and_unknown_usage_each_keep_the_whole_gain_null(self):
        for missing in ("review", "usage"):
            records = measurements(self.registration, self.packet, evidence="operator_model_observation")
            if missing == "review":
                records[0]["semantic_review"]["semantic_fidelity"] = "uncertain"
            else:
                records[0]["usage"] = None
            evidence = attestation(self.registration, self.packet, records)
            result = analyze_experiment(self.registration, self.packet, records, operator_attestation=evidence,
                                        attestation_verifier=lambda _: True)
            with self.subTest(missing=missing):
                self.assertIsNone(result["learning_gain"])

    def test_contextual_contrast_cannot_be_labelled_parameter_learning(self):
        registration = registered(self.packet, kind="in_context")
        records = measurements(registration, self.packet, evidence="operator_model_observation")
        evidence = attestation(registration, self.packet, records)
        result = analyze_experiment(registration, self.packet, records, operator_attestation=evidence,
                                    attestation_verifier=lambda _: True)
        self.assertIsNotNone(result["learning_gain"])
        self.assertFalse(result["parameter_learning_assessed"])

    def test_alias_split_conflict_and_unearned_clean_contamination_label_fail(self):
        packet = deepcopy(self.packet)
        packet["probes"][1]["parent_core_ids"] = ["core-0"]
        packet["probes"][1]["parent_contracts"] = {"core-0": digest(0)}
        with self.assertRaisesRegex(ValueError, "aliases disagree"):
            experiment_template(packet)
        registration = deepcopy(self.registration)
        registration["source_exposure"]["pretraining_exposure"] = "contamination_free"
        with self.assertRaisesRegex(ValueError, "public sources"):
            validate_experiment(registration, self.packet)


if __name__ == "__main__":
    unittest.main()
