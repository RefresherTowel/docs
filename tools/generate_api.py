#!/usr/bin/env python3
"""Generate a Just-the-Docs API reference from GameMaker JSDoc plus a small YAML manifest.

The GML source owns signatures, parameter/return types, descriptions, inheritance,
enum members, and macro values/descriptions. The manifest owns ordering, grouping,
examples, notes, and explicit See also relationships.
"""

from __future__ import annotations

import argparse
import dataclasses
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


@dataclasses.dataclass
class Param:
    name: str
    type: str = "Any"
    description: str = ""
    optional: bool = False
    default: str | None = None


@dataclasses.dataclass
class Symbol:
    name: str
    kind: str  # type, method, function
    description: str
    params: list[Param]
    return_type: str = "Undefined"
    return_description: str = ""
    owner: str | None = None
    parent: str | None = None
    source_file: str = ""
    source_line: int = 0
    order: int = 0
    hidden: bool = False

    @property
    def key(self) -> str:
        return f"{self.owner}.{self.name}" if self.owner else self.name


@dataclasses.dataclass
class EnumDef:
    name: str
    members: list[tuple[str, str | None]]
    source_file: str
    source_line: int
    description: str = ""


@dataclasses.dataclass
class MacroDef:
    name: str
    value: str
    source_file: str
    source_line: int
    description: str = ""
    hidden: bool = False


def strip_code_for_braces(line: str) -> str:
    out = []
    i = 0
    quote = None
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            i += 1
            continue
        if ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def find_matching(text: str, start: int, open_ch: str = "(", close_ch: str = ")") -> int:
    depth = 0
    quote = None
    i = start
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    stack: list[str] = []
    pairs = {"(": ")", "[": "]", "{": "}"}
    quote = None
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            current.append(ch)
            if ch == "\\" and i + 1 < len(text):
                current.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
            current.append(ch)
        elif ch in pairs:
            stack.append(pairs[ch])
            current.append(ch)
        elif stack and ch == stack[-1]:
            stack.pop()
            current.append(ch)
        elif ch == delimiter and not stack:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
        i += 1
    if current or text.strip():
        parts.append("".join(current).strip())
    return [p for p in parts if p]


def parse_actual_params(arg_text: str) -> list[Param]:
    result: list[Param] = []
    for raw in split_top_level(arg_text):
        if "=" in raw:
            name, default = raw.split("=", 1)
            name = name.strip()
            default = default.strip()
            optional = True
        else:
            name, default, optional = raw.strip(), None, False
        clean = name[1:] if name.startswith("_") else name
        result.append(Param(name=clean, optional=optional, default=default))
    return result


def parse_doc_block(block: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {"params": [], "ignore": False}
    current_key: tuple[str, int | None] | None = None
    for raw in block:
        text = raw.lstrip()[3:].strip()
        if not text:
            continue
        if text.startswith("@ignore"):
            data["ignore"] = True
            current_key = None
        elif text.startswith("@func"):
            data["func"] = text[len("@func"):].strip()
            current_key = None
        elif text.startswith("@macro"):
            data["macro"] = text[len("@macro"):].strip()
            current_key = None
        elif text.startswith("@desc"):
            data["desc"] = text[len("@desc"):].strip()
            current_key = ("desc", None)
        elif text.startswith("@param"):
            m = re.match(r"@param\s+\{([^}]*)\}\s+([^\s]+)\s*(.*)", text)
            if m:
                name = m.group(2).strip()
                if name.startswith("[") and name.endswith("]"):
                    name = name[1:-1].strip()
                if "=" in name:
                    name = name.split("=", 1)[0].strip()
                if name.startswith("_"):
                    name = name[1:]
                param = {"type": m.group(1).strip(), "name": name, "description": m.group(3).strip()}
                data["params"].append(param)
                current_key = ("param", len(data["params"]) - 1)
        elif text.startswith("@returns") or text.startswith("@return"):
            m = re.match(r"@returns?\s+\{([^}]*)\}\s*(.*)", text)
            if m:
                data["returns"] = {"type": m.group(1).strip(), "description": m.group(2).strip()}
                current_key = ("returns", None)
        elif not text.startswith("@") and current_key:
            key, index = current_key
            if key == "desc":
                data["desc"] = (data.get("desc", "") + " " + text).strip()
            elif key == "param" and index is not None:
                p = data["params"][index]
                p["description"] = (p["description"] + " " + text).strip()
            elif key == "returns":
                r = data["returns"]
                r["description"] = (r["description"] + " " + text).strip()
    return data


def preceding_doc_block(lines: list[str], line_idx: int) -> list[str]:
    """Return the contiguous /// block immediately above line_idx."""
    start = line_idx - 1
    while start >= 0 and lines[start].lstrip().startswith("///"):
        start -= 1
    return lines[start + 1:line_idx]


def doc_block_description(block: list[str]) -> str:
    """Read @desc text, or plain /// prose used by lightweight enum docs."""
    if not block:
        return ""
    parsed = parse_doc_block(block)
    if parsed.get("desc"):
        return str(parsed["desc"])
    prose: list[str] = []
    for raw in block:
        text = raw.lstrip()[3:].strip()
        if text and not text.startswith("@"):
            prose.append(text)
    return " ".join(prose).strip()


def strip_line_comment(line: str) -> str:
    """Remove // comments while preserving string contents for signature parsing."""
    out: list[str] = []
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < len(line):
                out.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _skip_ws(text: str, pos: int) -> int:
    while pos < len(text) and text[pos].isspace():
        pos += 1
    return pos


def _parse_constructor_tail(text: str, pos: int) -> tuple[bool, str | None, int]:
    """Parse optional inheritance then constructor keyword after a function parameter list."""
    pos = _skip_ws(text, pos)
    parent = None
    if pos < len(text) and text[pos] == ":":
        m = re.match(r":\s*([A-Za-z_]\w*)\s*\(", text[pos:])
        if not m:
            return False, None, pos
        parent = m.group(1)
        parent_open = pos + m.end() - 1
        parent_end = find_matching(text, parent_open)
        if parent_end < 0:
            return False, None, pos
        pos = _skip_ws(text, parent_end + 1)
    m = re.match(r"constructor\b", text[pos:])
    if not m:
        return False, parent, pos
    return True, parent, pos + m.end()


def constructor_ranges(lines: list[str]) -> list[tuple[int, int, str, str | None]]:
    """Find constructor body ranges, including declarations split across multiple lines."""
    clean_lines = [strip_code_for_braces(line) for line in lines]
    text = "\n".join(clean_lines)
    line_starts: list[int] = []
    offset = 0
    for line in clean_lines:
        line_starts.append(offset)
        offset += len(line) + 1

    def line_for_offset(char_offset: int) -> int:
        import bisect
        return max(0, bisect.bisect_right(line_starts, char_offset) - 1)

    ranges: list[tuple[int, int, str, str | None]] = []
    for m in re.finditer(r"(?m)^[ \t]*function\s+([A-Za-z_]\w*)\s*\(", text):
        name = m.group(1)
        param_open = text.find("(", m.start())
        param_end = find_matching(text, param_open)
        if param_end < 0:
            continue
        is_constructor, parent, after_constructor = _parse_constructor_tail(text, param_end + 1)
        if not is_constructor:
            continue
        body_open = text.find("{", after_constructor)
        if body_open < 0:
            continue
        body_end = find_matching(text, body_open, "{", "}")
        if body_end < 0:
            body_end = len(text) - 1
        ranges.append((line_for_offset(m.start()), line_for_offset(body_end), name, parent))
    return ranges


def owner_for_line(ranges: list[tuple[int, int, str, str | None]], line_idx: int) -> str | None:
    candidates = [r for r in ranges if r[0] < line_idx <= r[1]]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r[0])[2]


