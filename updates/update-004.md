# Update 004: Native 1175 Bug Fixes Porting

## Overview
Native 1175 is a native-like mod that preserves the original Warband gameplay experience while fixing numerous bugs and improving performance, since we want to reduce bugs we are porting the bug fixes from Native 1175 to our mod.

**Credits**: The fixes documented and applied in this update are originally from the [Native 1175] project. Full credit goes to the original authors of those fixes.
---

## 1. Optimize Loot Algorithm (Bug Fix 1.0)
- **Target File**: `source/module/module_scripts.py` (`script_party_calculate_loot`)
- **Reason**: In the base game, loot from defeated enemies was gathered without considering troop levels, which could lead to random or unfair distribution.
- **Change Made**: Inserted a block of logic right after fetching the companion stacks of the enemy party. The new logic loops through the enemy's troops, finds the highest-level troops, and sorts them before they are processed for loot dropping.

## 2. Count Wounded Enemies in Casualties (Bug Fix 2.0)
- **Target File**: `source/module/module_scripts.py` (Before battles)
- **Reason**: Wounded enemy troops present in an enemy party before an engagement were not being added to `p_total_enemy_casualties`. This skewed the casualty tracking and post-battle calculations.
- **Change Made**: Added logic immediately following `(party_clear, "p_total_enemy_casualties")`. We now iterate through all stacks in the collective enemy party, identify wounded troops, and add/wound them in `p_total_enemy_casualties` accordingly.

## 3. Fix Village Raid Yielding No Loot/Prisoners (Bug Fix 3.0)
- **Target File**: `source/module/module_mission_templates.py` (`village_raid` template)
- **Reason**: When raiding a village, the mission template lacked a trigger to record casualties when agents were killed or wounded. This resulted in no loot or prisoners being calculated after the raid.
- **Change Made**: Injected a new `ti_on_agent_killed_or_wounded` trigger into the `village_raid` template (right after `common_battle_init_banner`). The trigger checks if the casualty is a human enemy and correctly adds/wounds them in the `p_total_enemy_casualties` party.

## 4. Fix Lord Banner Replacement Bug (Bug Fix 4.0) - SKIPPED
- **Target File**: `source/module/module_presentations.py`
- **Reason**: The base 1175 bug fix addressed lords spawning red/white checkered banners when their original banner was taken. However, Diplomacy utilizes a completely different architectural approach to banner selection (`$g_edit_banner_troop`), rendering the Native fix incompatible and unnecessary without custom logic.

## 5. Fix Menu Options Cut Off (Bug Fixes 5.0, 6.0, 7.0) - SKIPPED
- **Target Files**: Various menus, simple triggers, and scripts.
- **Reason**: These "fixes" from 1175 are actually complex new sub-menu features and major logic restructuring (e.g., adding sub-menus for minister appointments, tracking NPC departure order, and randomizing castle court spawning). Since Diplomacy often manages its own court logic, dialogues, and minister systems, porting these would require large rewrites rather than applying simple patches.

## 6. Fix Lord Recruitment Dialogues (Bug Fix 8.0)
- **Target File**: `source/module/module_dialogs.py` (`lord_recruit_pledge` dialogs)
- **Reason**: During the dialogue where a lord pledges allegiance to the player, the encounter would prematurely close, cutting off the dialog and potentially failing to store who was actually recruited.
- **Change Made**: 
  1. We now properly assign the recruited lord to `slot_lord_recruitment_candidate` immediately after they change factions.
  2. We moved `(assign, "$g_leave_encounter", 1)` from the `lord_recruit_pledge` state to the final `lord_recruit_pledge_conclude` state.
  3. We also added logic to clear `slot_lord_recruitment_candidate` once the pledge has gracefully concluded.

## 7. Fix Duplicate Voulge IDs (Bug Fix 9.0) - SKIPPED
- **Target File**: `source/module/module_items.py`
- **Reason**: The base 1175 bug fix addressed two different polearms sharing the exact same `itm_voulge` ID. This fix is already present in the active Diplomacy module (which renames the second one to `long_voulge`), so no action was needed.

## 8. Fix Rescued Lords Hostile in Prison Break (Bug Fix 10.0)
- **Target File**: `source/module/module_mission_templates.py` (`prison_break` templates)
- **Reason**: When performing a prison break, the rescued lord would sometimes attack the player or the guards indiscriminately. This was because they were being hardcoded to spawn on `team 0` instead of the player's current team.
- **Change Made**: Replaced the hardcoded `(agent_set_team, ":agent_no", 0)` with logic that dynamically fetches the player's team (`agent_get_team`) and assigns the rescued lord agent to it.

