"""Freeze the completed internal review, preserving raw failed evidence."""
import json
import re
import shutil
from pathlib import Path
from check_review import HERE, ROOT, C23, OUT, EXPECTED_MANIFEST, digest, label, clean

assert digest(C23 / "final-binding-manifest.json") == EXPECTED_MANIFEST
assert not (HERE / "final-binding-manifest.json").exists()
state = json.loads((OUT / "private-state.json").read_text(encoding="utf-8"))
for p, sha in state["pins"].items():
    assert digest(Path(p)) == sha, "Input drift: " + label(Path(p))
assert json.loads((HERE / "consumer-v2.json").read_text(encoding="utf-8"))["exit"] == 0
assert digest(HERE / "IndependentConsumer.lean") == "03f09860c34dcf1866117efed445a4e92e1fd6f3c2b010cbf749c8b368cf8c9f"

# Preserve the first failed consumer byte-for-byte (it was already LF/UTF-8).
failed = json.loads((HERE / "consumer-v1.json").read_text(encoding="utf-8"))
assert digest(HERE / ".cache/snapshots/consumer-v1.lean") == failed["source_sha256"]
# The first external-source snapshot used newline-normalizing text capture.
# Add a byte-exact backup from the still-unchanged, pre/post bound source.
original = ROOT / "experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualCoefficients.lean"
backup = HERE / ".cache/snapshots/source-ActualCoefficients-original-bytes.lean"
assert not backup.exists()
shutil.copy2(original, backup)
assert digest(backup) == json.loads((HERE / "source-ActualCoefficients.json").read_text(encoding="utf-8"))["source_sha256"]

public_backup = HERE / ".cache/public-before-final-sanitize"
public_backup.mkdir()
for receipt in sorted(HERE.glob("*.json")):
    record = json.loads(receipt.read_text(encoding="utf-8"))
    if "selected_direct_imports" not in record:
        continue
    shutil.copy2(receipt, public_backup / receipt.name)
    log = HERE / record["log"]
    shutil.copy2(log, public_backup / log.name)
    log.write_text(clean(log.read_text(encoding="utf-8")).replace("[workspace]", "."), encoding="utf-8", newline="\n")
    record["log_sha256"] = digest(log)
    raw = HERE / ".cache/raw" / log.name
    if raw.exists():
        record["private_raw_log_sha256"] = digest(raw)
    dep = HERE / (receipt.stem + ".deps.log")
    if dep.exists():
        shutil.copy2(dep, public_backup / dep.name)
        # Public dependency listings are serialized from the actual recorded
        # --deps selection; do not mislabel library caches as the toolchain.
        dep.write_text("Sanitized selected direct imports from " + receipt.name + "\n" +
                       "\n".join(d["path"] for d in record["selected_direct_imports"]) + "\n",
                       encoding="utf-8", newline="\n")
        record["public_dependency_listing_sha256"] = digest(dep)
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")

shutil.copy2(HERE / "consumer-v2.log", HERE / "axioms.log")
public = {p.relative_to(HERE).as_posix(): digest(p) for p in sorted(HERE.iterdir()) if p.is_file()}
for rel in public:
    content = (HERE / rel).read_text(encoding="utf-8")
    assert not re.search(r"\b[A-Za-z]:[\\/](?:Users|Program Files)|[\\/]Users[\\/](?:84771|HUAWEI)", content, re.IGNORECASE), rel
sources = {label(p): digest(p) for p in [C23 / "ChargedSourceCache.lean", C23 / "CacheConsumerChecks.lean",
          C23 / "final-binding-manifest.json", original, ROOT / "QuantumBlockEncoding/StoredGivens.lean",
          ROOT / "QuantumBlockEncoding/StoredHermiteCoefficients.lean", ROOT / "lean-toolchain", ROOT / "lake-manifest.json"]}
private_evidence = {p.relative_to(HERE).as_posix(): digest(p)
                    for directory in (HERE / ".cache/raw", HERE / ".cache/snapshots", public_backup)
                    for p in sorted(directory.rglob("*")) if p.is_file()}
final = {"status": "FROZEN_INTERNAL_REVIEW", "verdict": "ACCEPT_INTERNAL_BOUNDED_CONTRACT",
         "artifact_hashes": public, "stable_reviewed_sources": sources,
         "private_failure_and_raw_evidence_hashes": private_evidence,
         "consumer_olean_sha256": digest(OUT / "IndependentConsumer.olean"),
         "final_source_module_outputs": state["fresh_modules"],
         "sources_and_selected_imports_verified_at_freeze": len(state["pins"]),
         "author_manifest_unchanged": True, "actual_deps_selections_in_gate_receipts": True,
         "snapshot_note": "External failed-source byte backup reconstructed from unchanged pre/post-bound source; first consumer snapshot is byte-exact",
         "public_dependency_listing_note": "Sanitized serialization of actual --deps selections in receipts; raw prior public listings retained privately",
         "source_publication_or_main_gate": False, "scientific_ROOT": False,
         "full_repository_gate": False, "full_documentation_gate": False,
         "clean_transitive_rebuild": False, "finite_bit_GCD_bound": False}
(HERE / "final-binding-manifest.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"manifest_sha256": digest(HERE / "final-binding-manifest.json"),
                  "review_sha256": digest(HERE / "review.md"), "consumer_sha256": digest(HERE / "IndependentConsumer.lean"),
                  "axioms_sha256": digest(HERE / "axioms.log"), "status": final["status"]}))
