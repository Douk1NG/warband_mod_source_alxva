# Update 006 - Modularizing module_scripts.py

## Overview
`module_scripts.py` is the largest file in the codebase (almost 80,000 lines). It contains 671 scripts, including heavy custom modifications for Diplomacy and Dickplomacy. To make this manageable, we are breaking it down into domain-specific files using an Assembly Pattern, similar to how we handled `module_strings.py`.

Unlike strings, scripts are referenced by name rather than array index, which gives us the flexibility to reorder them safely without breaking engine lookups. However, to preserve developer sanity, we will ensure that clustered scripts (e.g., base scripts followed by their `_aux`, `_alt`, or fixes) are kept strictly together in their original relative top-to-bottom sequence.

## Planned Folder Structure
We will extract scripts into `source/module/native/scripts/` organized by domain folders:
- `multiplayer/`
- `music/`
- `orders/`
- `siege/`
- `training_ground/`
- `economy/`
- `quest/`
- ...and so on.

Mod-specific scripts will go into:
- `diplomacy/`
- `dickplomacy/`

## Phase 1 Execution (In Progress)
Currently executing **Phase 1**: Extracting small, isolated, safe domains (Multiplayer, Music, Orders, Siege, Training Ground) to validate the pipeline before moving on to complex heavily interconnected scripts (like NPC logic or Party AI).
