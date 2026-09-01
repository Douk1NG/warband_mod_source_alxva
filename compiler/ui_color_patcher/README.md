# ui_color_patcher

Post-compile patcher for UI text colors stored in the compiled module's
`game_variables.txt`. Required because Warband's module system Python
pipeline does **not** expose UI color variables — the engine reads them
directly from the compiled file. Editing only the source `.py` files has
no effect on these values; you must patch the file after `compile.bat`
finishes (or run this script on its own).

## What it does

Two passes run on every invocation:

1. **ESC menu** (6 buttons, 12 lines)
   - In-place rewrite when W.R.E.C.K. preserves the section.
   - Full `#escape window` block re-injection if W.R.E.C.K. drops it.

2. **Party screen skill list** (1 panel, 2 lines)
   - The `party_bo_skills` geometry block exists in every Diplomacy-based
     module, but the engine-side `text_color` / `highlight_text_color`
     entries are missing. The skill list therefore renders in default
     black on dark parchment. We inject both lines right after the
     `party_bo_skills_size_y = 0.75` anchor.

## Configuration

Open `ui_color_patcher.py` and edit the four constants near the top:

```python
ESCAPE_TEXT_COLOR         = 0xFFE6D5B8  # cream  (resting)
ESCAPE_HIGHLIGHT_COLOR    = 0xFFFFD86B  # gold   (mouse hover)
PARTY_SKILLS_TEXT_COLOR   = 0xFFE6D5B8  # cream  (resting)
PARTY_SKILLS_HIGHLIGHT_COLOR = 0xFFFFD86B  # gold   (mouse hover)
```

Color format is `0xAARRGGBB`:
- `AA` = alpha. Use `0xFF` for opaque text.
- `RRGGBB` = red, green, blue channels, hex 00–FF.

The defaults are tuned for a dark coffee-purple background. Swap them to
whatever fits your palette.

## Usage

`compile.bat` invokes this script automatically at the end of every
build. Run it manually with:

```bat
python compiler\ui_color_patcher\ui_color_patcher.py
```

Pass `--module-dir PATH` to target a module that does not live at the
default location:

```bat
python compiler\ui_color_patcher\ui_color_patcher.py --module-dir "C:\path\to\MyMod"
```

## Output

The script prints exactly one line:

- `Patched` — at least one of the two passes modified the file.
- `Nothing to patch` — every value was already in sync.

No other output. No backups. No warnings.

## Why a separate script (not a module system edit)?

The Warband module system (1.171) provides no `module_game_variables.py`
or analogous hook for UI color variables. They are hardcoded in the
engine and surfaced only as values in `game_variables.txt`. A post-build
patcher is the only safe, repeatable way to ship color tweaks that
survive `compile.bat`.
