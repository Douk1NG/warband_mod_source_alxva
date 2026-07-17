# Dickplomacy Reloaded — Module System Project Orientation

Read-only survey of the repo at `C:\Users\Dibey\Documents\mount_warband_tools\source_dckplomacy`. Intended as input for a project-orientation skill.

---

## 1. Top-Level Map

### Project root

| Path | Description |
|------|-------------|
| `compile.bat` | **Primary build entry point** — clears stale `.pyc`, invokes W.R.E.C.K. (`compiler/compile.py`), pauses on completion |
| `compiler/` | W.R.E.C.K. compiler package (`compile.py`, `compiler.py`, path bootstrap, legacy batch scripts) |
| `source/` | All module-system Python source — the editable game-data layer |
| `updates/` | Hand-authored changelogs (`update-NNN.md`) documenting refactors and behavior changes |
| `README.md` | Project license, credits, OSP attributions |
| `.gitignore` | Ignores `.vscode/`, `.codegraph/`, `.agents/`, `1175source/` |
| `.gitattributes` | Git line-ending normalization (`* text=auto`) |
| `.agents/` | Local agent skills/rules (gitignored; includes `warband-modding` skill) |
| `1175source/` | Gitignored reference snapshot (Native 1.175 source port material) |

### `source/` top level

| Path | Description |
|------|-------------|
| `module_*.py` (31 files) | **GENERATED-INPUT** — hand-edited data files consumed by W.R.E.C.K.; each defines one entity list (`scripts`, `items`, `troops`, etc.) |
| `module_info.py` | Export destination config (`export_dir` → game `Modules/` folder) |
| `module_constants.py` | **HAND-AUTHORED** — slot numbers, mod constants (`dplmc_*`, `$g_*` vars), range markers; imports some `ID_*` files |
| `scripts/` | **HAND-AUTHORED** — domain-split script tuples; only `module_scripts.py` is split so far |
| `headers/` | **HAND-AUTHORED (do not treat as game data)** — opcode definitions (`header_operations.py`), entity field flags (`header_items.py`, `header_troops.py`, …), shared macros |
| `ids/` | **GENERATED-OUTPUT** — `ID_*.py` numeric index files; rewritten every successful compile |
| `process/` | **Legacy pipeline** — per-entity export scripts for the old Mount & Blade `build_module.bat` toolchain; superseded by W.R.E.C.K. but kept in repo |
| `modmerger/` | **HAND-AUTHORED framework** — merges third-party submod patches into `module_*` lists at import time; `mods/` holds per-mod delta files |
| `variables.txt` | **HAND-AUTHORED** — global `$variable` name registry consumed by compiler/process pipeline |
| `compiler` import hook | Every `module_*.py` ends with `from compiler import *` for W.R.E.C.K. syntax extensions |

### `module_*.py` inventory (all monolithic except scripts)

| File | ~Lines | Split? |
|------|--------|--------|
| `module_scripts.py` | 1,931 | **Yes** — inline legacy block + `.extend()` from `scripts/` |
| `module_dialogs.py` | 46,938 | No |
| `module_presentations.py` | 24,861 | No |
| `module_game_menus.py` | 23,438 | No |
| `module_mission_templates.py` | 19,487 | No |
| `module_strings.py` | 5,027 | No (may have been split historically per update notes) |
| `module_simple_triggers.py` | 7,698 | No |
| `module_constants.py` | 2,745 | No |
| `module_troops.py` | 2,793 | No |
| `module_items.py` | 2,273 | No |
| `module_scenes.py` | 1,430 | No |
| `module_triggers.py` | 1,827 | No |
| `module_parties.py` | 366 | No |
| + ~18 smaller `module_*.py` | varies | No (`animations`, `factions`, `meshes`, `sounds`, `quests`, …) |

---

## 2. Generated vs Hand-Authored

### Classification key

| Class | Meaning | Edit? |
|-------|---------|-------|
| **HAND-AUTHORED** | Human writes and maintains directly | Yes |
| **GENERATED-INPUT** | Human writes, but exists solely to feed the compiler | Yes — this is where game design lives |
| **GENERATED-OUTPUT** | Produced by compile; never hand-edit | No — safe to ignore unless debugging compiler |

### By area

