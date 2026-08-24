# KCTT Vanilla Export/Import + Community Sharing Journal

Working journal for replacing the WSE-only KCTT export/import system with a
vanilla-safe savegame backend, while still keeping a path for players to share
troop trees with the mod author/community through external tooling.

## Goal

Remove the hard dependency on WSE for KCTT import/export.

The in-game feature should work in vanilla Warband:

- player creates a KCTT troop tree;
- player saves it into one of several in-save template slots;
- player can load/delete those slots later in the same savegame;
- no `dict_*`, `array_*`, or file IO opcodes are required at runtime.

Community sharing is handled outside the engine:

- player sends a savegame or runs an external extractor;
- extractor reads the KCTT template slots from the savegame;
- extractor outputs a clean JSON/share file;
- author can review, rebalance, and optionally add the tree into the mod via code.

## Current Problem

The existing export/import implementation uses WSE2 persistence:

- `dict_save_json` / `dict_load_file_json` for one JSON file per tree;
- `array_save_file` / `array_load_file` for the 8-slot registry;
- `dict_delete_file` for deleting exported trees.

Vanilla Warband has no general-purpose file write/read API. The native character
exporter is hardcoded to the player character and cannot be reused for arbitrary
troops or full troop trees.

Therefore the vanilla system must store data inside the savegame.

## Chosen Direction

Use hidden/template troops as the canonical in-game storage backend.

Instead of writing `<prefix>.json`, `Export` copies the current KCTT tree into
reserved hidden troops. `Import` copies those hidden troops back into the live
KCTT tree.

This preserves the player-facing workflow while changing what "export" means:

- old WSE meaning: export to external file;
- new vanilla meaning: save tree into an in-save template slot.

Default/importable trees should use the same import-slot screen as player saved
trees. Do not add a separate presentation for defaults.

The current direction is:

- add more neutral KCTT presets so faction/default templates have shapes that
  can fit their branch logic;
- increase the vanilla template bank from 8 slots to 12 slots;
- seed some of those slots with curated/default trees;
- still allow the player to save/load/delete custom trees from the same screen.

Important distinction:

- presets define tree topology;
- import slots hold actual troop-tree data;
- default/faction trees should be implemented as seeded/importable slot data,
  not as a separate `Defaults` presentation.

## Storage Model

Reserve fixed hidden troops for KCTT template slots.

Example layout:

```text
trp_kct_template_slot_0_meta
trp_kct_template_slot_0_node_00
trp_kct_template_slot_0_node_01
...
trp_kct_template_slot_0_node_21

trp_kct_template_slot_1_meta
trp_kct_template_slot_1_node_00
...
trp_kct_template_slot_11_node_21
```

Why 22 nodes per slot:

- preset 4 is the largest current tree;
- smaller presets use only the first N nodes;
- fixed width makes import/export and external extraction simple.

Slot count direction:

- implemented slot count: 12;
- current seeded default/faction coverage: 8 of the 12 slots;
- remaining slots are available for player-created trees.

Default/faction slots:

- currently seeded and visible in the import-slot screen:
  - Swadia;
  - Vaegirs;
  - Khergit Khanate;
  - Nords;
  - Rhodoks;
  - Sarranid Sultanate;
  - Calradian;
  - Falcon.

The meta troop stores slot-level data:

- occupied flag;
- tree index/preset;
- gender, if needed by final design;
- troop count;
- budget mode;
- prefix/tree display name.

Each node troop stores one troop from the tree:

- singular name;
- plural name;
- attributes;
- skills;
- weapon proficiencies;
- equipment item IDs;
- equipment modifiers;
- configured flag;
- equipment-modified flag;
- class override.

Design note: hidden node troops should probably be heroes, so custom names and
runtime troop data persist in savegames reliably.

## Runtime Scripts

Replace the WSE file backend with vanilla copy scripts.

Candidate script responsibilities:

- `script_kct_save_tree_to_slot`
  - derive tree name from prefix;
  - find matching existing slot or first empty slot;
  - copy live KCTT tree into that slot;
  - set metadata;
  - show success/failure message.

- `script_kct_export_tree_to_slot`
  - low-level copy from live tree range to slot node troops.

- `script_kct_import_tree_from_slot`
  - validate occupied flag/version/tree count;
  - copy slot node troops back into live KCTT troops and dummies;
  - restore budget/configured/equipment/class flags;
  - open the creator on success.

- `script_kct_clear_template_slot`
  - clear occupied flag;
  - blank meta/name;
  - optionally reset node troops.

