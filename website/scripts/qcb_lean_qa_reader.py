"""Publish qualified Lean QA companions and a metadata-only assessment summary."""
from __future__ import annotations

from html import escape
from pathlib import PurePosixPath
from posixpath import relpath
from urllib.parse import quote

from qcb_core import digest, read_json, write_json
from website.scripts.qcb_lean_downloads import encoded
from website.scripts.qcb_navigation import card


HUB = "quantumcomputingbench/"
COMPANIONS = HUB + "lean/companions/"
SPARSE = HUB + "run/assessment/sparse-address/"
DATA = "data/quantumcomputingbench/lean-qa-v1/"
SOURCE = "benchmarks/quantumcomputingbench/"
TOPICS = {
    "qcb-core-be-011": (
        "Repair the phase cancellation",
        "Hamiltonian block encoding",
        "Compute a matrix entry, trace a failed cancellation, then compare the repaired operator blocks.",
    ),
    "qcb-core-la-019": (
        "When is a tensor sum Hermitian?",
        "Hamiltonian operator algebra",
        "Combine two adjoint arguments and build a finite counterexample when one premise is dropped.",
    ),
}


def publication(commit):
    """Read only public inputs and require the exact qualifications before projection."""
    from qcb_course_hamiltonian import EVIDENCE, PLAN, qualified
    from qcb_sparse_study import QUALIFICATION, load_seal, validate_qualification

    if not (EVIDENCE / "reference-checks.json").is_file() and not QUALIFICATION.is_file():
        return None

    manifest = {"schema_version": "qcb.lean_qa_reader.v1", "source_commit": commit,
                "model_performance_measured": False}
    task_nodes, training = {}, None
    if (EVIDENCE / "reference-checks.json").is_file():
        views, status, catalog, graph = qualified()
        plan = read_json(PLAN)
        selected = {row["core_id"]: row for row in plan["entries"] if row["core_id"] in TOPICS}
        public_cores = {row["core_id"]: row for row in catalog["cores"] if row["core_id"] in TOPICS}
        if set(selected) != set(TOPICS) or set(public_cores) != set(TOPICS) or len(views) != len(TOPICS):
            raise ValueError("Hamiltonian reader requires exactly its qualified public training companions")
        companions = []
        for core_id, (title, subject, question_summary) in TOPICS.items():
            entry = selected[core_id]
            view = views[entry["view_id"]]
            core = public_cores[core_id]
            if (view["entry"]["core_id"] != core_id or view["entry"]["task_hash"] != entry["task_hash"]
                    or view["entry"]["split"] != "train" or core["split"] != "train"):
                raise ValueError("Hamiltonian companion changed its exact train identity")
            anchors = [graph[key] for key in entry["source_node_ids"]]
            companions.append({
                "core_id": core_id, "view_id": entry["view_id"], "task_hash": entry["task_hash"],
                "subject": subject, "title": title, "question_summary": question_summary,
                "split": entry["split"], "construction_band": entry["difficulty"]["construction_band"],
                "construction_rationale": entry["difficulty"]["rationale"],
                "imported_shortcut": entry["difficulty"]["imported_shortcut"],
                "formal_scope": view["formal_scope"], "source_item_digest": entry["source_item_digest"],
                "graph_anchors": [{"id": node["id"], "source": node["source"], "line": node["line"]}
                                  for node in anchors],
            })
            task_nodes[core_id] = view["task"]["nodes"]
        manifest["hamiltonian"] = {
            "course_id": plan["course_id"], "plan_digest": digest(plan),
            "graph_snapshot_id": catalog["snapshot_id"], "graph_source_commit": catalog["graph_source_commit"],
            "reference_commit": status["reference_lineage"]["recorded_code_revision"],
            "execution_class": "trusted_local_authored_reference",
            "new_mathematical_cores": status["new_mathematical_cores"],
            "new_canonical_formal_admissions": status["new_canonical_formal_admissions"],
            "companions": companions,
        }

    if QUALIFICATION.is_file():
        seal = load_seal()
        validate_qualification(seal)
        manifest["sparse_address_assessment"] = {
            key: seal[key] for key in ("probe_count", "contrast_count", "source_group", "formal_scope",
                                       "public_source_exposure")
        }
        if "hamiltonian" in manifest:
            from lean_qa_training import export

            training = export()
            profile = training["study_training_profile"]
            manifest["training_profile"] = {
                "profile_id": profile["profile_id"], "profile_digest": training["profile_digest"],
                "training_fingerprint": profile["projection_training_fingerprint"],
                "excluded_core_ids": profile["excluded_core_ids"], "counts": training["counts"],
                "actual_model_exposure_authenticated": training["actual_model_exposure_authenticated"],
            }
    return manifest, task_nodes, training


