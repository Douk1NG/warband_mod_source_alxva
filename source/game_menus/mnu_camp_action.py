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
      ("action_modify_factions_color",[],"Change the color of factions.",
       [
          (assign, "$temp", 4),
          (start_presentation, "prsnt_cc_color_editor"),
       ]
       ),
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
  )
]