The existing script names can be preserved where useful to minimize UI churn.

## Presentation/UI Changes

Rewrite `prsnt_kct_manage_tree_files` so it no longer uses WSE arrays.

Current WSE dependencies to remove:

- registry array load/save;
- dynamic arrays for row overlay IDs;
- dynamic arrays for checkbox overlay IDs;
- `dict_delete_file`.

Replacement approach:

- read slot names directly from meta troops;
- store row overlay IDs in fixed globals, or in `trp_temp_array_a` troop slots;
- store checkbox overlay IDs in fixed globals, or in `trp_temp_array_b` troop slots;
- Delete becomes "clear in-save slot" instead of deleting a file.

Button labels can remain simple:

- `Load`
- `Delete`
- `Exit`

The creator button may keep `Export`, but a clearer vanilla label might be
`Save Slot`.

## External Sharing Tool

The external tool is not required for normal gameplay. It exists for community
submission and author curation.

Initial tool modes:

```text
kctt-tool extract-save <savegame> --slot N --out tree.json
kctt-tool inspect-json tree.json
kctt-tool json-to-modsys tree.json --out generated_template.py
```

Possible later modes:

```text
kctt-tool import-save <savegame> tree.json --slot N
kctt-tool pack-json tree.json --out share-code.txt
kctt-tool unpack-code share-code.txt --out tree.json
```

Recommended first milestone: extractor only.

Additional author-side conversion target:

```text
kctt-tool wse-json-to-modsys <wse-tree.json> --out generated_template.py
```

This lets the current Calradian/Falcon WSE exports become built-in vanilla
templates instead of being lost when the runtime WSE backend is removed.

Player/community workflow:

1. Player creates a tree in game.
2. Player saves it to KCTT template slot N.
3. Player sends the savegame or extracted JSON.
4. Author reviews the JSON.
5. Author converts the JSON to module-system data.
6. Approved trees can become built-in/curated templates.

## JSON Interchange Format

The external JSON should stay close to the current WSE JSON schema, because the
current schema already represents the full tree.

Suggested top-level shape:

```json
{
  "kct_version": 2,
  "source": "savegame-template-slot",
  "tree": 3,
  "gender": 0,
  "budget": 3,
  "prefix": "Calradian",
  "troops": [
    {
      "name": "Calradian Recruit",
      "plural": "Calradian Recruits",
      "attributes": [6, 5, 6, 5],
      "skills": [],
      "proficiencies": [],
      "equipment": [],
      "configured": 1,
      "equipment_modified": 1,
      "class_override": 0
    }
  ]
}
```

The extractor can output expanded arrays/objects even if the in-game storage is
flat. The tool is allowed to be nicer than the engine.

## Current Status Snapshot

### Done

- Removed the WSE runtime file backend from KCTT import/export.
- Replaced WSE JSON/array operations with vanilla hidden troop storage.
- Added fixed metadata/node storage troops for template slots.
- Added vanilla save/load/clear scripts:
  - `script_kct_save_tree_to_slot`;
  - `script_kct_export_tree_to_slot`;
  - `script_kct_import_tree_from_slot`;
  - `script_kct_clear_template_slot`.
- Rewrote `prsnt_kct_manage_tree_files` to load/delete hidden troop slots
  directly instead of WSE arrays/files.
- Removed stale WSE array-handle cleanup from the KCTT load trigger.
- Added new KCTT preset shapes for template compatibility:
  - Preset 5: 2 branches, 5 tiers;
  - Preset 6: 3 branches, 5 tiers;
  - Preset 7: 2 branches, 4 tiers.
- Kept Preset 4 as the existing large custom graph preset; only its select label
  should describe its intended shape/count, not change its actual topology
  unless explicitly requested.
- Removed the separate default-template presentation after deciding defaults
  belong in the same import-slot flow.
- Compiled successfully after each major stage.

### Left

- Increase template slots from 8 to 12. Done.
- Update `prsnt_kct_manage_tree_files` layout to display 12 slots cleanly. Done
  first pass.
- Decide which slots are seeded default/faction trees and which slots are empty
  player slots. Current implementation: slots 1-6 are native seeded defaults,
  slots 7-8 are Falcon/Calradian WSE conversions, and slots 9-12 are player
  slots.
- Implement default/faction slot seeding in vanilla code. Done for native
  faction templates.
- Convert/import Calradian and Falcon from current WSE data into the new slot
  format. Done; their original WSE JSON files are vendored as compile-time seed
  data.
- Add or adapt faction troop-tree data for Swadia, Vaegirs, Khergit Khanate,
  Nords, Rhodoks, and Sarranid Sultanate.
