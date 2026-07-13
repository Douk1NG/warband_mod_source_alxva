# Update 007 - Ported Changes from 1175 + New Features

## Features

- Defeated rulers and claimants who have lost their realm and become commoners __can be recruited as player vassals__ through lord dialogue or the minister.
- Captured enemy __prisoners are automatically selected__ before the prisoner exchange screen opens, prioritizing quest targets and then the highest-level prisoners up to the player's prisoner capacity; the __player prisoner capacity now gains a renown-based bonus__.
- When entering a player-owned castle or town, __prisoners traveling with the player are automatically moved__ into that center's dungeon.
- Constable prisoner selling now uses a __direct sell-all flow__ for the current dungeon, avoiding the old temporary garrison-prisoner trade screen.
- The constable can recruit eligible __dungeon prisoners__ directly __into the current garrison__.
- A lord suggestion __cheat option__ can force a lord to __accept recruitment into the player's kingdom__.
- While the player is hosting a feast, __resting in the feast center now automatically improves relation with attending lords__ once per day when the feast quality is at least adequate.
- Allied kingdom __lords who fought alongside the player__ now receive a small __post-battle relation increase__, with martial lords receiving a larger boost.
- Known lord personality/reputation type is now displayed on lord character pages after the player has met the lord, with cheat mode revealing it regardless of meeting state.
- Kingdom __lords defeated directly by the player can no longer escape__  from the player's captivity.
- Entering a __castle court__ now temporarily switches the player to __civilian body clothing__.
- __Autosell__ now __ignores capacity or money limits__ of the merchants and liquidates __all items__ marked as sellable(no option to rebuy).
- __Player and Companions__ can now __toggle between two weapon loadout sets__ from the camp menu, allowing quick loadout swaps (will be updated to swap on pre battle menu).
- __New inventory management screen__, accessible from the camp menu or by pressing __[M]__, letting the player __equip companions__ directly and sort the player's own inventory, include a button to __immediately equip all best equipment__ for each companion.
- __An all-items browser__, accessible from the report menu, allowing the player to __browse weapons, armors, and other item categories__, if __cheat mode__ is on, it also allows player to spawn items into their inventory, __can set quantity and quality for each item__.


## 1. Defeated Ruler Recruitment (Feature 1.0)
- **Target File**: `source/module/module_dialogs.py`
- **Change Made**: Added a late-game path to recruit fallen monarchs and pretenders into the player's kingdom as guaranteed vassals, supported by three pieces: (1) a new `lord_talk` player option after the rebellion dialogue block, shown when `$g_talk_troop` is a king or pretender (`kings_begin`..`kings_end` / `pretenders_begin`..`pretenders_end`), the target's faction is `fac_commoners`, its `slot_troop_original_faction` is an NPC kingdom, that original kingdom is `sfs_defeated` or re-established under a different leader, the player's kingdom is active and the player is its ruler, and the target is not a prisoner; on acceptance it stores the old faction, calls `script_change_troop_faction` into `$players_kingdom`, restores `slot_troop_occupation` to `slto_kingdom_hero`, queues `mnu_notification_troop_joined_players_faction`, and sets `$g_leave_encounter` / `$g_recalculate_ais` with no persuasion roll or random failure; (2) a `minister_talk` option 'I want to recruit a defeated ruler into our realm.' that appears when at least one eligible fallen ruler or claimant exists, lets the player pick from a troop list, and uses the same eligibility rules, immediately recruiting into `$players_kingdom` and recalculating AI; (3) a daily faction-defeat cleanup update so that when an NPC kingdom is marked `sfs_defeated`, its leader (king/pretender) and related claimant are moved to `fac_commoners` (unless the claimant is the currently supported pretender), plus an existing-save fallback that still accepts a claimant stuck in their original defeated faction.
- **Reason**: Once a kingdom is defeated, its former king or claimant can become hard to find or interact with. This adds a late-game recovery path where the player can absorb a fallen monarch or pretender into their realm as a vassal, but only after the original kingdom is truly defeated or no longer led by that character. The minister route covers the case where the target has gone into hiding as a commoner and would be impractical to track down in the field, while the cleanup ensures both the ruler and claimant are relocated to `fac_commoners` so the recruitment paths can detect and offer them — and fixes older saves where a claimant was still stuck in their original (now defeated) faction and invisible to both routes.

## 2. Cheat Lord Recruitment Dialog (Feature 2.0)
- **Target File**: `source/module/module_dialogs.py`
- **Change Made**: Added a cheat recruitment option under the lord suggestion cheat menu, shown when the player is the leader of `$players_kingdom`. Selecting it makes the talked-to lord consider `trp_player` as the recruitment candidate, uses the claim argument, clears the fief expectation flag, and forces `$pledge_chance` to `100`. The dialog reuses the normal final pledge flow, so the lord accepts through the existing faction-change and pledge consequences.