def parse_signature_at(lines: list[str], start_idx: int) -> tuple[str, list[Param], bool, str | None] | None:
    """Parse a top-level function/constructor or static method beginning at start_idx."""
    clean = "\n".join(strip_line_comment(line) for line in lines[start_idx:]).lstrip()
    top = re.match(r"function\s+([A-Za-z_]\w*)\s*\(", clean)
    if top:
        name = top.group(1)
        start = clean.find("(", top.start())
        end = find_matching(clean, start)
        if end < 0:
            return None
        params = parse_actual_params(clean[start + 1:end])
        is_constructor, parent, _ = _parse_constructor_tail(clean, end + 1)
        return name, params, is_constructor, parent
    static = re.match(r"static\s+([A-Za-z_]\w*)\s*=\s*function\s*\(", clean)
    if static:
        name = static.group(1)
        start = clean.find("(", static.start())
        end = find_matching(clean, start)
        if end < 0:
            return None
        return name, parse_actual_params(clean[start + 1:end]), False, None
    return None


def merge_doc_params(actual: list[Param], documented: list[dict[str, str]]) -> list[Param]:
    docs = {p["name"]: p for p in documented}
    merged: list[Param] = []
    for param in actual:
        d = docs.get(param.name, {})
        merged.append(Param(
            name=param.name,
            type=d.get("type", "Any"),
            description=d.get("description", ""),
            optional=param.optional,
            default=param.default,
        ))
    # Preserve documented params if source parsing somehow missed one.
    existing = {p.name for p in merged}
    for d in documented:
        if d["name"] not in existing:
            merged.append(Param(name=d["name"], type=d.get("type", "Any"), description=d.get("description", "")))
    return merged


