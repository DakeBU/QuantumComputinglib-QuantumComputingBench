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
  function revealFormalCompanion() {
    if (!["#lean", "#course"].includes(location.hash)) return;
    const panel = document.getElementById(location.hash.slice(1));
    if (panel instanceof HTMLDetailsElement) {
      panel.open = true;
      panel.scrollIntoView({ block: "start" });
    }
  }
  function start() {
    prepareDisclosures();
    revealFormalCompanion();
    window.addEventListener("hashchange", revealFormalCompanion);
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
