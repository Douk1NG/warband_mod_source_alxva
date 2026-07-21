# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_court_lost_menu = [
(
  "notification_court_lost",0,
  "{s12}",
  "none",
  [
    (try_begin),
		(is_between, "$g_player_court", centers_begin, centers_end),
		(str_store_party_name, s10, "$g_player_court"),
		(str_store_party_name, s11, "$g_player_court"),
	(else_try),
		(str_store_string, s10, "str_your_previous_court_some_time_ago"),
		(str_store_string, s11, "str_your_previous_court_some_time_ago"),
	(try_end),

	##diplomacy start+ Handle player is co-ruler of NPC kingdom
	(assign, ":alt_faction", "fac_player_supporters_faction"),
	(try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_faction", "$players_kingdom"),
	(try_end),
	##diplomacy end+

    (try_begin), #SB : loss of court = loss of right to rule
      (store_and, ":name_set", "$players_kingdom_name_set", rename_center),
      (eq, ":name_set", rename_center),
      (call_script, "script_change_player_right_to_rule", -20),
      #the old "capital" should be stored so that this penalty does not apply twice
      #but we'll let the player name a new center
      (val_sub, "$players_kingdom_name_set", rename_center),
    (else_try), #need a court to lose one
      (is_between, "$g_player_court", centers_begin, centers_end),
      (call_script, "script_change_player_right_to_rule", -5),
    (try_end),
    (assign, "$g_player_court", -1),
	(str_store_string, s14, "str_after_to_the_fall_of_s11_your_court_has_nowhere_to_go"),
	(try_begin),
		##diplomacy start+  Handle player is co-ruler of NPC kingdom
		(this_or_next|neg|is_between, ":alt_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(neg|faction_slot_eq, ":alt_faction", slot_faction_state, sfs_active),
		##diplomacy end+
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(str_store_string, s14, "str_as_you_no_longer_maintain_an_independent_kingdom_you_no_longer_maintain_a_court"),
	(try_end),

	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(eq, "$g_player_court", -1),
    ##diplomacy begin
    (neg|party_slot_eq, ":walled_center", slot_village_infested_by_bandits, "trp_peasant_woman"),
    ##diplomacy end
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(this_or_next|eq, ":alt_faction", ":walled_center_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(neg|party_slot_ge, ":walled_center", slot_town_lord, active_npcs_begin),

		(assign, "$g_player_court", ":walled_center"),
		(try_begin),
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			##diplomacy start+ Check that the spouse is not a hero, imprisoned (except by the player), or exiled/dead/etc.
            (try_begin),
                (neg|troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
                (neg|troop_slot_ge, ":spouse", slot_troop_occupation, slto_retirement),
                (neg|troop_slot_ge, ":spouse", slot_troop_prisoner_of_party, 1),
                ##diplomacy end+
                (neg|main_party_has_troop,":spouse"),
                (troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
            (try_end),
			(str_store_party_name, s11, "$g_player_court"),
		(try_end),

		(str_store_string, s14, "str_due_to_the_fall_of_s10_your_court_has_been_relocated_to_s12"), #actually s11
	(try_end),

	(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		(eq, "$g_player_court", -1),

		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
		##diplomacy start+ Handle player is co-ruler of NPC kingdom
		(this_or_next|eq, ":alt_faction", ":walled_center_faction"),
		##diplomacy end+
		(eq, ":walled_center_faction", "fac_player_supporters_faction"),

		(assign, "$g_player_court", ":walled_center"),

		(try_begin),
			(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
			(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
			##diplomacy start+ Check that the spouse is not a hero, imprisoned (except by the player), or exiled/dead/etc.
			(neg|troop_slot_eq, ":spouse", slot_troop_occupation, slto_kingdom_hero),
			(neg|troop_slot_ge, ":spouse", slot_troop_occupation, slto_retirement),
			(neg|troop_slot_ge, ":spouse", slot_troop_prisoner_of_party, 1),
			##diplomacy end+
			(troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
		(try_end),

		(party_get_slot, ":town_lord", ":walled_center", slot_town_lord),
		(str_store_party_name, s11, "$g_player_court"),
		(str_store_troop_name, s9, ":town_lord"),
		(str_store_string, s14, "str_after_to_the_fall_of_s10_your_faithful_vassal_s9_has_invited_your_court_to_s11_"),
	(try_end),

	(try_begin),
		##diplomacy start+  Handle player is co-ruler of NPC kingdom
		(this_or_next|neg|is_between, ":alt_faction", npc_kingdoms_begin, npc_kingdoms_end),
			(neg|faction_slot_eq, ":alt_faction", slot_faction_state, sfs_active),
		##diplomacy end+
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(str_store_string, s14, "str_as_you_no_longer_maintain_an_independent_kingdom_you_no_longer_maintain_a_court"),
	(try_end),
	(str_store_string, s12, s14),
  ],
  [
      ("continue",[],"Continue...",[
	  (change_screen_return),
	  ]),
     ],
  )
]