## 3. Constable Prisoner Sale and Storage Flow (Feature 3.0)
- **Target File**: `source/module/module_dialogs.py`
- **Change Made**: Replaced the old garrison-prisoner management route from the constable menu with an always-visible direct sell-all option for the current dungeon; if the dungeon has no sellable prisoners the constable reports none. The new sell-all route avoids moving dungeon prisoners through `p_main_party` and avoids opening the prisoner trade screen. Added a direct option to recruit eligible prisoners from the current dungeon into the current garrison, using a confirmation prompt and reporting when none are eligible; after success a log message reports how many were added.

## 4. Automatic Captured Prisoner Selection (Feature 4.0)
- **Target File**: `source/module/module_game_menus.py`
- **Change Made**: Added an automatic prisoner selection block in the `total_victory` flow immediately before `troop_set_slot, trp_temp_array_d, slot_adv_transfer_mode, 10` and `change_screen_exchange_with_party, p_temp_party`. It moves newly captured prisoners into `p_temp_party`, clears existing prisoners from `p_main_party`, checks the player's free prisoner capacity, prioritizes quest-relevant prisoners (`qst_follow_spy`: `trp_spy` and `trp_spy_partner`; `qst_capture_prisoners`: the quest target troop up to requested amount), then fills remaining capacity with the highest-level available prisoners from `p_temp_party`. The normal exchange screen still opens afterward.
- **Reason**: The post-battle prisoner exchange can be tedious, especially when the player needs specific quest targets or wants the most valuable prisoners. This change preserves the manual exchange screen while pre-selecting the most useful prisoners first.

## 5. Automatic Prisoner Dungeon Deposit (Feature 5.0)
- **Target File**: `source/module/module_game_menus.py`
- **Change Made**: Added a `mnu_town` entry hook for player-owned walled centers. When the player enters a castle or town where `slot_town_lord` is `trp_player`, any prisoners in `p_main_party` are moved into `$current_town` using `$g_move_heroes = 1` (so captured lords and hero prisoners move with regular prisoners), and the player receives a message reporting how many were moved.

