# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

fuck_encounter_menu = [
(
    "fuck_encounter",0,
    "Continue",
    "none",
    [
        # (troop_set_slot, "trp_temp_array_a", 0, "trp_player"),
        # (troop_set_slot, "trp_temp_array_b", 0, -1),
        # (troop_set_slot, "trp_temp_array_a", 1, "$g_talk_troop"),
        # (troop_set_slot, "trp_temp_array_b", 1, ":dna"),
        # (store_random_in_range, ":r", 0, 2),
        # (assign, "$g_sex_position", ":r"),

          (party_get_current_terrain, ":terrain_type", "p_main_party"),
          (assign, ":scene_to_use", "scn_camp_scene_plain"),
          (try_begin),
            (this_or_next|eq, ":terrain_type", rt_steppe),
            (eq, ":terrain_type", rt_steppe_forest),
            (assign, ":scene_to_use", "scn_camp_scene_steppe"),
          (else_try),
            (this_or_next|eq, ":terrain_type", rt_plain),
            (eq, ":terrain_type", rt_forest),
            (assign, ":scene_to_use", "scn_camp_scene_plain"),
          (else_try),
            (this_or_next|eq, ":terrain_type", rt_snow),
            (eq, ":terrain_type", rt_snow_forest),
            (assign, ":scene_to_use", "scn_camp_scene_snow"),
          (else_try),
            (this_or_next|eq, ":terrain_type", rt_desert),
            (eq, ":terrain_type", rt_desert_forest),
            (assign, ":scene_to_use", "scn_camp_scene_desert"),
          (else_try),
            (this_or_next|eq, ":terrain_type", rt_river),
            (eq, ":terrain_type", rt_water), #figure this out later
            (assign, ":scene_to_use", "scn_sea_1"),
          (else_try),
            (eq, ":terrain_type", rt_bridge),
            (try_for_parties, ":party_no"),
                (is_between, ":party_no", "p_bridge_1", "p_looter_spawn_point"),
                (store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
                (lt, ":distance", 2),
                (party_get_icon, ":icon", ":party_no"),
                (try_begin),
                    (eq, ":icon", "icon_bridge_snow_a"),
                    (assign, ":scene_to_use", "scn_camp_scene_snow"),
                (else_try),
                    (assign, ":scene_to_use", "scn_camp_scene_plain"),
                (try_end),
            (try_end),
          (try_end),

		(assign, "$f_temp_var", ":scene_to_use"),

		(assign, "$f_cons1", -1), #Non-con
		(assign, "$f_cons2", 0), #Con
     ],
    [
      ("continue",[],"Continue...",
       [
        (call_script, "script_start_fucking", 2, "$f_temp_var"),
		(assign, "$f_temp_var", 0),
       ]),
      ]
  )
]