def parse_gml(source_root: Path, globs: list[str]) -> tuple[dict[str, Symbol], dict[str, EnumDef], dict[str, MacroDef], dict[str, str | None]]:
    symbols: dict[str, Symbol] = {}
    enums: dict[str, EnumDef] = {}
    macros: dict[str, MacroDef] = {}
    parents: dict[str, str | None] = {}
    order = 0
    paths: list[Path] = []
    for pattern in globs:
        paths.extend(source_root.glob(pattern))
    for path in sorted(set(paths)):
        if not path.is_file() or path.suffix.lower() != ".gml":
            continue
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        ranges = constructor_ranges(lines)
        for _, _, constructor_name, parent_name in ranges:
            parents[constructor_name] = parent_name

        # Macros
        for macro_idx, macro_line in enumerate(lines):
            mm = re.match(r"^\s*#macro\s+([A-Za-z_]\w*)\s*(.*)$", strip_line_comment(macro_line))
            if mm:
                macro_name = mm.group(1)
                doc = {}
                doc_start = macro_idx - 1
                while doc_start >= 0 and lines[doc_start].lstrip().startswith("///"):
                    doc_start -= 1
                if doc_start + 1 < macro_idx:
                    candidate = parse_doc_block(lines[doc_start + 1:macro_idx])
                    documented_name = candidate.get("macro")
                    if documented_name == macro_name or (candidate.get("ignore") and not documented_name):
                        doc = candidate
                macros[macro_name] = MacroDef(
                    name=macro_name,
                    value=mm.group(2).strip(),
                    source_file=str(path.relative_to(source_root)),
                    source_line=macro_idx + 1,
                    description=doc.get("desc", ""),
                    hidden=bool(doc.get("ignore")),
                )

        # Enums
        i = 0
        while i < len(lines):
            m = re.match(r"^\s*enum\s+([A-Za-z_]\w*)\s*\{", strip_code_for_braces(lines[i]))
            if not m:
                i += 1
                continue
            name = m.group(1)
            members: list[tuple[str, str | None]] = []
            depth = strip_code_for_braces(lines[i]).count("{") - strip_code_for_braces(lines[i]).count("}")
            j = i + 1
            while j < len(lines) and depth > 0:
                clean = strip_code_for_braces(lines[j]).strip()
                depth += clean.count("{") - clean.count("}")
                if depth >= 1 and clean and not clean.startswith("}"):
                    member = clean.rstrip(",")
                    mm = re.match(r"([A-Za-z_]\w*)\s*(?:=\s*(.*?))?\s*,?$", member)
                    if mm:
                        members.append((mm.group(1), mm.group(2).strip() if mm.group(2) else None))
                j += 1
            enums[name] = EnumDef(
                name=name,
                members=members,
                source_file=str(path.relative_to(source_root)),
                source_line=i + 1,
                description=doc_block_description(preceding_doc_block(lines, i)),
            )
            i = j

        # JSDoc symbols
        i = 0
        while i < len(lines):
            if not lines[i].lstrip().startswith("///"):
                i += 1
                continue
            block: list[str] = []
            start = i
            while i < len(lines) and lines[i].lstrip().startswith("///"):
                block.append(lines[i])
                i += 1
            doc = parse_doc_block(block)
            if "func" not in doc or doc.get("ignore"):
                continue
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                continue
            parsed = parse_signature_at(lines, j)
            if not parsed:
                continue
            name, actual_params, is_constructor, parent = parsed
            owner = None if lines[j].lstrip().startswith("function ") else owner_for_line(ranges, j)
            if owner and name.startswith("__"):
                continue
            if not owner and name.startswith("__"):
                continue
            params = merge_doc_params(actual_params, doc.get("params", []))
            ret = doc.get("returns", {})
            kind = "type" if is_constructor else ("method" if owner else "function")
            order += 1
            sym = Symbol(
                name=name,
                kind=kind,
                description=doc.get("desc", ""),
                params=params,
                return_type=ret.get("type", "Undefined"),
                return_description=ret.get("description", ""),
                owner=owner,
                parent=parent,
                source_file=str(path.relative_to(source_root)),
                source_line=start + 1,
                order=order,
            )
            symbols[sym.key] = sym

        # Keep ignored/internal constructors in the source model as hidden type stubs.
        # A manifest can explicitly document one as opaque (for example, a returned
        # handle) without making its constructor part of the public API.
        for constructor_start, _, constructor_name, parent_name in ranges:
            if constructor_name in symbols:
                continue
            parsed = parse_signature_at(lines, constructor_start)
            if not parsed:
                continue
            name, actual_params, is_constructor, parent = parsed
            if not is_constructor:
                continue
            block = preceding_doc_block(lines, constructor_start)
            doc = parse_doc_block(block) if block else {"params": []}
            params = merge_doc_params(actual_params, doc.get("params", []))
            order += 1
            symbols[name] = Symbol(
                name=name,
                kind="type",
                description=doc.get("desc", doc_block_description(block)),
                params=params,
                parent=parent if parent is not None else parent_name,
                source_file=str(path.relative_to(source_root)),
                source_line=constructor_start + 1,
                order=order,
                hidden=True,
            )
    return symbols, enums, macros, parents


def slug(text: str) -> str:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return text.lower()


def type_anchor(name: str) -> str:
    return slug(name)


def symbol_anchor(symbol: Symbol) -> str:
    if symbol.kind == "method":
        return f"{slug(symbol.owner or '')}-{slug(symbol.name)}"
    return slug(symbol.name)


def enum_anchor(name: str) -> str:
    return f"enum-{slug(name)}"


def macro_anchor(name: str) -> str:
    return f"macro-{slug(name)}"


def signature(symbol: Symbol, constructor: bool = False) -> str:
    args = []
    for p in symbol.params:
        token = p.name
        if p.optional:
            token = f"[{token}]"
        args.append(token)
    prefix = "new " if constructor else ""
    return f"{prefix}{symbol.name}({', '.join(args)})"


def build_link_maps(
    symbols: dict[str, Symbol],
    enums: dict[str, EnumDef],
    macros: dict[str, MacroDef],
    represented: set[str],
    represented_enums: set[str],
    represented_macros: set[str],
) -> tuple[dict[str, str], dict[str, str]]:
    exact: dict[str, str] = {}
    bare: dict[str, str] = {}
    for key in represented:
        sym = symbols[key]
        anchor = symbol_anchor(sym)
        if sym.kind == "method":
            exact[f"{sym.owner}.{sym.name}()"] = anchor
            exact[f"{sym.owner}.{sym.name}"] = anchor
            # Bare method links are intentionally not automatic: method names often repeat across owners.
        else:
            exact[f"{sym.name}()"] = anchor
            bare[sym.name] = anchor
    for name in represented_enums:
        bare[name] = enum_anchor(name)
    for name in represented_macros:
        bare[name] = macro_anchor(name)
    return exact, bare


def _linkify_plain_text(text: str, exact: dict[str, str], bare: dict[str, str]) -> str:
    """Escape and cross-link ordinary prose that is already destined for HTML."""
    escaped = html.escape(text)
    placeholders: dict[str, str] = {}
    # Protect qualified references before linking bare type names so we never create nested anchors.
    for index, (token, anchor) in enumerate(sorted(exact.items(), key=lambda kv: len(kv[0]), reverse=True)):
        escaped_token = html.escape(token)
        if escaped_token not in escaped:
            continue
        marker = f"@@APIREF{index}@@"
        # Keep the parentheses inside the code label when they are part of the matched token.
        placeholders[marker] = f'<a href="#{anchor}"><code>{escaped_token}</code></a>'
        escaped = escaped.replace(escaped_token, marker)
    for token, anchor in sorted(bare.items(), key=lambda kv: len(kv[0]), reverse=True):
        escaped_token = html.escape(token)
        escaped = re.sub(
            rf"(?<![A-Za-z0-9_]){re.escape(escaped_token)}(?![A-Za-z0-9_])",
            f'<a href="#{anchor}"><code>{escaped_token}</code></a>',
            escaped,
        )
    for marker, replacement in placeholders.items():
        escaped = escaped.replace(marker, replacement)
    return escaped


