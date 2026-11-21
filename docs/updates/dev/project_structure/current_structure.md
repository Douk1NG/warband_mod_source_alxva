# Current Project Structure

```
repo root/
├── compile.bat                     # Entry: deletes stale .pyc → calls compiler\compile.py tag
├── compiler/                       # WRECK compiler + build scripts
│   ├── compiler.py                 # The WRECK engine (parses manifests, generates module files)
│   ├── compile.py                  # Build orchestrator (sets up paths, calls compiler.py)
│   ├── bootstrap_paths.py          # sys.path setup — adds source/, headers/, ids/, process/, modmerger/, mods/, compiler/
│   ├── id_paths.py                 # Where ID files get written (ids/ID_%s.py)
│   └── build_module.bat/.sh        # Direct build wrappers (alternative entry points)
├── headers/                        # Opcode definitions (header_operations.py, header_common.py, etc.)
├── ids/                            # Auto-generated ID files (ID_scripts.py, ID_troops.py, etc.) — never hand-edit
├── modmerger/                      # Modmerger plugin framework
│   ├── modmerger.py                # Core merger logic
│   ├── modmerger_options.py        # Merger options/config
│   ├── mods/                       # Active mod input sets (xgm_mod_options/, cstm/, etc.)
│   ├── util_scripts.py             # Merger helpers for scripts
│   ├── util_presentations.py       # Merger helpers for presentations
│   ├── template_tools.py           # Template utilities
│   ├── colorama/                   # Terminal color support
│   └── defaults/                   # Default merger data
├── process/                        # Legacy build pipeline (one processor per module type)
│   ├── process_scripts.py          # Scripts processor
│   ├── process_game_menus.py       # Game menus processor
│   ├── process_presentations.py    # Presentations processor
│   ├── process_dialogs.py          # Dialogs processor
│   ├── process_items.py            # Items processor
│   └── ...                         # One per module type (troops, parties, scenes, etc.)
├── source/                         # Module system root
│   ├── module_scripts.py           # Manifest — imports + extends all scripts
│   ├── module_game_menus.py        # Manifest — imports + extends all game menus
│   ├── module_presentations.py     # Manifest — imports + extends all presentations
│   ├── module_dialogs.py           # Dialogs (not atomized yet)
│   ├── module_troops.py            # Troop definitions
│   ├── module_items.py             # Item definitions
│   ├── module_parties.py           # Party definitions
│   ├── module_scenes.py            # Scene definitions
│   ├── module_strings.py           # String definitions
│   ├── module_constants.py         # Constants and tunable values
│   ├── module_simple_triggers.py   # Manifest — imports + extends all simple triggers
│   ├── module_triggers.py          # Manifest — imports + extends all triggers
│   ├── module_info_pages.py        # Game concept info pages
│   ├── module_factions.py          # Faction definitions
│   ├── module_mission_templates.py # Mission templates
│   ├── module_map_icons.py         # Map icons
│   ├── module_meshes.py            # Mesh definitions
│   ├── module_music.py             # Music definitions
│   ├── module_sounds.py            # Sound definitions
│   ├── module_skills.py            # Skill definitions
│   ├── module_skins.py             # Skin definitions
│   ├── module_animations.py        # Animation definitions
│   ├── module_particle_systems.py  # Particle system definitions
│   ├── module_postfx.py            # Post-processing effects
│   ├── module_scene_props.py       # Scene prop definitions
│   ├── module_tableau_materials.py # Tableau material definitions
│   ├── module_quests.py            # Quest definitions
│   ├── module_info.py              # Mod info
│   ├── module_variables.py         # Variable definitions
│   ├── module_party_templates.py   # Party template definitions
│   ├── variables.txt               # Global variable registry (auto-maintained)
│   ├── scripts/                    # ~877 files — one script per file
│   ├── game_menus/                 # ~294 files — one menu per file
│   ├── presentations/              # ~80 files — one presentation per file
│   ├── simple_triggers/            # ~126 files — one simple trigger (or dummy group) per file
│   └── triggers/                   # ~32 files — one trigger per file
├── docs/                           # Documentation
│   ├── guide/                      # In-game player guide drafts
│   └── updates/                    # Changelog by category (features/, fixes/, cheats/, project_structure/)
├── _unused/                        # Decommissioned files
├── .agents/skills/                 # Agent skill definitions (warband-project-orientation, warband-modsys)
├── .codegraph/                     # CodeGraph index (code intelligence)
├── README.md                       # Project readme (includes credits)
└── opencode.json                   # OpenCode configuration
```

## The Architecture Journey: From Monoliths to Vertical Slicing to Flat Atoms

The Dickplomacy Reloaded source originally suffered from massive monolithic files (e.g., `module_scripts.py` was almost 80,000 lines long). To improve maintainability, we went through several architectural phases:

