"""Calm reader entry points over the unchanged, frozen site renderer.

This final publication pass moves existing HTML sections intact into native
disclosures. It neither rewrites lesson content nor changes evidence records.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
MARKER = 'data-reader-hierarchy="1"'
PANEL = re.compile(r'<!-- qcb-textbook:start -->.*?<!-- qcb-textbook:end -->', re.S)
NO_SCRIPT = '''<noscript data-reader-mobile-navigation="1"><style>
@media (max-width: 820px) {
  .site-sidebar { position: static; width: 100%; padding-top: 0; transform: none; box-shadow: none; }
  .mobile-header .mobile-menu { display: none; }
}
</style></noscript>'''
GRAPH_LINKS = '''<div class="home-graph-links" aria-label="Explore the two graph views">
  <a href="lean-graph/index.html"><strong>Lean Graph <span aria-hidden="true">&#8594;</span></strong>
    <span>Library modules, imports and declaration branches.</span></a>
  <a href="functor-hypergraph/index.html"><strong>Functor Hypergraph <span aria-hidden="true">&#8594;</span></strong>
    <span>Conceptual transports, required inputs and failure boundaries.</span></a>
</div>'''
HERO_ACTIONS = '''<div class="hero-actions">
  <a class="text-link" href="learning/index.html">Start reading &#8594;</a>
  <a class="text-link" href="quantumcomputingbench/index.html">QuantumComputingBench &#8594;</a>
  <a class="text-link" href="example-cases/index.html">Explore a worked case &#8594;</a>
</div>'''
REVEAL_TARGET = '''<script data-reader-reveal="1">
(() => {
  function revealTarget() {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    for (let node = target.parentElement; node; node = node.parentElement) {
      if (node.tagName === "DETAILS") node.open = true;
    }
    requestAnimationFrame(() => target.scrollIntoView());
  }
  window.addEventListener("hashchange", revealTarget);
  revealTarget();
})();
</script>'''
LAZY_DIAGRAMS = '''
    // Disclosed diagrams need a visible layout before Mermaid measures them.
    let readerDiagramQueue = Promise.resolve();
    function renderReaderDiagrams() {
      readerDiagramQueue = readerDiagramQueue.then(async () => {
        await new Promise(requestAnimationFrame);
        const nodes = [...document.querySelectorAll('.mermaid:not([data-processed])')]
          .filter(node => !node.closest('details:not([open])') && node.getClientRects().length);
        if (nodes.length) await mermaid.run({nodes});
      });
    }
    document.querySelectorAll('.reader-disclosure').forEach(details => {
      details.addEventListener('toggle', () => { if (details.open) renderReaderDiagrams(); });
    });
    renderReaderDiagrams();
'''


@dataclass
class Span:
    tag: str
    attrs: dict[str, str | None]
    start: int
    open_end: int
    parent: int | None
    close_start: int = 0
    end: int = 0

    def has_class(self, name: str) -> bool:
        return name in (self.attrs.get("class") or "").split()


class Spans(HTMLParser):
    """Track source offsets; retain original markup rather than serializing it."""
    def __init__(self, text: str):
        super().__init__(convert_charrefs=False)
        self.text, self.nodes, self.stack = text, [], []
        self.lines = [0]
        self.lines.extend(match.end() for match in re.finditer("\n", text))
        self.feed(text)

    def source_offset(self) -> int:
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_offset()
        node = Span(tag, dict(attrs), start, start + len(self.get_starttag_text()), self.stack[-1] if self.stack else None)
        self.nodes.append(node)
        if tag in VOID_TAGS:
            node.close_start = node.end = node.open_end
        else:
            self.stack.append(len(self.nodes) - 1)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            node = self.nodes[self.stack.pop()]
            node.close_start = node.end = node.open_end

    def handle_endtag(self, tag):
        if not self.stack:
            return
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.nodes[self.stack[i]].tag == tag), None)
        if index is None:
            return
        node = self.nodes[self.stack[index]]
        node.close_start = self.source_offset()
        node.end = self.text.index(">", node.close_start) + 1
        del self.stack[index:]

    def one(self, predicate) -> Span:
        found = [node for node in self.nodes if predicate(node)]
        if len(found) != 1 or not found[0].end:
            raise ValueError("expected one complete reader HTML element")
        return found[0]


def _edit(text: str, changes: list[tuple[int, int, str]]) -> str:
    for start, end, replacement in sorted(changes, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def _disclosure(key: str, title: str, content: str) -> str:
    return (f'<details class="reader-disclosure" data-reader-group="{key}">'
            f'<summary>{title}</summary><div class="reader-disclosure-content">'
            + content + '</div></details>')


def _home_hero(text: str) -> str:
    spans = Spans(text)
    lede = spans.one(lambda n: n.has_class("lede"))
    actions = spans.one(lambda n: n.has_class("hero-actions"))
    folded = [spans.one(lambda n, name=name: n.has_class(name))
              for name in ("hero-scope", "home-book-links", "evidence-note")]
    scope = ('<details class="home-books"><summary>Four textbooks &amp; project scope</summary>'
             + "\n".join(text[node.start:node.end] for node in folded) + '</details>')
    hero = spans.one(lambda n: n.has_class("home-hero"))
    return _edit(text, [(node.start, node.end, "") for node in folded] + [
        (lede.end, lede.end, "\n" + GRAPH_LINKS),
        (actions.start, actions.end, HERO_ACTIONS),
        (hero.close_start, hero.close_start, scope),
    ])


def _home(text: str) -> str:
    panels = PANEL.findall(text)
    if len(panels) > 1:
        raise ValueError("duplicate benchmark home panel")
    text = PANEL.sub("", text)
    spans = Spans(text)
    sections = [node for node in spans.nodes if node.tag == "section" and node.parent is None]
    keyed = {str(node.attrs.get("id") or "hero"): text[node.start:node.end] for node in sections}
    expected = {"hero", "math-2-0", "applications", "state-process", "block-process", "evidence", "pipeline", "use", "news", "chapters", "navigation"}
    if set(keyed) != expected or len(sections) != len(expected):
        raise ValueError("home reader sections changed; inspect before regrouping")
    # Each authored section (including its heading, anchors and diagrams) is
    # copied whole. Only the hero's navigation and duplicated scope are moved.
    groups = (
        ("textbooks", "Textbooks &amp; construction workflows", ("applications", "state-process", "block-process", "chapters")),
        ("evidence", "Build evidence &amp; practical tools", ("evidence", "pipeline", "use", "navigation")),
        ("project", "Project context &amp; news", ("math-2-0", "news")),
    )
    body = _home_hero(keyed["hero"]) + "".join(panels) + "\n"
    body += '<section class="content-section home-explore" id="explore"><h2>Explore further</h2>'
    body += '<p class="hint">Choose an area to open its explanations, diagrams and full catalog.</p>'
    body += "\n".join(_disclosure(key, title, "\n".join(keyed[item] for item in items)) for key, title, items in groups)
    return body + '</section>'


def _learning(text: str) -> str:
    spans = Spans(text)
    changes = []
    for key, title in (
        ("reading-map", "Conceptual reading map"),
        ("chapter-list", "All four chapter maps"),
        ("textbook-explorer", "Search chapters by textbook, technique or proof status"),
        ("future-curriculum", "Curriculum, shared foundations &amp; reading sources"),
    ):
        node = spans.one(lambda n: n.attrs.get("id") == key)
        changes.append((node.start, node.end, _disclosure(key, title, text[node.start:node.end])))
    return _edit(text, changes)


def transform_page(text: str, current: str) -> str:
    """Idempotent final output transformation; the frozen renderer stays intact."""
    if 'data-reader-mobile-navigation="1"' not in text:
        if "</body>" not in text:
            raise ValueError("reader page has no body end")
        text = text.replace("</body>", NO_SCRIPT + "\n</body>", 1)
    if current not in ("index.html", "learning/index.html"):
        return text
    if MARKER in text:
        # A repeated benchmark publication reinserts its exact panel at the
        # beginning of main. Keep that publisher compatible without changing
        # its bytes or moving the benchmark ahead of the global introduction.
        panels = PANEL.findall(text)
        if current == "index.html" and panels:
            if len(panels) != 1:
                raise ValueError("duplicate benchmark home panel")
            text = PANEL.sub("", text)
            hero = Spans(text).one(lambda n: n.has_class("home-hero"))
            text = text[:hero.end] + panels[0] + text[hero.end:]
        return text
    spans = Spans(text)
    main = spans.one(lambda n: n.tag == "main" and n.attrs.get("id") == "main-content")
    original = text[main.open_end:main.close_start]
    body = _home(original) if current == "index.html" else _learning(original)
    text = text[:main.open_end] + '<div class="reader-entry" ' + MARKER + '>' + body + '</div>' + text[main.close_start:]
    if current == "index.html":
        spans = Spans(text)
        toc = spans.one(lambda n: n.has_class("toc"))
        text = _edit(text, [(toc.start, toc.end, "")])
        text = text.replace('class="page-shell"', 'class="page-shell no-toc"', 1)
    # Native disclosures work without JavaScript. Enhancement retains direct
    # fragments and renders Mermaid only when its measured region is visible.
    text = text.replace("</body>", REVEAL_TARGET + "\n</body>", 1)
    module = re.compile(r'(<script type="module">)(.*?import mermaid.*?)(</script>)', re.S)
    if len(module.findall(text)) != 1:
        raise ValueError("expected one Mermaid module in reader page")
    return module.sub(lambda m: m[1] + m[2].replace("startOnLoad: true", "startOnLoad: false", 1) + LAZY_DIAGRAMS + m[3], text, count=1)


def publish(root: Path) -> dict[str, object]:
    """Run after all page publishers and the canonical sidebar replacement."""
    root = Path(root)
    pages, entries = 0, []
    for path in root.rglob("*.html"):
        relative = path.relative_to(root)
        if "blueprint" in relative.parts:
            continue
        text = path.read_text(encoding="utf-8")
        result = transform_page(text, relative.as_posix())
        pages += 1
        if MARKER in result:
            entries.append(relative.as_posix())
        if result != text:
            path.write_text(result, encoding="utf-8")
    return {"schema_version": 1, "entry_routes": sorted(entries), "mobile_navigation_pages": pages}
