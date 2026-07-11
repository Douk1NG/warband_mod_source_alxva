# Update 007 - Late Game Defeated King Recruitment and Auto Prisoner Selection

## Purpose
This update documents branch 007 gameplay and quality-of-life changes:

- Defeated rulers and claimants who have lost their realm and become commoners can now be recruited as player vassals through lord dialogue or the minister.
- Captured enemy prisoners are automatically selected before the prisoner exchange screen opens, prioritizing quest targets and then the highest-level prisoners up to the player's prisoner capacity.
- A lord suggestion cheat option can force a lord to accept recruitment into the player's kingdom.
- While the player is hosting a feast, resting in the feast center now automatically improves relation with attending lords once per day when the feast quality is at least adequate.
- Allied kingdom lords who fought alongside the player now receive a small post-battle relation increase, with martial lords receiving a larger boost.
- Known lord personality/reputation type is now displayed on lord character pages after the player has met the lord, with cheat mode revealing it regardless of meeting state.
- Kingdom lords defeated directly by the player no longer roll the normal post-defeat escape chance before capture.
- Entering a castle court now temporarily switches the player to civilian body clothing.
- Autosell and autotrade sales no longer fail when the merchant runs out of money or inventory space.

These changes are behavior-affecting.

## File Changes

### `source/module/module_dialogs.py`

#### Defeated Ruler Recruitment Dialogue
- Added a new `lord_talk` player option immediately after the rebellion dialogue block.
- The option appears only when all of the following are true:
  - `$g_talk_troop` is in the `kings_begin` to `kings_end` range or the `pretenders_begin` to `pretenders_end` range.
  - The ruler or claimant's current faction is `fac_commoners`.
  - The ruler or claimant's `slot_troop_original_faction` is an NPC kingdom.
  - The original kingdom is either marked `sfs_defeated`, or it has been re-established under a different leader, such as a victorious pretender.
  - The player's kingdom is active.
  - The player is the ruler of the active player kingdom.
  - The king is not currently a prisoner.
- The recruitment is guaranteed. There is no persuasion roll, bribe, relation check, or random failure path.
- On acceptance:
  - The old faction is stored for the normal joined-faction notification.
  - `script_change_troop_faction` moves the king into `$players_kingdom`.
  - `slot_troop_occupation` is restored to `slto_kingdom_hero`.
  - `mnu_notification_troop_joined_players_faction` is queued.
  - `$g_leave_encounter` and `$g_recalculate_ais` are set.

#### Reason
Once a kingdom is defeated, its former king or claimant can become hard to find or interact with. This adds a late-game recovery path where the player can absorb a fallen monarch or pretender into their realm as a vassal, but only after the original kingdom is truly defeated or no longer led by that character.

#### Minister Recruitment Route
- Added a separate `minister_talk` option: "I want to recruit a defeated ruler into our realm."
- The minister option appears only if at least one eligible fallen ruler or claimant exists.
- The player can select an eligible ruler or claimant from a troop list.
- This minister route uses the same eligibility rules as direct lord conversation:
  - The target must be a king or pretender.
  - The target must currently belong to `fac_commoners`, or be stuck in their defeated original faction for save compatibility.
  - The target's original faction must be an NPC kingdom.
  - The original faction must be defeated or led by someone else.
  - The target must not be a prisoner.
- Confirming the minister action immediately recruits the king into `$players_kingdom`, restores `slto_kingdom_hero`, queues the joined-faction notification, and recalculates AI.

#### Fallen Ruler Debug Report
- Added and then disabled a diagnostic Reports-menu helper after it served its purpose during testing.
- The report code remains commented in `module_game_menus.py` for future troubleshooting.
- When uncommented, it lists every king and pretender whose `slot_troop_original_faction` is an NPC kingdom, even if they are not currently recruitable.
- Each character line reports:
  - Current faction.
  - Original faction.
  - Original faction state.
  - Current ruler of the original faction.
  - Occupation slot.
  - Recorded current center or prison party.
  - Whether the fallen-ruler recruitment rule currently evaluates as true.
