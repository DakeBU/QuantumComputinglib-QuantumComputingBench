"""Verify a supplementary intake against its repository and frozen declarations."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import re
import subprocess
import sys
from uuid import UUID

def load(path):
    return json.loads(path.read_bytes())

def sf(b):
    return hashlib.sha256(b).hexdigest()

def hashfile(p):
    return sf(p.read_bytes())

def lines(p):
    return [json.loads(row) for row in p.read_text(encoding='utf-8').splitlines()]

def require(condition,message):
    if not condition:
        raise ValueError(message)

def verify(p,root):
    p=p.resolve()
    root=root.resolve()
    m=load(p/'manifest.json')
    require(subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==m['base_commit'],'checkout must be at the pinned revision')
    rel=Path(m['package_path'])
    overlay=p
    for _ in rel.parts:
        overlay=overlay.parent
    require((overlay/rel).resolve()==p,'package path')
    snapshots=m['snapshot']
    snap=root/snapshots['path']
    require(hashfile(snap)==snapshots['sha256'],'snapshot digest')
    frozen=load(snap)
    require(frozen['snapshot_id']==snapshots['id'] and frozen['commit']==snapshots['source_commit'],'snapshot identity')
    b=root/'benchmarks/quantumcomputingbench'
    sys.path.insert(0,str(b/'src'))
    from qcb_core import digest
    from qcb_curriculum import load_catalog,validate_proposals,core_contract
    catalog,originals,graph=load_catalog()
    require(catalog['catalog_hash']==m['catalog_hash'],'catalog hash')
    seen=set()
    if 'handoff_wrapper' in m:
        cover=overlay/'OWNER_HANDOFF.md'
        require(m['handoff_wrapper']['sha256']==hashfile(cover) and m['handoff_wrapper']['bytes']==cover.stat().st_size,'owner cover note digest')
    for row in m['files']:
        name=Path(row['path'])
        require(not name.is_absolute() and '..' not in name.parts and name not in seen,'unsafe or duplicate filename')
        seen.add(name)
        f=overlay/name
        require(f.is_file() and f.stat().st_size==row['bytes'] and hashfile(f)==row['sha256'],'file differs: '+str(name))
    idx=load(p/'evidence/packet-index.json')
    precisely={f.relative_to(overlay) for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f!=p/'manifest.json'} | {Path(row['proposal_path']) for row in idx}
    require(seen==precisely,'manifest inventory does not close')
    require(idx==m['packets'],'packet identity list')
    baseline=load(p/'evidence/baseline.json')
    require(baseline['base_commit']==m['base_commit'] and baseline['catalog']['semantic_hash']==m['catalog_hash'],'baseline identity')
    for item in baseline['protocol_and_assessment_files']:
        raw=subprocess.check_output(['git','-C',str(root),'show',m['base_commit']+':'+item['path']])
        require(sf(raw)==item['sha256'],'pinned protocol/assessment file bytes: '+item['path'])
    slots=[r['slot'] for r in idx]
    require(len(slots)==len(set(slots))==m['distinct_packet_count'],'counts')
    require(len({r['core_id'] for r in idx})==len(slots),'duplicate target')
    source=load(p/'source-index.json')
    require(source['source_commit']==frozen['commit'],'source snapshot')
    cached={}
    def blob(path):
        if path not in cached:
            cached[path]=subprocess.check_output(['git','-C',str(root),'show',frozen['commit']+':'+path])
        return cached[path]
    for node,v in source['nodes'].items():
        n=graph[node]; a=v['start']; z=v['end']; raw=blob(v['path']); lf=raw.replace(b'\r\n',b'\n'); f=lf.splitlines(keepends=True)
        require(n['source']==v['path'] and n['id']==v['node_id'] and n['line']==a and 1<=a<=z<=len(f),'source span identity')
        require(n['label'].encode() in f[a-1] and sf(b''.join(f[a-1:z]))==v['span_sha256_lf'] and sf(raw)==v['sha256_raw'] and sf(lf)==v['sha256_lf']==frozen['input_hashes'][v['path']], 'frozen source bytes: '+node)
        require(v['graph_edge'] in frozen['edges'] and v['graph_edge']['target']==node,'missing ownership edge')
    future=load(p/'future-work.json')
    f=blob(future['path'])
    require(future['source_status']==graph[future['node_id']]['source_status']=='Planned' and sf(f)==future['sha256'] and sf(b''.join(f.splitlines(keepends=True)[future['start']-1:future['end']]))==future['span_sha256'],'planned source boundary')
    require(future['node_id'] not in source['nodes'],'future work used as evidence')
    student=lines(p/'questions-only.jsonl'); refs=lines(p/'references.jsonl'); meta=lines(p/'grader-metadata.jsonl')
    require(all([r['slot'] for r in data]==slots for data in [student,refs,meta]),'projections reordered or incomplete')
    repo_props={path.name:load(path) for path in (b/'tracks').glob('*/proposals/*.json')}
    proposed=[]; reverse={key:[] for key in source['nodes']}
    for row,q,ref,g in zip(idx,student,refs,meta,strict=True):
        slot=row['slot'];core=row['core_id'];path=overlay/row['payload_path'];v=load(path);qp=overlay/row['frozen_question_path'];question=load(qp);proof=row['review']
        require(set(question)=={'slot','title','question','assumptions','conventions'} and q==dict(question,core_id=core),'question-only projection')
        require(all(v[key]==value for key,value in question.items()) and v['core_id']==core,'frozen wording changed')
        require(not re.search(r'declaration:|QuantumBlockEncoding|\.lean\b|\bLean\b',str(question)),'implementation vocabulary in prompt')
        require(hashfile(path)==row['payload_sha256'] and hashfile(qp)==row['question_sha256'] and digest(v)==row['item_digest'],'packet digests')
        require(ref=={'slot':slot,'core_id':core,'question_file_sha256':row['question_sha256'],'item_digest':digest(v),'reference_answer':v['reference_answer']},'reference row')
        require(g=={'slot':slot,'core_id':core,'item_digest':digest(v),**{n:v[n] for n in ('rubric','reasoning_map','common_errors','boundary_cases','valid_alternatives','difficulty')}},'grading projection')
        require(sum(c['weight'] for c in v['rubric'])==10 and all(c['weight']>0 and c['criterion'] and c['partial'] for c in v['rubric']),'weighted rubric')
        require(len({c['id'] for c in v['rubric']})==len(v['rubric']),'rubric IDs')
        prop=load(overlay/row['proposal_path'])
        require(Path(row['proposal_path']).stem==prop['proposal_id']==str(UUID(prop['proposal_id'])) and prop['core_id']==core and prop['item_digest']==digest(v),'proposal identity')
        require(prop['source_nodes']==v['target_nodes']+v['supporting_nodes'] and prop['proposed_contract']==core_contract(v) and digest(core_contract(v))==prop['contract_hash']==row['contract_hash'],'proposal contract')
        if v['contribution_type']=='existing_core_view':
            require(core in originals and core_contract(v)==core_contract(originals[core]),'existing contract changed')
        else:
            require(core=='candidate:'+prop['proposal_id'] and v['admission']=='candidate_not_counted' and v['split']=='unassigned_pending_reconciliation','candidate escaped admission boundary')
        if prop['proposal_id']+'.json' in repo_props:
            require(repo_props[prop['proposal_id']+'.json']==prop,'UUID collision in checkout')
        repo_props[prop['proposal_id']+'.json']=prop
        proposed.append(prop['proposal_id'])
        nodekeys=v['target_nodes']+v['supporting_nodes']
        for role in ('target_nodes','supporting_nodes'):
            for n in v[role]:
                require(n in source['nodes'],'unbound source node')
                reverse[n].append({'slot':slot,'role':role})
        topo=v['reasoning_map'];nodes={}
        for n in topo['nodes']:
            require(n['id'] not in nodes and n['kind'] in ('given','derive') and n['claim'] and set(n['requires'])<=nodes.keys() and set(n['anchors'])<=set(nodekeys),'reasoning topology: '+slot+'/'+n['id'])
            nodes[n['id']]=n
        for j in topo['joins']:
            require(j['node'] in nodes and len(j['necessary_inputs'])>=2 and set(j['necessary_inputs'])<=set(nodes[j['node']]['requires']) and j['why_each'],'join tail')
        require(all(a['assumptions'] and a['route'] for a in topo['alternative_routes']) and v['boundary_cases'] and v['common_errors'] and v['valid_alternatives'],'routes or boundary cases')
        rr=overlay/proof['report_path'];ph=overlay/proof['phase1_path']
        require(hashfile(rr)==proof['report_sha256'] and hashfile(ph)==proof['phase1_sha256'],'review file bytes')
        late=load(rr); early=load(ph); order=load(rr.parent/'phase1-seal.json');freeze=load(rr.parent/'freeze.json')
        require(order['phase1_sha256']==hashfile(ph) and order['freeze_sha256']==hashfile(rr.parent/'freeze.json') and late['phase1_sha256']==hashfile(ph),'review stage binding')
        require(late['reviewer']==early['reviewer']==proof['reviewer']!=v['author'] and not late['human_approval'],'review roles')
        e=next(i for i in early['items'] if i['slot']==slot);l=next(i for i in late['items'] if i['slot']==slot)
        require(e['question_sha256']==l['question_sha256']==hashfile(qp)==freeze['questions'][slot] and e['derivation'] and e['source_checks'],'independent solution binding')
        require(l['verdict']=='accept' and l['payload_sha256_raw']==hashfile(path) and l['item_digest']==digest(v) and l['reasoning'] and l['rubric_assessment'] and l['map_assessment'] and l['source_checks'],'full review binding')
        for filename,h in freeze['files'].items():
            require(hashfile(p/filename)==h,'pre-authoring plan/source file changed')
        require(any(load(f)['payloads'].get(slot)==hashfile(path) and load(f)['phase1_seal_sha256']==hashfile(rr.parent/'phase1-seal.json') for f in rr.parent.glob('*authorization*.json')),'missing review authorization')
    for path in (p/'reviews').glob('*/history/review-v1.json'):
        prior=load(path)
        for item in prior['items']:
            slot=item['slot']
            current=p/'qa'/(slot+'.json')
            prev=path.parent/(slot+'-v1.json')
            raw=prev if prev.exists() else current
            require(hashfile(raw)==item['payload_sha256_raw'] and digest(load(raw))==item['item_digest'],'historical review lost its exact payload: '+slot)
            require(item['verdict'] in ('accept','revise'),'unknown historical verdict')
    import ast
    probe=p/'browser_check.py'
    if probe.exists():
        ast.parse(probe.read_text('utf-8'))
        browser=load(p/'evidence/reader-compatibility.json');current=browser['current_reader']
        require(current['sha256']==hashfile(p/'reader.html') and current['articles']==len(slots) and current['initially_closed_summaries']==5*len(slots),'offline HTML audit')
        gate=browser['browser_gate']
        require(gate['interactive_pass_claimed']==(gate['result']=='pass'),'interactive evidence status')
    validation=load(p/'evidence/validation.json') if (p/'evidence/validation.json').exists() else None
    if validation:
        render=validation['offline_reader']
        if m['visibility']=='public_study':
            pr=load(p/'evidence/print-check.json')
            require(pr['pdf_sha256']==hashfile(p/'questions-print.pdf') and pr['questions_only_export_sha256']==hashfile(p/'questions-only.jsonl') and [item['slot'] for item in pr['pages']]==slots, 'public print export binding')
        require(render['reader_html_sha256']==hashfile(p/'reader.html') and render['math_errors']==0,'reader validation digest')
        require(set(render['per_packet'])==set(slots) and sum(render['per_packet'].values())==render['formulas'],'reader packet/formula inventory')
    inv=load(p/'evidence/comparison-inventory.json')
    ov=load(p/'overlap-index.json')
    previous=inv['previous_delivery']
    require((any(key.startswith('owner_') for key in previous))==(m['visibility']=='owner_only'),'comparison exposure boundary')
    prior=[q for pack in previous.values() for q in pack['packets']]
    require(len(prior)==ov['compared_previous_packet_count'] and set(slots)=={c['slot'] for c in ov['candidates']},'per-packet overlap scope')
    official_contracts={row['contract_hash'] for row in inv['canonical'].values()}
    prior_contracts={row['contract_hash'] for row in prior}
    proposed_contracts=[row['contract_hash'] for row in idx]
    require(len(set(proposed_contracts))==len(proposed_contracts) and not set(proposed_contracts)&(official_contracts|prior_contracts),'candidate contract already represented')
    from datetime import datetime
    for freeze_path in (p/'reviews').glob('*/freeze.json'):
        folder=freeze_path.parent
        freeze=load(freeze_path)
        seal=load(folder/'phase1-seal.json')
        frozen_time=datetime.fromisoformat(freeze['utc'])
        sealed_time=datetime.fromisoformat(seal['utc_observed'])
        require(frozen_time<=sealed_time and freeze['questions']==seal['question_hashes'],'freeze and independent-derivation seal')
        for auth_path in folder.glob('*authorization*.json'):
            auth=load(auth_path)
            require(datetime.fromisoformat(auth['utc_observed'])>=sealed_time and
                    auth['phase1_sha256']==hashfile(folder/'phase1.json') and
                    auth['phase1_seal_sha256']==hashfile(folder/'phase1-seal.json'),
                    'full-content release precedes or mismatches blind seal')
        history=folder/'history/review-v1.json'
        if history.exists():
            first=load(folder/'phase2-authorization.json')
            for item in load(history)['items']:
                require(first['payloads'][item['slot']]==item['payload_sha256_raw'],'old verdict authorization mismatch')
    for q in student:
        require(all(sf(q['question'].encode())!=c['question_text_sha256'] and q['core_id']!=c['core_id'] for c in prior),'duplicate previous-delivery question or identity')
    sheet_report=load(p/'evidence/question-sheets.json')
    from lxml import html
    from importlib.util import spec_from_file_location,module_from_spec
    sheet_spec=spec_from_file_location('packet_sheet',p/'question_sheets.py');sheet_mod=module_from_spec(sheet_spec);sheet_spec.loader.exec_module(sheet_mod)
    norm=lambda t:' '.join(t.split())
    for q in student:
        info=sheet_report[q['slot']];sheet=p/info['path']
        require(hashfile(sheet)==info['sha256'],'standalone question sheet digest')
        dom=html.document_fromstring(sheet.read_bytes(),parser=html.HTMLParser(encoding='utf-8'));body=dom.find('body')
        require(body.xpath('h1/text()')==[q['title']] and not body.xpath('.//script|.//details|.//a|.//input'),'question sheet boundary')
        require([norm(sheet_mod.text_and_tex(li)) for li in body.xpath('ul[1]/li')]==list(map(norm,q['assumptions'])) and [norm(sheet_mod.text_and_tex(li)) for li in body.xpath('ul[2]/li')]==list(map(norm,q['conventions'])),'standalone premises differ')
        require([norm(sheet_mod.text_and_tex(el)) for el in body.xpath('div/p')]==list(map(norm,q['question'].split('\n\n'))),'standalone question differs')
    require(source['node_to_packets']==reverse,'reverse source index')
    imports=source['module_imports']
    graph_edges={edge['id']:edge for edge in frozen['edges']}
    for edge_id,bound in imports['edges'].items():
        edge=bound['graph_edge']
        require(edge==graph_edges[edge_id] and edge['type']=='module-supports-importer','module edge identity')
        dest=graph[edge['target']]['source']
        raw=blob(dest).replace(b'\r\n',b'\n')
        line=raw.splitlines(keepends=True)[bound['line']-1]
        stmt='import '+edge['source'].removeprefix('module:')
        require(dest==bound['importer_path'] and bound['source_commit']==frozen['commit'] and bound['statement']==stmt and line.strip()==stmt.encode(),'import statement location')
        require(sf(raw)==bound['file_sha256_lf']==frozen['input_hashes'][dest] and sf(line)==bound['line_sha256_lf'],'import statement bytes')
    require(set(imports['by_packet'])==set(slots),'import inventory incomplete')
    used=set()
    for slot,data in imports['by_packet'].items():
        q=load(p/'qa'/(slot+'.json'))
        own={source['nodes'][n]['graph_edge']['source'] for n in q['target_nodes']+q['supporting_nodes']}
        require(sorted(own)==data['anchor_modules'],'anchor-module membership')
        for route in data['shortest_import_paths']:
            here=route['dependency']
            require(here in own and route['importer'] in own and len(route['edge_ids'])>0,'import endpoints')
            for edge_id in route['edge_ids']:
                edge=imports['edges'][edge_id]['graph_edge']
                require(edge['source']==here,'disconnected import path')
                here=edge['target']
                used.add(edge_id)
            require(here==route['importer'],'wrong final importer')
    require(used==set(imports['edges']),'unreferenced import binding')
    validate_proposals(catalog,list(repo_props.values()))
    require(len(proposed)==len(set(proposed)),'duplicate UUIDs')
    print(f'PASS · {len(slots)} packets, {len(reverse)} frozen source nodes, {len(seen)} hashed files; contracts, exports, review hashes and graph bindings checked.')
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True,help='Full-history repository checkout at the stated base')
    parser.add_argument('--package',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    verify(args.package,args.repo)
