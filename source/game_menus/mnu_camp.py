# ======================================================================
# SHARED DEPENDENCY
# Entity: camp (menu)
# Called by menus in 4 domains: camp, cheats, dickplomacy, diplomacy
# ======================================================================

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
        ], "Cheat menu.",
       [(jump_to_menu, "mnu_camp_cheat"),
        ],
       ),

      ("dplmc_camp_preferences",
        [],
        "Settings",
        [
            (jump_to_menu, "mnu_dplmc_preferences"),
            (assign, "$g_presentation_next_presentation", -1),
        ]
      ),

      ("camp_action",[],"Take an action.",
       [(jump_to_menu, "mnu_camp_action"),
        ]
      ),

      ("camp_walk",[],"Walk around the campsite.",
       [(set_jump_mission,"mt_camp"),
        (call_script, "script_setup_camp_scene"),
        (change_screen_mission),
        ]
       ),

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
           (rest_for_hours_interactive, 24 * 365, 5, 1),
           (change_screen_return),
        ]
       ),

      ("camp_reveal_hideouts",
       [],
       "Reveal all bandit hideouts on map.",
        [
            # Reveal remaining lairs
           (assign, ":revealed", 0),
           (try_for_parties, ":camp"),
               (gt, ":camp", "p_spawn_points_end"),
               (party_get_template_id, ":template", ":camp"),
               (is_between, ":template", "pt_steppe_bandit_lair", "pt_bandit_lair_templates_end"),
               (party_set_flags, ":camp", pf_disabled, 0),
               (party_set_flags, ":camp", pf_always_visible, 1),
               (val_add, ":revealed", 1),
           (try_end),
           (assign, reg0, ":revealed"),
           (display_message, "@{!}Revealed {reg0} bandit hideout(s) on the map."),
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