- QA import/export:
  - save new custom tree;
  - overwrite same-name slot;
  - import seeded/default slot;
  - delete player slot;
  - verify seeded slots are protected or restored, depending final design.
- QA presets:
  - Presets 1-7 selectable;
  - gender selection correct;
  - dummy links correct;
  - branch renderer correct;
  - save/load round-trip correct.
- Research external extractor after the in-game vanilla backend is stable.

## Open Questions

- Should one slot store only the currently selected gender, or both male/female
  versions of a tree?
- Should the UI keep the word `Export`, or rename to `Save Slot` to avoid
  implying disk files?
- Should seeded/default slots be deletable by the player, or protected/read-only?
- Should default slots be copied into empty save slots on new game, or should
  they be re-seeded on every load if missing?
- How should the 12-slot screen distinguish defaults from player custom trees:
  label prefix, color, lock icon, or just naming?
- Do we want the external tool to patch savegames eventually, or only extract
  submissions for the author?
- Can the savegame format be parsed reliably enough for the extractor, or should
  the first external tool work from a controlled dump format instead?
- Should native/faction templates copy exact module troop stats/equipment or be
  balanced/adapted to KCTT budgets/classes?

## Implementation Phases

### Phase 1: Vanilla Backend Design

- Status: mostly done.
- Hidden template troop IDs exist.
- Metadata slots exist.
- Node data uses hidden hero troops.
- Save compatibility implication: changing slot count/node count changes the
  generated troop list and should be treated carefully before release.

### Phase 2: In-Game Save/Load

- Status: mostly done for player slots.
- Template troops exist for the current slot count.
- Live-tree-to-slot copy exists.
- Slot-to-live-tree copy exists.
- Clear slot exists.
- Budget, class override, configured, and equipment-modified state are preserved.
- Remaining: run in-game QA for the 12-slot/default faction imports,
  including Calradian/Falcon.

### Phase 3: UI Rewrite

- Status: done for 8 slots, needs 12-slot layout pass.
- WSE arrays removed from the manage screen.
- Slot labels read from meta troops.
- Fixed globals used for row/checkbox mappings.
- Load/Delete operate on template slots.
- 12-slot layout pass done first pass.
- Default slots are labeled `Default N: ...` and protected from Delete.
- Remaining: visual QA in-game.

### Phase 4: Remove WSE Dependency From KCTT Runtime

- Status: code removal mostly done.
- `dict_*` removed from KCTT import/export runtime.
- WSE `array_*` removed from KCTT import/export UI.
- Load trigger no longer resets WSE array handles.
- Compiles successfully.
- Remaining: vanilla in-game QA without WSE.

### Phase 5: External Extractor Research

- Status: started.
- Target deliverable: a small Windows `.exe` wrapper around a read-only CLI
  extractor, so players can submit custom KCTT trees without installing Python.
- First tool name/direction: `kctt-share-tool`.
- First mode:
  - `extract-save <savegame.sav> --slot N --module <module folder> --out tree.json`
- Save selection UX:
  - the player must be able to select the `.sav` manually;
  - the tool may offer common default folders, but must not assume only one;
  - known folders:
    - `Documents/Mount&Blade Warband Savegames/Dickplomacy Reloaded`;
    - `Documents/Mount&Blade Warband WSE2/Dickplomacy Reloaded/Savegames`.
  - current local test folder:
    - `C:/Users/Dibey/Documents/Mount&Blade Warband Savegames/Dickplomacy Reloaded`.
- Why `.exe`:
  - players can drag/select a `.sav` without setting up Python;
  - a console `.exe` is easier to distribute with the mod than a script;
  - the same code can still run as Python during development.
- Recommended packaging path:
  - implement in Python 3 for maintainability;
  - package with PyInstaller into a single-file Windows executable;
  - keep the source script in `tools/kctt_share_tool/`;
  - ship the `.exe` later under a release/tools folder, not as required runtime.
- Parser strategy:
  - start read-only;
  - parse Warband save structure up to the troop section;
  - use generated `ids/ID_troops.py` to locate
    `trp_kct_template_slot_<n>_meta` and node troops;
  - read meta troop slots/names plus each node troop's stats, inventory,
    flags, class, and persisted custom slots;
  - output the KCTT JSON interchange format.
- References checked:
  - Mount&Blade Modding Wiki documents Warband `.sav` section order and troop
    record fields;
  - WarBend exists as an MIT Python 2.7 savegame reader/writer and can be used
    as a reference or dependency candidate, but first milestone should avoid
    save writes.
