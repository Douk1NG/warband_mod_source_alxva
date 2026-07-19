# update-014 — game_menus granular split (one file per menu)

## What changed

The `source/game_menus/` topic files (e.g. `sneak.py`, `camp.py`) have been
split into one file per menu tuple, organized as
`source/game_menus/<topic>/mnu_<menu_id>.py`. Each menu file exports a single
`<menu_id>_menu` list containing exactly one 6-field menu tuple.

New structure:

```
source/game_menus/
  __init__.py                 <- imports each topic sub-package, extends in original order
  <topic>/__init__.py         <- imports each mnu_*.py, extends into <topic>_menus
  <topic>/mnu_<menu_id>.py    <- one menu tuple
  ...
```

- 23 topic folders; **291 menus** total, each in its own file.
- Every generated `mnu_*.py` and `__init__.py` carries the
  `# -*- coding: cp1254 -*-` header and the standard `header_*` / `module_constants`
  imports, matching the previous topic files.
- The top-level `game_menus/__init__.py` topic import order is unchanged from the
  previous split, so the authored menu order is preserved exactly.

## Verification

- AST comparison of all 291 menu tuples against the prior committed topic files:
  **structurally identical**.
- Menu-id order (291 entries) reproduced **exactly** from the prior state.
- `compile.bat` → **COMPILATION SUCCESSFUL**.

## Rationale

Full granularity prepares the game-menu corpus for a future re-classification /
re-organization. Menus can later be re-filed into different topic folders (or new
ones) by moving a single `mnu_*.py` file and adjusting the two `__init__.py`
`import`/`extend` lines that reference it — no large-file edits required.

## Notes / gotchas for future edits

- To **edit** a menu: open `source/game_menus/<topic>/mnu_<menu_id>.py`.
- To **add** a menu: create `mnu_<id>.py` in the right topic folder, then add a
  `from game_menus.<topic>.mnu_<id> import <id>_menu` line and an
  `<topic>_menus.extend(<id>_menu)` line to `source/game_menus/<topic>/__init__.py`.
- To **move** a menu between topics: move the file and update both the source and
  destination `<topic>/__init__.py`. Remember ordering affects generated IDs
  (see project-orientation skill) — keep the intended position in the relevant
  `__init__.py` `extend` sequence.
- `ID_menus.py` is regenerated every compile; do not hand-edit or treat its numbers
  as stable across reorders.
