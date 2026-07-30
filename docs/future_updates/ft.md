# Havenost's Proposed Changes — Detailed Breakdown & Integration Status

**Date:** 2026-07-28
**Source:** Forum post by Havenost (21 Apr 2026)
**Purpose:** Track each proposed change and what's already in the repo

---
(1175 mod)
**Buy Captured Lords**: Buy enemy lords held captive by your allies.
**Force peace/war**: `###(((force_peace`, `###(((force_war`
**Revoke fiefs**: Talk to minister to take away a lord's fief. `###(((minister_revoke_fief`
**Toggle DEBUG**: Turn debug messages on/off. `###(((debug_message_off`

## DIALOGUE CHANGES (`module_dialogs.py`)

### 1. Custom Armor Customization for All Troops (not just companions)

**Havenost says:** Gave everyone the dialogue option to customize their "Custom Armor" / Queens Blade armors via talk in the party screen / camp, so it's no longer limited to companions.

**Current status:** ✅ ALREADY IMPLEMENTED — The dialogue at `source/module_dialogs.py:3226-3239` has NO companion-only restriction. The only gating factor is whether the troop has a qualifying custom armor item equipped (checked by `script_find_customizable_item_equipped_on_troop`). Both companions and regular troops in the party show this option.

**Files:**
- `source/module_dialogs.py:3226-3239`
- `source/scripts/find_customizable_item_equipped_on_troop.py:17-63`

**Notes:** This check works in party screen talk (`member_talk`). For *camp* talk access, the camp dialogue has separate states (`camp_soldier_talk` for generic troops, `camp_lover_talk` for spouse) that don't include this option (see item 3 below).

---

### 2. Sparring with Spouse in Camp

**Havenost says:** Made it possible to spar with spouses in camp like all other companions/troops. Changed flavor text. Added option to ask someone to be on your team while sparring.

**Current status:** ❌ NOT IMPLEMENTED — The `camp_soldier_talk` state has a "Let's do some sparring" option (line 498-503) but it only applies to non-hero soldiers. The `camp_lover_talk` state (line 465-494) for spouses only offers sex and "Nothing now" — no sparring, no equipment inspection, no skill viewing.

**Files:**
- `source/module_dialogs.py:498-503` — existing sparring (soldiers only)
- `source/module_dialogs.py:465-494` — spouse camp talk (sex only)

**To implement:**
- Add sparring option to `camp_lover_talk`
- Add team choice mechanic
- Update flavor text

---

### 3. Party Screen "Talk" Dialogue Options in Camp

**Havenost says:** Made it possible to choose dialogue that was limited to the party screen "Talk" in camp. Specifically: change companion/spouse stats+equipment in camp, and view generic soldier stats/equipment in camp.

**Current status:** ❌ PARTIALLY IMPLEMENTED — In camp, the `camp_soldier_talk` offers:
- Sex ✓
- Sparring ✓
- "Tell me about yourself" → `change_screen_view_character` ✓ (line 709)
- "Nothing" ✓

**Missing from camp talk (compared to party screen `member_talk`):**
- ❌ Equipment inspection (`change_screen_equip_other`) — missing for all troops in camp
- ❌ Custom armor customization — missing in camp
- ❌ "I'd like to ask you something" (morale, background) — missing in camp
- ❌ Spouse-specific options (minister, feast, join/leave retinue) — missing from `camp_lover_talk`

**Files:**
- `source/module_dialogs.py:3220-3242` — party talk options
- `source/module_dialogs.py:465-713` — camp talk states

**To implement:**
- Add equipment inspection option to `camp_soldier_talk`
- Add skill/stat viewing to `camp_soldier_talk` (partially done via `view_char`)
- Add all of the above to `camp_lover_talk` for spouse
- Add custom armor customization to camp talk

---

### 4. Recruit Pretenders/Claimants to Party

**Havenost says:** Added option to recruit Pretenders/Claimants to your party if you already have a kingdom, so they can be your companions. Hid some recruitment/join cause dialogue options if you already have a kingdom (they always reject). Notes that even in party, game still treats them as independent (win tournaments, show up in courts).

**Current status:** ⚠️ THAT'S NATIVE BEHAVIOR, NOT OURS — The pretender dialogue tree at `module_dialogs.py:17229-17420` is vanilla Warband. **Our system** converts pretenders into vassals through the **minister dialog** under certain conditions, which still needs debugging for edge cases. Not the same as what Havenost describes.

**Where it happens (our mod):**
- Minister dialog → convert pretender → vassal
- Conditions exist but have edge-case bugs that need debugging

**Files:**
- `source/module_dialogs.py:17229-17420` — native pretender dialogue (not ours)
- Minister dialog files — where our vassal conversion lives

