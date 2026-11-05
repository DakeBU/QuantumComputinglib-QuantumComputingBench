#!/usr/bin/env python3
"""Append-only c29 AUTHOR metadata successor after specifically authorized static feedback.

Original source trio and v1 artifacts remain immutable. This author now has
read the pinned phase-2 static report, not decoder/CI/other review artifacts.
No Lean, Git, network, canonical changes or admission checker calls.
"""
from __future__ import annotations
import argparse
import base64
import copy
import json
import re
import runpy
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PREFIX = "reviews/publication/cubic-source-c29/metadata-v2/"
OLD_PREFIX = "reviews/publication/cubic-source-c29/"
REPORT_SHA = "ccdcd6cdb0d40d4645ed4d64c9381ffc9121c88309be4493979b7a35156a4f4e"
V1_MANIFEST_SHA = "555194f534a537e7d68c450caa8605a3d4a2a37dc02d5ac39f97422b28d0fd0c"
V1_GENERATOR_SHA = "1700097c91fb3f78d7ed6eafe10472a4bfc8d1211b8147660fe32014d90d784c"
WIP = "AUTHOR_WIP_NOT_ADMITTED"


def env(previous):
    source = (previous/"author-package-build.py").read_bytes()
    import hashlib
    assert hashlib.sha256(source).hexdigest() == V1_GENERATOR_SHA
    return runpy.run_path(str(previous/"author-package-build.py"), run_name="c29_v1_author_format_readonly")


def raw_trim_end(masked, start, end):
    while end > start and masked[end-1].isspace():
        end -= 1
    return end


def exact_structure(v1, relative, root):
    """Extract actual field source, stopping at top-level namespace/ambient commands."""
    raw_block = root["source_block"]
    masked = v1["mask_comments"](raw_block)
    header, body = v1["split_definition"](masked)
    body_at = len(masked)-len(body)
    assert masked[body_at:].startswith("where")
    limit_match = re.search(
        r"(?m)^(?:namespace|end|open|section|noncomputable section|set_option|variable|universe|scoped|local|notation|attribute|deriving)\b",
        masked[body_at:])
    limit = body_at+limit_match.start() if limit_match else len(masked)
    limit = raw_trim_end(masked, body_at, limit)
    matches = list(re.finditer(r"(?m)^  (?P<name>[A-Za-z_][\w']*)\s*:", masked[body_at:limit]))
    fields = []
    for index, match in enumerate(matches):
        start = body_at+match.start()
        end = body_at+matches[index+1].start() if index+1 < len(matches) else limit
        end = raw_trim_end(masked,start,end)
        field = match["name"]
        value = raw_block[start:end].strip()
        assert not re.search(r"(?m)^(namespace|end|deriving)\b", value)
        fields.append({"name":field,"exact_source_field_region":value,
                       "source_block_character_range":[start,end],
                       "source_path":relative,"extractor":"v2 actual structure region, no ambient namespace/deriving tail"})
    return raw_block[:limit], raw_block[body_at:limit], fields


def refine_bundles(v1, repo, data):
    catalog = {}
    changes = []
    for qualified, old in data.items():
        relative = old["provider_path"]
        raw = (repo/relative).read_bytes()
        roots = v1["inventory"](relative,raw)
        selected = [r for r in roots if r["name"]==qualified]
        assert len(selected)==1, qualified
        root = selected[0]
        result = copy.deepcopy(old)
        if root["kind"]=="structure":
            exact, members, fields = exact_structure(v1,relative,root)
            old_fields = {f["name"]:f for f in old["field_audit"]}
            assert set(old_fields)=={f["name"] for f in fields}, qualified
            result["full_navigational_declaration_block"] = old["exact_definition_region"]
            result["exact_definition_region"] = exact
            result["exact_structure_members_region"] = members
            new_fields = []
            for field in fields:
                original = old_fields[field["name"]]
                revised = dict(original)
                revised.update(field)
                if field["name"]=="angleConvention" and qualified.endswith(".ExpandedControlledRyWorkspaceReadonlyWitness"):
                    revised["classification"] = "SOURCE"
                    revised["reason"] = (
                        "Proof of the transparent universal supplied-tier angle law, not type/data. "
                        "SOURCE inside a supplied readonly witness; actual producers may discharge this field internally."
                    )
                    revised["nested_logical_expansion"] = [
                        {"definition":"expandedControlledRyUsesCubicAngleTransparent n workspaceQubits",
                         "unfolds_to":"forall tier : StandardRyCleanEntryScalarTier, expandedRyCleanEntryForCubicAmplitudes tier n",
                         "classification":"SOURCE universal proposition"},
                        {"definition":"expandedRyCleanEntryForCubicAmplitudes tier n",
                         "unfolds_to":"forall j : Fin (gridSize n), tier.cleanEntry (tier.thetaForAmplitude (tier.ratAmplitude (cubicAmplitude n j))) = tier.ratAmplitude (cubicAmplitude n j)",
                         "classification":"SOURCE all-index equality"},
                        {"supplied_tier_law":"cleanEntry_of_range",
                         "guards":"0<=a AND a<=1, both produced for a=cubicAmplitude n j by range lemmas",
                         "classification":"SOURCE law of supplied scalar tier; not physical Ry semantics"}
                    ]
                    revised["available_internal_producer"] = {
                        "name":"QuantumBlockEncoding.CubicDiagonalOracle.fixedDenomControlledRyRouteTransparent",
                        "uses":"expandedRyCleanEntryForCubicAmplitudes_of_standardTier and internally proved cubic range",
                        "scope":"Produces the transparent angle proposition only; no full readonly witness, actual rotation, cleanup or physical circuit is produced here.",
                        "evidence_layer":"Actual static source; no compile evidence from this author"}
                    changes.append({"finding":"F1","bundle":qualified,"field":field["name"],
                                    "old_classification":original["classification"],"new_classification":"SOURCE"})
                if original["exact_source_field_region"] != revised["exact_source_field_region"]:
                    changes.append({"finding":"F4","bundle":qualified,"field":field["name"],
                                    "old_sha256":v1["sha"](original["exact_source_field_region"].encode()),
                                    "new_sha256":v1["sha"](revised["exact_source_field_region"].encode()),
                                    "change":"End at real field boundary, exclude top-level ambient commands or navigational trailing text."})
                new_fields.append(revised)
            result["field_audit"] = new_fields
            result["exact_field_boundary_authority"] = "AUTHOR v2 lexical correction after authorized F4 feedback; no elaborated field/type certificate."
        catalog[qualified] = result
    return catalog, changes


