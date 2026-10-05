"""Helpers for parsing the module-system .py files.

The module-system source files are *not* normal Python — they're compiled by
WRECK into .txt files. We can't import them as modules because:

  1. Their bodies are mostly a giant list literal `[ ("script_name", [opcodes...]) ]`
     at module level. Executing that list would just throw `NameError` on every
     opcode like `try_begin` or `troop_get_slot`.

  2. They import from `header_operations`, `ID_animations`, etc. — those are
     also module-system files, not real Python packages.

So we parse them as text. Regex-only, no execution.
"""
from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "source"


# Matches `name = number,` or `name = "string",` at module scope.
# Also matches `name = identifier + identifier` style arithmetic chains
# (e.g. `slot_troop_armor_slots_end = slot_troop_armor_slots_begin + custom_armor_maximum_component`).
# We capture the right-hand side verbatim so we can resolve it later.
_ASSIGNMENT_RE = re.compile(
    r"""^[ \t]*([A-Za-z_][A-Za-z0-9_]*)[ \t]*=[ \t]*
        (
            "([^"\\]*(?:\\.[^"\\]*)*)"   # (3) quoted string
          |
            ([+-]?\s*(?:\d+|[A-Za-z_][A-Za-z0-9_]*)(?:\s*[+\-*/]\s*(?:\d+|[A-Za-z_][A-Za-z0-9_]*))*)  # (4) arithmetic expression
        )
        [ \t]*,?
    """,
    re.MULTILINE | re.VERBOSE,
)


def _resolve(expr: str, scope: dict[str, int]) -> int:
    """Best-effort evaluator for `IDENT (+/-/*//) IDENT (+/-...)` chains.

    Anything we can't resolve (unknown identifiers, parens, function calls)
    raises ValueError so callers can skip that constant. We intentionally
    keep this dumb: real Python `eval` would risk running module-system
    tuples through their top-level list literals.
    """
    expr = expr.strip()
    if not expr:
        raise ValueError("empty expr")
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|-?\d+|[+\-*/]", expr)
    if not tokens:
        raise ValueError("no tokens")
    # Parse left-to-right with same precedence as Python for + - * /.
    # No parens, no precedence split — good enough for `A + B + C` style.
    try:
        result = int(tokens[0]) if tokens[0].lstrip("-").isdigit() else scope[tokens[0]]
    except (KeyError, ValueError):
        raise ValueError(f"can't resolve identifier: {tokens[0]!r}")
    i = 1
    while i < len(tokens):
        op = tokens[i]
        rhs_tok = tokens[i + 1]
        try:
            rhs = int(rhs_tok) if rhs_tok.lstrip("-").isdigit() else scope[rhs_tok]
        except (KeyError, ValueError):
            raise ValueError(f"can't resolve identifier: {rhs_tok!r}")
        if op == "+":
            result += rhs
        elif op == "-":
            result -= rhs
        elif op == "*":
            result *= rhs
        elif op == "/":
            result //= rhs
        else:
            raise ValueError(f"unknown op: {op!r}")
        i += 2
    return result


def find_py(relative: str) -> Path:
    """Resolve a path under source/ or the repo root.

    Tries `source/<relative>` first (most callers want module-system files).
    Falls back to the repo root for files like `AGENTS.md`.
    """
    p_src = SOURCE_DIR / relative
    if p_src.exists():
        return p_src
    p_root = REPO_ROOT / relative
    if p_root.exists():
        return p_root
    raise FileNotFoundError(
        f"file not found under source/ or repo root: {relative}"
    )


def read_text(relative: str) -> str:
    return find_py(relative).read_text(encoding="utf-8", errors="replace")


def collect_constants(relative: str) -> dict[str, int | str]:
    """Parse top-level integer and string assignments from a module-system file.

    Returns a dict of {name: value}. Simple arithmetic expressions on the
    right-hand side are resolved against the same file (e.g.
    `slot_x_end = slot_x_begin + 18`). Bare-identifier assignments with no
    arithmetic and no surrounding numeric literal are kept as opaque
    identifiers — callers should treat those as unresolved.

    Note: this picks up ALL top-level assignments, including constants inside
    list literals like `factions = [("kingdom_1", ..., [("slot_x", 1), ...]), ...]`.
    That is usually fine — if anything, it overcounts, which makes our overlap
    checks *stricter*, not laxer.
    """
    text = read_text(relative)
    out: dict[str, int | str] = {}
    for m in _ASSIGNMENT_RE.finditer(text):
        name, _full_rhs, sval, expr = m.group(1), m.group(2), m.group(3), m.group(4)
        if sval is not None:
            out[name] = sval
            continue
        if expr is not None:
            # First pass: record any pure-literal-identifier RHS as a known
            # symbol so subsequent expressions can reference it.
            stripped = expr.strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", stripped):
                # Don't store opaque identifiers in `out` (we can't use them
                # as integers), but also don't fail: the helper layer will
                # skip them in the overlap checks. For self-references like
                # `slot_x_begin = 159`, the integer branch below handles it.
                continue
            try:
                out[name] = _resolve(expr, out)
            except (KeyError, ValueError):
                # Unresolvable expression — skip silently.
                pass
    return out


def collect_ranges(
    relative: str,
    *,
    prefix: str | None = None,
) -> list[tuple[str, int, int]]:
    """Find all `*_begin` / `*_end` pairs and return (name, begin, end).

    A range is detected when two constants share a stem (e.g. `slot_foo_begin`
    and `slot_foo_end`). We DO NOT assume they have the same numeric distance
    in every file — we just pair by suffix.

    If `prefix` is given, only consider names that start with that prefix.
    """
    consts = collect_constants(relative)
    begins: dict[str, int] = {}
    ends: dict[str, int] = {}
    for name, val in consts.items():
        if not isinstance(val, int):
            continue
        if prefix and not name.startswith(prefix):
            continue
        if name.endswith("_begin"):
            begins[name[: -len("_begin")]] = val
        elif name.endswith("_end"):
            ends[name[: -len("_end")]] = val
    pairs: list[tuple[str, int, int]] = []
    for stem in sorted(begins):
        if stem in ends:
            pairs.append((stem, begins[stem], ends[stem]))
    return pairs


def detect_overlaps(
    ranges: list[tuple[str, int, int]],
) -> list[tuple[str, int, int, str, int, int]]:
    """Return all pairwise overlaps in `ranges` as (name_a, a_lo, a_hi, name_b, b_lo, b_hi).

    An overlap exists when `[a_lo, a_hi) ∩ [b_lo, b_hi)` is non-empty AND the
    ranges are not the same range. Two pairs with the same numeric values but
    different names are still flagged — that's the bug class we want to catch.
    """
    out = []
    for i, (na, a_lo, a_hi) in enumerate(ranges):
        for nb, b_lo, b_hi in ranges[i + 1 :]:
            # Overlap of half-open intervals [lo, hi).
            if a_hi <= b_lo or b_hi <= a_lo:
                continue
            if a_lo == b_lo and a_hi == b_hi:
                continue
            out.append((na, a_lo, a_hi, nb, b_lo, b_hi))
    return out