@echo off

rem Remove stale .pyc bytecode before importing anything. compile.py sets
rem sys.dont_write_bytecode=True, so it never refreshes .pyc files;
rem after a folder restructure (e.g. git mv) an old .pyc can be imported
rem instead of the moved .py, silently producing corrupt module data.
del /s /q *.pyc 2>nul

call python compiler\compile.py tag %1 %2 %3 %4 %5 %6 %7 %8 %9
pause

