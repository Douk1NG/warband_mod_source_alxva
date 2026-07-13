# Update 008 - Folder & Files Restructure (Flatten source/)

## Summary

Flattened the `source/module/` directory. `module_*.py` definition files and the
`scripts/` package now live directly under `source/`, and the build/config entry files were
moved up to the repository root. This removes the redundant `module/` and `native/` nesting
layers so the layout is shallower and the build entry points sit at the repo root.

## Changes

### 1. Delete `source/module/`, flatten its contents
- **Target Files**: `source/module/`
- **Change Made**: Deleted `source/module/`. `module_*.py` definition files were moved
  to `source/module_*.py`, and `source/module/native/scripts/` was moved to `source/scripts/`
  (the `native` package layer was removed entirely). `source/module/native/__init__.py` is gone.
o errors.

## Notes

- Library folders (`compiler/`, `headers/`, `ids/`, `process/`, `modmerger/`) remain under
  `source/`. `modmerger/` holds the modmerger framework (`modmerger.py`, `modmerger_options.py`,
  `util_*.py`, `template_tools.py`, `colorama/`, `defaults/`) plus its input set under
  `modmerger/mods/` (previously a top-level `source/mods/`).
- The `modmerger/mods/` mechanism and the W.R.E.C.K. compiler are unaffected; they import `module_*`
  and `scripts` by bare name, and `bootstrap_paths._SOURCE_PATHS` now lists `modmerger` (was `lib`)
  with `mods_root = source/modmerger/mods`.
