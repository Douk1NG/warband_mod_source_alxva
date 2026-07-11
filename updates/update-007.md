# Update 007 - Late Game Defeated King Recruitment and Auto Prisoner Selection

## Purpose
This update documents two late-game and post-battle quality-of-life changes:

- Defeated rulers and claimants who have lost their realm and become commoners can now be recruited as player vassals through lord dialogue or the minister.
- Captured enemy prisoners are automatically selected before the prisoner exchange screen opens, prioritizing quest targets and then the highest-level prisoners up to the player's prisoner capacity.

Both changes are behavior-affecting.

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

## Verification
- `compile.bat` was run after the defeated king recruitment dialogue change.
- W.R.E.C.K. reported `COMPILATION SUCCESSFUL` after exporting with permission to write to the Warband module directory.

## Notes
- The defeated ruler dialogue intentionally uses direct faction change logic instead of the normal lord recruitment persuasion system, because this is meant to be a guaranteed late-game option.
- The prisoner auto-selection logic deliberately runs before the exchange screen rather than replacing it, so the player keeps final control.
