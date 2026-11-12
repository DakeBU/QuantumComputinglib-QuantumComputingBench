"""Source-bound RobinMatrix name/axiom observation, NOT a semantic proof review.

Run only after the existing real Lean 4.33 full-library + Tests build.
No compiler invocation occurs on import. All subprocess output is retained verbatim.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

MODULE = "QuantumBlockEncoding/RobinMatrix.lean"
MODULE_NAME = "QuantumBlockEncoding.RobinMatrix"
EXPECTED_SOURCE_SHA256 = "1cca5119ac056fe041b25c529909b9fb6c3e4995e04ebde2f69e83fce47a0835"
CATALOG = "web/library/declarations.json"
CONFIGS = ("lean-toolchain", "lakefile.lean", "lake-manifest.json")
OLEAN = ".lake/build/lib/lean/QuantumBlockEncoding/RobinMatrix.olean"
ORDINARY = frozenset(("propext", "Classical.choice", "Quot.sound"))
LEGACY_NATIVE = frozenset(("Lean.ofReduceBool", "Lean.ofReduceNat", "Lean.trustCompiler"))
IDENT = r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*"
NAME = re.compile(IDENT)
# Lean's observed generated/inaccessible names can retain a terminal dagger.
# Preserve it verbatim; it is not an axiom approval or a name normalization.
AXIOM_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*(?:✝)?")


class AuditError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return {"sha256": digest(data), "bytes": len(data)}


def local(root, relative):
    """Reject traversal, absolute names and symlink escapes, on both host OSes."""
    require(isinstance(relative, str) and relative and "\\" not in relative,
            "path must be a slash-separated relative name")
    parts = relative.split("/")
    require(all(x not in ("", ".", "..") and ":" not in x for x in parts), "unsafe relative path")
    path = root.joinpath(*parts).resolve()
    require(path.is_relative_to(root), "path escapes repository")
    return path


def write_json(path, value):
    temporary = path.with_name(path.name + ".pending")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def invalidate(out):
    """Never leave a previous green as the active result of a failed new attempt."""
    out.mkdir(parents=True, exist_ok=True)
    report = out / "report.json"
    require(not report.is_symlink(), "active report cannot be a symlink")
    if report.exists():
        previous = report.read_bytes()
        history = out / "history"
        history.mkdir(exist_ok=True)
        archived = history / ("report-" + digest(previous) + ".json")
        if archived.exists():
            require(archived.read_bytes() == previous, "historical report collision")
        else:
            with archived.open("xb") as stream:
                stream.write(previous)
        report.unlink()
    write_json(report, {"success": False, "status": "invalidated-before-new-observation"})


def inventory(raw_catalog):
    rows = json.loads(raw_catalog)["declarations"]
    selected = [r for r in rows if r.get("source") == MODULE]
    require(len(selected) == 395, "expected exactly 395 RobinMatrix catalog rows")
    names = []
    for row in selected:
        name = row.get("fullName")
        require(isinstance(name, str) and NAME.fullmatch(name), "unsupported catalog name syntax")
        require(row.get("experimental") is True and row.get("openProof") is False,
                "expected experimental=true and openProof=false on every selected row")
        names.append(name)
    # Python equality is ordinal/case-sensitive. Never casefold Lean identifiers.
    duplicates = sorted(n for n, count in Counter(names).items() if count > 1)
    require(not duplicates, "exact duplicate catalog names: " + ", ".join(duplicates))
    return [{"fullName": r["fullName"], "kind": r.get("kind"), "line": r.get("line")}
            for r in selected]


def source_for(rows, nonce):
    lines = ["import " + MODULE_NAME, "set_option pp.fullNames true", ""]
    for i, row in enumerate(rows):
        stem = f"C368|{nonce}|{i:04d}|"
        lines.extend((f'#eval IO.println "{stem}CHECK"', "#check " + row["fullName"],
                      f'#eval IO.println "{stem}AXIOMS"', "#print axioms " + row["fullName"],
                      f'#eval IO.println "{stem}END"'))
    return ("\n".join(lines) + "\n").encode("utf-8")


def native_marker(name):
    # Native.lean creates auxiliary names containing _native.<tactic>.ax.
    # This is a disclosed name-pattern classifier, not an axiom provenance proof.
    return name in LEGACY_NATIVE or bool(re.search(r"(?:^|\.)_native\..*\.ax(?:[._]|$)", name))


def exact_signature(signature, name):
    """Recognize #check's exact name and balanced binder prefix, not Lean types.

    Actual Lean may print parameters before the result colon. Keep the original
    full signature; reject malformed/unknown prefixes instead of guessing types.
    """
    head = re.match(r"\A" + re.escape(name) + r"(?:\.\{[^}]*\})?(?=\s|:)", signature)
    if head is None:
        return False
    rest = signature[head.end():].lstrip()
    pairs = {"(": ")", "{": "}", "[": "]", "⦃": "⦄"}
    while rest and rest[0] in pairs:
        stack, quoted, escaped = [], False, False
        for i, char in enumerate(rest):
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char in pairs:
                stack.append(pairs[char])
            elif char in pairs.values():
                if not stack or char != stack.pop():
                    return False
                if not stack:
                    rest = rest[i + 1:].lstrip()
                    break
        else:
            return False
    return rest.startswith(":") and bool(rest[1:].strip())


def parse_observations(raw, rows, nonce):
    text = raw.decode("utf-8", errors="strict").replace("\r\n", "\n")
    cursor = 0
    observations = []
    for i, row in enumerate(rows):
        name = row["fullName"]
        sections = []
        for marker in ("CHECK", "AXIOMS", "END"):
            token = f"C368|{nonce}|{i:04d}|{marker}"
            match = re.search(r"(?m)^" + re.escape(token) + r"$", text[cursor:])
            require(match is not None, f"missing ordered {marker} marker at row {i}")
            sections.append(text[cursor:cursor + match.start()].strip())
            cursor += match.end()
        # Strict command-order grammar; unexpected prelude/warnings fail closed.
        require(not sections[0], f"unexpected text before CHECK at row {i}")
        signature, axioms_text = sections[1:]
        require(exact_signature(signature, name),
                f"missing exact case-sensitive #check signature at row {i}")
        none = "'" + name + "' does not depend on any axioms"
        if axioms_text == none:
            axioms = []
        else:
            match = re.fullmatch(re.escape("'" + name + "' depends on axioms: ")
                                 + r"\[([^\[\]]*)\]", axioms_text, re.DOTALL)
            require(match is not None, f"missing exact axiom result at row {i}")
            axioms = [x.strip() for x in match.group(1).split(",")]
            require(all(AXIOM_NAME.fullmatch(x) for x in axioms) and len(set(axioms)) == len(axioms),
                    f"unsupported or duplicate axiom syntax at row {i}")
        additional = [a for a in axioms if a not in ORDINARY]
        native = [a for a in additional if native_marker(a)]
        observations.append(dict(row=row, signature=signature, axioms=axioms,
                                 additional_axioms=additional, native_name_markers=native,
                                 classification=("additional-with-native-name-marker" if native else
                                                 "additional" if additional else
                                                 "ordinary-only" if axioms else "no-axioms")))
    require(not text[cursor:].strip(), "unexpected trailing compiler output")
    return observations


def audit(repo, out_relative="_out/robin-export-audit",
          full_build_relative="_out/installed-lean433-public/result.json", timeout=180):
    root = Path(repo).resolve()
    require(out_relative.startswith("_out/"), "output must be below repository _out/")
    out = local(root, out_relative)
    invalidate(out)  # Before catalog/source/receipt checks or subprocess calls.
    record = {"success": False, "status": "started", "commands": []}
    attempt = out / ("run-" + uuid.uuid4().hex)
    attempt.mkdir()
    # One writer per out directory. A stale lock is a failure, never reuse a green.
    lock = out / "audit.lock"
    locked = False
    try:
        with lock.open("x", encoding="ascii") as stream:
            stream.write(attempt.name)
        locked = True
        require(isinstance(timeout, int) and 1 <= timeout <= 3600, "invalid finite timeout")
        tool_before = pin(Path(__file__))
        raw_catalog = local(root, CATALOG).read_bytes()
        rows = inventory(raw_catalog)
        required = (MODULE, CATALOG, *CONFIGS, OLEAN, full_build_relative)
        before = {p: pin(local(root, p)) for p in required}
        require(before[CATALOG] == dict(sha256=digest(raw_catalog), bytes=len(raw_catalog)),
                "catalog changed while constructing inventory")
        require(before[MODULE]["sha256"] == EXPECTED_SOURCE_SHA256, "RobinMatrix source pin mismatch")
        require(local(root, "lean-toolchain").read_text(encoding="utf-8").strip()
                == "leanprover/lean4:v4.33.0", "wrong toolchain")
        receipt = json.loads(local(root, full_build_relative).read_bytes())
        require(receipt.get("full_Lean_Tests_success") is True
                and receipt.get("input_bytes_unchanged") is True, "no successful real full-build receipt")
        require("version 4.33.0" in receipt.get("Lean_version", ""), "full-build version mismatch")
        inputs = receipt.get("inputs")
        require(isinstance(inputs, dict) and all(p in inputs for p in (MODULE, *CONFIGS)),
                "full-build receipt lacks required source/config bindings")
        for p, sha in inputs.items():
            require(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha), "bad receipt digest")
            require(pin(local(root, p))["sha256"] == sha, "stale full-build input: " + p)

        def command(label, args):
            stdout = attempt / (label + ".stdout")
            stderr = attempt / (label + ".stderr")
            entry = dict(command=args, cwd="repository-root", timeout_seconds=timeout,
                         stdout=stdout.relative_to(out).as_posix(), stderr=stderr.relative_to(out).as_posix())
            record["commands"].append(entry)
            result = None
            try:
                result = subprocess.run(args, cwd=root, capture_output=True, timeout=timeout, check=False)
                require(isinstance(result, subprocess.CompletedProcess), "no actual subprocess result")
                require(isinstance(result.stdout, bytes) and isinstance(result.stderr, bytes),
                        "subprocess did not return captured bytes")
                stdout.write_bytes(result.stdout)
                stderr.write_bytes(result.stderr)
                entry["exit_code"] = result.returncode
            except subprocess.TimeoutExpired as error:
                stdout.write_bytes(error.stdout or b"")
                stderr.write_bytes(error.stderr or b"")
                entry["timeout"] = True
                raise AuditError("command timed out: " + label) from error
            finally:
                for key, path in (("stdout_pin", stdout), ("stderr_pin", stderr)):
                    if path.exists():
                        entry[key] = pin(path)
            require(result.returncode == 0, "command failed: " + label)
            return result.stdout

        prefix = Path(command("01-prefix", ["lake", "env", "lean", "--print-prefix"])
                      .decode("utf-8").strip())
        require(prefix.is_absolute(), "Lean prefix is not absolute")
        candidates = [p for p in (prefix / "bin/lean", prefix / "bin/lean.exe") if p.is_file()]
        require(len(candidates) == 1, "ambiguous or missing actual Lean binary")
        binary = candidates[0]
        binary_before = pin(binary)
        require(binary_before["sha256"] == receipt.get("Lean_binary_sha256"), "Lean binary pin mismatch")
        version = command("02-version", ["lake", "env", "lean", "--version"]).decode("utf-8").strip()
        require(version == receipt["Lean_version"], "actual Lean version differs from full build")
        nonce = attempt.name.removeprefix("run-")
        probe = attempt / "RobinExportProbe.lean"
        probe.write_bytes(source_for(rows, nonce))
        probe_before = pin(probe)
        probe_relative = probe.relative_to(root).as_posix()
        deps = command("03-deps", ["lake", "env", "lean", "--deps", probe_relative]).decode("utf-8")
        resolved = []
        for line in deps.splitlines():
            if line.strip():
                candidate = Path(line.strip())
                resolved.append((candidate if candidate.is_absolute() else root / candidate).resolve())
        expected = local(root, OLEAN)
        robin_deps = [p for p in resolved if p.name == "RobinMatrix.olean"]
        require(robin_deps == [expected], "--deps did not select the exact production RobinMatrix olean")
        raw = command("04-observation", ["lake", "env", "lean", "-M1536", "-j1", probe_relative])
        observations = parse_observations(raw, rows, nonce)
        for p, original in before.items():
            require(pin(local(root, p)) == original, "input changed during audit: " + p)
        for p, sha in inputs.items():
            require(pin(local(root, p))["sha256"] == sha, "full-build input changed during audit: " + p)
        require(pin(binary) == binary_before and pin(probe) == probe_before
                and pin(Path(__file__)) == tool_before,
                "binary, tool or generated probe changed during audit")
        record.update(success=True, status="observed-name-and-axiom-coverage-only", inputs=before,
                      tool_pin=tool_before, lean_binary_pin=binary_before, version=version,
                      generated_probe=dict(path=probe_relative, **probe_before),
                      resolved_target=OLEAN, catalog_row_count=len(rows),
                      case_sensitive_unique_names=len({r["fullName"] for r in rows}),
                      observations=observations, classification_counts=dict(Counter(
                          x["classification"] for x in observations)),
                      limits=["Catalog rows are not an exhaustive elaborated export inventory.",
                              "#check establishes name/type output, not per-declaration semantic review.",
                              "Additional/native axioms are disclosed, not rejected or approved by this tool.",
                              "Receipt is inherited evidence, not an independent rerun of the full build.",
                              "Direct --deps selection is not a clean transitive TCB reconstruction.",
                              "Source/olean hashes do not themselves prove source-to-binary correspondence."])
    except Exception as error:
        # Avoid publishing exception strings that may contain local paths. Full raw
        # compiler output remains in the private run directory, never truncated.
        record.update(success=False, status="failed", failure_class=type(error).__name__)
        if isinstance(error, AuditError):
            record["failure_reason"] = str(error)
    finally:
        if locked:
            lock.unlink()
        write_json(out / "report.json", record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--out", default="_out/robin-export-audit")
    parser.add_argument("--full-build-report", default="_out/installed-lean433-public/result.json")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    try:
        result = audit(args.repo, args.out, args.full_build_report, args.timeout)
    except (AuditError, OSError) as error:
        print("audit could not initialize safely: " + type(error).__name__, file=sys.stderr)
        return 1
    print(json.dumps({"success": result["success"], "status": result["status"]}))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
