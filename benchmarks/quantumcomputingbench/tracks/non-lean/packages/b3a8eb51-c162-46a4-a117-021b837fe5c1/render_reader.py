"""Build an offline workbook preview from reviewed packets using the repository TeX renderer and native MathML."""
import argparse
from html import escape
import json
import re
import shutil
import sys
from pathlib import Path

FORMULA = re.compile(r'(\\\((.*?)\\\)|\\\[(.*?)\\\])', re.S)
CSS = """
:root { color-scheme:light; font-family:system-ui,sans-serif; color:#1b2730; background:#fff; }
body { max-width:66rem; margin:0 auto; padding:2rem clamp(1rem,4vw,3.5rem) 4rem; }
h1,h2,h3 { line-height:1.22; color:#143b45; } h1{font-size:clamp(2rem,5vw,3rem);margin-bottom:.6rem}
h2{margin-top:0} p,li,dd{line-height:1.57} dd{margin:0 0 1rem} dt{font-weight:650}
nav{padding:1rem 0;border-top:1px solid #b8c8cc} nav li{margin:.25rem 0} a{color:#135670}
article{border-top:2px solid #476a74;padding:1.5rem 0;margin-top:2rem} .meta{font-size:.88rem;color:#395460}
details{margin:.7rem 0;border:1px solid #c9d3d5;border-radius:5px;padding:.65rem .85rem} summary{cursor:pointer;font-weight:650}
summary:focus-visible,a:focus-visible{outline:3px solid #a65919;outline-offset:3px} .source,code{overflow-wrap:anywhere}
.qcb-equation{display:block;overflow-x:auto;max-width:100%;margin:.45rem 0;padding:.22rem 0}
.qcb-math-token{display:inline-block;max-width:100%;overflow-x:auto;vertical-align:middle;padding:.12rem 0}
math[display=block]{text-align:left;margin:0} ol,ul{padding-inline-start:1.5rem}
@media(max-width:550px){body{padding:1rem .9rem 3rem}details{padding:.5rem}li{overflow-wrap:anywhere}}
"""
def read(path):
    return json.loads(path.read_bytes())

