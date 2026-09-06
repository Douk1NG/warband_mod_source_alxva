"""
ui_color_patcher.py
Post-compile patcher for game_variables.txt UI colors.

The Warband engine reads UI color variables directly from
`game_variables.txt` at module load time. The module system Python
pipeline does NOT generate these values - the W.R.E.C.K. compiler
preserves them as-is, but on certain module configurations it drops
the trailing UI sections entirely.

This script reads the active module's `game_variables.txt` and writes
a sidecar `game_variables_pop.txt` next to it with the configured
palette applied. The active module file is never touched. Users who
want the custom colors rename the sidecar over the original.

Prints exactly one line: "Patched" or "Nothing to patch". Nothing else.
"""

from __future__ import print_function

import io
import os
import re
import sys

# Palette tuned for a dark coffee-purple background:
#   text     0xFFE6D5B8  warm cream
#   highlight 0xFFFFD86B warm gold
ESCAPE_TEXT_COLOR = 0xFFE6D5B8
ESCAPE_HIGHLIGHT_COLOR = 0xFFFFD86B

# Party skill list inside the Party/Manage screen. Shares the ESC menu
# palette so the screen reads as one design.
PARTY_SKILLS_TEXT_COLOR = 0xFFE6D5B8
PARTY_SKILLS_HIGHLIGHT_COLOR = 0xFFFFD86B

ESCAPE_BUTTON_KEYS = [
    "return", "options", "save_exit", "save", "save_as", "exit",
]

_ESCAPE_LAYOUT = {
    "return":    (0.18, 0.48, 0.25, 0.02),
    "options":   (0.18, 0.42, 0.25, 0.05),
    "save_exit": (0.18, 0.36, 0.25, 0.025),
    "save":      (0.18, 0.30, 0.25, 0.025),
    "save_as":   (0.18, 0.24, 0.25, 0.025),
    "exit":      (0.18, 0.18, 0.25, 0.025),
}

_ESCAPE_LINE_RE = re.compile(
    u"^(escape_(?:{keys})_button_(?:highlight_)?text_color)"
    u"\s*=\s*0x[0-9A-Fa-f]{{1,8}}\s*$".format(keys="|".join(ESCAPE_BUTTON_KEYS))
)
_ESCAPE_SECTION_RE = re.compile(r"^\s*#escape\s+window\s*$", re.IGNORECASE)

_PARTY_SKILLS_ANCHOR_RE = re.compile(
    u"^party_bo_skills_size_y\s*=\s*0\.75\s*$"
)
_PARTY_SKILLS_LINE_RE = re.compile(
    u"^party_bo_skills_(text|highlight_text)_color\s*="
    u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
)


def _to_hex(value):
    return u"0x{0:08X}".format(value & 0xFFFFFFFF)


def _to_unicode(s):
    if isinstance(s, bytes):
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            return s.decode("latin-1")
    return s


def _build_escape_block():
    text_hex = _to_hex(ESCAPE_TEXT_COLOR)
    high_hex = _to_hex(ESCAPE_HIGHLIGHT_COLOR)
    out = [
        u"#escape window",
        u"escape_game_logo_position_x = 0.15",
        u"escape_game_logo_position_y = 0.55",
        u"escape_game_logo_size_x = 0.32",
        u"escape_game_logo_size_y = 0.105",
        u"",
    ]
    for key, (px, py, sx, sy) in _ESCAPE_LAYOUT.items():
        out.extend([
            u"escape_{0}_button_position_x = {1}".format(key, px),
            u"escape_{0}_button_position_y = {1}".format(key, py),
            u"escape_{0}_button_size_x = {1}".format(key, sx),
            u"escape_{0}_button_size_y = {1}".format(key, sy),
            u"escape_{0}_button_text_size_x = 0.032".format(key),
            u"escape_{0}_button_text_size_y = 0.045".format(key),
            u"escape_{0}_button_text_flags = 0x10".format(key),
            u"escape_{0}_button_text_color = {1}".format(key, text_hex),
            u"escape_{0}_button_highlight_text_color = {1}".format(key, high_hex),
            u"",
        ])
    return out


