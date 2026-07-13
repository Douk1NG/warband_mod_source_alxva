# Update 008 - Folder & Files Restructure (Flatten source/)

## Summary

Flattened the `source/module/` directory. The 30 `module_*.py` definition files and the
`scripts/` package now live directly under `source/`, and the build/config entry files were
moved up to the repository root. This removes the redundant `module/` and `native/` nesting
layers so the layout is shallower and the build entry points sit at the repo root.

## Changes

### 1. Delete `source/module/`, flatten its contents
- **Target Files**: `source/module/`
- **Change Made**: Deleted `source/module/`. Its 30 `module_*.py` definition files were moved
  to `source/module_*.py`, and `source/module/native/scripts/` was moved to `source/scripts/`
  (the `native` package layer was removed entirely). `source/module/native/__init__.py` is gone.

### 2. Move build/config files to the repository root
- **Target Files**: `source/` -> repo root (`source_dckplomacy/`)
- **Change Made**: Moved the following files up one level to the repo root:
  `bootstrap_paths.py`, `id_paths.py`, `compile.py`, `compile.bat`, `build_module.bat`,
  `build_module.sh`, `build_module_lav.bat`, `credits.txt`, `dummypyc`, `userDefineLang.xml`,
  `variables.txt`, `xgm_mod_options_readme.txt`.

### 3. Rewrite the `native.scripts` import path to `scripts`
- **Target Files**: `source/module_scripts.py`; `source/scripts/feats/__init__.py`
- **Change Made**: Replaced every `from native.scripts.` import with `from scripts.`
  (22 lines in `module_scripts.py`, 3 lines in `scripts/feats/__init__.py`). The `scripts`
  package is now a top-level package under `source/`, and internal cross-folder imports inside
  `scripts/` (which already used relative imports) are unaffected by the rename.

### 4. Rewire bootstrap/paths for the new root location
Because `bootstrap_paths.py` (and `id_paths.py`) now live at the repo root, `SOURCE_ROOT` could
no longer point at their own directory.
- **`bootstrap_paths.py`**: added `REPO_ROOT` (the repo root) and redefined
  `SOURCE_ROOT = os.path.join(REPO_ROOT, "source")`; dropped `"module"` from `_STANDARD_PATHS`;
  added `SOURCE_ROOT` itself to `sys.path` so the flat `module_*.py` files and the `scripts`
  package resolve.
- **`compile.py`**: `write_id_files` now targets `os.path.join(bootstrap_paths.SOURCE_ROOT, "ids", ...)`
  so generated ID files are still written to `source/ids` (consistent with `id_paths`).
- **`build_module.bat` / `build_module.sh`**: `cd` into `source/` and put both `source` and the
  repo root on `PYTHONPATH` so `bootstrap_paths`/`id_paths` (root) and `module_*`/`scripts`
  (source) are all importable.
- **`source/process/process_init.py`, `process_global_variables.py`, `process_global_variables_unused.py`**:
  the `variables.txt` reads were pinned to `os.path.join(bootstrap_paths.REPO_ROOT, "variables.txt")`
  because the build runs from `source/` but the file now lives at the repo root.
- **`source/process/process_line_correction.py`**: prepends the repo root to `sys.path` (so it can
  import `bootstrap_paths` from any working directory) and updated its `module_scripts.py` path
  (no longer under `module/`).

## Verification

- `python compile.py` -> **COMPILATION SUCCESSFUL.**
- `build_module.bat` -> full legacy process pipeline ran to completion (`Script processing has ended.`)
  with no errors.

## Notes

- Library folders (`compiler/`, `headers/`, `ids/`, `process/`, `lib/`, `mods/`) remain under `source/`.
- The `mods/` mechanism and the W.R.E.C.K. compiler are unaffected; they import `module_*` and
  `scripts` by bare name.
- `1175source/`, the `updates/*.md` history docs, and `.codegraph/` were intentionally left unchanged.
