#!/usr/bin/env python3
"""Verify the actual deployed reader, not merely a successful Pages API response."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request

ORIGIN = 'https://dakebu.github.io/QuantumComputinglib-QuantumComputingBench/'
ROOT = Path(__file__).resolve().parents[2]


def fetch(path: str, commit: str) -> bytes:
    url = ORIGIN + path + '?publication=' + commit
    request = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if not response.geturl().startswith(ORIGIN):
            raise ValueError('live reader redirected outside the project origin')
        content = response.read(8_000_001)
    if len(content) > 8_000_000:
        raise ValueError('oversized live verification response')
    return content


def check(commit: str) -> dict:
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('expected a pinned 40-character commit')
    report = json.loads(fetch('build-report.json', commit))
    if report.get('commit') != commit or not report.get('leanGate', {}).get('passed'):
        raise ValueError('the expected proof-backed reader version is not live yet')
    from website.scripts.proof_inputs import proof_input_digest, lean_module_targets
    gate = report['leanGate']
    if gate.get('proofInputsSha256') != proof_input_digest(ROOT) or gate.get('compiledModules') != lean_module_targets(ROOT):
        raise ValueError('live proof inputs or compiled module inventory differ')
    from website.scripts.research_atlas import FILES, load_catalog, public_catalog
    expected_catalogue = public_catalog(load_catalog(ROOT / 'website/research'))
    catalogue = {}
    for name, filename in FILES.items():
        actual = json.loads(fetch('data/research/' + filename, commit))
        if actual != expected_catalogue[name]:
            raise ValueError('live canonical source mismatch: ' + filename)
        catalogue[filename] = actual
    curriculum = json.loads(fetch('data/curriculum-parts.json', commit))
    expected_curriculum = json.loads((ROOT / 'website/curriculum-parts.json').read_text(encoding='utf-8'))
    if curriculum != expected_curriculum or len(curriculum.get('parts', [])) != 4:
        raise ValueError('live four-part curriculum differs from the canonical catalog')
    routes = {'lean-graph/index.html': 'Underlying Lean Graph of Libraries',
              'mathematical-methods/index.html': 'Mathematical methods',
              'functor-hypergraph/index.html': 'Functor Hypergraph',
              'state-preparation-wiki/index.html': 'StatePreparationWiki',
              'progress/index.html': 'Current Progress',
              'research-protocol/index.html': 'ASPBE publication and graph protocol',
              'index.html': 'four peer parts',
              'learning/index.html': 'Four peer textbook parts'}
    for part in curriculum['parts']:
        routes[part['route'] + 'index.html'] = part['title']
    for family in catalogue['atlas.json']['families']:
        routes['mathematical-methods/' + family['id'].split(':', 1)[1] + '/index.html'] = family['label']
    for route in catalogue['state-preparation-wiki.json']['routes']:
        routes['state-preparation-wiki/' + route['id'] + '/index.html'] = route['title']
    for path, label in routes.items():
        text = fetch(path, commit).decode('utf-8')
        if label.casefold() not in html.unescape(text).casefold() or commit[:12] not in text:
            raise ValueError('missing page title/version: ' + path)
        if not all(marker in text for marker in ('data-taxonomy-nav="papers"', 'data-taxonomy-nav="example-cases"', 'research-nav:start')):
            raise ValueError('incomplete common navigation: ' + path)
    progress = json.loads(fetch('data/research/progress.json', commit))
    browser = json.loads(fetch('data/research/browser-report.json', commit))
    if progress.get('commit') != commit or not progress.get('paper_frontier'):
        raise ValueError('live progress version/source-paper frontier mismatch')
    from website.scripts.research_browser_contract import validate_browser_report
    combinations = validate_browser_report(browser)
    if json.loads(fetch('build-report.json', commit)).get('commit') != commit:
        raise ValueError('live deployment changed during verification')
    return {'passed': True, 'origin': ORIGIN, 'commit': commit,
            'checked_reader_routes': len(routes), 'canonical_sources_match': True,
            'source_author_display_projection_match': True,
            'proof_inputs_match': True, 'browser_combinations': combinations,
            'curriculum_parts_match': True,
            'live_reader_check_only': True}


def main() -> None:
    import sys
    sys.path.insert(0, str(ROOT))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--attempts', type=int, default=12)
    parser.add_argument('--output', type=Path, default=ROOT / '_out/live-reader.json')
    args = parser.parse_args()
    attempts = max(1, min(args.attempts, 20))
    for i in range(attempts):
        try:
            result = check(args.commit)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, indent=2))
            return
        except (OSError, ValueError, KeyError) as error:
            print(f'Live verification {i + 1}/{attempts}: {error}', flush=True)
            if i + 1 == attempts:
                raise SystemExit('Live reader verification failed; no deployment verification claimed.') from error
            time.sleep(10)


if __name__ == '__main__':
    main()
