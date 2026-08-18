(function () {
  function normalizeRoot(root) {
    return root.endsWith("/") ? root : root + "/";
  }

  function normalizePath(path) {
    path = path || "";
    path = path.replace(/^\/+/, "");
    if (path === "index.html") return "";
    return path;
  }

  function navPathFromCurrent(activeRoot) {
    var currentPath = window.location.pathname;
    if (currentPath.indexOf(activeRoot) !== 0) return "";
    return normalizePath(currentPath.slice(activeRoot.length));
  }

  function directChild(element, selector) {
    for (var i = 0; i < element.children.length; i++) {
      var child = element.children[i];
      if (child.matches(selector)) return child;
    }
    return null;
  }

  function pathForLink(link) {
    try {
      return new URL(link.href, window.location.origin).pathname;
    } catch (_) {
      return "";
    }
  }

  function findLibraryNavItem(currentRoot) {
    var links = document.querySelectorAll(".site-nav > .nav-list > .nav-list-item > a.nav-list-link[href]");
    for (var i = 0; i < links.length; i++) {
      var path = normalizeRoot(pathForLink(links[i]));
      if (path === currentRoot) return links[i].parentElement;
    }
    return null;
  }

  function makeExpander(title) {
    var button = document.createElement("button");
    button.className = "nav-list-expander btn-reset";
    button.setAttribute("aria-label", "toggle items in " + title + " category");
    button.setAttribute("aria-pressed", "false");
    button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><use xlink:href="#svg-arrow-right"></use></svg>';
    return button;
  }

  function makeArchiveNavList(items, activeRoot, currentSuffix) {
    var list = document.createElement("ul");
    list.className = "nav-list";

    items.forEach(function (item) {
      var li = document.createElement("li");
      li.className = "nav-list-item";

      var itemPath = normalizePath(item.path || "");
      var isCurrent = itemPath === currentSuffix;
      var hasActiveDescendant = false;

      if (item.children && item.children.length) {
        var childList = makeArchiveNavList(item.children, activeRoot, currentSuffix);
        hasActiveDescendant = childList.dataset.containsCurrent === "true";
        li.appendChild(makeExpander(item.title));

        var link = document.createElement("a");
        link.className = "nav-list-link";
        link.href = activeRoot + itemPath;
        link.textContent = item.title;
        if (isCurrent) link.classList.add("active");
        li.appendChild(link);
        li.appendChild(childList);

        if (isCurrent || hasActiveDescendant) {
          li.classList.add("active");
          var expander = directChild(li, ".nav-list-expander");
          if (expander) expander.setAttribute("aria-pressed", "true");
        }
      } else {
        var leafLink = document.createElement("a");
        leafLink.className = "nav-list-link";
        leafLink.href = activeRoot + itemPath;
        leafLink.textContent = item.title;
        if (isCurrent) leafLink.classList.add("active");
        li.appendChild(leafLink);
        if (isCurrent) li.classList.add("active");
      }

      if (isCurrent || hasActiveDescendant) {
        list.dataset.containsCurrent = "true";
      }

      list.appendChild(li);
    });

    return list;
  }

  async function loadArchiveNav(activeRoot) {
    try {
      var response = await fetch(activeRoot + "nav.json", {
        method: "GET",
        cache: "no-store",
        credentials: "same-origin"
      });
      if (!response.ok) return null;
      return await response.json();
    } catch (_) {
      return null;
    }
  }

  function activateRootOnly(navItem, rootLink, activeRoot, currentSuffix) {
    navItem.classList.add("active");
    var expander = directChild(navItem, ".nav-list-expander");
    if (expander) expander.setAttribute("aria-pressed", "true");
    rootLink.href = activeRoot;
    if (!currentSuffix) rootLink.classList.add("active");
  }

  async function installArchiveNavigation(currentRoot, activeRoot) {
    var navItem = findLibraryNavItem(currentRoot);
    if (!navItem) return;

    var rootLink = directChild(navItem, "a.nav-list-link");
    if (!rootLink) return;

    var currentSuffix = navPathFromCurrent(activeRoot);
    var archiveNav = await loadArchiveNav(activeRoot);

    // Even if nav.json is missing, keep the current library expanded and make
    // its root link stay inside the selected archive.
    activateRootOnly(navItem, rootLink, activeRoot, currentSuffix);

    if (!archiveNav || !Array.isArray(archiveNav.items)) return;

    var oldList = directChild(navItem, "ul.nav-list");
    var newList = makeArchiveNavList(archiveNav.items, activeRoot, currentSuffix);

    if (oldList) {
      navItem.replaceChild(newList, oldList);
    } else {
      navItem.appendChild(newList);
    }

    // If this is a child page, the generated list marks the matching child.
    // The live library root remains expanded but does not pretend to be the
    // current page itself.
    if (currentSuffix) rootLink.classList.remove("active");
  }

  async function targetExists(url) {
    try {
      var response = await fetch(url, {
        method: "GET",
        cache: "no-store",
        credentials: "same-origin"
      });
      return response.ok;
    } catch (_) {
      return false;
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var picker = document.querySelector(".docs-version-picker");
    var select = document.getElementById("docs-version-select");
    if (!picker || !select) return;

    var activeRoot = normalizeRoot(picker.dataset.activeRoot || "/");
    var currentRoot = normalizeRoot(picker.dataset.currentRoot || "/");
    var activeVersion = picker.dataset.activeVersion || "current";

    select.addEventListener("change", async function () {
      var selectedRoot = normalizeRoot(select.value);
      var currentPath = window.location.pathname;
      var suffix = "";

      if (currentPath.indexOf(activeRoot) === 0) {
        suffix = currentPath.slice(activeRoot.length);
      }

      var target = selectedRoot + suffix;

      // Keep the reader on the equivalent page when it exists. Page names can
      // change between breaking releases, so fall back to that version's home.
      if (suffix && !(await targetExists(target))) {
        target = selectedRoot;
      }

      window.location.href = target + window.location.hash;
    });

    if (activeVersion !== "current") {
      installArchiveNavigation(currentRoot, activeRoot);
    }
  });
})();
