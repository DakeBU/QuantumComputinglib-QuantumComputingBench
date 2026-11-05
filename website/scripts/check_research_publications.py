#!/usr/bin/env python3
"""Fail closed for changed production modules lacking a reviewed publication packet.

This is an evidence-integrity checker, not a natural-language equivalence prover
or a detector of fabricated human identities. Existing Lean/trust gates remain
mandatory. An unchanged unregistered module keeps its historical audit debt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path("website/research/publications.json")
CATEGORIES = {"same", "source-implicit", "mathematically-necessary", "API-limitation", "generalization", "unresolved"}
CLASSES = {"add-node", "shortcut", "reorganisation", "bridge"}


def local_file(root: Path, name: str) -> Path:
    path = PurePosixPath(name)
    if path.is_absolute() or PureWindowsPath(name).is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"non-portable evidence path: {name}")
    full = root / path
    if not full.resolve().is_relative_to(root.resolve()) or not full.is_file():
        raise ValueError(f"missing evidence file: {name}")
    return full


def load(root: Path, name: str) -> Any:
    return json.loads(local_file(root, name).read_text(encoding="utf-8"))


def changed_modules(root: Path, base: str) -> list[str]:
    check = subprocess.run(["git", "rev-parse", "--verify", base + "^{commit}"], cwd=root, text=True, capture_output=True)
    if check.returncode:
        raise ValueError(f"unresolvable diff base: {base}")
    run = subprocess.run(["git", "diff", "--name-only", base, "--", "QuantumBlockEncoding"], cwd=root, text=True, capture_output=True)
    if run.returncode:
        raise ValueError("cannot inventory changed production modules")
    return sorted(name for name in run.stdout.splitlines() if name.endswith(".lean"))


def binding_digest(root: Path, record: dict[str, Any]) -> str:
    keys = ("module", "source_id", "source_statement", "source_anchor", "lesson_path", "declarations", "obligation_map", "assumption_deltas", "graph_contribution", "formalizer", "residual_boundary")
    payload = {key: record.get(key) for key in keys}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    for name in (record["module"], record["lesson_path"], "lean-toolchain", "lake-manifest.json"):
        digest.update(name.encode())
        digest.update(local_file(root, name).read_bytes())
    # Bind local ambient definitions too: imports/private helpers in another
    # production module must not leave an old semantic review apparently fresh.
    for directory in ("QuantumBlockEncoding", "ABEISTests"):
        for path in sorted((root / directory).rglob("*.lean")):
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(path.read_bytes())
    sources = load(root, "website/research/sources.json")["sources"]
    source = next((s for s in sources if s["id"] == record["source_id"]), None)
    if source is None:
        raise ValueError(f"unknown publication source {record['source_id']}")
    if source["status"] == "primary-source-unavailable":
        raise ValueError("an unavailable source cannot support source assimilation")
    digest.update(json.dumps(source, sort_keys=True, ensure_ascii=False).encode())
    return digest.hexdigest()


def validate_record(root: Path, record: dict[str, Any], inventory: dict[str, dict[str, Any]]) -> None:
    required = ("module", "source_id", "source_statement", "source_anchor", "lesson_path", "declarations", "obligation_map", "assumption_deltas", "graph_contribution", "formalizer", "residual_boundary", "binding_sha256", "decoder_evidence", "reviewer_evidence")
    for key in required:
        if key not in record or record[key] in (None, ""):
            raise ValueError(f"publication lacks {key}: {record.get('module')}")
    actual = {name for name, item in inventory.items() if item.get("source") == record["module"]}
    declared = record["declarations"]
    if not actual:
        raise ValueError("changed module has no inventoried public declarations; unsupported syntax/module requires explicit inventory support, not silent exemption")
    if len(declared) != len(set(declared)) or set(declared) != actual:
        raise ValueError("publication target set must equal the whole changed-module inventory")
    if any(inventory[name].get("openProof") or inventory[name].get("experimental") for name in declared):
        raise ValueError("unfinished/experimental source cannot enter the source-assimilated lane")
    if not record["obligation_map"] or not record["assumption_deltas"]:
        raise ValueError("explicit source obligations and assumption comparison are required")
    mapped: set[str] = set()
    for item in record["obligation_map"]:
        if item.get("kind") not in {"proof-edge", "prerequisite"} or not item.get("source_obligation"):
            raise ValueError("proof-edge and prerequisite obligations must be distinguished")
        for name in item.get("declarations", []):
            if name not in actual:
                raise ValueError("obligation binds an undeclared theorem")
            mapped.add(name)
    if mapped != actual:
        raise ValueError("not every changed declaration has a source obligation or explicit prerequisite role")
    for delta in record["assumption_deltas"]:
        if delta.get("classification") not in CATEGORIES or not all(delta.get(key) for key in ("source", "formal", "explanation")):
            raise ValueError("invalid assumption-delta ledger")
        if delta["classification"] == "unresolved":
            raise ValueError("unresolved source assumptions cannot be published as assimilated")
    graph = record["graph_contribution"]
    for key in ("baseline", "classes", "node_ids", "views", "preserved_contract", "remaining_boundary"):
        if not graph.get(key):
            raise ValueError(f"graph contribution lacks {key}")
    if not set(graph["classes"]).issubset(CLASSES):
        raise ValueError("invalid graph contribution classes")
    if not {"declaration:" + name for name in actual}.issubset(graph["node_ids"]):
        raise ValueError("graph contribution omits changed Lean identities")
    expected = binding_digest(root, record)
    if record["binding_sha256"] != expected:
        raise ValueError("publication binding is stale")
    decoder = load(root, record["decoder_evidence"])
    reviewer = load(root, record["reviewer_evidence"])
    for evidence, role in ((decoder, "decoder"), (reviewer, "reviewer")):
        if evidence.get("role") != role or evidence.get("binding_sha256") != expected:
            raise ValueError("independent evidence has the wrong role or stale context")
        if not evidence.get("identity") or not evidence.get("run_id") or not evidence.get("packet_path"):
            raise ValueError("independent evidence lacks identity/run/packet")
        packet = local_file(root, evidence["packet_path"])
        if hashlib.sha256(packet.read_bytes()).hexdigest() != evidence.get("packet_sha256"):
            raise ValueError("independent evidence packet has changed")
        if not evidence.get("artifact_path"):
            raise ValueError("review result artifact missing")
        artifact = local_file(root, evidence["artifact_path"])
        if hashlib.sha256(artifact.read_bytes()).hexdigest() != evidence.get("artifact_sha256"):
            raise ValueError("independent result artifact has changed")
    if len({record["formalizer"], decoder["identity"], reviewer["identity"]}) != 3:
        raise ValueError("formalizer, decoder and reviewer must be distinct")
    decoder_hash = hashlib.sha256(local_file(root, record["decoder_evidence"]).read_bytes()).hexdigest()
    if reviewer.get("decoder_evidence_sha256") != decoder_hash:
        raise ValueError("reviewer is not bound to the exact decoder result")
    if decoder.get("source_blind") is not True or not decoder.get("reconstruction"):
        raise ValueError("decoder must retain a source-blind reconstruction")
    if reviewer.get("anti_anchored") is not True or reviewer.get("verdict") != "accepted":
        raise ValueError("source assimilation needs an accepted anti-anchored review")
    slots = {"target", "normalization", "registers", "oracles", "ancillas_phases", "error_success", "resources"}
    if set(reviewer.get("semantic_slots", {})) != slots or not all(reviewer["semantic_slots"].values()):
        raise ValueError("review must compare all quantum semantic slots")
    if record.get("repair"):
        repair = record["repair"]
        local_file(root, repair["proposal_path"])
        review = load(root, repair["independent_review"])
        proposal_hash = hashlib.sha256(local_file(root, repair["proposal_path"]).read_bytes()).hexdigest()
        if review.get("proposal_sha256") != proposal_hash or review.get("verdict") != "accepted" or review.get("identity") == record["formalizer"] or not review.get("minimality_evidence"):
            raise ValueError("repair needs a separate exact-proposal independent minimality review")


def check(root: Path, base: str, inventory_path: Path | None = None) -> dict[str, Any]:
    registry = load(root, REGISTRY.as_posix())
    if registry.get("schema_version") != 1:
        raise ValueError("unsupported publication registry")
    # Direct script invocation starts with website/scripts on sys.path, not
    # the repository root. Use this script's trusted root, never --root input.
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from website.scripts import check_toolchain_maintenance as maintenance
    by_module, by_maintenance = maintenance.partition_records(registry)
    changed = changed_modules(root, base)
    missing = [name for name in changed if name not in by_module and name not in by_maintenance]
    if missing:
        raise ValueError("changed production modules lack reviewed publication records: " + ", ".join(missing))
    if changed:
        source = inventory_path or root / "web/library/declarations.json"
        if not source.is_file():
            raise ValueError("generate the current declaration inventory before admission")
        inventory = {item["fullName"]: item for item in json.loads(source.read_text(encoding="utf-8"))["declarations"]}
        for module in changed:
            if module in by_module:
                validate_record(root, by_module[module], inventory)
            else:
                maintenance.validate_record(root, by_maintenance[module], inventory)
    return {"base": base, "changed_modules": changed, "accepted_module_packets": len(changed),
            "source_assimilated_module_packets": sum(m in by_module for m in changed),
            "compatibility_maintenance_module_packets": sum(m in by_maintenance for m in changed),
            "unchanged_legacy_policy": "not retroactively source-reviewed", "natural_language_equivalence_proved": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.root.resolve(), args.base, args.inventory), indent=2))
    except (ValueError, KeyError, OSError) as error:
        raise SystemExit("publication gate failed: " + str(error)) from error


if __name__ == "__main__":
    main()