1. **Atomization:** We broke down the giant monolithic files (`module_scripts.py`, `module_presentations.py`, `module_game_menus.py`) so that every single script, presentation, and menu was extracted into its own isolated `.py` file.
2. **Vertical Slicing (Experiment):** We initially attempted to organize these hundreds of new atomic files into domain-specific subfolders (e.g., `scripts/multiplayer/`, `game_menus/diplomacy/`, `presentations/arena/`).
3. **The Rollback (Current State):** Empirical call-graph analysis revealed that the Warband engine's logic is highly coupled — over 76% of script calls crossed our artificial domain boundaries. The vertical slicing created too much overhead and miscategorization. We rolled back the nested domain folders in favor of a clean, flattened directory structure.

### Atomic Component Directories

All logic is isolated into single files, stored flatly in their respective component directories:

- `source/scripts/`: Contains all ~890 atomic script files.
- `source/game_menus/`: Contains all ~290 atomic game menu files.
- `source/presentations/`: Contains all ~74 atomic presentation files.
- `source/simple_triggers/`: Contains all ~126 atomic simple trigger files (each exports `<name>_simple_triggers`).
- `source/triggers/`: Contains all ~32 atomic trigger files (each exports `<name>_triggers`).

### The Manifest Files

The original `module_*.py` files (e.g., `module_scripts.py`, `module_game_menus.py`, `module_simple_triggers.py`, `module_triggers.py`) now sit at the root of `source/`. They act purely as **manifests** or **assemblers**. They contain no inline logic; instead, they import the atomic files from the directories above and `extend()` them into the master arrays required by the compiler. The modmerger hook (`# modmerger_start` block) stays at the bottom of each manifest verbatim so submods still merge their trigger blocks in.

## Generated vs Hand-Authored Classification

Knowing what's safe to hand-edit vs what's compiler output is critical.

| Class | Meaning | Edit? |
|-------|---------|-------|
| **HAND-AUTHORED** | Human writes and maintains directly | Yes |
| **GENERATED-INPUT** | Human writes, but exists solely to feed the compiler | Yes — this is where game design lives |
| **GENERATED-OUTPUT** | Produced by compile; never hand-edit | No — safe to ignore unless debugging compiler |

### By area

| Path | Class | Notes |
|------|-------|-------|
| `source/scripts/**/*.py` | HAND-AUTHORED | Script tuple bodies; primary edit surface for logic |
| `source/game_menus/**/*.py` | HAND-AUTHORED | Menu definitions |
| `source/presentations/**/*.py` | HAND-AUTHORED | Presentation definitions |
| `source/module_*.py` (entity lists) | GENERATED-INPUT | Authoritative source of record order and content |
| `source/module_constants.py` | HAND-AUTHORED | Slot indices, `$g_*` names, faction range markers |
| `source/variables.txt` | HAND-AUTHORED | Global variable name list |
| `source/headers/**` | HAND-AUTHORED | Stable engine constants |
| `source/modmerger/**` | HAND-AUTHORED | Framework + submod patch files |
| `source/ids/ID_*.py` | **GENERATED-OUTPUT** | Never hand-edit — overwritten every compile |
| `source/process/**` | HAND-AUTHORED (legacy) | Old export pipeline; not used by `compile.bat` |
| `compiler/**` | HAND-AUTHORED | W.R.E.C.K. itself |
| Game module `.txt` files | **GENERATED-OUTPUT** | `scripts.txt`, `troops.txt`, `menus.txt`, etc. |

## Compiler Flow

```
compile.bat
  └─ deletes *.pyc (prevents stale bytecode after file moves)
  └─ python compiler\compile.py tag [args]
       └─ bootstrap_paths.setup_paths()
            └─ adds to sys.path:
                 source/
                 headers/
                 ids/
                 process/
                 modmerger/
                 modmerger/mods/*/
                 compiler/
       └─ WRECK parses manifest files (module_*.py)
            └─ resolves scripts/, game_menus/, presentations/ packages via imports
            └─ processes modmerger mods
            └─ writes output to Modules/Dickplomacy Reloaded/
            └─ regenerates ID files (ids/ID_*.py)
       └─ tag mode: prefixes all IDs (trp_player, itm_sword, mnu_camp, etc.)
            for human-readable output instead of raw numbers
```

### W.R.E.C.K. Phases (in order)

1. **Load module** — `module_info.py` (export_dir, plugins), required `module_*.py` (fixed import order). Modmerger hooks at the bottom of many files mutate lists before compile.
2. **Load plugins** — WRECK plugin injections (if any registered).
3. **Check module syntax** — validate all entity lists.
4. **Allocate identifiers** — positional IDs from list order; verify no undefined references.
5. **Compile module** — preprocess (entity + plugin preprocessors), per-entity processor + aggregator, postprocess.
6. **Export module** — write `.txt` binaries to `export_dir`, regenerate `source/ids/ID_*.py`.

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

### Path Bootstrapping

`compiler/bootstrap_paths.py` dynamically adds `source/` and other root folders to Python's `sys.path`. When the compiler runs, it resolves imports as if everything was still sitting in a single flat directory. This is what allows moving files around without rewriting thousands of `from header_common import *` statements.

