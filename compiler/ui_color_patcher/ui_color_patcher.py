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

# Selected troop name in the Party screen center panel. Same palette.
SELECTED_TROOP_TEXT_COLOR = 0xFFE6D5B8
SELECTED_TROOP_HIGHLIGHT_COLOR = 0xFFFFD86B

# Inventory screen text colors. Applies to the slot name labels
# (inv_t_name1/2, inv_t_gold1/2) and the armor stats block
# (inv_t_armor_base/base2). Same palette.
INVENTORY_TEXT_COLOR = 0xFFE6D5B8
INVENTORY_HIGHLIGHT_COLOR = 0xFFFFD86B

# Face generation window label color. The module ships this at
# 0xFFFFFFDD (near-white), which is unreadable on the cream parchment
# background. Same palette.
FACE_GEN_TEXT_COLOR = 0xFFE6D5B8

# Character window: attributes / skills / weapon proficiencies base
# text color. The module ships each with a different dark hue
# (0xFF000033 / 0xFF003300 / 0xFF330000) which is unreadable on the
# cream parchment. We unify them to the cream palette so the labels
# read as one design.
CHAR_WINDOW_TEXT_COLOR = 0xFFE6D5B8

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

_PARTY_PRISONER_ANCHOR_RE = re.compile(
    u"^party_t_prisoner_management_text_flags\s*=\s*0x111\s*$"
)
_PARTY_PRISONER_LINE_RE = re.compile(
    u"^party_t_prisoner_management_(text|highlight_text)_color\s*="
    u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
)

_SELECTED_TROOP_ANCHOR_RE = re.compile(
    u"^party_t_selected_troop_name_text_flags\s*=\s*0x10\s*$"
)
_SELECTED_TROOP_LINE_RE = re.compile(
    u"^party_t_selected_troop_name_(text|highlight_text)_color\s*="
    u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
)

# Inventory slot name / gold labels (one _text_flags line each).
_INVENTORY_NAME_LINE_RE = re.compile(
    u"^inv_(t_name[12]|t_gold[12])_(text|highlight_text)_color\s*="
    u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
)
_INVENTORY_ARMOR_LINE_RE = re.compile(
    u"^inv_t_armor_base2_(text|highlight_text)_color\s*="
    u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
)

_FACE_GEN_LINE_RE = re.compile(
    u"^face_t_(deform_key_base|age|hair_color)_text_color\s*=\s*"
    u"0x[0-9A-Fa-f]{1,8}\s*$"
)

# Anchors used to inject the missing color lines for the face-gen
# labels that the module does not ship with a _text_color entry.
_FACE_GEN_DEFORM_ANCHOR_RE = re.compile(
    u"^face_bo_deform_text_size_y\s*=\s*0\.02\s*$"
)

