"""Pure registration and conservative offline matched-learning analysis.

Imported JSON cannot attest to itself. An optional trusted caller-supplied
attestation verifier is the only route to an operator-attested contrast. This
module calls neither models nor Lean and admits no new gold or parallel forms.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from copy import deepcopy
from uuid import uuid4

from qcb_core import digest
from qcb_learning_validity import (
    OUTCOMES,
    stage_a_input,
    validate_answer,
    validate_probe,
)

CELLS = ("update_pre", "update_post", "no_update_pre", "no_update_post")
SCOPES = {"public_retest", "fresh_instance_transfer", "family_transfer", "composition_transfer"}
PROVENANCE = {"synthetic_fixture", "unattested_import", "operator_model_observation"}
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_REVISION = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


def _shape(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError("unexpected fields: " + label)


def _text(value, label, *, limit=4096):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError("bounded nonempty text required: " + label)


def _hash(value, label, *, nullable=False, revision=False):
    if nullable and value is None:
        return
    if not isinstance(value, str) or not (_REVISION if revision else _HASH).fullmatch(value):
        raise ValueError("literal SHA identity required: " + label)


def _number(value, label, *, minimum=0, maximum=1e9, integer=False):
    if (type(value) not in ((int,) if integer else (int, float)) or not math.isfinite(value)
            or not minimum <= value <= maximum):
        raise ValueError("finite bounded numeric value required: " + label)


def canonical_prompt_policy():
    """The fixed, content-bound policy; controller identities are never text."""
    return {"schema_version": "qcb.learning_prompt_policy.v1",
            "system_instruction": "Assess the mathematical proposition using the supplied assumptions and conventions. "
                "Treat any preceding lesson as study material, not additional assumptions. Return exactly one JSON object "
                "with decision (holds, refuted, or abstain) and explanation containing your argument or a precise witness. "
                "Do not use tools or request formal-proof feedback.",
            "assessment_fields": ["question", "assumptions", "conventions", "response_format"],
            "serialization": {"sort_keys": True, "ensure_ascii": False, "separators": [",", ":"], "allow_nan": False},
            "message_order": ["system_instruction", "optional_literal_user_lesson", "user_assessment_json"],
            "lesson_condition": "in_context_update_post_only_exact_utf8_text",
            "controller_metadata_in_messages": False}


def _lesson_material(intervention):
    lesson = intervention["lesson_text"]
    if intervention["kind"] == "weight_update":
        if lesson is not None:
            raise ValueError("weight-update assessment cannot contain a lesson or hidden prefix")
        return None
    if intervention["kind"] != "in_context":
        raise ValueError("unknown lesson intervention kind")
    if lesson is None:
        return None
    _text(lesson, "literal lesson text", limit=64000)
    try:
        actual = hashlib.sha256(lesson.encode("utf-8")).hexdigest()
    except UnicodeEncodeError as error:
        raise ValueError("lesson must have a literal valid UTF-8 encoding") from error
    if intervention["material_sha256"] != actual:
        raise ValueError("lesson material must hash the exact UTF-8 lesson text, without normalization")
    return lesson


def canonical_messages(registration, probe, *, cell):
    """Assemble declared messages, not proof of the adapter's rendered tokens.

    The fixed allowlist excludes Stage-A probe/schema/state/controller IDs and
    all evaluator metadata. Weight-update prompts are identical across cells.
    """
    if cell not in CELLS:
        raise ValueError("unknown matched cell")
    policy = canonical_prompt_policy()
    source = stage_a_input(probe)
    assessment = {key: deepcopy(source[key]) for key in policy["assessment_fields"]}
    intervention = registration["intervention"]
    lesson = _lesson_material(intervention)
    messages = [{"role": "system", "content": policy["system_instruction"]}]
    if cell == "update_post" and intervention["kind"] == "in_context":
        if lesson is None:
            raise ValueError("an in-context prompt needs the registered literal lesson, not an opaque prefix hash")
        messages.append({"role": "user", "content": lesson})
    messages.append({"role": "user", "content": json.dumps(assessment, sort_keys=True, ensure_ascii=False,
                                                              separators=(",", ":"), allow_nan=False)})
    return messages


def _probes(packet):
    if not isinstance(packet, dict) or not isinstance(packet.get("probes"), list) or not packet["probes"]:
        raise ValueError("a nonempty normalized cohort is required")
    result = {}
    parents = {}
    for raw in packet["probes"]:
        probe = validate_probe(raw)
        if probe["probe_id"] in result:
            raise ValueError("duplicate probe identity")
        result[probe["probe_id"]] = probe
        for core in probe["parent_core_ids"]:
            identity = (probe["split"], probe["parent_contracts"][core])
            _hash(identity[1], "parent contract")
            if core in parents and parents[core] != identity:
                raise ValueError("source aliases disagree about split or contract")
            parents[core] = identity
    return result, parents


def experiment_template(packet, *, scope="public_retest"):
    """Create a valid NOT_READY draft, never invented model or review evidence."""
    probes, _ = _probes(packet)
    if scope not in SCOPES:
        raise ValueError("unknown learning scope")
    return {"schema_version": "qcb.learning_experiment.v1", "experiment_id": str(uuid4()),
            "cohort_digest": digest(packet), "scope": scope, "operator_identity": None,
            "assessment": {"probe_ids": sorted(k for k, p in probes.items()
                                               if scope == "public_retest" or p["split"] != "train"),
                           "form_kind": "same_public_items" if scope == "public_retest" else "unprepared_parallel_forms",
                           "parallel_form_review_digest": None,
                           "cluster_policy": "merge_shared_mechanism_or_parent_core",
                           "minimum_clusters_for_inference": 10},
            "intervention": {"kind": "weight_update", "training_core_ids": [],
                             "material_sha256": None, "lesson_text": None, "planned_optimizer_steps": None},
            "profiles": dict.fromkeys(CELLS),
            "assumptions": {"fresh_context": True, "no_assessment_feedback": True,
                            "no_assessment_gold_in_intervention": True, "pretest_not_used_for_training": True},
            "assumptions_are_operator_declarations": True,
            "source_exposure": {"cohort": "public_semantic_calibration", "pretraining_exposure": "unknown"},
            "registration_evidence": "planned_not_executed"}


def profile_template():
    """Explicit placeholders deliberately do not qualify an actual model."""
    return {"model_id": None, "checkpoint_revision": None, "chat_template_sha256": None,
            "architecture_sha256": None, "runtime_sha256": None, "parameter_count": None,
            "dtype": None, "quantization": None,
            "tokenizer_sha256": None, "adapter_sha256": None, "prompt_policy_sha256": digest(canonical_prompt_policy()),
            "lesson_prefix_sha256": None, "exposure": "nl_only_closed_book_no_feedback",
            "sampling": {"seed": 0, "temperature": 0, "top_p": 1, "thinking_mode": "unspecified"},
            "resources": {"max_calls": 1, "max_input_tokens": 8192, "max_output_tokens": 2048,
                          "max_wall_seconds": 120, "max_endpoint_cost_usd": 0}}


def _profile(profile):
    _shape(profile, profile_template(), "model profile")
    missing = []
    for field in ("model_id", "checkpoint_revision", "chat_template_sha256", "tokenizer_sha256",
                  "adapter_sha256", "prompt_policy_sha256", "architecture_sha256", "runtime_sha256"):
        value = profile[field]
        if value is None:
            missing.append(field)
        elif field == "model_id":
            _text(value, field)
            if value.startswith("fixture:"):
                raise ValueError("fixture identity cannot be registered as an actual model")
        else:
            _hash(value, field, revision=field == "checkpoint_revision")
            if field == "prompt_policy_sha256" and value != digest(canonical_prompt_policy()):
                raise ValueError("profile must bind this implementation's actual canonical prompt policy")
    if profile["parameter_count"] is None:
        missing.append("parameter_count")
    else:
        _number(profile["parameter_count"], "parameter count", minimum=1, maximum=10**15, integer=True)
    for field in ("dtype", "quantization"):
        if profile[field] is None:
            missing.append(field)
        else:
            _text(profile[field], field)
            if profile[field].strip().casefold() in {"unknown", "unspecified", "auto", "placeholder"}:
                missing.append(field)
    _hash(profile["lesson_prefix_sha256"], "lesson prefix", nullable=True)
    if profile["exposure"] != "nl_only_closed_book_no_feedback":
        raise ValueError("semantic learning profiles cannot expose Lean, retrieval or feedback")
    sampling = profile["sampling"]
    _shape(sampling, {"seed", "temperature", "top_p", "thinking_mode"}, "sampling")
    _number(sampling["seed"], "seed", integer=True, maximum=2**32-1)
    _number(sampling["temperature"], "temperature", maximum=2)
    _number(sampling["top_p"], "top_p", minimum=1e-9, maximum=1)
    if sampling["thinking_mode"] not in {"enabled", "disabled", "unspecified"}:
        raise ValueError("explicit thinking mode required")
    if sampling["thinking_mode"] == "unspecified":
        missing.append("sampling.thinking_mode")
    resources = profile["resources"]
    _shape(resources, profile_template()["resources"], "resources")
    for field in ("max_calls", "max_input_tokens", "max_output_tokens"):
        _number(resources[field], field, minimum=1, maximum=1000000, integer=True)
    _number(resources["max_wall_seconds"], "wall ceiling", minimum=0.001, maximum=86400)
    _number(resources["max_endpoint_cost_usd"], "cost ceiling")
    return missing


def validate_experiment(registration, packet):
    """Validate exact identities/matching, returning explicit readiness blockers."""
    probes, parents = _probes(packet)
    expected = {"schema_version", "experiment_id", "cohort_digest", "scope", "operator_identity", "assessment",
                "intervention", "profiles", "assumptions", "assumptions_are_operator_declarations", "source_exposure",
                "registration_evidence"}
    _shape(registration, expected, "registration")
    if (registration["schema_version"] != "qcb.learning_experiment.v1"
            or registration["cohort_digest"] != digest(packet) or registration["scope"] not in SCOPES
            or registration["registration_evidence"] != "planned_not_executed"
            or registration["assumptions_are_operator_declarations"] is not True):
        raise ValueError("registration identity, scope or evidence policy differs")
    _text(registration["experiment_id"], "experiment identity")
    blockers = []
    if registration["operator_identity"] is None:
        blockers.append("missing_operator_identity")
    else:
        _text(registration["operator_identity"], "operator identity")
    assessment = registration["assessment"]
    _shape(assessment, {"probe_ids", "form_kind", "parallel_form_review_digest", "cluster_policy",
                        "minimum_clusters_for_inference"}, "assessment")
    keys = assessment["probe_ids"]
    if (not isinstance(keys, list) or not keys or any(not isinstance(k, str) or k not in probes for k in keys)
            or len(set(keys)) != len(keys)):
        raise ValueError("assessment must select unique known probes")
    if (assessment["cluster_policy"] != "merge_shared_mechanism_or_parent_core"
            or type(assessment["minimum_clusters_for_inference"]) is not int
            or not 10 <= assessment["minimum_clusters_for_inference"] <= 1000):
        raise ValueError("conservative declared cluster policy required")
    if assessment["parallel_form_review_digest"] is not None:
        raise ValueError("this version admits no independently reviewed parallel-form registry")
    retest = registration["scope"] == "public_retest"
    if assessment["form_kind"] != ("same_public_items" if retest else "unprepared_parallel_forms"):
        raise ValueError("contrasted propositions are not parallel pre/post forms")
    if not retest:
        if any(probes[k]["split"] == "train" for k in keys):
            raise ValueError("train aliases cannot be included in a heldout-transfer claim")
        blockers.append("no_independently_reviewed_parallel_forms_NOT_READY")
    assumptions = registration["assumptions"]
    _shape(assumptions, {"fresh_context", "no_assessment_feedback", "no_assessment_gold_in_intervention",
                         "pretest_not_used_for_training"}, "operator assumptions")
    if any(v is not True for v in assumptions.values()):
        raise ValueError("fresh context, no feedback and no evaluation-data training must be declared")
    if registration["source_exposure"] != {"cohort": "public_semantic_calibration", "pretraining_exposure": "unknown"}:
        raise ValueError("public sources do not establish absent pretraining contamination")
    intervention = registration["intervention"]
    _shape(intervention, {"kind", "training_core_ids", "material_sha256", "lesson_text", "planned_optimizer_steps"}, "intervention")
    if intervention["kind"] not in {"weight_update", "in_context"}:
        raise ValueError("weight updates and contextual instruction are separate interventions")
    training = intervention["training_core_ids"]
    if (not isinstance(training, list)
            or any(not isinstance(k, str) or k not in parents or parents[k][0] != "train" for k in training)
            or len(set(training)) != len(training)):
        raise ValueError("training aliases must bind known train parents, never dev/public-test answers")
    if not training:
        blockers.append("missing_training_core_reservation")
    _hash(intervention["material_sha256"], "intervention material", nullable=True)
    if intervention["material_sha256"] is None:
        blockers.append("missing_intervention_material_identity")
    lesson = _lesson_material(intervention)
    if intervention["kind"] == "in_context" and lesson is None:
        blockers.append("missing_literal_lesson_text")
    steps = intervention["planned_optimizer_steps"]
    if intervention["kind"] == "in_context":
        if steps is not None:
            raise ValueError("contextual instruction cannot declare optimizer steps")
    elif steps is None:
        blockers.append("missing_optimizer_step_plan")
    else:
        _number(steps, "optimizer steps", integer=True, minimum=1, maximum=100000000)
    profiles = registration["profiles"]
    _shape(profiles, CELLS, "four matched profiles")
    for cell, profile in profiles.items():
        if profile is None:
            blockers.append("missing_profile:" + cell)
        else:
            blockers.extend("missing_profile_identity:" + cell + ":" + k for k in _profile(profile))
    if all(p is not None for p in profiles.values()):
        baseline = profiles["update_pre"]
        for cell, profile in profiles.items():
            # Only the registered checkpoint or lesson prefix may differ.
            matched = {k: v for k, v in profile.items() if k not in {"checkpoint_revision", "lesson_prefix_sha256"}}
            if matched != {k: v for k, v in baseline.items() if k not in {"checkpoint_revision", "lesson_prefix_sha256"}}:
                raise ValueError("arms/phases differ in model, architecture, runtime, precision, template, sampling, exposure or declared resource ceilings")
            if cell != "update_post" and profile["checkpoint_revision"] != baseline["checkpoint_revision"]:
                raise ValueError("no-update control and pretest must retain the same checkpoint")
            prefix = intervention["material_sha256"] if cell == "update_post" and intervention["kind"] == "in_context" else None
            if profile["lesson_prefix_sha256"] != prefix:
                raise ValueError("only contextual update-post may carry the registered lesson prefix")
        after = profiles["update_post"]["checkpoint_revision"]
        before = baseline["checkpoint_revision"]
        if (before is not None and after is not None
                and (intervention["kind"] == "weight_update") == (before == after)):
            raise ValueError("weight learning requires a different artifact; contextual learning requires unchanged weights")
    return {"schema_version": "qcb.learning_registration_check.v1", "registration_digest": digest(registration),
            "cohort_digest": digest(packet), "status": "NOT_READY" if blockers else "REGISTERED",
            "blockers": blockers, "scope": registration["scope"],
            "train_alias_probe_ids": sorted(k for k in keys if probes[k]["split"] == "train"),
            "heldout_transfer_ready": False, "public_semantic_calibration": True,
            "operator_assumptions_verified": False, "model_performance_measured": False, "learning_gain": None}


def review_input(probe, answer):
    """A blinded review projection has no arm, phase, checkpoint or Lean outcome."""
    return {"input": stage_a_input(probe), "answer": validate_answer(answer), "rubric": deepcopy(probe["gold"]["rubric"])}


def _review(probe, answer, review, profile):
    _shape(review, {"schema_version", "probe_id", "answer_digest", "rubric_digest", "reviewer", "respondent_identity",
                    "blinded_packet_digest", "blinding", "criteria", "semantic_fidelity", "reasoning"}, "semantic review")
    if (review["schema_version"] != "qcb.learning_semantic_review.v1" or review["probe_id"] != probe["probe_id"]
            or review["answer_digest"] != digest(answer) or review["rubric_digest"] != digest(probe["gold"]["rubric"])
            or review["blinded_packet_digest"] != digest(review_input(probe, answer))):
        raise ValueError("review must bind exact answer, rubric and blinded packet")
    reviewer = review["reviewer"]
    _shape(reviewer, {"identity", "kind", "method"}, "reviewer")
    for field in ("identity", "method"):
        _text(reviewer[field], "reviewer " + field)
    if reviewer["kind"] not in {"human", "ai"}:
        raise ValueError("actual reviewer kind required")
    _text(review["respondent_identity"], "respondent identity")
    if (profile is None or profile["model_id"] is None
            or review["respondent_identity"] != profile["model_id"]
            or reviewer["identity"] in {review["respondent_identity"], probe["author_identity"]}):
        raise ValueError("respondent/self/author grades cannot act as independent semantic review")
    _shape(review["blinding"], {"arm_hidden", "phase_hidden", "model_hidden", "formal_result_hidden"}, "review blinding")
    if any(v is not True for v in review["blinding"].values()):
        raise ValueError("semantic review must declare all four blinding boundaries")
    if review["semantic_fidelity"] not in {"faithful", "unfaithful", "uncertain"}:
        raise ValueError("explicit semantic fidelity required")
    _text(review["reasoning"], "review reasoning")
    criteria = review["criteria"]
    if not isinstance(criteria, list):
        raise TypeError("complete criterion marks required")
    by_id = {}
    for mark in criteria:
        _shape(mark, {"id", "score", "reason"}, "criterion mark")
        _text(mark["id"], "criterion ID")
        if mark["id"] in by_id:
            raise ValueError("duplicate semantic criterion")
        _number(mark["score"], "criterion mark", maximum=1)
        _text(mark["reason"], "criterion reason")
        by_id[mark["id"]] = mark["score"]
    rubric = probe["gold"]["rubric"]
    if set(by_id) != {c["id"] for c in rubric}:
        raise ValueError("full bound semantic rubric required")
    partial = sum(c["weight"] * by_id[c["id"]] for c in rubric) / sum(c["weight"] for c in rubric)
    if review["semantic_fidelity"] == "uncertain":
        return partial, None
    semantic = partial if review["semantic_fidelity"] == "faithful" and answer["decision"] == probe["gold"]["decision"] else 0.0
    return partial, semantic


def _measurement(record, registration, packet, probes):
    _shape(record, {"schema_version", "measurement_id", "registration_digest", "cohort_digest", "cell", "probe_id",
                    "profile_digest", "execution_class", "generation_status", "answer", "answer_digest", "semantic_review",
                    "session", "usage"}, "measurement")
    if (record["schema_version"] != "qcb.learning_measurement.v1" or record["registration_digest"] != digest(registration)
            or record["cohort_digest"] != digest(packet) or record["cell"] not in CELLS
            or record["probe_id"] not in registration["assessment"]["probe_ids"]
            or record["execution_class"] not in PROVENANCE or record["generation_status"] not in OUTCOMES):
        raise ValueError("measurement identity, selected probe or typed provenance differs")
    _text(record["measurement_id"], "measurement identity")
    probe = probes[record["probe_id"]]
    profile = registration["profiles"][record["cell"]]
    if profile is None or record["profile_digest"] != digest(profile):
        raise ValueError("measurement must bind its registered cell profile")
    session = record["session"]
    _shape(session, {"id", "fresh_context", "assessment_feedback_received", "input_digest", "messages", "prompt_digest"}, "session")
    _text(session["id"], "fresh session identity")
    _hash(session["prompt_digest"], "actual prompt")
    if (session["fresh_context"] is not True or session["assessment_feedback_received"] is not False
            or session["input_digest"] != digest(stage_a_input(probe))):
        raise ValueError("assessment context/feedback/input differs from the registered no-feedback projection")
    messages = canonical_messages(registration, probe, cell=record["cell"])
    if session["messages"] != messages or session["prompt_digest"] != digest(messages):
        raise ValueError("prompt/messages differ from the exact canonical policy; hidden instructions and metadata are forbidden")
    status = record["generation_status"]
    answer = record["answer"]
    if status in {"answered", "abstained"}:
        answer = validate_answer(answer)
        if ((answer["decision"] == "abstain") != (status == "abstained") or record["answer_digest"] != digest(answer)):
            raise ValueError("answer digest or outcome disagrees")
    elif answer is not None or record["answer_digest"] is not None or record["semantic_review"] is not None:
        raise ValueError("missing/blocked outcomes cannot carry answers or semantic grades")
    usage = record["usage"]
    if usage is not None:
        resources = profile["resources"]
        _shape(usage, {"calls", "input_tokens", "output_tokens", "wall_seconds", "endpoint_cost_usd"}, "realized usage")
        for field, cap in (("calls", "max_calls"), ("input_tokens", "max_input_tokens"), ("output_tokens", "max_output_tokens"),
                           ("wall_seconds", "max_wall_seconds"), ("endpoint_cost_usd", "max_endpoint_cost_usd")):
            _number(usage[field], "usage " + field, integer=field in {"calls", "input_tokens", "output_tokens"}, maximum=resources[cap])
        if status in {"answered", "abstained"} and usage["calls"] < 1:
            raise ValueError("a claimed model answer must record a generation call")
    review = record["semantic_review"]
    partial = semantic = None
    if review is not None:
        if status != "answered":
            raise ValueError("only a substantive answered response can receive a semantic grade")
        partial, semantic = _review(probe, answer, review, profile)
    correct = answer["decision"] == probe["gold"]["decision"] if status == "answered" else None
    return {"cell": record["cell"], "probe_id": record["probe_id"], "generation_status": status,
            "execution_class": record["execution_class"], "decision_correct": correct,
            "semantic_status": "needs_review" if review is None and status == "answered" else
                "wrong" if semantic == 0 or correct is False else "uncertain" if review is not None and semantic is None else
                "reviewed" if review is not None else status,
            "supplied_partial_mark_unauthenticated": partial, "supplied_semantic_mark_unauthenticated": semantic,
            "measurement_digest": digest(record), "review_digest": None if review is None else digest(review),
            "usage_available": usage is not None}


def _clusters(selected):
    groups = []
    for probe in selected:
        touched = [g for g in groups if probe["cluster_id"] in g["mechanisms"] or set(probe["parent_core_ids"]) & g["cores"]]
        merged = {"probes": {probe["probe_id"]}, "mechanisms": {probe["cluster_id"]}, "cores": set(probe["parent_core_ids"])}
        for group in touched:
            for key in merged:
                merged[key] |= group[key]
            groups.remove(group)
        groups.append(merged)
    return [{"cluster_id": digest(sorted(g["probes"])), "probe_ids": sorted(g["probes"]),
             "declared_mechanisms": sorted(g["mechanisms"]), "parent_core_ids": sorted(g["cores"])}
            for g in sorted(groups, key=lambda g: sorted(g["probes"]))]


def _attestation(attestation, registration, packet, records):
    _shape(attestation, {"schema_version", "registration_digest", "cohort_digest", "operator_identity", "measurement_digests",
                         "review_digests", "prompt_execution_receipts", "intervention_receipt", "claims",
                         "evidence_reference", "signature"}, "operator attestation")
    if (attestation["schema_version"] != "qcb.learning_operator_attestation.v1"
            or attestation["registration_digest"] != digest(registration) or attestation["cohort_digest"] != digest(packet)
            or attestation["operator_identity"] != registration["operator_identity"]):
        raise ValueError("attestation binds a different registration/cohort/operator")
    for field, expected in (("measurement_digests", [digest(r) for r in records]),
                            ("review_digests", sorted({digest(r["semantic_review"]) for r in records if r["semantic_review"] is not None}))):
        values = attestation[field]
        if (not isinstance(values, list) or any(not isinstance(v, str) or not _HASH.fullmatch(v) for v in values)
                or len(set(values)) != len(values) or sorted(values) != sorted(expected)):
            raise ValueError("attestation must bind every exact measurement/review, without extras")
    _shape(attestation["claims"], {"actual_model_execution_observed", "checkpoint_identities_checked",
                                   "registration_precedes_assessment_checked", "fresh_context_and_no_feedback_checked",
                                   "reviews_blinded_and_independent_checked", "cohort_gold_and_rubrics_reviewed_checked",
                                   "training_excludes_dev_test_answers_checked",
                                   "architecture_runtime_precision_and_size_checked",
                                   "actual_prompt_transcripts_match_canonical_messages_checked",
                                   "rendered_tokens_match_registered_template_and_policy_checked",
                                   "assessment_records_excluded_from_training_checked"}, "operator claims")
    if any(v is not True for v in attestation["claims"].values()):
        raise ValueError("all operator evidence obligations must be explicit")
    for field in ("evidence_reference", "signature"):
        _text(attestation[field], field)
    # References/hashes bind evidence for the trusted verifier to inspect; they
    # are not themselves authentication of the actual adapter or token stream.
    expected_prompts = {digest(r): r["session"]["prompt_digest"] for r in records
                        if r["generation_status"] in {"answered", "abstained"}
                        or r["usage"] is not None and r["usage"]["calls"] > 0}
    prompt_receipts = attestation["prompt_execution_receipts"]
    if not isinstance(prompt_receipts, list) or len(prompt_receipts) != len(expected_prompts):
        raise ValueError("actual generation needs one bound prompt/transcript execution receipt per measurement")
    seen = set()
    for prompt_receipt in prompt_receipts:
        _shape(prompt_receipt, {"measurement_digest", "prompt_digest", "rendered_input_sha256", "rendered_token_ids_sha256",
                               "transcript_sha256", "evidence_reference"}, "prompt execution receipt")
        key = prompt_receipt["measurement_digest"]
        if (not isinstance(key, str) or key not in expected_prompts or key in seen
                or prompt_receipt["prompt_digest"] != expected_prompts[key]):
            raise ValueError("prompt execution receipt binds a different or duplicate measurement/message payload")
        seen.add(key)
        for field in ("rendered_input_sha256", "rendered_token_ids_sha256", "transcript_sha256"):
            _hash(prompt_receipt[field], field)
        _text(prompt_receipt["evidence_reference"], "actual prompt execution evidence")
    receipt = attestation["intervention_receipt"]
    _shape(receipt, {"kind", "base_checkpoint_revision", "post_checkpoint_revision", "material_sha256", "completed",
                     "optimizer_steps", "evidence_reference"}, "intervention receipt")
    intervention = registration["intervention"]
    profiles = registration["profiles"]
    if (receipt["kind"] != intervention["kind"] or receipt["completed"] is not True
            or receipt["material_sha256"] != intervention["material_sha256"]
            or type(receipt["optimizer_steps"]) is not type(intervention["planned_optimizer_steps"])
            or receipt["optimizer_steps"] != intervention["planned_optimizer_steps"]
            or profiles["update_pre"] is None or profiles["update_post"] is None
            or receipt["base_checkpoint_revision"] != profiles["update_pre"]["checkpoint_revision"]
            or receipt["post_checkpoint_revision"] != profiles["update_post"]["checkpoint_revision"]):
        raise ValueError("completed intervention receipt disagrees with its registered plan/checkpoints")
    _text(receipt["evidence_reference"], "actual intervention evidence")


def analyze_experiment(registration, packet, measurements, *, operator_attestation=None, attestation_verifier=None):
    """Analyze imported records; only trusted external attestation unlocks a DiD.

    ``attestation_verifier`` is trusted caller code, never an import/name from
    data. It must authenticate the whole attestation and return literal True.
    Without it, even impeccable signed-looking JSON remains unauthenticated.
    """
    readiness = validate_experiment(registration, packet)
    probes, _ = _probes(packet)
    if not isinstance(measurements, list) or len(measurements) > 4 * len(probes):
        raise ValueError("bounded measurement list required")
    rows, seen, session_ids, measurement_ids = [], set(), set(), set()
    for record in measurements:
        row = _measurement(record, registration, packet, probes)
        key = (row["cell"], row["probe_id"])
        if key in seen or record["session"]["id"] in session_ids or record["measurement_id"] in measurement_ids:
            raise ValueError("duplicate cell, measurement or reused assessment context")
        seen.add(key)
        session_ids.add(record["session"]["id"])
        measurement_ids.add(record["measurement_id"])
        rows.append(row)
    for cell in CELLS:
        for key in registration["assessment"]["probe_ids"]:
            if (cell, key) not in seen:
                rows.append({"cell": cell, "probe_id": key, "generation_status": "not_submitted",
                             "decision_correct": None, "semantic_status": "not_submitted",
                             "supplied_partial_mark_unauthenticated": None, "supplied_semantic_mark_unauthenticated": None,
                             "measurement_digest": None, "review_digest": None, "usage_available": False,
                             "execution_class": None})
    evidence_status = "not_supplied"
    attested = False
    if operator_attestation is not None:
        _attestation(operator_attestation, registration, packet, measurements)
        evidence_status = "unverified_import"
        if attestation_verifier is not None:
            if not callable(attestation_verifier):
                raise ValueError("trusted verifier must be caller code, never a data identifier")
            try:
                attested = attestation_verifier(deepcopy(operator_attestation)) is True
            except Exception:  # noqa: BLE001 - failed external authentication cannot award a gain.
                attested = False
            evidence_status = "externally_attested" if attested else "authentication_failed"
    elif attestation_verifier is not None:
        raise ValueError("a verifier needs an exact operator attestation to authenticate")
    indexed = {(r["cell"], r["probe_id"]): r for r in rows}
    complete = [key for key in registration["assessment"]["probe_ids"] if all(
        indexed[cell, key]["supplied_semantic_mark_unauthenticated"] is not None for cell in CELLS)]
    blockers = list(readiness["blockers"])
    if len(complete) != len(registration["assessment"]["probe_ids"]):
        blockers.append("incomplete_four_cell_semantic_matrix")
    if not attested:
        blockers.append("operator_measurement_and_review_evidence_not_authenticated")
    if any(r["execution_class"] != "operator_model_observation" for r in rows):
        blockers.append("non_model_or_missing_observation_provenance")
    if any(not r["usage_available"] for r in rows):
        blockers.append("missing_actual_usage")
    groups = _clusters([probes[k] for k in registration["assessment"]["probe_ids"]])
    gain = None
    contrasts = []
    if not blockers:
        for group in groups:
            means = {cell: sum(indexed[cell, key]["supplied_semantic_mark_unauthenticated"] for key in group["probe_ids"])
                     / len(group["probe_ids"]) for cell in CELLS}
            update = means["update_post"] - means["update_pre"]
            control = means["no_update_post"] - means["no_update_pre"]
            contrasts.append({"cluster_id": group["cluster_id"], "cell_means": means,
                              "update_change": update, "no_update_change": control, "difference_in_differences": update-control})
        gain = sum(c["difference_in_differences"] for c in contrasts) / len(contrasts)
    too_few = len(groups) < registration["assessment"]["minimum_clusters_for_inference"]
    return {"schema_version": "qcb.learning_analysis.v1", "registration_digest": digest(registration),
            "cohort_digest": digest(packet), "scope": registration["scope"], "status": "ATTESTED_CONTRAST" if gain is not None else "NO_LEARNING_ESTIMATE",
            "planned_measurements": 4 * len(registration["assessment"]["probe_ids"]), "submitted_measurements": len(measurements),
            "generation_outcomes": dict(Counter(r["generation_status"] for r in rows)),
            "decision_outcomes": dict(Counter("answered_correct" if r["decision_correct"] is True else
                "answered_wrong" if r["decision_correct"] is False else r["generation_status"] for r in rows)),
            "semantic_outcomes": dict(Counter(r["semantic_status"] for r in rows)),
            "complete_four_cell_probe_count": len(complete), "complete_probe_ids": complete,
            "excluded_from_complete_matrix": sorted(set(registration["assessment"]["probe_ids"]) - set(complete)),
            "operator_evidence_status": evidence_status, "blockers": blockers, "clusters": groups,
            "cluster_count": len(groups), "probe_count_is_independent_sample_size": False,
            "too_few_clusters_for_inference": too_few,
            "inference_status": "too_few_clusters_no_significance_claim" if too_few else "inferential_statistics_not_implemented",
            "p_value": None, "confidence_interval": None, "cluster_contrasts": contrasts,
            "learning_gain": gain, "model_performance_measured": gain is not None,
            "learning_claim_supported": False, "understanding_established": False, "heldout_transfer_established": False,
            "parameter_learning_assessed": gain is not None and registration["intervention"]["kind"] == "weight_update",
            "realized_compute_matched": False,
            "declared_resource_profiles_matched": all(p is not None and not _profile(p) for p in registration["profiles"].values()),
            "train_alias_probe_ids": readiness["train_alias_probe_ids"],
            "independent_authentication_performed_by_this_module": False,
            "canonical_declared_messages_validated": bool(measurements),
            "actual_prompt_execution_basis": "external_operator_attestation" if attested else "not_authenticated",
            "rendered_tokens_independently_authenticated_by_this_module": False,
            "scope_note": "An externally attested public-retest contrast is not fresh-instance/family/composition transfer or proof of understanding. Supplied marks stay unauthenticated until the trusted caller verifies the bound evidence.",
            "rows": rows}
