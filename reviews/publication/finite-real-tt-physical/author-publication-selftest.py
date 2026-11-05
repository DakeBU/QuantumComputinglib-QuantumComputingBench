"""Read-only author mechanics, not admission or mathematical/source acceptance."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch

sys.dont_write_bytecode=True
SHA=lambda b:hashlib.sha256(b).hexdigest()
LOAD=lambda p:json.loads(p.read_text(encoding="utf-8"))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,required=True);p.add_argument("--packet",type=Path,required=True)
    a=p.parse_args(); root=a.root.resolve();here=a.packet.resolve()
    f=LOAD(here/"publication-freeze.json")
    for n,h in f["artifacts"].items(): assert SHA((here/n).read_bytes())==h,n
    for r in f["binding_production_inputs"]+f["other_inputs"]: assert SHA((root/r["path"]).read_bytes())==r["sha256"],r["path"]
    src=(here/"finite-real-tt-physical-source-only.txt").read_bytes()
    assert SHA(src)==f["source_sha256"]
    lesson="docs/lessons/finite-real-tt-primitive-preparation-and-word-order.md"
    if (root/lesson).exists(): assert (root/lesson).read_bytes()==src
    old=here/"author-freeze.json"
    if old.exists(): assert SHA(old.read_bytes())==f["unchanged_original_source_freeze_sha256"]
    cov=LOAD(here/"author-source-coverage.json")
    assert "".join(r["exact_text"] for r in cov["source_paragraphs"]).encode()==src
    at=0
    for r in cov["source_paragraphs"]:
        raw=r["exact_text"].encode();assert r["start_utf8_byte"]==at and r["end_utf8_byte"]==at+len(raw)
        assert SHA(raw)==r["sha256"]
        assert r["disposition"]=="NODE" and r["source_nodes"] or r["disposition"]=="EXCLUDED" and r["reason"]
        at+=len(raw)
    assert at==len(src)
    ctx=LOAD(here/"author-formal-context.json");pkt=LOAD(here/"author-decoder-packet.json");seal=LOAD(here/"formal-input-seal.json")
    for n,h in seal["artifacts"].items():assert SHA((here/n).read_bytes())==h
    assert pkt["formal_context_sha256"]==SHA((here/"author-formal-context.json").read_bytes())==cov["full_target_source_context_sha256"]
    for r in ctx["target_files"]:
        raw="".join(r["full_source_lines"]).encode();assert SHA(raw)==r["sha256"] and raw==(root/r["path"]).read_bytes()
    for r in ctx["provider_index"]:assert SHA((root/r["path"]).read_bytes())==r["sha256"]
    assert len(ctx["target_files"])==3 and len(ctx["inventory"])==37
    assert "statement_source" not in (here/"author-formal-context.json").read_text(encoding="utf-8")
    assert len(cov["whole_module_inventory"])==37
    assert cov["additional_top_level_named_instances"]==cov["private_target_helpers"]==0
    for r in cov["whole_module_inventory"]:
        assert r["output_logic"]=="AND" and r["output_conjuncts"] and r["source_paragraphs"]
        assert all(x["classification"]=="SOURCE" for x in r["logical_inputs"])
    graph=LOAD(here/"author-graph-views.json")
    assert graph["coverage_sha256"]==SHA((here/"author-source-coverage.json").read_bytes())
    sg=graph["views"]["source-construction-graph"];nodes={r["id"]:r for r in sg["nodes"]}
    assert len(nodes)==len(sg["nodes"]) and len(sg["hyperedges"])==32
    for e in sg["hyperedges"]:
        assert e["logic"]=="AND" and e["tails"] and e["heads"]
        assert set(e["tails"]+e["heads"])<=set(nodes)
    gaps={n for n,v in nodes.items() if v["kind"]=="SOURCE_GAP"}
    assert gaps==set(cov["open_source_gap_ids"]) and len(gaps)==6
    assert all(nodes[n]["status"]=="OPEN" and not nodes[n]["mathematical_proof_node"] for n in gaps)
    assert {r["to"] for r in sg["source_gap_links"]}==gaps
    assert len(graph["views"]["lean-graph"]["target_import_edges"])==10
    assert len(graph["views"]["lean-graph"]["ownership_edges"])==37
    assert not graph["views"]["lean-graph"]["elaborated_theorem_dependencies"]
    assert graph["views"]["functor-hypergraph"]["certified_transport"] is False
    assert not graph["views"]["functor-hypergraph"]["implication_hyperedges"]
    inventory=LOAD(root/"web/library/declarations.json")["declarations"]
    spec=importlib.util.spec_from_file_location("c26_readonly_public_checker",root/"website/scripts/check_research_publications.py")
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    original_file,original_load=checker.local_file,checker.load
    source_row=LOAD(here/"author-source-row-candidate.json")["source"]
    def pf(r,n):return here/"finite-real-tt-physical-source-only.txt" if n==lesson else original_file(r,n)
    def pl(r,n):
        data=original_load(r,n)
        if n=="website/research/sources.json":
            found=[x for x in data["sources"] if x["id"]==source_row["id"]]
            assert not found or found==[source_row]
            if not found:data["sources"].append(source_row)
        return data
    bindings=[]
    with patch.object(checker,"local_file",pf),patch.object(checker,"load",pl):
        for slug,count in (("local-compiler",10),("word",12),("primitive-preparation",15)):
            r=LOAD(here/("publication-candidate-"+slug+".json"))
            actual=[x["fullName"] for x in inventory if x.get("source")==r["module"]]
            assert r["declarations"]==actual and len(actual)==count
            assert set(actual)=={n for item in r["obligation_map"] for n in item["declarations"]}
            assert checker.binding_digest(root,r)==r["binding_sha256"]
            assert r["status"]=="AUTHOR_WIP_NOT_ADMITTED" and not r["main_admission"] and not r["scientific_ROOT"]
            assert all(x in ("EXISTS_UNREAD_NOT_VALIDATED","PLACEHOLDER_NOT_PRESENT") for x in r["evidence_paths_status"].values())
            bindings.append({"module":r["module"],"publication_binding_sha256":r["binding_sha256"]})
    bridge=LOAD(here/"author-binding-bridge-proposal.json")
    assert [{"module":r["module"],"publication_binding_sha256":r["publication_binding_sha256"]} for r in bridge["bindings"]]==bindings
    assert bridge["frozen_packet_sha256"]==SHA((here/"author-decoder-packet.json").read_bytes())
    assert bridge["opaque_context_binding_sha256"]==pkt["opaque_context_binding_sha256"]
    for n in ("author-formal-context.json","author-decoder-packet.json"):
        raw=(here/n).read_text(encoding="utf-8")
        assert source_row["id"] not in raw and f["source_sha256"] not in raw
        assert "assumption_deltas" not in raw and "independent_source_topology_ground" not in raw
    for n in f["artifacts"]:
        raw=(here/n).read_text(encoding="utf-8")
        for drive in ("C","D"):
            for sep in ("/","\\\\"):assert drive+":"+sep+"Users"+sep not in raw
    print(json.dumps({"status":"MECHANICAL_AUTHOR_INTEGRITY_PASS_NOT_ADMISSION","source_bytes":len(src),"lossless_paragraphs":len(cov["source_paragraphs"]),"inventory":37,"named_ambient_or_private_extra":0,"independent_source_AND_chains":32,"open_consumer_gaps":6,"target_import_edges":10,"ownership_edges":37,"formal_packet_sha256":SHA((here/"author-decoder-packet.json").read_bytes()),"public_binding_digest_replayed":bindings,"validate_record_called":False,"Lean_executed":False,"independent_evidence_fabricated":False,"main_admission":False,"scientific_ROOT":False},ensure_ascii=False))


if __name__=="__main__":main()
