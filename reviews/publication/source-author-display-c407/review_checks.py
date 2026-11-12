"""Bounded independent checks for the C407 display-only patch.

Runtime repository/scratch locations are supplied by the caller, never stored.
This script performs only read-only Git object access and focused mocked tests.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


BASE = "37ebfef80e0043ff96b54796a6a8fe747f983644"
PATCH_FILES = (
    "website/scripts/research_atlas.py",
    "website/scripts/check_deployed_research.py",
    "website/scripts/test_research_atlas.py",
    "website/scripts/test_deployed_research.py",
)
CONTROLS = (
    "scripts/sanitize-blueprint-paths.py",
    "website/research/sources.json",
    "website/research/atlas.json",
    "website/research/state-preparation-wiki.json",
    "website/research/publications.json",
    "website/scripts/proof_inputs.py",
    "website/scripts/research_browser_contract.py",
    "website/scripts/check_research_publications.py",
    "website/scripts/build_site.py",
    "scripts/build-all.sh",
)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def lf(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n")


def definitions(value: bytes) -> dict[str, str]:
    return {
        item.name: ast.dump(item, include_attributes=False)
        for item in ast.parse(value.decode("utf-8")).body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--scratch", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    scratch = args.scratch.resolve()
    expected_parent = Path(__file__).resolve().parent
    if not scratch.is_relative_to(expected_parent):
        raise ValueError("scratch must remain inside this review artifact directory")
    scratch.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(scratch)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repository))

    def git(*arguments: str) -> bytes:
        return subprocess.check_output(
            ["git", "--git-dir=" + str(repository / ".git"), *arguments]
        )

    if git("rev-parse", "--verify", "HEAD").decode().strip() != BASE:
        raise ValueError("HEAD changed from the independently resolved review base")
    before = {name: (repository / name).read_bytes() for name in PATCH_FILES + CONTROLS}
    baseline = {name: git("show", BASE + ":" + name) for name in PATCH_FILES + CONTROLS}
    control_results = {name: lf(before[name]) == lf(baseline[name]) for name in CONTROLS}
    if not all(control_results.values()):
        raise AssertionError("a scoped control differs beyond checkout newline spelling")

    unchanged_definitions = {}
    for name, allowed in (
        (PATCH_FILES[0], {"publish", "check_published"}),
        (PATCH_FILES[1], {"check"}),
    ):
        old, new = definitions(baseline[name]), definitions(before[name])
        actual_changed = {key for key in old if new.get(key) != old[key]}
        if actual_changed != allowed:
            raise AssertionError("runtime definition changes exceed the reviewed patch")
        unchanged_definitions[name] = sorted(set(old) - allowed)

    from website.scripts import research_atlas as atlas

    canonical = atlas.load_catalog()
    canonical_snapshot = json.dumps(canonical, sort_keys=True)
    source_digest = atlas.source_digest()
    projected = atlas.public_catalog(canonical)
    expected_ids = {
        "aspbe-local-exact-primitives-controlled-rotations-finite-cubic",
        "aspbe-local-stored-rectangular-elimination-v1",
        "aspbe-local-retrospective-sequential-primitive-assembly-c48",
    }
    changed_ids = set()
    for original, displayed in zip(canonical["sources"]["sources"], projected["sources"]["sources"]):
        if original != displayed:
            changed_ids.add(original["id"])
            assert {k: v for k, v in original.items() if k != "authors"} == {
                k: v for k, v in displayed.items() if k != "authors"
            }
            assert displayed["authors"].replace("agent-task:", "/") == original["authors"]
    assert changed_ids == expected_ids
    assert projected["atlas"] == canonical["atlas"]
    assert projected["wiki"] == canonical["wiki"]
    assert json.dumps(canonical, sort_keys=True) == canonical_snapshot
    assert atlas.source_digest() == source_digest

    suite = unittest.defaultTestLoader.loadTestsFromNames([
        "website.scripts.test_research_atlas",
        "website.scripts.test_deployed_research",
    ])
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
    after = {name: (repository / name).read_bytes() for name in PATCH_FILES + CONTROLS}
    assert before == after, "focused checks changed reviewed source/control bytes"
    observation = {
        "review_base": BASE,
        "python_version": sys.version.split()[0],
        "focused_tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "all_source_and_control_bytes_unchanged_by_test_run": before == after,
        "all_control_files_equal_baseline_after_CRLF_to_LF": all(control_results.values()),
        "unchanged_existing_runtime_definitions": unchanged_definitions,
        "only_three_exact_author_records_changed": sorted(changed_ids),
        "canonical_source_digest_unchanged": source_digest == atlas.source_digest(),
        "input_pins": [
            {
                "artifact": name,
                "sha256": digest(before[name]),
                "byte_length": len(before[name]),
                "baseline_sha256": digest(baseline[name]),
                "baseline_byte_length": len(baseline[name]),
                "equal_after_CRLF_to_LF": lf(before[name]) == lf(baseline[name]),
            }
            for name in PATCH_FILES + CONTROLS
        ],
    }
    print(json.dumps(observation, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