def build(package, repo, path):
    import subprocess
    from lxml import etree, html as etree_html
    sys.path.insert(0,str(repo))
    from website.scripts.qcb_math import math_html
    raw_formulas=[]
    def prose(s):
        output=[]
        cursor=0
        for match in FORMULA.finditer(s):
            output.append(escape(s[cursor:match.start()]).replace('\n','<br>'))
            tex=match[2] if match[2] is not None else match[3]
            markup=math_html(match[0],tex,display=match[3] is not None)
            if 'qcb-math-literal' in markup:
                raise ValueError('Unsupported source TeX: '+tex)
            # A block-styled span is valid inside a paragraph. The HTML parser
            # would implicitly close the paragraph around a div and detach its tail.
            if match[3] is not None and markup.startswith('<div') and markup.endswith('</div>'):
                markup='<span'+markup[4:-6]+'</span>'
            output.append(markup)
            raw_formulas.append(tex)
            cursor=match.end()
        output.append(escape(s[cursor:]).replace('\n','<br>'))
        return ''.join(output)
    def paragraphs(strings):
        return ''.join('<p>'+prose(s)+'</p>' for s in strings)
    def bullets(strings):
        return '<ul>'+''.join('<li>'+prose(s)+'</li>' for s in strings)+'</ul>'
    def panel(name,body):
        return '<details><summary>'+escape(name)+'</summary>'+body+'</details>'
    order_file=package/'questions-only.jsonl'
    if order_file.exists():
        slot_order=[json.loads(row)['slot'] for row in order_file.read_bytes().splitlines()]
        data=[read(package/'qa'/(slot+'.json')) for slot in slot_order]
    else:
        data=[read(p) for p in sorted((package/'qa').glob('*.json'))]
    private=data[0]['proposed_use']['status'].startswith('owner')
    title='Owner-only evaluation handoff' if private else 'QuantumComputingBench study workbook'
    scope='Private controller copy. Supply one frozen question at a time. All three packets share an exposure group.' if private else 'Public study candidates. Each question carries its assumptions and conventions. Proposed training use awaits maintainer reconciliation.'
    parts=['<h1>'+title+'</h1><p>'+scope+'</p><nav aria-label="Contents"><ol>']
    for p in data:
        parts.append(f'<li><a href="#{p["slot"]}">{escape(p["title"])}</a></li>')
    parts.append('</ol></nav>')
    for p in data:
        slot=p['slot']; reasoning=p['reasoning_map']
        parts.append(f'<article id="{slot}"><p class="meta">{slot} · {escape(p["difficulty"]["construction_band"])} provisional</p><h2>{escape(p["title"])}</h2>')
        parts.append('<h3>Assumptions</h3>'+bullets(p['assumptions'])+'<h3>Conventions</h3>'+bullets(p['conventions']))
        parts.append('<div data-question><h3>Question</h3>'+paragraphs(p['question'].split('\n\n'))+'</div>')
        parts.append(panel('Reference solution',paragraphs(p['reference_answer'].split('\n\n'))))
        criteria='<ol>'+''.join(f'<li><b>{r["id"]} · {r["weight"]}/10</b><p>{prose(r["criterion"])}</p><p>Partial credit. {prose(r["partial"])}</p></li>' for r in p['rubric'])+'</ol>'
        parts.append(panel('Grading and alternative proofs',criteria+'<h3>Valid alternatives</h3>'+bullets(p['valid_alternatives'])+'<p>Credit any mathematically equivalent argument establishing the requested claims under their stated premises.</p>'))
        parts.append(panel('Boundary cases and common errors','<dl>'+''.join('<dt>'+prose(b['condition'])+'</dt><dd>'+prose(b['conclusion'])+'</dd>' for b in p['boundary_cases'])+'</dl>'+bullets(p['common_errors'])))
        pathnodes=''.join('<dt>'+escape(n['id']+' · '+n['kind'])+'</dt><dd>'+prose(n['claim'])+'<p class="meta">'+escape(', '.join(n['requires']) or 'Input')+'</p></dd>' for n in reasoning['nodes'])
        routes=paragraphs([a['assumptions']+' '+a['route'] for a in reasoning['alternative_routes']])
        joins=paragraphs([j['node']+' ← '+', '.join(j['necessary_inputs'])+'. '+j['why_each'] for j in reasoning['joins']])
        parts.append(panel('Reasoning map and difficulty','<dl>'+pathnodes+'</dl>'+joins+routes+paragraphs([p['difficulty']['rationale']])))
        source_list=''
        source_nodes=read(package/'source-index.json')['nodes']
        for node_id in p['target_nodes']+p['supporting_nodes']:
            entry=source_nodes[node_id]
            ref={'path':entry['path'],'source_commit':entry['source_commit'],'declaration_spans':[{'node_id':node_id,'start':entry['start'],'end':entry['end'],'scope':entry['scope']}]}
            for span in ref['declaration_spans']:
                href='https://github.com/DakeBU/QuantumComputinglib-QuantumComputingBench/blob/'+ref['source_commit']+'/'+ref['path']+f'#L{span["start"]}-L{span["end"]}'
                source_list+=f'<li class="source"><a href="{escape(href)}">{escape(span["node_id"])}</a><p>{prose(span["scope"])}</p></li>'
        parts.append(panel('Source declarations and evidence',paragraphs([p['evidence_boundary']])+'<ul>'+source_list+'</ul>')+'</article>')
    html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+CSS+'</style></head><body>'+''.join(parts)+'</body></html>'
    doc=etree_html.document_fromstring(html)
    spans=doc.xpath('//*[@data-qcb-math-tex]')
    api=json.loads(subprocess.check_output(['pandoc','-f','markdown','-t','json'],input=b''))['pandoc-api-version']
    blocks=[]
    def font_alias(tex):
        return re.sub(r'\{\\rm\s+([A-Za-z]+)\}',lambda m:r'{\mathrm{'+m[1]+'}}',tex)
    for span in spans:
        mode='DisplayMath' if span.get('class')=='qcb-equation' else 'InlineMath'
        blocks.append({'t':'Para','c':[{'t':'Math','c':[{'t':mode},font_alias(span.get('data-qcb-math-tex'))]}]})
    batch={'pandoc-api-version':api,'meta':{},'blocks':blocks}
    converted=subprocess.run(['pandoc','-f','json','-t','html5','--mathml'],input=json.dumps(batch),text=True,capture_output=True,check=True)
    parsed=etree_html.fragment_fromstring(converted.stdout,create_parent=True)
    equations=parsed.xpath('.//math')
    if len(equations)!=len(raw_formulas) or converted.stderr.strip():
        raise ValueError('TeX to MathML: '+converted.stderr[:3000]+'; converted '+str(len(equations))+' of '+str(len(spans)))
    for span,math in zip(spans,equations,strict=True):
        if math.xpath('.//merror') or math.find('.//annotation').text!=font_alias(span.get('data-qcb-math-tex')):
            raise ValueError('Compiled equation differs from exact source: '+span.get('data-qcb-math-tex'))
        math.find('.//annotation').text=span.get('data-qcb-math-tex')
        span.text=None
        span.append(math)
    assert len(doc.xpath('//details[not(@open)]'))==5*len(data)
    assert len(doc.xpath('//details/summary'))==5*len(data)
    for packet,question_div in zip(data,doc.xpath('//*[@data-question]'),strict=True):
        assert len(question_div.xpath('.//math'))==len(FORMULA.findall(packet['question']))
    ids=set(doc.xpath('//*[@id]/@id'))
    assert all(h[1:] in ids for h in doc.xpath('//a[starts-with(@href,"#")]/@href'))
    assert not doc.xpath('//script|//merror')
    saved=etree.tostring(doc,method='html',encoding='unicode',doctype='<!doctype html>')
    path.write_text(saved+'\n',encoding='utf-8')
    report={'math_engine':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0]+' with texmath, source tokens bound by repository qcb_math.math_html','formulas':len(raw_formulas),'per_packet':{a.get('id'):len(a.xpath('.//math')) for a in doc.xpath('//article')},'math_errors':0,'checks':['Compiled each explicit formula to native MathML; Traditional roman-font declarations are expanded for texmath. Every MathML annotation preserves the exact original TeX.','All local contents links resolve, all five disclosures per packet start closed and contain a summary, questions expose their own formulas, and no active scripts or external resources are required.'],'interactive_browser_test':'Not run inside this local process; Chromium could not open its process-singleton socket in this environment.'}
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--package',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(build(args.package.resolve(),args.repo.resolve(),args.output.resolve()),indent=2))
