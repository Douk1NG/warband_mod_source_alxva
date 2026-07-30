# Script Modularization Attempt

An early attempt to break `module_scripts.py` into domain-based modules. Later replaced by the granular (one file per script) refactor.

## Phase 1 — Safe Domains (9bc0372)
Extracted low-risk, self-contained script groups into separate modules.

## Phase 2 — Medium-Risk Domains (30f64ca)
Extracted moderately coupled script groups.

## Phase 3 — Complex Native Mechanics (cd4efe7)
Extracted tightly coupled native mechanics scripts.

## Documentation Update (33a4b85)
- Updated docs reflecting the modular structure
- Regenerated ID files

## Outcome
The modular (domain-based) structure was abandoned due to inconsistent naming and organizational issues. Replaced by a granular approach where each script is its own file.
