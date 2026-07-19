# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_menu = [
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
  )
]