| Path | Class | Notes |
|------|-------|-------|
| `source/scripts/**/*.py` | HAND-AUTHORED | Script tuple bodies; primary edit surface for logic |
| `source/module_scripts.py` (inline block ~L88–1898) | HAND-AUTHORED | Legacy scripts not yet migrated to domain files; **may duplicate domain copies** |
| `source/module_*.py` (all entity lists) | GENERATED-INPUT | Authoritative source of record order and content |
| `source/module_constants.py` | HAND-AUTHORED | Slot indices, `$g_*` names, faction range markers |
| `source/variables.txt` | HAND-AUTHORED | Global variable name list |
| `source/headers/**` | HAND-AUTHORED | Stable engine constants; `header_operations.py` says "DO NOT EDIT" but it is source, not compiler output |
| `source/modmerger/**` | HAND-AUTHORED | Framework + submod patch files |
| `source/ids/ID_*.py` | **GENERATED-OUTPUT** | See below |
| `source/process/**` | HAND-AUTHORED (legacy tooling) | Old export pipeline; not used by `compile.bat` |
| `compiler/**` | HAND-AUTHORED | W.R.E.C.K. itself |
| Game module `.txt` files in `export_dir` | **GENERATED-OUTPUT** | `scripts.txt`, `troops.txt`, `menus.txt`, etc. |
| `Data/item_modifiers.txt`, `Languages/en/*.csv` | GENERATED-OUTPUT | Optional exports when those modules exist |

### `ID_*.py` — explicit rules for agents

**Confirmed: regenerated automatically on every successful W.R.E.C.K. compile.**

Flow (from `compiler/compile.py`):

1. Compiler loads all `module_*.py` lists in a fixed order.
2. `calculate_identifiers()` assigns each entity a **positional index** (0-based) from list order.
3. Compiled `.txt` data is written to `export_dir` (game module folder).
4. Each `source/ids/ID_<entity>.py` is **overwritten** with lines like `itm_tutorial_dagger = 2`.

**Source of truth for IDs is list position in the corresponding `module_*.py`**, not the ID file. The ID file is a derived index for Python cross-references during editing.

| Question | Answer |
|----------|--------|
| Hand-edit `ID_*.py`? | **Never** — next compile overwrites it |
| Scan `ID_*.py` for design intent? | **No** — read `module_*.py` instead |
| When do IDs change? | Any insert/remove/reorder in the parent `module_*.py` list |
| What if ID write fails? | Compile still succeeds; `.txt` exports are valid; warning printed about stale ID files |

**25 ID files** under `source/ids/`: `animations`, `factions`, `info_pages`, `items`, `map_icons`, `menus`, `meshes`, `mission_templates`, `music`, `particle_systems`, `parties`, `party_templates`, `postfx`, `postfx_params`, `presentations`, `quests`, `scene_props`, `scenes`, `scripts`, `skills`, `sounds`, `strings`, `tableau_materials`, `troops`. (`ID_items_old.py` appears to be a stale manual artifact.)

**Legacy note:** `process/process_*.py` also wrote ID files (e.g. `process_scripts.py` → `ID_scripts.py`). That path is obsolete; W.R.E.C.K. is canonical.

---

## 3. The Compile / Export Pipeline

### Entry point (use this)

```
compile.bat
  → del *.pyc (avoid stale bytecode after moves)
  → python compiler\compile.py
  → pause
```

Requires **Python 2.6 or 2.7**. Compiler sets `sys.dont_write_bytecode = True`.

Invocation from skill/docs:

```
cmd /c "cd /d c:\Users\Dibey\Documents\mount_warband_tools\source_dckplomacy && compile.bat"
```

Success marker: `COMPILATION SUCCESSFUL`.

### Path setup (`compiler/bootstrap_paths.py`)

Before any imports, adds to `sys.path`:

- `source/` (root — holds `module_*.py` and `scripts` package)
- `source/headers/`, `source/ids/`, `source/process/`, `source/modmerger/`
- Each active subfolder under `source/modmerger/mods/`
- `compiler/`

### W.R.E.C.K. phases (in order)

