"""Bounded AUTHOR/WIP successor; no canonical writes, native calls or reviews."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREDECESSOR = "reviews/publication/real-preparation-c32/metadata-v2-wip-public-bundle.zip"
PRE_SHA = "14e37b46ed7fdd358c67a1c9557c7e8d1da8faae4eb2119aadfe15f929c003de"
V2 = "936020bf35582267a8149ed49addd9a9b106c23512205acaf49e9a3febaa6d80"
V3 = "dba646110300c6a8e9f8b275eeb0dba2140add2a9f0096934f03a51e886da6cd"
FORMAL = "16aed6ce6806d4423a421683905cead1cd2bb9818665b86594965bcae197694c"
CHECKER = "f8f6d7232376b5bc19a480b7e0ef549a5fafa8d66017e07482f7e6999962f8ad"
LESSON = "docs/publication-c32-v3/source-effective-v3.md"
SOURCE_ID = "candidate:retrospective-real-preparation-c32-v3"
AUTHOR = "/root/real_preparation_metadata_v3_c40"
PENDING = "AUTHOR_PROPOSED_RZ_CLARIFICATION_PENDING_INDEPENDENT_MINIMALITY_AND_FORMAL_REVIEW"
RZ_PENDING = "A2 literal Rz convention is author-proposed clarified; independent minimality and whole-module source-to-formal comparison remain PENDING. No sourceAgreement closure by metadata."
CONFIG = ("QuantumBlockEncoding.lean", "Tests.lean", "lakefile.lean", "lake-manifest.json", "lean-toolchain")
GATES = {"sourceAgreement": None, "publicationBinding": None, "axiomPolicyPass": None,
         "nativeAccepted": False, "scientific_ROOT": False, "main_admission": False}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packed(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()


def emit(name, obj):
    path = HERE / name
    assert path.resolve().is_relative_to(HERE)
    path.write_bytes(packed(obj))


def read(name):
    return json.loads((HERE / name).read_bytes())


def predecessor(repo):
    data = (repo / PREDECESSOR).read_bytes()
    assert sha(data) == PRE_SHA
    z = zipfile.ZipFile(repo / PREDECESSOR)
    assert len(z.namelist()) == 42
    # Audited predecessor top-level contains definitions/constants only plus a
    # guarded CLI. Never call its mutating build/snapshot/emit routines.
    ns = {"__name__": "audited_v2_helpers_only", "__file__": str(HERE / "packet_v3.py")}
    exec(compile(z.read("rebase_metadata.py"), "predecessor:rebase_metadata.py", "exec"), ns)
    return z, ns


def version(value):
    if isinstance(value, str):
        return value.replace("source-effective-v2.md", "source-effective-v3.md").replace(V2, V3)
    if isinstance(value, list):
        return [version(x) for x in value]
    if isinstance(value, dict):
        return {k: version(v) for k, v in value.items()}
    return value


def proof_inputs(repo):
    files = [repo / n for n in CONFIG]
    files += [p for d in ("QuantumBlockEncoding", "ABEISTests") for p in (repo / d).rglob("*.lean")]
    records = []
    normalized = {}
    for p in sorted(files):
        assert p.is_file() and p.resolve().is_relative_to(repo)
        name = p.relative_to(repo).as_posix()
        data = p.read_bytes()
        norm = sha(data.replace(b"\r\n", b"\n"))
        records.append({"path": name, "sha256": sha(data), "lf_normalized_sha256": norm,
                        "bytes": len(data), "role": "raw proof-input pin; not semantic/native audit"})
        normalized[name] = norm
    assert sum(x["path"].startswith("QuantumBlockEncoding/") for x in records) == 142
    assert sum(x["path"].startswith("ABEISTests/") for x in records) == 60
    assert len(records) == 207
    digest = sha(json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode())
    return {"files": records, "counts": {"production_lean": 142, "test_lean": 60,
             "proof_configurations": 5, "total": 207}, "proofInputsSha256": digest}


def official_proof_digest(repo):
    path = repo / "website/scripts/proof_inputs.py"
    spec = importlib.util.spec_from_file_location("c40_unchanged_official_proof_inputs", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    assert tuple(module.CONFIG) == CONFIG
    return module.proof_input_digest(repo)


def source_row():
    return {"id": SOURCE_ID,
            "title": "Exact real amplitude trees and local isometry completion (literal Rz clarification v3)",
            "authors": ["Retrospective recovery author real-preparation-author-c32; source v3 author /root; historical formalizer UNKNOWN"],
            "url": "", "year": 2026,
            "status": "candidate-retrospective-original-source-v3-unreviewed-formal-correspondence",
            "anchor": "source-effective-v3.md SHA256 " + V3,
            "scope": "Same three whole modules; only A2 literal Rz convention added; exact phase retained, no new tree instruction, theorem, hypothesis or bound.",
            "formal_status": "AUTHOR/WIP; independent source minimality and formal comparison PENDING; no acceptance from metadata",
            "source_sha256": V3, "predecessor_source_sha256": V2,
            "historical_formalizer": "UNKNOWN", "natural_clarification_author": "/root"}


def overlay(repo, ns, records=None):
    catalog = json.loads((repo / "website/research/sources.json").read_bytes())
    assert not any(x["id"] == SOURCE_ID for x in catalog["sources"])
    row = source_row()
    catalog["sources"].append(row)
    overrides = {LESSON: (HERE / "source-effective-v3.md").read_bytes(),
                 "website/research/sources.json": json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode()}
    return ns["OverlayPath"](repo, overrides), overrides, row


def graph_anchor(data, identity):
    text = data.decode()
    marker = '"id": "' + identity + '"'
    assert text.count(marker) == 1, identity
    return {"file": "four-view-graph.json", "id": identity, "anchor": marker,
            "line": text.count("\n", 0, text.index(marker)) + 1}


def build(repo, source_dir):
    assert not (HERE / "freeze.json").exists(), "frozen packet; make additive successor"
    z, ns = predecessor(repo)
    before = proof_inputs(repo)
    assert official_proof_digest(repo) == before["proofInputsSha256"]
    protected = {p: sha((repo / p).read_bytes()) for p in (
        PREDECESSOR, "website/research/sources.json", "website/research/publications.json",
        "website/scripts/check_research_publications.py", "website/scripts/proof_inputs.py")}
    assert protected["website/scripts/check_research_publications.py"] == CHECKER
    old = z.read("source-effective-v2.md").decode().replace("\r\n", "\n")
    for name in ("source-effective-v3.md", "source-change-record-v3.json", "author-seal-v3.json"):
        (HERE / name).write_bytes((source_dir / name).read_bytes())
    new_bytes = (HERE / "source-effective-v3.md").read_bytes()
    assert sha(new_bytes) == V3
    new = new_bytes.decode().replace("\r\n", "\n")
    change = read("source-change-record-v3.json")
    assert old.count(change["before"]) == 1
    assert old.replace(change["before"], change["after"], 1) == new
    for name, digest in read("author-seal-v3.json")["files"].items():
        assert sha((HERE / name).read_bytes()) == digest
    old_graph = json.loads(z.read("four-view-graph.json"))
    old_quotes = json.loads(z.read("per-root-source-quotes.json"))
    old_audit = json.loads(z.read("recursive-binder-audit.json"))
    old_records = json.loads(z.read("prospective-publication-records.json"))["records"]
    old_pins = json.loads(z.read("current-pins.json"))
    assert len(old_quotes["roots"]) == len(old_audit["roots"]) == 57
    inventory = json.loads(z.read("whole-module-inventory.json"))
    pins_by = {x["path"]: x for x in before["files"]}
    for p in old_pins["raw_ambient_context"] + old_pins["configs"]:
        assert pins_by[p["path"]]["sha256"] == p["sha256"], p["path"]
    assert sha(z.read("formal-context.md")) == FORMAL
    for mod in old_graph["lean_view"]["modules"]:
        assert pins_by[mod["path"]]["sha256"] == mod["sha256"]
    emit("predecessor.json", {"path": PREDECESSOR, "sha256": PRE_SHA, "member_count": 42,
         "immutable": True, "resolution": "predecessor:<member> addresses exact ZIP member bytes",
         "members_retained_not_copied": [{"member": n, "sha256": sha(z.read(n)), "bytes": len(z.read(n))}
             for n in z.namelist()], "formal_packet_sha256": FORMAL,
         "historical_ledger": "predecessor:prospective-publication-records.json",
         "no_review_outputs_consulted": True})

    inv = version(inventory)
    inv["source_version"] = "natural-v3; only source links versioned; raw 57 signatures/private inventory unchanged in predecessor"
    emit("whole-module-inventory.json", inv)
    quotes = version(old_quotes)
    quotes["source_version"] = "natural-v3; author correspondence only, pending independent review"
    changed_roots = []
    for r in quotes["roots"]:
        prior = next(x for x in old_quotes["roots"] if x["fullName"] == r["fullName"])
        r["quote"] = ns["section"](new, r["source_section"])
        r["quote_sha256"] = sha(r["quote"].encode())
        r["source_span"] = ns["span"](new, r["quote"])
        r["formal_source"] = "predecessor:formal-context.md"
        r["source_mapping_status"] = PENDING if r["source_section"] == "A2" else "AUTHOR_PROPOSED_NOT_INDEPENDENTLY_REVIEWED"
        if "remaining_boundary" in r:
            r["remaining_boundary"] = RZ_PENDING
        if r["quote"] != prior["quote"]:
            assert r["source_section"] == "A2"
            changed_roots.append(r["fullName"])
    quotes["additional_source_context"] = [{"source_section": label,
        "quote": ns["section"](new, label), "source_span": ns["span"](new, ns["section"](new, label)),
        "role": "unchanged H0/use-site/finite-bit boundary, not a new target root"} for label in ("H", "I")]
    emit("per-root-source-quotes.json", quotes)
    audit = version(old_audit)
    audit["metadata_version"] = 3
    audit["source_change_effect"] = "Only literal A2 Rz source formula clarified by author; all 57 exact raw signatures/logical premises/definition bodies unchanged. Independent minimality and formal agreement pending."
    old_rz = next(x for x in old_audit["open_source_mappings"] if x.startswith("Rz natural scope gap:"))
    audit["open_source_mappings"] = [RZ_PENDING if x == old_rz else x for x in old_audit["open_source_mappings"]]
    audit["literal_rz_addendum"] = {"id": "source:A2-literal-rz-v3", "kind": "literal",
         "matrix": "diag(cos(theta/2)-i*sin(theta/2), cos(theta/2)+i*sin(theta/2)); off-diagonal=0",
         "typing_data": ["theta : Real", "two input/output bit indices"], "proof_inputs_added": [],
         "exact_phase": True, "new_preparation_tree_instruction": False,
         "status": PENDING, "historical_unresolved_ledger": "predecessor:recursive-binder-audit.json"}
    emit("recursive-binder-audit.json", audit)
    emit("assumption-ledger-history.json", {"preserved": "predecessor:prospective-publication-records.json",
         "predecessor_member_sha256": sha(z.read("prospective-publication-records.json")),
         "old_rows": [{"module": r["module"], "assumption_deltas": r["assumption_deltas"]} for r in old_records],
         "v3_proposal": "Only the Rz unresolved row becomes author-proposed same against literal v3; no independent acceptance or historical ledger rewrite", **GATES})

    graph = version(old_graph)
    graph["schema"] = "aspbe-candidate-four-view-graph/v3"
    by_text = {x["text"]: x for x in old_graph["source_view"]["all_regions"]}
    regions, added = [], []
    for block in new.strip().split("\n\n"):
        if block in by_text:
            item = copy.deepcopy(by_text[block])
        else:
            identity = "source-region:v3-A2-literal-rz"
            assert not added, "only one new maximal source block permitted"
            item = {"id": identity, "text": block, "disposition": "NODE", "review": PENDING}
            added.append(identity)
        item["source_span"] = ns["span"](new, block)
        regions.append(item)
    graph["source_view"]["all_regions"] = regions
    assert all(x["text"] in new for x in old_graph["source_view"]["all_regions"])
    graph["source_view"]["source_gaps"] = [RZ_PENDING if x == old_rz else x for x in old_graph["source_view"]["source_gaps"]]
    graph["source_view"]["literal_definition_nodes"] = [dict(audit["literal_rz_addendum"],
         region=added[0], source_span=ns["span"](new, next(x["text"] for x in regions if x["id"] == added[0])),
         consumer="A2 generic one-qubit lifting; not used as Rz in C3 tree")]
    graph["source_view"]["and_hyperedges"].append({"id": "source:A2-literal-rz-lift-v3",
         "tails": ["A2 literal Rz matrix, zero off-diagonals and exact phase", "A1 highest-bit extension L", "A2 arbitrary one-qubit context lifting", "unchanged old target wire and theta"],
         "heads": ["A2 Rz instance of instruction lifting"],
         "mechanism": "Instantiate the existing arbitrary one-qubit lifting statement with the now-explicit source matrix; metadata only, no new Lean theorem", "status": PENDING,
         "boundary": "Independent minimality and whole-module comparison pending; no Rz inserted into C3"})
    graph["compressed_spine"]["nodes"].append({"id": "concept:literal-rz-lift-convention-v3",
         "expands": ["A2", "source:A2-literal-rz-v3", "source:A2-literal-rz-lift-v3"], "status": PENDING,
         "boundary": "No new reusable mathematical primitive, purification, or tree gate"})
    graph["contribution"]["successor"] = {"parent_reported_head": "8662dd854457aefaa52d9f6f8ac4467a82039459; not Git-observed by worker",
         "source_version": 3, "delta": "Only literal Rz coverage and versioned metadata; no Lean delta"}
    emit("four-view-graph.json", graph)
    emit("source-coverage-v3.json", {"source_sha256": V3,
         "method": "Every maximal blank-line-delimited source block has inherited or new explicit NODE/EXCLUDED disposition; author topology only",
         "regions": [{k: x[k] for k in ("id", "disposition", "source_span")} for x in regions],
         "formal_root_coverage": [{k: r[k] for k in ("fullName", "source_section", "source_span", "source_mapping_status")} for r in quotes["roots"]],
         "source_level_inventory": {"total": 57, "public": 53, "private": 4, "definitions": 13, "theorems": 44,
                                    "lexical_not_native_success_counts": True},
         "new_formula_coverage_node": "source:A2-literal-rz-v3", "open_scope": audit["open_source_mappings"], **GATES})
    graph_data = (HERE / "four-view-graph.json").read_bytes()
    labels = sorted(set(x["source_section"] for x in old_quotes["roots"]) | {"H", "I"})
    emit("source-change-topology.json", {"old_source_sha256": V2, "new_source_sha256": V3,
         "exact_replacement": {"change_id": change["change_id"], "before": change["before"], "after": change["after"],
             "old_span": ns["span"](old, change["before"]), "new_span": ns["span"](new, change["after"])},
         "section_equality": [{"id": label, "content_equal": ns["section"](old, label) == ns["section"](new, label),
             "old_span": ns["span"](old, ns["section"](old, label)), "new_span": ns["span"](new, ns["section"](new, label))} for label in labels],
         "root_quote_content_changes": changed_roots, "old_region_ids_removed": [], "new_region_ids": added,
         "graph_sha256": sha(graph_data), "graph_line_anchors": [graph_anchor(graph_data, i) for i in added +
             ["source:A2-literal-rz-v3", "source:A2-literal-rz-lift-v3", "concept:literal-rz-lift-convention-v3"]],
         "graph_delta": ["Version natural source links/hash and refresh region line spans",
             "Preserve all old source-region content, IDs and dispositions; append one literal Rz block",
             "Replace only the Rz OPEN wording with pending author clarification, never accepted closure",
             "Append Rz literal definition, complete conjunctive instance edge and proposed compressed drilldown",
             "All old AND hyperedges, OR routes, H0/use-site, refuted frontier and Functor hyperedges unchanged"],
         "proof_signature_or_body_changes": [], "independent_minimality": "PENDING", **GATES})

    checker = ns["load_checker"](repo)
    facade, overrides, row = overlay(repo, ns)
    records, bridge = [], []
    for prior in old_records:
        r = copy.deepcopy(prior)
        r.update(source_id=SOURCE_ID, source_statement=LESSON, lesson_path=LESSON,
                 source_anchor="natural-v3 exact whole-root quotes: reviews/publication/real-preparation-c32/metadata-v3/per-root-source-quotes.json; exact A2 delta and H0/I preservation: metadata-v3/source-change-topology.json",
                 source_version=3, natural_clarification_author="/root", metadata_rebase_author=AUTHOR,
                 predecessor_binding_sha256=prior["binding_sha256"], historical_formalizer="UNKNOWN", formalizer="UNKNOWN",
                 decoder_evidence=None, reviewer_evidence=None,
                 publication_status="AUTHOR_WIP_PROSPECTIVE_V3_NOT_ADMISSIBLE")
        for o in r["obligation_map"]:
            o["source_obligation"] = o["source_obligation"].replace("docs/publication-c32-v2/source-effective-v2.md", LESSON)
        if r["module"].endswith("RealAmplitudePreparation.lean"):
            rz = next(d for d in r["assumption_deltas"] if d["classification"] == "unresolved")
            rz.update(classification="same", source="A2 literal Rz diagonal cos-minus/plus-i-sin entries and zero off-diagonals, exact phase",
                      explanation="AUTHOR-PROPOSED SAME only for literal v3; historical unresolved row preserved in predecessor and assumption-ledger-history.json. Independent minimality and formal agreement PENDING.")
        r["graph_contribution"]["remaining_boundary"] = prior["graph_contribution"]["remaining_boundary"].replace("Rz natural scope gap retained.", RZ_PENDING)
        r["residual_boundary"] = "Historical formalizer UNKNOWN; retrospective author metadata only. Source v3 minimality and whole-module decoder/reviewer evidence PENDING; no reviewer output read. H0 use-site, actual adapter/global placement, structured/finite-bit suppliers and all inherited boundaries remain."
        r["mandatory_blockers"] = [RZ_PENDING if x == old_rz else x for x in prior["mandatory_blockers"]]
        r.update(GATES)
        r["binding_sha256"] = checker.binding_digest(facade, r)
        assert checker.binding_digest(facade, r) == r["binding_sha256"]
        isolated = dict(overrides)
        isolated[LESSON] = z.read("source-effective-v2.md")
        old_source_digest = checker.binding_digest(ns["OverlayPath"](repo, isolated), r)
        assert old_source_digest != r["binding_sha256"]
        bridge.append({"module": r["module"], "v2_historical_binding": prior["binding_sha256"],
            "v3_binding": r["binding_sha256"], "same_v3_record_and_row_with_only_v2_lesson": old_source_digest,
            "source_bytes_alone_change_digest": True, "historical_binding_reusable": False})
        records.append(r)
    emit("prospective-publication-records.json", {"schema_version": 1, "kind": "AUTHOR/WIP; actual prospective content bindings, not accepted records", "records": records, **GATES})
    emit("binding-bridge.json", {"checker_sha256": CHECKER, "method": "Actual unchanged binding_digest, read-only virtual overlay; validate_record NOT called",
         "own_unreviewed_source_row_candidate": row, "virtual_lesson_path": LESSON, "virtual_lesson_sha256": V3,
         "virtual_source_catalog_sha256": sha(overrides["website/research/sources.json"]), "bridges": bridge,
         "actual_checker_bound": "Selected record fields; target + lesson + lean-toolchain + lake-manifest.json; all 142 production + 60 test raw Lean files; selected candidate source row",
         "not_checker_bound": ["QuantumBlockEncoding.lean", "Tests.lean", "lakefile.lean", "unrelated source catalog rows", "registry bytes", "other metadata not contained in bound record fields"],
         "canonical_writes": False, "binding_is_not_acceptance": True, **GATES})
    after = proof_inputs(repo)
    assert before == after
    assert official_proof_digest(repo) == after["proofInputsSha256"]
    assert all(sha((repo / p).read_bytes()) == h for p, h in protected.items())
    emit("current-pins.json", {**before, "unchanged_before_after": True,
         "official_proof_input_digest_replayed_equal_before_after": True,
         "parent_reported_checkout": "8662dd854457aefaa52d9f6f8ac4467a82039459", "git_observed": False,
         "checker_sha256": CHECKER, "protected_read_only_inputs": protected,
         "v2_equality": {"raw_202_lean_files": True, "prior_3_configs": True,
             "two_root_config_files": "newly pinned now and unchanged before/after; no unsupported v2 whole-proof equality claim"},
         "configs": [{**pins_by[n], "actual_checker_bound": n in ("lean-toolchain", "lake-manifest.json")} for n in CONFIG],
         "toolchain_text": (repo / "lean-toolchain").read_text().strip(),
         "dependency_pins": [{"name": x["name"], "rev": x.get("rev"), "inputRev": x.get("inputRev")} for x in json.loads((repo / "lake-manifest.json").read_bytes())["packages"]]})
    emit("source-seal-v3.json", {"source_sha256": V3, "predecessor_source_sha256": V2,
         "source_author": "/root", "metadata_author": AUTHOR, "historical_formalizer": "UNKNOWN",
         "evidence_class": "RETROSPECTIVE_IMPLEMENTATION_INFORMED_AUTHOR_WIP",
         "independent_source_minimality": "PENDING", "decoder_evidence": None, "reviewer_evidence": None,
         "preproof_seal": False, "formal_packet": "predecessor:formal-context.md", "formal_packet_sha256": FORMAL,
         "production_changes": [], "proof_input_before_after_equal": True, **GATES})
    verify(repo, write_receipt=True)


def verify(repo, write_receipt=False):
    z, ns = predecessor(repo)
    receipt = []
    def check(label, condition):
        assert condition, label
        receipt.append({"check": label, "passed": True})
    old = z.read("source-effective-v2.md").decode().replace("\r\n", "\n")
    new = (HERE / "source-effective-v3.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    change = read("source-change-record-v3.json")
    check("exact v3 source bytes", sha((HERE / "source-effective-v3.md").read_bytes()) == V3)
    check("only authorized literal A2 replacement", old.replace(change["before"], change["after"], 1) == new)
    check("full 207 current proof inputs equal packet", proof_inputs(repo)["files"] == read("current-pins.json")["files"])
    check("actual official proof_input_digest replay", official_proof_digest(repo) == read("current-pins.json")["proofInputsSha256"])
    for p, h in read("current-pins.json")["protected_read_only_inputs"].items():
        check("protected bytes " + p, sha((repo / p).read_bytes()) == h)
    check("formal packet unchanged", sha(z.read("formal-context.md")) == FORMAL)
    inv_old = version(json.loads(z.read("whole-module-inventory.json")))
    inv = read("whole-module-inventory.json")
    check("57 raw inventory/signatures unchanged except version label and links", {k:v for k,v in inv.items() if k != "source_version"} == {k:v for k,v in inv_old.items() if k != "source_version"})
    a_old = version(json.loads(z.read("recursive-binder-audit.json")))
    check("all 57 recursive root binder audits unchanged except source links", read("recursive-binder-audit.json")["roots"] == a_old["roots"])
    q = read("per-root-source-quotes.json")
    check("all 57 exact root quotes/spans", len(q["roots"]) == 57 and all(r["quote"] == ns["section"](new,r["source_section"]) and r["source_span"] == ns["span"](new,r["quote"]) and r["quote_sha256"] == sha(r["quote"].encode()) for r in q["roots"]))
    g = read("four-view-graph.json")
    oldg = version(json.loads(z.read("four-view-graph.json")))
    check("Lean imports and ownership unchanged except versioned source links", g["lean_view"] == oldg["lean_view"])
    for key in ("or_routes", "or_route_and_tail_resolution", "coordinate_nodes", "status_edges", "refuted_frontier"):
        check("preserved complete source topology " + key, g["source_view"][key] == oldg["source_view"][key])
    check("all old AND tails preserved", g["source_view"]["and_hyperedges"][:-1] == oldg["source_view"]["and_hyperedges"])
    check("all Functor edges and complete conditional tails preserved", g["functor_view"] == oldg["functor_view"])
    regions = g["source_view"]["all_regions"]
    check("exhaustive source blocks and one added formula block", [r["text"] for r in regions] == new.strip().split("\n\n") and len(regions) == len(oldg["source_view"]["all_regions"]) + 1)
    check("every source block exact span and disposition", all(r["source_span"] == ns["span"](new,r["text"]) and (r["disposition"] == "NODE" or re.fullmatch(r"EXCLUDED\(.+\)", r["disposition"])) for r in regions))
    topology = read("source-change-topology.json")
    data = (HERE / "four-view-graph.json").read_bytes()
    check("exact graph hash and line anchors", sha(data) == topology["graph_sha256"] and all(x == graph_anchor(data,x["id"]) for x in topology["graph_line_anchors"]))
    check("only A2 subsection quote changed", all(x["content_equal"] == (x["id"] != "A2") for x in topology["section_equality"]))
    checker = ns["load_checker"](repo)
    facade, overrides, row = overlay(repo,ns)
    records = read("prospective-publication-records.json")["records"]
    check("exactly one virtual unreviewed source row", sum(x["id"] == SOURCE_ID for x in json.loads(overrides["website/research/sources.json"])["sources"]) == 1)
    for r in records:
        label = r["module"]
        actual = checker.binding_digest(facade,r)
        check("actual prospective binding replay " + label, actual == r["binding_sha256"])
        altered = dict(overrides)
        altered[LESSON] = z.read("source-effective-v2.md")
        check("source-byte-only sensitivity " + label, checker.binding_digest(ns["OverlayPath"](repo,altered),r) != actual)
        changed = copy.deepcopy(r)
        changed["source_anchor"] += " sensitivity-probe"
        check("bound record-field sensitivity " + label, checker.binding_digest(facade,changed) != actual)
        cat = json.loads(overrides["website/research/sources.json"])
        next(x for x in cat["sources"] if x["id"] == SOURCE_ID)["title"] += " sensitivity-probe"
        altered = dict(overrides)
        altered["website/research/sources.json"] = json.dumps(cat,ensure_ascii=False,sort_keys=True).encode()
        check("selected-row sensitivity " + label, checker.binding_digest(ns["OverlayPath"](repo,altered),r) != actual)
        ambient_path = read("current-pins.json")["files"][0]["path"]
        ambient_path = next(x["path"] for x in read("current-pins.json")["files"] if x["path"].startswith("ABEISTests/"))
        altered = dict(overrides)
        altered[ambient_path] = (repo / ambient_path).read_bytes() + b"\n-- in-memory sensitivity probe\n"
        check("ambient-test-byte sensitivity " + label, checker.binding_digest(ns["OverlayPath"](repo,altered),r) != actual)
        check("UNKNOWN formalizer and pending independent evidence " + label, r["formalizer"] == "UNKNOWN" and r["decoder_evidence"] is None and r["reviewer_evidence"] is None)
        check("no accepted gates " + label, all(r[k] == v for k,v in GATES.items()))
    check("proof-input before/after equality during verification", proof_inputs(repo)["files"] == read("current-pins.json")["files"])
    if (HERE / "freeze.json").exists():
        freeze = read("freeze.json")
        check("frozen manifest hash", sha((HERE / "manifest.json").read_bytes()) == freeze["manifest_sha256"])
        manifest = read("manifest.json")
        check("exact frozen file set", sorted(x.name for x in HERE.iterdir() if x.is_file() and x.name not in ("manifest.json","freeze.json")) == sorted(x["path"] for x in manifest["files"]))
        check("all frozen content hashes", all(sha((HERE/x["path"]).read_bytes()) == x["sha256"] for x in manifest["files"]))
    report = {"schema": "C40_BOUNDED_PYTHON_METADATA_INTEGRITY", "evidence_class": "metadata integrity and actual digest sensitivity only",
              "checks": receipt, "check_count": len(receipt), "failure_class": "NONE",
              "no_validator_acceptance_or_native_execution": True, **GATES}
    if write_receipt:
        assert not (HERE / "freeze.json").exists()
        emit("test-receipt.json",report)
    print(json.dumps({"bounded_checks_passed": len(receipt), "frozen": (HERE / "freeze.json").exists(),
         "bindings": [{"module":r["module"],"binding_digest":r["binding_sha256"]} for r in records], **GATES},ensure_ascii=False,indent=2))


def freeze(repo):
    assert not (HERE / "freeze.json").exists(), "already frozen"
    verify(repo)
    names = sorted(x.name for x in HERE.iterdir() if x.is_file() and x.name not in ("manifest.json","freeze.json","public-safe-projection-allowlist.json"))
    for name in names:
        data = (HERE / name).read_bytes()
        text = data.decode("utf-8")
        # Require a standalone drive and path-segment start: mathematical
        # e:\{...\} and escaped JSON newlines after 'unchanged:' are not paths.
        assert not re.search(r"(?i)(?<![a-z0-9_])[a-z]:[/\\](?=[\w.])",text), name
        assert not re.search(r"(?i)(?:api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]+",text), name
    emit("public-safe-projection-allowlist.json", {"policy": "deny by default; exact listed text bytes only; not release authorization",
         "files": [{"path":n,"sha256":sha((HERE/n).read_bytes())} for n in names],
         "self_and_seals": ["public-safe-projection-allowlist.json", "manifest.json", "freeze.json"],
         "blind_stage_routing": {"natural_review": ["source-effective-v3.md","source-change-record-v3.json","author-seal-v3.json"],
                                "formal_decode": ["predecessor:formal-context.md"],
                                "metadata_author_files": "NOT blind-stage inputs"},
         "actual_local_absolute_paths_or_credentials": False})
    names.append("public-safe-projection-allowlist.json")
    emit("manifest.json", {"files": [{"path": n,"sha256":sha((HERE/n).read_bytes()),"bytes":(HERE/n).stat().st_size} for n in sorted(names)],
         "excludes": ["manifest.json","freeze.json"], "predecessor_sha256": PRE_SHA})
    emit("freeze.json", {"state": "FROZEN_AUTHOR_WIP_NOT_ADMISSIBLE", "manifest_sha256":sha((HERE/"manifest.json").read_bytes()),
         "source_sha256":V3, "predecessor_sha256":PRE_SHA, "metadata_author":AUTHOR,
         "scope": "Same 3 modules; literal Rz source metadata only; no production change or independent verdict",
         "proofInputsSha256":read("current-pins.json")["proofInputsSha256"],
         "source_minimality_review":"PENDING", "decoder_evidence":None,"reviewer_evidence":None, **GATES})
    verify(repo)
    print("freeze_sha256=" + sha((HERE/"freeze.json").read_bytes()))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--source-dir",type=Path)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build",action="store_true")
    modes.add_argument("--verify-only",action="store_true")
    modes.add_argument("--freeze",action="store_true")
    args=parser.parse_args()
    repo=args.repo.resolve()
    if args.build:
        assert args.source_dir is not None
        build(repo,args.source_dir)
    elif args.freeze:
        freeze(repo)
    else:
        verify(repo)