- Prototype tasks:
  - create binary reader helpers for int32/uint32/int64/uint64/float/bool/string;
  - reuse/extend the local `tools/recovery/save_fixer.py` header parsing;
  - implement skip parsers for quests, info pages, sites, factions, map tracks,
    party templates, party records, player-party extras, and map events;
  - implement full troop parser;
  - map template slot indexes to troop IDs through `ids/ID_troops.py`;
  - produce JSON for occupied slots only, with `--list-slots` as a convenience.
- Required prototype input:
  - one `.sav` made after saving a custom tree into slot 9-12;
  - the matching built module folder or this repo's generated `ids/` files.

### Phase 6: Community Curation Pipeline

- Status: not started.
- Add `json-to-modsys` converter.
- Define review/balance checklist.
- Decide how curated trees are shipped in-game.
- Document player submission instructions.

### Phase 7: Additional Preset Shapes

- Status: partly done.
- Added neutral preset shapes:
  - Preset 5: 2 branches, 5 tiers;
  - Preset 6: 3 branches, 5 tiers;
  - Preset 7: 2 branches, 4 tiers.
- Preset 4 kept as its existing custom graph; do not change its actual topology
  without an explicit request.
- Remaining:
  - verify select labels;
  - verify dummy/gender behavior in game;
  - make sure preset shapes are sufficient for the faction/default templates.

### Phase 8: Seeded Default/Faction Import Slots

- Status: not started.
- Increase `kct_template_slot_count` from 8 to 12. Done.
- Increase presentation rows/layout to 12. Done first pass.
- Current fixed slot assignments:
  - Slot 1: Swadia;
  - Slot 2: Vaegirs;
  - Slot 3: Khergit Khanate;
  - Slot 4: Nords;
  - Slot 5: Rhodoks;
  - Slot 6: Sarranid Sultanate;
  - Slot 7: Falcon;
  - Slot 8: Calradian;
  - Slots 9-12: player custom trees.
- Add seed data for native factions. Done first pass.
- Add seeding script/start/load logic. Done.
- Seeded slots cannot be deleted from the UI.
- Still pending:
  - visual/gameplay QA;
  - final balance/adaptation pass.
- Keep this inside `prsnt_kct_manage_tree_files`; do not create a separate
  default-template presentation.

## Non-Goals

- No reliance on native character export/import.
- No mandatory WSE.

## Current Decision (2026-08-23 update — hybrid revived)

Vanilla per-save sigue siendo el backend por defecto (slots ocultos `trp_kct_template_slot_*`). Además, **se revivió el backend WSE como opcional y condicional**: mismos índices `8-11` usan `kct_slot_8.json`..`11.json` (`dict_save_json`/`dict_load_file_json`) cuando `neg|is_vanilla_warband 1004` es true, con wrappers `kct_slot_is_occupied/get_name/export_tree/import_tree/clear/save_tree_auto` (`kct_scripts/tree_io.py:209,740`). Sin WSE el juego cae a vanilla sin cambios de UI; con WSE esos 4 slots son cross-save. Ver `export_import_info.md` para esquema y flujos. El tool externo `kctt_share_tool` sigue para share sin WSE.

## Implementation Log

### 2026-08-22

Started the vanilla runtime backend.

Completed:

- Added fixed hidden template storage troops:
  - 8 metadata troops;
  - 8 x 22 node troops.
- Added template metadata constants and troop-id helper functions.
- Replaced KCTT WSE JSON/array save-load scripts with vanilla troop-backed
  slot scripts:
  - `script_kct_export_tree_to_slot`;
  - `script_kct_import_tree_from_slot`;
  - `script_kct_clear_template_slot`;
  - resolver helpers for meta/node storage troops.
- Preserved `script_kct_save_tree_to_slot` as the creator button backend:
  same-name overwrite, otherwise first empty slot.
- Rewrote `prsnt_kct_manage_tree_files` to read hidden template troops directly
  instead of WSE arrays/files.
- Removed stale WSE array-handle cleanup from the KCTT load trigger.
- Compiled successfully with `.\compile.bat`.
- Removed the separate native/default-template presentation direction after
  design review.
- Added neutral graph presets instead:
  - Preset 5: 2 branches, 5 tiers;
  - Preset 6: 3 branches, 5 tiers;
  - Preset 7: 2 branches, 4 tiers.
- Clarified runtime behavior:
  - player `Export`/save is not hardcoded to slot 1;
  - it overwrites a slot with the same tree prefix when one exists;
  - otherwise it uses the first empty slot;
  - if all 8 player slots are full, the player must delete one first;
  - preset choices do not consume player save slots.
