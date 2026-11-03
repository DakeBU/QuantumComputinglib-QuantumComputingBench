"""Shared cohort readers; metadata consistency is not mathematical authentication."""
from copy import deepcopy
from pathlib import Path

from qcb_core import digest, read_json
from qcb_evaluation_registry import _source_lineage
from qcb_reference_receipt import validate_course_receipt

SOURCE_FIELDS = ("question", "reference_answer", "assumptions", "conventions")


def source_semantics(item):
    """Source mathematics only: omit prior reviews, evidence and author labels."""
    return {k: deepcopy(item[k]) for k in SOURCE_FIELDS}


def _canonical_items():
    from qcb_curriculum import load_catalog
    return load_catalog()[1]


def bind_review_input(fixture, evidence_dir, cases, *, require_sanitized=False):
    """Bind the actual source/decoder payload read by a source-aware reviewer.

    Rehashing a report cannot substitute a different source question, ambient
    context or reconstruction while retaining the original labelled item hash.
    The source item hash is independently checked by load_candidates.
    """
    try:
        _bind_review_input(Path(fixture), Path(evidence_dir), cases, require_sanitized)
    except (KeyError, TypeError, AttributeError, IndexError, StopIteration) as error:
        raise ValueError("malformed source-aware comparison input") from error


def _bind_review_input(fixture, evidence_dir, cases, require_sanitized):
    comparison = read_json(evidence_dir / "comparison.json")
    inputs = read_json(evidence_dir / "comparison-input.json")
    sanitized = inputs.get("schema_version") == "qcb.course_semantic_comparison_input.v2"
    if (inputs.get("schema_version") not in {"qcb.course_semantic_comparison_input.v1", "qcb.course_semantic_comparison_input.v2"}
            or require_sanitized and not sanitized
            or comparison.get("comparison_input_digest") != digest(inputs)
            or inputs.get("candidate_batch_digest") != digest(read_json(fixture))
            or any(inputs.get(k) != comparison.get(k) for k in ("candidate_batch_digest", "packet_digests", "decoder_digests"))):
        raise ValueError("source-aware review must bind its actual comparison input")
    rows = inputs.get("views")
    expected = {c["task"]["core_id"]: c for c in cases}
    if (not expected or len(expected) != len(cases) or not isinstance(rows, list) or len(rows) != len(expected)
            or {r["core_id"] for r in rows} != set(expected)):
        raise ValueError("source-aware input must cover the exact cohort once")
    canonical = _canonical_items() if sanitized else None
    if sanitized and set(inputs) != {"schema_version", "candidate_batch_digest", "packet_digests", "decoder_digests", "views"}:
        raise ValueError("sanitized review input cannot carry extra metadata")
    contexts, decoders = {}, {}
    for case in cases:
        group = case["semantic_evidence"]["group"]
        if group not in contexts:
            # Group grammar/cardinality has already been checked by the caller's
            # load_candidates. This routine is not an untrusted path selector.
            contexts[group] = read_json(evidence_dir / (group + "-decoder-input.json"))
            decoders[group] = read_json(evidence_dir / (group + "-decoder.json"))
    for row in rows:
        case = expected[row["core_id"]]
        group, anonymous = (case["semantic_evidence"][k] for k in ("group", "anonymous_id"))
        context, decoder = contexts[group], decoders[group]
        formal_view = next(v for v in context["views"] if v["anonymous_id"] == anonymous)
        reconstruction = next(v for v in decoder["views"] if v["anonymous_id"] == anonymous)
        if sanitized:
            fields = {"core_id", "task_hash", "source_item_digest", "source_semantics", "formal_context_digest",
                      "formal_view", "ambient_context", "source_blind_decode", "retrieval_interfaces"}
            if (set(row) != fields or row["source_semantics"] != source_semantics(canonical[row["core_id"]])
                    or digest(canonical[row["core_id"]]) != case["source_item_digest"]
                    or row["retrieval_interfaces"] != case["task"]["interfaces"]):
                raise ValueError("sanitized source/retrieval payload differs from the actual canonical item")
        elif digest(row["source_item"]) != case["source_item_digest"]:
            raise ValueError("source-aware review input substituted a source payload")
        if (row["source_item_digest"] != case["source_item_digest"]
                or row["task_hash"] != digest(case["task"])
                or row["formal_context_digest"] != digest(formal_view["formal_context"])
                or row["formal_view"] != formal_view
                or row["ambient_context"] != {k: v for k, v in context.items() if k != "views"}
                or row["source_blind_decode"] != reconstruction):
            raise ValueError("source-aware review input substituted a source, formal or decoded payload")


def qualify_candidate_batch(cases, identity, receipt_path, profile, expected_pipeline_paths):
    """Read an exact evaluator-selected cohort; no Lean execution here."""
    report = read_json(receipt_path)
    validate_course_receipt(report, cases, identity, expected_pipeline_paths)
    if report.get("authored_reference_profile") != profile:
        raise ValueError("cohort requires its exact disclosed authored-only runtime profile")
    lineage = _source_lineage(report["tested_code_commit"], report["pipeline_source_hashes_lf"])
    views = {}
    for case in cases:
        task = case["task"]
        entry = {"view_id": case["view_id"], "task_hash": digest(task),
                 "allowed_modes": ["root_only", "proof_dag"], "allowed_exposures": ["closed_book", "approved_interface"],
                 **{k: task[k] for k in ("core_id", "contract_hash", "family", "split", "snapshot_id")}}
        views[case["view_id"]] = {"entry": entry, "task": task, "registry_digest": identity["fixture_digest"], "reference_lineage": lineage}
    return views, {"qualified_course_companions": len(views), "new_mathematical_cores": 0,
                   "new_canonical_formal_admissions": 0, "model_performance_measured": False,
                   "authored_reference_profile": deepcopy(profile), "reference_lineage": lineage}
