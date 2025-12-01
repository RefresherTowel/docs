(() => {
  const toc = document.querySelector(".sticky-toc");
  if (!toc) return;

  console.log("[toc-scrollspy] loaded");

  const links = Array.from(toc.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  const safeDecode = (s) => {
    try { return decodeURIComponent(s); } catch { return s; }
  };

  const items = links
    .map((a) => {
      const href = a.getAttribute("href");
      if (!href || !href.startsWith("#")) return null;

      const id = safeDecode(href.slice(1));
      const el = document.getElementById(id);
      if (!el) return null;

      return { id, el, a, li: a.closest("li") };
    })
    .filter(Boolean);

  if (!items.length) return;

  // Sort by document position (safer than TOC order if anything weird happens)
  items.sort((x, y) => x.el.compareDocumentPosition(y.el) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1);

  const HEADER_OFFSET_PX = 110; // tweak to taste

  const clearActive = () => {
    for (const it of items) {
      it.a.classList.remove("is-active");
      it.li?.classList.remove("is-active");
    }
  };

  const setActive = (id) => {
    clearActive();
    const it = items.find((x) => x.id === id);
    if (!it) return;

    it.a.classList.add("is-active");
    it.li?.classList.add("is-active");

    // Keep active item visible in the TOC (nice for very long API lists)
    const tocBox = toc;
    const linkBox = it.a.getBoundingClientRect();
    const tocRect = tocBox.getBoundingClientRect();
    if (linkBox.top < tocRect.top || linkBox.bottom > tocRect.bottom) {
      it.a.scrollIntoView({ block: "nearest" });
    }
  };

  const pickCurrent = () => {
    // last heading whose top edge has passed our offset line
    let current = items[0].id;

    for (const it of items) {
      const top = it.el.getBoundingClientRect().top;
      if (top <= HEADER_OFFSET_PX) current = it.id;
      else break;
    }

    return current;
  };

  let raf = 0;
  const schedule = () => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      setActive(pickCurrent());
    });
  };

  // Attach listeners to both window and likely scroll containers used by Just the Docs.
  const candidates = [
    window,
    document,
    document.scrollingElement,
    document.querySelector(".main-content-wrap"),
    document.querySelector(".main"),
    document.querySelector(".site-wrap"),
  ].filter(Boolean);

  const unique = [];
  for (const c of candidates) if (!unique.includes(c)) unique.push(c);

  for (const target of unique) {
    try {
      target.addEventListener("scroll", schedule, { passive: true });
    } catch {
      // ignore targets that don't support addEventListener
    }
  }

  window.addEventListener("resize", schedule);
  window.addEventListener("hashchange", schedule);

  // Initial highlight
  schedule();
})();