```
1. Load module
   ├── module_info.py          → export_dir, plugins
   ├── optional: item_modifiers, ui_strings, user_hints
   └── required module_*.py    → fixed import order (see compile.py L84–138)
       └── modmerger hooks at bottom of many files mutate lists before compile

2. Load plugins
   └── WRECK plugin injections (if any registered)

3. Check module syntax
   └── validate all entity lists

4. Allocate identifiers
   └── positional IDs from list order; verify no undefined references

5. Compile module
   ├── preprocess (entity + plugin preprocessors)
   ├── per-entity processor + aggregator
   └── postprocess

6. Export module
   ├── Write .txt binaries to export_dir (module_info.export_dir)
   └── Regenerate source/ids/ID_*.py
```

### Export mapping (source list → game file)

| Python list | Output file |
|-------------|-------------|
| `scripts` | `scripts.txt` |
| `dialogs` | `conversation.txt` + `dialog_states.txt` |
| `game_menus` | `menus.txt` |
| `presentations` | `presentations.txt` |
| `mission_templates` | `mission_templates.txt` |
| `triggers` | `triggers.txt` |
| `simple_triggers` | `simple_triggers.txt` |
| `troops` | `troops.txt` |
| `items` | `item_kinds1.txt` |
| `strings` | `strings.txt` |
| … | (see `compile.py` L349–380) |

**Current `export_dir`** (`source/module_info.py`):

```
C:/Program Files (x86)/Steam/steamapps/common/MountBlade Warband/Modules/Dickplomacy Reloaded/
```

Change this to point at your local module folder before compiling.

### Legacy pipeline (do not use for normal work)

`compiler/build_module.bat` runs 30+ `source/process/process_*.py` scripts sequentially — the original Taleworlds toolchain predating W.R.E.C.K. Still present for reference; **this project standardizes on `compile.bat`**.

### Practical workflow: "I changed a script"

| You edited | Then run | Result |
|------------|----------|--------|
| `source/scripts/<domain>/*_scripts.py` | `compile.bat` | Updated `scripts.txt` + `ID_scripts.py` in game module |
| Inline block in `module_scripts.py` | `compile.bat` | Same |
| `module_dialogs.py`, menus, troops, etc. | `compile.bat` | Corresponding `.txt` + ID file |
| `module_constants.py` only | `compile.bat` | Constants baked into compiled output |
| `modmerger/mods/*` patch file | `compile.bat` | Patch applied at import, then compiled |
| `source/ids/ID_*.py` | **Don't** — edit parent `module_*.py` instead | — |

No separate "link" step. One compile produces both game data and refreshed ID files.

---

## 4. How Other Module Files Relate to Scripts

All listed files are **monolithic** (not split like scripts). Each ends with a **modmerger hook** that merges active submod patches.

### Record formats and examples

#### `module_scripts.py` — 2-field tuple *(split across `scripts/`)*

```python
("game_get_money_text",
  [
    (store_script_param_1, ":amount"),
    (try_begin),
      (eq, ":amount", 1),
      (str_store_string, s1, "str_1_denar"),
    (try_end),
  ]),
```

Assembly: inline `scripts = [...]` then `scripts.extend(domain_scripts)` × 21 domains.

#### `module_dialogs.py` — 46,938 lines — **7-field list** (graph-linked, not flat tuple)

```python
[anyone, "start", [(eq, "$talk_context", tc_tavern_talk), ...],
 "What is it?", "tavern_dialog", []],
```

Fields: `[partner, start_state, conditions, text, end_state, consequences, voiceover]`

#### `module_game_menus.py` — 23,438 lines — **6-field menu + nested 4-field options**

```python
("start_game_0", menu_text_color(0xFF000000)|mnf_disable_all_keys,
 "Welcome, adventurer...", "none", [], [
   ("continue", [], "Continue...", [
     (jump_to_menu, "mnu_choose_skill"),
   ]),
 ]),
```

Menu: `(id, flags, text, mesh, on_enter_ops, [options])`  
Option: `(option_id, conditions, text, consequences)`

#### `module_presentations.py` — 24,861 lines — **4-field tuple**

```python
("game_credits", prsntf_read_only, mesh_load_window, [
    (ti_on_presentation_load, [(assign, "$g_presentation_credits_obj_1", -1), ...]),
    (ti_on_presentation_run, [...]),
]),
```

Fields: `(id, flags, background_mesh, [triggers])`

