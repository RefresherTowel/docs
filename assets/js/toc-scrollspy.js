(() => {
  const toc = document.querySelector(".sticky-toc");
  if (!toc) return;

  console.log("[toc-scrollspy] loaded");

  const ScrollTocLinkToCenter = (linkEl) => {
    // Only relevant if the TOC panel is actually scrollable
    if (toc.scrollHeight <= toc.clientHeight + 1) return;

    // Only recenter if it's drifting toward edges (reduces jitter)
    const edgePadding = 40;

    const tocRect = toc.getBoundingClientRect();
    const linkRect = linkEl.getBoundingClientRect();

    const linkTop = linkRect.top - tocRect.top;
    const linkBottom = linkRect.bottom - tocRect.top;

    const alreadyComfortable =
      linkTop >= edgePadding && linkBottom <= (toc.clientHeight - edgePadding);

    if (alreadyComfortable) return;

    const reduceMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
    const behavior = reduceMotion ? "auto" : "smooth";

    // link's top position within the TOC scroll content
    const linkTopInToc = linkTop + toc.scrollTop;
    const linkCenter = linkTopInToc + (linkRect.height * 0.5);

    // target scrollTop to center that link
    let target = linkCenter - (toc.clientHeight * 0.5);

    // clamp
    const maxScroll = toc.scrollHeight - toc.clientHeight;
    if (target < 0) target = 0;
    if (target > maxScroll) target = maxScroll;

    toc.scrollTo({ top: target, behavior });
  };

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

  // Keep order consistent with document layout
  items.sort((x, y) => (x.el.offsetTop || 0) - (y.el.offsetTop || 0));

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

    ScrollTocLinkToCenter(it.a);
  };

  const pickCurrent = () => {
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

  // Listen to possible scrollers (Just the Docs often scrolls .main-content-wrap)
  const candidates = [
    window,
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
    } catch {}
  }

  window.addEventListener("resize", schedule);
  window.addEventListener("hashchange", schedule);

  schedule();
})();