**Ongoing issues (match Havenost's observation):**
- Engine still treats them as independent lords (tournament wins, court appearances) even when converted — likely requires slot manipulation
- Edge cases in the conversion conditions need debugging

---

### 5. Sex with Pretenders/Claimants

**Havenost says:** Added option to have sex with Pretenders/Claimants as if they were any lord that you meet.

**Current status:** ⚠️ PARTIALLY POSSIBLE — You CAN have sex with pretenders when:
- They join your party (some dialogue path exists)
- You open a dialog with them after conquering the kingdom (when they're rulers)

**But needs investigation:** The exact scenarios and conditions aren't clear — may be different paths than expected. The TODO comments at `module_dialogs.py:13850,13884` suggest the pretender-as-spouse case specifically needs work.

**Files:**
- `source/module_dialogs.py:13850,13884`

---

### 6. Spouse Sex Dialogue Condition Changes

**Havenost says:** Changed condition for sex with spouse from requiring (spouse occupation = `slto_kingdom_lady` + is spouse + ≥1 relation) to just checking if they are your spouse. This allows sex with spouse even if they're a starting lord, a converted companion, or a savegame-edited spouse with <1 relation.

**Current status:** ⚠️ PARTIALLY — The sex dialogue in `camp_lover_talk` is gated by spouse identity checks (line 465-477), not by occupation or relation. However, the "change clothing" dialogue in `spouse_talk` (line 11511-11519) still requires `slto_kingdom_lady` occupation. Let me verify the sex conditions more specifically.

**To verify:** Need to check exact conditions on the `fuck_decision` state and the `camp_lover_talk` entry points.

**Codesearch needed:** Exact conditions at `camp_lover_talk` entry and `fuck_decision`.

**To implement (if not done):**
- Remove `slto_kingdom_lady` requirement from spouse sex dialogue
- Remove relation ≥ 1 requirement
- Keep only the spouse slot check

---

### 7. Generic Temporary Minister Dialogue Expansion

**Havenost says:** Gave the generic temporary minister all the dialogue options as if you had appointed a companion/spouse as minister. Can now declare war, do spying actions, etc. Also added option to rehire him if you want to free up companions/spouse.

**Current status:** ❌ NOT FULLY IMPLEMENTED — The temporary minister (`trp_temporary_minister`) currently:
- Gets auto-assigned if `$g_player_minister ≤ 0` (`source/module_simple_triggers.py:3396-3412`)
- When player has since appointed a real minister, the temporary says goodbye and closes window (line 2815-2817)
- When temporary IS the current minister, they enter `minister_issues` state, but restricted:
  - ❌ Political quests, emissary, indict, rename, change marshal — blocked behind hero checks
  - ✅ Basic advice, retire/rejoin, grant fief, make self lord

**Files:**
- `source/module_dialogs.py:2806-2817` — minister talk triggers
- `source/module_dialogs.py:5160-5292` — restricted options

**Opportunity — review & reorganize minister dialog:**
- Too many dialog options currently — could group them into categories
- Bug: game offers recruit option, you deny, then can't hire again until conquering a city
- This is a good chance to clean up the whole minister dialog structure while expanding temp minister capabilities

---

## ITEMS CHANGES (`module_items.py`)

### 8. Add `itp_merchandise` to Various Items

**Havenost says:** Added `itp_merchandise` flag to: Black Knight/Khergit Guard armors, noble/court clothes, wood practice/tournament weapons, Armored Tunics.

**Current status:** ❓ NEEDS BETTER INVESTIGATION — Likely refers to **Angela/Queens Blade** items and **Dark Hunter** items. Need to check their item IDs and `itp_merchandise` status. Generic tunics (linen, red, etc.) already have the flag.

**Note from maintainer (28 Jul 2026):** "yes and probably dark hunter items aswell"

**Items flagged in initial search (preliminary — may not be what Havenost means):**

| Item | `itp_merchandise` | Status |
|------|-------------------|--------|
| `black_armor` (line 484) | ❌ Missing | NOT done |
| `khergit_guard_armor` (line 1194) | ❌ Missing | NOT done |
| `courtly_outfit` (line 330) | ❌ Missing | NOT done |
| `nobleman_outfit` (line 331) | ❌ Missing | NOT done |
| `court_dress` (line 1192) | ❌ Missing | NOT done |
| `rich_outfit` (line 1193) | ❌ Missing | NOT done |
| `court_hat` (line 543) | ❌ Missing | NOT done |
| `practice_sword` (line 61) | ❌ Missing | NOT done |
| `practice_axe` (line 65) | ❌ Missing | NOT done |
| `practice_staff` (line 74) | ❌ Missing | NOT done |
| `practice_lance` (line 75) | ❌ Missing | NOT done |
| `practice_bow` (line 77) | ❌ Missing | NOT done |
| `practice_crossbow` (line 79) | ❌ Missing | NOT done |
| `practice_javelin` (line 80) | ❌ Missing | NOT done |
| `practice_shield` (line 76) | ❌ Missing | NOT done |
| `practice_horse` (line 85) | ❌ Missing | NOT done |
| `practice_arrows` (line 86) | ❌ Missing | NOT done |
| `practice_bolts` (line 88) | ❌ Missing | NOT done |
| `tournament_warhorse` (line 247) | ❌ Missing | NOT done |
| `mail_with_tunic_red` (line 349) | ❌ Missing | NOT done |
| `mail_with_tunic_green` (line 350) | ❌ Missing | NOT done |
| `black_greaves` (line 298) | ❌ Missing | NOT done (35 leg, best in game) |

**Note:** Many vanilla weapons are commented out in this mod (swords, axes, spears, shields at lines 664-994). This appears to be a deliberate item-pool reduction by Dickplomacy.

**Also:** The CSTM eligibility script (`cstmmerge_scripts.py:269-300`) requires `itp_merchandise` AND `value > 0` for items to appear in the CSTM equipment editor. Adding `itp_merchandise` to these items would also make them available for CSTM troop customization.

---

### 9. Custom Armor / Queen's Blade Price Normalization

**Havenost says:** Made custom armor the same price as equivalent vanilla gear with same stats. Examples:
- `plate_boots_dthun`: 2770 → 1770 (same as `plate_boots` / `iron_greaves`, both 33 leg armor)
- `custom_armor3` (Heavy): 9000 → 6900 (same as `plate_armor_dthun`)

**Current status:** ❓ NEEDS BETTER INVESTIGATION — The prices Havenost changed are likely for **Angela/Queens Blade** items specifically, not the custom armor / DtheHun items listed below. Need to check the angela items' prices.

**Note from maintainer (28 Jul 2026):** "Probably refers to angela items and things like that, need to check better later."

**Preliminary scan (may not be relevant — DtheHun items, not Angela):**

| Item | Current Price | Equivalent Item | Equivalent Price | Notes |
|------|--------------|-----------------|-----------------|-------|
| `plate_boots_dthun` (line 1575) | **2770** | `plate_boots` / `iron_greaves` | 1770 | Same stats (33 leg, 3.5 wt). Dthun has lower diff (6 vs 9) |
| `custom_armor3` (line 1957) | **9000** | `plate_armor` | 6553 | Same stats (55 body, 17 leg, 27 wt). Dthun diff 8 vs plate diff 9 |
| `plate_armor_dthun` (line 2034) | **6900** | `plate_armor` | 6553 | 345 more (5% premium) |
| `scale_armor_dthun` (line 1711) | **2500** | `scale_armor` | 2558 | 58 less, BUT worse stats (42 body vs 52) |
| `custom_armor2` (line 1879) | **3000** | `scale_armor` | 2558 | Worse body (42 vs 52) but costs more |
| `custom_armor1` (line 1797) | **1000** | `tribal_warrior_outfit` | 520 | ~2x price for same body (30) |
| `diabassa_armor` (line 2076) | **3000** | `scale_armor` | 2558 | 40 body vs 52 body, costs MORE |
| `risty_armor` (line 1751) | **1700** | `byrnie` | 780 | 36 body vs 34 body, rough match |
| `sonja_armor` (line 2122) | **696** | `tribal_warrior_outfit` | 520 | 30 body vs 30 body, close |

**Havenost's stance:** "I didn't change any stats prices" — meaning he only changed purchase price, not stat-based pricing.

---

## CSTM TROOP TREES (`cstm_troop_trees.py`)

### 10. Remove Level-Up Aging

**Havenost says:** Removed the level-up aging script where leveling up troops made them 15-20 years older per tier, causing tier 5-7 troops to look like elderly 60-90 year olds.

**Current status:** ⚠️ AGING EXISTS — The `get_custom_troop()` function at `modmerger/mods/cstm/cstm_troop_trees.py:40-47` applies age proportional to tier:

```python
fc1 = face_code_with_age(skin.face_code_1, MAX_AGE * tier / self.num_tiers)
fc2 = face_code_with_age(skin.face_code_2, MAX_AGE * (tier + 1) / self.num_tiers)
```

- `MAX_AGE = 0xfc = 252`
- `num_tiers = 5` (for most trees)
- Tier 0: age 0 → Tier 4: age ~201

**Opportunity — review troop trees:** This is a good chance to review the CSTM troop trees as a whole and make adjustments, not just remove the aging. Check balance, progression, equipment assignments across all trees.

**Files:**
- `modmerger/mods/cstm/cstm_troop_trees.py:40-47` (and entire file for review)

---

## PLANNED FIXES (Havenost's WIP)

### 11. Auto-Sell Logic — Sell to Proper Merchant

**Skip — not relevant.** The auto-sell system has been completely rewritten. Havenost's complaints about the old Diplomacy auto-sell don't apply to the current codebase.

---

### 12. Force Troops to Spawn with All Melee Weapons

**Havenost says:** Plans to integrate a script (referenced from MBModWiki) to force generic troops to spawn with all melee weapons given in the custom tree designer, rather than the game randomly picking 1-2.

**Current status:** ❓ UNKNOWN — Havenost mentions an MBModWiki script for forcing all melee weapons on spawn. Need to investigate what this actually means in practice. The `tf_guarantee_*` flags in Warband don't cover melee weapons, so this would need a script-level workaround at mission spawn time.

---

### 13. Disable Debug Messages with Cheat Setting

**Havenost says:** Wants an option to disable debug messages while cheat setting is enabled. Currently can only toggle between All/Political/Economic messages, not "None".

**Current status:** ⚠️ CAN COPY FROM CC — "cc had something like that we can copy from there since we have the source code." Need to locate the relevant CC source and port the debug message toggle feature.

---

### 14. Recruit Any Spouse Regardless of Personality Type

**Havenost says:** Currently only 2 of 5 spouse personality types can be recruited to party (Adventurous and Otherworldly). He plans to allow any personality type to be recruited, with relationship penalty. Also notes a bug where re-recruiting resets stats/equipment.

**Current status:** ❓ NEVER TESTED — Haven't looked at spouse recruitment at all. The `spouse_join` code at `module_dialogs.py:31868-32086` from code analysis shows:
- Only `lrep_adventurous` and `lrep_otherworldly` accept
- Others refuse with relation penalties
- Recruitment scripts hard-set equipment/stats — re-recruit would wipe player-given gear

**Priority:** Low — needs testing first.

---

## SUMMARY TABLE

| # | Feature | Status | Notes |
|---|--------|--------|-------|
| 1 | Custom armor for all troops | ✅ Already implemented | — |
| 2 | Spar with spouse in camp | ❌ Not implemented | — |
| 3 | Party talk options in camp | ❌ Missing many options | Also a chance to review/reorganize |
| 4 | Recruit pretenders as companions | ⚠️ Native behavior; ours converts via minister | Needs edge-case debugging |
| 5 | Sex with pretenders/claimants | ⚠️ Partially works (different scenarios) | Needs investigation |
| 6 | Relax spouse sex conditions | ⚠️ Need to verify exact conditions | — |
| 7 | Expand temp minister dialogue | ❌ Not implemented | Opportunity to reorganize all minister dialog |
| 8 | Add `itp_merchandise` | ❓ Angela + Dark Hunter items | Needs check |
| 9 | Normalize armor prices | ❓ Angela items | Needs check |
| 10 | CSTM level-up aging | ⚠️ Still exists | Opportunity to review all troop trees |
| 11 | Auto-sell to correct merchant | ✅ Skip — system rewritten | Not relevant |
| 12 | Force all melee weapons on spawn | ❓ Unknown what this means | Needs investigation |
| 13 | Disable debug messages | ⚠️ Can copy from CC source | CC source code available |
| 14 | Recruit any spouse personality | ❓ Never tested | Needs testing first |

---

## KEY FILE INDEX

| File | Path |
|------|------|
| Main dialogs | `source/module_dialogs.py` |
| Items | `source/module_items.py` |
| Troops | `source/module_troops.py` |
| Constants | `source/module_constants.py` |
| Camp menu | `source/game_menus/mnu_camp_action.py` |
| Camp scene setup | `source/scripts/setup_camp_scene.py` |
| Custom armor presentation | `source/presentations/prsnt_customize_armor.py` |
| CSTM troop trees | `modmerger/mods/cstm/cstm_troop_trees.py` |
| CSTM presentations | `modmerger/mods/cstm/cstm_presentations.py` |
| CSTM scripts | `modmerger/mods/cstm/cstm_scripts.py` |
| CSTM merge dialogs | `modmerger/mods/cstmmerge/cstmmerge_dialogs.py` |
| CSTM merge scripts | `modmerger/mods/cstmmerge/cstmmerge_scripts.py` |
| Auto-sell core | `source/scripts/dplmc_auto_sell.py` |
| Auto-sell at center | `source/scripts/dplmc_player_auto_sell_at_center.py` |
| Auto-trade sell | `source/scripts/auto_trade_sell_to_merchant.py` |
| Simple triggers | `source/module_simple_triggers.py` |
| Sort mod dialogs | `modmerger/mods/sort/sort_dialogs.py` |
