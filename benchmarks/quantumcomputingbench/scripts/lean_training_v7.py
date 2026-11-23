#!/usr/bin/env python3
"""Export cumulative v7 train references only, without training."""
import argparse
import json
import sys
from pathlib import Path

B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(B / "src"))
from qcb_core import write_json
from qcb_course_hamiltonian import reference_records as hamiltonian_records
from qcb_course_linear_circuit import reference_records as linear_circuit_records
from qcb_course_circuit_basics import reference_records as basics_records
from qcb_course_registry_v7 import load_course_registry
from qcb_course_training import export_training, reference_records as previous_records


def export():
    return _export_from_registry(*load_course_registry())


def _export_from_registry(views, qualification):
    """Use a registry already qualified in the current trusted process."""
    records = {}
    for loader in (previous_records, hamiltonian_records, linear_circuit_records, basics_records):
        additional = loader()
        if records.keys() & additional.keys():
            raise ValueError("v7 training sources would replace an earlier authored root")
        records.update(additional)
    return export_training(views, qualification, records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise FileExistsError("choose a fresh output; previous exports are preserved")
        result = export()
        write_json(args.output, result, immutable=True)
        print(json.dumps({"output": str(args.output), "distinct_train_cores": result["distinct_shared_cores"],
                          "training_launched": False}))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