## 9. Optimize Battle Morale Logic (Bug Fix 11.0)
- **Target File**: `source/module/module_scripts.py` (`apply_effect_of_other_people_on_courage_scores` script)
- **Reason**: The base script executed an O(N^2) operation continuously for every human agent in massive battles. It iterated over all alive agents, compared distances to all other alive agents, and updated courage scores. This caused catastrophic lag.
- **Change Made**: 
  1. Modified the outer agent loop to immediately skip if the agent is **not** actively running away (`agent_slot_eq, ":centered_agent_no", slot_agent_is_running_away, 1`). This reduces the loop from "all agents" to only "fleeing agents".
  2. Flattened the complex, nested conditions calculating the positive and negative effect of distance into linear `try_begin...else_try` blocks saving directly into a `:pos_effect` and `:neg_effect` variable, drastically reducing script execution time.

## 10. Castle Banner Fix on Lord Exile (Bug Fix 12.0)
- **Target File**: `source/module/module_scripts.py` (`indict_lord_for_treason` script)
- **Reason**: When a lord was indicted for treason and their property returned to the faction leader, the banner on their previous castle or town was not being reset, leaving their old banner flying instead of changing to neutral/unassigned or updating when re-granted.
- **Change Made**: Added a `(party_set_banner_icon, ":center", 0)` immediately after setting the town's lord to unassigned during the `indict_lord_for_treason` script loop over centers.

## 11. Fix Wounded Kings and Pretenders in Enemy Casualties (Bug Fix 17.0)
- **Target File**: `source/module/module_game_menus.py` (`total_victory` menu)
- **Reason**: The script `party_get_num_companion_stacks` iterating over `p_collective_enemy` was using a bounds check of `is_between, ":stack_troop", lords_begin, lords_end`, which erroneously excluded faction leaders (kings) and pretenders, meaning if they were wounded in battle, they weren't added to `p_total_enemy_casualties` and thus were missing from the post-battle loot/prisoner calculation.
- **Change Made**: Changed the bounds check from `lords_begin, lords_end` to `active_npcs_begin, active_npcs_end` to ensure all heroes (including kings and pretenders) are properly processed as casualties.

## 12. Fix Error Hosting Feast Without Town (Bug Fix 18.0)
- **Target File**: `source/module/module_dialogs.py` (`spouse_feast_confirm_yes` dialog)
- **Reason**: When a player requested to host a feast but did not own any walled center (town or castle), the script iterated over walled centers trying to find a valid venue but left `:feast_venue` as `-1`. It then attempted to use `-1` in `(str_store_party_name_link, s9, ":feast_venue")` and `quest_set_slot`, causing script errors.
- **Change Made**: Added a check `(gt, ":feast_venue", -1)` before falling through to the next `(else_try)` block. If no venue is found, it will now default to assigning `"$g_encountered_party"`.

## 13. Fix Changing Minister Failing Quests (Bug Fix 20.0)
- **Target File**: `source/module/module_dialogs.py` (`minister_replace_confirm` dialog)
- **Reason**: When changing ministers, the script iterates through all quests and aborts any given by the previous minister. However, this caused an issue where unaccepted/inactive quests would "fail" improperly.
- **Change Made**: Added `(check_quest_active, ":minister_quest")` before calling `script_abort_quest`, ensuring only active quests are aborted.

## 14. Fix Rebel Ladies' Faction Update (Bug Fix 21.0)
- **Target File**: `source/module/module_game_menus.py` (`notification_pretender_denounced_ruler` menu)
- **Reason**: When a rebellion succeeded and the old faction was taken over by the pretender, rebel lords were correctly moved from the player supporters faction to the original faction. However, rebel ladies were not updated, leaving them stuck in `fac_player_supporters_faction`.
- **Change Made**: Added a loop over `kingdom_ladies_begin` to `kingdom_ladies_end` to check if their faction is `fac_player_supporters_faction`, and if so, change it back to the original faction (`$g_notification_menu_var1`), setting their title appropriately.

## 15. Fix Escort Lady Spouse Quest Dialog (Bug Fix 22.0)
- **Target File**: `source/module/module_dialogs.py` (`spouse_talk` dialog)
- **Reason**: When the player escorts their spouse in the `qst_escort_lady` quest and arrives at the destination, talking to the spouse would trigger the generic `Yes, my husband?` (or wife) dialog rather than the quest completion dialog, rendering the quest uncompletable.
- **Change Made**: Added a check at the start of the `spouse_talk` dialog conditions that prevents it from triggering if `qst_escort_lady` is active, the context is `tc_entering_center_quest_talk`, and the spouse is the object of the quest.
