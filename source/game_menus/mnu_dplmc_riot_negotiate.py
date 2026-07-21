# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_riot_negotiate (menu)
# Called by menus in 2 domains: castle, village
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

dplmc_riot_negotiate_menu = [
(
    "dplmc_riot_negotiate",mnf_disable_all_keys,
    "You approach the angry crowd and begin negotiations. The leader of the riot demands {reg0} denars. He agrees to lay down arms if you are willing to pay.",
    "none",
    [
      (party_get_slot, ":center_relation", "$g_encountered_party", slot_center_player_relation),
      (val_min, ":center_relation", 0),
      (try_begin),
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
        (val_sub, ":center_relation", 75),
        (set_background_mesh, "mesh_pic_townriot"),
      (else_try),
        (val_sub, ":center_relation", 50),
        (set_background_mesh, "mesh_pic_villageriot"),
      (try_end),

      (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
      (val_add, ":center_relation", ":persuasion_level"),
      (val_mul, ":center_relation", ":center_relation"),
      (assign, reg0, ":center_relation"),
    ],
    [
      ("dplmc_pay_riot_treasury",
      [
        (gt, "$g_player_chamberlain", 0),
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (ge, ":gold", reg0),
      ],"Induce your chamberlain to pay the money from the treasury.",
       [
        (call_script, "script_dplmc_withdraw_from_treasury", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),
       ("dplmc_pay_riot_cash",
      [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", reg0),
      ],"Pay cash.",
       [
        (troop_remove_gold, "trp_player", reg0),
        (party_set_slot, "$g_encountered_party", slot_village_infested_by_bandits, 0),
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),

       ]),

      ("dplmc_back",[],"Back...",
       [
        (try_begin),
          (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
          (jump_to_menu, "mnu_castle_outside"),
        (else_try),
          (jump_to_menu, "mnu_village"),
        (try_end),
       ]),
    ],
  )
]