## Importance of Manifest Ordering & Save Compatibility

**The order of imports in manifest files is critical.** It dictates the generated Warband ID numbers (e.g., `ID_scripts.py`). Modifying the order in the manifests will shift the IDs and break save-game compatibility.

- Always **append** new imports and `.extend()` calls to the **bottom** of the list — never insert mid-list.
- Never reorder existing imports in `module_scripts.py`, `module_game_menus.py`, `module_presentations.py`, `module_simple_triggers.py`, or `module_triggers.py`.
- `ID_*.py` files are regenerated automatically on every successful compile. The source of truth for IDs is list position in the corresponding `module_*.py`, not the ID file.

## What Was Removed / Changed

| Original | Current | Reason |
|----------|---------|--------|
| `source/module/` (nested subfolder) | `source/` (flat) | Flattened — module_*.py now live at source root |
| `source/module/native/scripts/` | `source/scripts/` | Flattened — native layer removed |
| `source/compiler/` | `compiler/` (repo root) | Moved to root for cleaner source/ |
| `source/lib/` | `source/modmerger/` | Renamed to reflect actual framework name |
| `source/mods/` | `source/modmerger/mods/` | Moved inside modmerger |
| `dummypyc` | deleted | Legacy unused artifact |
| `userDefineLang.xml` | deleted | Notepad++ config, build-irrelevant |
| `credits.txt` | merged into `README.md` | Consolidated documentation |

## What Touches What: Dependency Map

High-level dependency map for "if I change X, what else is affected":

```
module_items.py  ──order──►  ID_items.py  ──imported by──►  module_troops, module_constants,
                                                              module_scripts, presentations, ...

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

### Common Cross-Reference Patterns

| From | References | By |
|------|------------|-----|
| Dialogs, menus, triggers, scripts, presentations | Scripts | `(call_script, "script_<name>")` — string name, not numeric |
| Menus | Other menus | `(jump_to_menu, "mnu_<id>")` |
| Menus, scripts | Presentations | `(start_presentation, "prsnt_<id>")` |
| Troops | Items | Inventory lists use `"itm_*"` string constants |
| Any operation block | Troops, factions, items, strings | `"trp_*"`, `"fac_*"`, `"itm_*"`, `"str_*"` |
| Dialogs | Troops | Partner field: `trp_*`, `anyone`, `anyone|plyr` |
| Mission templates | Scenes, troops, items | Spawn tuples, disguise item lists |
| `module_constants.py` | ID files | Range boundaries (`*_begin`/`*_end`) depend on stable ordering |

## Naming / ID Conventions

### String Constants vs Numeric IDs

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

### Flag / Type Prefixes (in `headers/`, not ID files)

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

### Do Humans Need Numeric IDs?

**Almost never.** Author in `module_*.py` using bare name strings; reference elsewhere using prefixed string constants (`"trp_player"`, `"itm_sword"`, etc.). W.R.E.C.K. resolves these to integers at compile time.

**Exceptions where numbers matter:**
- **List order** in `module_*.py` — positional; reordering changes all downstream numeric IDs and breaks saves if done carelessly.
- **Hardwired item block** — first N items in `module_items.py` are engine-fixed (see comment at L55).
- **`module_constants.py` slot numbers** — hand-assigned integers for `$variable` slots and `slot_*` indices; must stay stable across saves.
- **Face codes, mesh modifiers** — literal hex/int in troop/item records.

## How to Work in This Architecture

- **To edit existing logic:** Find the specific file in `source/scripts/`, `source/game_menus/`, `source/presentations/`, `source/simple_triggers/`, or `source/triggers/` and modify it. You do not need to touch the manifest files.
- **To add new logic:**
  1. Create a new atomic file in the appropriate directory (e.g., `source/scripts/my_new_script.py`).
  2. Open the corresponding manifest file (e.g., `source/module_scripts.py`).
  3. Add the import statement and `extend()` call at the bottom of the list.
  4. Run `compile.bat` to regenerate the `ids/` and build the `.txt` files.
- **To add a new trigger:** create `source/triggers/my_trigger.py` exporting `my_trigger_triggers = [...]`, then append `from triggers.my_trigger import my_trigger_triggers` and `triggers.extend(my_trigger_triggers)` at the bottom of `source/module_triggers.py`.
- **Do not manually edit `ID_*.py` files:** These are strictly generated output.

### Encoding

All `.py` under `source/` should use `# -*- coding: cp1254 -*-` as line 1 where non-ASCII appears. Read/write as cp1254, not UTF-8.

### Python Version

Module source targets **Python 2.7** syntax: no f-strings, `print` statement, `xrange`, `except Exception, e`, etc.

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

## The Philosophy

Atomize → decouple → reduce agent and human cost.

- **First attempt:** domain-based modularization (scripts grouped by theme — abandoned due to inconsistent naming)
- **Current state:** granular — one file per script/menu/presentation
- **Goal:** enables single-file edits, future bridge system for external tools, eventual choice of a new workflow
