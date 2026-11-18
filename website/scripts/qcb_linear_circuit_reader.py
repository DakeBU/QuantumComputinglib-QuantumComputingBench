"""Concise mathematical readers and exact public downloads for Lean course v6."""
from html import escape
from pathlib import PurePosixPath
from posixpath import relpath
from urllib.parse import quote

from qcb_core import digest, read_json, write_json
from website.scripts.qcb_lean_downloads import encoded
from website.scripts.qcb_math import render_prose
from website.scripts.qcb_navigation import card

HUB = "quantumcomputingbench/"
START = HUB + "lean/orientation-and-wires/"
RUN = HUB + "run/course-v6/"
DATA = "data/quantumcomputingbench/lean-course-v6/"
SOURCE = "benchmarks/quantumcomputingbench/"
TOPICS = {
    "qcb-core-la-006": ("Preserve columns, fix orientation", "orientation/",
                        "Use one free column to repair a determinant, then explain the fully prescribed boundary."),
    "qcb-core-la-013": ("Rename wires, preserve circuit meaning", "wires/",
                        "Connect wire labels to basis permutations and keep the order of a whole circuit."),
}


def link(route, target, label, *, download=False):
    return ('<a' + (' download' if download else '') + ' href="'
            + escape(relpath(target, route), quote=True) + '">' + escape(label) + '</a>')


def route_for(core_id):
    return START + TOPICS[core_id][1]


def source_link(source_url, path, line, label):
    url = source_url(path, line)
    if url is None:
        return escape(label) + ' · <code>' + escape(path) + '</code> (source link unavailable)'
    return '<a href="' + escape(url, quote=True) + '">' + escape(label) + '</a>'


def publication(commit):
    from qcb_course_linear_circuit import EVIDENCE, qualified
    if not (EVIDENCE / "reference-checks.json").is_file():
        return None
    from lean_course_v6 import load_course
    from lean_training_v6 import export
    from qcb_lean_course import export_course

    plan, views, catalog, graph, coverage = load_course()
    additions, status, _, _ = qualified()
    entries = [e for e in plan["entries"] if e["core_id"] in TOPICS]
    if len(entries) != len(TOPICS) or {v["task"]["core_id"] for v in additions.values()} != set(TOPICS):
        raise ValueError("Course v6 reader requires both exact qualified companions")
    if any(e["split"] != "train" for e in entries):
        raise ValueError("Course v6 companion solutions may only describe train tasks")
    artifacts = {split + "-inputs.json": export_course(plan, views, catalog, graph, split=split)
                 for split in ("train", "dev", "test_public")}
    artifacts["train-references.json"] = export()
    artifacts["coverage.json"] = coverage
    manifest = {
        "schema_version": "qcb.lean_course_v6_reader.v1", "source_commit": commit,
        "course_id": plan["course_id"], "course_digest": digest(plan),
        "catalog_hash": catalog["catalog_hash"], "snapshot_id": catalog["snapshot_id"],
        "new_mathematical_cores": 0, "new_canonical_formal_admissions": 0,
        "additional_existing_core_views": len(entries),
        "model_performance_measured": False, "difficulty_empirically_calibrated": False,
        "public_source_exposure": "public_related_mechanisms; not_a_blind_test",
        "reference_execution": "trusted_local_authored_reference",
        "reference_commit": status["reference_lineage"]["recorded_code_revision"],
        "entries": entries,
        "artifacts": {name: {"digest": digest(value), "contains_reference_answers": name == "train-references.json"}
                      for name, value in artifacts.items()},
    }
    return manifest, artifacts, additions, graph


def entry_links(route, record):
    if record is None:
        return ""
    targets = []
    if route in (HUB + "lean/", HUB + "lean/compose/", HUB + "course/", HUB + "course/d3/", HUB + "course/d4/"):
        targets.append((START + "index.html", "Orientation and wires · Course v6"))
    if route in (HUB + "run/", HUB + "run/agentic-lean/", HUB + "train/"):
        targets.append((RUN + "index.html", "Course v6 tasks and training references"))
    for core_id in TOPICS:
        if route == HUB + "cores/" + core_id + "/":
            targets.append((route_for(core_id) + "index.html", "Read the Lean training companion"))
    return ('<p class="qcb-reading-options">' + " · ".join(link(route, *t) for t in targets) + "</p>") if targets else ""