## 6. Allied Lord Relation Reward Hooks (Feature 6.0)
- **Target File**: `source/module/module_game_menus.py`; `source/module/native/scripts/encounters/encounters_scripts.py`
- **Change Made**: Added the Native1175 allied-lord relation script call (`script_change_player_relation_with_lords_after_battle`, defined in #12) across the player victory and siege paths so allied lords who fought alongside the player are rewarded consistently: (1) in `module_game_menus.py` — the major allied field battle branch where the player participated but provided less than 40 percent of allied strength, the `mnu_castle_taken` path when the player captures a center, and the siege success path after the center is assigned and the player participation log is recorded; (2) in `encounters_scripts.py` — immediately after the existing player-participated-in-siege log entry in the scripted siege capture, covering the siege mission itself, which the menu hooks do not reach.
- **Reason**: The Native1175 allied-lord relation reward only fired in one victory branch, so allied lords who fought alongside the player were inconsistently rewarded — especially when the player captured a center or won a siege rather than a straight field battle. These hooks call the same relation script from the major allied battle, castle-taken, siege-success, and scripted-siege paths so the reward triggers consistently across every way the player can win, layered on top of Diplomacy's existing ally-leader thank-you.

## 7. Toggle Weapons Camp Menu (Feature 7.0)
- **Target File**: `source/module/module_game_menus.py`
- **Change Made**: Added a camp menu option that lets the player toggle companion weapon loadout sets. It reads the current `$g_weapons_set_no` value, cycles between available sets, and calls `script_all_toggle_weapons_set` to apply the selected loadout to all companions in the party.

## 8. Manage Inventory (Player & Companion) (Feature 8.0)
- **Target File**: `source/module/module_game_menus.py`; `source/module/module_troops.py`
- **Change Made**: Added a camp menu option that opens the `prsnt_manage_inventory` presentation. The presentation displays the player's equipped items on the left and inventory on the right, with a companion list sidebar for switching between party members, and supports item dragging, sort, lock toggles, and auto-upgrade-all. `module_troops.py` adds four temporary troop entries used as data arrays by this presentation (and the all-items browser): `trp_temp_array_x` (overlay X positions), `trp_temp_array_y` (overlay Y positions), `trp_temp_array_lock` (per-slot lock state), and `trp_temp_array_sort` (companion hero list by troop ID).

## 9. All Items Browser Camp Menu (Feature 9.0)
- **Target File**: `source/module/module_game_menus.py`; `source/module/module_strings.py`
- **Change Made**: Added a camp menu option that opens the `prsnt_all_items` presentation, displaying items in three browsable categories (Weapons, Armors, Others) with names, stats, and a mesh-viewer preview. `module_strings.py` adds the supporting string entries: imod quality descriptions (e.g. Fine, Masterwork, Cracked, Rusty) and troop attribute / proficiency category names, used by the item extra text display; When cheats are enabled, the item browser will also display three buttons to give items to the player, quality, quantity and get button.

## 10. Manage Inventory Hotkey (Feature 10.0)
- **Target File**: `source/module/module_simple_triggers.py`
- **Change Made**: Added a simple trigger on `map_free` that opens the companion inventory management presentation when the player presses the assigned hotkey (`key_m` by default), firing only when the player is on the world map and not in a conversation or menu.

## 11. Automatic Feast Relation Gain (Feature 11.0)
- **Target File**: `source/module/module_triggers.py`
- **Change Made**: Ported the Native1175 `auto change relations during feast` trigger. It checks once per hour while the player is resting/interacting inside the active player feast center, requiring `$players_kingdom` to be using `sfai_feast`, the faction feast target to be the currently encountered party, `qst_organize_feast` active and targeting that same center, and the player not map-free. Before applying changes it rates the feast with `script_internal_politics_rate_feast_to_s9`; if quality is at least `20`, every hero attached to the feast center can gain `+1` relation toward the player once every 24 hours, throttled by `slot_troop_last_talk_time`.
- **Reason**: Native feast dialogue already gives direct relation bumps when speaking to guests, but long rests during a player-hosted feast can pass time without naturally rewarding the player for keeping guests gathered and supplied. This adds the 1175 automatic relation drip while keeping the original feast quality gate and once-per-day limit.

## 12. Allied Lord Post-Battle Relation Script (Feature 12.0)
- **Target File**: `source/module/module_scripts.py`
- **Change Made**: Ported the Native1175 `script_change_player_relation_with_lords_after_battle` helper. It scans `p_collective_friends` for active NPC kingdom heroes present in the player-side battle group, granting `+1` relation by default, `+2` if their personality is `lrep_martial`, and `0` if their current player relation is below `-5`.

## 13. Renown-Based Prisoner Capacity (Feature 13.0)
- **Target File**: `source/module/native/scripts/core/core_scripts.py`
- **Change Made**: Updated `script_game_get_party_prisoner_limit` (the engine callback for a party's prisoner limit). For `p_main_party` the returned limit now adds `slot_troop_renown / 20`, on top of the existing base `skl_prisoner_management * 5` and after the existing Diplomacy `$diplomacy_var2` override. Non-player parties keep their existing behavior.

## 14. Lord Personality Note Data (Feature 14.0)
- **Target File**: `source/module/native/scripts/core/core_scripts.py`
- **Change Made**: Ported the Native1175 lord personality note setup into `script_game_get_troop_note`. The note code initializes `s61` to `unknown`, then for active NPC lords replaces it with the matching `str_personality_archetypes` entry when cheat mode is enabled or the player has met the lord.

## 15. Lord Personality Display (Feature 15.0)
- **Target File**: `source/module/module_strings.py`
- **Change Made**: Updated `str_lord_info_string` to include `Personality: {s61}.`, preserving the existing Diplomacy additions on the same line (marshal status and wealth display).

## 16. Player-Defeated Lord Capture (No Escape) (Feature 16.0)
- **Target File**: `source/module/native/scripts/encounters/encounters_scripts.py`; `source/module/native/scripts/npcs/npcs_scripts.py`
- **Change Made**: Made lords defeated directly by the player go to capture instead of rolling the normal escape chance, implemented at two layers: (1) in `encounters_scripts.py`, the immediate hero-defeat capture branch now sends the defeated hero to the capture branch (instead of rolling against `hero_escape_after_defeat_chance`) when `p_main_party` is the winning party, while non-player winners still use the existing constant; (2) in `npcs_scripts.py`, `script_cf_check_hero_can_escape_from_player` now makes regular active kingdom heroes defeated by the player fail the escape check and proceed to the capture/dialog path. The existing quest-target rules are preserved: peace-quest targets remain non-escaping capture targets, and bandit leaders keep their special quest/run behavior. This does not change the later prisoner escape system for heroes already held in parties or centers.

## 17. Automatic Civilian Clothes in Castle Courts (Feature 17.0)
- **Target File**: `source/module/native/scripts/misc/misc_scripts.py`
- **Change Made**: Ported the Native1175 civilian-clothes behavior into the local modular `script_enter_court` flow. When entering `mt_visit_town_castle`, player entry `0` now uses `af_override_all` and receives a temporary civilian body item, chosen in order: the player's currently equipped civilian body armor, the first civilian body armor found in the player's inventory, then `itm_tabard` as fallback. This is mission-entry override equipment only and does not change the player's real inventory or equipped armor.

## 18. Direct Liquidation for Autosell & Autotrade (Feature 18.0)
- **Target File**: `source/module/native/scripts/diplomacy/diplomacy_scripts.py`; `source/module/native/scripts/misc/misc_scripts_extra.py`
- **Change Made**: In `script_dplmc_auto_sell` (diplomacy) and `script_auto_trade_sell_to_merchant` (misc_scripts_extra, Custom Commander autotrade), items are now liquidated directly from the player inventory instead of being transferred into a merchant inventory, and the merchant-gold and merchant-free-space requirements were removed from both the dry-run quote calculation and actual sale execution. The center autosell path uses a cleanup mode that skips backup-equipment protection and starts from the first inventory slot after equipped items and the food slot (instead of skipping Diplomacy's four alternate-item reserve slots); the existing price limit, item range, rotten-food exception, book/trade-good exclusions, and lordly-item protection are unchanged. Merchant-dialog autosell still uses the conservative personal-equipment safety checks, and autotrade buying remains merchant-based.

## 19. Party-Specific Sell-All Prisoner Script (Feature 19.0)
- **Target File**: `source/module/native/scripts/diplomacy/diplomacy_scripts.py`
- **Change Made**: Added `script_dplmc_sell_all_prisoners_from_party`, mirroring the existing ransom-broker sell-all calculation but taking a source party as its first parameter and only selling prisoners accepted by `script_game_check_prisoner_can_be_sold` (so hero prisoners remain). The original `script_dplmc_sell_all_prisoners` now wraps the new script with `p_main_party`, preserving ransom-broker and Ramun behavior, and the constable uses the new party-specific script for current-dungeon prisoners.

## 20. Recruit Dungeon Prisoners to Garrison (Feature 20.0)
- **Target File**: `source/module/native/scripts/diplomacy/diplomacy_scripts.py`
- **Change Made**: Added `script_dplmc_recruit_all_prisoners_to_garrison`, which scans a center's prisoner stacks and converts eligible regular prisoners into normal garrison members of the same troop type. Eligibility follows `script_game_check_prisoner_can_be_sold`, so lord prisoners remain in the dungeon. The script supports dry-run mode for dialog confirmation and execute mode for the actual conversion, and the constable uses it for the current dungeon.

---

## Notes
- The defeated ruler dialogue intentionally uses direct faction change logic instead of the normal lord recruitment persuasion system, because this is meant to be a guaranteed late-game option.
- The prisoner auto-selection logic deliberately runs before the exchange screen rather than replacing it, so the player keeps final control.
- The renown prisoner-capacity bonus is added in the engine prisoner-limit callback, so it affects the player's actual prisoner capacity rather than only the auto-selection pass.
- The automatic dungeon deposit only runs for centers directly owned by `trp_player`; allied or vassal-owned centers are not auto-filled.
- The constable dungeon sell-all flow intentionally sells only regular sellable prisoners and leaves lord prisoners in the dungeon.
- The constable dungeon recruit flow also leaves lord prisoners in the dungeon and only converts eligible regular prisoners into garrison troops.
- The cheat lord recruitment dialog deliberately reuses the existing final recruitment decision path rather than duplicating the pledge consequences.
- The feast relation trigger is intentionally copied into `module_triggers.py` instead of `module_simple_triggers.py`, matching the 1175 source location and using existing local feast helper scripts.
- The post-battle relation feature is not a replacement for Diplomacy's ally-leader thank-you reward. It layers the Native1175 all-allied-lords reward on top of the existing primary ally reward.
- The root module already contained personality archetype strings and a cheat-mode conversation debug display. This task adds the player-facing character-page display.
- The defeated-lord escape change is player-specific by design. It does not globally set lord escape chance to zero, so AI battles and ongoing prisoner escape behavior keep their existing balance.
- The civilian-clothes feature is intentionally limited to indoor court entry. The local town-center, tavern, merchant, courtyard, and disguise routes already had Diplomacy/Dickplomacy override handling and were left alone.
- Autosell and autotrade sale prices still use the existing price-factor scripts; this change only removes merchant wallet and stock capacity as blockers for automatic selling.
- Equipped items and the active food slot remain protected because cleanup mode still starts after those slots; the center cleanup mode only affects eligible items in the inventory.