def refine_graph(graph):
    result = copy.deepcopy(graph)
    sg = result["views"]["source-construction-graph"]
    old_cases = sg.pop("guarded_OR_cases")
    sg["legacy_case_record_sha256_retained_in_v1"] = "See predecessor manifest; v1 is immutable."
    case_by_id = {item["id"]:item for item in old_cases}
    typed = []
    specifications = [
        ("rank-one-column","CASE_SPLIT","result:rank-one-adapter","For every fixed row/column, prove the correct rank-one contract-to-target entry under the exhaustive column guards."),
        ("Householder-validity","BOUNDARY_PARTITION","result:reflection","On-locus arm supports reflection claims; off-locus arm only retains total formula and cannot prove reflection."),
        ("directsum-system","CASE_SPLIT","result:directsum","For every pair of full indices, same-branch and different-branch identities jointly establish the universal row/column theorem."),
        ("fiber-membership","CASE_SPLIT","result:fiber","Each index either belongs to the chosen finite branch fiber or contributes a proved zero term."),
        ("modular-wrap","CASE_SPLIT","result:modular-cleanup","For w,p<M, split w+p<M or M<=w+p<2M; both guarded proofs establish one inverse identity."),
    ]
    for key,kind,head,meaning in specifications:
        old = case_by_id[key]
        item = {k:v for k,v in old.items() if k not in ("join","meaning")}
        item.update(kind=kind,logic="GUARDED_UNIVERSAL_PROOF_CASES",heads=[head],
                    semantics=meaning,alternative_sufficient_constructions=False,
                    branch_obligations_jointly_required=True,status="AUTHOR_PROVISIONAL")
        if key=="Householder-validity":
            item["logic"] = "DOMAIN_BOUNDARY_NOT_TWO_REFLECTION_PROOFS"
            item["branch_obligations_jointly_required"] = False
            item["branch_heads"] = [
                {"guard":"dot(v,v)=1 AND v0!=1","head":"result:reflection","claim":"Guarded reflection/clean entry."},
                {"guard":"outside this locus","head":"boundary:total-Householder-formula","claim":"Formula is defined by total Rat division; no reflection theorem."}]
        typed.append(item)
    typed.append({
        "id":"four-square-target","kind":"TARGET_DISPATCH","logic":"DIFFERENT_TARGETS_NOT_SUFFICIENT_OR",
        "branches":[{"guard":"target X","heads":["result:completion-linear"],"formula":"N^2-j^2 residual"},
                    {"guard":"target D","heads":["result:completion-cubic"],"formula":"N^6-j^6 residual"}],
        "alternative_sufficient_constructions":False,"status":"AUTHOR_PROVISIONAL"})
    typed += [
        {"id":"cubic-zero-register-boundary","kind":"BOUNDARY_PARTITION","heads":["result:targets"],
         "parameter":"n : Nat","guards":["n=0","n>0"],"exhaustive_for_this_parameter":True,
         "branches":[{"guard":"n=0","claim":"N=M=1; j=p=w=0; v=0; normalized SP target undefined."},
                     {"guard":"n>0","claim":"Nonempty finite grid formulas valid; normalized SP still requires its separate theorem."}],
         "alternative_sufficient_constructions":False,"status":"AUTHOR_PROVISIONAL"},
        {"id":"euclidean-empty-dimension-boundary","kind":"BOUNDARY_PARTITION","heads":["result:euclidean-error"],
         "parameter":"generic error dimension m : Nat","guards":["m=0","m>0"],"exhaustive_for_this_parameter":True,
         "branches":[{"guard":"m=0","claim":"Both finite sums empty; E still requires epsilon>=0."},
                     {"guard":"m>0","claim":"All-input diagonal error proof uses row terms under supplied entry bounds."}],
         "alternative_sufficient_constructions":False,"status":"AUTHOR_PROVISIONAL"}
    ]
    sg["typed_guarded_partitions"] = typed
    sg["construction_alternatives"] = []
    nodes = sg["nodes"]
    def node(identity, kind, formula, status="AUTHOR_PROVISIONAL"):
        assert identity not in {n["id"] for n in nodes}
        nodes.append({"id":identity,"kind":kind,"formula":formula,"status":status})
    node("boundary:total-Householder-formula","boundary-only","Total rational formula outside theorem guard; no second reflection construction.")
    node("target:rank-one-physical","OPEN-PHYSICAL-TARGET","An actually denoted unitary family whose alpha=N clean block equals O, with all rejection/workspace/phase semantics certified.","OPEN_NOT_PROVED")
    # Distinct routes retain each actual full uncertainty; none is promoted by its syntax.
    route_edges = []
    for route,syntax in (("arithmetic-wrapper","10-label arithmetic wrapper, not seven-label middle block alone"),
                         ("counting","eight-label separate-reject counting route with row/threshold path registers")):
        fields = {
            "transcript-denotation":"Actual coherent denotation of "+syntax+" on all input/workspace branches.",
            "unitarity":"Actual unitary semantics of every gate/oracle/composed transcript, not an opaque/name assertion.",
            "nonzero-column-rejection":"Nonzero input columns have zero clean block; separate reject information cannot be erased by cleanup.",
            "workspace-cleanup":"Clean extracted branch and every auxiliary/garbage register agree with the frozen projection; desired output row is preserved.",
            "phase-and-normalization":"Relative signs/phases and amplitude normalization agree exactly with a_j/N; arithmetic transduction or Hadamard sandwich analysis as appropriate.",
            "entry-extraction":"Derive the scaled first-column and every other-column-zero equations from actual denotation, not assume the rank-one target contract.",
        }
        tails = ["result:targets","result:range-norm","result:label-accounting"]
        if route=="counting":
            tails.append("result:threshold")
        for key,formula in fields.items():
            nid="OPEN:"+route+":"+key
            node(nid,"OPEN-ROUTE-OBLIGATION",formula,"OPEN_NOT_PROVED")
            tails.append(nid)
        edge={"id":"route:rank-one-"+route,"logic":"AND","tails":tails,
              "heads":["target:rank-one-physical"],"status":"OPEN_PROPOSED_SUFFICIENT_CONSTRUCTION_NOT_A_PROOF",
              "source_region":"S03","formal_support":"Transcript/accounting/arithmetic leaves only; these OPEN tails have no completed denotation producer.",
              "not_final_finite_bit_success":"Even a physical exact clean block still needs resource/finite-bit refinement and normalized-SP/success consumers if requested."}
        route_edges.append(edge)
    sg["AND_hyperedges"] += route_edges
    sg["construction_alternatives"].append({
        "id":"rank-one-construction-routes","kind":"SUFFICIENT_CONSTRUCTION_OR","logic":"OR",
        "heads":["target:rank-one-physical"],"route_edge_ids":[edge["id"] for edge in route_edges],
        "semantics":"Each alternative requires its entire AND tail; neither current route is closed.",
        "status":"ALL_ROUTES_OPEN","not_case_split":True})
    # Retain the previous physical-D alternatives, now typed as routes with explicit open tails.
    node("target:diagonal-physical","OPEN-PHYSICAL-TARGET","Uniform actual unitary/circuit block encoding of D with a matched implementation tier.","OPEN_NOT_PROVED")
    d_routes=[
        ("Householder",["result:matrix-D","SOURCE_GAP-FOUR-SQUARE-PRODUCER","SOURCE_GAP-CONTROLLED-GATE-SYNTHESIS","SOURCE_GAP-FAMILY-EXECUTABLE"]),
        ("expanded-arithmetic",["result:fixed-payload","result:scalar-specialization","result:modular-cleanup","SOURCE_GAP-COMMON-BACKEND-COMPOSITION","SOURCE_GAP-OPAQUE-CLEANUP-EXTRACTION","SOURCE_GAP-CONTROLLED-GATE-SYNTHESIS","SOURCE_GAP-FAMILY-EXECUTABLE"]),
        ("QSVT",["result:matrix-X","result:qsvt-local","SOURCE_GAP-QSVT-SUPPLY","SOURCE_GAP-CONTROLLED-GATE-SYNTHESIS","SOURCE_GAP-FAMILY-EXECUTABLE"]),
    ]
    for route,tails in d_routes:
        sg["AND_hyperedges"].append({"id":"route:diagonal-"+route,"logic":"AND","tails":tails,
            "heads":["target:diagonal-physical"],"status":"OPEN_PROPOSED_SUFFICIENT_CONSTRUCTION_NOT_A_PROOF",
            "source_region":"S12","all_tail_requirements_joint":True})
    sg["construction_alternatives"].append({
        "id":"diagonal-construction-routes","kind":"SUFFICIENT_CONSTRUCTION_OR","logic":"OR",
        "heads":["target:diagonal-physical"],"route_edge_ids":["route:diagonal-"+route for route,_ in d_routes],
        "status":"ALL_ROUTES_OPEN","semantics":"Householder, actual expanded arithmetic or full QSVT supply are alternatives, not individually closed by one existing leaf."})
    # Literal two-coordinate producer and all its genuine guards.
    node("data:circle-coordinates","TYPING-DATA","Supplied functions q,r : Fin N -> Rat.")
    node("premise:circle-equation","SOURCE-CONDITIONAL-GUARD","For every j, q_j^2+r_j^2=1.")
    node("premise:circle-nontrivial","SOURCE-CONDITIONAL-GUARD","For every j, q_j!=1; this is not implied by the circle equation.")
    node("result:circle-literal-vector","literal-definition","v_j=(q_j,r_j,0,0,0,0,0,0), with literal ordered rational coordinates.")
    node("result:circle-unit","produced-local-fact","For every j, dot8(v_j,v_j)=1, produced by expanding the literal vector and hcircle.")
    node("result:circle-clean-coordinate","produced-local-fact","For every j, v_j[0]=q_j, produced by literal coordinate evaluation.")
    node("result:circle-nontrivial-coordinate","produced-local-fact","For every j, v_j[0]!=1 from the clean-coordinate identity AND q_j!=1.")
    producers=[
        ("circle-literal",["data:circle-coordinates"],["result:circle-literal-vector"]),
        ("circle-unit",["result:circle-literal-vector","premise:circle-equation"],["result:circle-unit"]),
        ("circle-coordinate",["result:circle-literal-vector"],["result:circle-clean-coordinate"]),
        ("circle-nontrivial-coordinate",["result:circle-clean-coordinate","premise:circle-nontrivial"],["result:circle-nontrivial-coordinate"]),
    ]
    for key,tails,heads in producers:
        sg["AND_hyperedges"].append({"id":"construction:"+key,"logic":"AND","tails":tails,"heads":heads,
             "status":"AUTHOR_PROVISIONAL","source_region":"S08","actual_source_anchor":"CubicStatePreparation.lean:2635–2651"})
    circle=next(edge for edge in sg["AND_hyperedges"] if edge["id"]=="construction:circle-branch")
    circle["tails"]=["data:circle-coordinates","result:circle-literal-vector","premise:circle-equation",
        "result:circle-unit","result:circle-clean-coordinate","premise:circle-nontrivial",
        "result:circle-nontrivial-coordinate","result:reflection","result:fiber","result:clean-diagonal"]
    circle["guard_discharge"]={"premise:unit-branch":["result:circle-unit","result:circle-nontrivial-coordinate"],
        "premise:branch-value":["result:circle-clean-coordinate"],
        "interpretation":"Instantiate the generic clean-diagonal theorem with this actual supplied vector; unit norm is produced from hcircle, not an extra independent constructor assumption."}
    circle["scope"]="Exactly supplied q,r satisfying all circle/nontrivial guards; no approximation quality or physical gate theorem follows."
    sg["status"]="AUTHOR_PROVISIONAL_V2_AFTER_AUTHORIZED_STATIC_FEEDBACK"
    sg["review_feedback_read"]=True
    # Path-only successor updates; no fabricated independent transport.
    result["views"]["compressed-quantum-spine"]["lossless_drilldown"]=[
        PREFIX+"author-source-coverage.json",PREFIX+"author-formal-context.json"]
    result["status"]="AUTHOR_PROVISIONAL_V2_NOT_INDEPENDENT_TOPOLOGY"
    return result