- Decided default/faction trees should use the same import-slot presentation,
  not a separate presentation.
- New target: 12 template slots, with 7/8 used for default/faction trees and
  the rest available for player custom trees.
- Implemented 12 slots.
- Implemented six native default/faction slots in the same import presentation:
  Swadia, Vaegirs, Khergit Khanate, Nords, Rhodoks, Sarranid Sultanate.
- Protected seeded default slots from Delete.
- Export now skips seeded default slots and uses only player slots.

Compile notes:

- `COMPILATION SUCCESSFUL`.
- Remaining warnings are pre-existing unused locals in
  `prsnt_cstm_create_troop_tree`.

Still pending:

- In-game manual QA: save a tree, load it back, delete slot, overwrite by same
  name, test all tree shapes and both genders.
- Manual QA for Presets 5-7: select each shape, edit every node, save/export,
  import back from a slot, and apply kingdom recruitment.
- In-game QA for 12-slot presentation and seeded faction imports.
- Added Calradian/Falcon from the WSE export/source files:
  - vendored `Falcon.json` and `Calradian.json` under the KCTT package;
  - loaded them at compile time into vanilla seeded slot operations;
  - protected them as default slots along with the native faction templates;
  - seeded slot count is now 8, leaving slots 9-12 for player saves.
- Temporary save migration added and later retired/commented: old saves seeded
  the 12-slot/default-template bank once through
  `$kct_template_slots_preset8_rhodoks_migrated`; active saves have now been
  updated.
- Corrected native faction defaults to use exact native upgrade topology instead
  of padding existing KCTT shapes with repeated troops.
- Presets now follow the native template logic:
  - Preset 5: Swadia/Vaegirs/Sarranids, 5-tier split with C2 branching to D2/D3;
  - Preset 6: Khergit, 3-branch 4-tier split;
  - Preset 7: Nords, uneven 3-branch 6-tier split;
  - Preset 8: Rhodoks, equal 5-tier split.
- Import now preserves the current gender selector instead of forcing the
  template slot's saved gender. Built-in faction templates are neutral data;
  Male/Female should decide which live troop block receives the import.
- Added a generic gender self-heal for KCTT graph presets 4-8: on new game,
  on save load, and when opening the create-tree presentation, every real troop
  and dummy in skin block 0 is forced male and every real troop/dummy in skin
  block 1 is forced female. This fixes old-save dummy gender pollution without
  adding faction-specific special cases.
- Moved import-slot row labels 10 UI units upward to better align with the
  checkbox rows.
- External savegame/JSON extractor research.
- Retired the temporary 12-slot/Rhodoks/Falcon/Calradian save migration after
  active saves were opened/saved. The code remains commented in the load trigger
  as a breadcrumb in case another migration is needed later.

Known follow-up issues:

- Import preview/session state is currently destructive before the player
  presses the creator Save button: importing a template copies its names into
  the live custom troop/dummy block immediately. If the player exits to choose
  another option without saving, the UI can still show names from the last
  imported branch instead of the previously saved custom tree. Review later:
  either make import stage into a temporary preview buffer, add a cancel/restore
  path, or force the flow to clearly commit/revert before leaving.

Close-out QA:

- Done: manual QA old saves after migration cleanup:
  - import native faction slots 1-6;
  - import Falcon/Calradian slots 7-8;
  - save/export player custom trees into slots 9-12;
  - reload and verify the seeded slots remain visible.
- Done: manual QA gender behavior:
  - presets 5-8 with Male and Female selected;
  - Khergit/Nords imports specifically;
  - verify dummy portraits and store troop bodies agree.
- Done: manual QA branch/display behavior:
  - Swadia, Vaegirs, and Sarranids use preset 5 topology;
  - Khergit uses preset 6;
  - Nords uses preset 7;
  - Rhodoks uses preset 8.
- In-game vanilla import/export is ready to commit.
- External savegame extractor is now a separate follow-up/prototype task.

### 2026-08-23

Hybrid optional revived: wrappers `kct_slot_*` hacen que slots `8-11` usen WSE JSON `kct_slot_8.json` etc cuando WSE está presente (`neg|is_vanilla_warband`) y vanilla troop-slots cuando no. `prsnt_kct_manage_tree_files` y botón Export del creador ya usan wrappers; `quick_strings` vacía corregida (`@` → sin default). Compila y carga ok en native y WSE; cross-save verificado por presencia del archivo.
