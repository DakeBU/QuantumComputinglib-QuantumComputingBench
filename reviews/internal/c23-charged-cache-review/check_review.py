"""Bounded independent C23 source replay; writes only this review directory."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
C23 = ROOT / "experiments/hermite-polynomial/precision/charged-coefficient-cache-c23"
AUTHOR = C23 / ".cache/fresh-v3"
OUT = HERE / ".cache/source-replay-v1"
EXPECTED_MANIFEST = "b96de55a061b27e05efcff01df5ca0005278d9dec4f3dc61c75f09018554c104"
PROVIDERS = [
    (ROOT / "QuantumBlockEncoding/StoredGivens.lean", "QuantumBlockEncoding/StoredGivens"),
    (ROOT / "experiments/hermite-polynomial/precision/piecewise-kernel-assembly-c21/ActualCoefficients.lean", "ActualCoefficients"),
    (ROOT / "QuantumBlockEncoding/StoredHermiteCoefficients.lean", "QuantumBlockEncoding/StoredHermiteCoefficients"),
    (C23 / "ChargedSourceCache.lean", "ChargedSourceCache"),
    (C23 / "CacheConsumerChecks.lean", "CacheConsumerChecks"),
]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def label(p):
    p = p.resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        if "/lib/lean/" in p.as_posix():
            return "[lean-toolchain]/lib/lean/" + p.as_posix().split("/lib/lean/", 1)[1]
        if "/bin/" in p.as_posix():
            return "[lean-toolchain]/bin/" + p.name
        return "[external]/" + p.name

def clean(s):
    for p in (ROOT, Path.home()):
        replacement = "." if p == ROOT else "[user]"
        s = re.sub(re.escape(str(p)), replacement, s, flags=re.IGNORECASE)
        s = re.sub(re.escape(p.as_posix()), replacement, s, flags=re.IGNORECASE)
    s = re.sub(r"\[user\][\\/]\.elan[\\/]toolchains[\\/][^\\/\r\n]+[\\/]lib[\\/]lean[\\/]",
               "[lean-toolchain]/lib/lean/", s)
    return s

def save(name, value):
    p = HERE / name
    assert not p.exists(), "Preserve existing evidence: " + name
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        p.write_text(value, encoding="utf-8", newline="\n")
    else:
        p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return p

def setup():
    assert not OUT.exists(), "Never overwrite a prior private cache"
    assert digest(C23 / "final-binding-manifest.json") == EXPECTED_MANIFEST
    manifest = json.loads((C23 / "final-binding-manifest.json").read_text(encoding="utf-8"))
    pins = {}
    for rel, sha in manifest["artifact_hashes"].items():
        p = C23 / rel
        assert digest(p) == sha, "Frozen author artifact changed: " + rel
        pins[p] = sha
    pins[C23 / "final-binding-manifest.json"] = EXPECTED_MANIFEST
    for key in ("selected_direct_imports_and_companions_at_freeze", "selected_import_source_snapshots_at_freeze"):
        for rel, sha in manifest[key].items():
            if rel.startswith("[lean-toolchain]"):
                continue
            p = ROOT / rel
            assert digest(p) == sha, "Bound provider changed: " + rel
            pins[p] = sha
    for p, _ in PROVIDERS:
        pins[p] = digest(p)
    for rel in ("lean-toolchain", "lake-manifest.json", "AGENTS.md", "HARNESS.md",
                "docs/theorem-publication-protocol.md", "docs/proof-digestion-protocol.md",
                "docs/evidence-routed-memory-protocol.md", ".agents/skills/qbe-substantive-worker/SKILL.md"):
        pins[ROOT / rel] = digest(ROOT / rel)
    prefix = subprocess.run(["lake", "env", "lean", "--print-prefix"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8")
    paths = subprocess.run(["lake", "env", "powershell", "-NoProfile", "-Command", "$env:LEAN_PATH"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    assert prefix.returncode == paths.returncode == 0
    binary = Path(prefix.stdout.strip()) / "bin/lean.exe"
    inherited = [ROOT / "experiments/hermite-polynomial/precision" / d / ".cache"
                 for d in ("piecewise-kernel-assembly-c21", "piecewise-kernel-producer", "piecewise-kernel-uniform-c20")]
    for directory in inherited:
        for p in directory.rglob("*"):
            if p.is_file():
                pins[p] = digest(p)
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join([str(OUT), str(AUTHOR), *map(str, inherited), paths.stdout.strip()])
    OUT.mkdir(parents=True)
    # Complete namespace root. Copied providers remain explicitly inherited,
    # and the two source-gated module files are not copied as target providers.
    qbe = AUTHOR / "QuantumBlockEncoding"
    for p in qbe.rglob("*"):
        if p.is_file():
            pins[p] = digest(p)
            if p.name.startswith(("StoredGivens.", "StoredHermiteCoefficients.")):
                continue
            dst = OUT / "QuantumBlockEncoding" / p.relative_to(qbe)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            pins[dst] = digest(dst)
    version = subprocess.run([str(binary), "--version"], cwd=ROOT, env=env,
                             capture_output=True, text=True, encoding="utf-8")
    assert version.returncode == 0 and "version 4.33.0" in version.stdout
    state = {"binary": str(binary), "env_path": env["LEAN_PATH"],
             "pins": {str(p): h for p, h in pins.items()}, "fresh_modules": []}
    (OUT / "private-state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    save("pre-gate.json", {"author_manifest_sha256": EXPECTED_MANIFEST,
         "lean_version": version.stdout.strip(), "lean_binary_sha256": digest(binary),
         "frozen_inputs": {label(p): h for p, h in pins.items()},
         "path_priority": [label(OUT), label(AUTHOR), *map(label, inherited)],
         "library_tail": "Resolved lake paths behind explicit private paths",
         "namespace_copy": "Inherited fresh-v3 namespace except recompiled target modules",
         "clean_transitive_rebuild": False})
    for src, mod in PROVIDERS:
        if not gate(src, mod, "source-" + mod.replace("/", "-")):
            return False
    return True

def gate(src, module, tag):
    statepath = OUT / "private-state.json"
    state = json.loads(statepath.read_text(encoding="utf-8"))
    pins = {Path(p): h for p, h in state["pins"].items()}
    def verify():
        for p, h in pins.items():
            assert digest(p) == h, "Input drift: " + label(p)
    verify()
    source_hash = digest(src)
    snapshot = HERE / ".cache/snapshots" / (tag + ".lean")
    assert not snapshot.exists()
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, snapshot)
    env = os.environ.copy()
    env["LEAN_PATH"] = state["env_path"]
    def invoke(args):
        return subprocess.run([state["binary"], *args], cwd=ROOT, env=env,
                              capture_output=True, text=True, encoding="utf-8")
    deps = invoke(["--deps", src.relative_to(ROOT).as_posix()])
    save(".cache/raw/" + tag + ".deps.log", deps.stdout + deps.stderr)
    save(tag + ".deps.log", clean(deps.stdout + deps.stderr))
    assert deps.returncode == 0
    selected = []
    for line in deps.stdout.splitlines():
        if not line.strip().endswith(".olean"):
            continue
        p = Path(line.strip()).resolve()
        assert p.is_file()
        selected.append({"path": label(p), "sha256": digest(p),
                         "fresh_source_in_this_review": p.relative_to(OUT).as_posix()[:-6] in state["fresh_modules"]
                         if p.is_relative_to(OUT) else False})
        pins[p] = digest(p)
        for suffix in (".private", ".server"):
            companion = Path(str(p) + suffix)
            if companion.is_file():
                pins[companion] = digest(companion)
    required = {"ChargedSourceCache": ["ActualCoefficients", "QuantumBlockEncoding/StoredGivens"],
                "CacheConsumerChecks": ["ChargedSourceCache", "QuantumBlockEncoding/StoredHermiteCoefficients"],
                "IndependentConsumer": ["ChargedSourceCache", "QuantumBlockEncoding/StoredHermiteCoefficients"]}.get(module, [])
    for mod in required:
        assert any(d["path"] == label(OUT / (mod + ".olean")) and d["fresh_source_in_this_review"] for d in selected)
    target = OUT / (module + ".olean")
    assert not target.exists(), "Target must not preexist: " + module
    target.parent.mkdir(parents=True, exist_ok=True)
    proc = invoke(["-o", str(target), src.relative_to(ROOT).as_posix()])
    raw = proc.stdout + proc.stderr
    save(".cache/raw/" + tag + ".log", raw)
    log = save(tag + ".log", clean(raw))
    verify()
    assert digest(src) == source_hash, "Source changed during compilation"
    reports = re.findall(r"depends on axioms: \[([^\]]*)\]", raw)
    no_axioms = re.findall(r"does not depend on any axioms", raw)
    ordinary = all(set(re.findall(r"[A-Za-z_][\w.]*", s)) <=
                   {"propext", "Classical.choice", "Quot.sound"} for s in reports)
    record = {"source": label(src), "source_sha256": source_hash, "exit": proc.returncode,
              "log": log.name, "log_sha256": digest(log), "selected_direct_imports": selected,
              "axiom_reports": len(reports), "axiom_free_reports": len(no_axioms),
              "ordinary_axioms_only": ordinary, "sources_and_selected_imports_stable_pre_post": True}
    if target.exists():
        record["output"] = {"path": label(target), "sha256": digest(target)}
    save(tag + ".json", record)
    if proc.returncode == 0 and ordinary:
        state["fresh_modules"].append(module)
    state["pins"] = {str(p): h for p, h in pins.items()}
    statepath.write_text(json.dumps(state, indent=2), encoding="utf-8")
    print(json.dumps({"gate": tag, "exit": proc.returncode, "ordinary_axioms_only": ordinary}), flush=True)
    return proc.returncode == 0 and ordinary

if __name__ == "__main__":
    if sys.argv[1] == "setup":
        ok = setup()
    elif sys.argv[1] == "resume-source-order":
        # ActualDecomposition's cached transitive graph imports the real cache.
        # Preserve the first failure and fix only provider scheduling.
        ok = True
        for src, mod in [PROVIDERS[2], PROVIDERS[1], PROVIDERS[3], PROVIDERS[4]]:
            if not gate(src, mod, "source-v2-" + mod.replace("/", "-")):
                ok = False
                break
    else:
        attempt = sys.argv[1]
        ok = gate(HERE / "IndependentConsumer.lean", "IndependentConsumer", "consumer-" + attempt)
    raise SystemExit(0 if ok else 1)
