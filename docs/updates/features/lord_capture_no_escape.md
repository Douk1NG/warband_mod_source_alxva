# Player-Defeated Lord Capture (No Escape)

Lords defeated directly by the player go to captivity instead of rolling the normal escape chance.

## source/scripts/encounters/encounters_scripts.py
- Hero-defeat capture branch sends defeated hero to capture (instead of rolling against `hero_escape_after_defeat_chance`) when `p_main_party` is the winning party

## source/scripts/npcs/npcs_scripts.py
- `script_cf_check_hero_can_escape_from_player` makes regular active kingdom heroes defeated by the player fail the escape check
- Quest targets and bandit leaders keep their existing special behavior
- Does not change the prisoner escape system for heroes already held in parties or centers
