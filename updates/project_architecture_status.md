# Project Architecture Summary

This document consolidates and supersedes previous architectural updates (003, 006, 008, 011, 012, and 013/014). It reflects the current, stable state of the `source/` directory and the rationale behind our structural decisions.

## 1. The Journey: From Monoliths to Vertical Slicing to Flat Atoms

The Dickplomacy Reloaded source originally suffered from massive monolithic files (e.g., `module_scripts.py` was almost 80,000 lines long). To improve maintainability, we went through several architectural phases:

1. **Atomization:** We successfully broke down the giant monolithic files (`module_scripts.py`, `module_presentations.py`, and `module_game_menus.py`) so that every single script, presentation, and menu was extracted into its own isolated `.py` file.
2. **Vertical Slicing (Experiment):** We initially attempted to organize these hundreds of new atomic files into domain-specific subfolders (e.g., `scripts/multiplayer/`, `game_menus/diplomacy/`, `presentations/arena/`). 
3. **The Rollback (Current State):** Empirical call-graph analysis revealed that the Warband engine's logic is highly coupled (over 76% of script calls crossed our artificial domain boundaries). The vertical slicing created too much overhead and miscategorization. We decided to roll back the nested domain folders in favor of a clean, **flattened directory structure**.

## 2. The Current Directory Structure

The project now uses a shallow, horizontal structure where components are grouped by their module type rather than their thematic domain. 

### Atomic Component Directories
All logic is isolated into single files, but they are stored flatly in their respective component directories:
- `source/scripts/`: Contains all ~890 atomic script files.
- `source/game_menus/`: Contains all ~290 atomic game menu files.
- `source/presentations/`: Contains all ~74 atomic presentation files.

### The Manifest Files
The original `module_*.py` files (e.g., `module_scripts.py`, `module_game_menus.py`) now sit at the root of `source/`. They act purely as **manifests** or **assemblers**. They contain no inline logic; instead, they simply import the atomic files from the directories above and `extend()` them into the master arrays required by the compiler.

**Important Note on Ordering:** The order of imports in these manifest files is critical because it dictates the generated Warband ID numbers (e.g., `ID_scripts.py`). Modifying the order in the manifests will shift the IDs and break save-game compatibility.

### Library and Tooling Directories
- **`source/compiler/`**: Contains the W.R.E.C.K. compiler core.
- **`source/headers/`**: Opcode definitions and shared constants (`header_*.py`).
- **`source/ids/`**: Generated identifier constants (`ID_*.py`). These are dynamically rewritten by W.R.E.C.K. on each compile.
- **`source/process/`**: Legacy export pipeline scripts.
- **`source/modmerger/`**: The Modmerger framework and its `mods/` input set.

## 3. Compilation and Path Bootstrapping

To support moving files around without rewriting thousands of `from header_common import *` statements, we use `compiler/bootstrap_paths.py`. 

This script dynamically adds `source/` and other root folders to the Python `sys.path`. When the compiler (`compile.bat`) runs, it resolves imports as if everything was still sitting in a single flat directory. 

## 4. How to Work in This Architecture

- **To edit existing logic:** Find the specific file in `source/scripts/`, `source/game_menus/`, or `source/presentations/` and modify it. You do not need to touch the manifest files.
- **To add new logic:** 
  1. Create a new atomic file in the appropriate directory (e.g., `source/scripts/my_new_script.py`).
  2. Open the corresponding manifest file (e.g., `source/module_scripts.py`).
  3. Add the import statement and `extend()` call at the bottom of the list.
  4. Run `compile.bat` to regenerate the `ids/` and build the `.txt` files.
- **Do not manually edit `ID_*.py` files:** These are strictly generated output.
