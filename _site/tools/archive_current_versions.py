#!/usr/bin/env python3
"""Freeze the exact pre-breaking-change docs supplied on 2026-08-19."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from archive_docs_version import archive_library

VERSIONS = {
    "catalyst": "1.1.0",
    "echo": "2.3.1",
    "pulse": "2.0.0",
    "statement": "1.3.7",
    "whisper": "1.0.5",
    "fate": "1.0.1",
    "quill": "1.0.3",
}


def main() -> int:
    site_root = Path(__file__).resolve().parent.parent
    print("Freezing the current pre-breaking-change documentation:\n")
    for library, version in VERSIONS.items():
        try:
            destination = archive_library(site_root, library, version)
        except Exception as exc:
            print(f"ERROR while archiving {library} v{version}: {exc}", file=sys.stderr)
            return 1
        print(f"  {library:<10} v{version:<8} -> {destination.relative_to(site_root)}")

    print("\nDone. The live library folders have not been changed.")
    print("You can now replace those live folders with the new documentation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
