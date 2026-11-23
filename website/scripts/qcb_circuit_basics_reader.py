"""Reader and exact answer-separated downloads for the circuit foundations cohort."""
from html import escape
from pathlib import PurePosixPath
from posixpath import relpath
from urllib.parse import quote

from qcb_core import digest, read_json, write_json
from website.scripts.qcb_lean_downloads import encoded
from website.scripts.qcb_linear_circuit_reader import link, source_link
from website.scripts.qcb_math import render_prose
from website.scripts.qcb_navigation import card

HUB = "quantumcomputingbench/"
START = HUB + "lean/circuit-foundations/"
RUN = HUB + "run/course-v7/"
DATA = "data/quantumcomputingbench/lean-course-v7/"
SOURCE = "benchmarks/quantumcomputingbench/"
TOPICS = {
    "qcb-core-la-004": ("Register layout and block projection", "register-layout/", "Relate a flat basis index to two ordered registers and a selected signal branch."),
    "qcb-core-la-007": ("Linearity on a two-term state", "linearity/", "Identify which matrix columns or entries determine the action on a specified superposition."),
    "qcb-core-la-017": ("Reversible controlled flips", "controlled-flips/", "Analyze when a two-control bit flip is its own inverse, including repeated controls."),
    "qcb-core-la-018": ("When control and target overlap", "overlap/", "Check a concrete invalid control-target configuration and the limits of reversibility."),
}
SPLITS = {"train": "Train", "dev": "Development", "test_public": "Public test"}

# Question-side notation only. The content-bound independent review is checked
# before publication; dev/test notation must not insert worked solutions.
NOTATION = {
    "qcb-core-la-004": r"Write \(N=2^n\) for the system dimension and \(S=2^a\) for the signal dimension. A basis label is a pair \((s,i)\), where \(0\le s<S\) and \(0\le i<N\). Compare the two matrix representations on a fixed branch \(s\).",
    "qcb-core-la-007": r"Let \(A\in\mathbb C^{m\times n}\), with input basis vectors \(|\ell\rangle,|r\rangle\) and \(|\psi\rangle=a|\ell\rangle+b|r\rangle\). The question concerns the whole vector \(A|\psi\rangle\) and its output coordinate \((A|\psi\rangle)_k\).",
    "qcb-core-la-017": r"Let \(b\in\{0,1\}^N\) be a basis bitstring, with controls \(c_0,c_1\) and target \(t\), subject to \(c_0\ne t\) and \(c_1\ne t\). If \(F\) denotes the specified controlled flip, investigate \(F\circ F\) and the case \(c_0=c_1\).",
    "qcb-core-la-018": r"Write the stated raw bit update as \(F(c,t)=(c\oplus(ct),t)\), where \(\oplus\) is addition modulo two and \(ct\) is the ordinary product of the two bits. Is \(F\) still a reversible basis action?",
}


def check_notation(evidence, task_questions):
    review = read_json(evidence / "notation-review.json")
    inputs = read_json(evidence / "notation-review-input.json")
    expected_input = {"schema_version":"qcb.circuit_question_notation_review_input.v1",
                      "notation_digest":digest(NOTATION),
                      "question_digests":{key:digest(value) for key,value in task_questions.items()},
                      "views":[{"core_id":key,"source_question":task_questions[key],"notation":NOTATION[key]} for key in NOTATION]}
    rows = review.get("views", [])
    if (inputs != expected_input or review.get("input_digest") != digest(inputs)
            or review.get("schema_version") != "qcb.circuit_question_notation_review.v1"
            or review.get("notation_digest") != digest(NOTATION)
            or review.get("question_digests") != {key:digest(value) for key,value in task_questions.items()}
            or review.get("reviewer") != read_json(evidence / "comparison.json")["reviewer"]
            or len(rows) != len(TOPICS) or {row["core_id"] for row in rows} != set(TOPICS)
            or any(row["verdict"] != "accept" or row["introduces_answer_or_assumption"] is not False for row in rows)):
        raise ValueError("circuit-foundation notation needs its exact independent content review")
    return digest(review)