def mathematics(core_id, section, disclosure):
    """Reader mathematics is separate from the exact checked Lean propositions."""
    if core_id == "qcb-core-la-006":
        setup = r"Let \(V\in\mathbb R^{N\times r}\) satisfy \(V^\mathsf{T}V=I_r\). An injection \(e:\{0,\ldots,r-1\}\to\{0,\ldots,N-1\}\) gives the prescribed column positions. Assume an orthogonal completion \(U\in\mathbb R^{N\times N}\) exists, with \(U_{:,e(a)}=V_{:,a}\), and \(r<N\). The target is a completion in \(SO(N)\): orthogonal with determinant \(+1\)."
        steps = [
            r"Taking determinants of \(U^\mathsf{T}U=I_N\) gives \((\det U)^2=1\), hence \(\det U\in\{1,-1\}\). If the determinant is already \(+1\), keep \(U\).",
            r"Since \(e\) is injective and \(r<N\), choose \(j\notin\operatorname{range}(e)\). Let \(S_j\) be diagonal, with \(-1\) at position \(j\) and \(+1\) elsewhere. Then \(S_j^\mathsf{T}S_j=I_N\) and \(\det S_j=-1\).",
            r"If \(\det U=-1\), set \(W=US_j\). Right multiplication flips column \(j\) only. Thus every prescribed column is unchanged, while \(W^\mathsf{T}W=S_j^\mathsf{T}U^\mathsf{T}US_j=I_N\) and \(\det W=(-1)(-1)=1\).",
        ]
        boundary = r"When \(r=N>0\), prescribe every column of \(\operatorname{diag}(-1,1,\ldots,1)\). The resulting matrix is fixed and has determinant \(-1\), so no repair can preserve all columns. This is a failure of the universal guarantee: a fully prescribed matrix whose determinant is already \(+1\) needs no repair. At \(N=r=0\), the unique empty matrix has determinant \(1\)."
        meaning = "A spare direction lets an orthonormal frame extend with the requested orientation. This is a statement about real linear algebra used in state-preparation constructions; it does not supply a gate synthesis or a complexity bound."
    else:
        setup = r"There are \(N\) wires and basis labels \(b:\{0,\ldots,N-1\}\to\{0,1\}\). A wire permutation \(\sigma\) induces \(R_\sigma(b)(w)=b(\sigma^{-1}(w))\). Define the \(2^N\times2^N\) permutation matrix \(P_\sigma\) by \(P_\sigma|b\rangle=|R_\sigma(b)\rangle\). The first listed gate acts first: a list \(g_1,\ldots,g_t\) denotes \(U_t\cdots U_1\). Rename every target and control by the same \(\sigma\), preserving gate kinds and angles."
        steps = [
            r"For one renamed gate, \(U_k'=P_\sigma U_kP_\sigma^{-1}\). Both input and output basis labels change, with \(R_\sigma(b)(\sigma(w))=b(w)\). Single-wire gates still act on the corresponding bit; a controlled gate reads the renamed control and updates the renamed target, preserving all other bits.",
            r"For two stages, \((P_\sigma U_2P_\sigma^{-1})(P_\sigma U_1P_\sigma^{-1})=P_\sigma U_2(P_\sigma^{-1}P_\sigma)U_1P_\sigma^{-1}=P_\sigma(U_2U_1)P_\sigma^{-1}\). Induction preserves the order and cancels every internal pair. The empty list denotes the identity, so it obeys the same equation.",
            r"The entry formula is \((P_\sigma MP_\sigma^{-1})_{a,b}=M_{R_\sigma^{-1}(a),R_\sigma^{-1}(b)}\). This connects the basis-state equation to the library's matrix reindexing operation; it is not an extra physical gate.",
        ]
        boundary = r"Changing only outputs gives \(T(M)=P_\sigma M\), which need not preserve multiplication. For a nontrivial swap of two wires, \(P_\sigma^2=I\ne P_\sigma\). Two identity stages then give \(T(I)T(I)=I\), while \(T(II)=P_\sigma\). Such a wire swap needs \(N\ge2\). For \(N=1\) the wire permutation is trivial; \(N=0\) has one empty bitstring and a \(1\times1\) identity, not a zero-dimensional state space. An arbitrary permutation of computational basis states is also more general than a wire permutation: a bit flip on one wire is not a wire relabeling. Conjugating a noncommuting rotation by that bit flip changes its operator while an unchanged one-wire gate list does not. A nonzero rotation angle alone is insufficient to guarantee noncommutation; an explicit witness is needed."
        boundary += r" Concretely, \(X=\begin{pmatrix}0&1\\1&0\end{pmatrix}\) satisfies \(XR_Y(\theta)X=R_Y(-\theta)\) for \(R_Y(\theta)=\begin{pmatrix}\cos(\theta/2)&-\sin(\theta/2)\\\sin(\theta/2)&\cos(\theta/2)\end{pmatrix}\). At \(\theta=\pi\), the original matrix is \(\begin{pmatrix}0&-1\\1&0\end{pmatrix}\), while conjugation gives \(\begin{pmatrix}0&1\\-1&0\end{pmatrix}\). They differ as exact operators, which is the equality notion used here."
        boundary += " These two matrices differ only by a global sign, so this witness does not assert physical distinguishability modulo global phase."
        meaning = "Consistent reindexing preserves circuit meaning under a change of labels. Physically moving qubits on hardware is a different construction and can require SWAP gates; this theorem gives no free routing operation."
    body = section("Objects and assumptions", render_prose(setup), "setup")
    body += section("Why this matters", "<p>" + escape(meaning) + "</p>", "meaning")
    body += disclosure("Follow the mathematical argument", "<ol>" + "".join("<li>" + render_prose(s) + "</li>" for s in steps) + "</ol>", "derivation")
    body += disclosure("Check the boundaries and counterexamples", render_prose(boundary), "boundaries")
    return body


