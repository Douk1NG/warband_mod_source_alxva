# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_cheat_menu = [
("camp_cheat",0,
   "Select a cheat:",
   "none",
   [ # Character preview
     (try_begin),
       (neq, "$g_player_icon_state", pis_ship),
     (assign, "$g_player_icon_state", pis_normal),
        (party_get_slot, ":player_party", "$marshalship"),
        (ge, ":player_party", 0),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, 70),
        (position_set_y, pos1, 5),
        (position_set_z, pos1, 75),
        (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
        (try_end),
    ],
    [
      ("camp_cheat_find_item",[], "Find an item...",
       [(jump_to_menu, "mnu_cheat_find_item"),]
       ),

      ("camp_cheat_0",[],"{!}Increase player RTR.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_player_right_to_rule", 25),
          (else_try),
            (call_script, "script_change_player_right_to_rule", 3),
          (try_end),
        ]
       ),

      ("camp_cheat_1",[],"{!}Increase player renown.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_troop_renown", "trp_player", 500),
          (else_try),
            (call_script, "script_change_troop_renown", "trp_player", 100),
          (try_end),
        ]
       ),

      ("camp_cheat_2",[],"{!}Increase player honor.",
       [
          (try_begin),
            (this_or_next|key_is_down, key_left_shift),
            (key_is_down, key_right_shift),
            (call_script, "script_change_player_honor", 50),
          (else_try),
            (call_script, "script_change_player_honor", 5),
          (try_end),
        ]
       ),

        ("gender_change", [], "Change player gender",
         #This part of the mod could not be added to the presentation properly. It just changes the gender, so you can't really make it a drop down.
        [(store_sub, "$character_gender", 1, "$character_gender"),
         (troop_set_type, "trp_player", "$character_gender"),
         (display_message, "@Your gender has been changed!"),
         ]
        ),

       #SB : update tavern npcs
      ("camp_cheat_5",[],"{!}Scramble taverngoers.",
       [
        (try_for_range, ":slots", slot_center_ransom_broker, slot_center_tavern_minstrel + 1),
          (neq, ":slots", slot_center_traveler_info_faction),
          #initialize
          (try_for_range, ":towns", towns_begin, towns_end),
            (party_set_slot, ":towns", ":slots", -1),
          (try_end),

          (try_begin), #parse
            (eq, ":slots", slot_center_ransom_broker),
            (assign, ":start", ransom_brokers_begin),
            (assign, ":end", ransom_brokers_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_traveler),
            (assign, ":start", tavern_travelers_begin),
            (assign, ":end", tavern_travelers_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_minstrel),
            (assign, ":start", tavern_minstrels_begin),
            (assign, ":end", tavern_minstrels_end),
          (else_try),
            (eq, ":slots", slot_center_tavern_bookseller),
            (assign, ":start", tavern_booksellers_begin),
            (assign, ":end", tavern_booksellers_end),
          (try_end),

          #populate
          (assign, ":num_towns", 0),
          (str_store_string, s51, "@nowhere in particular"),
          (try_for_range, ":troop_no", ":start", ":end"),
            (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
            (store_random_in_range, ":town_no", towns_begin, towns_end),

            (try_begin), #ensure no overlaps
              (party_slot_ge, ":town_no", ":slots", ":start"),
              # (assign, ":limit", towns_end),
              # (try_for_range, ":center_no", towns_begin, ":limit"),
                # (assign, ":town_used", 0),
                # (try_for_range, ":other_troop", ":start", ":troop_no"),
                  # (troop_slot_eq, ":other_troop", slot_troop_cur_center, ":center_no"),
                  # (assign, ":town_used", 1),
                # (try_end),
                # (eq, ":town_used", 0), #no other troop uses this slot
                # (party_set_slot, ":center_no", ":slots", ":troop_no"),
                # (assign, ":limit", 1),
              # (try_end),
            (else_try),
              (val_add, ":num_towns", 1),
              (str_store_party_name_link, s50, ":town_no"),
              (party_set_slot, ":town_no", ":slots", ":troop_no"),
              (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
              (try_begin),
                (eq, ":num_towns", 1),
                (str_store_string, s51, s50),
              (else_try),
                (str_store_string, s51, "str_s50_comma_s51"),
              (try_end),
            (try_end),
          (try_end),
          (str_store_troop_name_plural, s10, ":start"), #default titles "book_merchant" "ransom_broker" etc
          (str_store_string_reg, s11, s51),
          (display_message, "@You can find {s10}s at {s11}."),
        (try_end),
        (call_script, "script_update_mercenary_units_of_towns"), #might as well
        ]
       ),

      ("camp_cheat_6",[],"{!}Infinite camp",
       [
         (assign,"$g_camp_mode", 1),
         (assign, "$g_infinite_camping", 1),
         (assign, "$g_player_icon_state", pis_camping),
         (rest_for_hours_interactive, 10 * 24 * 365, 20), #10 year rest while not attackable with 20x speed
         (change_screen_return),
        ]
       ),

	   ##nested diplomacy start+
	  ("camp_cheat_7",[(troop_slot_ge, "trp_player", slot_troop_spouse, 1),],"{!}Divorce player spouse",
       [
	 	 (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
        #set this before the loop below, to avoid potential wierdness in the family relation check
		 (troop_set_slot, ":spouse", slot_troop_spouse, -1),
	     (troop_set_slot, "trp_player", slot_troop_spouse, -1),

		#apply relation loss with the spouse
		 (call_script, "script_change_player_relation_with_troop", ":spouse", -40),
	    #change relations with family - inverse of gain from marriage
		(try_for_range, ":family_member", heroes_begin, heroes_end),
		    (neq, ":family_member", ":spouse"),
			(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":spouse", ":family_member"),
			(gt, reg0, 0),
			(val_mul, reg0, -2),
			(val_div, reg0, 3),
			(val_min, reg0, -1),
			(call_script, "script_change_player_relation_with_troop", ":family_member", reg0),
		(try_end),
        ]
       ),
	   ##nested diplomacy end+

      ("camp_cheat_heal",[],"Heal party.",
       [
         (heal_party, "p_main_party"),
        ]
       ),
      ("camp_cheat_xp",[],"Add xp to party.",
       [
         (set_show_messages, 0),
         (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
         (try_for_range, ":stack", 0, ":num_stacks"), #include player if too lazy to ctrl+x
            (party_stack_get_troop_id, ":id", "p_main_party", ":stack"),
            (try_begin),
                # (troop_is_hero, ":id"),
                # (store_character_level, ":level", ":id"),
                # (get_level_boundary, ":xp", ":level"),
                # (troop_get_xp, ":cur_exp", ":id"),
                # (val_sub, ":xp", ":cur_exp"),
                # (add_xp_to_troop, ":xp", ":id"),
            # (else_try),
                (party_stack_get_size, ":size", "p_main_party", ":stack"),
                (call_script, "script_game_get_upgrade_xp", ":id"),
                (store_mul, ":xp", reg0, ":size"),
                (try_begin),
                  (troop_is_hero, ":id"),
                  # (troop_get_xp, ":cur_exp", ":id"),
                  # (val_sub, ":xp", ":cur_exp"),
                  (store_character_level, ":level", ":id"),
                  ##this is so stupid but it works (probably), but add_xp_to_troop caps out at 29999
                  (assign, ":end", 100),
                  (try_begin), #assign block of exp
                    (le, ":level", 10),
                    (assign, ":xp", 100),
                  (else_try),
                    (le, ":level", 25),
                    (assign, ":xp", 1000),
                  (else_try), #most people stop before level 30
                    (le, ":level", 35),
                    (assign, ":xp", 10000),
                  (else_try),
                    (le, ":level", 50),
                    (assign, ":xp", 30000),
                  (else_try),
                    (le, ":level", 60),
                    (assign, ":xp", 1000000),
                  (else_try), #good luck, level caps at 63
                    (assign, ":xp", 10000000),
                  (try_end),
                  # (val_mul, ":xp", ":level"),
                  (try_for_range, ":unused", 0, ":end"),
                    (party_add_xp_to_stack, "p_main_party", ":stack", ":xp"),
                    (add_xp_to_troop, 1, ":id"), #this actually upgrades the level
                    # (add_xp_as_reward, ":xp"),
                    (store_character_level, ":cur_level", ":id"),
                    (lt, ":level", ":cur_level"), #done
                    (assign, ":end", 0),
                  (try_end),
                (else_try),
                  (party_add_xp_to_stack, "p_main_party", ":stack", ":xp"),
                (try_end),
            (try_end),
         (try_end),
         (set_show_messages, 1),
         # (party_upgrade_with_xp, "p_main_party", 1, 0), #random upgrade - disabled
         # (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),
      ("camp_cheat_prisoner",[
          (party_get_num_prisoner_stacks, ":stack", "p_main_party"),
          (gt, ":stack", 0),
          (try_for_range, ":i_stack", 0, ":stack"),
            (party_prisoner_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
            (neg|troop_is_hero, ":troop"),
            (assign, ":stack", 0),
          (try_end),
          (eq, ":stack", 0), #found one non-hero entity
      ],"Recruit all prisoners.",
       [ # (call_script, "script_party_add_party_prisoners"),
         # (call_script, "script_party_remove_all_prisoners"),
         (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
         (try_for_range_backwards, ":stack", 0, ":num_stacks"),
            (party_prisoner_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
            (neg|troop_is_hero, ":troop"),
            (gt, ":troop", 0),
            (party_prisoner_stack_get_size, ":amount", "p_main_party", ":stack"),
            (party_remove_prisoners, "p_main_party", ":troop", ":amount"),
            (party_add_members, "p_main_party", ":troop", ":amount"),
         (try_end),
         # (jump_to_menu, "mnu_camp_cheat"),
        ]
       ),

      ("to_advanced_cheats",[],"{!}Advanced Cheats",
		[
         (jump_to_menu, "mnu_camp_cheat_adv"),
		]
       ),

      ("back_to_camp_menu",[],"{!}Back to camp menu.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
