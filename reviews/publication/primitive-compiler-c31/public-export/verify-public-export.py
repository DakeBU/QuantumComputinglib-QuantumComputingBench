#!/usr/bin/env python3
"""Read-only privacy/integrity screen of the explicit public projection.

Safe original references must be accessible beside the export directory.
Withheld original handoff bytes are never read or claimed verified here.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def leaves(value, pointer="$"):
    if isinstance(value, str):
        yield pointer, value
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, pointer + "/" + str(index))
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, pointer + "/" + key)


PATTERNS = {
    "host-path": re.compile(r"(?i)(?<![\w])[a-z]:[\\/][^\s\"<>]*|(?:/Users/|/home/)[^/\s|()\[\]{}]+(?:/|$)|\\\\[A-Za-z0-9_.-]+\\[^\s]+"),
    "credential": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_|sk-(?:proj-)?)[A-Za-z0-9_-]{20,}|\bAKIA[A-Z0-9]{16}\b|(?i:bearer)\s+[A-Za-z0-9._-]{24,}|(?i:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"'][A-Za-z0-9+/=_-]{16,}[\"']"),
}


def scan_bytes(name, raw):
    text = raw.decode("utf-8")
    values = list(leaves(json.loads(text))) if name.endswith(".json") else [("$text", text)]
    findings = []
    for pointer, value in values:
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(value):
                captured = match.group().encode()
                findings.append({"kind": kind, "decoded_string_pointer": pointer,
                                 "decoded_start_character": match.start(), "decoded_end_character": match.end(),
                                 "matched_utf8_bytes": len(captured), "matched_sha256": sha(captured)})
    return findings


def verify(export):
    export = export.resolve()
    manifest_path = export / "public-allowlist.json"
    raw_manifest = manifest_path.read_bytes()
    manifest = json.loads(raw_manifest)
    assert not scan_bytes(manifest_path.name, raw_manifest), "Unsafe allowlist."
    assert manifest["unsafe_originals_not_exported"] == ["handoff.txt"]
    safe, derivatives = 0, 0
    records = []
    for rec in manifest["original_artifacts"]:
        if rec["kind"] == "EXACT_ORIGINAL_REFERENCE":
            assert rec["reference_path"] == "../" + rec["original_file"]
            path = export.parent / rec["original_file"]
            safe += 1
        else:
            assert rec["kind"] == "PATH_ONLY_DERIVATIVE" and rec["original_alias"] is False
            assert rec["original_file"] == "handoff.txt" and rec["public_file"] == "handoff.public.txt"
            path = export / rec["public_file"]
            receipt = json.loads((export / rec["receipt"]).read_bytes())
            assert receipt["original"]["sha256"] == rec["original_sha256"]
            assert receipt["derived"]["sha256"] == rec["sha256"]
            assert receipt["original"]["not_exported"] is True
            assert receipt["original"]["sha256"] != receipt["derived"]["sha256"]
            derivatives += 1
        raw = path.read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], rec["original_file"]
        assert not scan_bytes(path.name, raw), "Unsafe intended public file: " + path.name
        records.append({"public_file": rec.get("public_file", rec["original_file"]), "sha256": sha(raw)})
    for rec in manifest["new_public_artifacts"]:
        assert Path(rec["file"]).name == rec["file"]
        raw = (export / rec["file"]).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], rec["file"]
        assert not scan_bytes(rec["file"], raw), "Unsafe export artifact: " + rec["file"]
    assert safe == 22 and derivatives == 1
    return {"status": "PUBLICSAFE_AUTHOR_PROJECTION_SCREEN_PASS", "exact_safe_references": safe, "path_only_derivatives": derivatives,
            "decoded_JSON_string_leaf_scanning": True, "host_path_findings_in_public_content": 0, "credential_pattern_findings": 0,
            "public_allowlist_sha256": sha(raw_manifest), "public_paths_and_hashes": records,
            "withheld_private_original_bytes_read": False, "standalone_verification_of_private_originals": False,
            "original_bindings_modified": False, "mathematical_acceptance": False, "read_only": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.export), ensure_ascii=False, indent=2))
