# Native 1175 Bug Fixes Port

Bug fixes ported from the Native 1175 project. Credit to the original authors.

## 1. Optimize Loot Algorithm
- **File:** `module_scripts.py` (`script_party_calculate_loot`)
- Sorts enemy troops by level before loot processing for fairer distribution

## 2. Count Wounded Enemies in Casualties
- **File:** `module_scripts.py`
- Wounded enemies before battle now added to `p_total_enemy_casualties`

## 3. Village Raid Loot/Prisoners
- **File:** `module_mission_templates.py` (`village_raid`)
- Added `ti_on_agent_killed_or_wounded` trigger to record casualties during raids

## 4. Fix Lord Recruitment Dialogues
- **File:** `module_dialogs.py` (`lord_recruit_pledge`)
- Properly assigns `slot_lord_recruitment_candidate` immediately after faction change
- Moves `$g_leave_encounter` assignment to `lord_recruit_pledge_conclude`
- Clears candidate slot after pledge concludes

## 5. Fix Rescued Lords Hostile in Prison Break
- **File:** `module_mission_templates.py` (`prison_break`)
- Replaced hardcoded `(agent_set_team, ":agent_no", 0)` with dynamic player team lookup

## 6. Optimize Battle Morale Logic
- **File:** `module_scripts.py` (`apply_effect_of_other_people_on_courage_scores`)
- Outer loop now skips non-fleeing agents (reduces O(N²) to only fleeing agents)
- Flattened nested conditions into linear `try_begin...else_try` blocks

## 7. Castle Banner Fix on Lord Exile
- **File:** `module_scripts.py` (`indict_lord_for_treason`)
- Added `(party_set_banner_icon, ":center", 0)` when resetting lordless centers

## 8. Fix Wounded Kings/Pretenders in Casualties
- **File:** `module_game_menus.py` (`total_victory`)
- Changed bounds check from `lords_begin, lords_end` to `active_npcs_begin, active_npcs_end`

## 9. Fix Hosting Feast Without Town
- **File:** `module_dialogs.py` (`spouse_feast_confirm_yes`)
- Added `(gt, ":feast_venue", -1)` check before using venue

## 10. Fix Changing Minister Failing Quests
- **File:** `module_dialogs.py` (`minister_replace_confirm`)
- Added `(check_quest_active, ":minister_quest")` before aborting quest

## 11. Fix Rebel Ladies' Faction Update
- **File:** `module_game_menus.py` (`notification_pretender_denounced_ruler`)
- Added loop to move rebel ladies from `fac_player_supporters_faction` back to original faction

## 12. Fix Escort Lady Spouse Quest Dialog
- **File:** `module_dialogs.py` (`spouse_talk`)
- Added check preventing spouse dialog when `qst_escort_lady` is active and arriving at destination

