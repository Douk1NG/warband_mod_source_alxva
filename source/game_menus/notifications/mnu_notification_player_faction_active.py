# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_player_faction_active_menu = [
(
    "notification_player_faction_active",0,
    "You now possess land in your name, without being tied to any kingdom. This makes you a monarch in your own right, with your court temporarily located at {s12}. However, the other kings in Calradia will at first consider you a threat, for if any upstart warlord can grab a throne, then their own legitimacy is called into question.^^You may find it desirable at this time to pledge yourself to an existing kingdom. If you want to continue as a sovereign monarch, then your first priority should be to establish an independent right to rule. You can establish your right to rule through several means -- marrying into a high-born family, recruiting new lords, governing your lands, treating with other kings, or dispatching your companions on missions.^^At any rate, your first step should be to appoint a chief minister from among your companions, to handle affairs of state. Different companions have different capabilities.^You may appoint new ministers from time to time. You may also change the location of your court, by speaking to the minister.",
    "none",
    [
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),

      (unlock_achievement, ACHIEVEMENT_CALRADIAN_TEA_PARTY),
      (play_track, "track_coronation"),

	  (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
	    (lt, "$g_player_court", walled_centers_begin),
		(store_faction_of_party, ":walled_center_faction", ":walled_center"),
	    (eq, ":walled_center_faction", "fac_player_supporters_faction"),
		(assign, "$g_player_court", ":walled_center"),

		##diplomacy start+
		#OLD VERSION:
		#(try_begin),
		#	(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
		#	(is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
		#	(troop_set_slot, ":spouse", slot_troop_cur_center, "$g_player_court"),
		#(try_end),
		#
		#NEW VERSION:
		#For settings with polygamy, check all kingdom ladies to see if they are wives.
		#Also move unmarried daughters/sisters of the player if they exist (they cannot
		#in Native, but might in mods).
		(try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
			#Make sure the spouse hasn't been promoted, and is not a prisoner, and is not exiled/dead
			(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
			(neg|troop_slot_ge, ":lady", slot_troop_leaded_party, 0),
			#Make sure the lady isn't a prisoner
			(neg|troop_slot_ge, ":lady", slot_troop_prisoner_of_party, 0),
            (neg|main_party_has_troop, ":lady"),
			(try_begin),
				#Check if the lady is the player's spouse
				(this_or_next|troop_slot_eq, "trp_player", slot_troop_spouse, ":lady"),
					(troop_slot_eq, ":lady", slot_troop_spouse, "trp_player"),
				#Update location
				(troop_set_slot, ":lady", slot_troop_cur_center, "$g_player_court"),
			(else_try),
				#If the lady is unmarried, check if she is the player's dependent.
				(troop_slot_eq, ":lady", slot_troop_spouse, -1),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_father, "trp_player"),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_mother, "trp_player"),
					(troop_slot_eq, ":lady", slot_troop_guardian, "trp_player"),
				#Update location
				(troop_set_slot, ":lady", slot_troop_cur_center, "$g_player_court"),
			(try_end),
		(try_end),
		##diplomacy end+

		(str_store_party_name, s12, "$g_player_court"),
	  (try_end),

      ],
    [
	  ##diplomacy start+
	  #Make compatible with polygamy
      ("appoint_spouse",[
	  (troop_slot_ge, "trp_player", slot_troop_spouse, 1),
	  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	  (neg|troop_slot_eq, ":player_spouse", slot_troop_occupation, slto_kingdom_hero),
	  ##diplomacy start+
	  #Also do not appoint the missing or the dead
	  (neg|troop_slot_ge, ":player_spouse", slot_troop_occupation, slto_retirement),
	  (call_script, "script_dplmc_store_troop_is_female", ":player_spouse"),#reg0 make gender-correct
	  ##diplomacy end+
	  (str_store_troop_name, s10, ":player_spouse"),
	  ],"Appoint your {reg0?wife:husband}, {s10}...",
       [
	   (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	   (assign, "$g_player_minister", ":player_spouse"),
	   (jump_to_menu, "mnu_minister_confirm"),
	   ]),
	  ##diplomacy end+

	  ##diplomacy start+
	  #Check for one additional spouse (polygamy may be enabled)
      ("dplmc_appoint_spouse_plus_1",[
	  (troop_slot_ge, "trp_player", slot_troop_spouse, 1),
	  (assign, ":player_spouse", -1),
	  (try_for_range_backwards, ":troop_no", heroes_begin, heroes_end),#Go backwards to ensure we end with the first match
		(troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		(neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),#Not ordinary spouse
		(neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),#Not retired/dead/exiled
		(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#Not leading a party
		(assign, ":player_spouse", ":troop_no"),
	  (try_end),
	  (ge, ":player_spouse", 1),
	  (call_script, "script_dplmc_store_troop_is_female", ":player_spouse"),
	  (str_store_troop_name, s10, ":player_spouse"),
	  ],"Appoint your {reg0?wife:husband}, {s10}...",
       [
	   (assign, ":player_spouse", -1),
	   (try_for_range_backwards, ":troop_no", heroes_begin, heroes_end),#Go backwards to ensure we end with the first match
	     (troop_slot_eq, ":troop_no", slot_troop_spouse, "trp_player"),
		 (neg|troop_slot_eq, "trp_player", slot_troop_spouse, ":troop_no"),#Not ordinary spouse
		 (neg|troop_slot_ge, ":troop_no", slot_troop_occupation, slto_retirement),#Not retired/dead/exiled
		 (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#Not leading a party
		 (assign, ":player_spouse", ":troop_no"),
	   (try_end),
	   (try_begin),
		  (lt, ":player_spouse", 1),#This shouldn't be possible
		  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	   (try_end),

	   (assign, "$g_player_minister", ":player_spouse"),
	   (jump_to_menu, "mnu_minister_confirm"),
	   ]),
	  ##diplomacy end+
      ]+

    #SB : roll into loop
      [("appoint_npc"+str(x), [
      (main_party_has_troop, "trp_npc"+str(x)),
      (str_store_troop_name, s10, "trp_npc"+str(x)),
      ],"Appoint {s10}", [
       (assign, "$g_player_minister", "trp_npc"+str(x)),
       (jump_to_menu, "mnu_minister_confirm"),
      ]) for x in range (1, 17)]

    +[
      ("appoint_default",[],"Appoint a prominent citizen from the area...",
       [
	   (assign, "$g_player_minister", "trp_temporary_minister"),
	   (troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
	   (jump_to_menu, "mnu_minister_confirm"),
        ]),
     ]
  )
]
