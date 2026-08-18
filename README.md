# Archived sidebar fix

This patch fixes archived/versioned pages collapsing the active library in the
Just the Docs sidebar.

It also fixes a more important long-term problem: an archived version now uses
its own archived page tree in the sidebar instead of borrowing the live/current
library's child navigation. That matters once Current is replaced by breaking-
change documentation with different page names or structure.

## Install

Copy the patch into the docs root, replacing the existing files when asked.

Because your seven old versions are already archived, run this once:

```powershell
python .\tools\rebuild_archive_nav.py
```

Then restart Jekyll:

```powershell
bundle exec jekyll serve --livereload --config _config.yml,_config_local.yml
```

Hard-refresh the browser with Ctrl+F5.

Future calls to `archive_docs_version.py` generate each archive's `nav.json`
automatically, so the rebuild command is only needed for archives that already
exist today.