def _code_span_anchor(code_text: str, exact: dict[str, str], bare: dict[str, str]) -> str | None:
    """Resolve a whole Markdown code span to an API anchor when that is unambiguous."""
    if code_text in exact:
        return exact[code_text]
    if code_text in bare:
        return bare[code_text]

    # Calls often include arguments in prose, while the link map stores only the symbol name.
    if "(" in code_text and code_text.endswith(")"):
        call_target = code_text.split("(", 1)[0]
        if call_target in exact:
            return exact[call_target]
        if call_target in bare:
            return bare[call_target]

    # Enum/member-style references can sensibly link to the owning public API type/enum.
    if "." in code_text:
        owner = code_text.split(".", 1)[0]
        if owner in bare:
            return bare[owner]

    return None


def linkify(text: str, exact: dict[str, str], bare: dict[str, str]) -> str:
    """Render inline JSDoc/YAML prose as HTML, including Markdown code spans.

    API descriptions are embedded inside raw HTML tables and divs in the generated page,
    so Jekyll/Kramdown will not reliably process Markdown backticks there. Consume those
    spans here instead of leaking literal backticks into the rendered documentation.
    """
    if not text:
        return ""

    parts: list[str] = []
    cursor = 0
    # JSDoc descriptions use ordinary inline code spans. Supporting repeated backtick
    # delimiters also avoids mangling a span whose contents contain a single backtick.
    for match in re.finditer(r"(`+)(.+?)\1", text, flags=re.DOTALL):
        if match.start() > cursor:
            parts.append(_linkify_plain_text(text[cursor:match.start()], exact, bare))

        code_text = match.group(2)
        escaped_code = html.escape(code_text)
        anchor = _code_span_anchor(code_text, exact, bare)
        rendered = f'<code>{escaped_code}</code>'
        if anchor:
            rendered = f'<a href="#{anchor}">{rendered}</a>'
        parts.append(rendered)
        cursor = match.end()

    if cursor < len(text):
        parts.append(_linkify_plain_text(text[cursor:], exact, bare))

    return "".join(parts)

def type_html(type_text: str, bare: dict[str, str]) -> str:
    escaped = html.escape(type_text)
    parts = re.split(r"([A-Za-z_]\w*)", escaped)
    for i, part in enumerate(parts):
        if part in bare:
            parts[i] = f'<a href="#{bare[part]}">{part}</a>'
    return "".join(parts)


def manual_for(manifest: dict[str, Any], key: str) -> dict[str, Any]:
    return (manifest.get("symbols") or {}).get(key, {}) or {}


def render_detail(symbol: Symbol, manifest: dict[str, Any], exact: dict[str, str], bare: dict[str, str]) -> list[str]:
    manual = manual_for(manifest, symbol.key)
    lines: list[str] = []
    lines.append(f'<div class="api-method-entry" id="{symbol_anchor(symbol)}">')
    lines.append(f'  <div class="api-method-name">{html.escape(signature(symbol))}</div>')
    desc = manual.get("description", symbol.description)
    if desc:
        lines.append(f'  <p class="api-method-summary">{linkify(desc, exact, bare)}</p>')
    if symbol.params:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">Arguments</div>')
        for p in symbol.params:
            lines.append('    <div class="api-argument">')
            opt = ' <span class="api-optional">optional</span>' if p.optional else ''
            lines.append(f'      <span class="api-argument-name">{html.escape(p.name)}{opt}</span>')
            lines.append(f'      <span class="api-argument-type">{type_html(p.type, bare)}</span>')
            lines.append(f'      <span class="api-argument-description">{linkify(p.description, exact, bare)}</span>')
            lines.append('    </div>')
        lines.append('  </div>')
    if symbol.return_type and symbol.return_type != "Undefined" or symbol.return_description:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">Returns</div>')
        rdesc = manual.get("return_description", symbol.return_description)
        row_class = "api-return-row" if rdesc else "api-return-row api-return-only"
        lines.append(f'    <div class="{row_class}">')
        lines.append(f'      <span class="api-return-type">{type_html(symbol.return_type, bare)}</span>')
        if rdesc:
            lines.append(f'      <span class="api-return-description">{linkify(rdesc, exact, bare)}</span>')
        lines.append('    </div>')
        lines.append('  </div>')
    notes = manual.get("notes")
    fields = manual.get("fields")
    if notes or fields:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">Extra notes</div>')
        lines.append('    <div class="api-extra-notes">')
        if isinstance(notes, str):
            notes = [notes]
        for paragraph in notes or []:
            lines.append(f'      <p>{linkify(str(paragraph), exact, bare)}</p>')
        if fields:
            lines.append('      <div class="api-field-list">')
            for f in fields:
                lines.append('        <div class="api-field-row">')
                lines.append(f'          <span class="api-field-name">{html.escape(str(f["name"]))}</span>')
                lines.append(f'          <span class="api-field-type">{type_html(str(f.get("type", "Any")), bare)}</span>')
                lines.append(f'          <span class="api-field-description">{linkify(str(f.get("description", "")), exact, bare)}</span>')
                lines.append('        </div>')
            lines.append('      </div>')
        lines.append('    </div>')
        lines.append('  </div>')
    example = manual.get("example")
    if example:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">Example</div>')
        lines.append(f'    <pre class="api-example"><code>{html.escape(str(example))}</code></pre>')
        lines.append('  </div>')
    see_also = manual.get("see_also") or []
    if see_also:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">See also</div>')
        lines.append(f'    <div class="api-see-also">{render_see_also(see_also, exact, bare)}</div>')
        lines.append('  </div>')
    lines.append('</div>')
    return lines