def companion_route(core_id):
    return COMPANIONS + core_id.removeprefix("qcb-core-") + "/"


def _link(route, target, label, *, download=False):
    attribute = " download" if download else ""
    return f'<a{attribute} href="{escape(relpath(target, route), quote=True)}">{escape(label)}</a>'


def entry_links(route, record):
    """Keep earlier course versions intact and link out from their existing entry points."""
    if record is None:
        return ""
    manifest, _, _ = record
    targets = []
    if "hamiltonian" in manifest:
        if route in (HUB + "lean/", HUB + "lean/compose/", HUB + "course/", HUB + "course/d3/"):
            targets.append((COMPANIONS + "index.html", "Hamiltonian companions · Course v5"))
        for core in manifest["hamiltonian"]["companions"]:
            if route == HUB + "cores/" + core["core_id"] + "/":
                targets.append((companion_route(core["core_id"]) + "index.html", "Open the Lean training companion"))
    if "sparse_address_assessment" in manifest and route in (HUB + "run/assessment/", HUB + "run/agentic-lean/"):
        targets.append((SPARSE + "index.html", "Owner-sealed sparse-address assessment"))
    if not targets:
        return ""
    return '<p class="qcb-reading-options">' + " · ".join(_link(route, *target) for target in targets) + "</p>"


def _evidence_link(source_url, path, label, *, line=1):
    url = source_url(path, line)
    return (f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' if url
            else f'<span>{escape(label)} · <code>{escape(path)}</code></span>')


def _companion(write, intro, section, disclosure, source_url, core, nodes, live_nodes, reference_commit):
    core_id = core["core_id"]
    route = companion_route(core_id)
    math = HUB + "cores/" + core_id + "/index.html#question"
    body = intro(core["title"], core["question_summary"])
    body += '<p class="qcb-breadcrumb">' + _link(route, COMPANIONS + "index.html", "Hamiltonian companions") + "</p>"
    body += '<p class="qcb-meta">' + escape(f'{core["subject"]} · {core["construction_band"]} · Train · {core_id.upper().removeprefix("QCB-CORE-")}') + "</p>"
    body += '<p>' + _link(route, math, "Read the mathematical question") + "</p>"
    body += section("What the proof checks", "<p>" + escape(core["formal_scope"]) + "</p>", "scope")
    body += '<p class="qcb-status-line">' + escape(core["construction_rationale"]) + "</p>"
    steps = []
    for node in nodes:
        inputs = ", ".join(node["depends_on"])
        steps.append("<li><code>" + escape(node["id"]) + "</code>"
                     + (" · all inputs: " + escape(inputs) if inputs else "")
                     + "<pre><code>" + escape(node["target"]) + "</code></pre></li>")
    body += disclosure("Exact Lean obligations and available shortcuts",
                       "<p>" + escape(core["imported_shortcut"]) + "</p><ol>" + "".join(steps)
                       + "</ol><p>These arrows describe the supplied task inputs. Lean proof terms and measured reasoning difficulty have separate evidence.</p>",
                       "obligations")
    anchors = []
    for node in core["graph_anchors"]:
        label = node["id"].rsplit(".", 1)[-1]
        live = live_nodes.get(node["id"])
        if live is None:
            anchors.append("<li>" + escape(label) + " · frozen graph anchor</li>")
            continue
        target = "lean-graph/index.html?focus=" + quote(node["id"], safe="")
        anchors.append("<li>" + _link(route, target, label) + " · "
                       + _evidence_link(source_url, live["source"], "Lean source", line=live["line"]) + "</li>")
    proof = SOURCE + "reports/lean-course-hamiltonian-v1/"
    evidence = "<ul>" + "".join(anchors) + "</ul>"
    evidence += "<p>" + " · ".join([
        _evidence_link(source_url, proof + "comparison.json", "Independent semantic comparison"),
        _evidence_link(source_url, proof + "reference-checks.json", "Authored Lean replay receipt"),
    ]) + "</p>"
    evidence += "<p>Reference execution commit <code>" + escape(reference_commit) + "</code>.</p>"
    body += disclosure("Graph anchors and proof evidence", evidence, "evidence")
    write(route, core["title"], body + "</div>", core["question_summary"])


