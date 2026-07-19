# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_town_riot_removed_menu = [
(
    "dplmc_town_riot_removed",mnf_disable_all_keys,
    "In bloody battle you and your men slaughter the rebels and regain control over the town.",
    "none",
    [],
    [
      ("dplmc_continue",[],"Continue...",
       [
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (assign, "$new_encounter", 1),
        (try_begin),
          (party_get_slot, ":town_lord","$g_encountered_party", slot_town_lord),
          (troop_get_slot, ":cur_banner", ":town_lord", slot_troop_banner_scene_prop),
          (try_begin),
              (gt, ":cur_banner", 0),
              (val_sub, ":cur_banner", banner_scene_props_begin),
              (val_add, ":cur_banner", banner_map_icons_begin),
              (party_set_banner_icon, "$g_encountered_party", ":cur_banner"),
          (else_try),
              (eq, ":cur_banner", -1),
              (troop_get_slot, ":flag_icon", ":town_lord", slot_troop_custom_banner_map_flag_type),
              (try_begin),
                (ge, ":flag_icon", 0),
                (val_add, ":flag_icon", custom_banner_map_icons_begin),
                (party_set_banner_icon, "$g_encountered_party", ":flag_icon"),
              (try_end),
          (try_end), #custom_banner_begin
        (try_end),
        (jump_to_menu, "mnu_castle_outside"),
       ]),
    ],
  )
]
