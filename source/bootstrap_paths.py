# Shared import-path setup for W.R.E.C.K. and legacy process pipeline.
# Import this module before any module/header/ID/mod imports.

import os
import sys

SOURCE_ROOT = os.path.dirname(os.path.abspath(__file__))

_STANDARD_PATHS = (
	"compiler",
	"headers",
	"module",
	"ids",
	"process",
	"lib",
)


def _ensure_path(path):
	if os.path.isdir(path) and path not in sys.path:
		sys.path.insert(0, path)


def setup_paths(source_root=None):
	root = source_root or SOURCE_ROOT
	for name in _STANDARD_PATHS:
		_ensure_path(os.path.join(root, name))
	mods_root = os.path.join(root, "mods")
	if os.path.isdir(mods_root):
		for mod_name in os.listdir(mods_root):
			mod_path = os.path.join(mods_root, mod_name)
			if os.path.isdir(mod_path):
				_ensure_path(mod_path)


setup_paths()
