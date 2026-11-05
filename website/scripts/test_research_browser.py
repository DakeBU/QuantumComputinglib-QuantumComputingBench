#!/usr/bin/env python3
"""Browser-level publication checks; screenshots are artifacts, not human review."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import threading
from pathlib import Path

if not __package__:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from website.scripts.research_browser_contract import ROUTES, WIDTHS, THEMES


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def check_blueprint_search(page, base: str) -> None:
    """Exercise emitted modules and the real declaration jump, not just files."""
    name = "QuantumBlockEncoding.HermiteStatePreparation.hermiteStatePreparation_complete"
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(f"{base}/blueprint/html-multi/index.html", wait_until="networkidle", timeout=90000)
    page.wait_for_selector('[role="searchbox"]', timeout=30000)
    mapped = page.evaluate("""async (name) => {
      const module = await import('./-verso-search/domain-mappers.js');
      const domain = '«Informal.LeanCodePreview»';
      const xref = await (await fetch('xref.json')).json();
      const mapped = module.domainMappers[domain].dataToSearchables(xref[domain]);
      return {names: mapped.map(entry => entry.searchKey),
              destination: mapped.find(entry => entry.searchKey === name)?.address};
    }""", name)
    names = mapped["names"]
    destination = mapped["destination"]
    if name not in names or len(names) != len(set(names)) or not destination:
        raise AssertionError("Blueprint search lost the exact root or duplicated declarations")
    # Verso's combobox listens to keyboard events, not a synthetic input fill.
    page.locator('[role="searchbox"]').press_sequentially(name, delay=1)
    # The pinned Verso runtime uses clickable ARIA options, not anchor elements.
    result = page.locator('#cb1-listbox [role="option"].doc-domain').filter(has_text=name).first
    result.wait_for(state="visible", timeout=30000)
    expected_url = page.evaluate("(address) => new URL(address.replace(/^\\//, ''), document.baseURI).href", destination)
    result.click()
    page.wait_for_load_state("networkidle", timeout=90000)
    if page.url != expected_url or not page.evaluate("""() => {
      const anchor = decodeURIComponent(location.hash.slice(1));
      return Boolean(anchor && document.getElementById(anchor));
    }"""):
        raise AssertionError("Blueprint exact declaration jump reached an absent anchor")


def check_curriculum_explorer(page, base: str) -> None:
    """Exercise filters and disclosures on real rendered chapter cards."""
    page.goto(f"{base}/learning/index.html", wait_until="networkidle", timeout=90000)
    page.locator('[data-reader-group="textbook-explorer"] > summary').click()
    cards = page.locator('[data-curriculum-card]')
    total = cards.count()
    if total < 4 or not page.locator('[data-curriculum-controls]').is_visible():
        raise AssertionError('Missing textbook explorer or progressive controls')
    page.locator('select[data-curriculum-part]').select_option('part-iii-quantum-information')
    if page.locator('[data-curriculum-card]:visible').count() != page.locator('[data-curriculum-card][data-part="part-iii-quantum-information"]').count():
        raise AssertionError('Textbook filter changed or lost planned chapter cards')
    page.locator('[data-curriculum-reset]').click()
    page.locator('[data-curriculum-query]').fill('Walsh')
    if not page.locator('[data-curriculum-card]:visible').count():
        raise AssertionError('Walsh source/technique search returned no chapter')
    page.locator('[data-curriculum-query]').fill('not-a-real-chapter-190284')
    if page.locator('[data-curriculum-card]:visible').count() or not page.locator('[data-curriculum-empty]').is_visible():
        raise AssertionError('Empty search is not fail-visible')
    page.locator('[data-curriculum-reset]').click()
    page.locator('[data-curriculum-status]').select_option('Compiled')
    if page.locator('[data-curriculum-card]:visible').count() != page.locator('[data-curriculum-card][data-status="Compiled"]').count():
        raise AssertionError('Compiled filter promoted a planned chapter')
    page.locator('[data-curriculum-reset]').click()
    details = page.locator('.curriculum-intake').first
    details.locator('summary').click()
    if not details.get_by_text('Not local admission', exact=False).first.is_visible():
        raise AssertionError('Expanded upstream memory lost its trust boundary')
    if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'):
        raise AssertionError('Expanded textbook memory overflows mobile viewport')
    if page.locator('[data-curriculum-card]:visible').count() != total:
        raise AssertionError('Reset did not restore all four books')


def check_compact_sidebar(page, base: str) -> None:
    """Check real final publication, disclosure keyboard access and mobile menu."""
    page.set_viewport_size({"width": 1280, "height": 900})
    page.goto(f"{base}/index.html", wait_until="networkidle", timeout=90000)
    nav = page.locator('nav[data-compact-navigation="1"]')
    if nav.count() != 1 or nav.locator('[data-book-part]').count() != 4:
        raise AssertionError("Missing single compact four-textbook sidebar")
    hrefs = nav.locator('a').evaluate_all('(links) => links.map(a => a.href)')
    if len(hrefs) != len(set(hrefs)) or nav.locator('details[open]').count():
        raise AssertionError("Home sidebar duplicated a destination or expanded all content")
    for route in ('lean-graph/', 'functor-hypergraph/'):
        if not nav.locator(f'.sidebar-primary a[href="./{route}index.html"]').is_visible():
            raise AssertionError('Graph entry is hidden in a secondary collection')
    nav.locator('[data-nav-section="research"] > summary').click()
    summary = nav.locator('[data-nav-section="examples"] > summary')
    summary.focus()
    summary.press('Enter')
    if not nav.locator('[data-case="hermite-smooth-state-preparation"]').is_visible():
        raise AssertionError("Keyboard expansion lost the Hermite example")
    summary.press('Enter')
    page.set_viewport_size({"width": 390, "height": 900})
    page.locator('[data-menu-button]').click()
    page.wait_for_function("document.querySelector('.site-sidebar').getBoundingClientRect().left >= -1")
    if page.locator('[data-menu-button]').get_attribute('aria-expanded') != 'true':
        raise AssertionError("Mobile sidebar did not announce its open state")
    page.keyboard.press('Escape')
    page.goto(f"{base}/library/index.html", wait_until="networkidle", timeout=90000)
    if not page.locator('[data-nav-section="textbooks"][open]').count():
        raise AssertionError("Current library page did not open its navigation group")


def check_curriculum_diagram(page, base: str, output: Path) -> None:
    """Check the rendered legend, sparse links and disclosures at both widths."""
    page.goto(f"{base}/index.html", wait_until="networkidle", timeout=90000)
    page.locator('[data-reader-group="textbooks"] > summary').click()
    figure = page.locator('#diagram-quantum-domain-roadmap')
    figure.locator('[data-curriculum-layout="stacked"]').wait_for(state='attached', timeout=30000)
    if figure.locator('[data-curriculum-node="CORE"] h3').text_content() != 'Shared Lean foundations':
        raise AssertionError('Shared foundation label is absent from the rendered diagram')
    if figure.locator('[data-curriculum-link]').count() != 4:
        raise AssertionError('Curriculum diagram lost its four-link compressed structure')
    if figure.locator('[data-curriculum-layout]').get_attribute('aria-label') != 'Textbooks and shared Lean foundations':
        raise AssertionError('Curriculum diagram lost its accessible title')
    for width in WIDTHS:
        page.set_viewport_size({'width': width, 'height': 900})
        for theme in THEMES:
            page.evaluate('theme => document.documentElement.dataset.theme = theme', theme)
            geometry = figure.evaluate('''element => {
              const legend = element.querySelector('.diagram-legend').getBoundingClientRect();
              const graph = element.querySelector('.curriculum-flow').getBoundingClientRect();
              const frame = element.getBoundingClientRect();
              return {outsideGraph: legend.bottom <= graph.top + 1,
                legendFits: legend.left >= frame.left - 1 && legend.right <= frame.right + 1,
                overflow: document.documentElement.scrollWidth > innerWidth + 2,
                textReadable: [...element.querySelectorAll('.curriculum-node p')].every(node => parseFloat(getComputedStyle(node).fontSize) >= 13)};
            }''')
            if not geometry['outsideGraph'] or not geometry['legendFits'] or geometry['overflow'] or not geometry['textReadable']:
                raise AssertionError('Curriculum legend overlaps its graph or page overflows: ' + str(geometry))
            details = figure.locator('.curriculum-transport-notes')
            details.locator('summary').focus()
            details.locator('summary').press('Enter')
            if details.get_attribute('open') is None or not details.get_by_text('nonzero accepted branch', exact=False).is_visible():
                raise AssertionError('Transport conditions are not keyboard accessible')
            if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'):
                raise AssertionError('Expanded curriculum conditions overflow the page')
            details.locator('summary').press('Enter')
            figure.screenshot(path=str(output / f'curriculum-{width}-{theme}.png'))


def check_licensing(page, base: str, output: Path) -> None:
    page.goto(f"{base}/licensing/index.html", wait_until="networkidle", timeout=90000)
    if 'default license is MIT' not in page.locator('main').inner_text():
        raise AssertionError('License guide lost its project MIT boundary')
    for name in ('MIT.txt', 'Apache-2.0.txt', 'NOTICE.md', 'Third-party-notices.md', 'MathJax-LICENSE.txt'):
        if page.locator(f'main a[href="../licenses/{name}"]').count() != 1:
            raise AssertionError('License guide lost a full-text download: ' + name)
    if page.locator('footer a[data-license-link="1"]').count() != 1:
        raise AssertionError('Native license footer entry is missing or duplicated')
    for width in WIDTHS:
        page.set_viewport_size({'width': width, 'height': 900})
        for theme in THEMES:
            page.evaluate('theme => document.documentElement.dataset.theme = theme', theme)
            if page.evaluate('document.documentElement.scrollWidth > innerWidth + 2'):
                raise AssertionError('License guide overflows at ' + str(width) + '/' + theme)
            page.screenshot(path=str(output / f'licensing-{width}-{theme}.png'), full_page=True)


def run(root: Path, output: Path, browser_channel: str | None = None,
        require_blueprint: bool = False) -> None:
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(root.resolve())))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    records = []
    failures = []
    blueprint_passed = False
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel=browser_channel)
            context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
            page = context.new_page()
            page.on("pageerror", lambda error: failures.append(str(error)))
            check_compact_sidebar(page, base)
            check_curriculum_diagram(page, base, output)
            check_licensing(page, base, output)
            page.set_viewport_size({"width": 390, "height": 900})
            check_curriculum_explorer(page, base)
            for width in WIDTHS:
                page.set_viewport_size({"width": width, "height": 900})
                for theme in THEMES:
                    for route in ROUTES:
                        page.goto(f"{base}/{route}/index.html", wait_until="networkidle", timeout=90000)
                        page.evaluate("theme => document.documentElement.dataset.theme = theme", theme)
                        page.wait_for_function("Boolean(window.MathJax && window.MathJax.startup && window.MathJax.startup.promise)", timeout=60000)
                        page.evaluate("async () => { await MathJax.startup.promise; await MathJax.typesetPromise(); }")
                        size = page.evaluate("({width: innerWidth, scroll: document.documentElement.scrollWidth})")
                        if size["scroll"] > width + 2:
                            failures.append(f"global horizontal overflow {route} {width} {theme}: {size}")
                        math_errors = page.locator("mjx-merror").count()
                        if math_errors:
                            failures.append(f"MathJax errors {route}: {math_errors}; " + str(page.locator("mjx-merror").all_text_contents()))
                        if route == "functor-hypergraph":
                            page.wait_for_selector('svg[data-edge-id]', timeout=30000)
                            select = page.locator("[data-ra-edge]")
                            for edge_id, tail_count in (("transport:walsh-loader", 4),
                                                         ("transport:diagonal-filter-state", 3)):
                                select.select_option(edge_id)
                                page.wait_for_function("count => Number(document.querySelector('[data-ra-svg]').dataset.tailCount) === count", arg=tail_count)
                                if page.locator("[data-ra-svg] a").count() != tail_count + 1:
                                    failures.append("AND input set was dropped from " + edge_id)
                            select.select_option("transport:tt-to-sp")
                            page.wait_for_function("document.querySelector('[data-ra-svg]').dataset.tailCount === '3'")
                            if page.locator("[data-ra-svg] a").count() != 4:
                                failures.append("AND input set was dropped from the TT-to-SP graph")
                            page.locator("[data-ra-svg] a").first.focus()
                            if not page.evaluate("document.activeElement.closest('[data-ra-svg]') !== null"):
                                failures.append("SVG nodes are not keyboard-focusable")
                        if route == "mathematical-methods":
                            page.locator("[data-ra-search]").fill("Bernstein")
                            if not page.locator("[data-ra-item]:visible").count():
                                failures.append("mechanism search lost Bernstein")
                            page.locator("[data-ra-search]").fill("a-string-not-present-in-any-card")
                            if page.locator("[data-ra-item]:visible").count():
                                failures.append("mechanism search did not filter cards")
                            page.locator("[data-ra-search]").fill("")
                        page.screenshot(path=str(output / f"{route}-{width}-{theme}.png"), full_page=False)
                        records.append({"route": route, "width": width, "theme": theme, "math_errors": math_errors, "scroll_width": size["scroll"]})
            # Inspect every authored formula route, including source and long-code disclosures.
            for path in sorted((root / "mathematical-methods").glob("*/index.html")) + sorted((root / "state-preparation-wiki").glob("*/index.html")):
                relative = path.relative_to(root).as_posix()
                page.set_viewport_size({"width": 390, "height": 900})
                page.goto(f"{base}/{relative}", wait_until="networkidle", timeout=90000)
                page.wait_for_function("Boolean(window.MathJax && window.MathJax.startup && window.MathJax.startup.promise)", timeout=60000)
                page.evaluate("async () => { await MathJax.startup.promise; await MathJax.typesetPromise(); }")
                if page.locator("mjx-merror").count():
                    failures.append("MathJax error in " + relative)
                if relative == "state-preparation-wiki/spw-uncompute/index.html":
                    layers = page.locator("[data-reading-layer]")
                    if layers.count() != 4 or page.locator("[data-reading-layer][open]").count():
                        failures.append("Uncompute reading depths are missing or all expanded")
                    layers.first.locator("summary").focus()
                    page.keyboard.press("Enter")
                    if not layers.first.get_attribute("open") == "":
                        failures.append("Uncompute reading depth is not keyboard accessible")
                if page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"):
                    failures.append("mobile overflow in " + relative)
            page.goto(f"{base}/mathematical-methods/hermite-bernstein/index.html", wait_until="networkidle", timeout=90000)
            details = page.locator("details.ra-code").first
            details.locator("summary").click()
            if page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"):
                failures.append("expanded Lean source causes page overflow")
            # Exercise the exact declaration link and real imported-edge delta, not only cards.
            name = "QuantumBlockEncoding.ConstructiveHermitePreparation.prepare_spec"
            from urllib.parse import quote
            page.goto(f"{base}/lean-graph/index.html?focus=" + quote("declaration:" + name, safe=""), wait_until="networkidle", timeout=90000)
            page.wait_for_function("document.body.textContent.includes('Focused exact shared identity: declaration:QuantumBlockEncoding.ConstructiveHermitePreparation.prepare_spec')", timeout=30000)
            page.screenshot(path=str(output / "exact-lean-focus.png"), full_page=False)
            page.goto(f"{base}/functor-hypergraph/index.html", wait_until="networkidle", timeout=90000)
            page.wait_for_function("Number(document.querySelector('[data-ra-delta-svg]').dataset.edgeCount) > 0", timeout=30000)
            for width in (390, 1280):
                page.set_viewport_size({"width": width, "height": 900})
                page.locator('[data-ra-hypergraph]').scroll_into_view_if_needed()
                page.screenshot(path=str(output / f"and-graph-{width}.png"), full_page=False)
                page.locator('[data-ra-delta]').scroll_into_view_if_needed()
                page.screenshot(path=str(output / f"contribution-graph-{width}.png"), full_page=False)
            with page.expect_download() as download_event:
                page.locator('[data-ra-download-svg]').click()
            download_event.value.save_as(output / "transport-export.svg")
            if require_blueprint:
                try:
                    check_blueprint_search(page, base)
                    blueprint_passed = True
                    page.screenshot(path=str(output / "blueprint-exact-root.png"), full_page=False)
                except Exception as error:
                    failures.append("Blueprint browser check failed: " + type(error).__name__)
            context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    report = {"automated_browser_checks": records, "failures": failures, "browser_channel": browser_channel or "playwright-chromium", "blueprint_search_required": require_blueprint, "blueprint_search_passed": blueprint_passed, "manual_visual_review": "not asserted by this script"}
    (output / "browser-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Research browser checks failed:\n" + "\n".join(failures))
    print(f"Research browser checks passed: {len(records)} route/viewport/theme combinations and all authored formula pages")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("_out/research-browser"))
    parser.add_argument("--require-blueprint", action="store_true",
                        help="Also check the real Blueprint search and exact-root jump; absence fails.")
    parser.add_argument("--browser-channel", choices=("chrome", "msedge"),
                        help="Use an installed Chromium-family browser; CI defaults to Playwright Chromium.")
    args = parser.parse_args()
    run(args.root.resolve(), args.output, args.browser_channel, args.require_blueprint)