def route_for(core_id):
    return START + TOPICS[core_id][1]


def publication(commit):
    from qcb_course_circuit_basics import EVIDENCE
    if not (EVIDENCE / "reference-checks.json").is_file():
        return None
    from lean_course_v7 import load_course
    from lean_training_v7 import _export_from_registry
    from qcb_course_registry_v7 import _registry_from_qualified_course
    from qcb_lean_course import export_course

    course = load_course()
    plan, views, catalog, graph, coverage = course
    additions = {key: view for key, view in views.items() if view["task"]["core_id"] in TOPICS}
    status = coverage["reference_qualification"]["circuit_basics"]
    entries = [entry for entry in plan["entries"] if entry["core_id"] in TOPICS]
    if len(entries) != len(TOPICS) or {v["task"]["core_id"] for v in additions.values()} != set(TOPICS):
        raise ValueError("Course v7 requires all four qualified source views")
    notation_review = check_notation(EVIDENCE, {v["task"]["core_id"]:v["task"]["question"] for v in additions.values()})
    artifacts = {split + "-inputs.json": export_course(plan, views, catalog, graph, split=split)
                 for split in SPLITS}
    artifacts["train-references.json"] = _export_from_registry(*_registry_from_qualified_course(course))
    artifacts["coverage.json"] = coverage
    manifest = {
        "schema_version": "qcb.lean_course_v7_reader.v1", "source_commit": commit,
        "course_id": plan["course_id"], "course_digest": digest(plan),
        "catalog_hash": catalog["catalog_hash"], "snapshot_id": catalog["snapshot_id"],
        "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
        "additional_existing_core_views": len(entries), "model_performance_measured": False,
        "difficulty_empirically_calibrated": False, "blind_test": False,
        "public_source_exposure": "public_related_mechanisms; not_family_held_out",
        "reference_execution": "trusted_local_authored_reference",
        "reference_commit": status["reference_lineage"]["recorded_code_revision"],
        "question_notation_review_digest": notation_review,
        "entries": entries,
        "artifacts": {name: {"digest": digest(value), "contains_reference_answers": name == "train-references.json"}
                      for name, value in artifacts.items()},
    }
    return manifest, artifacts, additions, graph


def entry_links(route, record):
    if record is None:
        return ""
    targets = []
    if route in (HUB + "lean/", HUB + "course/", HUB + "course/d1/", HUB + "course/d2/"):
        targets.append((START + "index.html", "Circuit foundations · Course v7"))
    if route in (HUB + "run/", HUB + "run/agentic-lean/", HUB + "train/"):
        targets.append((RUN + "index.html", "Course v7 questions and training references"))
    for core_id in TOPICS:
        if route == HUB + "cores/" + core_id + "/":
            targets.append((route_for(core_id) + "index.html", "Explore the formal task and graph anchors"))
    return ('<p class="qcb-reading-options">' + " · ".join(link(route, *target) for target in targets) + "</p>") if targets else ""


