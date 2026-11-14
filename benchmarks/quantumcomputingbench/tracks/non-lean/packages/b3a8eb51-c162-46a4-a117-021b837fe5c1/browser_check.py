"""Run offline keyboard, layout and MathML regressions on one exact workbook handoff.

Requires Python Playwright and a locally available Chromium. It makes no HTTP
requests. Use --reader only to test a previous reader without its question sheets.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def layout(page):
    return page.evaluate('''() => {
        const root = document.documentElement;
        const math = [...document.querySelectorAll('math')];
        return {viewport: root.clientWidth, pageWidth: root.scrollWidth,
                annotations: math.filter(m => m.querySelector('annotation[encoding="application/x-tex"]')).length,
                formulas: math.length, mathErrors: document.querySelectorAll('merror').length};
    }''')


def check(reader, executable, sheets):
    from playwright.sync_api import sync_playwright
    sha=lambda p:sha256(p.read_bytes()).hexdigest()
    out={'reader_sha256':sha(reader),'result':'pass','viewports':[]}
    with sync_playwright() as pw:
        args={} if executable is None else {'executable_path':str(executable)}
        browser=pw.chromium.launch(headless=True,**args)
        out['browser_version']=browser.version
        for width,height in [(1280,900),(390,844)]:
            ctx=browser.new_context(viewport={'width':width,'height':height},offline=True)
            page=ctx.new_page(); external=[];errors=[]
            page.on('request',lambda r: external.append(r.url.split(':',1)[0]) if r.url.startswith(('http:','https:')) else None)
            page.on('pageerror',lambda exc:errors.append(str(exc)))
            page.goto(reader.as_uri()); page.wait_for_selector('article')
            metrics=layout(page);assert metrics['pageWidth']<=metrics['viewport']+1,metrics
            assert metrics['formulas']>0 and metrics['annotations']==metrics['formulas'] and metrics['mathErrors']==0,metrics
            summaries=page.locator('article details > summary'); articles=page.locator('article'); assert summaries.count()==5*articles.count()
            assert page.locator('article details[open]').count()==0
            links=page.locator('nav a[href^="#"]'); assert links.count()==articles.count()
            first=links.first;first.focus();page.keyboard.press('Enter');assert page.evaluate('() => Boolean(document.querySelector(location.hash))')
            toggles=0
            for i in range(summaries.count()):
                summary=summaries.nth(i);parent=summary.locator('..'); summary.focus(); assert summary.evaluate('(el)=>document.activeElement===el')
                page.keyboard.press('Enter'); assert parent.evaluate('(el)=>el.open'); assert summary.evaluate('(el)=>getComputedStyle(el).outlineStyle!="none"')
                for formula in parent.locator('math').all():
                    assert formula.evaluate('(el)=>el.getBoundingClientRect().height>0'),(i,'invisible MathML')
                assert layout(page)['pageWidth']<=metrics['viewport']+1,(i,'reader leaks horizontally')
                page.keyboard.press('Space'); assert not parent.evaluate('(el)=>el.open');toggles+=2
            for i in range(articles.count()):
                item=articles.nth(i);slot=item.get_attribute('id');assert slot
                assert item.locator('[data-question] math').count()==item.locator('[data-question] math:visible').count()
                if sheets:
                    local=reader.parent/'question-sheets'/(slot+'.html');sheet=ctx.new_page();sheet.goto(local.as_uri());m=layout(sheet)
                    assert m['pageWidth']<=m['viewport']+1 and m['formulas']==m['annotations'] and m['mathErrors']==0,(slot,m)
                    assert sheet.locator('details,script,a,input').count()==0;sheet.close()
            assert external==[] and errors==[],(external,errors)
            out['viewports'].append(dict(metrics,articles=articles.count(),keyboard_toggles=toggles,standalone_sheets_checked=articles.count() if sheets else 0));ctx.close()
        browser.close()
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader',type=Path,default=Path(__file__).resolve().with_name('reader.html'))
    parser.add_argument('--chromium',type=Path)
    parser.add_argument('--reader-only',action='store_true',help='Skip standalone participant sheets when testing an earlier handoff.')
    args=parser.parse_args();print(json.dumps(check(args.reader.resolve(),args.chromium,not args.reader_only),indent=2))