def resolve_type_methods(type_name: str, symbols: dict[str, Symbol]) -> list[Symbol]:
    return sorted([s for s in symbols.values() if s.kind == "method" and s.owner == type_name], key=lambda s: s.order)


def expand_inherited_methods(
    manifest: dict[str, Any],
    symbols: dict[str, Symbol],
    parents: dict[str, str | None],
) -> dict[str, Symbol]:
    """Materialise inherited methods for manifest types that opt into inherited API rendering."""
    expanded = dict(symbols)
    for type_name, cfg in (manifest.get("types") or {}).items():
        if not cfg.get("include_inherited_methods") or type_name not in symbols:
            continue
        seen = {m.name for m in resolve_type_methods(type_name, expanded)}
        parent = parents.get(type_name)
        visited: set[str] = set()
        while parent and parent not in visited:
            visited.add(parent)
            parent_methods = sorted(
                [s for s in symbols.values() if s.kind == "method" and s.owner == parent],
                key=lambda s: s.order,
            )
            for method in parent_methods:
                if method.name in seen:
                    continue
                return_type = method.return_type
                return_type = return_type.replace(f"Struct.{parent}", f"Struct.{type_name}")
                inherited = dataclasses.replace(method, owner=type_name, return_type=return_type)
                expanded[inherited.key] = inherited
                seen.add(method.name)
            parent = parents.get(parent)
    return expanded


def render_type(type_name: str, manifest: dict[str, Any], symbols: dict[str, Symbol], exact: dict[str, str], bare: dict[str, str]) -> list[str]:
    sym = symbols[type_name]
    cfg = (manifest.get("types") or {}).get(type_name, {}) or {}
    methods = resolve_type_methods(type_name, symbols)
    excluded = set(cfg.get("exclude_methods") or [])
    methods = [m for m in methods if m.name not in excluded]
    lines: list[str] = []
    display_name = str(cfg.get("display_name", type_name))
    lines.append(f'### {display_name}')
    lines.append(f'{{: #{type_anchor(type_name)} .api-type-title }}')
    lines.append('')
    if display_name != type_name:
        lines.append(f'Returned as `{type_name}`.')
        lines.append('')
    desc = cfg.get("description", sym.description)
    if desc:
        lines.append(linkify(desc, exact, bare))
        lines.append('')
    if sym.parent and sym.parent in bare:
        lines.append(f'Inherits from [`{sym.parent}`](#{bare[sym.parent]}).')
        lines.append('')
    if not cfg.get("opaque"):
        # Constructor signature is source-derived. Keep it visually strong but valid-looking.
        required_args = [p.name for p in sym.params if not p.optional]
        optional_args = [p.name for p in sym.params if p.optional]
        call_args = required_args + optional_args
        call = f'new {sym.name}({", ".join(call_args)})'
        lines.append('```gml')
        lines.append(call)
        lines.append('```')
        lines.append('')
        if sym.params:
            lines.append('<div class="api-constructor-meta">')
            lines.append('  <div class="api-detail-section">')
            lines.append('    <div class="api-detail-heading">Arguments</div>')
            for p in sym.params:
                opt = ' <span class="api-optional">optional</span>' if p.optional else ''
                lines.append('    <div class="api-argument">')
                lines.append(f'      <span class="api-argument-name">{html.escape(p.name)}{opt}</span>')
                lines.append(f'      <span class="api-argument-type">{type_html(p.type, bare)}</span>')
                lines.append(f'      <span class="api-argument-description">{linkify(p.description, exact, bare)}</span>')
                lines.append('    </div>')
            lines.append('  </div>')
            lines.append('</div>')
            lines.append('')
    if methods:
        lines.append('#### Methods')
        lines.append('')
        group_cfg = cfg.get("method_groups") or {}
        assigned: set[str] = set()
        if group_cfg:
            for group_name, names in group_cfg.items():
                group_methods = [next((m for m in methods if m.name == n), None) for n in names]
                group_methods = [m for m in group_methods if m]
                if not group_methods:
                    continue
                lines.append(f'<div class="api-method-group-title">{html.escape(str(group_name))}</div>')
                lines.append('<table class="api-methods"><tbody>')
                for m in group_methods:
                    assigned.add(m.name)
                    lines.append(f'<tr><td><a href="#{symbol_anchor(m)}"><code>{html.escape(m.name)}()</code></a></td><td>{linkify(m.description, exact, bare)}</td></tr>')
                lines.append('</tbody></table>')
                lines.append('')
            leftovers = [m for m in methods if m.name not in assigned]
            if leftovers:
                lines.append('<div class="api-method-group-title">Other</div>')
                lines.append('<table class="api-methods"><tbody>')
                for m in leftovers:
                    lines.append(f'<tr><td><a href="#{symbol_anchor(m)}"><code>{html.escape(m.name)}()</code></a></td><td>{linkify(m.description, exact, bare)}</td></tr>')
                lines.append('</tbody></table>')
                lines.append('')
        else:
            lines.append('<table class="api-methods"><thead><tr><th>Method</th><th>What it does</th></tr></thead><tbody>')
            for m in methods:
                lines.append(f'<tr><td><a href="#{symbol_anchor(m)}"><code>{html.escape(m.name)}()</code></a></td><td>{linkify(m.description, exact, bare)}</td></tr>')
            lines.append('</tbody></table>')
            lines.append('')
        for m in methods:
            lines.extend(render_detail(m, manifest, exact, bare))
            lines.append('')
    return lines


