#!/usr/bin/env python3
"""Archive one library's current docs into an immutable version folder.

Run from the Jekyll docs root, for example:
    python .\tools\archive_docs_version.py --library fate --version 1.0.1

The script intentionally uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path, PurePosixPath

LIBRARIES = {"catalyst", "echo", "pulse", "statement", "whisper", "fate", "quill"}


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        raise ValueError("Markdown file has no YAML front matter")
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n?", text, re.S)
    if not match:
        raise ValueError("Could not parse YAML front matter")
    return match.group(1), text[match.end():]


def set_frontmatter_value(frontmatter: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^(\s*{re.escape(key)}\s*:).*$", re.M)
    line = f"{key}: {value}"
    if pattern.search(frontmatter):
        return pattern.sub(line, frontmatter, count=1)
    if frontmatter and not frontmatter.endswith("\n"):
        frontmatter += "\n"
    return frontmatter + line


def get_frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.*?)\s*$", frontmatter, re.M)
    if not match:
        return None
    value = match.group(1)
    # Strip inline comments from the current docs' simple title/parent fields.
    value = re.sub(r"\s+#.*$", "", value).strip()
    if (len(value) >= 2) and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value


def archive_root_for(data: dict, library: str, version: str) -> str:
    item = data.get(library, {})
    for version_item in item.get("versions", []):
        if str(version_item.get("id")) == version:
            return version_item["root"]
    return f"/archive/{library}/{version}/"


def preferred_archived_version(data: dict, library: str) -> str | None:
    versions = data.get(library, {}).get("versions", [])
    if not versions:
        return None
    return str(versions[0].get("id"))


def rewrite_target(target: str, current_rel: PurePosixPath, library: str, version: str,
                   source_library_root: Path, data: dict) -> str:
    stripped = target.strip()
    if not stripped or stripped.startswith(("http://", "https://", "mailto:", "#", "{{")):
        return target

    # Assets belong to the live site and are intentionally shared between versions.
    asset_match = re.match(r"^(?:\.\./)+assets/(.+)$", stripped)
    if asset_match:
        asset_path = "/assets/" + asset_match.group(1)
        return "{{ '" + asset_path + "' | relative_url }}"

    # Cross-library links should point at the archived version that existed when
    # this initial snapshot was made, rather than silently taking old readers to
    # breaking current documentation.
    cross = re.match(r"^\.\./(catalyst|echo|pulse|statement|whisper|fate|quill)(?:/(.*))?$", stripped)
    if cross and cross.group(1) != library:
        other_library = cross.group(1)
        rest = cross.group(2) or ""
        other_version = preferred_archived_version(data, other_library)
        if other_version:
            root = archive_root_for(data, other_library, other_version).rstrip("/")
            path = root + ("/" + rest if rest else "/")
            return "{{ '" + path + "' | relative_url }}"

    # A root-relative link may actually be a link to another page inside the same
    # library (the old Echo docs contain one of these). Keep it in this archive.
    if stripped.startswith("/"):
        candidate = source_library_root / stripped.lstrip("/")
        if candidate.exists():
            from_dir = current_rel.parent
            rel = os.path.relpath(candidate.relative_to(source_library_root), from_dir).replace("\\", "/")
            if not rel.startswith("."):
                rel = "./" + rel
            return rel

    return target


def rewrite_links(body: str, current_rel: PurePosixPath, library: str, version: str,
                  source_library_root: Path, data: dict) -> str:
    # Markdown links and images.
    markdown_link = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<suffix>\))")

    def md_replace(match: re.Match) -> str:
        target = match.group("target")
        replacement = rewrite_target(target, current_rel, library, version, source_library_root, data)
        return match.group("prefix") + replacement + match.group("suffix")

    body = markdown_link.sub(md_replace, body)

    # Jekyll {% link library/file.md %} tags resolve against the live source tree.
    # Turn same-library link tags into ordinary relative links so the archive stays
    # inside itself.
    link_tag = re.compile(r"{%\s*link\s+([^%]+?)\s*%}")

    def tag_replace(match: re.Match) -> str:
        target = match.group(1).strip().replace("\\", "/")
        prefix = library + "/"
        if target.startswith(prefix):
            within_library = PurePosixPath(target[len(prefix):])
            rel = os.path.relpath(str(within_library), str(current_rel.parent)).replace("\\", "/")
            if not rel.startswith("."):
                rel = "./" + rel
            return rel
        return match.group(0)

    body = link_tag.sub(tag_replace, body)

    # Basic local HTML src/href paths, if any are added later.
    html_attr = re.compile(r'(?P<prefix>\b(?:src|href)=["\'])(?P<target>[^"\']+)(?P<suffix>["\'])')

    def html_replace(match: re.Match) -> str:
        target = match.group("target")
        replacement = rewrite_target(target, current_rel, library, version, source_library_root, data)
        return match.group("prefix") + replacement + match.group("suffix")

    return html_attr.sub(html_replace, body)


def nav_output_path(rel: PurePosixPath) -> str:
    if rel.name == "index.md":
        parent = rel.parent.as_posix()
        return "" if parent == "." else parent.rstrip("/") + "/"
    return rel.with_suffix(".html").as_posix()


def nav_order_key(value: str | None, title: str) -> tuple:
    if value is None:
        return (1, float("inf"), title.lower())
    try:
        return (0, float(value), title.lower())
    except ValueError:
        return (1, float("inf"), value.lower(), title.lower())


def build_archive_nav(destination: Path, library: str, display_name: str, version: str) -> Path:
    """Write the archived library's own sidebar tree as static JSON.

    Archived pages stay excluded from Just the Docs' global navigation so every
    historical release is not duplicated in every page's sidebar. The browser
    swaps the active live library branch for this small archived tree instead.
    """
    root_title = f"{display_name} v{version}"
    nodes = []

    for path in sorted(destination.rglob("*.md")):
        rel = PurePosixPath(path.relative_to(destination).as_posix())
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = split_frontmatter(text)
        title = get_frontmatter_value(frontmatter, "title")
        if not title:
            continue
        if rel == PurePosixPath("index.md"):
            continue

        nodes.append({
            "title": title,
            "path": nav_output_path(rel),
            "parent": get_frontmatter_value(frontmatter, "parent"),
            "grand_parent": get_frontmatter_value(frontmatter, "grand_parent"),
            "nav_order": get_frontmatter_value(frontmatter, "nav_order"),
            "children": [],
        })

    by_title: dict[str, list[dict]] = {}
    for node in nodes:
        by_title.setdefault(node["title"], []).append(node)

    roots = []
    for node in nodes:
        parent_title = node["parent"]
        if not parent_title or parent_title == root_title:
            roots.append(node)
            continue

        candidates = by_title.get(parent_title, [])
        parent_node = None
        if node["grand_parent"]:
            for candidate in candidates:
                if candidate.get("parent") == node["grand_parent"]:
                    parent_node = candidate
                    break
        if parent_node is None and candidates:
            parent_node = candidates[0]

        if parent_node is None:
            # Do not make a historical page disappear just because its old
            # front matter was unconventional. Put it at the library root.
            roots.append(node)
        else:
            parent_node["children"].append(node)

    def sort_nodes(items: list[dict]) -> None:
        items.sort(key=lambda node: nav_order_key(node.get("nav_order"), node["title"]))
        for node in items:
            sort_nodes(node["children"])

    sort_nodes(roots)

    def public_node(node: dict) -> dict:
        result = {
            "title": node["title"],
            "path": node["path"],
        }
        if node["children"]:
            result["children"] = [public_node(child) for child in node["children"]]
        return result

    payload = {
        "library": library,
        "version": version,
        "items": [public_node(node) for node in roots],
    }
    output = destination / "nav.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output


def process_markdown(path: Path, rel: PurePosixPath, library: str, display_name: str,
                     version: str, source_library_root: Path, data: dict) -> None:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)

    root_title = f"{display_name} v{version}"
    original_parent = get_frontmatter_value(frontmatter, "parent")

    frontmatter = set_frontmatter_value(frontmatter, "nav_exclude", "true")
    frontmatter = set_frontmatter_value(frontmatter, "search_exclude", "true")
    frontmatter = set_frontmatter_value(frontmatter, "doc_library", library)
    frontmatter = set_frontmatter_value(frontmatter, "doc_version", f'"{version}"')

    if rel == PurePosixPath("index.md"):
        frontmatter = set_frontmatter_value(frontmatter, "title", root_title)
    elif original_parent == display_name:
        frontmatter = set_frontmatter_value(frontmatter, "parent", root_title)
    elif original_parent:
        # Nested pages (currently Echo Chamber) can have a parent title duplicated
        # between Current and the archive. The archived grand parent disambiguates it.
        frontmatter = set_frontmatter_value(frontmatter, "grand_parent", root_title)

    body = rewrite_links(body, rel, library, version, source_library_root, data)
    path.write_text("---\n" + frontmatter.rstrip() + "\n---\n" + body, encoding="utf-8")


def update_version_data(data_path: Path, library: str, version: str, display_name: str) -> dict:
    if data_path.exists():
        data = json.loads(data_path.read_text(encoding="utf-8"))
    else:
        data = {}

    entry = data.setdefault(library, {
        "name": display_name,
        "current_root": f"/{library}/",
        "versions": []
    })
    entry.setdefault("name", display_name)
    entry.setdefault("current_root", f"/{library}/")
    versions = entry.setdefault("versions", [])

    if not any(str(item.get("id")) == version for item in versions):
        versions.insert(0, {
            "id": version,
            "label": f"v{version}",
            "root": f"/archive/{library}/{version}/"
        })
        data_path.parent.mkdir(parents=True, exist_ok=True)
        data_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    return data


def archive_library(site_root: Path, library: str, version: str, force: bool = False) -> Path:
    site_root = site_root.resolve()
    source = site_root / library
    if not source.is_dir():
        raise FileNotFoundError(f"Library docs folder does not exist: {source}")

    data_path = site_root / "_data" / "doc_versions.json"
    existing_data = json.loads(data_path.read_text(encoding="utf-8")) if data_path.exists() else {}
    display_name = existing_data.get(library, {}).get("name", library.capitalize())
    data = update_version_data(data_path, library, version, display_name)

    destination = site_root / "archive" / library / version
    if destination.exists():
        if not force:
            raise FileExistsError(
                f"Archive already exists: {destination}\n"
                "Refusing to overwrite an immutable documentation snapshot."
            )
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)

    markdown_files = sorted(destination.rglob("*.md"))
    for file_path in markdown_files:
        rel = PurePosixPath(file_path.relative_to(destination).as_posix())
        process_markdown(file_path, rel, library, display_name, version, source, data)

    build_archive_nav(destination, library, display_name, version)

    # Sanity check for the link forms that are known to break after moving deeper.
    leftovers = []
    for file_path in markdown_files:
        text = file_path.read_text(encoding="utf-8")
        if re.search(r"\]\((?:\.\./)+assets/", text):
            leftovers.append(f"{file_path}: relative asset link")
        if re.search(r"{%\s*link\s+" + re.escape(library) + r"/", text):
            leftovers.append(f"{file_path}: live Jekyll link tag")

    if leftovers:
        raise RuntimeError("Archive created but link validation failed:\n" + "\n".join(leftovers))

    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze one library's current docs as a versioned archive.")
    parser.add_argument("--library", required=True, choices=sorted(LIBRARIES))
    parser.add_argument("--version", required=True)
    parser.add_argument("--site-root", default=".", help="Jekyll docs root. Defaults to the current directory.")
    parser.add_argument("--force", action="store_true", help="Replace an existing archive. Use with care.")
    args = parser.parse_args()

    try:
        destination = archive_library(Path(args.site_root), args.library, str(args.version), args.force)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Archived {args.library} v{args.version}")
    print(f"  -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
