# Shared import-path setup for W.R.E.C.K. and legacy process pipeline.
# Import this module before any module/header/ID/mod imports.
#
# This file lives in the repository's `compiler/` folder. REPO_ROOT is the
# repo root; SOURCE_ROOT points at the `source/` folder that holds the
# module_*.py files, the `scripts` package, and the headers/ids/process/modmerger
# folders. `modmerger` holds the modmerger framework plus its `mods/` input set.
# The W.R.E.C.K. compiler package lives at REPO_ROOT/compiler.

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_ROOT = os.path.join(REPO_ROOT, "source")

# Folders under REPO_ROOT that hold module-system code/headers/IDs.
_ROOT_PATHS = (
	"headers",
	"ids",
	"process",
	"modmerger",
)

def _ensure_path(path):
	if os.path.isdir(path) and path not in sys.path:
		sys.path.insert(0, path)

def setup_paths(source_root=None):
	root = source_root or SOURCE_ROOT
	# The `source/` root itself holds module_*.py and the `scripts` package.
	_ensure_path(root)
	for name in _ROOT_PATHS:
		_ensure_path(os.path.join(REPO_ROOT, name))
	# W.R.E.C.K. compiler package lives at REPO_ROOT/compiler.
	_ensure_path(os.path.join(REPO_ROOT, "compiler"))
	mods_root = os.path.join(REPO_ROOT, "modmerger", "mods")
	if os.path.isdir(mods_root):
		for mod_name in os.listdir(mods_root):
			mod_path = os.path.join(mods_root, mod_name)
			if os.path.isdir(mod_path):
				_ensure_path(mod_path)

setup_paths()