def publish(write, intro, section, disclosure, source_url, data_dir, record, live_nodes):
    if record is None:
        return None
    manifest, artifacts, views, graph = record
    routes = []
    body = intro("Orientation and wire order", "Two training companions connect quantum linear algebra to circuit semantics. Begin with the objects, follow the argument, then try the Lean obligations.")
    body += '<p class="qcb-breadcrumb">' + link(START, HUB + "lean/index.html", "Lean learning route") + " / Course v6</p>"
    body += '<div class="qcb-grid">' + "".join(card(TOPICS[e["core_id"]][0], TOPICS[e["core_id"]][2],
              relpath(route_for(e["core_id"]) + "index.html", START), e["difficulty"]["construction_band"] + " · Train") for e in manifest["entries"]) + "</div>"
    body += '<p>' + link(START, RUN + "index.html", "Get the cumulative course tasks") + '</p>'
    body += '<p class="qcb-status-line">These are Lean views of existing mathematical cores. Construction levels describe the authored route; model difficulty has not been measured.</p>'
    write(START, "Orientation and wire order", body + "</div>", "Two Lean training companions with mathematical explanations and explicit boundary checks.")
    routes.append(START + "index.html")
    for entry in manifest["entries"]:
        core_id = entry["core_id"]
        view, route = views[entry["view_id"]], route_for(core_id)
        body = intro(TOPICS[core_id][0], TOPICS[core_id][2])
        body += '<p class="qcb-breadcrumb">' + link(route, START + "index.html", "Orientation and wire order") + "</p>"
        body += '<p class="qcb-meta">' + escape(core_id.upper().removeprefix("QCB-CORE-")) + " · " + escape(entry["difficulty"]["construction_band"]) + " · Train</p>"
        body += "<p>" + link(route, HUB + "cores/" + core_id + "/index.html#question", "Try the full mathematical question") + "</p>"
        body += mathematics(core_id, section, disclosure)
        obligations = "<p>" + escape(view["formal_scope"]) + "</p><p>" + escape(entry["difficulty"]["imported_shortcut"]) + "</p><ol>"
        for node in view["task"]["nodes"]:
            dependencies = ", ".join(node["depends_on"]) or "No earlier obligation"
            obligations += "<li><strong>" + escape(node["id"]) + "</strong><p>Inputs: " + escape(dependencies) + "</p><pre><code>" + escape(node["target"]) + "</code></pre></li>"
        obligations += "</ol><p>This is the supplied obligation graph, not a measured model reasoning depth. Imported shortcuts for individual subclaims are available in the public library.</p>"
        body += disclosure("Inspect the exact Lean obligations", obligations, "obligations")
        anchors = []
        for key in entry["source_node_ids"]:
            node = live_nodes.get(key)
            if node is None:
                raise ValueError("Course v6 source anchor missing from live graph: " + key)
            anchors.append("<li>" + link(route, "lean-graph/index.html?focus=" + quote(key, safe=""), key.rsplit(".", 1)[-1])
                           + ' · ' + source_link(source_url, node["source"], node["line"], "Lean source") + '</li>')
        evidence = "<ul>" + "".join(anchors) + "</ul><p>"
        proof_dir = SOURCE + "reports/lean-course-linear-circuit-v1/"
        evidence += " · ".join(source_link(source_url, proof_dir + path, 1, label) for path, label in (
            ("comparison.json", "Semantic comparison"), ("reference-checks.json", "Authored proof replay"),
            ("exposure-review.json", "Public-source relationships"))) + "</p>"
        evidence += "<p>Kernel checking certifies the exact formal proposition under its allowed axioms. The mathematical explanation and its alignment require separate review. It does not establish that a model learned the domain.</p>"
        body += disclosure("Inspect graph anchors and evidence", evidence, "evidence")
        write(route, TOPICS[core_id][0], body + "</div>", TOPICS[core_id][2])
        routes.append(route + "index.html")

    coverage = artifacts["coverage.json"]
    body = intro("Run Lean course v6", "Choose a question-only split, or the separate public training references. Earlier course versions remain reproducible.")
    body += '<p class="qcb-breadcrumb">' + link(RUN, HUB + "run/index.html", "Run the benchmark") + " / Course v6</p>"
    body += '<p class="qcb-inventory-line">' + str(coverage["distinct_shared_cores"]) + " shared mathematical cores · " + str(coverage["task_anchor_node_count"]) + " frozen graph anchors.</p>"
    body += '<div class="qcb-grid">' + "".join(card(label, description, relpath(DATA + name, RUN), "JSON download") for name, label, description in (
        ("train-inputs.json", "Train questions", "Practice inputs without reference proofs."),
        ("dev-inputs.json", "Development questions", "A separate split for protocol development."),
        ("test_public-inputs.json", "Public test questions", "Public evaluation inputs; not a secret or exposure-free test."),
        ("train-references.json", "Training references", "Authored proofs for train cores only."))) + "</div>"
    body += section("Interpret a result", "<p>Report correctness together with the model, task mode, source access, resource budget and exposure profile. The new wire-renaming material shares public mechanisms with existing permutation tasks. Course v6 is a public curriculum and source-assisted evaluation resource; it is not a family-held-out assessment profile.</p><p>Separate statement understanding, local algebra, composition and boundary reasoning. A successful imported theorem call alone does not demonstrate all four.</p>", "interpretation")
    body += disclosure("Construction levels and coverage", "<ul>" + "".join("<li>" + escape(band) + ": " + str(count) + " cores</li>" for band, count in sorted(coverage["by_construction_band"].items())) + "</ul><p>These levels are provisional mathematical assessments. Core and graph counts do not establish independent question capacity or mastery.</p><p>" + link(RUN, DATA + "coverage.json", "Download exact coverage", download=True) + " · " + link(RUN, DATA + "manifest.json", "Download identities and evidence", download=True) + "</p>", "coverage")
    body += disclosure("Command-line entry points", '<pre><code>python benchmarks/quantumcomputingbench/scripts/lean_course_v6.py audit\npython benchmarks/quantumcomputingbench/scripts/lean_course_v6.py export --help\npython benchmarks/quantumcomputingbench/scripts/lean_training_v6.py --help\npython benchmarks/quantumcomputingbench/scripts/evaluate_course_v6.py --help</code></pre><p>Real model evaluation requires the accepted isolated verifier profile. Authored local reference replay is a separate operation.</p>', "commands")
    write(RUN, "Run Lean course v6", body + "</div>", "Cumulative course v6 question-only splits, separate train proofs and reproducible entry points.")
    routes.append(RUN + "index.html")
    folder = data_dir / PurePosixPath(DATA).name
    for name, value in {**artifacts, "manifest.json": manifest}.items():
        write_json(folder / name, value)
    return {"routes": routes, "manifest_digest": digest(manifest)}


def check(root, reader_manifest):
    record = publication(reader_manifest["source_commit"])
    summary = reader_manifest.get("lean_course_v6")
    folder = root / DATA
    if record is None:
        known_routes = {START + "index.html", RUN + "index.html",
                        *(route_for(core_id) + "index.html" for core_id in TOPICS)}
        if (summary is not None or folder.exists()
                or known_routes & set(reader_manifest["routes"])
                or any((root / route).exists() for route in known_routes)):
            raise ValueError("Course v6 reader has no qualified source")
        return
    manifest, artifacts, _, _ = record
    routes = [START + "index.html", *(route_for(e["core_id"]) + "index.html" for e in manifest["entries"]), RUN + "index.html"]
    expected = {**artifacts, "manifest.json": manifest}
    if (summary != {"routes": routes, "manifest_digest": digest(manifest)}
            or not set(routes) <= set(reader_manifest["routes"])
            or {p.name for p in folder.iterdir()} != set(expected)):
        raise ValueError("Course v6 reader differs from its qualified inventory")
    for name, value in expected.items():
        if (folder / name).read_bytes() != encoded(value):
            raise ValueError("Course v6 download differs from its qualified projection: " + name)
