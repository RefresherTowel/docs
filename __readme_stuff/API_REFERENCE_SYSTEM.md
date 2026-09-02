# API reference system

The API reference has two sources of information.

The GML source owns facts that should never be copied by hand:

- public constructors, methods, and global functions
- signatures and optional arguments
- parameter types and descriptions
- return types and descriptions
- inheritance
- enum members
- macro names, values, and descriptions

The YAML manifest owns presentation decisions:

- which conceptual section a type belongs to
- method grouping for large types
- ordering
- optional examples
- optional extra notes and returned-struct field descriptions
- explicit See also links
- short enum/member explanations when the source does not carry them
- macro grouping

This keeps the reference tied to the code without asking JSDoc to decide how the docs should be organised.

## Generate Fate

From the docs-site root on Windows:

```powershell
.\tools\generate_fate_api.ps1 -FateRoot "C:\path\to\Fate"
```

Or call the generic generator directly:

```powershell
python tools\generate_api.py `
	--manifest api-manifests\fate.yml `
	--source-root "C:\path\to\Fate" `
	--output fate\api-reference.md
```

The generator exits with an error when the manifest refers to a symbol, enum, or macro that no longer exists. Fate also enables `require_public_coverage`, so a new public top-level Fate symbol or enum must be deliberately placed in the manifest before generation succeeds. Libraries that expose public macros can additionally enable `require_macro_coverage`; `library.macro_prefix` controls which macros that coverage check owns. Large types can enable `require_grouping`, which similarly catches new methods that have not been assigned to a method group.

Methods on types without explicit groups are added automatically in source order. A type that inherits callable public methods from a base constructor can opt into `include_inherited_methods: true`; inherited methods are then rendered as methods of the public child type, with nearer overrides winning. This is primarily useful when the implementation uses internal base constructors to compose a public API.

## Generate Echo and Echo Chamber

Echo, Echo Chamber, and the Echo Chamber style API share one source project but generate three reference pages. From the docs-site root on Windows:

```powershell
.\tools\generate_echo_api.ps1 -EchoRoot "C:\path\to\Echo"
```

This generates:

```text
echo/api-reference.md
echo-chamber/api-reference.md
echo-chamber/style-api-reference.md
```

The three manifests live in `api-manifests/` and use strict public coverage so newly exposed API must be deliberately represented before generation succeeds.

## Manual method metadata

The source remains authoritative for the ordinary reference entry. Manual metadata is only for material the source cannot sensibly provide.

```yaml
symbols:
  FateTable.Roll:
    example: |-
      var _result = loot_table.Roll(new FateRollRequest().SetCount(3))
    see_also:
      - FateTable.Preview
      - FateRollRequest

  FateRollResult.GetTableSummary:
    notes:
      - Table summaries are only retained when detailed capture is enabled.
    fields:
      - name: requested_count
        type: Real
        description: Number of direct selections requested from this table call.
```

`notes`, `fields`, `example`, `return_description`, and `see_also` are all optional.

Macro values and ordinary descriptions come from the source, just like functions and constructors:

```gml
/// @macro EXAMPLE_DEBUG_ENABLED
/// @desc Compile-time switch for the library's debug features.
#macro EXAMPLE_DEBUG_ENABLED 1
```

The manifest decides where the macro appears:

```yaml
macro_sections:
  - title: Configuration
    macros:
      - EXAMPLE_DEBUG_ENABLED
```

A manifest-level `macros.<name>.description` remains available as an exceptional presentation override, but normal API facts should stay in source JSDoc.

## Cross-links

Recognised public API types, enums, macros, and qualified method references in JSDoc are linked automatically. Explicit `see_also` entries are for relationships that are useful to a reader but are not obvious from a signature.

The Symbol index is generated automatically from the represented public API.

## Current Fate prototype

The current Fate manifest represents the complete non-internal Fate-prefixed public surface in the supplied repo. `FateTable`, `FateEntry`, `FateRollResult`, and `FateSimulationChecks` have hand-organised method groups; other types currently use source order so we can judge the full generated page before deciding which additional types benefit from grouping.