def normalize_macro_manifest(manifest: dict[str, Any]) -> None:
    """Normalize legacy inline macro metadata into the top-level macros mapping."""
    macro_meta = dict(manifest.get("macros") or {})

    def normalize_entries(entries: list[Any]) -> list[str]:
        names: list[str] = []
        for entry in entries:
            if isinstance(entry, str):
                names.append(entry)
                continue
            if not isinstance(entry, dict) or not entry.get("name"):
                continue
            name = str(entry["name"])
            inline = {k: v for k, v in entry.items() if k != "name"}
            # Explicit top-level metadata wins over the legacy inline form.
            macro_meta[name] = {**inline, **(macro_meta.get(name) or {})}
            names.append(name)
        return names

    for section in manifest.get("macro_sections") or []:
        if section.get("macros"):
            section["macros"] = normalize_entries(section.get("macros") or [])
        for group in section.get("groups") or []:
            if group.get("macros"):
                group["macros"] = normalize_entries(group.get("macros") or [])
    if macro_meta:
        manifest["macros"] = macro_meta


def collect_represented(manifest: dict[str, Any]) -> tuple[set[str], set[str], set[str]]:
    represented: set[str] = set()
    for section in manifest.get("sections") or []:
        represented.update(section.get("types") or [])
    for section in manifest.get("function_sections") or []:
        represented.update(section.get("functions") or [])
        for sub in section.get("subsections") or []:
            represented.update(sub.get("functions") or [])
    represented_enums: set[str] = set()
    for section in manifest.get("enum_sections") or []:
        represented_enums.update(section.get("enums") or [])
        for group in section.get("groups") or []:
            represented_enums.update(group.get("enums") or [])
    represented_macros: set[str] = set()
    for section in manifest.get("macro_sections") or []:
        represented_macros.update(section.get("macros") or [])
        for group in section.get("groups") or []:
            represented_macros.update(group.get("macros") or [])
    return represented, represented_enums, represented_macros


def render_enum(name: str, enum: EnumDef, manifest: dict[str, Any], exact: dict[str, str], bare: dict[str, str]) -> list[str]:
    cfg = ((manifest.get("enums") or {}).get(name) or {})
    member_docs = cfg.get("members") or {}
    lines = [f'<div class="api-enum-entry" id="{enum_anchor(name)}">', f'  <div class="api-enum-name">{html.escape(name)}</div>']
    desc = cfg.get("description", enum.description)
    if desc:
        lines.append(f'  <p>{linkify(str(desc), exact, bare)}</p>')
    lines.append('  <div class="api-enum-members">')
    for member, value in enum.members:
        mcfg = member_docs.get(member, {}) if isinstance(member_docs, dict) else {}
        desc = mcfg.get("description", "") if isinstance(mcfg, dict) else str(mcfg)
        value_text = f' = {html.escape(value)}' if value else ''
        lines.append('    <div class="api-enum-row">')
        lines.append(f'      <span class="api-enum-member">{html.escape(member)}{value_text}</span>')
        lines.append(f'      <span class="api-enum-description">{linkify(desc, exact, bare)}</span>')
        lines.append('    </div>')
    lines.append('  </div>')
    lines.append('</div>')
    return lines


def render_see_also(see_also: list[Any], exact: dict[str, str], bare: dict[str, str]) -> str:
    links: list[str] = []
    for target in see_also:
        if isinstance(target, str):
            if target in exact:
                links.append(f'<a href="#{exact[target]}"><code>{html.escape(target)}</code></a>')
            elif target in bare:
                links.append(f'<a href="#{bare[target]}"><code>{html.escape(target)}</code></a>')
            else:
                links.append(html.escape(target))
        else:
            label = str(target.get("label", target.get("href", "")))
            href = str(target.get("href", "#"))
            if href.startswith("/"):
                rendered_href = "{{ '" + html.escape(href, quote=True) + "' | relative_url }}"
            else:
                rendered_href = html.escape(href, quote=True)
            links.append(f'<a href="{rendered_href}">{html.escape(label)}</a>')
    return ' <span aria-hidden="true">·</span> '.join(links)


def render_macro(
    name: str,
    macro: MacroDef,
    manifest: dict[str, Any],
    exact: dict[str, str],
    bare: dict[str, str],
    inherited_role: str | None = None,
) -> list[str]:
    cfg = ((manifest.get("macros") or {}).get(name) or {})
    role = str(cfg.get("role", inherited_role or "value")).strip().lower()
    lines = [
        f'<div class="api-method-entry api-macro-entry api-macro-{html.escape(role)}" id="{macro_anchor(name)}">',
        f'  <div class="api-method-name">{html.escape(name)}</div>',
    ]
    desc = cfg.get("description", macro.description)
    if desc:
        lines.append(f'  <p class="api-method-summary">{linkify(str(desc), exact, bare)}</p>')
    if role != "symbol":
        value_heading = "Default" if role == "setting" else "Value"
        lines.append('  <div class="api-detail-section">')
        lines.append(f'    <div class="api-detail-heading">{value_heading}</div>')
        lines.append(f'    <pre class="api-example"><code>{html.escape(macro.value)}</code></pre>')
        lines.append('  </div>')
    macro_type = cfg.get("type")
    if macro_type:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">Type</div>')
        lines.append(f'    <div class="api-return-row api-return-only"><span class="api-return-type">{type_html(str(macro_type), bare)}</span></div>')
        lines.append('  </div>')
    see_also = cfg.get("see_also") or []
    if see_also:
        lines.append('  <div class="api-detail-section">')
        lines.append('    <div class="api-detail-heading">See also</div>')
        lines.append(f'    <div class="api-see-also">{render_see_also(see_also, exact, bare)}</div>')
        lines.append('  </div>')
    lines.append('</div>')
    return lines