- This is intended to help diagnose why a claimant does not appear in the recruitment list, especially whether they are captured, not on `fac_commoners`, still tied to an active original faction, or blocked by occupation/state data.

#### Pretender Victory Note
When a pretender wins a rebellion, the original kingdom is reactivated under the pretender instead of remaining `sfs_defeated`. The former king is moved to `fac_commoners`, but the faction itself becomes active again. For that reason, the defeated-ruler eligibility check also accepts cases where the original faction's current leader is not the former king. If that pretender-led kingdom later falls, the pretender can also become eligible. If a pretender never became ruler and their original faction is defeated, they can also be recruited as a vassal once they are on `fac_commoners`.

#### Defeated Claimant Cleanup
- Updated the daily faction defeat cleanup so that when an NPC kingdom is marked `sfs_defeated`, its current leader is moved to `fac_commoners` if that leader is a king or pretender.
- The related claimant for the defeated kingdom is also moved to `fac_commoners` when the kingdom falls and that claimant is not the currently supported pretender.
- The recruitment eligibility also accepts an existing-save fallback where a claimant is still in their original faction while that original faction is already `sfs_defeated`. This handles saves created before the cleanup fix, where the daily defeat trigger will not run again for that faction.

#### Cheat Lord Recruitment Dialog
- Added a cheat recruitment option under the lord suggestion cheat menu.
- The option appears when the player is the leader of `$players_kingdom`.
- Selecting it makes the talked-to lord consider `trp_player` as the recruitment candidate, uses the claim argument, clears the fief expectation flag, and forces `$pledge_chance` to `100`.
- The dialog reuses the normal final pledge flow, so the lord accepts through the existing faction-change and pledge consequences.

### `source/module/module_game_menus.py`

#### Automatic Captured Prisoner Selection
- Added an automatic prisoner selection block in the `total_victory` flow immediately before:
  - `(troop_set_slot, "trp_temp_array_d", slot_adv_transfer_mode, 10)`
  - `(change_screen_exchange_with_party, "p_temp_party")`
- The feature is always on when captured enemies exist.
- Before opening the prisoner exchange screen, the script:
  1. Moves newly captured prisoners into `p_temp_party`.
  2. Clears existing prisoners from `p_main_party`.
  3. Checks the player's free prisoner capacity.
  4. Prioritizes quest-relevant prisoners:
     - If `qst_follow_spy` is active, it takes `trp_spy` and `trp_spy_partner` first when available.
     - If `qst_capture_prisoners` is active, it takes the quest target troop up to the requested amount and remaining capacity.
  5. Fills any remaining capacity with the highest-level available prisoners from `p_temp_party`.
- After the automatic pass, the normal prisoner exchange screen still opens, allowing the player to review and adjust the result.

#### Reason
The post-battle prisoner exchange can be tedious, especially when the player needs specific quest targets or wants the most valuable prisoners. This change preserves the manual exchange screen while pre-selecting the most useful prisoners first.

### `source/module/module_triggers.py`

#### Automatic Feast Relation Gain
- Ported the Native1175 `auto change relations during feast` trigger.
- The trigger checks once per hour while the player is resting/interacting inside the active player feast center.
- It only runs when:
  - `$players_kingdom` is currently using `sfai_feast`.
  - The faction feast target is the currently encountered party.
  - `qst_organize_feast` is active and targets that same center.
  - The player is not map-free.
- Before applying relation changes, it rates the feast with `script_internal_politics_rate_feast_to_s9`.
- If the feast quality is at least `20`, every hero attached to the feast center is considered.
- Each attending hero can gain `+1` relation toward the player once every 24 hours, using `slot_troop_last_talk_time` as the throttle.