_CHAR_WINDOW_LINE_RE = re.compile(
    u"^char_b_(attribs_base|skills_base|weapon_proficiencies_base)_"
    u"(text|highlight_text)_color\s*=\s*0x[0-9A-Fa-f]{1,8}\s*$"
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


def _patch_selected_troop(lines):
    """Inject / replace party_t_selected_troop_name_text_color and
    party_t_selected_troop_name_highlight_text_color. Same pattern as
    the party skills list - the block exists but the color lines are
    missing, so the name renders in default black.
    """
    expected = {
        u"party_t_selected_troop_name_text_color": _to_hex(SELECTED_TROOP_TEXT_COLOR),
        u"party_t_selected_troop_name_highlight_text_color": _to_hex(SELECTED_TROOP_HIGHLIGHT_COLOR),
    }

    new_lines = []
    matched = set()
    for line in lines:
        replaced = _apply_replace(line, _SELECTED_TROOP_LINE_RE, expected)
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
        if not injected and _SELECTED_TROOP_ANCHOR_RE.match(
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


def _patch_inventory(lines):
    """Patch inventory labels. Money labels (inv_t_gold1/2) are left
    alone - the user wants their default color preserved.

    Patched:
    - inv_t_name1, inv_t_name2 (slot name labels, e.g. "Discard", troop
      name in the inventory header).
    - inv_t_armor_base (in-place rewrite to the configured palette).
    - inv_t_armor_base2 (inject both lines after _text_flags = 0x10).
    """
    text_hex = _to_hex(INVENTORY_TEXT_COLOR)
    high_hex = _to_hex(INVENTORY_HIGHLIGHT_COLOR)

    expected_replace = {}
    for k in ("inv_t_name1", "inv_t_name2",
             "inv_t_armor_base", "inv_t_armor_base2"):
        expected_replace[u"{0}_text_color".format(k)] = text_hex
        expected_replace[u"{0}_highlight_text_color".format(k)] = high_hex

    re_inventory_any = re.compile(
        u"^inv_t_(?:name[12]|armor_base2?)_"
        u"(text|highlight_text)_color\s*="
        u"\s*0x[0-9A-Fa-f]{1,8}\s*$"
    )

    matched = set()
    new_lines = []
    for line in lines:
        stripped = line.rstrip(u"\r\n")
        m = re_inventory_any.match(stripped)
        if m:
            name = stripped.split(None, 1)[0]
            if name in expected_replace:
                replaced = _apply_replace(line, re_inventory_any, expected_replace)
                matched.add(name)
                if replaced is not None:
                    new_lines.append(replaced)
                    continue
        new_lines.append(line)

    if matched == set(expected_replace):
        return new_lines, True

    out = []
    pending = [(n, expected_replace[n]) for n in expected_replace
               if n not in matched]

    anchor_to_prefix = [
        (u"inv_t_name1_text_flags", u"inv_t_name1_"),
        (u"inv_t_name2_text_flags", u"inv_t_name2_"),
        (u"inv_t_armor_base_text_flags", u"inv_t_armor_base_"),
        (u"inv_t_armor_base2_text_flags", u"inv_t_armor_base2_"),
    ]
    remaining = dict(pending)
    for line in new_lines:
        out.append(line)
        for anchor, prefix in anchor_to_prefix:
            if re.match(
                u"^{0}\s*=\s*0x10\s*$".format(re.escape(anchor)),
                line.rstrip(u"\r\n"),
            ):
                for full, value in list(remaining.items()):
                    if full.startswith(prefix):
                        out.append(u"{0} = {1}\n".format(full, value))
                        remaining.pop(full, None)

    if remaining:
        for full, value in remaining.items():
            out.append(u"{0} = {1}\n".format(full, value))
    return out, True


def _patch_party_prisoner(lines):
    """Inject / replace party_t_prisoner_management_text_color and
    party_t_prisoner_management_highlight_text_color. Same pattern as
    the party skills list - the block exists but the color lines are
    missing, so the "You need to learn Prisoner Management skill..."
    hint renders in default black on the dark blue panel.
    """
    expected = {
        u"party_t_prisoner_management_text_color": _to_hex(PARTY_SKILLS_TEXT_COLOR),
        u"party_t_prisoner_management_highlight_text_color": _to_hex(PARTY_SKILLS_HIGHLIGHT_COLOR),
    }

    new_lines = []
    matched = set()
    for line in lines:
        stripped = line.rstrip(u"\r\n")
        m = _PARTY_PRISONER_LINE_RE.match(stripped)
        if m:
            name = stripped.split(None, 1)[0]
            replaced = _apply_replace(line, _PARTY_PRISONER_LINE_RE, expected)
            matched.add(name)
            if replaced is not None:
                new_lines.append(replaced)
            continue
        new_lines.append(line)

    if matched == set(expected):
        return new_lines, True

    out = []
    injected = False
    for line in new_lines:
        out.append(line)
        if not injected and _PARTY_PRISONER_ANCHOR_RE.match(
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


def _patch_face_gen(lines):
    """In-place rewrite of face-gen labels and inject the missing
    face_bo_deform_text_color entry. The shipped defaults
    (0xFFFFFFDD, near-white) are unreadable on the cream parchment.
    Targets:
      - face_t_deform_key_base_text_color (deform key labels)
      - face_t_age_text_color (Age label)
      - face_t_hair_color_text_color (Hair Color label)
      - face_bo_deform_text_color (deform value labels, e.g. "Face
        Width", "Face Ratio"). This entry is missing entirely from
        the compiled file, so we inject it after the anchor.
    """
    new_hex = _to_hex(FACE_GEN_TEXT_COLOR)
    targets = (
        u"face_t_deform_key_base_text_color",
        u"face_t_age_text_color",
        u"face_t_hair_color_text_color",
    )
    injected = u"face_bo_deform_text_color"
    new_lines = []
    matched = set()
    changed = False
    for line in lines:
        if _FACE_GEN_LINE_RE.match(line.rstrip(u"\r\n")):
            name = line.rstrip(u"\r\n").split(None, 1)[0]
            if name in targets:
                matched.add(name)
                leading = re.match(r"^(\s*)", line).group(1)
                new_lines.append(u"{0}{1} = {2}\n".format(
                    leading, name, new_hex
                ))
                changed = True
                continue
        new_lines.append(line)

    if matched == set(targets):
        # All in-place targets already at the configured value, but
        # still check for the deform-value color line which is not in
        # `targets` and may be missing entirely.
        out = list(new_lines)
        if not any(
            line.rstrip(u"\r\n").startswith(u"face_bo_deform_text_color")
            for line in out
        ):
            injected_now = False
            for i, line in enumerate(out):
                if _FACE_GEN_DEFORM_ANCHOR_RE.match(line.rstrip(u"\r\n")):
                    out.insert(
                        i + 1,
                        u"face_bo_deform_text_color = {0}\n".format(new_hex),
                    )
                    injected_now = True
                    break
            if not injected_now:
                out.append(
                    u"face_bo_deform_text_color = {0}\n".format(new_hex)
                )
        return out, changed

    # Anchor missing (unusual): inject under each respective flags
    # line, or append at end as a last resort.
    anchors = (
        (u"face_t_deform_key_base_text_flags", u"face_t_deform_key_base_text_color"),
        (u"face_t_age_text_flags", u"face_t_age_text_color"),
        (u"face_t_hair_color_text_flags", u"face_t_hair_color_text_color"),
    )
    out = []
    pending = [name for name in targets if name not in matched]
    for line in new_lines:
        out.append(line)
        for anchor, full in anchors:
            if full in pending and re.match(
                u"^{0}\s*=\s*0x8\s*$".format(re.escape(anchor)),
                line.rstrip(u"\r\n"),
            ):
                out.append(u"{0} = {1}\n".format(full, new_hex))
                pending.remove(full)
    if pending:
        for full in pending:
            out.append(u"{0} = {1}\n".format(full, new_hex))

    # Inject face_bo_deform_text_color if missing (the deform value
    # labels in the right column - Face Width, Face Ratio, etc.).
    if not any(
        line.rstrip(u"\r\n").startswith(u"face_bo_deform_text_color")
        for line in out
    ):
        injected_now = False
        for i, line in enumerate(out):
            if _FACE_GEN_DEFORM_ANCHOR_RE.match(line.rstrip(u"\r\n")):
                out.insert(
                    i + 1,
                    u"face_bo_deform_text_color = {0}\n".format(new_hex),
                )
                injected_now = True
                break
        if not injected_now:
            out.append(
                u"face_bo_deform_text_color = {0}\n".format(new_hex)
            )
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
    lines, _ = _patch_party_prisoner(lines)
    lines, _ = _patch_selected_troop(lines)
    lines, _ = _patch_inventory(lines)

    # Always rewrite - delete any stale sidecar from a prior run first so the
    # mtime/size change is unambiguous to the user. This guards against the
    # case where a partial run leaves the old _pop.txt behind and the user
    # renames it by mistake.
    if os.path.isfile(output_path):
        os.remove(output_path)
    with io.open(output_path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)

    sys.stdout.write("Patched\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
