# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_cheats_2_menu = [
(
    "town_cheats_2",0,
    "Select an option to interact with the center itself. Prosperity is {reg1}, Relation is {reg2}, there are {reg3} parties in town.",
    "none",[
        (call_script, "script_set_town_picture"),
        (party_get_slot, reg1, "$current_town", slot_town_prosperity),
        (party_get_slot, reg2, "$current_town", slot_center_player_relation),

        (assign, ":count", 0),
        (try_for_parties, ":party_no"),
          (party_is_active, ":party_no"),
          (party_is_in_town, ":party_no", "$current_town"),
          (val_add, ":count", 1),
        (try_end),
        (assign, reg3, ":count"),
      ],
      [
          ("page",
          [],
          "Previous Page.",
          [
            (jump_to_menu, "mnu_town_cheats"),
          ]),

          ("toggle_state",
          [(party_slot_eq, "$current_town", slot_party_type, spt_village),
           (party_get_slot, reg1, "$current_town", slot_village_state),],
          "{reg1?Restore:Raze} this village.",
          [
            (try_begin),
              (party_slot_eq, "$current_town", slot_village_state, svs_normal),
              (call_script, "script_village_set_state", "$current_town", svs_looted),
            (else_try),
              (call_script, "script_village_set_state", "$current_town", svs_normal),
            (try_end),
          ]),

          ("village_manage",
          [], "Manage this center.",
          [
           (assign, "$g_next_menu", "mnu_town_cheats_2"),
           (jump_to_menu, "mnu_center_manage"),
          ]),
          ("increase_rel",
          [],
          "Increase Relation.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_player_relation_with_center", "$current_town", 1),
            (else_try),
              (call_script, "script_change_player_relation_with_center", "$current_town", 5),
            (try_end),
          ]),

          ("decrease_rel",
          [],
          "Decrease Relation.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_player_relation_with_center", "$current_town", -1),
            (else_try),
              (call_script, "script_change_player_relation_with_center", "$current_town", -5),
            (try_end),
          ]),

          ("increase_prosp",
          [],
          "Increase Prosperity.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_center_prosperity", "$current_town", 1),
            (else_try),
              (call_script, "script_change_center_prosperity", "$current_town", 5),
            (try_end),
          ]),

          ("decrease_prosp",
          [],
          "Decrease Prosperity.",
          [
            (try_begin),
              (this_or_next|key_is_down, key_left_shift),
              (key_is_down, key_right_shift),
              (call_script, "script_change_center_prosperity", "$current_town", -1),
            (else_try),
              (call_script, "script_change_center_prosperity", "$current_town", -5),
            (try_end),
          ]),

          ("castle_cheat_interior",
          [(neg|party_slot_eq, "$current_town", slot_party_type, spt_village)],
          "{!}Interior.",
          [
            (set_jump_mission,"mt_ai_training"),
            (party_get_slot, ":castle_scene", "$current_town", slot_town_castle),
            (jump_to_scene,":castle_scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_town_exterior",
          [],
          "{!}Exterior.",
          [
            # (try_begin),
              # (party_slot_eq, "$current_town",slot_party_type, spt_castle),
              # (party_get_slot, ":scene", "$current_town", slot_castle_exterior),
            # (else_try),
              # (party_get_slot, ":scene", "$current_town", slot_town_center),
            # (try_end),
            (party_get_slot, ":scene", "$current_town", slot_town_center),
            (set_jump_mission,"mt_ai_training"),
            (jump_to_scene,":scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_dungeon",
          [(neg|party_slot_eq, "$current_town", slot_party_type, spt_village)],
          "{!}Prison.",
          [
            (set_jump_mission,"mt_ai_training"),
            (party_get_slot, ":castle_scene", "$current_town", slot_town_prison),
            (jump_to_scene,":castle_scene"),
            (change_screen_mission),
          ]),

          ("castle_cheat_town_walls",
          [
            (party_slot_eq,"$current_town",slot_party_type, spt_town),
          ],
          "{!}Town Walls.",
          [
            (party_get_slot, ":scene", "$current_town", slot_town_walls),
            (set_jump_mission,"mt_ai_training"),
            (jump_to_scene,":scene"),
            (change_screen_mission),
          ]),

          ("cheat_town_start_siege",
          [ (neg|party_slot_eq, "$current_town", slot_party_type, spt_village),
            (party_slot_eq, "$g_encountered_party", slot_center_is_besieged_by, -1),
            (lt, "$g_encountered_party_2", 1),
            # (call_script, "script_party_count_fit_for_battle","p_main_party"),
            # (gt, reg(0), 1),
            # (try_begin),
              # (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
              # (assign, reg6, 1),
            # (else_try),
              # (assign, reg6, 0),
            # (try_end),
          ],
          "Besiege the center...",
          [
            (assign,"$g_player_besiege_town","$g_encountered_party"),
            (jump_to_menu, "mnu_castle_besiege"),
          ]),

          ("center_reports",
          [],
          "Show reports.",
          [
            (jump_to_menu,"mnu_center_reports"),
          ]),

          ("sail_from_port",
          [
            (party_slot_eq,"$current_town",slot_party_type, spt_town),
            (party_get_position, pos1, "$current_town"),
            (map_get_water_position_around_position, pos2, pos1, 8),
            (get_distance_between_positions_in_meters, ":dist", pos1, pos2),
            (lt, ":dist", 8),
            # (party_set_position, "p_main_party", pos2),
            # (ge, "$cheat_mode", 1),
            #(party_slot_eq,"$current_town",slot_town_near_shore, 1),
          ],
          "{!}Sail from port.",
          [
            (assign, "$g_player_icon_state", pis_ship),
            (party_set_flags, "p_main_party", pf_is_ship, 1),
            # (party_get_position, pos1, "p_main_party"),
            # (map_get_water_position_around_position, pos2, pos1, 6),
            (party_set_position, "p_main_party", pos2),
            (assign, "$g_main_ship_party", -1),
            (change_screen_return),
          ]),


          ("go_back",
          [(neg|party_slot_eq,"$current_town",slot_party_type, spt_village),],
          "Go Back.",
          [
            (jump_to_menu,"mnu_town"),
          ]),

          ("continue",
          [(party_slot_eq,"$current_town",slot_party_type, spt_village),],
          "Continue.",
          [
            (jump_to_menu,"mnu_village"),
          ]),
      ]
    )
]
