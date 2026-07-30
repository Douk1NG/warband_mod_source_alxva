# Lord Personality Display

Lord reputation/personality type displayed on the character page after meeting them.

## source/scripts/core/core_scripts.py, module_strings.py
- `script_game_get_troop_note` initializes `s61` to "unknown", then replaces it with matching `str_personality_archetypes` entry
- Hidden until player has met the lord (always visible in cheat mode)
- Displayed as "Personality: {s61}" in `str_lord_info_string`
