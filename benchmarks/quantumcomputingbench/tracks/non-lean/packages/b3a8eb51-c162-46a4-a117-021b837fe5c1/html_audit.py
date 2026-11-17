"""Audit reader structure and its MathML/links without executing the browser."""
from hashlib import sha256
from pathlib import Path
from lxml import html
import json

def check(raw):
    dom=html.document_fromstring(raw,parser=html.HTMLParser(encoding='utf-8'));abstract=dom.xpath('//article');nav=dom.xpath('//nav//a/@href');ids=[a.get('id') for a in abstract]
    assert ids and len(set(ids))==len(ids) and set(nav)=={'#'+i for i in ids}
    summaries=dom.xpath('//article/details/summary');assert len(summaries)==len(abstract)*5 and not dom.xpath('//details[@open]')
    assert all(s.getparent()[0]==s and s.text_content().strip() for s in summaries)
    math=dom.xpath('//math');assert math and not dom.xpath('//merror|//script|//iframe|//link[@rel="stylesheet"]|//img[@src]')
    assert all(len(m.xpath('.//annotation[@encoding="application/x-tex"]'))==1 for m in math)
    css=''.join(dom.xpath('//style/text()'));viewport=dom.xpath('//meta[@name="viewport"]/@content');assert any('width=device-width' in v for v in viewport)
    assert 'summary:focus-visible' in css and 'overflow-x:auto' in css and '@media' in css
    return {'sha256':sha256(raw).hexdigest(),'articles':len(abstract),'navigation_targets':len(nav),'initially_closed_summaries':len(summaries),'mathml_expressions':len(math),'scope':'Parsed static HTML, native controls, viewport/focus/overflow rules, local navigation and MathML annotations. Keyboard events and pixel layout require a browser run.'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('reader',type=Path);args=ap.parse_args();print(json.dumps(check(args.reader.read_bytes()),indent=2))
