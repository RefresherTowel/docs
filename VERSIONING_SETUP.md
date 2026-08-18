# Documentation versioning: initial migration

This folder contains only the machinery needed to preserve the existing library documentation before replacing the live pages with the new breaking-change documentation.

It does **not** include the API-reference generator.

## What will be archived

The one-shot archive command freezes the current live folders as:

- Catalyst v1.1.0
- Echo v2.3.1
- Pulse v2.0.0
- Statement v1.3.7
- Whisper v1.0.5
- Fate v1.0.1
- Quill v1.0.3

The archive paths are:

```text
archive/catalyst/1.1.0/
archive/echo/2.3.1/
archive/pulse/2.0.0/
archive/statement/1.3.7/
archive/whisper/1.0.5/
archive/fate/1.0.1/
archive/quill/1.0.3/
```

The live folders (`catalyst/`, `fate/`, etc.) are **not changed** by the archive command.

## First-time setup

Copy the contents of this patch into the root of the current docs repository. Merge the folders; do not put this patch inside its own subfolder.

After copying, the important new/replaced files are:

```text
_data/doc_versions.json
_includes/header_custom.html
_includes/head_custom.html
assets/css/docs-versioning.css
assets/js/docs-versioning.js
tools/archive_docs_version.py
tools/archive_current_versions.py
tools/rebuild_archive_nav.py
VERSIONING_SETUP.md
```

`_includes/head_custom.html` is a replacement for the existing file, but it keeps the existing `toc-scrollspy.js` include and adds the versioning CSS/JS after it.

No Python packages are required. The archive scripts use only the Python standard library.

## Freeze all current documentation now

Before doing this, commit or otherwise back up the current docs repository. The archive operation is intentionally non-destructive, but having a clean commit makes the migration easy to inspect and undo.

Open PowerShell in the docs repository root and run:

```powershell
python .\tools\archive_current_versions.py
```

Expected output begins like:

```text
Freezing the current pre-breaking-change documentation:

  catalyst   v1.1.0    -> archive/catalyst/1.1.0
  echo       v2.3.1    -> archive/echo/2.3.1
  pulse      v2.0.0    -> archive/pulse/2.0.0
  statement  v1.3.7    -> archive/statement/1.3.7
  whisper    v1.0.5    -> archive/whisper/1.0.5
  fate       v1.0.1    -> archive/fate/1.0.1
  quill      v1.0.3    -> archive/quill/1.0.3
```

The script refuses to overwrite an archive that already exists. This is deliberate: versioned documentation should be treated as an immutable snapshot.

## Test locally before replacing the live docs

Run the site using your normal local Jekyll command. With the local config we set up earlier that is:

```powershell
bundle exec jekyll serve --livereload --config _config.yml,_config_local.yml
```

Then open the site and test at least one current and archived page for every library.

For example, with `baseurl: ""` in the local override:

```text
http://127.0.0.1:4000/fate/
http://127.0.0.1:4000/archive/fate/1.0.1/
```

On GitHub Pages, with the production `/docs` base URL, those become:

```text
https://refresher-towel.github.io/docs/fate/
https://refresher-towel.github.io/docs/archive/fate/1.0.1/
```

Each library page should now have a version picker in the top header. Before you replace the live docs, `Current` and the archived version contain the same documentation. That is expected.

## What the archive command changes in the copied pages

The archive script copies each library folder and then adjusts only the archived copy.

It:

1. marks archived pages `nav_exclude: true`, so every historical release does not get duplicated into the global Just the Docs sidebar;
2. marks them `search_exclude: true`, so normal site search does not return a mixture of current and historical API results;
3. gives the archived root a versioned title such as `Fate v1.0.1`;
4. adjusts parent metadata so archived child-page relationships remain coherent;
5. rewrites shared asset links back to the site's normal `/assets/` folder, so images are not duplicated for every version;
6. rewrites same-library Jekyll `{% link ... %}` tags so they stay inside the archived version;
7. rewrites the few existing cross-library relative documentation links to the matching archived versions from this snapshot;
8. writes a small `nav.json` beside the archived pages containing that release's own sidebar tree.

While a reader is on an archived page, the versioning JavaScript keeps the normal top-level library entry in the same place, expands it automatically, and swaps its children for the archived release's `nav.json` tree. This means an old release keeps its own Quickstart/API/etc. navigation even after Current is reorganised for a breaking release. The current archived page is highlighted and its ancestor branch stays expanded after every navigation.


## One-time sidebar upgrade for archives created before `nav.json`

If you created your archives using the first versioning patch, the archive folders already exist but do not yet contain the sidebar snapshots described above. After copying the updated versioning files, run this once from the docs root:

```powershell
python .\tools\rebuild_archive_nav.py
```

It creates one `nav.json` in every existing version folder without changing any archived Markdown page. Then restart Jekyll and hard-refresh the browser. Future calls to `archive_docs_version.py` create `nav.json` automatically, so this migration command is not part of the normal release workflow.

## After the archives look correct

Commit the archives and versioning machinery **before** replacing the live docs. That gives you a clean historical checkpoint.

Then replace the live folders with the newly rewritten documentation:

```text
catalyst/
echo/
pulse/
statement/
whisper/
fate/
quill/
```

Do not edit the corresponding `archive/...` folders when updating Current.

After replacing the live docs, the selector will naturally mean:

```text
Current    -> the new breaking-change documentation
v1.0.1     -> the old Fate documentation
```

and similarly for each library.

## Archive one library in the future

The general rule is:

> Archive the live docs **while they still describe the release you are freezing**, then replace Current with the next release's docs.

For example, if Fate's live docs eventually describe v2.0.0 and you are about to replace them with v3 docs:

```powershell
python .\tools\archive_docs_version.py --library fate --version 2.0.0
```

That creates:

```text
archive/fate/2.0.0/
```

and adds `v2.0.0` to `_data/doc_versions.json` automatically.

Other examples:

```powershell
python .\tools\archive_docs_version.py --library statement --version 2.0.0
python .\tools\archive_docs_version.py --library pulse --version 3.0.0
python .\tools\archive_docs_version.py --library catalyst --version 2.1.0
```

Valid library ids are:

```text
catalyst
echo
pulse
statement
whisper
fate
quill
```

## If you accidentally archive the wrong content

The tool deliberately refuses to overwrite an existing archive. If you have not committed/published it yet and genuinely need to redo the snapshot, delete that archive folder manually and remove its entry from `_data/doc_versions.json`, then run the archive command again.

Do not use the script's `--force` option on a version that has already been published unless you explicitly want to rewrite historical documentation.

## The version data file

`_data/doc_versions.json` drives the dropdown. It is intentionally plain JSON so the versioning system has no PyYAML dependency.

A library entry looks like:

```json
"fate": {
  "name": "Fate",
  "current_root": "/fate/",
  "versions": [
    {
      "id": "1.0.1",
      "label": "v1.0.1",
      "root": "/archive/fate/1.0.1/"
    }
  ]
}
```

Normally you do not need to edit this by hand; `archive_docs_version.py` adds future versions for you.