def publish(write, intro, section, disclosure, source_url, data_dir, record, live_nodes):
    if record is None:
        return None
    manifest, task_nodes, training = record
    routes = []
    hamiltonian = manifest.get("hamiltonian")
    if hamiltonian:
        body = intro("Hamiltonian proof companions",
                     "Two training views connect matrix calculations and counterexamples to the Lean graph. Start with either mathematical question.")
        body += '<p class="qcb-breadcrumb">' + _link(COMPANIONS, HUB + "lean/index.html", "Lean learning route") + " / Course v5</p>"
        body += '<div class="qcb-grid">' + "".join(
            card(core["title"], core["question_summary"], relpath(companion_route(core["core_id"]) + "index.html", COMPANIONS),
                 core["subject"] + " · " + core["construction_band"])
            for core in hamiltonian["companions"]
        ) + "</div>"
        body += '<p class="qcb-status-line">The original mathematical questions keep their core IDs and train split. D3 describes the construction route; model difficulty has yet to be measured.</p>'
        body += "<p>" + _link(COMPANIONS, DATA + "manifest.json", "Download the public manifest", download=True) + "</p>"
        write(COMPANIONS, "Hamiltonian proof companions", body + "</div>",
              "Two graph-grounded train companions for Hamiltonian block encoding and operator algebra.")
        routes.append(COMPANIONS + "index.html")
        for core in hamiltonian["companions"]:
            _companion(write, intro, section, disclosure, source_url, core, task_nodes[core["core_id"]],
                       live_nodes, hamiltonian["reference_commit"])
            routes.append(companion_route(core["core_id"]) + "index.html")

    sparse = manifest.get("sparse_address_assessment")
    if sparse:
        body = intro("Sparse-address assessment",
                     "An owner-sealed study of address arithmetic in banded sparse access.")
        body += '<p class="qcb-breadcrumb">' + _link(SPARSE, HUB + "run/assessment/index.html", "Assessment") + "</p>"
        body += f'<p class="qcb-inventory-line">{sparse["probe_count"]} propositions in {sparse["contrast_count"]} contrasts.</p>'
        body += '<p>The formal check is limited to the decision on each proposition. The questions and reference proofs are held by the evaluator. The library source is public and prior model exposure is unknown.</p>'
        profile = manifest.get("training_profile")
        if profile:
            counts = profile["counts"]
            body += section("Train with the matched profile",
                            f'<p>{counts["distinct_existing_cores"]} existing cores · {counts["nl_and_semantic_views"]} language and reasoning views · {counts["lean_views"]} Lean views.</p>'
                            '<p>Use this export to withhold the nearest public training cores in every view.</p><p>'
                            + _link(SPARSE, DATA + "train.json", "Download train examples and references", download=True)
                            + " · " + _link(SPARSE, DATA + "training-profile.json", "Download the profile", download=True)
                            + "</p>", "training-profile")
        body += '<p class="qcb-status-line">Trusted authored references have been checked. Model results and isolated candidate evaluation remain pending.</p>'
        write(SPARSE, "Sparse-address assessment", body + "</div>", "Public scope and the matched training profile for the owner-sealed sparse-address study.")
        routes.append(SPARSE + "index.html")

    folder = data_dir / PurePosixPath(DATA).name
    for name, value in _artifacts(manifest, training).items():
        write_json(folder / name, value)
    return {"routes": routes, "manifest_digest": digest(manifest)}


def _artifacts(manifest, training):
    artifacts = {"manifest.json": manifest}
    if training is not None:
        artifacts.update({"train.json": training, "training-profile.json": manifest["training_profile"]})
    return artifacts


def check(root, reader_manifest):
    record = publication(reader_manifest["source_commit"])
    folder = root / DATA
    summary = reader_manifest.get("lean_qa_v1")
    if record is None:
        if summary is not None or folder.exists():
            raise ValueError("Lean QA publication has no qualified source")
        return
    manifest, _, training = record
    routes = []
    if "hamiltonian" in manifest:
        routes = [COMPANIONS + "index.html", *(
            companion_route(core["core_id"]) + "index.html" for core in manifest["hamiltonian"]["companions"])]
    if "sparse_address_assessment" in manifest:
        routes.append(SPARSE + "index.html")
    artifacts = _artifacts(manifest, training)
    if (summary != {"routes": routes, "manifest_digest": digest(manifest)}
            or not set(routes) <= set(reader_manifest["routes"])
            or {p.name for p in folder.iterdir()} != set(artifacts)):
        raise ValueError("Lean QA publication differs from the qualified route and file inventory")
    for name, value in artifacts.items():
        if (folder / name).read_bytes() != encoded(value):
            raise ValueError("Lean QA artifact differs from its exact public projection: " + name)