def validate(
    manifest: dict[str, Any],
    symbols: dict[str, Symbol],
    enums: dict[str, EnumDef],
    macros: dict[str, MacroDef],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    represented, represented_enums, represented_macros = collect_represented(manifest)
    for key in represented:
        if key not in symbols:
            errors.append(f"Manifest references missing symbol: {key}")
    for name in represented_enums:
        if name not in enums:
            errors.append(f"Manifest references missing enum: {name}")
    for name in represented_macros:
        if name not in macros:
            errors.append(f"Manifest references missing macro: {name}")
        elif macros[name].hidden:
            errors.append(f"Ignored/internal macro cannot be represented: {name}")

    valid_macro_roles = {"value", "setting", "symbol", "metadata"}
    for section in manifest.get("macro_sections") or []:
        section_role = section.get("role")
        if section_role is not None and str(section_role).strip().lower() not in valid_macro_roles:
            errors.append(f"Unknown macro role on section {section.get('title', '')}: {section_role}")
        for group in section.get("groups") or []:
            group_role = group.get("role")
            if group_role is not None and str(group_role).strip().lower() not in valid_macro_roles:
                errors.append(f"Unknown macro role on group {group.get('title', '')}: {group_role}")
    for name, cfg in (manifest.get("macros") or {}).items():
        role = (cfg or {}).get("role") if isinstance(cfg, dict) else None
        if role is not None and str(role).strip().lower() not in valid_macro_roles:
            errors.append(f"Unknown macro role for {name}: {role}")
    for type_name, cfg in (manifest.get("types") or {}).items():
        if type_name not in symbols:
            continue
        if symbols[type_name].hidden and not cfg.get("opaque"):
            errors.append(f"Ignored/internal constructor must be opaque when represented: {type_name}")
        existing = {m.name for m in resolve_type_methods(type_name, symbols)}
        assigned: list[str] = []
        for names in (cfg.get("method_groups") or {}).values():
            assigned.extend(names)
            for name in names:
                if name not in existing:
                    errors.append(f"{type_name} method group references missing method: {name}")
        duplicates = {n for n in assigned if assigned.count(n) > 1}
        for n in sorted(duplicates):
            errors.append(f"{type_name}.{n} appears in more than one method group")
        if cfg.get("require_grouping"):
            unassigned = existing - set(assigned) - set(cfg.get("exclude_methods") or [])
            for n in sorted(unassigned):
                errors.append(f"Public method is not assigned to a group: {type_name}.{n}")
    # Every manual symbol/macro metadata entry must resolve.
    for key in (manifest.get("symbols") or {}):
        if key not in symbols:
            errors.append(f"Manual metadata references missing symbol: {key}")
    for name in (manifest.get("macros") or {}):
        if name not in macros:
            errors.append(f"Manual metadata references missing macro: {name}")
        elif macros[name].hidden:
            errors.append(f"Manual metadata references ignored/internal macro: {name}")
    # Optional broad coverage lint: all library-prefixed public top-level symbols should be represented.
    prefix = str(manifest.get("library", {}).get("symbol_prefix", ""))
    if manifest.get("require_public_coverage") and prefix:
        for key, sym in symbols.items():
            if sym.owner or sym.hidden:
                continue
            if not sym.name.startswith(prefix):
                continue
            if sym.name not in represented:
                errors.append(f"Public top-level symbol is not represented: {sym.name}")
        for name in enums:
            if (name.startswith(prefix) or name.startswith("e" + prefix)) and name not in represented_enums:
                errors.append(f"Public enum is not represented: {name}")
    macro_prefix = str(manifest.get("library", {}).get("macro_prefix", prefix))
    if manifest.get("require_macro_coverage") and macro_prefix:
        for name, macro in macros.items():
            if macro.hidden:
                continue
            if name.startswith(macro_prefix) and name not in represented_macros:
                errors.append(f"Public macro is not represented: {name}")
    return errors, warnings


def generate(manifest_path: Path, source_root: Path, output_path: Path | None, dump_model: Path | None) -> int:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    normalize_macro_manifest(manifest)
    globs = manifest.get("source_globs") or ["scripts/**/*.gml"]
    source_symbols, enums, macros, parents = parse_gml(source_root, globs)
    symbols = expand_inherited_methods(manifest, source_symbols, parents)
    errors, warnings = validate(manifest, symbols, enums, macros)
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 2

    represented, represented_enums, represented_macros = collect_represented(manifest)
    # Include methods of represented types in the link/index model.
    for type_name in list(represented):
        if type_name in symbols and symbols[type_name].kind == "type":
            represented.update(m.key for m in resolve_type_methods(type_name, symbols))
    exact, bare = build_link_maps(symbols, enums, macros, represented, represented_enums, represented_macros)

    page = manifest.get("page") or {}
    lines: list[str] = ["---"]
    front = {
        "layout": page.get("layout", "default"),
        "title": page.get("title", "API Reference"),
        "parent": page.get("parent"),
        "nav_order": page.get("nav_order"),
        "library_id": manifest.get("library", {}).get("id"),
        "doc_version": page.get("doc_version", "current"),
        "api_reference": page.get("api_reference", True),
    }
    for key, value in front.items():
        if value is None:
            continue
        if isinstance(value, str):
            rendered = json.dumps(value)
        elif isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", "", "<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->", f"<!-- Source: GML JSDoc + {manifest_path.name} -->", "", '<div class="sticky-toc" markdown="block">', '<details open markdown="block">', '  <summary>On this page</summary>', '', '1. TOC', '{:toc}', '', '</details>', '</div>', '', f'# {page.get("heading", "API Reference")}', ''])
    intro = page.get("intro")
    if intro:
        lines.append(str(intro))
        lines.append('')
    lines.append('---')
    lines.append('')

    for section in manifest.get("sections") or []:
        lines.append(f'## {section["title"]}')
        lines.append('')
        if section.get("intro"):
            lines.append(str(section["intro"]))
            lines.append('')
        for type_name in section.get("types") or []:
            lines.extend(render_type(type_name, manifest, symbols, exact, bare))

    for section in manifest.get("function_sections") or []:
        lines.append(f'## {section["title"]}')
        lines.append('')
        if section.get("intro"):
            lines.append(str(section["intro"]))
            lines.append('')
        if section.get("subsections"):
            for sub_index, sub in enumerate(section["subsections"]):
                lines.append(f'### {sub["title"]}')
                subsection_classes = ".api-function-subsection-title"
                if sub_index == 0:
                    subsection_classes += " .api-function-subsection-title-first"
                lines.append(f'{{: {subsection_classes} }}')
                lines.append('')
                for name in sub.get("functions") or []:
                    lines.extend(render_detail(symbols[name], manifest, exact, bare))
                    lines.append('')
        else:
            for name in section.get("functions") or []:
                lines.extend(render_detail(symbols[name], manifest, exact, bare))
                lines.append('')

    for section in manifest.get("enum_sections") or []:
        lines.append(f'## {section["title"]}')
        lines.append('')
        for group_index, group in enumerate(section.get("groups") or []):
            lines.append(f'### {group["title"]}')
            subsection_classes = ".api-function-subsection-title"
            if group_index == 0:
                subsection_classes += " .api-function-subsection-title-first"
            lines.append(f'{{: {subsection_classes} }}')
            lines.append('')
            for name in group.get("enums") or []:
                lines.extend(render_enum(name, enums[name], manifest, exact, bare))
                lines.append('')
        if not section.get("groups"):
            for name in section.get("enums") or []:
                lines.extend(render_enum(name, enums[name], manifest, exact, bare))
                lines.append('')

    for section in manifest.get("macro_sections") or []:
        lines.append(f'## {section["title"]}')
        lines.append('')
        if section.get("intro"):
            lines.append(str(section["intro"]))
            lines.append('')
        for group_index, group in enumerate(section.get("groups") or []):
            lines.append(f'### {group["title"]}')
            subsection_classes = ".api-function-subsection-title"
            if group_index == 0:
                subsection_classes += " .api-function-subsection-title-first"
            lines.append(f'{{: {subsection_classes} }}')
            lines.append('')
            macro_role = group.get("role", section.get("role"))
            for name in group.get("macros") or []:
                lines.extend(render_macro(name, macros[name], manifest, exact, bare, macro_role))
                lines.append('')
        if not section.get("groups"):
            macro_role = section.get("role")
            for name in section.get("macros") or []:
                lines.extend(render_macro(name, macros[name], manifest, exact, bare, macro_role))
                lines.append('')

    lines.append('## Symbol index')
    lines.append('')
    index_symbols = [symbols[k] for k in represented if k in symbols]
    index_symbols.sort(key=lambda s: (s.name.lower(), (s.owner or '').lower()))
    current_letter = None
    lines.append('<div class="api-symbol-index">')
    for sym in index_symbols:
        letter = sym.name[0].upper()
        if letter != current_letter:
            if current_letter is not None:
                lines.append('  </div>')
            lines.append(f'  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">{html.escape(letter)}</div>')
            current_letter = letter
        owner_text = f'<span class="api-symbol-owner">{html.escape(sym.owner)}</span>' if sym.owner else ''
        lines.append(f'    <div class="api-symbol-row"><a href="#{symbol_anchor(sym)}"><code>{html.escape(sym.name)}{("()" if sym.kind != "type" else "")}</code></a>{owner_text}</div>')
    if current_letter is not None:
        lines.append('  </div>')
    if represented_enums:
        lines.append('  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Enums</div>')
        for name in sorted(represented_enums, key=str.lower):
            lines.append(f'    <div class="api-symbol-row"><a href="#{enum_anchor(name)}"><code>{html.escape(name)}</code></a><span class="api-symbol-owner">enum</span></div>')
        lines.append('  </div>')
    if represented_macros:
        lines.append('  <div class="api-symbol-letter"><div class="api-symbol-letter-heading">Macros</div>')
        for name in sorted(represented_macros, key=str.lower):
            lines.append(f'    <div class="api-symbol-row"><a href="#{macro_anchor(name)}"><code>{html.escape(name)}</code></a><span class="api-symbol-owner">macro</span></div>')
        lines.append('  </div>')
    lines.append('</div>')
    lines.append('')

    output = "\n".join(lines).rstrip() + "\n"
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    if dump_model:
        model = {
            "symbols": {k: dataclasses.asdict(v) for k, v in symbols.items()},
            "source_symbols": {k: dataclasses.asdict(v) for k, v in source_symbols.items()},
            "parents": parents,
            "enums": {k: dataclasses.asdict(v) for k, v in enums.items()},
            "macros": {k: dataclasses.asdict(v) for k, v in macros.items()},
            "represented": sorted(represented),
            "represented_enums": sorted(represented_enums),
            "represented_macros": sorted(represented_macros),
        }
        dump_model.write_text(json.dumps(model, indent=2), encoding="utf-8")

    print(f"Generated {len(represented)} symbols, {len(represented_enums)} enums, and {len(represented_macros)} macros -> {output_path or 'stdout'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--dump-model", type=Path)
    args = parser.parse_args()
    return generate(args.manifest, args.source_root, args.output, args.dump_model)


if __name__ == "__main__":
    raise SystemExit(main())