def _apply_replace(line, name_regex, expected):
    """If `line` matches `name_regex`, return a rewritten line with the
    expected hex. Otherwise return None.
    """
    stripped = line.rstrip(u"\r\n")
    m = name_regex.match(stripped)
    if not m:
        return None
    name = stripped.split(None, 1)[0]
    leading = re.match(r"^(\s*)", line).group(1)
    return u"{0}{1} = {2}\n".format(leading, name, expected[name])


def _patch_escape_menu(lines):
    """Return (new_lines, changed_flag)."""
    section_start = next(
        (i for i, line in enumerate(lines) if _ESCAPE_SECTION_RE.match(line)),
        None,
    )

    expected = {}
    for key in ESCAPE_BUTTON_KEYS:
        expected[u"escape_{0}_button_text_color".format(key)] = _to_hex(ESCAPE_TEXT_COLOR)
        expected[u"escape_{0}_button_highlight_text_color".format(key)] = _to_hex(ESCAPE_HIGHLIGHT_COLOR)

    new_lines = []
    in_section = section_start is not None
    matched = 0
    for line in lines:
        if in_section:
            replaced = _apply_replace(line, _ESCAPE_LINE_RE, expected)
            if replaced is not None:
                matched += 1
                new_lines.append(replaced)
                continue
        new_lines.append(line)

    if matched > 0:
        return new_lines, True

    # Section was dropped by W.R.E.C.K. - re-inject.
    block_lines = [u"{0}\n".format(l) for l in _build_escape_block()]
    if section_start is not None:
        end = len(lines)
        for j in range(section_start + 1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith(u"#"):
                end = j
                break
        return lines[:section_start] + block_lines + lines[end:], True

    out = list(lines)
    if out and not out[-1].endswith(u"\n"):
        out[-1] = out[-1] + u"\n"
    out.append(u"\n")
    out.extend(block_lines)
    return out, True


def _patch_party_skills(lines):
    """Return (new_lines, changed_flag)."""
    expected = {
        u"party_bo_skills_text_color": _to_hex(PARTY_SKILLS_TEXT_COLOR),
        u"party_bo_skills_highlight_text_color": _to_hex(PARTY_SKILLS_HIGHLIGHT_COLOR),
    }

    new_lines = []
    matched = set()
    for line in lines:
        replaced = _apply_replace(line, _PARTY_SKILLS_LINE_RE, expected)
        if replaced is not None:
            name = line.rstrip(u"\r\n").split(None, 1)[0]
            matched.add(name)
            new_lines.append(replaced)
        else:
            new_lines.append(line)

    if matched == set(expected):
        return new_lines, True

    out = []
    injected = False
    for line in new_lines:
        out.append(line)
        if not injected and _PARTY_SKILLS_ANCHOR_RE.match(
            line.rstrip(u"\r\n")
        ):
            for name in expected:
                if name not in matched:
                    out.append(u"{0} = {1}\n".format(name, expected[name]))
            injected = True
    if not injected:
        for name in expected:
            if name not in matched:
                out.append(u"{0} = {1}\n".format(name, expected[name]))
    return out, True


def main():
    module_dir = (
        r"C:/Program Files (x86)/Steam/steamapps/common/"
        r"MountBlade Warband/Modules/Dickplomacy Reloaded"
    )
    input_path = os.path.join(module_dir, "game_variables.txt")
    output_path = os.path.join(module_dir, "game_variables_pop.txt")

    if not os.path.isfile(input_path):
        sys.exit(1)

    with io.open(input_path, "r", encoding="utf-8") as fh:
        lines = [_to_unicode(line) for line in fh.readlines()]

    lines, _ = _patch_escape_menu(lines)
    lines, _ = _patch_party_skills(lines)

    with io.open(output_path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

    sys.stdout.write("Patched\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
