"""Offline operator-profile preparation; no adapter import or model discovery."""
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator
from qcb_core import digest, read_json
from qcb_model_loop import validate_config

B = Path(__file__).resolve().parents[1]
SCHEMA = B / "schemas/operator-run-config-v1.schema.json"
TEMPLATE = B / "configs/agentic-operator.template.json"
MAX_PROFILE_BYTES = 65536


def profile_schema():
    schema = read_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return schema


def profile_template(*, purpose="formal_proof", mode="proof_dag", exposure=None):
    if purpose not in {"formal_proof", "explanation_only"} or mode not in {"root_only", "proof_dag"}:
        raise ValueError("unsupported profile condition")
    exposure = exposure or ("closed_book" if purpose == "explanation_only" else "approved_interface")
    if exposure not in {"closed_book", "approved_interface"} or purpose == "explanation_only" and exposure != "closed_book":
        raise ValueError("explanation-only profiles require closed-book exposure")
    template = deepcopy(read_json(TEMPLATE))
    template["condition"] = {"purpose": purpose, "mode": mode, "exposure": exposure}
    return template


def validate_operator_profile(config):
    # Keep diagnostic values out of errors: accidental credential fields are
    # rejected by the closed schema, not echoed back into a public log.
    error = next(Draft202012Validator(profile_schema()).iter_errors(config), None)
    if error is not None:
        pointer = "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in error.absolute_path)
        raise ValueError("operator profile schema error at " + pointer + " (" + str(error.validator) + ")")
    # Cross-field ceilings, strict Python numeric types and finite values are
    # runtime contracts; a JSON Schema pass alone is not a usable run profile.
    return validate_config(config)


def read_operator_profile(path):
    path = Path(path)
    if path.stat().st_size > MAX_PROFILE_BYTES:
        raise ValueError("operator profile exceeds the 64 KiB input ceiling")
    return validate_operator_profile(read_json(path))


def validation_summary(config):
    config = validate_operator_profile(config)
    return {"schema_version": "qcb.operator_profile_validation.v1", "valid": True,
            "config_digest": digest(config), "model": config["model"], "condition": config["condition"],
            "validation_scope": "configuration structure and budgets only; no endpoint identity attestation",
            "adapter_imported": False, "model_calls": 0, "candidate_execution_enabled": False}
