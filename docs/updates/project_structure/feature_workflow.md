# Feature Workflow

Step-by-step process for adding a new gameplay feature.

## 1. Create the Script

Create a new `.py` file in `source/scripts/` with one or more script definitions.

```
source/scripts/my_new_feature.py
```

Each file exports a `*_scripts` list:
```python
from header_common import *
from header_operations import *
from module_constants import *

my_new_feature_scripts = [
    ("my_new_feature",
        [
            (store_script_param_1, ":param"),
            # script operations
            (assign, ":result", 1),
        ]),
]
```

The tuple format is: `(name_string, [operation_tuples])`. Flags (optional, defaults to 0) can be added as a second field if needed. The `script_` prefix is added automatically by the compiler. Conditional scripts (used in `(call_script,)` conditions) should be prefixed `cf_`.

## 2. Register in the Manifest

Add import + extend to `source/module_scripts.py`:

```python
from scripts.my_new_feature import my_new_feature_scripts

scripts.extend(my_new_feature_scripts)
```

**Append to the bottom** of both the import block and the extend block — inserting mid-list changes ID ordering and breaks save compatibility.

## 3. Add Menu or Presentation (if needed)

If the feature needs a new menu:
- Create `source/game_menus/mnu_my_feature.py`
- Add import + extend in `source/module_game_menus.py`

If the feature needs a new presentation:
- Create `source/presentations/prsnt_my_feature.py`
- Add import + extend in `source/module_presentations.py`

## 4. Add Strings and Constants (if needed)

- **Strings:** Add entries in `source/module_strings.py` for any new text displayed to the player
- **Constants:** Add tunable values in `source/module_constants.py`
- **Troops/Items/Parties:** Add new entities in their respective `module_*.py`

## 5. Compile

```bash
python compiler\compile.py tag
```

Or from the wrapper (which also clears stale `.pyc` files):
```bash
compile.bat
```

Confirm output shows "COMPILATION SUCCESSFUL".

## 6. Document

Create a documentation file in the appropriate folder:

| Type | Folder |
|------|--------|
| Gameplay feature | `docs/updates/features/<name>.md` |
| Fix | `docs/updates/fixes/<name>.md` |
| Cheat | `docs/updates/cheats/<name>.md` |

## 7. Player Guide (optional)

For game-changer features that significantly impact gameplay, draft a player-facing entry in `docs/guide/`. This content can later be added as an info page (`source/module_info_pages.py`) viewable from Notes → Info Pages in-game.

## Modmerger Overlay Alternative (instead of direct source edits)

For features that should be applied as an overlay (keeping core files untouched):

1. Create a mod folder under `modmerger/mods/<your_mod>/`
2. Place script/string/presentation override files in the mod folder
3. Add the mod to `modmerger/mods_active` so WRECK processes it
4. The mod's files are merged on top of the base definitions during compilation

This approach is used by `xgm_mod_options/` and `cstm/` for optional features that don't belong in the core module.