#### Reason
Native feast dialogue already gives direct relation bumps when speaking to guests, but long rests during a player-hosted feast can pass time without naturally rewarding the player for keeping guests gathered and supplied. This adds the 1175 automatic relation drip while keeping the original feast quality gate and once-per-day limit.

### `source/module/module_scripts.py`

#### Allied Lord Post-Battle Relation Script
- Ported the Native1175 `script_change_player_relation_with_lords_after_battle` helper.
- The script scans `p_collective_friends` for active NPC kingdom heroes who were present in the player-side battle group.
- Eligible allied lords gain:
  - `+1` relation by default.
  - `+2` relation if their lord personality is `lrep_martial`.
  - `0` relation if their current player relation is below `-5`.

#### Diplomacy Overlap
Diplomacy already rewards the primary ally leader after victory through the existing `tc_ally_thanks` flow in `mnu_total_victory`. That existing reward is based on battle odds and can also improve the ally faction relation. The 1175 script is intentionally broader and smaller: it rewards every allied kingdom lord present in `p_collective_friends`. In qualifying battles, the main ally leader can therefore receive both the existing Diplomacy ally-leader reward and this new general allied-lord reward, matching the 1175 flow.

### `source/module/native/scripts/core/core_scripts.py`

#### Lord Personality Note Data
- Ported the Native1175 lord personality note setup into the modular `script_game_get_troop_note` flow.
- The note code now initializes `s61` to `unknown`.
- For active NPC lords, `s61` is replaced with the matching `str_personality_archetypes` entry when either:
  - cheat mode is enabled, or
  - the player has met the lord.

### `source/module/module_strings.py`

#### Lord Personality Display
- Updated `str_lord_info_string` to include `Personality: {s61}.`
- Preserved existing Diplomacy additions in the same line, including marshal status and wealth display.

### `source/module/native/scripts/encounters/encounters_scripts.py`

#### Scripted Siege Capture Hook
- Added the 1175 relation script call after the existing player-participated-in-siege log entry when the player was involved in a scripted center capture.

#### Player Defeat Capture Override
- Updated the immediate hero-defeat capture branch so that when `p_main_party` is the winning party, the defeated hero goes through the capture branch instead of rolling against `hero_escape_after_defeat_chance`.
- Non-player winner parties still use the existing `hero_escape_after_defeat_chance` constant.

### `source/module/native/scripts/npcs/npcs_scripts.py`

#### Player-Defeated Lord Escape Check
- Updated `script_cf_check_hero_can_escape_from_player` so regular active kingdom heroes defeated by the player fail the escape check and proceed to the capture/dialog path.
- Preserved the existing quest-target rules:
  - peace-quest targets remain non-escaping capture targets.
  - bandit leaders still use their special quest/run behavior.
- This does not change the later prisoner escape system for heroes already held in parties or centers.

### `source/module/native/scripts/misc/misc_scripts.py`

#### Automatic Civilian Clothes In Castle Courts
- Ported the Native1175 `civilian cloth` behavior into the local modular `script_enter_court` flow.
- When entering `mt_visit_town_castle`, player entry `0` now uses `af_override_all` and receives a temporary civilian body item.
- The selection order is:
  - the player's currently equipped body armor if it is already civilian,
  - the first civilian body armor found in the player's inventory,
  - `itm_tabard` as the fallback common clothing.
- This is mission-entry override equipment only; it does not permanently change the player's real inventory or equipped armor.
- The existing Diplomacy court setup, guard culture selection, spouse/minister/chamberlain visitors, and lord/lady visitor flow are unchanged.

### `source/module/native/scripts/diplomacy/diplomacy_scripts.py`

