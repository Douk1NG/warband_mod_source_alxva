# Fallen Ruler Recruitment

Recruit defeated kings, pretenders, and claimants who have lost their realm as player vassals.

## source/module_dialogs.py

### lord_talk recruitment path
- New player option when target is a king or pretender (`kings_begin`..`kings_end` / `pretenders_begin`..`pretenders_end`)
- Requirements: target faction is `fac_commoners`, original faction is `sfs_defeated` or re-established under a different leader, player is ruler of an active kingdom, target not a prisoner
- On acceptance: stores old faction, calls `script_change_troop_faction` into `$players_kingdom`, restores `slot_troop_occupation` to `slto_kingdom_hero`, sets `$g_leave_encounter` / `$g_recalculate_ais`
- No persuasion roll or random failure — guaranteed late-game option

### minister_talk recruitment path
- Option "I want to recruit a defeated ruler into our realm."
- Shows troop list of eligible fallen rulers/claimants
- Same eligibility rules, immediate recruitment into `$players_kingdom`

### Daily faction-defeat cleanup
- When an NPC kingdom is marked `sfs_defeated`, its leader and related claimant are moved to `fac_commoners`
- Existing-save fallback: accepts claimants still stuck in their original defeated faction
