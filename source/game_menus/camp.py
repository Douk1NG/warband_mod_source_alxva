# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_menus = [
  ("camp",mnf_scale_picture|mnf_enable_hot_keys,
   "You set up camp. What do you want to do?",
   "none",
   [
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

      ("camp_cheat",
       [(ge, "$cheat_mode", 1)
        ], "CHEAT MENU!",
       [(jump_to_menu, "mnu_camp_cheat"),
        ],
       ),

      ("camp_action",[],"Take an action.",
       [(jump_to_menu, "mnu_camp_action"),
        ]
       ),

      #("content_options",[],"Dickplomacy Reloaded Content Options.",[(jump_to_menu, "mnu_content_options")]), Not used anymore, as the mod now uses a presentation

		("dplmc_camp_preferences",
			[
			],
			"Settings", # Global options menu now
			[
				(jump_to_menu, "mnu_dplmc_preferences"),
				(assign, "$g_presentation_next_presentation", -1),
			]
		),

      ("camp_fuck_1",[(ge, "$cheat_mode", 1),(ge, "$g_sexual_content", 1)],"Fuck Test", # Even in cheat mode we should respect content preferances.
       [(jump_to_menu, "mnu_fuck"),
        ]
       ),

       ##diplomacy begin
###################################################################################
# Autoloot: Allow item management from camp
###################################################################################
##nested diplomacy start+
#Made some changes to autoloot conditions
	("dplmc_camp_manage_inventory",
		[
	  #OLD:
	  #(eq, "$g_autoloot", 1),
      #(store_skill_level, ":inv_skill", "skl_inventory_management", "trp_player"),
      #(gt, "$g_player_chamberlain", 0),
      #(ge, ":inv_skill", 3),
	  #NEW:
	  #1. Must have companions
	  #2. Either a hero in the party must have inventory management 3 or higher, or the player must have inventory management of 2 or higher, or the player or a hero in the party must have a looting skill of 2 or higher
	  (call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
	    ],
	  #"Manage your party's inventory.",
	  "Manage auto-loot settings.",
		[
			(try_begin),
				#dplmc+ Add check if autoloot has not been initialized yet
				(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
			(try_end),
			(troop_clear_inventory, "trp_temp_troop"),
			##diplomacy start+
			(assign, "$pool_troop", "trp_temp_troop"),
			(assign, "$dplmc_return_menu", "mnu_camp"),
			##diplomacy end+
			(assign, "$inventory_menu_offset", 0),
            #SB : variable resets
			(assign, "$lord_selected", "trp_player"),
            (str_clear, dplmc_loot_string),
			(jump_to_menu, "mnu_dplmc_manage_loot_pool")
		]
	),

#Alternate display: make it clear why autoloot isn't appearing
	("dplmc_camp_manage_inventory_disabled",
		[
	  #Print this when the player has companions but doesn't meet
	  #the minimum skill levels.
		(try_begin),
			(call_script, "script_cf_dplmc_player_party_meets_autoloot_conditions"),
		(try_end),
		(eq, reg0, 0),
		(disable_menu_option),
	    ],
	  "Auto-loot requires Inventory Management or Looting at rank 2.",
		[
		]
	),
##nested diplomacy end+ Finished changes to autoloot conditions
###################################################################################
# End Autoloot
###################################################################################

##diplomacy end

      ###(((manage_inventory
      ("camp_manage_inventory",[],"Manage your inventory.",
        [
          (assign, "$g_prsnt_param_1", "trp_player"),
          (start_presentation, "prsnt_manage_inventory"),
        ]),
      ###)))

      ("camp_action_1",[],"Walk around the campsite.", #dckplmc
       [(set_jump_mission,"mt_camp"),
        (call_script, "script_setup_camp_scene"),
        (change_screen_mission),
        ]
       ),

      ("camp_disembark", [(eq, "$g_player_icon_state", pis_ship),
        (party_get_position, pos1, "p_main_party"),
        (map_get_land_position_around_position, pos0, pos1, 3),
        (get_distance_between_positions_in_meters, ":dist", pos1, pos0),
        (lt, ":dist", 3),
      ], "Disembark.",
       [(assign, "$g_player_icon_state", pis_normal),
        (party_set_flags, "p_main_party", pf_is_ship, 0),
        (party_set_position, "p_main_party", pos0),
        (party_get_slot, ":ship_type", "p_main_party", slot_party_ship_type),
        (try_begin),
          (le, "$g_main_ship_party", 0),
          (set_spawn_radius, 0),
          (spawn_around_party, "p_main_party", "pt_none"),
          (assign, "$g_main_ship_party", reg0),
          (party_set_flags, "$g_main_ship_party", pf_is_static|pf_always_visible|pf_hide_defenders|pf_is_ship, 1),
          (str_store_troop_name, s1, "trp_player"),
          (party_set_slot, "$g_main_ship_party", slot_party_ship_type, ":ship_type"),
          (party_set_name, "$g_main_ship_party", "@{s1}'s Ship"),
          (party_set_icon, "$g_main_ship_party", "icon_ship"),
          (party_set_slot, "$g_main_ship_party", slot_party_type, spt_ship),

          (try_begin),
            (eq, ":ship_type", 1),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Longship"),
          (else_try),
            (eq, ":ship_type", 2),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Galley"),
          (else_try),
            (eq, ":ship_type", 3),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Cog"),
          (else_try),
            (eq, ":ship_type", 4),
            (party_set_name, "$g_main_ship_party", "@{s1}'s Dhow"),
          (try_end),

        (try_end),
        (enable_party, "$g_main_ship_party"),
        (party_set_position, "$g_main_ship_party", pos0),
        (party_set_icon, "$g_main_ship_party", "icon_ship_on_land"),
        (assign, "$g_main_ship_party", -1),
        (party_set_slot, "p_main_party", slot_party_ship_type, 0),
        (change_screen_return),
        ]),


      ("camp_wait_here",[],"Wait here for some time.",
       [
           (assign,"$g_camp_mode", 1),
           (assign, "$g_infinite_camping", 0),

           (try_begin),
             (neq, "$g_player_icon_state", pis_ship),
           (assign, "$g_player_icon_state", pis_camping),
           (try_end),

           (try_begin),
             (party_is_active, "p_main_party"),
             (party_get_current_terrain, ":cur_terrain", "p_main_party"),
             (try_begin),
               (eq, ":cur_terrain", rt_desert),
               (unlock_achievement, ACHIEVEMENT_SARRANIDIAN_NIGHTS),
             (try_end),
           (try_end),

           (rest_for_hours_interactive, 24 * 365, 5, 1), #rest while attackable

           (change_screen_return),
        ]
       ),

      ("resume_travelling",[],"Resume travelling.",
       [
           (change_screen_return),
        ]
       ),
      ]
  ),
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
  ),
  ("camp_cheat_adv",0,       # New menu for less used cheats, because old one ran out of space.
   "Select advanced cheat:", # Fancy name so they feel classy and elite, when in reality they're just never used.
   "none",
   [],
    [

      ("camp_cheat_weather",[], "Change weather..",
       [(jump_to_menu, "mnu_cheat_change_weather"),]
       ),

      ("camp_cheat_3",[],"{!}Update political notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_political_notes", ":hero"),
         (try_end),

         (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
           (call_script, "script_update_faction_political_notes", ":kingdom"),
         (try_end),
        ]
       ),

      ("camp_cheat_4",[],"{!}Update troop notes.",
       [
         (try_for_range, ":hero", active_npcs_begin, active_npcs_end),
           (troop_slot_eq, ":hero", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_update_troop_notes", ":hero"),
         (try_end),

         (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
           (call_script, "script_update_troop_notes", ":lady"),
           (call_script, "script_update_troop_political_notes", ":lady"),
           (call_script, "script_update_troop_location_notes", ":lady", 0),
         (try_end),
        ]
       ),

      ("cheat_faction_orders",[(ge,"$cheat_mode",1)],
	  "{!}Cheat: Set Debug messages to All.",
       [(assign,"$cheat_mode",1),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",3)],"{!}Cheat: Set Debug messages to Econ Only.",
       [(assign,"$cheat_mode",3),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),
      ("cheat_faction_orders",[
	  (ge, "$cheat_mode", 1),
	  (neq,"$cheat_mode",4)],"{!}Cheat: Set Debug messages to Political Only.",
       [(assign,"$cheat_mode",4),
         (jump_to_menu, "mnu_camp_cheat_adv"),
        ]
       ),

      ("to_simple_cheats",[],"{!}Simple Cheats",
		[
         (jump_to_menu, "mnu_camp_cheat"),
		]
       ),
      ("back_to_camp_menu",[],"{!}Back to camp menu.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
    ]
  ),
  ("cheat_find_item",0,
   "{!}Current item range: {reg5} to {reg6}",
   "none",
   [
     (assign, reg5, "$cheat_find_item_range_begin"),
     (store_add, reg6, "$cheat_find_item_range_begin", max_inventory_items),
     (val_min, reg6, "itm_items_end"),
     (val_sub, reg6, 1),
     ],
    [

    #SB : easier debug
      ("cheat_find_item_prev_range",[], "{!}Move to previous range.",
       [
        (val_sub, "$cheat_find_item_range_begin", max_inventory_items),
        (try_begin),
          (lt, "$cheat_find_item_range_begin", 0),
          (assign, "$cheat_find_item_range_begin", itm_items_end-max_inventory_items),
        (try_end),
        (jump_to_menu, "mnu_cheat_find_item"),
       ]
       ),

      ("cheat_find_item_next_range",[], "{!}Move to next item range.",
       [
        (val_add, "$cheat_find_item_range_begin", max_inventory_items),
        (try_begin),
          (ge, "$cheat_find_item_range_begin", "itm_items_end"),
          (assign, "$cheat_find_item_range_begin", 0),
        (try_end),
        (jump_to_menu, "mnu_cheat_find_item"),
       ]
       ),

       ("cheat_find_item_choose_this",[], "{!}Choose from this range.",
       [
        (troop_clear_inventory, "trp_find_item_cheat"),
        (store_add, ":max_item", "$cheat_find_item_range_begin", max_inventory_items),
        (val_min, ":max_item", "itm_items_end"),
        (store_sub, ":num_items_to_add", ":max_item", "$cheat_find_item_range_begin"),
        (try_begin), #SB : even more super-cheats
          (this_or_next|key_is_down, key_left_shift),
          (key_is_down, key_right_shift),
          (try_for_range, ":i_slot", 0, ":num_items_to_add"),
            (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
            (item_get_type, ":i_type", ":item_id"),
            (try_begin),
              (eq, ":i_type", itp_type_horse),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_champion),
            (else_try),
              (this_or_next|eq, ":i_type", itp_type_shield),
              (is_between, ":i_type", itp_type_head_armor, itp_type_pistol),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_lordly),
            (else_try),
              (this_or_next|is_between, ":i_type", itp_type_one_handed_wpn, itp_type_goods),
              (is_between, ":i_type", itp_type_pistol, itp_type_animal),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_masterwork),
            (else_try),
              (troop_add_item, "trp_find_item_cheat", ":item_id", imod_plain),
            (try_end),
          (try_end),
          (change_screen_loot, "trp_find_item_cheat"),
        (else_try), #Native behaviour
          (try_for_range, ":i_slot", 0, ":num_items_to_add"),
            (store_add, ":item_id", "$cheat_find_item_range_begin", ":i_slot"),
            (troop_add_items, "trp_find_item_cheat", ":item_id", 1),
          (try_end),
          (change_screen_trade, "trp_find_item_cheat"),
        (try_end),
       ]
       ),

      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),

   ("cheat_change_weather",0,
   "{!}Current cloud amount: {reg5}^Current Fog Strength: {reg6}",
   "none",
   [
     (get_global_cloud_amount, reg5),
     (get_global_haze_amount, reg6),
     ],
    [
      ("cheat_increase_cloud",[], "{!}Increase Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_add, ":cur_cloud_amount", 5),
		(val_min, ":cur_cloud_amount", 100),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_decrease_cloud",[], "{!}Decrease Cloud Amount.",
       [
	    (get_global_cloud_amount, ":cur_cloud_amount"),
		(val_sub, ":cur_cloud_amount", 5),
		(val_max, ":cur_cloud_amount", 0),
	    (set_global_cloud_amount, ":cur_cloud_amount"),
	   ]
       ),
      ("cheat_increase_fog",[], "{!}Increase Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_add, ":cur_fog_amount", 5),
		(val_min, ":cur_fog_amount", 100),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),
      ("cheat_decrease_fog",[], "{!}Decrease Fog Amount.",
       [
	    (get_global_haze_amount, ":cur_fog_amount"),
		(val_sub, ":cur_fog_amount", 5),
		(val_max, ":cur_fog_amount", 0),
	    (set_global_haze_amount, ":cur_fog_amount"),
	   ]
       ),

      ("camp_action_4",[],"{!}Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_action",0,
   "Choose an action:",
   "none",

   [
            (try_begin),
              (party_get_slot, ":player_party", "$marshalship"),
              (ge, ":player_party", 0),
              (set_fixed_point_multiplier, 100),
              (position_set_x, pos1, 70),
              (position_set_y, pos1, 5),
              (position_set_z, pos1, 75),
              (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", ":player_party", pos1),
              (try_end),

			 #custom armor #2/1
			 (call_script, "script_find_customizable_item_equipped_on_troop", "$g_player_troop"),
			 (assign, "$g_current_opened_troop_dthehun", "$g_player_troop"),
			 #
     ],
    [

      ("camp_recruit_prisoners",
       [(troops_can_join, 1),
        (store_current_hours, ":cur_time"),
        (val_sub, ":cur_time", 24),
        (gt, ":cur_time", "$g_prisoner_recruit_last_time"),
        (try_begin),
          (gt, "$g_prisoner_recruit_last_time", 0),
          (assign, "$g_prisoner_recruit_troop_id", 0),
          (assign, "$g_prisoner_recruit_size", 0),
          (assign, "$g_prisoner_recruit_last_time", 0),
        (try_end),
        ], "Recruit some of your prisoners to your party.",
       [(jump_to_menu, "mnu_camp_recruit_prisoners"),
        ],
       ),

      ("action_read_book",[],"Select a book to read.",
       [(jump_to_menu, "mnu_camp_action_read_book"),
        ]
       ),

      ("action_sort_inventory",[],"Sort player inventory.",
       [(jump_to_menu, "mnu_camp_action_sort_inventory"),
        ]
        ),

       #("queens_blade", [], "Queens blade options.",
       #[(jump_to_menu, "mnu_queens_blade"),
       # ],
       #),

	  #custom armor	#2/2
	  ("custom_armor",[
        (neq, "$g_current_opened_item_details", -1),
        (str_store_item_name, s0, "$g_current_opened_item_details"),
      ],"Customize {s0}",
        [
        (start_presentation, "prsnt_customize_armor"),
        ]),
	  #/custom armor

      ("action_food",[],"Change your party's food consumption habits.",
       [(start_presentation, "prsnt_food_options"),
        ]
       ),

      #SB : rename changes
      ("camp_change_name",[],"Change the name of your party.",
       [(assign, "$g_presentation_state", rename_party),
       (assign, "$g_encountered_party", "p_main_party"),
       (start_presentation, "prsnt_name_kingdom"),
       ]
       ),
       # #SB : recolor from CC, call this from other presentation
      # ("action_modify_factions_color",[],"Change the color of factions.",
       # [
          # (assign, "$g_presentation_state", recolor_kingdom),
          # (try_begin),
            # (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            # (store_sub, "$temp", "$players_kingdom", npc_kingdoms_begin),
            # (store_sub, "$temp", 8, "$temp"), #3 to 8 are npc kingdoms
          # (else_try),
            # (assign, "$temp", 9), #player faction
          # (try_end),
          # (start_presentation, "prsnt_change_color"),
        # ]
       # ),
      ("action_rename_kingdom",
       [
         #SB : use bits
         (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
         (eq, ":name_set", rename_kingdom),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
         ],"Rename your kingdom.",
       [
         #SB : explicitly state kingdom
         (assign, "$g_presentation_state", rename_kingdom),
         (start_presentation, "prsnt_name_kingdom"),
        ]
       ),
      # ("action_recolor_troops",
       # [
         # ],"Recolor your troop groups.",
       # [(assign, "$g_presentation_state", recolor_groups),
        # (jump_to_menu, "mnu_recolor_groups"),
        # ]
       # ),

      # ("action_rename_troops",
       # [
         # (gt, "$g_player_constable", 0),
         # (call_script, "script_cf_has_custom_troops"),
         # ],"Rename your custom troops.",
       # [
        # (jump_to_menu, "mnu_custom_troops"),
        # ]
       # ),
      ##diplomacy begin+
      ##Custom player kingdom vassal titles, credit Caba'drin start
       ("action_change_vassal_title",
        [
        #SB : allow action if co-ruler of $players_kingdom
          (assign, ":is_coruler", -1),
          (try_begin),
           (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
           (eq, ":name_set", rename_kingdom),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
            (assign, ":is_coruler", 1),
          (else_try),
            (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            (call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
            (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
            (assign, ":is_coruler", 1),
          (try_end),
          (eq, ":is_coruler", 1),
        ],"Change your vassals' title of nobility.",
        [(start_presentation, "prsnt_dplmc_set_vassal_title"),
        ]
       ),
       ("action_change_policies",
        [
            (gt, "$cheat_mode", 0),
            #SB : name set bits
            (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
            (eq, ":name_set", rename_kingdom),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
            (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        ],"{!}Cheat: Change kingdom policies",
        [(start_presentation, "prsnt_dplmc_policy_management"),

        ]
       ),
      ##Custom player kingdom vassal titles, credit Caba'drin end
      ##diplomacy end+
      ("action_modify_banner",[(eq, "$cheat_mode", 1)],"{!}Cheat: Modify your banner.",
       [
           #(start_presentation, "prsnt_banner_selection"),
           #(start_presentation, "prsnt_custom_banner"),
           (assign, "$g_edit_banner_troop", "trp_player"),
           (jump_to_menu, "mnu_choose_banner"),
        ]
       ),
      ("action_retire",[],"Retire from adventuring.",
       [(jump_to_menu, "mnu_retirement_verify"),
        ]
       ),
      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_recruit_prisoners",0,
   "You offer your prisoners freedom if they agree to join you as soldiers. {s18}",
   "none",
   [(assign, ":num_regular_prisoner_slots", 0),
    (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
    (try_for_range, ":cur_stack", 0, ":num_stacks"),
      (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
      # (neg|troop_is_hero, ":cur_troop_id"),
      #SB : use script check
      (call_script, "script_game_check_prisoner_can_be_sold", ":cur_troop_id"),
      (eq, reg0, 1),
      (val_add, ":num_regular_prisoner_slots", 1),
    (try_end),
    (try_begin),
      (eq, ":num_regular_prisoner_slots", 0),
      (jump_to_menu, "mnu_camp_no_prisoners"),
    (else_try),
      (eq, "$g_prisoner_recruit_troop_id", 0),
      (store_current_hours, "$g_prisoner_recruit_last_time"),
      (store_random_in_range, ":rand", 0, 100),
      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (store_sub, ":reject_chance", 15, ":persuasion_level"),
      (val_mul, ":reject_chance", 4),
      (try_begin),
        (lt, ":rand", ":reject_chance"),
        (assign, "$g_prisoner_recruit_troop_id", -7),
      (else_try),
        # (assign, ":num_regular_prisoner_slots", 0),
        # (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
        # (try_for_range, ":cur_stack", 0, ":num_stacks"),
          # (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          # (neg|troop_is_hero, ":cur_troop_id"),
          # (val_add, ":num_regular_prisoner_slots", 1),
        # (try_end),
        (store_random_in_range, ":random_prisoner_slot", 0, ":num_regular_prisoner_slots"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", "p_main_party", ":cur_stack"),
          (call_script, "script_game_check_prisoner_can_be_sold", ":cur_troop_id"),
          (eq, reg0, 1), #SB : use script call to prevent quest troops from being recruited
          (val_sub, ":random_prisoner_slot", 1),
          (lt, ":random_prisoner_slot", 0),
          (assign, ":num_stacks", 0),
          (assign, "$g_prisoner_recruit_troop_id", ":cur_troop_id"),
          (party_prisoner_stack_get_size, "$g_prisoner_recruit_size", "p_main_party", ":cur_stack"),
        (try_end),
      (try_end),

      (try_begin),
        (gt, "$g_prisoner_recruit_troop_id", 0),
        (party_get_free_companions_capacity, ":capacity", "p_main_party"),
        (val_min, "$g_prisoner_recruit_size", ":capacity"),
        (assign, reg1, "$g_prisoner_recruit_size"),
        (gt, "$g_prisoner_recruit_size", 0),
        (try_begin),
          (gt, "$g_prisoner_recruit_size", 1),
          (assign, reg2, 1),
        (else_try),
          (assign, reg2, 0),
        (try_end),
        (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (str_store_string, s18, "@{reg1} {s1} {reg2?accept:accepts} the offer."),
      (else_try),
        (str_store_string, s18, "@No one accepts the offer."),
      (try_end),
    (try_end),
    ],
    [
      ("camp_recruit_prisoners_accept",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Take them.",
       [(remove_troops_from_prisoners, "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        (party_add_members, "p_main_party", "$g_prisoner_recruit_troop_id", "$g_prisoner_recruit_size"),
        #SB : change base morale reduction by difficulty
        (game_get_reduce_campaign_ai, ":reduce"), #0 to 2
        (val_sub, ":reduce", 4), #-4 to -2
        (store_mul, ":morale_change", ":reduce", "$g_prisoner_recruit_size"),
        (store_troop_faction, ":troop_faction", "$g_prisoner_recruit_troop_id"),
        (store_character_level, ":troop_level", "$g_prisoner_recruit_troop_id"),

        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_set_slot, ":faction", slot_faction_temp_slot, 0),
        (try_end),
        (try_begin), #give extra penalty to faction morale if we recruit high-level enemy troops
          (this_or_next|eq, ":troop_faction", "fac_outlaws"),
          (eq, ":troop_faction", "fac_deserters"),
          (call_script, "script_objectionable_action", tmt_aristocratic, "str_hire_deserters"),
        (else_try),
          (is_between, ":troop_faction", npc_kingdoms_begin, npc_kingdoms_end),
          # (store_character_level, ":relation", "$g_prisoner_recruit_troop_id"),
          (try_begin), #check culture
            (eq, "$players_kingdom", "fac_player_supporters_faction"),
            (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
            (eq, "$g_player_culture", ":troop_faction"),
            (assign, ":troop_faction", "$players_kingdom"),
          (try_end),
          (try_begin), #no penalty for same faction
            (eq, ":troop_faction", "$players_kingdom"),
            # (val_sub, ":relation", ":morale_change"), #bonus
            (assign, ":morale_change", 0),
            (assign, "$g_prisoner_recruit_troop_id", 0),
            (assign, "$g_prisoner_recruit_size", 0),
          (else_try), #one point per offended party
            (party_get_num_companion_stacks, ":cap", "p_main_party"),
            (try_for_range, ":stack", 1, ":cap"),
              (party_stack_get_troop_id, ":troop", "p_main_party", ":stack"),
              # (neg|troop_is_hero, ":troop"),
              # (neq, ":troop", "$g_prisoner_recruit_troop_id"), #not just recruited
              (store_faction_of_troop, ":stack_faction", ":troop"),
              # (neq, ":stack_faction", ":troop_faction"),
              (store_relation, ":faction_relation", ":troop_faction", ":stack_faction"),
              (lt, ":faction_relation", 0),
              (faction_get_slot, ":amount", ":stack_faction", slot_faction_temp_slot),
              (party_stack_get_size, ":reduce", "p_main_party", ":stack"),
              (val_sub, ":amount", ":reduce"),
              (faction_set_slot, ":stack_faction", slot_faction_temp_slot, ":amount"),
            (try_end),
          (try_end),
        (try_end),
        (call_script, "script_change_player_party_morale", ":morale_change"),
        (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
          (faction_get_slot, ":relation", ":faction", slot_faction_temp_slot),
          (neq, ":relation", 0),
          (val_sub, ":relation", ":troop_level"),
          (call_script, "script_change_faction_troop_morale", ":faction", ":relation", 1),
        (try_end),
        (jump_to_menu, "mnu_camp"),
        ]
       ),
      ("camp_recruit_prisoners_reject",[(gt, "$g_prisoner_recruit_troop_id", 0)],"Reject them.",
       [(jump_to_menu, "mnu_camp"),
        (assign, "$g_prisoner_recruit_troop_id", 0),
        (assign, "$g_prisoner_recruit_size", 0),
        ]
       ),
      ("continue",[(le, "$g_prisoner_recruit_troop_id", 0)],"Go back.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_no_prisoners",0,
   "You have no prisoners to recruit from.",
   "none",
   [],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),

#This is the menu for the Universal Inventory Sorting Script
    ("camp_action_sort_inventory",0,
     "Choose what to sort by.",
     "none",
     [
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
        ("camp_sort_by_cost",
         [], "Sort inventory by cost.",
         [
         (call_script, "script_rearrange_inventory","trp_player", 1),
         (display_message, "@Your inventory is now sorted by cost."),
         ],
         ),

        ("camp_sort_by_type",
         [], "Sort inventory by type.",
         [
        (call_script, "script_rearrange_inventory","trp_player", 2),
        (display_message, "@Your inventory is now sorted by type."),
        ]
       ),
       ("camp_sort_leave_to_menu",[],"Back to camp menu.",
        [(jump_to_menu, "mnu_camp"),
        ]
       ),
     ]
  ),
  #End Menu,
  ("camp_action_read_book",0,
   "Choose a book to read:",
   "none",
   [],
    [
      ("action_read_book_1",[(player_has_item, "itm_book_tactics"),
                             (item_slot_eq, "itm_book_tactics", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_tactics"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_tactics"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_2",[(player_has_item, "itm_book_persuasion"),
                             (item_slot_eq, "itm_book_persuasion", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_persuasion"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_persuasion"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_3",[(player_has_item, "itm_book_leadership"),
                             (item_slot_eq, "itm_book_leadership", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_leadership"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_leadership"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_4",[(player_has_item, "itm_book_intelligence"),
                             (item_slot_eq, "itm_book_intelligence", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_intelligence"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_intelligence"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_5",[(player_has_item, "itm_book_trade"),
                             (item_slot_eq, "itm_book_trade", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_trade"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_trade"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_6",[(player_has_item, "itm_book_weapon_mastery"),
                             (item_slot_eq, "itm_book_weapon_mastery", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_weapon_mastery"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_weapon_mastery"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("action_read_book_7",[(player_has_item, "itm_book_engineering"),
                             (item_slot_eq, "itm_book_engineering", slot_item_book_read, 0),
                             (str_store_item_name, s1, "itm_book_engineering"),
                             ],"{s1}.",
       [(assign, "$temp", "itm_book_engineering"),
        (jump_to_menu, "mnu_camp_action_read_book_start"),
        ]
       ),
      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("camp_action_read_book_start",0,
   "{s1}",
   "none",
   [(assign, ":new_book", "$temp"),
    (str_store_item_name, s2, ":new_book"),
    (try_begin),
      (store_attribute_level, ":int", "trp_player", ca_intelligence),
      (item_get_slot, ":int_req", ":new_book", slot_item_intelligence_requirement),
      (le, ":int_req", ":int"),
      (str_store_string, s1, "@You start reading {s2}. After a few pages,\
 you feel you could learn a lot from this book. You decide to keep it close by and read whenever you have the time."),
      (assign, "$g_player_reading_book", ":new_book"),
    (else_try),
      (str_store_string, s1, "@You flip through the pages of {s2}, but you find the text confusing and difficult to follow.\
 Try as you might, it soon gives you a headache, and you're forced to give up the attempt."),
    (try_end),],
    [
      ("continue",[],"Continue...",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("retirement_verify",0,
   "You are at day {reg0}. Your current luck is {reg1}. Are you sure you want to retire?",
   "none",
   [
     (store_current_day, reg0),
     (assign, reg1, "$g_player_luck"),
     ],
    [
      ("retire_yes",[],"Yes.",
       [
         (start_presentation, "prsnt_retirement"),
        ]
       ),
      ("retire_no",[],"No.",
       [
         (jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  ),
  ("end_game",0,
   "The decision is made, and you resolve to give up your adventurer's\
 life and settle down. You sell off your weapons and armour, gather up\
 all your money, and ride off into the sunset....",
   "none",
   [],
    [
      ("end_game_bye",[],"Farewell.",
       [
         (change_screen_quit),
        ]
       ),
      ]
  ),
]
