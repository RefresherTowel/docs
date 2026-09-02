# Echo / Echo Chamber current-docs migration

This migration replaces the old live nested Echo Chamber documentation with two sibling current documentation roots:

```text
/echo/
/echo-chamber/
```

The historical `/archive/echo/2.3.1/` snapshot is intentionally unchanged.

## Live page mapping

| Old live route | New current route |
| --- | --- |
| `/echo/reference.html` | `/echo/api-reference.html` |
| `/echo/echo_chamber/` | `/echo-chamber/` |
| `/echo/echo_chamber/usage.html` | `/echo-chamber/getting-started.html` |
| `/echo/echo_chamber/console.html` | `/echo-chamber/console.html` |
| `/echo/echo_chamber/themes.html` | `/echo-chamber/themes.html` |
| `/echo/echo_chamber/advanced.html` | `/echo-chamber/advanced.html` |
| `/echo/echo_chamber/scripting.html` | `/echo-chamber/api-reference.html` |
| `/echo/echo_chamber/style_reference.html` | `/echo-chamber/style-api-reference.html` |

The redirects are implemented with `redirect_from` on the destination pages.

## Site metadata changes

- `_data/doc_versions.json` now knows about `echo-chamber` as its own current docs root.
- `_data/library_footer.yml` has separate Echo and Echo Chamber entries.
- Both footer entries use `product_group: echo`, so they are treated as one distributed product for cross-promotion.
- Echo Chamber uses `show_in_other_stuff: false`, so other library footers advertise Echo once rather than showing two cards that lead to the same product.
- `_includes/library-footer.html` understands `page.library_id`, product groups, and hidden companion entries.
- `_includes/header_custom.html` hides the version selector for a docs family with no archived versions yet. Echo Chamber will automatically gain the selector once its first version is archived.
- `tools/archive_docs_version.py` accepts `echo-chamber` for future archives.

## Generated API references

The docs site now contains:

```text
api-manifests/echo.yml
api-manifests/echo-chamber.yml
api-manifests/echo-chamber-styles.yml
tools/generate_api.py
tools/generate_echo_api.ps1
```

The current sidebar order is:

### Echo
1. Using Echo
2. API Reference

### Echo Chamber
1. Getting Started
2. Echo Console
3. Themes
4. Advanced Usage
5. API Reference
6. Style API Reference

## Validation performed

- all three API manifests regenerated successfully against the migrated Echo source;
- YAML and JSON data files parsed successfully;
- no broken relative Markdown links were found in the live Echo/Echo Chamber pages;
- the old live `echo/echo_chamber/` folder is absent;
- the archived Echo v2.3.1 documentation was not modified.

A full Jekyll render was not run in the migration environment because Bundler was unavailable. Run the normal local Jekyll command before publishing to visually verify navigation, redirects, footer rendering, and the version picker.
