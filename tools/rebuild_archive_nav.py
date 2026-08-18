#!/usr/bin/env python3
"""Rebuild sidebar nav.json files for documentation archives that already exist.

Run from the Jekyll docs root:
    python .\tools\rebuild_archive_nav.py

This is only needed once when upgrading archives created before archived sidebar
snapshots were added. Future archives generate nav.json automatically.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from archive_docs_version import build_archive_nav


def main() -> int:
    site_root = Path(__file__).resolve().parent.parent
    data_path = site_root / "_data" / "doc_versions.json"
    if not data_path.exists():
        print(f"ERROR: Version data does not exist: {data_path}", file=sys.stderr)
        return 1

    data = json.loads(data_path.read_text(encoding="utf-8"))
    built = 0

    for library, info in data.items():
        display_name = info.get("name", library.capitalize())
        for version_item in info.get("versions", []):
            version = str(version_item.get("id"))
            root = str(version_item.get("root", f"/archive/{library}/{version}/"))
            destination = site_root / root.strip("/")
            if not destination.is_dir():
                print(f"WARNING: Archive folder is missing, skipped: {destination}")
                continue

            output = build_archive_nav(destination, library, display_name, version)
            print(f"  {library:<10} v{version:<8} -> {output.relative_to(site_root)}")
            built += 1

    print(f"\nRebuilt {built} archived navigation snapshot(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
