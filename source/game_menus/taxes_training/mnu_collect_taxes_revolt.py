# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

collect_taxes_revolt_menu = [
(
    "collect_taxes_revolt",0,
    "You are interrupted while collecting the taxes at {s3}. A large band of angry {reg9?peasants:townsmen} is marching nearer,\
 shouting about the exorbitant taxes and waving torches and weapons. It looks like they aim to fight you!",
    "none",
    [(str_store_party_name, s3, "$current_town"),
     #SB : town pictures
     (try_begin),
       (party_slot_eq, "$current_town", slot_party_type, spt_village),
       (assign, reg9, 1),
       (set_background_mesh, "mesh_pic_villageriot"),
     (else_try),
       (set_background_mesh, "mesh_pic_townriot"),
       (assign, reg9, 0),
     (try_end),
     ],
    [
      ("continue", [], "Continue...",
       [(set_jump_mission,"mt_back_alley_revolt"),
        (quest_get_slot, ":target_center", "qst_collect_taxes", slot_quest_target_center),
        (try_begin),
          (party_slot_eq, ":target_center", slot_party_type, spt_town),
          (party_get_slot, ":town_alley", ":target_center", slot_town_alley),
        (else_try),
          (party_get_slot, ":town_alley", ":target_center", slot_castle_exterior),
        (try_end),
        (modify_visitors_at_site,":town_alley"),
        (reset_visitors),
        (assign, ":num_rebels", 6),
        (store_character_level, ":level", "trp_player"),
        (val_div, ":level", 5),
        (val_add, ":num_rebels", ":level"),
        (set_visitors, 1, "trp_tax_rebel", ":num_rebels"),
        (jump_to_scene,":town_alley"),
        (change_screen_mission),
        ]),
    ]
  )
]
