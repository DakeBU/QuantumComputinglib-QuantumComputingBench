#!/usr/bin/env python3
"""Bounded AUTHOR graph-only successor. Build is exclusive; verify is read-only."""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
WIP = "AUTHOR_WIP_NOT_ADMITTED"
AUTHOR = "/root/ghl_graph_successor_c30"
ORIGINAL_AUTHOR = "ghl-source-author-c30"
TARGET = "QuantumBlockEncoding/GHL2025.lean"
GRAPH = "author-graph-views.json"
CANDIDATE = "publication-candidate-GHL2025.json"
BRIDGE = "author-binding-bridge-proposal.json"
INHERIT = (
    "author-binder-definition-audit.json", "author-decoder-packet.json",
    "author-formal-context.json", "author-source-coverage.json",
    "author-source-row-candidate.json", "formal-input-seal.json",
    "ghl-global-slot-clean-domain-and-transpose-boundary.md", "source-clarification-v2.md",
)
CHANGES = {
    "construction:swap-permutation": (["result:carriers"], "result:layout-data"),
    "construction:indicator-permutation": (["result:carriers"], "result:layout-data"),
    "construction:conditional-witness": (
        ["premise:supplied-preimage", "result:splice"], "result:transpose-matrix"),
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(path.read_bytes())

def jb(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()

def record(path, name=None, scope=None):
    raw = path.read_bytes()
    result = {"path": name or path.name, "sha256": sha(raw), "bytes": len(raw)}
    if scope:
        result["scope"] = scope
    return result

def emit(out, name, value):
    raw = value if isinstance(value, bytes) else jb(value)
    path = out / name
    assert path.parent == out and not path.exists(), ("EXCLUSIVE_NEW_FILE", name)
    assert raw.endswith(b"\n") and b"\x00" not in raw
    exe = shutil.which("codex.exe")
    assert exe, "apply_patch unavailable"
    blocks, block, count = [], [], 0
    for line in raw.decode().splitlines():
        assert len(line.encode("utf-16-le")) // 2 < 12000
        if block and count + len(line) > 6500:
            blocks.append(block)
            block, count = [], 0
        block.append(line)
        count += len(line) + 2
    if block:
        blocks.append(block)
    last = None
    for index, block in enumerate(blocks):
        patch = "*** Begin Patch\n"
        if index == 0:
            patch += "*** Add File: " + name + "\n"
        else:
            patch += "*** Update File: " + name + "\n@@\n " + last + "\n"
        patch += "".join("+" + line + "\n" for line in block)
        if index:
            patch += "*** End of File\n"
        patch += "*** End Patch"
        argv = [exe, "--codex-run-as-apply-patch", patch]
        assert len(subprocess.list2cmdline(argv).encode("utf-16-le")) // 2 + 1 < 30000
        run = subprocess.run(argv, cwd=out, capture_output=True, text=True)
        assert run.returncode == 0, (name, index, run.stdout, run.stderr)
        last = block[-1]
    assert path.read_bytes() == raw, ("APPLIED_BYTES_MISMATCH", name)

def diff(before, after, prefix=""):
    if type(before) is not type(after):
        return [{"path": prefix, "before": before, "after": after}]
    if isinstance(before, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            child = prefix + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in before or key not in after:
                result.append({"path": child, "before": before.get(key), "after": after.get(key)})
            else:
                result.extend(diff(before[key], after[key], child))
        return result
    if isinstance(before, list):
        if len(before) != len(after):
            return [] if before == after else [{"path": prefix, "before": before, "after": after}]
        return [item for i, (a, b) in enumerate(zip(before, after))
                for item in diff(a, b, prefix + "/" + str(i))]
    return [] if before == after else [{"path": prefix, "before": before, "after": after}]

class FileView:
    def __init__(self, root, relative, overlay):
        self.root, self.relative, self.overlay = root, relative, overlay

    def read_bytes(self):
        return self.overlay[self.relative] if self.relative in self.overlay else (self.root / self.relative).read_bytes()

    def read_text(self, encoding="utf-8"):
        return self.read_bytes().decode(encoding)

def binding(repo, predecessor, candidate):
    """Execute only the unchanged checker binding_digest AST, not admission entrypoints."""
    checker = repo / "website/scripts/check_research_publications.py"
    tree = ast.parse(checker.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "binding_digest")
    row = read(predecessor / "author-source-row-candidate.json")["source"]
    catalog = read(repo / "website/research/sources.json")
    existing = [s for s in catalog["sources"] if s["id"] == row["id"]]
    assert not existing or existing == [row]
    if not existing:
        catalog["sources"].append(row)
    overlay = {candidate["lesson_path"]: (predecessor / INHERIT[6]).read_bytes(),
               "website/research/sources.json": json.dumps(catalog, ensure_ascii=False).encode()}

    def local_file(root, name):
        path = PurePosixPath(name)
        assert not path.is_absolute() and not PureWindowsPath(name).is_absolute()
        assert ".." not in path.parts and "\\" not in name
        assert name in overlay or (root / name).is_file()
        return FileView(root, name, overlay)

    ns = {"Path": Path, "Any": Any, "hashlib": hashlib, "json": json,
          "local_file": local_file, "load": lambda root, name: json.loads(local_file(root, name).read_bytes())}
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<unchanged-checker-binding-digest>", "exec"), ns)
    return ns["binding_digest"](repo, candidate)

def snapshot(predecessor):
    author = predecessor.parent.parent
    return [record(p, p.relative_to(author).as_posix()) for p in sorted(author.rglob("*")) if p.is_file()]

def unchanged_inputs(repo, predecessor):
    frozen = read(predecessor / "metadata-freeze.json")
    for rec in frozen["strict_inputs"]:
        assert record(repo / rec["path"], rec["path"]) == rec, ("REPO_INPUT_DRIFT", rec["path"])
    for rec in read(predecessor / "outputs-manifest.json")["artifacts"]:
        actual = record(predecessor / rec["path"], rec["path"])
        assert all(actual[key] == rec[key] for key in actual), rec["path"]
    return frozen

def verify(repo, predecessor, out, manifest=True):
    frozen = unchanged_inputs(repo, predecessor)
    freeze = read(out / "metadata-freeze-v4.json")
    assert snapshot(predecessor) == freeze["predecessor_tree_snapshot"]
    for rec in freeze["artifacts"]:
        actual = record((predecessor if rec["scope"] == "predecessor" else out) / rec["path"], rec["path"], rec["scope"])
        assert actual == rec, rec["path"]
    old = read(predecessor / GRAPH)
    new = read(out / GRAPH)
    old_sg = old["views"]["source-construction-graph"]
    sg = new["views"]["source-construction-graph"]
    expected = copy.deepcopy(old)
    for edge in expected["views"]["source-construction-graph"]["AND_hyperedges"]:
        if edge["id"] in CHANGES:
            before, extra = CHANGES[edge["id"]]
            assert edge["tails"] == before
            edge["tails"] = before + [extra]
    assert new == expected, "NONAUTHORIZED_GRAPH_DIFF"
    changes = diff(old, new)
    assert len(changes) == 3
    assert read(out / "semantic-diff-v4.json")["graph_diff"] == changes
    ids = {n["id"] for n in sg["nodes"]}
    assert len(ids) == len(sg["nodes"])
    for edge in sg["AND_hyperedges"] + new["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"] == "AND" and set(edge["tails"] + edge["heads"]) <= ids
    assert sg["nodes"] == old_sg["nodes"]
    assert sg["open_source_gap_ids"] == old_sg["open_source_gap_ids"]
    assert all(n["status"] == "OPEN" for n in sg["nodes"] if n["kind"] == "SOURCE_GAP")
    assert sg["construction_OR_routes"] == []
    # Acyclicity over complete hyperedges, not independently sufficient split arrows.
    adjacency = {key: set() for key in ids}
    for edge in sg["AND_hyperedges"]:
        for tail in edge["tails"]:
            adjacency[tail].update(edge["heads"])
    visiting, visited = set(), set()

    def visit(key):
        assert key not in visiting, ("GRAPH_CYCLE", key)
        if key not in visited:
            visiting.add(key)
            for head in adjacency[key]:
                visit(head)
            visiting.remove(key)
            visited.add(key)
    for key in ids:
        visit(key)
    candidate = read(out / CANDIDATE)
    assert candidate["graph_contribution"]["source_graph_sha256"] == sha((out / GRAPH).read_bytes())
    assert binding(repo, predecessor, candidate) == candidate["binding_sha256"]
    assert binding(repo, predecessor, read(predecessor / CANDIDATE)) == read(predecessor / CANDIDATE)["binding_sha256"]
    bridge = read(out / BRIDGE)
    assert bridge["bindings"][0]["binding_sha256"] == candidate["binding_sha256"]
    assert bridge["formal_context_sha256"] == sha((predecessor / "author-formal-context.json").read_bytes())
    assert bridge["formal_packet_sha256"] == sha((predecessor / "author-decoder-packet.json").read_bytes())
    seal = read(out / "author-successor-seal-v4.json")
    for rec in seal["bindings"]:
        assert rec == record((predecessor if rec["scope"] == "predecessor" else out) / rec["path"], rec["path"], rec["scope"])
    for obj in (candidate, seal, freeze):
        assert obj["status"] == WIP
        assert not obj["independent_acceptance"] and not obj["main_admission"] and not obj["scientific_ROOT"]
    assert candidate["formalizer"] == AUTHOR and candidate["historical_formalizer"] == "UNKNOWN"
    assert candidate["original_author"] == ORIGINAL_AUTHOR
    if manifest:
        man = read(out / "outputs-manifest-v4.json")
        for rec in man["effective_artifacts"]:
            assert rec == record((predecessor if rec["scope"] == "predecessor" else out) / rec["path"], rec["path"], rec["scope"])
        assert {r["path"] for r in man["effective_artifacts"] if r["scope"] == "successor-v4"} == {
            p.name for p in out.iterdir() if p.is_file() and p.name != "outputs-manifest-v4.json"}
    return {"status": WIP, "mechanical_integrity": "PASS_NOT_ADMISSION", "read_only_verify": True,
            "exact_graph_diff_paths": [c["path"] for c in changes], "graph_AND_edges": len(sg["AND_hyperedges"]),
            "OPEN_source_gaps": len(sg["open_source_gap_ids"]), "all_other_graph_semantics_unchanged": True,
            "inherited_artifacts_rehashed_not_regenerated": len(INHERIT), "publication_binding_replayed": candidate["binding_sha256"],
            "predecessor_bytes_unchanged": True, "strict_repo_inputs_unchanged": len(frozen["strict_inputs"]),
            "manifest_verified": manifest, "Lean_executed": False, "Git_executed": False, "network_used": False,
            "independent_result_files_read": False, "independent_evidence_fabricated": False,
            "independent_acceptance": False, "main_admission": False, "scientific_ROOT": False, "PURIFIED": False}

def build(repo, predecessor, out):
    assert sorted(p.name for p in out.iterdir()) == [Path(__file__).name], "NEW_DIRECTORY_REQUIRED"
    frozen = unchanged_inputs(repo, predecessor)
    before_tree = snapshot(predecessor)
    graph = read(predecessor / GRAPH)
    previous_graph = copy.deepcopy(graph)
    for edge in graph["views"]["source-construction-graph"]["AND_hyperedges"]:
        if edge["id"] in CHANGES:
            before, extra = CHANGES[edge["id"]]
            assert edge["tails"] == before
            edge["tails"] = before + [extra]
    emit(out, GRAPH, graph)
    feedback = {
        "status": WIP, "id": "STATIC-GRAPH-01", "current_author": AUTHOR,
        "original_author": ORIGINAL_AUTHOR, "historical_formalizer": "UNKNOWN",
        "authority": "Explicit parent delegation of bounded independent STATIC feedback only; not new theorem premises or source/math error.",
        "feedback_received": [
            "conditional-witness complete tail additionally needs result:transpose-matrix",
            "swap-permutation complete tail additionally needs result:layout-data",
            "indicator-permutation complete tail additionally needs result:layout-data"],
        "input_boundary": "Original AUTHOR final package, source M0-M14, target/provider/config/checker as needed; no decoder/runtime/CI/reviewer result files or other independent conclusions.",
        "direct_code_reads": [
            {"lines": "5585-5616 -> 5534-5544 -> 5505-5512 and 3561-3564", "reason": "Cleanup constructor supplies daggerEntry through literal transpose-matrix definition; splice safety does not supply that matrix entry alone."},
            {"lines": "5972-5996 -> 2076-2081", "reason": "Both shifted XOR masks need address-block width <= total width; M10 separates involution from finite-range closure."},
            {"lines": "8352-8363 -> 8341-8345; 8275-8283 -> 8265-8269", "reason": "Indicator range needs q<T, while row preservation and involution need q>=1+n. These follow from existing layout data, not added premises."}],
        "source_reads": ["M10 finite-range, row-preservation and finite-basis permutation argument", "M14 existing canonical n-only bulk and branch priority unchanged"],
        "independent_result_files_read": False, "new_theorem_premises": False,
        "source_or_math_error_claim": False, "independent_approval": False,
    }
    emit(out, "authorized-feedback-v4.json", feedback)
    candidate = read(predecessor / CANDIDATE)
    candidate["graph_contribution"]["source_graph_sha256"] = sha((out / GRAPH).read_bytes())
    candidate["formalizer"] = AUTHOR
    candidate["original_author"] = ORIGINAL_AUTHOR
    candidate["current_author_role"] = "AUTHOR-side graph-only successor curator; NOT independent source reviewer, decoder or historical formalizer"
    candidate["graph_successor"] = "successor-v4; STATIC-GRAPH-01; original source and formal inputs unchanged; review pending"
    candidate["binding_sha256"] = binding(repo, predecessor, candidate)
    emit(out, CANDIDATE, candidate)
    bridge = read(predecessor / BRIDGE)
    bridge["bindings"][0]["binding_sha256"] = candidate["binding_sha256"]
    bridge["feedback_scope"] = "Prior M14 clarification retained; new explicitly authorized STATIC-GRAPH-01 complete-AND-tail correction only. No independent result files read."
    bridge["current_author"] = AUTHOR
    bridge["original_author"] = ORIGINAL_AUTHOR
    bridge["historical_formalizer"] = "UNKNOWN"
    bridge["source_graph_sha256"] = sha((out / GRAPH).read_bytes())
    bridge["successor"] = "v4; formal-only seal and packet unchanged, publication binding renewed, independent re-review pending"
    emit(out, BRIDGE, bridge)
    semantic = {"status": WIP, "graph_diff": diff(previous_graph, graph),
                "publication_diff": diff(read(predecessor / CANDIDATE), candidate),
                "bridge_diff": diff(read(predecessor / BRIDGE), bridge),
                "source_statement_and_binders_changed": False,
                "all_nodes_gaps_OR_routes_and_other_graph_views_unchanged": True}
    emit(out, "semantic-diff-v4.json", semantic)
    seal = {"status": WIP, "kind": "AUTHOR_GRAPH_ONLY_SUCCESSOR_SEAL_NOT_PROOF_SEAL", "version": "successor-v4",
            "current_author": AUTHOR, "original_author": ORIGINAL_AUTHOR, "historical_formalizer": "UNKNOWN",
            "bindings": [record(predecessor / n, scope="predecessor") for n in INHERIT] +
                        [record(out / n, scope="successor-v4") for n in (GRAPH, CANDIDATE, BRIDGE, "authorized-feedback-v4.json", "semantic-diff-v4.json")],
            "formal_input_seal_disposition": "Inherited byte-for-byte: graph correction cannot alter formal-only context/packet. This seal binds the new graph and renewed publication/bridge instead.",
            "independent_re_review": "PENDING_SAME_ORIGINAL_SOURCEFIRST_REVIEWER", "independent_acceptance": False,
            "main_admission": False, "scientific_ROOT": False, "PURIFIED": False}
    emit(out, "author-successor-seal-v4.json", seal)
    emit(out, "re-review-packet-v4.md", RE_REVIEW.encode())
    emit(out, "worker-handoff-v4.md", HANDOFF.encode())
    freeze = {"status": WIP, "version": "successor-v4", "current_author": AUTHOR,
              "predecessor": "$AUTHOR/final/metadata/successor-v3", "predecessor_tree_snapshot": before_tree,
              "predecessor_manifest": record(predecessor / "outputs-manifest.json", scope="predecessor"),
              "artifacts": [record(predecessor / n, scope="predecessor") for n in INHERIT] +
                           [record(p, scope="successor-v4") for p in sorted(out.iterdir()) if p.is_file()],
              "strict_inputs_inherited_from_predecessor_freeze": True,
              "binding_recipe": {"checker_sha256": frozen["checker_sha256"], "function": "binding_digest",
                                 "unchanged_AST": True, "admission_entrypoints_called": False},
              "feedback_provenance": "authorized-feedback-v4.json", "independent_acceptance": False,
              "main_admission": False, "scientific_ROOT": False, "production_writes": False,
              "Lean_executed": False, "Git_executed": False, "all_artifacts_WIP": True}
    emit(out, "metadata-freeze-v4.json", freeze)
    report = verify(repo, predecessor, out, manifest=False)
    emit(out, "mechanical-selftest-v4.json", report)
    manifest = {"status": WIP, "version": "successor-v4", "sparse_successor": True,
                "effective_artifacts": [record(predecessor / n, scope="predecessor") for n in INHERIT] +
                                       [record(p, scope="successor-v4") for p in sorted(out.iterdir()) if p.is_file()],
                "scope_resolution": {"predecessor": "--predecessor immutable directory", "successor-v4": "--out new directory"},
                "retired_effective_metadata": ["author-package-build.py", "mechanical-selftest.json", "metadata-freeze.json", "outputs-manifest.json"],
                "manifest_self_hash_excluded": True, "canonical_integration_owner": "Parent only; no canonical paths written",
                "independent_acceptance": False, "main_admission": False, "scientific_ROOT": False}
    emit(out, "outputs-manifest-v4.json", manifest)
    print(json.dumps(verify(repo, predecessor, out), ensure_ascii=False, indent=2))

RE_REVIEW = """# Source-first graph successor-v4: bounded re-review request

Recipient: SAME original source-first reviewer, routed by parent; no new reviewer identity or approval is manufactured. Current curator /root/ghl_graph_successor_c30 is AUTHOR-side, original author ghl-source-author-c30 is distinct, historical formalizer UNKNOWN.

Scope: STATIC-GRAPH-01 only. Natural source M0-M14, target Lean, theorem binders and all OPEN gaps are unchanged. This is a missing graph-dependency correction, not a source/math repair or proof. Keep your original source-first restrictions; the code traces here are AUTHOR provenance, not authorization to inspect implementation in a source-only review phase.

Smallest sufficient evidence packet:

1. The unchanged original source-only.md plus predecessor source-clarification-v2.md (M14), or their byte-identical predecessor prospective lesson. Relevant regions M5, M10, M12, M14; no replacement prose.
2. New author-graph-views.json; semantic-diff-v4.json graph_diff gives exactly three complete AND-tail changes. Every prior tail is retained.
3. authorized-feedback-v4.json for narrowly authorized feedback provenance; author-successor-seal-v4.json and outputs-manifest-v4.json for exact content bindings and inherited-byte resolution.

Questions: Does conditional-witness retain supplied-preimage and splice AND transpose-matrix? Do swap-permutation and indicator-permutation each retain carriers AND layout-data? Are these dependencies rather than new public premises? Are all nodes, existing tails, boundaries, OPEN gaps and other graph views preserved? Re-read the raw source against the complete proposed graph, not just this author summary. No independent acceptance, main admission, ROOT, full-space unitary closure or PURIFIED claim is made.

Separate source-first review from later formal correspondence review. New candidate/bridge hashes are available for parent integration but are not source-review conclusions. Parent must preserve original independent artifacts and explicitly determine what evidence requires re-binding or re-review; do not silently retarget prior accepted evidence.
"""

HANDOFF = """# Bounded worker handoff: AUTHOR graph-only successor-v4

Objective / frontier node: correct complete AND tails under STATIC-GRAPH-01, preserving source/formal contracts.
Mathematical delta: missing dependency bookkeeping only, no theorem, source repair or scientific root closure. Conditional-witness additionally depends on transpose-matrix; both finite permutation constructions additionally depend on layout-data.
Effect on root frontier: more faithful graph; every prior OPEN gap remains OPEN.
Named evidence: authorized-feedback-v4.json code traces and source M10/M14; semantic-diff-v4.json; read-only verify command below. No Lean build/test run was authorized or performed.
Assumptions/conventions: inherited byte-identical formal inputs and source M0-M14; no extra theorem premises.
Files changed: new scratch successor only. Eight inherited artifacts rehashed/referenced without regeneration; old artifacts, production Lean, registry and lesson untouched.
Reusable insight: finite involution and finite-range/layout obligations are separate; a supplied preimage plus splice does not by itself supply a literal transpose-matrix entry.
Failure class: NONE for bounded graph correction. All independent reviews/admission remain pending, not blocked mathematics.
Salvage audit: no routes/declarations removed; prior evidence retained, none promoted.
Process-memory IDs consulted: none; explicit bounded input restriction.
Direction fingerprint / expected information gain: STATIC-GRAPH-01 complete-AND-tail-minimal-successor; exactly three graph semantic paths corrected.
Parallel admission/common-blind-spot: no child agents, no competing routes; not applicable.
Default verified route/comparator: none selected or promoted.
Purification / Exposition Seal: PENDING unchanged; no new Exposition Seal.
Source/Lean expansion nodes: existing M0-M14/source inventory and lexical Lean ownership unchanged. No elaborated theorem-dependency claim.
Residual risk: static integrity and content binding do not establish mathematical completeness or reviewer independence. Same original source-first reviewer must re-review; parent alone integrates.

Read-only verification (PowerShell, from successor directory):

```powershell
python .\\derive-successor-v4.py --verify --repo 'REPOSITORY_ROOT' --predecessor '../../ghl-source-author-c30/final/metadata/successor-v3' --out '.'
```

Artifact dependency order: inherited source/formal/coverage/audit/row/seal -> graph -> publication binding -> bridge -> semantic diff -> author successor seal -> re-review/handoff + metadata freeze -> mechanical selftest -> effective output manifest. No cyclic self-hashes; output manifest excludes itself. Source/formal packet digests do not change; graph/publication/bridge digests do. The old producer is reference-only, never executed.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--predecessor", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    repo, predecessor, out = args.repo.resolve(), args.predecessor.resolve(), args.out.resolve()
    if args.verify:
        print(json.dumps(verify(repo, predecessor, out), ensure_ascii=False, indent=2))
    else:
        build(repo, predecessor, out)
