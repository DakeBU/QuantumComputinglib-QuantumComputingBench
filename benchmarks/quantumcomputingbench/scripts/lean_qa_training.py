#!/usr/bin/env python3
"""Export the versioned complementary corpus for the sparse-address study."""
import argparse
import json
import sys
from pathlib import Path

import assessment
from qcb_assessment_training import core_bindings, exclusion_closure, training_fingerprint
from qcb_bench_runtime import build_registry
from qcb_core import digest, read_json
from qcb_course_hamiltonian import B, qualified, reference_records
from qcb_course_training import export_training

PROFILE = B / "tracks/lean/assessment-sparse-v1/training-profile.json"


def training_package():
    baseline = assessment._training()
    views, status, _, _ = qualified()
    qualification = {"suite_id": "qcb-lean-graph-course-hamiltonian-v1",
                     "registry_digest": digest({key: row["entry"] for key, row in views.items()})}
    new = export_training(views, qualification, reference_records())["examples"]
    bindings = core_bindings(build_registry())
    return baseline, new, bindings


def project(baseline, new, bindings, profile):
    if (profile["baseline_training_fingerprint"] != training_fingerprint(baseline)
            or profile["train_task_bindings_digest"] != digest(bindings)
            or profile["hamiltonian_examples_digest"] != digest(new)):
        raise ValueError("sparse training profile differs from its reviewed inputs")
    omitted = profile["excluded_core_ids"]
    if omitted != exclusion_closure(omitted, bindings):
        raise ValueError("a sparse holdout must omit every view of each linked core")
    excluded = set(omitted)
    language = [row for row in baseline["nl_and_semantic_examples"]
                if not excluded.intersection(bindings[row["task_id"]]["core_ids"])]
    lean = [row for row in baseline["lean_examples"] + new if row["core_id"] not in excluded]
    represented = {core for row in language for core in bindings[row["task_id"]]["core_ids"]}
    if (any(row["core_id"] not in represented for row in lean)
            or len({row["core_id"] for row in lean}) != len(lean)
            or any(row["split"] != "train" for row in language + lean)):
        raise ValueError("formal supervision must retain a unique existing train core")
    counts = {"nl_and_semantic_views": len(language), "lean_views": len(lean),
              "distinct_existing_cores": len(represented)}
    if counts != profile["counts"] or sorted(represented) != profile["retained_core_ids"]:
        raise ValueError("sparse profile counts or retained core IDs changed")
    result = {**baseline, "schema_version": "qcb.sparse_study_training_export.v1",
              "nl_and_semantic_examples": language, "lean_examples": lean, "counts": counts,
              "study_training_profile": profile, "profile_digest": digest(profile),
              "actual_model_exposure_authenticated": False}
    if training_fingerprint(result) != profile["projection_training_fingerprint"]:
        raise ValueError("sparse training records differ from the frozen projection")
    return result


def export():
    return project(*training_package(), read_json(PROFILE))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh training export output")
        package = export()
        assessment._write(args.output, package, private=False)
        print(json.dumps(package["counts"]))
        return 0
    except (KeyError, TypeError, ValueError, OSError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
