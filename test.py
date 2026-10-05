#!/usr/bin/env python3
"""Run the module-system invariants test suite.

This is a thin wrapper around `pytest`. It's here so any agent (or Marlon)
can run the tests without remembering the right command, and so the
intent is obvious when the script shows up in `compile.bat` or a CI step.

Usage:
    python test.py             # run all tests
    python test.py -v          # verbose
    python test.py -k bandit   # only tests matching "bandit"
    python test.py --help      # full pytest options

Exit code: 0 if all tests pass, non-zero otherwise. Safe to chain from
compile.bat or any automation.
"""
from __future__ import annotations

import subprocess


def run() -> int:
    # We invoke pytest via `python -m pytest` rather than importing it,
    # so the same code path runs whether the caller does `python test.py`
    # or `python -m pytest tests/` directly.
    cmd = ["python", "-m", "pytest", "tests/", *__import__("sys").argv[1:]]
    print(f"[test.py] running: {' '.join(cmd)}")
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(run())