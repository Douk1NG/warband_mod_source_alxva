# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notifications_menus = [
  (
    "notification_truce_expired",0,
    "Truce Has Expired^^The truce between {s1} and {s2} has expired.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_feast_quest_expired",0,
    "{s10}",
    "none",
    [
    (str_store_string, s10, "str_feast_quest_expired"),
    ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_sortie_possible",0,
    "Enemy Sighted: Enemies have been sighted outside the walls of {s4}, and {s5} and others are preparing for a sortie. You may join them if you wish.",
    "none",
    [
	(str_store_party_name, s4, "$g_notification_menu_var1"),
	(party_stack_get_troop_id, ":leader", "$g_notification_menu_var2", 0),
	(str_store_troop_name, s5, ":leader"),
      ],
    [
      ("continue",[],"Continue",
       [
	   #stop auto-clock

	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_casus_belli_expired",0,
    "Kingdom Fails to Respond^^The {s1} has not responded to the {s2}'s provocations, and {s3} suffers a loss of face among {reg4?her:his} more bellicose subjects...^",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
	  (faction_get_slot, ":faction_leader", "$g_notification_menu_var1", slot_faction_leader),
      (str_store_troop_name, s3, ":faction_leader"),
	  ##diplomacy start+ use a script for gender
	  #(troop_get_type, reg4, ":faction_leader"),#<- OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":faction_leader", 4),
     ##diplomacy end+

      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue",
       [
	   (call_script, "script_faction_follows_controversial_policy", "$g_notification_menu_var1", logent_policy_ruler_ignores_provocation),
	   (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_lord_defects",0,
##diplomacy start+ Fix gender of pronouns
    "Defection: {s4} has abandoned the {s5} and joined the {s7}, taking {reg4?her:his} fiefs with {reg4?her:him}",
##diplomacy end+
    "none",
	[
	  (assign, ":defecting_lord", "$g_notification_menu_var1"),
	  (assign, ":old_faction", "$g_notification_menu_var2"),
	  (str_store_troop_name, s4, ":defecting_lord"),
	  (str_store_faction_name, s5, ":old_faction"),
	  (store_faction_of_troop, ":new_faction", ":defecting_lord"),
	  (str_store_faction_name, s7, ":new_faction"),
	  ##diplomacy start+ get gender with script
	  #(troop_get_type, reg4, ":defecting_lord"),#<-OLD
	  (call_script, "script_dplmc_store_troop_is_female_reg", ":defecting_lord", 4),
	  ##diplomacy end+

	],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
	),
  (
    "notification_treason_indictment",0,
    "Treason Indictment^^{s9}",
    "none",
    [
	  (assign, ":indicted_lord", "$g_notification_menu_var1"),
	  (assign, ":former_faction", "$g_notification_menu_var2"),
	  (faction_get_slot, ":former_faction_leader", ":former_faction", slot_faction_leader),

	  #Set up string
	  (try_begin),
			(eq, ":indicted_lord", "trp_player"),
			(str_store_troop_name, s7, ":former_faction_leader"),
			(str_store_string, s9, "str_you_have_been_indicted_for_treason_to_s7_your_properties_have_been_confiscated_and_you_would_be_well_advised_to_flee_for_your_life"),
	  (else_try),
			(str_store_troop_name_link, s4, ":indicted_lord"),
			(str_store_faction_name_link, s5, ":former_faction"),
			(str_store_troop_name_link, s6, ":former_faction_leader"),

		   ##diplomacy start+ get gender with script
			#(troop_get_type, reg4, ":indicted_lord"),#<-OLD
			(call_script, "script_dplmc_store_troop_is_female_reg", ":indicted_lord", 4),
			##diplomacy end+
			(store_faction_of_troop, ":new_faction", ":indicted_lord"),
			(try_begin),
				(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				(str_store_faction_name_link, s10, ":new_faction"),
				(str_store_string, s11, "str_with_the_s10"),
			(else_try),
				(str_store_string, s11, "str_outside_calradia"),
			(try_end),
			(str_store_string, s9, "str_by_order_of_s6_s4_of_the_s5_has_been_indicted_for_treason_the_lord_has_been_stripped_of_all_reg4herhis_properties_and_has_fled_for_reg4herhis_life_he_is_rumored_to_have_gone_into_exile_s11"),
		(try_end),


	],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
	),
  (
    "notification_border_incident",0,
    "Border incident^^Word reaches you that {s9}. Though you don't know whether or not the rumors are true, you do know one thing -- this seemingly minor incident has raised passions among the {s4}, making it easier for them to go to war against the {s3}, if they want it...",
    "none",
    [
	  (assign, ":acting_village", "$g_notification_menu_var1"),
	  (assign, ":target_village", "$g_notification_menu_var2"),
	  (store_faction_of_party, ":acting_faction", ":acting_village"),

	  (try_begin),
			(eq, ":target_village", -1),
			(party_get_slot, ":target_faction", ":acting_village", slot_center_original_faction),
			(try_begin),
				(this_or_next|eq, ":target_faction", ":acting_faction"),
                              		(neg|faction_slot_eq, ":target_faction", slot_faction_state, sfs_active),
				(party_get_slot, ":target_faction", ":acting_village", slot_center_ex_faction),
			(try_end),

		    (str_store_party_name, s1, ":acting_village"),
		    (str_store_faction_name, s3, ":acting_faction"),
		    (str_store_faction_name, s4, ":target_faction"),
			(faction_get_slot, ":target_leader", ":target_faction", slot_faction_leader),
		    (str_store_troop_name, s5, ":target_leader"),

			(str_store_string, s9, "str_local_notables_from_s1_a_village_claimed_by_the_s4_have_been_mistreated_by_their_overlords_from_the_s3_and_petition_s5_for_protection"),
			(display_log_message, "@There has been an alleged border incident: {s9}"),

			(call_script, "script_add_log_entry", logent_border_incident_subjects_mistreated, ":acting_village", -1, -1, ":acting_faction"),


      (else_try),
			(store_faction_of_party, ":target_faction", ":target_village"),

		    (str_store_party_name, s1, ":acting_village"),
		    (str_store_party_name, s2, ":target_village"),

			(store_random_in_range, ":random", 0, 3),
			(try_begin),
				(eq, ":random", 0),

				(str_store_string, s9, "str_villagers_from_s1_stole_some_cattle_from_s2"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),

				(call_script, "script_add_log_entry", logent_border_incident_cattle_stolen, ":acting_village", ":target_village", -1,":acting_faction"),

			(else_try),
				(eq, ":random", 1),

				(str_store_string, s9, "str_villagers_from_s1_abducted_a_woman_from_a_prominent_family_in_s2_to_marry_one_of_their_boys"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),

				(call_script, "script_add_log_entry", logent_border_incident_bride_abducted, ":acting_village", ":target_village", -1, ":acting_faction"),
			(else_try),
				(eq, ":random", 2),

				(str_store_string, s9, "str_villagers_from_s1_killed_some_farmers_from_s2_in_a_fight_over_the_diversion_of_a_stream"),
				(display_log_message, "@There has been an alleged border incident: {s9}"),

			    (call_script, "script_add_log_entry", logent_border_incident_villagers_killed, ":acting_village", ":target_village", -1,":acting_faction"),
			(try_end),

	  (try_end),

	  (str_store_faction_name, s3, ":acting_faction"),
	  (str_store_faction_name, s4, ":target_faction"),

	  (store_add, ":slot_provocation_days", ":acting_faction", slot_faction_provocation_days_with_factions_begin),
	  (val_sub, ":slot_provocation_days", kingdoms_begin),
	  (faction_set_slot, ":target_faction", ":slot_provocation_days", 30),

      ],
    [
      ("continue",[],"Continue",
       [
	   (change_screen_return),
        ]),
     ]
  ),
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
  ),
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
  ),
  (
    "notification_player_faction_deactive",0,
    "Your kingdom no longer holds any land.",
    "none",
    [
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [
       (assign, "$g_player_minister", -1),
       (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_wedding_day",mnf_scale_picture,
    "{s8} wishes to inform you that preparations for your wedding at {s10} have been complete, and that your presence is expected imminently .",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),
		(str_store_troop_name, s8, "$g_notification_menu_var1"),
		(str_store_party_name, s10, "$g_notification_menu_var2"),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_kingdom_holds_feast",mnf_scale_picture,
    "{s11}",
    "none",
    [
		(set_background_mesh, "mesh_pic_messenger"),

		(str_store_troop_name, s8, "$g_notification_menu_var1"),
		(store_faction_of_troop, ":host_faction", "$g_notification_menu_var1"),
		(str_store_faction_name, s9, ":host_faction"),

#		(str_store_faction_name, s9, "$players_kingdom"),
		(str_store_party_name, s10, "$g_notification_menu_var2"),

		(str_clear, s12),
		(try_begin),
			(check_quest_active, "qst_wed_betrothed"),
			(quest_get_slot, ":giver_troop", "qst_wed_betrothed", slot_quest_giver_troop),
			(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
			(eq, ":giver_troop_faction", "$players_kingdom"),
			(str_store_string, s12, "str_feast_wedding_opportunity"),
		(try_end),



		(str_store_string, s11, "str_s8_wishes_to_inform_you_that_the_lords_of_s9_will_be_gathering_for_a_feast_at_his_great_hall_in_s10_and_invites_you_to_be_part_of_this_august_assembly"),
		(try_begin),
			(eq, "$g_notification_menu_var1", 0),
			(str_store_string, s11, "str_the_great_lords_of_your_kingdom_plan_to_gather_at_your_hall_in_s10_for_a_feast"),
		(try_end),
		(str_store_string, s11, "@{!}{s11}{s12}"),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(store_current_hours, ":hours_since_last_feast"),
			(faction_get_slot, ":last_feast_start_time", "$players_kingdom", slot_faction_last_feast_start_time),
			(val_sub, ":hours_since_last_feast", ":last_feast_start_time"),
			(assign, reg4, ":hours_since_last_feast"),
			(display_message, "@{!}DEBUG -- Hours since last feast started: {reg4}"),
		(try_end),

      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_center_under_siege",0,
    "{s1} has been besieged by {s2} of {s3}!",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_village_raided",0,
    "Enemies have Laid Waste to a Fief^^{s1} has been raided by {s2} of {s3}!",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_village_raid_started",0,
    "Your Village is under Attack!^^{s2} of {s3} is laying waste to {s1}.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_troop_name, s2, "$g_notification_menu_var2"),
      (store_troop_faction, ":troop_faction", "$g_notification_menu_var2"),
      (str_store_faction_name, s3, ":troop_faction"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_one_faction_left",0,
    "Calradia Conquered by One Kingdom^^{s1} has defeated all rivals and stands as the sole kingdom.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
	  (try_begin),
		(faction_slot_eq, "$g_notification_menu_var1", slot_faction_leader, "trp_player"),
		(unlock_achievement, ACHIEVEMENT_THE_GOLDEN_THRONE),
	  (else_try),
		(unlock_achievement, ACHIEVEMENT_MANIFEST_DESTINY),
	  (try_end),

        (try_begin),
            (troop_get_type, ":is_female", "trp_player"),
            (eq, ":is_female", 1),
            (unlock_achievement, ACHIEVEMENT_EMPRESS),
        (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_oath_renounced_faction_defeated",0,
    "Your Old Faction was Defeated^^You won the battle against {s1}! This ends your struggle which started after you renounced your oath to them.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_center_lost",0,
    "An Estate was Lost^^You have lost {s1} to {s2}.",
    "none",
    [
      (str_store_party_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 62),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_center_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_troop_left_players_faction",0,
    "Betrayal!^^{s1} has left {s2} and joined {s3}.",
    "none",
    [
      (str_store_troop_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$players_kingdom"),
      (str_store_faction_name, s3, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_troop_joined_players_faction",0,
    "Good news!^^ {s1} has left {s2} and joined {s3}.",
    "none",
    [
      (str_store_troop_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (str_store_faction_name, s3, "$players_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_war_declared",0,
    "Declaration of War^^{s1} has declared war against {s2}!",
    "none",
    [

#	  (try_begin),
#		(eq, "$g_include_diplo_explanation", "$g_notification_menu_var1"),
#		(assign, "$g_include_diplo_explanation", 0),
#		(str_store_string, s57, "$g_notification_menu_var1"),
#	  (else_try),
#	    (str_clear, s57),
#	  (try_end),


	#to do the reason, have war_damage = 0 yield pre-war reasons
      (try_begin),
#        (eq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
#        (str_store_faction_name, s1, "$g_notification_menu_var2"),
#        (str_store_string, s2, "@you"),
#      (else_try),
#        (eq, "$g_notification_menu_var2", "fac_player_supporters_faction"),
#        (str_store_faction_name, s1, "$g_notification_menu_var1"),
#        (str_store_string, s2, "@you"),
#      (else_try),
        (str_store_faction_name, s1, "$g_notification_menu_var1"),
        (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (try_end),


      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_peace_declared",0,
    "Peace Agreement^^{s1} and {s2} have made peace!^{s57}",
    "none",
    [

	  (try_begin),
		(eq, 1, 0), #Alas, this does not seem to work
		(eq, "$g_include_diplo_explanation", "$g_notification_menu_var1"),
		(assign, "$g_include_diplo_explanation", 0),
	  (else_try),
	    (str_clear, s57),
	  (try_end),

	  (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (store_sub, ":faction_1", "$g_notification_menu_var1", kingdoms_begin),
      (store_sub, ":faction_2", "$g_notification_menu_var2", kingdoms_begin),
      (val_mul, ":faction_1", 128),
      (val_add, ":faction_1", ":faction_2"),
      (set_game_menu_tableau_mesh, "tableau_2_factions_mesh", ":faction_1", pos0),
      ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_faction_defeated",0,
    "Faction Eliminated^^{s1} is no more!",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", npc_kingdoms_begin, kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
         (try_begin),
           (is_between, "$supported_pretender", pretenders_begin, pretenders_end),
           (troop_slot_eq, "$supported_pretender", slot_troop_original_faction, "$g_notification_menu_var1"),

           #All rebels switch to kingdom
           (try_for_range, ":cur_troop", heroes_begin, heroes_end),
             (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (troop_set_faction, ":cur_troop", "$g_notification_menu_var1"),
             (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", "$g_notification_menu_var1"),
             (try_begin),
               (this_or_next|eq, "$g_notification_menu_var1", "$players_kingdom"),
               (eq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
               (call_script, "script_check_concilio_calradi_achievement"),
             (try_end),
           (else_try), #all loyal lords gain a small bonus with the player
             (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "$g_notification_menu_var1"),
             (call_script, "script_troop_change_relation_with_troop", ":cur_troop", "trp_player", 5),
           (try_end),
           ###(((rebels_switch FIX
           (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (troop_set_faction, ":cur_troop", "$g_notification_menu_var1"),
             (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", "$g_notification_menu_var1"),
           (try_end),
           ###)))

           (try_for_parties, ":cur_party"),
             (store_faction_of_party, ":cur_faction", ":cur_party"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (party_set_faction, ":cur_party", "$g_notification_menu_var1"),
           (try_end),

           (assign, "$players_kingdom", "$g_notification_menu_var1"),
           (try_begin),
            (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
            (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
            (troop_set_faction, ":spouse", "$g_notification_menu_var1"),
           (try_end),


           (call_script, "script_add_notification_menu", "mnu_notification_rebels_switched_to_faction", "$g_notification_menu_var1", "$supported_pretender"),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_state, sfs_active),
           (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),

           (faction_get_slot, ":old_leader", "$g_notification_menu_var1", slot_faction_leader),
           #(troop_set_slot, ":old_leader", slot_troop_change_to_faction, "fac_commoners"),
           (call_script, "script_change_troop_faction", ":old_leader", "fac_commoners"), #dckplmc - prevent possible respawn before actual faction changes
           #SB : renown loss of under 25%
           (troop_get_slot, ":old_renown", ":old_leader", slot_troop_renown),
           (store_random_in_range, ":renown_loss", 10, 25),
           (val_mul, ":renown_loss", ":old_renown"),
           (val_div, ":renown_loss", 100),
           (val_sub, ":old_renown", ":renown_loss"),
           (troop_set_slot, ":old_leader", slot_troop_renown, ":old_renown"),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_leader, "$supported_pretender"),
           (troop_set_faction, "$supported_pretender", "$g_notification_menu_var1"),

           (faction_get_slot, ":old_marshall", "$g_notification_menu_var1", slot_faction_marshall),
           (try_begin),
             (ge, ":old_marshall", 0),
             (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
             (party_is_active, ":old_marshall_party"),
             (party_set_marshal, ":old_marshall_party", 0),
           (try_end),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_marshall, "trp_player"),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_state, sfai_default),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_object, -1),
           (troop_set_slot, "$supported_pretender", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_change_troop_renown", "$supported_pretender", 1000), #SB : keep existing renown
           (val_div, ":renown_loss", 2), #and add to it half of what old king lost
           (call_script, "script_change_troop_renown", "$supported_pretender", ":renown_loss"),
           # (troop_set_slot, "$supported_pretender", slot_troop_renown, 1000),

           (party_remove_members, "p_main_party", "$supported_pretender", 1),
           (call_script, "script_troop_set_title_according_to_faction", "$supported_pretender", "$g_notification_menu_var1"),
           (troop_set_auto_equip, "$supported_pretender",1), #SB : diplomacy suggestion: claimants
           (call_script, "script_set_player_relation_with_faction", "$g_notification_menu_var1", 12), #dckplmc
           (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
             (neq, ":cur_kingdom", "$g_notification_menu_var1"),
             (store_relation, ":reln", ":cur_kingdom", "fac_player_supporters_faction"),
             (set_relation, ":cur_kingdom", "$g_notification_menu_var1", ":reln"),
           (try_end),
           (assign, "$supported_pretender", 0),
           (assign, "$supported_pretender_old_faction", 0),
           (assign, "$g_recalculate_ais", 1),
           (call_script, "script_update_all_notes"),
         (try_end),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_rebels_switched_to_faction",0,
    "Rebellion Success^^ Your rebellion is victorious! Your faction now has the sole claim to the title of {s11}, with {s12} as the single ruler.",
    "none",
    [
      (str_store_faction_name, s11, "$g_notification_menu_var1"),
      (str_store_troop_name, s12, "$g_notification_menu_var2"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", npc_kingdoms_begin, kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
         (assign, "$talk_context", tc_rebel_thanks),
         (start_map_conversation, "$g_notification_menu_var2", -1),
         (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_should_consult",0,
##diplomacy start+ Replace "Your minister" with "{reg0?Your minister:{s11}}" and "him" with "{reg4?her:him}".
#Also "sends words" to "sends word"
    "{reg0?Your minister:{s11}} send word that there are problems brewing in the realm which, if left untreated, could sap your authority. You should consult with {reg4?her:him} at your earliest convenience",
	##diplomacy end+
    "none",
    [
      ],
    [
      ("continue",[],"Continue...",
       [
	    (setup_quest_text, "qst_consult_with_minister"),

        (str_store_troop_name, s11, "$g_player_minister"),
        (str_store_party_name, s12, "$g_player_court"),

		(str_store_string, s2, "str_consult_with_s11_at_your_court_in_s12"),
	    (call_script, "script_start_quest", "qst_consult_with_minister", -1),
		##diplomacy start+ Set minister gender and reg0 for generic vs specific
		(assign, reg4, 0),
		(try_begin),
			(call_script, "script_cf_dplmc_troop_is_female", "$g_player_minister"),
			(assign, reg4, 1),
		(try_end),
		(assign, reg0, 1),
		(try_begin),
			(is_between, "$g_player_minister", heroes_begin, heroes_end),
			(assign, reg0, 0),
		(try_end),
		##diplomacy end+

		(quest_set_slot, "qst_consult_with_minister", slot_quest_expiration_days, 30),
		(quest_set_slot, "qst_consult_with_minister", slot_quest_giver_troop, "$g_player_minister"),


	    (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_feast_in_progress",0,
##diplomacy start+ make gender correct
    "Feast in Preparation^^Your {wife/husband} has started preparations for a feast in your hall in {s11}",
##diplomacy end+
    "none",
    [
    (str_store_party_name, s11, "$g_notification_menu_var1"),
    ],
    [
      ("continue",[],"Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
  (
    "notification_lady_requests_visit",0, #add this once around seven days after the last visit, or three weeks, or three months
    "An elderly woman approaches your party and passes one of your men a letter, sealed in plain wax. It is addressed to you. When you break the seal, you see it is from {s15}. It reads, 'I so enjoyed your last visit. {s14} I am currently in {s10}.{s12}'",
    "none",
    [

      (assign, ":lady_no", "$g_notification_menu_var1"),
      (assign, ":center_no", "$g_notification_menu_var2"),

      (str_store_troop_name, s15, ":lady_no"),
      (str_store_party_name, s10, ":center_no"),

      (store_current_hours, ":hours_since_last_visit"),
      (troop_get_slot, ":last_visit_hours", ":lady_no", slot_troop_last_talk_time),
      (val_sub, ":hours_since_last_visit", ":last_visit_hours"),

      (call_script, "script_get_kingdom_lady_social_determinants", ":lady_no"),
      (assign, ":lady_guardian", reg0),

      (str_store_troop_name, s16, ":lady_guardian"),
      (call_script, "script_troop_get_family_relation_to_troop", ":lady_guardian", ":lady_no"),

      (str_clear, s14),
      (try_begin),
        (lt, ":hours_since_last_visit", 336),
        (try_begin),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_otherworldly),
            (str_store_string, s14, "str_as_brief_as_our_separation_has_been_the_longing_in_my_heart_to_see_you_has_made_it_seem_as_many_years"),
        (else_try),
            (str_store_string, s14, "str_although_it_has_only_been_a_short_time_since_your_departure_but_i_would_be_most_pleased_to_see_you_again"),
        (try_end),
      (else_try),
        (ge, ":hours_since_last_visit", 336),
        (try_begin),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_ambitious),
            (str_store_string, s14, "str_although_i_have_received_no_word_from_you_for_quite_some_time_i_am_sure_that_you_must_have_been_very_busy_and_that_your_failure_to_come_see_me_in_no_way_indicates_that_your_attentions_to_me_were_insincere_"),
        (else_try),
            (troop_slot_eq, ":lady_no", slot_lord_reputation_type, lrep_moralist),
            (str_store_string, s14, "str_i_trust_that_you_have_comported_yourself_in_a_manner_becoming_a_gentleman_during_our_long_separation_"),
        (else_try),
            (str_store_string, s14, "str_it_has_been_many_days_since_you_came_and_i_would_very_much_like_to_see_you_again"),
        (try_end),
      (try_end),


      (str_clear, s12),
      (str_clear, s18),
      ##diplomacy start+ Store gender in register for use below
      (assign, ":save_reg4", reg4),
      (call_script, "script_dplmc_store_troop_is_female_reg", ":lady_guardian", 4),
      ##diplomacy end+
      (try_begin),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 0),
        (str_store_string, s12, "str__you_should_ask_my_s11_s16s_permission_but_i_have_no_reason_to_believe_that_he_will_prevent_you_from_coming_to_see_me"),
        (str_store_string, s18, "str__you_should_first_ask_her_s11_s16s_permission"),
      (else_try),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, -1),
        (str_store_string, s12, "str__alas_as_we_know_my_s11_s16_will_not_permit_me_to_see_you_however_i_believe_that_i_can_arrange_away_for_you_to_enter_undetected"),
      (else_try),
        (troop_slot_eq, ":lady_guardian", slot_lord_granted_courtship_permission, 1),
        (str_store_string, s12, "str__as_my_s11_s16_has_already_granted_permission_for_you_to_see_me_i_shall_expect_your_imminent_arrival"),
      (try_end),
      ##diplomacy start+ Revert register
      (assign, reg4, ":save_reg4"),
      ##diplomacy end+

      #SB : add tableau for lady
      (set_fixed_point_multiplier, 100),
      (init_position, pos0),
      (position_set_x, pos0, 60),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_dplmc_lord_profile", ":lady_no", pos0),
      ],
    [

      ("continue",[],"Tell the woman to inform her mistress that you will come shortly",
       [

        (assign, ":lady_to_visit", "$g_notification_menu_var1"),
        (str_store_troop_name_link, s3, ":lady_to_visit"),
        (str_store_party_name_link, s4, "$g_notification_menu_var2"),

        (str_store_string, s2, "str_visit_s3_who_was_last_at_s4s18"),
        (call_script, "script_start_quest", "qst_visit_lady", ":lady_to_visit"),
        (quest_set_slot, "qst_visit_lady", slot_quest_giver_troop, ":lady_to_visit"), #don't know why this is necessary

        (try_begin),
            (eq, "$cheat_mode", 1),
            (quest_get_slot, ":giver_troop", "qst_visit_lady", slot_quest_giver_troop),
            (str_store_troop_name, s2, ":giver_troop"),
            (display_message, "str_giver_troop_=_s2"),
        (try_end),

        (quest_set_slot, "qst_visit_lady", slot_quest_expiration_days, 30),
        (change_screen_return),
        ]),

      ("continue",[],"Tell the woman to inform her mistress that you are indisposed",
       [
        (troop_set_slot, "$g_notification_menu_var1", slot_lady_no_messages, 1),
        (change_screen_return),
        ]),
     ]
  ),



  ( #pre lady visit
    "garden",0,
    "{s12}",
    "none",
    [

    (call_script, "script_get_kingdom_lady_social_determinants", "$love_interest_in_town"),
	(assign, ":guardian_lord", reg0),
	(str_store_troop_name, s11, "$love_interest_in_town"),

	(try_begin),
		(call_script, "script_npc_decision_checklist_male_guardian_assess_suitor", ":guardian_lord", "trp_player"),
		(lt, reg0, 0),
		(troop_set_slot, ":guardian_lord", slot_lord_granted_courtship_permission, -1),
	(try_end),

	(assign, "$nurse_assists_entry", 0),
	(try_begin),
		(troop_slot_eq, ":guardian_lord", slot_lord_granted_courtship_permission, 1),
		(str_store_string, s12, "str_the_guards_at_the_gate_have_been_ordered_to_allow_you_through_you_might_be_imagining_things_but_you_think_one_of_them_may_have_given_you_a_wink"),
	(else_try), #the circumstances under which the lady arranges for a surreptitious entry
		(call_script, "script_troop_get_relation_with_troop", "trp_player", "$love_interest_in_town"),
		(gt, reg0, 0),

		(assign, ":player_completed_quest", 0),
		(try_begin),
			(check_quest_active, "qst_visit_lady"),
			(quest_slot_eq, "qst_visit_lady", slot_quest_giver_troop, "$love_interest_in_town"),
			(assign, ":player_completed_quest", 1),
		(else_try),
			(check_quest_active, "qst_formal_marriage_proposal"),
			(quest_slot_eq, "qst_formal_marriage_proposal", slot_quest_giver_troop, "$love_interest_in_town"),
			(this_or_next|check_quest_succeeded, "qst_formal_marriage_proposal"),
				(check_quest_failed, "qst_formal_marriage_proposal"),
			(assign, ":player_completed_quest", 1),
		(else_try),
			(check_quest_active, "qst_duel_courtship_rival"),
			(quest_slot_eq, "qst_duel_courtship_rival", slot_quest_giver_troop, "$love_interest_in_town"),
			(this_or_next|check_quest_succeeded, "qst_duel_courtship_rival"),
				(check_quest_failed, "qst_duel_courtship_rival"),
			(assign, ":player_completed_quest", 1),
		(try_end),

		(try_begin),
			(store_current_hours, ":hours_since_last_visit"),
			(troop_get_slot, ":last_visit_time", "$love_interest_in_town", slot_troop_last_talk_time),
			(val_sub, ":hours_since_last_visit", ":last_visit_time"),
			(this_or_next|ge, ":hours_since_last_visit", 96), #at least four days
				(eq, ":player_completed_quest", 1),

			(try_begin),
				(is_between, "$g_encountered_party", towns_begin, towns_end),
				(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_don_this_dress_and_throw_the_hood_over_your_face_i_will_smuggle_you_inside_the_castle_to_meet_her_in_the_guise_of_a_skullery_maid__the_guards_will_not_look_too_carefully_but_i_beg_you_for_all_of_our_sakes_be_discrete"),
				(assign, "$nurse_assists_entry", 1),
			(else_try),
				(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_wait_for_a_while_by_the_spring_outside_the_walls_i_will_smuggle_her_ladyship_out_to_meet_you_dressed_in_the_guise_of_a_shepherdess_but_i_beg_you_for_all_of_our_sakes_be_discrete"),
				(assign, "$nurse_assists_entry", 2),
			(try_end),
		(else_try),
			(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter_however_as_you_walk_back_towards_your_lodgings_an_elderly_lady_dressed_in_black_approaches_you_i_am_s11s_nurse_she_whispers_urgently_her_ladyship_asks_me_to_say_that_yearns_to_see_you_but_that_you_should_bide_your_time_a_bit_her_ladyship_says_that_to_arrange_a_clandestine_meeting_so_soon_after_your_last_encounter_would_be_too_dangerous"),
		(try_end),
	(else_try),
		(str_store_string, s12, "str_the_guards_glare_at_you_and_you_know_better_than_to_ask_permission_to_enter"),
	(try_end),

	],
    [

	("enter",
	[
    (call_script, "script_get_kingdom_lady_social_determinants", "$love_interest_in_town"),
	(troop_slot_eq, reg0, slot_lord_granted_courtship_permission, 1)
	], "Enter",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),

	("nurse",
	[
    (eq, "$nurse_assists_entry", 1),
	], "Go with the nurse",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),


	("nurse",
	[
    (eq, "$nurse_assists_entry", 2),
	], "Wait by the spring",
	[
	(jump_to_menu, "mnu_town"),
	(call_script, "script_setup_meet_lady", "$love_interest_in_town", "$g_encountered_party"),
	]
	),

	("leave",
	[],
	"Leave",
	[(jump_to_menu, "mnu_town")]),

    ]


  ),


    (
    "kill_local_merchant_begin",0,
    "You spot your victim and follow him, observing as he turns a corner into a dark alley.\
 This will surely be your best opportunity to attack him.",
    "none",
    [
    ],
    [
      ("continue",[],"Continue...",
       [(set_jump_mission,"mt_back_alley_kill_local_merchant"),
        (party_get_slot, ":town_alley", "$qst_kill_local_merchant_center", slot_town_alley),
        (modify_visitors_at_site,":town_alley"),
        (reset_visitors),
        (set_visitor, 0, "trp_player"),
        (set_visitor, 1, "trp_local_merchant"),
        (jump_to_menu, "mnu_town"),
        (jump_to_scene,":town_alley"),
        (change_screen_mission),
        ]),
     ]
  ),


    (
    "debug_alert_from_s65",0,
    "DEBUG ALERT: {s65}",
    "none",
    [
    ],
    [
      ("continue",[],"Continue...",
       [
        (assign, "$debug_message_in_queue", 0),
        (change_screen_return),
        ]),
     ]
  ),
  (
    "notification_player_faction_political_issue_resolved",0,
    "After consulting with the peers of the realm, {s10} has decided to confer {s11} on {s12}.",
    "none",
    [
    (assign, ":faction_issue_resolved", "$g_notification_menu_var1"),
    (assign, ":faction_decision", "$g_notification_menu_var2"),
    (faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
    (str_store_troop_name, s10, ":leader"),
    (try_begin),
        (eq, ":faction_issue_resolved", 1),
        (str_store_string, s11, "str_the_marshalship"),
    (else_try),
        (str_store_party_name, s11, ":faction_issue_resolved"),
    (try_end),
    (str_store_troop_name, s12, ":faction_decision"),

    ],
    [
       ("continue",
       [],"Continue...",
       [
        (change_screen_return),
        ]),


    ]
  ),
  (
    "notification_player_faction_political_issue_resolved_for_player",0,
    "After consulting with the peers of the realm, {s10} has decided to confer {s11} on you. You may decline the honor, but it will probably mean that you will not receive other awards for a little while.{s12}",
    "none",
    [
    (faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
    (str_store_troop_name, s10, ":leader"),
    (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
    (try_begin),
        (eq, ":issue", 1),
        (str_store_string, s11, "str_the_marshalship"),
        (str_store_string, s12, "@^^Note that so long as you remain marshal, the lords of the realm will be expecting you to lead them on campaign. So, if you are awaiting a feast, either for a wedding or for other purposes, you may wish to resign the marshalship by speaking to your liege."),
    (else_try),
        (str_clear, s12),
        (str_store_party_name, s11, ":issue"),
    (try_end),
    ],
    [
       ("accept",
       [],"Accept the honor",
       [
        (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),

        (try_begin),
            (eq, ":issue", 1),
            (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
            (call_script, "script_appoint_faction_marshall", "$players_kingdom", "trp_player"),
            (unlock_achievement, ACHIEVEMENT_AUTONOMOUS_COLLECTIVE),
        (else_try),
            (call_script, "script_give_center_to_lord", ":issue", "trp_player", 0), #Zero means don't add garrison
        (try_end),

        (faction_set_slot, "$players_kingdom", slot_faction_political_issue, 0),
        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
            (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
            (eq, ":active_npc_faction", "$players_kingdom"),
            (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
        (try_end),
        (change_screen_return),
        ]),

       ("decline",
       [],"Decline the honor",
       [
        (faction_get_slot, ":issue", "$players_kingdom", slot_faction_political_issue),
        (try_begin),
            (is_between, ":issue", centers_begin, centers_end),
            (assign, "$g_dont_give_fief_to_player_days", 30),
        (else_try),
            (assign, "$g_dont_give_marshalship_to_player_days", 30),
        (try_end),

        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
            (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
            (eq, ":active_npc_faction", "$players_kingdom"),
            (troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
        (try_end),
        (change_screen_return),
        ]),
    ]
  ),
  ("notification_relieved_as_marshal", mnf_disable_all_keys,
    "{s4} wishes to inform you that your services as marshal are no longer required. In honor of valiant efforts on behalf of the realm over the last {reg4} days, however, {reg8?she:he} offers you a purse of {reg5} denars.",
    "none",
    [
	(assign, reg4, "$g_player_days_as_marshal"),



	(store_div, ":renown_gain", "$g_player_days_as_marshal",4),
	(val_min, ":renown_gain", 20),
	(store_mul, ":denar_gain", "$g_player_days_as_marshal", 50),
	(val_max, ":denar_gain", 200),
	(val_min, ":denar_gain", 4000),
	(troop_add_gold, "trp_player", ":denar_gain"),
	(call_script, "script_change_troop_renown", "trp_player", ":renown_gain"),
	(assign, "$g_player_days_as_marshal", 0),
	(assign, "$g_dont_give_marshalship_to_player_days", 15),
	(assign, reg5, ":denar_gain"),

	(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
	(str_store_troop_name, s4, ":faction_leader"),
	##diplomacy start+ get gender with script
	#(troop_get_type, reg8, ":faction_leader"),#<- OLD
	(assign, ":save_reg0", reg0),
	(call_script, "script_dplmc_store_troop_is_female", ":faction_leader"),
	(assign, reg8, reg0),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
	],

	 [
      ("continue",[],"Continue",
       [
         (change_screen_return),
       ]),
    ]
  ),


  ##diplomacy begin
########################################################
# Autoloot Game Menus Begin
########################################################

	##########################################################
	# Inventory allocation / Loot allocation Game Menu  -  by Fisheye
	# Parameters:
	# $return_menu : return to this menu after managing loot.  0 if this menu is called via random encounter
	##diplomacy start+
	#Added "return_menu", renaming it to "$dplmc_return_menu"
	##diplomacy end+
	("dplmc_manage_loot_pool", mnf_enable_hot_keys,
		"{s10}^{s30}",
		"none",
		[
			##diplomacy start+
			#Use a different troop!
			#(assign, "$pool_troop", "trp_dplmc_chamberlain"),
			(assign, "$pool_troop", "trp_temp_troop"),
			#Make sure things are initialized
			(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
			##diplomacy end+
			(assign, reg20,0),
			(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
			(try_for_range, ":i_slot", 0, ":inv_cap"),
				(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
				(ge, ":item_id", 0),
				(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
				(val_add, reg20, 1),
			(try_end),
			# reg20 now contains number of items in loot pool
			(try_begin),
				(eq, reg20, 0),
				(str_store_string, s10, "str_dplmc_item_pool_no_items"),
				(str_store_string, s20, "str_dplmc_item_pool_leave"),
			(else_try),
				(eq, reg20, 1),
				(str_store_string, s10, "str_dplmc_item_pool_one_item"),
				(str_store_string, s20, "str_dplmc_item_pool_abandon"),
			(else_try),
				(str_store_string, s10, "str_dplmc_item_pool_many_items"),
				(str_store_string, s20, "str_dplmc_item_pool_abandon"),
			(try_end),
		  ## CC
			(try_begin), #only show when we don't have equipment logs
              (str_is_empty, dplmc_loot_string),
			  (set_fixed_point_multiplier, 100),
              (position_set_x, pos0, 20),
              (position_set_y, pos0, 30),
              (position_set_z, pos0, 80),
			  (set_game_menu_tableau_mesh, "tableau_game_character_sheet", "$lord_selected", pos0),
			(try_end),
		  ## CC

          #SB : str30 shows items looted after script_dplmc_auto_loot_troop was called
          # (try_begin),
            # (neg|str_is_empty, dplmc_loot_string),
            # (str_store_string, s10, "@{s10}^^{s30}"),
          # (try_end),
		],
		[
			("dplmc_auto_loot",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(ge, ":space", 10),
					(gt, reg20, 0),
				],
				##diplomacy start+
				#"Let your heroes select gear from the item pool.",
				"Let your heroes select gear from the items on the ground.",
				##diplomacy end+
				[
					# (set_player_troop, "trp_player"),
					# (assign, "$lord_selected", "trp_player"),
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					##diplomacy end+
					(jump_to_menu, "mnu_dplmc_auto_loot")
				]
			),
			("dplmc_auto_loot_no",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(lt, ":space", 10),
					(disable_menu_option)
				],
				"Insufficient item pool space for auto-upgrade.",
				[]
			),
			("dplmc_loot",
				[],
				##diplomacy start+
				#"Access the item pool.",
				"Access the items on the ground.",
				##diplomacy end+
				[
					(change_screen_loot, "$pool_troop"),
				]
			),

            #SB : improve usability, if only change_screen_loot worked with the player
			("dplmc_loot_player",
				[(is_between, "$lord_selected", companions_begin, companions_end),],
				"Access the captain's inventory.",
                #can't use honorific, since the player troop is the companion and strings will be malformed
				[
					(set_player_troop, "trp_player"),
					(change_screen_equip_other, "$lord_selected"),
					(assign, "$lord_selected", "trp_player"),
				]
			),
      ("dplmc_auto_loot_upgrade_management", [],
##diplomacy start+
#        "Upgrade management of the NPC's equipments.",
         "Update management of NPCs' equipment.",
##diplomacy end+
        [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          ##nested diplomcy start+ Add error check.

          ##nested diplomacy end+
          (try_begin),
            (is_between, "$lord_selected", companions_begin, companions_end),
            (assign, "$temp", "$lord_selected"),
          (else_try),
            (assign, "$temp", -1),
            (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop", "p_main_party", ":stack_no"),
              (is_between, ":stack_troop", companions_begin, companions_end),
              (assign, "$temp", ":stack_troop"),
              (assign, ":num_stacks", 0),
            (try_end),
          (try_end),
          ##nested diplomacy start+   Add error check.
          (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
          (try_begin),#<- dplmc+ added
            (ge, "$temp", 1),#<- dplmc+ added
            (assign, "$temp_2", -1), #SB : other globals
            (try_for_range, ":item_slot", ek_item_0, ek_food),
              (troop_set_slot, "trp_stack_selection_ids", ":item_slot", 0),
            (try_end),
            (str_clear, dplmc_loot_string),
            (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
          (try_end),
          ##nested diplomacy end+
        ]
      ),

      #all other options will reset player eventually, this is for convenience
      ("dplmc_auto_loot_reset_player", [(neq, "$lord_selected", "trp_player")],
         "Reset current troop to the player",
        [
          (assign, "$lord_selected", "trp_player"),
          (set_player_troop, "$lord_selected"),
        ]
      ),
			("dplmc_leave",
				[],
				"{s20}",
				[
				##diplomacy start+
				#Actually abandon the lost loot
				(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
				(try_for_range, ":i_slot", 10, ":inv_cap"),
					(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					(ge, ":item_id", 0),
					(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					(troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #delete it
					(troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
				(try_end),

				#(jump_to_menu, "mnu_camp"),
				(set_player_troop, "trp_player"),
				(jump_to_menu, "$dplmc_return_menu"),
				(assign, "$pool_troop", -1), #mark ending
				##diplomacy end+
				]
			),
			##nested diplomacy start+
			#Leave & take everything you can
			("dplmc_leave_and_take_a",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(lt, ":space", reg20),
				(gt, reg20, 0),
				(gt, ":space", 0),
				(assign, reg0, ":space"),
				],
				"Gather {reg0} of the {reg20} items on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(troop_sort_inventory, "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item from pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					#(jump_to_menu, "mnu_camp"),
					(set_player_troop, "trp_player"),
					(jump_to_menu, "$dplmc_return_menu"),
					(assign, "$pool_troop", -1), #mark ending
				]
			),
			("dplmc_leave_and_take_b",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(ge, ":space", reg20),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(store_sub, reg0, reg20, 1),
				],
				"Gather the remaining {reg20} {reg0?items:item} on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item frlom pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					(set_player_troop, "trp_player"),
					(jump_to_menu, "$dplmc_return_menu"),
					(assign, "$pool_troop", -1), #mark ending
				]
			),
			("dplmc_leave_and_take_c",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(eq, ":space", 0),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(disable_menu_option),
				],
				"There is no space left in your bags.",
				[
				]
			),
			##nested diplomacy end+
		]
	),

	("dplmc_auto_loot",
		0,
##diplomacy start+
		"Your heroes will automatically grab items from the loot pool based on their pre-selected upgrade options. Heroes listed first in the party order will have first pick. Any equipment no longer needed will be dropped back into the loot pool. Any items in the loot pool will be lost when you leave.^ Are you sure you wish to do this?",
##diplomacy end+
		"none",
		[],
		[
			("dplmc_autoloot_no",
				[],
				"No, I've changed my mind.",
				[
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
			("dplmc_autoloot_yes",
				[],
				"Yes, perform the upgrading.",
				[
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					(assign, "$pool_troop", "trp_temp_troop"),
					#SB : reset variables
					(set_player_troop, "trp_player"),
					(assign, "$lord_selected", "trp_player"),
					##diplomacy end+
					(call_script, "script_dplmc_auto_loot_all", "trp_temp_troop", dplmc_loot_string),
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),

            #SB : individual looting
			("dplmc_autoloot_personal",
				[(is_between, "$lord_selected", companions_begin, companions_end),(str_store_troop_name, s1, "$lord_selected")],
				"Yes, only upgrade {s1}.",
				[
					##diplomacy start+
					(assign, "$pool_troop", "trp_temp_troop"),
					(call_script, "script_dplmc_auto_loot_troop", "$lord_selected", "$pool_troop", dplmc_loot_string),
					##diplomacy end+
					(jump_to_menu, "mnu_dplmc_manage_loot_pool"),
				]
			),
		]
	),
]
