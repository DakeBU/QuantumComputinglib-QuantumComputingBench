/* Progressive enhancement: all exercise links work without JavaScript. */
(() => {
  "use strict";
  let mathQueue = Promise.resolve();
  window.qcbMathReady = () => mathQueue;
  function prepareDisclosures() {
    const render = (panel) => {
      if (!panel.open) return;
      const content = panel.querySelector(':scope > [data-qcb-math-deferred]');
      if (!content || content.dataset.qcbMathState) return;
      content.classList.remove('tex2jax_ignore');
      content.dataset.qcbMathState = 'rendering';
      mathQueue = mathQueue.then(async () => {
        await window.MathJax.startup.promise;
        await window.MathJax.typesetPromise([content]);
        content.dataset.qcbMathState = 'ready';
      });
      mathQueue.catch(() => { content.dataset.qcbMathState = 'error'; });
    };
    document.querySelectorAll('details.qcb-disclosure').forEach((panel) => {
      panel.addEventListener('toggle', () => render(panel));
      render(panel);
    });
  }
  function revealLinkedPanel() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    // Deep links remain useful after progressive disclosure, including nested dossiers.
    for (let node = target; node; node = node.parentElement) {
      if (node instanceof HTMLDetailsElement) node.open = true;
    }
    target.scrollIntoView({ block: "start" });
  }
  function prepareTaskSearch() {
    const form = document.querySelector('[data-qcb-task-filters]');
    if (!form) return;
    const rows = [...document.querySelectorAll('[data-task-row]')];
    const query = form.querySelector('[data-task-query]');
    const parts = form.querySelector('[data-task-part]');
    const splits = form.querySelector('[data-task-split]');
    const kinds = form.querySelector('[data-task-kind]');
    const bands = form.querySelector('[data-task-band]');
    const views = form.querySelector('[data-task-view]');
    const count = form.querySelector('[data-task-count]');
    const pager = document.querySelector('[data-task-pages]');
    const previous = pager.querySelector('[data-task-prev]');
    const next = pager.querySelector('[data-task-next]');
    const pageLabel = pager.querySelector('[data-task-page]');
    let page = 0;
    const size = 15;
    function update(reset = true) {
      if (reset) page = 0;
      const terms = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const matches = rows.filter(row => terms.every(t => row.dataset.search.includes(t))
        && (!parts.value || parts.value === row.dataset.part)
        && (!splits.value || splits.value === row.dataset.split)
        && (!kinds.value || kinds.value === row.dataset.kind)
        && (!bands.value || bands.value === row.dataset.band)
        && (!views.value || row.dataset.lean === 'true'));
      const pages = Math.max(1, Math.ceil(matches.length / size));
      page = Math.max(0, Math.min(page, pages - 1));
      rows.forEach(row => { row.hidden = true; });
      matches.slice(page * size, (page + 1) * size).forEach(row => { row.hidden = false; });
      count.textContent = `${matches.length} of ${rows.length} mathematical cores`;
      pageLabel.textContent = matches.length ? `Page ${page + 1} of ${pages}` : 'No matches';
      previous.disabled = page === 0;
      next.disabled = page === pages - 1;
      document.querySelector('[data-task-empty]').hidden = matches.length !== 0;
    }
    form.hidden = false; pager.hidden = false;
    form.addEventListener('submit', e => { e.preventDefault(); update(); });
    form.addEventListener('input', () => update());
    form.addEventListener('change', () => update());
    previous.addEventListener('click', () => { page--; update(false); });
    next.addEventListener('click', () => { page++; update(false); });
    update();
  }
  function start() {
    prepareDisclosures();
    prepareTaskSearch();
    revealLinkedPanel();
    window.addEventListener("hashchange", revealLinkedPanel);
    const controls = document.querySelector("[data-qcb-controls]");
    if (!controls) return;
    const query = controls.querySelector("[data-qcb-query]");
    const count = controls.querySelector("[data-qcb-count]");
    const cards = [...document.querySelectorAll("[data-qcb-card]")];
    controls.hidden = false;
    function update() {
      const terms = query.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      for (const card of cards) {
        const text = card.dataset.qcbSearch.toLocaleLowerCase();
        card.hidden = !terms.every(term => text.includes(term));
        if (!card.hidden) visible++;
      }
      count.textContent = `${visible} of ${cards.length} exercises${visible ? "" : " — no matches"}`;
    }
    query.addEventListener("input", update);
    update();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