#### `module_mission_templates.py` — 19,487 lines — **6-field tuple**

```python
("town_default", 0, -1, "Default town visit",
  [(0, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, pilgrim_disguise), ...],
  [(0, 0, ti_once, [...], [...]), ...]  # triggers
),
```

Fields: `(id, flags, mission_type, description, spawn_records, triggers)`

#### `module_triggers.py` — 1,827 lines — **5-field tuple** (old-style, stateful)

```python
(0.0, 0, 168.0, [], [
  (call_script, "script_refresh_center_inventories"),
]),
```

Fields: `(check_interval, delay, rearm, conditions, consequences)`

#### `module_simple_triggers.py` — 7,698 lines — **2-field tuple** (stateless)

```python
(1.0, [
  (call_script, "script_initialize_item_info"),
]),
```

Fields: `(check_interval, operations)`

#### `module_troops.py` — 2,793 lines — **list record, up to 14 fields**

```python
["player", "Player", "Player", tf_hero|tf_unmoveable_in_party_window,
 no_scene, reserved, fac_player_faction, [], str_4|agi_4|int_4|cha_4,
 wp(15), 0, 0x000000018000004136db6db6db6db6db00000000001db6db0000000000000000],
```

Uses helper `def`s (`wp()`, `wpex()`) at top of file — rare pattern; mostly data.

#### `module_items.py` — 2,273 lines — **list record, 7–10 fields**

```python
["tutorial_dagger", "Dagger", [("dagger_b", 0), ("dagger_b_scabbard", ixmesh_carry)],
 itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry,
 itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,
 3, weight(1.5)|spd_rtng(103)|..., imodbits_none],
```

**Critical:** comment at L55 — items before that line are **engine-hardwired**; order must not change casually.

---

## 5. What Touches What

High-level dependency map for "if I change X, what else is affected":

```
module_items.py  ──order──►  ID_items.py  ──imported by──►  module_troops, module_constants,
                                                              module_scripts, presentations, …

module_troops.py ──order──►  ID_troops.py  ──referenced in──►  dialogs, missions, scripts

module_strings.py ──order──► ID_strings.py ──referenced as──►  "str_*" in dialogs, menus, triggers

module_scripts.py ──order──► ID_scripts.py
       ▲                           │
       │                           ▼
  scripts/ domain files      call_script, "script_*" everywhere

module_game_menus.py ──► jump_to_menu "mnu_*" (self + other menus)
                    ──► call_script "script_*"
                    ──► start_presentation "prsnt_*" (via ops)
                    ──► item/troop/string ID constants

module_dialogs.py ──► trp_*, fac_*, str_*, call_script
                 ──► dialog state strings link records (graph)
                 ──► jump_to_menu, change_screen_*, party/troop slots

module_presentations.py ──► mesh_*, str_*, call_script
                       ──► ti_on_presentation_* triggers
                       ──► referenced from menus/scripts via start_presentation

module_mission_templates.py ──► mt_* referenced when entering scenes/battles
                           ──► spawn records reference trp_*, itm_*
                           ──► embedded trigger blocks (same op format as module_triggers)

module_triggers.py + module_simple_triggers.py ──► call_script, slot ops, party/troop refs
                                              ──► exported separately (triggers.txt vs simple_triggers.txt)

module_constants.py ──► slot_* indices, range markers (e.g. walkers_begin/end)
                   ──► imports ID_items, ID_quests, ID_factions
                   ──► used by virtually all module files

modmerger ──► runs last on each module_* list before compile
         ──► active mods in modmerger_options.mods_active[]

variables.txt ──► $g_* / $q_* global names used in operation blocks
```

### Common cross-reference patterns

| From | References | By |
|------|------------|-----|
| Dialogs, menus, triggers, scripts, presentations | Scripts | `(call_script, "script_<name>")` — string name, not numeric |
| Menus | Other menus | `(jump_to_menu, "mnu_<id>")` |
| Menus, scripts | Presentations | `(start_presentation, "prsnt_<id>")` |
| Troops | Items | Inventory lists use `"itm_*"` string constants |
| Any operation block | Troops, factions, items, strings | `"trp_*"`, `"fac_*"`, `"itm_*"`, `"str_*"` |
| Dialogs | Troops | Partner field: `trp_*`, `anyone`, `anyone\|plyr` |
| Mission templates | Scenes, troops, items | Spawn tuples, disguise item lists |
| `module_constants.py` | ID files | Range boundaries (`*_begin`/`*_end`) depend on stable ordering |

