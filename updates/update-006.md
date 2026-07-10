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

## The Roadmap

### [x] Phase 0: Preparation
- [x] Document the plan in `updates/update-006.md`
- [x] Write an automated, bullet-proof Python extraction script (`updates/extract_scripts.py`) that uses bracket counting to extract whole script tuples safely and preserves their original sequence.
- [x] Verify baseline compilation with `compile.bat`.

### [x] Phase 1: Small & Safe Domains (Completed)
Extracting the most isolated systems to test the pipeline.
- [x] **Music & Sound** -> `native/scripts/music/`
- [x] **Orders** -> `native/scripts/orders/`
- [x] **Siege** -> `native/scripts/siege/`
- [x] **Training Ground** -> `native/scripts/training_ground/`
- [x] **Multiplayer** -> `native/scripts/multiplayer/`

### [x] Phase 2: Medium-Risk Domains (Completed)
- [x] **Economy & Trade** -> `native/scripts/economy/`
- [x] **Quest System** -> `native/scripts/quests/`
- [x] **Morale & Courage** -> `native/scripts/morale/`
- [x] **Banner & Heraldry** -> `native/scripts/heraldry/`

### [ ] Phase 3: Complex Core Mechanics (Native)
Extracting deeply interconnected but well-defined Native logic domains.
- [ ] **Tournament & Arena** -> `native/scripts/arena/`
- [ ] **Encounters & Battle Setup** -> `native/scripts/encounters/`
- [ ] **Party AI & Routing** -> `native/scripts/party_ai/`
- [ ] **Center Management** (Prosperity, building, reinforcements) -> `native/scripts/centers/`
- [ ] **NPC Logic & Conversations** (Companions, Lords) -> `native/scripts/npcs/`
- [ ] **Faction AI & Politics** (War/Peace, Marshals) -> `native/scripts/faction_ai/`

### [ ] Phase 4: The Core Loop & Remaining Native Scripts
- [ ] **Core Game Loops** (Initialization, time progression, game start) -> `native/scripts/core/`
- [ ] Anything remaining that is strictly Native Mount & Blade Warband.

### [ ] Phase 5: The Mod Content (Dickplomacy & Diplomacy)
- [ ] **Diplomacy Mod Logic** -> `diplomacy/scripts/`
- [ ] **Dickplomacy Mod Logic** (Adult content, extended features) -> `dickplomacy/scripts/`

## Tracking Progress
We are currently entering **Phase 3**. The assembly pattern has proven stable, and we are working our way down the file.
