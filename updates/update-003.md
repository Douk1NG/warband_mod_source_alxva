# Update 003 - Source Folder Refactor (Complete)

## Overview

We successfully reorganized the Dickplomacy Reloaded `source` directory. Previously, it was a completely flat structure containing over 200 Python files, making navigation and maintenance difficult. We have now refactored this into a clean, logical folder hierarchy.

**Crucially, this was achieved without altering any existing Python syntax or breaking the build pipelines.** Both the W.R.E.C.K. compiler (`compile.bat`) and the legacy process pipeline (`build_module.bat`) are fully functional.

## The New Folder Structure

The source files have been grouped by their prefix and purpose into the following layout:

*   **`compiler/`**: Contains the W.R.E.C.K. compiler core (`compiler.py`).
*   **`headers/`**: Opcode definitions and shared constants (`header_*.py`).
*   **`module/`**: The core Module-system data (troops, items, scripts, scenes, etc. - `module_*.py`).
*   **`ids/`**: Generated identifier constants (`ID_*.py`). These are dynamically rewritten on each compile.
*   **`process/`**: Legacy export pipeline scripts (`process_*.py`).
*   **`mods/`**: Contains subfolders for each Modmerger plugin overlay (e.g., `cstm`, `tournament`, `freelancer`).
*   **`lib/`**: Shared tooling, including `util_*`, Modmerger core files, `colorama`, and `template_tools`.

Entry points like `compile.py`, `compile.bat`, and `build_module.bat` remain at the root of the `source/` folder.

## How It Works (The Bootstrap Mechanism)

To avoid rewriting `import` statements across ~200 files (e.g., changing `from header_common import *` to `from headers.header_common import *`), we introduced a dynamic path resolution system.

A new script, `bootstrap_paths.py`, sits at the source root. It dynamically adds all the new subfolders (including every active mod folder inside `mods/`) to the Python `sys.path` environment variable during runtime. 

By having our entry points (`compile.py` and `process/process_common.py`) import this bootstrap first, the Python interpreter is tricked into finding the relocated files as if they were still sitting in a flat directory.

## Compilation Blockers Resolved (The BOM Issue)

During the smoke testing phase, we encountered a `SyntaxError: encoding problem: cp1254 with BOM` which halted the `compile.bat` build. 

*   **The Issue:** 16 Python files (including `module_scripts.py` and `compiler.py`), as well as `compile.bat` and `build_module.bat`, contained invisible UTF-8 Byte Order Marks (BOM: `\xEF\xBB\xBF`) at the very beginning of the files. This conflicted directly with the `# -*- coding: cp1254 -*-` declarations required by the Warband module system.
*   **The Fix:** We wrote a custom script to detect and cleanly strip these 3-byte BOM markers from all affected files without altering a single character of the actual Python code. This instantly resolved the encoding conflicts and unblocked the compilers.

## Modmerger & Adding New Mods

The Modmerger system dynamically imports plugins by name. Our new structure fully supports this. 
To add a new mod in the future:
1. Create a `mods/{modname}/` directory and place your `{modname}_*.py` files inside.
2. Add `{modname}` to the `mods_active` list in `lib/modmerger_options.py`.
3. The `bootstrap_paths.py` script will automatically discover the new folder and include it in the paths—no manual path registration is required.

## Next Steps & Future Planning

With a clean, stable folder structure in place, we are well-positioned for deeper architectural improvements. Potential next steps include:
1. **Splitting Monolithic Files:** Breaking down massive files like `module_scripts.py` and `module_dialogs.py` into smaller, domain-specific files within the `module/` directory.
2. **Normalizing Mod Overlays:** Standardizing the patterns used by the various overlays in the `mods/` directory.
3. **Pipeline Consolidation:** Evaluating if W.R.E.C.K. can completely replace the legacy `process_*` pipeline to reduce maintenance overhead.
