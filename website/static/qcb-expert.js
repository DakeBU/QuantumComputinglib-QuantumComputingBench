/* Graph review is a projection of recorded relations, never a proof inference. */
(() => {
  "use strict";
  document.querySelectorAll('[data-qcb-expert-filter]').forEach(filter => {
    const input = filter.querySelector('input');
    const rows = [...document.querySelectorAll('[data-qcb-expert-row]')];
    const count = filter.querySelector('[data-qcb-expert-count]');
    function apply() {
      const words = input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      rows.forEach(row => { row.hidden = !words.every(w => row.dataset.search.includes(w)); });
      count.textContent = `${rows.filter(r => !r.hidden).length} of ${rows.length} cited anchors shown`;
    }
    input.addEventListener('input', apply);
    apply();
  });
  const app = document.querySelector('[data-qcb-expert-viewer]');
  if (!app) return;
  const form = app.querySelector('form');
  const input = form.querySelector('input');
  const choices = app.querySelector('datalist');
  const status = app.querySelector('[data-qcb-expert-status]');
  const result = app.querySelector('[data-qcb-expert-result]');
  const prefix = app.dataset.sitePrefix;
  const NS = 'http://www.w3.org/2000/svg';
  let index;
  function el(tag, text, parent, attrs = {}) {
    const n = document.createElement(tag);
    if (text !== null) n.textContent = text;
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    if (parent) parent.append(n);
    return n;
  }
  function svgEl(tag, attrs, parent, text) {
    const n = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v));
    if (text) n.textContent = text;
    parent.append(n);
    return n;
  }
  function graphLink(node, parent) {
    if (node.live_identity === 'present_by_exact_id') {
      el('a', 'Locate exact identity in Lean Graph', parent,
         {href: prefix + 'lean-graph/index.html?focus=' + encodeURIComponent(node.id), 'data-qcb-graph': ''});
    } else el('span', 'Frozen anchor only; no exact live identity was matched.', parent);
  }
  function show(id) {
    result.replaceChildren();
    const node = index.nodes[id];
    if (!node) { status.textContent = 'No exact node identity matched. Select an entry from the list.'; return; }
    input.value = id;
    const url = new URL(location.href); url.searchParams.set('node', id); history.replaceState(null, '', url);
    status.textContent = `Selected exact library identity: ${id}`;
    el('h2', node.label, result);
    el('p', node.module || node.topic, result);
    const source = el('p', null, result);
    graphLink(node, source);
    if (node.frozen_source_url) {
      source.append(document.createTextNode(' · '));
      el('a', 'Frozen source' + (node.source_line ? ':' + node.source_line : ''), source,
         {href: node.frozen_source_url});
    }
    el('p', `${node.inventory_status || node.evidence_class.replaceAll('_', ' ')}. ` + index.source_policy, result);
    const edges = index.structural_edges.filter(e => e.source === id || e.target === id);
    const neighborIds = [...new Set(edges.flatMap(e => [e.source, e.target]))].filter(n => n !== id);
    el('h3', 'Recorded structural neighborhood', result);
    el('p', 'Arrows below retain their recorded type: ownership or module availability. They do not assert theorem entailment.', result);
    if (neighborIds.length) {
      const selected = neighborIds.slice(0, 8);
      const svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('viewBox', '0 0 900 440'); svg.setAttribute('class', 'qcb-expert-svg');
      svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'Recorded local structural neighborhood');
      const diagram = el('div', null, result, {class: 'qcb-expert-scroll', tabindex: '0',
        'aria-label': 'Scrollable library neighborhood; links and complete relations follow below'});
      diagram.append(svg);
      requestAnimationFrame(() => { diagram.scrollLeft = Math.max(0, (900 - diagram.clientWidth) / 2); });
      const defs = svgEl('defs', {}, svg);
      const marker = svgEl('marker', {id: 'qcb-expert-arrow', viewBox: '0 0 10 10', refX: 9,
        refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse'}, defs);
      svgEl('path', {d: 'M 0 0 L 10 5 L 0 10 z', fill: 'var(--muted)'}, marker);
      const positions = {[id]: [340, 190]};
      selected.forEach((n, i) => { positions[n] = [i % 2 ? 650 : 30, 20 + Math.floor(i / 2) * 105]; });
      edges.filter(e => positions[e.source] && positions[e.target]).forEach(e => {
        const [sx, sy] = positions[e.source], [tx, ty] = positions[e.target];
        const line = svgEl('line', {x1: sx < tx ? sx + 200 : sx, y1: sy + 35,
          x2: sx < tx ? tx : tx + 200, y2: ty + 35, class: 'qcb-expert-edge',
          'marker-end': 'url(#qcb-expert-arrow)'}, svg);
        svgEl('title', {}, line, e.label + ': ' + e.source + ' → ' + e.target);
      });
      Object.entries(positions).forEach(([n, [x, y]]) => {
        const link = svgEl('a', {href: '?node=' + encodeURIComponent(n), 'aria-label': index.nodes[n].label}, svg);
        const group = svgEl('g', {class: n === id ? 'qcb-expert-selected' : 'qcb-expert-neighbor'}, link);
        svgEl('rect', {x, y, width: 200, height: 70, rx: 7}, group);
        const name = index.nodes[n].label;
        svgEl('text', {x: x + 10, y: y + 28}, group, name.length > 24 ? name.slice(0, 21) + '…' : name);
        svgEl('text', {x: x + 10, y: y + 51, class: 'qcb-expert-node-kind'}, group, index.nodes[n].kind);
        svgEl('title', {}, group, n);
      });
      if (neighborIds.length > selected.length) el('p', `Diagram shows ${selected.length} of ${neighborIds.length} neighbors. Every recorded relation is listed below.`, result);
      const list = el('ul', null, result);
      edges.forEach(e => {
        const other = index.nodes[e.source === id ? e.target : e.source];
        const row = el('li', e.label + ': ', list);
        el('a', other.label, row, {href: '?node=' + encodeURIComponent(other.id)});
        row.append(document.createTextNode(e.source === id ? ' (outgoing)' : ' (incoming)'));
      });
    } else el('p', 'No recorded structural edge is present in this bounded neighborhood.', result);
    const references = index.reverse_index[id] || [];
    el('h3', 'Questions and views citing this node', result);
    if (!references.length) el('p', 'This node is neighborhood context, not a directly cited question anchor.', result);
    const questions = el('ul', null, result);
    references.forEach(ref => {
      const row = el('li', null, questions);
      el('a', ref.title, row, {href: prefix + ref.href});
      el('small', `${ref.kind.replaceAll('_', ' ')} · ${ref.role.replaceAll('_', ' ')} · ${ref.split}`, row);
    });
    const hyperedges = index.curated_hyperedges.filter(h => [...h.tails, ...h.heads].includes(id));
    if (hyperedges.length) {
      el('h3', 'Curated composition records', result);
      hyperedges.forEach(h => {
        const section = el('section', null, result);
        el('h4', h.label + ' · ' + h.status, section);
        ['mechanism', 'hypothesis_map', 'conclusion_map', 'failure_boundary', 'review'].forEach(k => {
          if (h[k]) el('p', k.replaceAll('_', ' ') + ': ' + h[k], section);
        });
        el('p', 'These are curated records; inspect their stated assumptions and review status.', section);
      });
    }
  }
  form.addEventListener('submit', event => { event.preventDefault(); if (index) show(input.value.trim()); });
  fetch(app.dataset.url).then(r => { if (!r.ok) throw Error('Graph index unavailable'); return r.json(); }).then(data => {
    if (data.schema_version !== 'qcb.expert_graph_index.v1') throw Error('Unsupported graph index');
    index = data;
    Object.values(index.nodes).forEach(n => el('option', n.label, choices, {value: n.id}));
    const requested = new URLSearchParams(location.search).get('node');
    if (requested) show(requested);
    else status.textContent = `Select one of ${index.anchor_node_ids.length} cited anchors, or a recorded context module.`;
  }).catch(error => { status.textContent = error.message + '. Use the static node-to-question index.'; });
})();
