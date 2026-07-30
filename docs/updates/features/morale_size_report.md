# Combined Morale & Size Report

Separate "View party morale report" and "View party size report" menus removed and replaced with a single combined presentation.

## Access
Reports → Character/Party Reports → View combined morale and size report.

## source/game_menus/mnu_reports_character.py
- Removed "View party size report" (mnu_party_size_report)
- Removed "View party morale report" (mnu_morale_report)
- Added "View combined morale and size report" → `prsnt_party_size_and_morale`

## source/module_game_menus.py
- Removed imports and menu list entries for `mnu_morale_report` (#15) and `mnu_party_size_report` (#21)
- Old menu files moved to `_unused/`

## source/presentations/prsnt_party_size_and_morale.py
- New presentation showing party size, morale, and related details in one screen