def publish(write, intro, section, disclosure, source_url, data_dir, record, live_nodes):
    if record is None:
        return None
    manifest, artifacts, views, _ = record
    routes = [START + "index.html"]
    body = intro("Circuit foundations", "Begin with basis states and register order, then reason about linearity and the reversibility of controlled gates.")
    body += '<p class="qcb-breadcrumb">' + link(START, HUB + "lean/index.html", "Lean learning route") + " / Course v7</p>"
    body += '<div class="qcb-grid">' + "".join(card(TOPICS[e["core_id"]][0], TOPICS[e["core_id"]][2],
        relpath(route_for(e["core_id"]) + "index.html", START), e["difficulty"]["construction_band"] + " · " + SPLITS[e["split"]])
        for e in manifest["entries"]) + "</div>"
    body += "<p>" + link(START, RUN + "index.html", "Get course v7 questions and training references") + "</p>"
    body += '<p class="qcb-status-line">These four companions extend existing mathematical cores. Levels describe the constructed proof route, not measured model difficulty.</p>'
    write(START, "Circuit foundations", body + "</div>", "Four formal interfaces for foundational circuit reasoning.")

    for entry in manifest["entries"]:
        core_id = entry["core_id"]
        route, view = route_for(core_id), views[entry["view_id"]]
        task = view["task"]
        title, _, subtitle = TOPICS[core_id]
        body = intro(title, subtitle)
        body += '<p class="qcb-breadcrumb">' + link(route, START + "index.html", "Circuit foundations") + "</p>"
        body += '<p class="qcb-meta">' + escape(core_id.upper().removeprefix("QCB-CORE-")) + " · " + escape(entry["difficulty"]["construction_band"]) + " · " + SPLITS[entry["split"]] + "</p>"
        # Use the exact, source-reviewed question; no new unsourced formula or
        # repeated worked solution is inserted into development/test input.
        body += section("Question", render_prose(task["question"]) + render_prose(NOTATION[core_id]), "question")
        conditions = "<ul>" + "".join("<li>" + render_prose(x) + "</li>" for x in task["assumptions"] + task["conventions"]) + "</ul>"
        body += disclosure("Assumptions and notation", conditions, "setup")
        body += "<p>" + link(route, HUB + "cores/" + core_id + "/index.html#question", "Open the mathematical core and its reviewed reader material") + "</p>"
        body += "<p>" + (link(route, DATA + "train-references.json", "Download the separate training proofs") if entry["split"] == "train"
                           else "Development and public-test views are not included in the training reference export.") + "</p>"
        obligations = "<p>" + escape(view["formal_scope"]) + "</p><p>" + escape(entry["difficulty"]["imported_shortcut"]) + "</p><ol>"
        for node in task["nodes"]:
            dependencies = ", ".join(node["depends_on"]) or "No earlier obligation"
            obligations += "<li><strong>" + escape(node["id"]) + "</strong><p>Inputs: " + escape(dependencies) + "</p><pre><code>" + escape(node["target"]) + "</code></pre></li>"
        obligations += "</ol><p>The supplied graph is one proof decomposition, not measured model reasoning depth.</p>"
        body += disclosure("Exact Lean statements and proof dependencies", obligations, "obligations")
        anchors = []
        for key in entry["source_node_ids"]:
            node = live_nodes.get(key)
            if node is None:
                raise ValueError("Course v7 source anchor missing: " + key)
            anchors.append("<li>" + link(route, "lean-graph/index.html?focus=" + quote(key, safe=""), key.rsplit(".", 1)[-1])
                           + " · " + source_link(source_url, node["source"], node["line"], "Lean source") + "</li>")
        evidence_path = SOURCE + "reports/lean-course-circuit-basics-v1/"
        evidence = "<ul>" + "".join(anchors) + "</ul><p>" + " · ".join(source_link(source_url, evidence_path + name, 1, label)
            for name, label in (("source-and-exposure-review.json", "Independent mathematics and exposure review"), ("comparison.json", "Semantic comparison"), ("notation-review.json", "Notation review"),
                                ("reference-checks.json", "Authored proof replay"))) + "</p>"
        evidence += "<p>Lean checks the exact formal claim under the allowed axioms. Explanation quality must be assessed separately. Related public proofs and examples remain accessible.</p>"
        body += disclosure("Graph anchors and validation evidence", evidence, "evidence")
        write(route, title, body + "</div>", subtitle)
        routes.append(route + "index.html")

    coverage = artifacts["coverage.json"]
    body = intro("Run Lean course v7", "Select a question-only split. Training references are separate, and earlier course versions remain reproducible.")
    body += '<p class="qcb-breadcrumb">' + link(RUN, HUB + "run/index.html", "Run the benchmark") + " / Course v7</p>"
    body += '<p class="qcb-inventory-line">' + str(coverage["distinct_shared_cores"]) + " shared cores · " + str(coverage["task_anchor_node_count"]) + " frozen graph anchors.</p>"
    body += '<div class="qcb-grid">' + "".join(card(label, description, relpath(DATA + name, RUN), "JSON download") for name, label, description in (
        ("train-inputs.json", "Train questions", "Question-only practice inputs."),
        ("dev-inputs.json", "Development questions", "Tune the evaluation protocol separately."),
        ("test_public-inputs.json", "Public test questions", "Public evaluation inputs; no secrecy or exposure-free claim."),
        ("train-references.json", "Train references", "Authored proofs for train cores only."))) + "</div>"
    body += section("Report the evaluation condition", "<p>Choose whole-root submission (<code>root_only</code>) or stepwise submission (<code>proof_dag</code>), source-access condition, model and resource budget. Both submission modes expose the same supplied obligation graph; neither is a graph-withheld autonomous planning test. Record correctness, compiler calls, costs, and exposure separately. A successful theorem retrieval need not show independent discovery.</p>", "interpretation")
    body += disclosure("Coverage and identities", "<ul>" + "".join("<li>" + escape(b) + ": " + str(n) + " cores</li>" for b, n in sorted(coverage["by_construction_band"].items()))
        + "</ul><p>" + link(RUN, DATA + "coverage.json", "Exact coverage", download=True) + " · " + link(RUN, DATA + "manifest.json", "Manifest and evidence", download=True) + "</p>", "coverage")
    body += disclosure("Command-line entry points", '<pre><code>python benchmarks/quantumcomputingbench/scripts/lean_course_v7.py audit\npython benchmarks/quantumcomputingbench/scripts/lean_course_v7.py export --help\npython benchmarks/quantumcomputingbench/scripts/lean_training_v7.py --help\npython benchmarks/quantumcomputingbench/scripts/course_task_v7.py package --help\npython benchmarks/quantumcomputingbench/scripts/evaluate_course_v7.py --help</code></pre><p>Single-task packages bind the question, pinned environment, execution conditions and grading contract without the answers. They are task specifications, not container images. Untrusted model proof execution still requires an accepted isolated verifier. Authored replay is a separate trust condition.</p>', "commands")
    write(RUN, "Run Lean course v7", body + "</div>", "Versioned answer-free inputs, train-only reference export and coverage evidence.")
    routes.append(RUN + "index.html")
    folder = data_dir / PurePosixPath(DATA).name
    for name, value in {**artifacts, "manifest.json": manifest}.items():
        write_json(folder / name, value)
    return {"routes": routes, "manifest_digest": digest(manifest)}


def check(root, reader_manifest):
    record = publication(reader_manifest["source_commit"])
    summary = reader_manifest.get("lean_course_v7")
    folder = root / DATA
    known = {START + "index.html", RUN + "index.html", *(route_for(core) + "index.html" for core in TOPICS)}
    if record is None:
        if summary is not None or folder.exists() or known & set(reader_manifest["routes"]) or any((root / p).exists() for p in known):
            raise ValueError("Course v7 has no qualified source")
        return
    manifest, artifacts, _, _ = record
    routes = [START + "index.html", *(route_for(e["core_id"]) + "index.html" for e in manifest["entries"]), RUN + "index.html"]
    expected = {**artifacts, "manifest.json": manifest}
    if summary != {"routes": routes, "manifest_digest": digest(manifest)} or not set(routes) <= set(reader_manifest["routes"]) or {p.name for p in folder.iterdir()} != set(expected):
        raise ValueError("Course v7 reader differs from qualified inventory")
    for name, value in expected.items():
        if (folder / name).read_bytes() != encoded(value):
            raise ValueError("Course v7 download differs from qualified projection: " + name)
