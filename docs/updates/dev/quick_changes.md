# Quick Changes

## Camp Menu Restructure

Camp menu reordered in commit 7c111c4:

**mnu_camp** (main camp):
- Cheat menu (cheat mode only)
- Settings (mnu_dplmc_preferences)
- Take an action (mnu_camp_action)
- Walk around the campsite
- Wait here for some time
- Resume travelling

**mnu_camp_action** (sub-menu):
- Disembark (when on ship)
- Manage your inventory (prsnt_equip_npcs)
- Configure autoloot for heroes
- Recruit prisoners
- Read book
- Customize armor
- Change food consumption habits
- Change party name
- Rename kingdom
- Change vassal titles
- Retire
- Back to camp menu

Removed from camp action: Sort inventory sub-menu, Modify banner cheat, Cheat: Change kingdom policies.

Cheat menu split into sub-menus: party, player/kingdom, player stats, world, advanced, debug.

## Reports Structure

**mnu_reports** (main):
- Cheat Reports (cheat mode only)
- Character/Party Reports
- Faction/Relations Reports
- Economic Reports
- All Items
- Resume travelling

**Character/Party Reports:**
- View character report
- View companion mission report
- View combined morale and size report

**Faction/Relations Reports:**
- View list of known lords by relation
- View courtship relations
- View affiliated family/spouse report
- View faction relations report
- View faction/lords relations report

## Troop Tree Creator Adjustments

- Removed automatic troop tree conversion that ran every time the customisation screen was opened (was converting player faction troops, garrisons, lord armies, guard troops, and village recruits). Game start no longer overrides existing troops.
- Equipment funds doubled — more gold for troop creation
- Save-load fix: rebuilds item arrays, recalculates funds and proficiency requirements on load
- Item filtering fix: removed broken skip logic that caused duplicate/missing items
- Cost calculation fix: modifier divisor used wrong variable, giving incorrect prices
- Proficiency max fix: switched to proper calculation script

## Removed
- Removed "View the world map" from reports menu (520f27f)
- Removed separate morale report and party size report menus; replaced with combined presentation (ae07740)
