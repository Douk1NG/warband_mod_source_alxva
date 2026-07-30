# Folder Roles and Key Files

## source/scripts/ — One File Per Script

**~877 files.** Every Warband script lives in its own `.py` file inside `source/scripts/`. Each file exports a list of script tuples (name, flags, body) that gets imported into `module_scripts.py`.

Key conventions:
- File name matches the script name (e.g. `auto_upgrade_troops.py` → `auto_upgrade_troops_scripts`)
- Each file defines a `*_scripts` list with one or more scripts
- The manifest (`module_scripts.py`) imports and extends them all
- Conditional function scripts prefixed `cf_` (e.g. `cf_check_hero_can_escape_from_player.py`)
- `__init__.py` and `_helpers.py` exist at `scripts/` root for package support

## source/game_menus/ — One File Per Menu

**~294 files.** Each menu in its own file, prefixed `mnu_`. Same pattern — import + extend in `module_game_menus.py`.

Naming: `mnu_<menu_name>.py` → exports `<menu_name>_menu`

## source/presentations/ — One File Per Presentation

**~80 files.** Each presentation in its own file, prefixed `prsnt_`. Same pattern — import + extend in `module_presentations.py`.

Naming: `prsnt_<name>.py` → exports `<name>`

## Manifest Files (source/module_*.py)

These are the **build entry points**. They contain zero inline logic — only imports and `.extend()` calls.

Example pattern (`module_scripts.py`):
```python
from scripts.auto_upgrade_troops import auto_upgrade_troops_scripts
from scripts.abort_quest import abort_quest_scripts
# ... ~877 imports ...

scripts = []
scripts.extend(auto_upgrade_troops_scripts)
scripts.extend(abort_quest_scripts)
# ...
```

**IMPORTANT:** The order of imports and extends must never change. It determines the generated Warband ID numbers. Changing order breaks save-game compatibility.

Manifests that have been atomized:
- `module_scripts.py` — fully atomized (~877 files)
- `module_game_menus.py` — fully atomized (~294 files)
- `module_presentations.py` — fully atomized (~80 files)

Not yet atomized:
- `module_dialogs.py` — still monolithic (engine-locked dialog structure)
- All other `module_*.py` (troops, items, parties, etc.)

## module_constants.py — Tunable Values

Holds gameplay constants that can be adjusted without touching logic:
- `num_max_bandits` (bandit caps)
- `bandit_lair_respawn_hours`
- `num_max_manhunters`

## module_strings.py — Text Content

All in-game text strings. New features that display text to the player need entries here.

## modmerger/ — Plugin Overlay System

Framework for mods that inject changes into the build without modifying core files.

```
modmerger/
├── modmerger.py             # Core engine — applies mod overlays
├── modmerger_options.py     # Mod configuration
├── mods/                    # Individual mod input sets
│   ├── xgm_mod_options/    # XGM mod options (auto-upgrade, etc.)
│   └── cstm/               # CSTM features (troop tree editor, all-items, etc.)
├── util_scripts.py          # Helpers for script merging
├── util_presentations.py    # Helpers for presentation merging
├── template_tools.py        # Presentation template tools
└── colorama/               # Terminal colors for build output
```

## process/ — Legacy Build Pipeline

One processor per module type. These are called by WRECK during compilation:

| File | Processes |
|------|-----------|
| `process_scripts.py` | Scripts → module_scripts.txt |
| `process_game_menus.py` | Game menus → module_game_menus.txt |
| `process_presentations.py` | Presentations → module_presentations.txt |
| `process_dialogs.py` | Dialogs → module_dialogs.txt |
| `process_items.py` | Items → module_items.txt |
| `process_troops.py` | Troops → module_troops.txt |
| `process_parties.py` | Parties → module_parties.txt |
| `process_scenes.py` | Scenes → module_scenes.txt |
| `process_strings.py` | Strings → module_strings.txt |
| `process_info_pages.py` | Info pages → info_pages.txt |
| ... | ... |
| `process_line_correction.py` | Post-processing line fixes |

## compiler/ — WRECK Build Engine

| File | Role |
|------|------|
| `compiler.py` | Core WRECK engine — parses, resolves IDs, generates output |
| `compile.py` | Orchestrator — sets up paths, version checks, color, timing |
| `bootstrap_paths.py` | Configures `sys.path` for all module system folders |
| `id_paths.py` | ID file write location template |
| `build_module.bat` / `.sh` / `build_module_lav.bat` | Alternative build entry points |

## headers/ — Opcode Definitions

Predefined constants and operation macros used in scripts. Key files:
- `header_operations.py` — All Warband opcodes (`(assign,)`, `(troop_get_slot,)`, etc.)
- `header_common.py` — Common constants
- `header_triggers.py` — Trigger constants (`ti_on_agent_killed_or_wounded`, etc.)
- `header_items.py` — Item flags (`itp_merchandise`, etc.)
- `header_presentations.py` — Presentation flags

## module_info.py — Mod Info

Basic mod metadata (name, version, author). Shown in the Warband module launcher.

## module_variables.py — Custom Variable Definitions

Defines slot numbers and custom variables used across scripts.

## ids/ — Auto-Generated ID Files

**Never hand-edit these.** They are overwritten on every compile. Examples:
- `ID_scripts.py` — `script_my_script = 1234`
- `ID_troops.py` — `trp_player = 0`
- `ID_menus.py` — `mnu_camp = 42`