### Scripts-specific gotcha

Some scripts exist in **both** the inline `module_scripts.py` block and a domain file. Both ship (concatenated). Editing one copy without checking the other causes "fix didn't work" bugs.

---

## 6. Naming / ID Conventions

### String constants vs numeric IDs

| Entity | Record ID (in module file) | Runtime reference | Auto prefix | Numeric backing |
|--------|---------------------------|-------------------|-------------|-----------------|
| Script | `"my_script"` | `"script_my_script"` | `script_` | `ID_scripts.py` |
| Troop | `"player"` | `"trp_player"` | `trp_` | `ID_troops.py` |
| Item | `"tutorial_dagger"` | `"itm_tutorial_dagger"` | `itm_` | `ID_items.py` |
| Faction | `"player_faction"` | `"fac_player_faction"` | `fac_` | `ID_factions.py` |
| String | `"1_denar"` | `"str_1_denar"` | `str_` | `ID_strings.py` |
| Menu | `"start_game_0"` | `"mnu_start_game_0"` | `mnu_` | `ID_menus.py` |
| Presentation | `"game_credits"` | `"prsnt_game_credits"` | `prsnt_` | `ID_presentations.py` |
| Mission template | `"town_default"` | `"mt_town_default"` | `mt_` | `ID_mission_templates.py` |
| Scene | `"main_scene"` | `"scn_main_scene"` | `scn_` | `ID_scenes.py` |
| Party | `"main_party"` | `"p_main_party"` | `p_` | `ID_parties.py` |

### Flag / type prefixes (in `headers/`, not ID files)

| Prefix | File | Purpose |
|--------|------|---------|
| `itp_` | `header_items.py` | Item type/property bitflags |
| `itc_` | `header_items.py` | Item capability / animation |
| `tf_` | `header_troops.py` | Troop flags |
| `mnf_` | `header_game_menus.py` | Menu flags |
| `prsntf_` | `header_presentations.py` | Presentation flags |
| `ti_` | `header_triggers.py` | Trigger interval constants |
| `slot_` | `module_constants.py` | Agent/party/troop/item slot indices |
| `skl_` | `ID_skills.py` / headers | Skill IDs |
| `imodbit_` | `header_item_modifiers.py` | Item modifier bits |

### Do humans need numeric IDs?

**Almost never.** Author in `module_*.py` using bare name strings; reference elsewhere using prefixed string constants (`"trp_player"`, `"itm_sword"`, etc.). W.R.E.C.K. resolves these to integers at compile time.

**Exceptions where numbers matter:**

- **List order** in `module_*.py` — positional; reordering changes all downstream numeric IDs and breaks saves if done carelessly.
- **Hardwired item block** — first N items in `module_items.py` are engine-fixed (L55 comment).
- **`module_constants.py` slot numbers** — hand-assigned integers for `$variable` slots and `slot_*` indices; must stay stable across saves.
- **Face codes, mesh modifiers** — literal hex/int in troop/item records.

### Encoding

All `.py` under `source/` should use **`# -*- coding: cp1254 -*-`** as line 1 where non-ASCII appears. Read/write as cp1254, not UTF-8.

### Python version

Module source targets **Python 2.7** syntax: no f-strings, `print` statement, `xrange`, `except Exception, e`, etc.

---

## Quick Reference Card

```
EDIT SURFACES          BUILD              OUTPUT
─────────────          ─────              ──────
scripts/**/*.py   ─┐
module_scripts.py ─┤
module_*.py       ─┼──► compile.bat ──► Modules/<name>/*.txt  (game)
module_constants  ─┤                  └──► source/ids/ID_*.py  (dev index)
modmerger/mods/*  ─┘

NEVER EDIT: source/ids/ID_*.py, exported .txt files
ALWAYS RUN AFTER SOURCE CHANGES: compile.bat
PRIMARY COMPILER: W.R.E.C.K. (compiler/compile.py)
LEGACY (ignore): compiler/build_module.bat + source/process/
```
