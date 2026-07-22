# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

camp_action_menu = [
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

      ("camp_manage_inventory",[],"Manage your inventory.",
        [
          (assign, "$g_prsnt_param_1", "trp_player"),
          (assign, "$g_selected_troop", "trp_player"),
          (start_presentation, "prsnt_equip_npcs"),
        ]),

      ("camp_autoloot",[],"Configure autoloot for heroes.",
        [
          (assign, "$g_selected_troop", "trp_player"),
          (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
        ]),

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

      ("custom_armor",[
        (neq, "$g_current_opened_item_details", -1),
        (str_store_item_name, s0, "$g_current_opened_item_details"),
      ],"Customize {s0}",
        [
        (start_presentation, "prsnt_customize_armor"),
        ]),

      ("action_food",[],"Change your party's food consumption habits.",
       [(start_presentation, "prsnt_food_options"),
        ]
       ),

      ("camp_change_name",[],"Change the name of your party.",
       [(assign, "$g_presentation_state", rename_party),
       (assign, "$g_encountered_party", "p_main_party"),
       (start_presentation, "prsnt_name_kingdom"),
       ]
       ),

      ("action_rename_kingdom",
       [
         (store_and, ":name_set", "$players_kingdom_name_set", rename_kingdom),
         (eq, ":name_set", rename_kingdom),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
         (faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
         ],"Rename your kingdom.",
       [
         (assign, "$g_presentation_state", rename_kingdom),
         (start_presentation, "prsnt_name_kingdom"),
        ]
       ),

       ("action_change_vassal_title",
        [
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

      ("action_retire",[],"Retire from adventuring.",
       [(jump_to_menu, "mnu_retirement_verify"),
        ]
       ),

      ("camp_action_4",[],"Back to camp menu.",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
