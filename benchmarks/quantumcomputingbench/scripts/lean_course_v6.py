#!/usr/bin/env python3
"""Cumulative sixth Lean course with linear/circuit training companions."""
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))

import lean_course as driver
import lean_course_v5 as previous
from qcb_core import read_json
from qcb_course_linear_circuit import PLAN, PROFILE, candidates, pipeline_identity, qualified
from qcb_lean_course import coverage


def load_course():
    _, earlier, _, _, old_report = previous.load_course()
    additional, status, catalog, graph = qualified()
    if earlier.keys() & additional.keys():
        raise ValueError("linear/circuit companions would replace an existing course view")
    views = {**earlier, **additional}
    plan = read_json(PLAN)
    report = coverage(plan, views, catalog, graph)
    report["reference_qualification"] = {
        "previous_course": old_report["reference_qualification"], "linear_circuit": status,
    }
    return plan, views, catalog, graph, report


if __name__ == "__main__":
    raise SystemExit(driver.main(course_loader=load_course, source_loader=candidates,
                                 pipeline_loader=pipeline_identity, reference_profile=PROFILE))
