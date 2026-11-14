"""Export standalone question sheets with no grader data and check exact math annotations."""
import argparse
import collections
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
from lxml import etree, html

MATH=re.compile(r'\\\((.*?)\\\)|\\\[(.*?)\\\]',re.S)

def text_and_tex(node):
    copy=deepcopy(node)
    for span in copy.xpath('.//*[@data-qcb-math-tex]'):
        delim=('\\[','\\]') if span.get('class')=='qcb-equation' else ('\\(','\\)')
        annotation=span.xpath('.//annotation[@encoding="application/x-tex"]/text()')
        assert annotation==[span.get('data-qcb-math-tex')]
        literal=etree.Element('span');literal.text=delim[0]+annotation[0]+delim[1];literal.tail=span.tail
        span.getparent().replace(span,literal)
    for br in copy.xpath('.//br'):
        br.tail=' '+(br.tail or '')
    return ''.join(copy.itertext()).strip()

def export(package):
    doc=html.document_fromstring((package/'reader.html').read_bytes(),parser=html.HTMLParser(encoding='utf-8'))
    questions=[json.loads(line) for line in (package/'questions-only.jsonl').read_bytes().splitlines()]
    qmap={q['slot']:q for q in questions}
    folder=package/'question-sheets';folder.mkdir(exist_ok=True)
    result={}
    norm=lambda s:' '.join(s.split())
    for a in doc.xpath('//article'):
        slot=a.get('id');q=qmap[slot]
        new=etree.Element('html',lang='en');head=etree.SubElement(new,'head');etree.SubElement(head,'meta',charset='utf-8');etree.SubElement(head,'meta',name='viewport',content='width=device-width,initial-scale=1');etree.SubElement(head,'title').text=q['title'];head.append(deepcopy(doc.xpath('//style')[0]));body=etree.SubElement(new,'body');body.set('class','question-sheet');etree.SubElement(body,'h1').text=q['title']
        for child in a.xpath('./h3|./ul|./div[@data-question]'):
            body.append(deepcopy(child))
        assert body.xpath('./h3/text()')==['Assumptions','Conventions']
        for ul,values in zip(body.xpath('./ul'),[q['assumptions'],q['conventions']],strict=True):
            assert [norm(text_and_tex(li)) for li in ul.xpath('./li')]==[norm(s) for s in values]
        assert [norm(text_and_tex(x)) for x in body.xpath('./div/p')]==[norm(s) for s in q['question'].split('\n\n')]
        assert not body.xpath('.//details|.//a|.//script|.//input|.//*[@id]')
        expected=[x or y for s in q['assumptions']+q['conventions']+[q['question']] for x,y in MATH.findall(s)]
        annotations=body.xpath('.//math/semantics/annotation/text()');assert annotations==expected
        out=folder/(slot+'.html');out.write_bytes(etree.tostring(new,method='html',encoding='utf-8',doctype='<!doctype html>')+b'\n')
        result[slot]={'sha256':sha256(out.read_bytes()).hexdigest(),'mathml_elements':len(annotations),'path':out.relative_to(package).as_posix()}
    assert set(result)==set(qmap)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--package',type=Path,required=True)
    print(json.dumps(export(parser.parse_args().package),indent=2))