#### Autosell Direct Liquidation
- Updated `script_dplmc_auto_sell` so autosold items are liquidated directly from the player inventory instead of being transferred into a merchant inventory.
- Removed merchant-gold and merchant-free-space requirements from both dry-run quote calculation and actual sale execution.
- The center autosell path now uses a cleanup mode that skips backup-equipment protection, so inventory items like spare armor, boots, bows, melee weapons, throwing stones, and horses can be sold when they meet the autosell price and range rules.
- Cleanup mode starts from the first inventory slot after equipped items and the food slot, instead of skipping Diplomacy's four alternate-item reserve slots. This prevents items placed near the top of the inventory from being silently protected.
- The existing price limit, item range, rotten-food exception, book/trade-good exclusions, and lordly-item protection are unchanged.
- Merchant-dialog autosell still uses the conservative personal-equipment safety checks.

### `source/module/native/scripts/misc/misc_scripts_extra.py`

#### Autotrade Sell Direct Liquidation
- Updated `script_auto_trade_sell_to_merchant` with the same direct-sale behavior for Custom Commander autotrade selling.
- Removed merchant-gold and merchant-free-space requirements that could block otherwise valid trade-good sales.
- Autotrade selling still respects enabled/disabled item settings, minimum quantities, full-stack checks, and configured sell-over prices.
- Autotrade buying remains merchant-based and still depends on player funds, inventory space, item settings, and configured buy-under prices.

### `source/module/module_game_menus.py`

#### Victory Menu Hooks
- Added the 1175 relation script call in the major allied field battle branch where the player participated but provided less than 40 percent of allied strength.
- Added the call when the player captures a center through the `mnu_castle_taken` path.
- Added the call in the siege success path after the center is assigned and the player participation log is recorded.

## Verification
- `compile.bat` was run after the defeated king recruitment dialogue change.
- W.R.E.C.K. reported `COMPILATION SUCCESSFUL` after exporting with permission to write to the Warband module directory.
- The feast relation trigger was syntax-checked with Python AST parsing only. `compile.bat` was not run for this task, per branch instruction.
- The allied lord post-battle relation script and call sites were syntax-checked with Python AST parsing only. `compile.bat` was not run for this task, per branch instruction.
- The lord personality display changes were syntax-checked with Python AST parsing only. `compile.bat` was not run for this task, per branch instruction.
- The player-defeated lord escape changes were syntax-checked with Python AST parsing only. `compile.bat` was not run for this task, per branch instruction.
- The automatic civilian-clothes court-entry change was syntax-checked with Python AST parsing only. `compile.bat` was not run for this task, per branch instruction.
- The autosell/autotrade sale changes were statically reviewed only. `compile.bat` was not run for this task, per branch instruction.

## Notes
- The defeated ruler dialogue intentionally uses direct faction change logic instead of the normal lord recruitment persuasion system, because this is meant to be a guaranteed late-game option.
- The prisoner auto-selection logic deliberately runs before the exchange screen rather than replacing it, so the player keeps final control.
- The cheat lord recruitment dialog deliberately reuses the existing final recruitment decision path rather than duplicating the pledge consequences.
- The feast relation trigger is intentionally copied into `module_triggers.py` instead of `module_simple_triggers.py`, matching the 1175 source location and using existing local feast helper scripts.
- The post-battle relation feature is not a replacement for Diplomacy's ally-leader thank-you reward. It layers the Native1175 all-allied-lords reward on top of the existing primary ally reward.
- The root module already contained personality archetype strings and a cheat-mode conversation debug display. This task adds the player-facing character-page display.
- The defeated-lord escape change is player-specific by design. It does not globally set lord escape chance to zero, so AI battles and ongoing prisoner escape behavior keep their existing balance.
- The civilian-clothes feature is intentionally limited to indoor court entry. The local town-center, tavern, merchant, courtyard, and disguise routes already had Diplomacy/Dickplomacy override handling and were left alone.
- Autosell and autotrade sale prices still use the existing price-factor scripts; this change only removes merchant wallet and stock capacity as blockers for automatic selling.
- Equipped items and the active food slot remain protected because cleanup mode still starts after those slots; the center cleanup mode only affects eligible items in the inventory.