def build(repo, out, previous, feedback):
    v1=env(previous)
    sha,emit,emit_raw,record=(v1[k] for k in ("sha","emit","emit_raw","file_record"))
    # Only own immutable packet; no decoder, CI or additional independent output.
    assert sha((previous/"outputs-manifest.json").read_bytes())==V1_MANIFEST_SHA
    predecessor_manifest=json.loads((previous/"outputs-manifest.json").read_bytes())
    for item in predecessor_manifest["artifacts"]:
        actual=(previous/item["path"]).read_bytes()
        assert sha(actual)==item["sha256"] and len(actual)==item["bytes"]
    old_freeze=json.loads((previous/"metadata-freeze.json").read_bytes())
    pinned=old_freeze["whole_ambient_binding_inputs"]+old_freeze["strict_config_and_direct_external_inputs"]
    v1["assert_current"](repo,pinned)
    feedback_raw=feedback.read_bytes()
    assert sha(feedback_raw)==REPORT_SHA
    assert "F1 —" in feedback_raw.decode() and "F5 —" in feedback_raw.decode()
    original_copies=[]
    for name in v1["ORIGINAL"]:
        raw=(previous/name).read_bytes()
        assert sha(raw)==v1["ORIGINAL"][name]
        emit_raw(out,name,raw)
        original_copies.append(record(out/name,name))
    # Byte-identical transport, not an author-written independent verdict.
    emit_raw(out,"authorized-static-feedback.md",feedback_raw)
    emit_raw(out,"author-formal-context.json",(previous/"author-formal-context.json").read_bytes())
    emit_raw(out,"cubic-grid-rational-operators-and-contracts.md",(previous/"source-only.md").read_bytes())
    formal=json.loads((out/"author-formal-context.json").read_bytes())
    packet=json.loads((previous/"author-decoder-packet.json").read_bytes())
    packet["formal_context_path"]=PREFIX+"author-formal-context.json"
    emit(out,"author-decoder-packet.json",packet)
    context_hash=sha((out/"author-formal-context.json").read_bytes())
    packet_hash=sha((out/"author-decoder-packet.json").read_bytes())
    audit=json.loads((previous/"author-binder-definition-audit.json").read_bytes())
    coverage=json.loads((previous/"author-source-coverage.json").read_bytes())
    refined,changes=refine_bundles(v1,repo,audit["project_owned_bundle_expansions"])
    audit["project_owned_bundle_expansions"]=refined
    coverage["project_owned_bundle_expansions"]=copy.deepcopy(refined)
    provenance={
        "stage":"AUTHOR_METADATA_V2_AFTER_AUTHORIZED_STATIC_FEEDBACK",
        "feedback_sha256":REPORT_SHA,
        "author_has_read_this_static_review":True,
        "author_claims_blindness_to_this_feedback":False,
        "decoder_or_CI_or_other_independent_review_read":False,
        "new_independent_review_of_v2":"PENDING",
        "original_source_and_reviewer_phase1_mutated":False,
        "all_claims_still_AUTHOR_WIP":True}
    audit["successor_provenance"]=provenance
    coverage["successor_provenance"]=provenance
    # Source named declarations remain exactly the same; only metadata views improve.
    for obj in (audit,coverage):
        for obligation in obj["whole_module_inventory"]:
            if obligation.get("kind")=="structure" or obligation["name"] in refined:
                bundle=refined.get(obligation["name"])
                if bundle and "exact_structure_members_region" in bundle:
                    obligation["definition_audit"]["expanded_structure_members"]=bundle["exact_structure_members_region"]
    emit(out,"author-binder-definition-audit.json",audit)
    emit(out,"author-source-coverage.json",coverage)
    graph=refine_graph(json.loads((previous/"author-graph-views.json").read_bytes()))
    graph["coverage_sha256"]=sha((out/"author-source-coverage.json").read_bytes())
    graph["successor_provenance"]=provenance
    emit(out,"author-graph-views.json",graph)
    # Source-row identity and actual source bytes are not changed to manufacture a new binding.
    emit_raw(out,"author-source-row-candidate.json",(previous/"author-source-row-candidate.json").read_bytes())
    candidate=json.loads((previous/"publication-candidate-CubicStatePreparation.json").read_bytes())
    old_binding=candidate["binding_sha256"]
    candidate["successor_provenance"]=provenance
    candidate["assumption_comparison_scope"]={
        "classification_rows_are_not_acceptance":True,
        "n_zero":"Explicit in the sealed natural source and actual Nat signature, not a new premise; old source-implicit category is only historical prose comparison.",
        "historical_policy_compatibility":"Not independently endorsed by this feedback; the source-first reviewer did not inspect historical task files.",
        "native_axiom_generated_signature_compatibility":"PENDING, not certified by author metadata or same/source-implicit rows.",
        "F1_F4_correction_acceptance":"AUTHOR corrected, distinct reviewer must recheck; original static report remains immutable.",
        "stale_comments":"Actual later statements and natural boundary disclosures govern; comments do not assert compiler/phase/physical closure."}
    candidate["source_proof_coverage"]=PREFIX+"author-source-coverage.json"
    candidate["binder_definition_audit"]=PREFIX+"author-binder-definition-audit.json"
    candidate["graph_views"]=PREFIX+"author-graph-views.json"
    candidate["formal_context"]=PREFIX+"author-formal-context.json"
    candidate["formal_packet"]=PREFIX+"author-decoder-packet.json"
    # Evidence locations are future unattached slots, never authored acceptance.
    candidate["decoder_evidence"]=PREFIX+"decoder-pending/CubicStatePreparation-evidence.json"
    candidate["reviewer_evidence"]=PREFIX+"reviewer-pending/CubicStatePreparation-evidence.json"
    contribution=candidate["graph_contribution"]
    contribution.update(
        head="84c4341",
        head_provenance="Parent-supplied metadata-only reference; no Git execution, proof source byte change or new scientific result.",
        source_graph_sha256=sha((out/"author-graph-views.json").read_bytes()),
        coverage_sha256=sha((out/"author-source-coverage.json").read_bytes()),
        formal_context_sha256=context_hash,
        formal_packet_sha256=packet_hash)
    node_ids={node["id"] for node in graph["views"]["source-construction-graph"]["nodes"]}
    contribution["node_ids"] += sorted(node_ids-set(contribution["node_ids"]))
    contribution["metadata_successor_reason"]="Only actual F1–F4 precision corrections; F5 remains qualification, no new source ID or mathematical success."
    catalog_raw=(repo/"website/research/sources.json").read_bytes()
    catalog=json.loads(catalog_raw)
    row=json.loads((out/"author-source-row-candidate.json").read_bytes())["source"]
    existing=[s for s in catalog["sources"] if s["id"]==v1["SOURCE_ID"]]
    assert not existing or existing==[row]
    if not existing:
        catalog["sources"].append(row)
    overlay=v1["OverlayRoot"](repo,{v1["LESSON"]:(out/"source-only.md").read_bytes(),
        "website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind,checker_sha=v1["binding_function"](repo)
    v1["assert_current"](repo,pinned)
    candidate["binding_sha256"]=bind(overlay,candidate)
    emit(out,"publication-candidate-CubicStatePreparation.json",candidate)
    seal=json.loads((previous/"formal-input-seal.json").read_bytes())
    seal["formal_packet_sha256"]=packet_hash
    emit(out,"formal-input-seal.json",seal)
    bridge=json.loads((previous/"author-binding-bridge-proposal.json").read_bytes())
    bridge["formal_context_sha256"]=context_hash
    bridge["formal_packet_sha256"]=packet_hash
    bridge["bindings"]=[{"module":v1["TARGET"],"binding_sha256":candidate["binding_sha256"]}]
    bridge["procedure"]="Author v2 read only specifically authorized static feedback. Parent may attach a late opaque binding bridge only after actual independently frozen formal reconstruction and exact input comparison; no decoder result or success is supplied here."
    bridge["reviewer_result_inspected"]=True
    bridge["reviewer_result_scope"]="Only pinned phase-2 STATIC report, not native final review/decoder/CI."
    bridge["successor_provenance"]=provenance
    emit(out,"author-binding-bridge-proposal.json",bridge)
    # Versioned comparison makes changed vs unchanged bytes explicit.
    comparisons=[]
    compare_names=list(v1["ORIGINAL"])+[
        "author-formal-context.json","author-decoder-packet.json","formal-input-seal.json",
        "author-source-row-candidate.json","author-binder-definition-audit.json","author-source-coverage.json",
        "author-graph-views.json","publication-candidate-CubicStatePreparation.json","author-binding-bridge-proposal.json"]
    for name in compare_names:
        old,new=(previous/name).read_bytes(),(out/name).read_bytes()
        comparisons.append({"path":name,"v1_sha256":sha(old),"v2_sha256":sha(new),
                            "bytes_identical":old==new,"v1_bytes":len(old),"v2_bytes":len(new)})
    delta={"status":WIP,"feedback_sha256":REPORT_SHA,"findings":[
        {"id":"F1","change":"angleConvention logical universal Prop marked SOURCE with recursive actual transparent-angle and scalar-tier law expansion; available internal producer identified without creating full readonly semantics."},
        {"id":"F2","change":"Proof CASE_SPLIT, domain BOUNDARY_PARTITION and target dispatch separated from sufficient-construction OR; rank-one arithmetic-wrapper/counting routes share typed physical head with independent complete OPEN tails; zero-register and zero-error-dimension boundaries separated."},
        {"id":"F3","change":"Literal q/r vector, hcircle->unit, clean coordinate, q!=1->nontrivial coordinate and complete generic-reflection/directsum instantiation tails explicit."},
        {"id":"F4","change":"All structured bundle fields end before actual namespace/ambient/deriving tails. Full original navigational blocks remain separately accessible."},
        {"id":"F5","change":"Qualification retained: metadata classifications do not certify elaboration, historical policy compatibility, compiler/native trust or physical construction."}],
        "exact_field_changes":changes,"artifacts":comparisons,
        "binding":{"v1":old_binding,"v2":candidate["binding_sha256"],
                   "changed":old_binding!=candidate["binding_sha256"],
                   "source_id_unchanged":True,"reason":"Actual audit/coverage/graph hashes and formal packet location changed; no arbitrary replacement source identity."},
        "all_route_fulltails":graph["views"]["source-construction-graph"]["construction_alternatives"],
        "route_AND_edges":[edge for edge in graph["views"]["source-construction-graph"]["AND_hyperedges"] if edge["id"].startswith("route:")],
        "independent_v2_review":"PENDING","Lean_executed":False,"main_admission":False}
    emit(out,"v1-v2-delta.json",delta)
    lines=[
        "# c29 AUTHOR metadata successor v2",
        "",
        "This new author packet responds only to the specifically authorized pinned STATIC feedback. The author has read that report and does not claim blindness to it. Decoder, CI and other independent review outputs were not read.",
        "",
        "Original source trio, all v1 artifacts, original manifest and review phase-1 records remain untouched. No production/canonical/Lean/Git change or independent acceptance is made.",
        "",
        "| Finding | v2 correction | Still not certified |",
        "|---|---|---|",
        "| F1 | angleConvention is SOURCE proof of a recursively expanded universal proposition; source producer identified. | Actual Ry amplitudes, full readonly witness and physical semantics. |",
        "| F2 | Typed CASE_SPLIT / BOUNDARY_PARTITION / TARGET_DISPATCH separate from SUFFICIENT_CONSTRUCTION_OR; rank-one two-route full OPEN tails. | Any completed arithmetic/counting denotation or unitary circuit. |",
        "| F3 | Literal q/r vector and hcircle unit producer, coordinate and q!=1 guard exposed. | Choice of approximation q, error quality or circuit realization. |",
        "| F4 | Exact structured field boundaries exclude namespace/ambient commands; whole navigational source remains. | Compiler-elaborated field/projection/signature audit. |",
        "| F5 | Qualifications retained; n=0 is already explicit and historical policy compatibility is not independently endorsed. | Native/axiom/reader/integration/PURIFIED gates. |",
        "",
        "## Exact v1 → v2 byte comparison",
        "",
        "| Artifact | v1 SHA256 | v2 SHA256 | Identical |",
        "|---|---|---|---|",
    ]
    lines += ["| "+item["path"]+" | "+item["v1_sha256"]+" | "+item["v2_sha256"]+" | "+str(item["bytes_identical"])+" |" for item in comparisons]
    lines += ["","Publication binding v1: "+old_binding,"","Publication binding v2: "+candidate["binding_sha256"],
              "","The formal context stays byte-identical. Source identity and natural source stay unchanged; source/audit/topology correction requires a genuine successor binding, not a new source ID.",
              "","## Rank-one route full AND tails"]
    for edge in delta["route_AND_edges"]:
        lines += ["",edge["id"]+" → "+", ".join(edge["heads"])+" (OPEN; all jointly required):",""]
        lines += ["- "+tail for tail in edge["tails"]]
    lines += ["","Both rank-one routes are alternative proposed sufficient constructions at the same physical head. Proof cases are not alternative circuits; no OPEN tail is discharged by its name.",
              "","Independent re-review of this v2 remains PENDING. Invalid Windows partial context and failure history remain only in immutable v1; none is copied as a successful input.",""]
    emit_raw(out,"v1-v2-difference.md","\n".join(lines).encode())
    registry_raw=(repo/"website/research/publications.json").read_bytes()
    registry_count=len(json.loads(registry_raw)["records"])
    v1["assert_current"](repo,pinned)
    new_names=sorted(p.name for p in out.iterdir() if p.is_file())
    emit(out,"metadata-freeze.json",{
        "status":WIP,"version":2,"successor_provenance":provenance,
        "original_trio_copies":original_copies,
        "new_artifacts":[record(out/name,name) for name in new_names],
        "predecessor_manifest_sha256":V1_MANIFEST_SHA,
        "predecessor_artifacts":predecessor_manifest["artifacts"],
        "whole_ambient_binding_inputs":old_freeze["whole_ambient_binding_inputs"],
        "strict_config_and_direct_external_inputs":old_freeze["strict_config_and_direct_external_inputs"],
        "checker_sha256":checker_sha,"binding_recipe":old_freeze["binding_recipe"],
        "registry_observed_count":registry_count,"registry_sha256":sha(registry_raw),
        "head_context":"84c4341 parent-supplied metadata-only reference; no Git execution.",
        "independent_review":"PENDING","canonical_writes":False,"Lean_executed":False,
        "freeze_self_hash_excluded":True})
    report=verify(repo,out,previous,manifest=False)
    emit(out,"mechanical-selftest.json",report)
    names=sorted(p.name for p in out.iterdir() if p.is_file())
    outputs=[]
    for name in names:
        rec=record(out/name,name)
        rec["planned_canonical_path"]=v1["LESSON"] if name=="cubic-grid-rational-operators-and-contracts.md" else PREFIX+name
        outputs.append(rec)
    emit(out,"outputs-manifest.json",{
        "status":WIP,"version":2,"artifacts":outputs,"planned_prefix":PREFIX,
        "manifest_self_hash_excluded":True,"successor_provenance":provenance,
        "mechanical_selftest":report,"main_admission":False,"scientific_ROOT":False,
        "independent_v2_review":"PENDING","source_id_unchanged":True})
    print(json.dumps(verify(repo,out,previous),ensure_ascii=False,indent=2))


def verify(repo,out,previous,manifest=True):
    v1=env(previous)
    sha=v1["sha"]
    load=lambda name:json.loads((out/name).read_bytes())
    frozen=load("metadata-freeze.json")
    assert sha((previous/"outputs-manifest.json").read_bytes())==V1_MANIFEST_SHA
    for item in frozen["predecessor_artifacts"]:
        raw=(previous/item["path"]).read_bytes()
        assert sha(raw)==item["sha256"] and len(raw)==item["bytes"]
    for item in frozen["new_artifacts"]:
        raw=(out/item["path"]).read_bytes()
        assert sha(raw)==item["sha256"] and len(raw)==item["bytes"]
    for name,expected in v1["ORIGINAL"].items():
        assert sha((out/name).read_bytes())==sha((previous/name).read_bytes())==expected
    v1["assert_current"](repo,frozen["whole_ambient_binding_inputs"]+frozen["strict_config_and_direct_external_inputs"])
    assert sha((out/"authorized-static-feedback.md").read_bytes())==REPORT_SHA
    assert (out/"author-formal-context.json").read_bytes()==(previous/"author-formal-context.json").read_bytes()
    formal=load("author-formal-context.json")
    assert len(formal["inventory"])==319
    assert sum(not item["private"] for item in formal["inventory"])==269
    assert sum(item["private"] for item in formal["inventory"])==50
    assert (out/"source-only.md").read_bytes()==(out/"cubic-grid-rational-operators-and-contracts.md").read_bytes()
    coverage=load("author-source-coverage.json")
    assert "".join(p["exact_text"] for p in coverage["source_paragraphs"]).encode()==(out/"source-only.md").read_bytes()
    audit=load("author-binder-definition-audit.json")
    assert audit["project_owned_bundle_expansions"]==coverage["project_owned_bundle_expansions"]
    for bundle in audit["project_owned_bundle_expansions"].values():
        for field in bundle["field_audit"]:
            assert not re.search(r"(?m)^(?:namespace|end|deriving)\b",field["exact_source_field_region"])
            if bundle["name"].endswith(".ExpandedControlledRyWorkspaceReadonlyWitness") and field["name"]=="angleConvention":
                assert field["classification"]=="SOURCE" and len(field["nested_logical_expansion"])==3
    graph=load("author-graph-views.json")
    sg=graph["views"]["source-construction-graph"]
    assert "guarded_OR_cases" not in sg
    assert len(sg["construction_alternatives"])==2
    identities={node["id"] for node in sg["nodes"]}
    assert len(identities)==len(sg["nodes"])
    for edge in sg["AND_hyperedges"]+graph["views"]["functor-hypergraph"]["hyperedges"]:
        assert edge["logic"]=="AND" and set(edge["tails"]+edge["heads"])<=identities
    caseids={case["id"] for case in sg["typed_guarded_partitions"]}
    assert "empty-cases" not in caseids
    assert {"cubic-zero-register-boundary","euclidean-empty-dimension-boundary"}<=caseids
    routes=[edge for edge in sg["AND_hyperedges"] if edge["id"].startswith("route:rank-one-")]
    assert len(routes)==2 and all(edge["heads"]==["target:rank-one-physical"] for edge in routes)
    for edge in routes:
        assert len([tail for tail in edge["tails"] if tail.startswith("OPEN:")])==6
        assert edge["status"]=="OPEN_PROPOSED_SUFFICIENT_CONSTRUCTION_NOT_A_PROOF"
    circle=next(edge for edge in sg["AND_hyperedges"] if edge["id"]=="construction:circle-branch")
    assert {"premise:circle-equation","premise:circle-nontrivial","result:circle-unit","result:circle-clean-coordinate"}<=set(circle["tails"])
    candidate=load("publication-candidate-CubicStatePreparation.json")
    old=json.loads((previous/"publication-candidate-CubicStatePreparation.json").read_bytes())
    assert candidate["source_id"]==old["source_id"]==v1["SOURCE_ID"]
    assert candidate["source_statement"]==old["source_statement"]
    assert candidate["declarations"]==old["declarations"] and len(candidate["declarations"])==269
    assert candidate["status"]==WIP and not candidate["independent_acceptance"] and not candidate["main_admission"]
    row=load("author-source-row-candidate.json")["source"]
    catalog=json.loads((repo/"website/research/sources.json").read_bytes())
    existing=[entry for entry in catalog["sources"] if entry["id"]==v1["SOURCE_ID"]]
    assert not existing or existing==[row]
    if not existing:
        catalog["sources"].append(row)
    overlay=v1["OverlayRoot"](repo,{v1["LESSON"]:(out/"source-only.md").read_bytes(),
        "website/research/sources.json":json.dumps(catalog,ensure_ascii=False).encode()})
    bind,checker_sha=v1["binding_function"](repo)
    assert checker_sha==frozen["checker_sha256"]
    assert bind(overlay,candidate)==candidate["binding_sha256"]
    if manifest:
        man=load("outputs-manifest.json")
        for item in man["artifacts"]:
            raw=(out/item["path"]).read_bytes()
            assert sha(raw)==item["sha256"] and len(raw)==item["bytes"]
            assert not re.search(r"(?:[A-Za-z]:[\\/]|^/|\\)",item["planned_canonical_path"])
    return {
        "status":"MECHANICAL_AUTHOR_V2_INTEGRITY_PASS_NOT_ADMISSION","source_trio_unchanged":True,
        "all_predecessor_artifacts_unchanged":True,"formal_context_bytes_unchanged":True,
        "public_roots":269,"private_helpers":50,"ambient_source_files":len(frozen["whole_ambient_binding_inputs"]),
        "lossless_source_paragraphs":len(coverage["source_paragraphs"]),
        "source_AND_edges":len(sg["AND_hyperedges"]),"sufficient_construction_OR_groups":2,
        "typed_guarded_partitions":len(sg["typed_guarded_partitions"]),
        "rank_one_routes":2,"open_tail_obligations_per_rank_one_route":6,
        "registry_observed_count":frozen["registry_observed_count"],
        "publication_binding_v1":old["binding_sha256"],"publication_binding_v2":candidate["binding_sha256"],
        "binding_changed":old["binding_sha256"]!=candidate["binding_sha256"],
        "checker_call":"binding_digest only, unchanged implementation; no validate_record/check/main",
        "independent_review_of_v2":"PENDING","author_read_authorized_static_feedback":True,
        "decoder_CI_or_other_review_read":False,"Lean_executed":False,
        "main_admission":False,"scientific_ROOT":False,"manifest_verified":manifest}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--previous",type=Path,required=True)
    parser.add_argument("--feedback",type=Path)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    if args.verify:
        print(json.dumps(verify(args.repo.resolve(),args.out.resolve(),args.previous.resolve()),ensure_ascii=False,indent=2))
    else:
        assert args.feedback
        build(args.repo.resolve(),args.out.resolve(),args.previous.resolve(),args.feedback.resolve())

