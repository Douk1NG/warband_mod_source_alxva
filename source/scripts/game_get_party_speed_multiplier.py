# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_get_party_speed_multiplier_scripts = [
##diplomacy end+
##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##diplomacy begin
#script_game_get_party_speed_multiplier
# This script is called from the game engine when a skill's modifiers are needed
# INPUT: arg1 = party_no
# OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
("game_get_party_speed_multiplier",
  [
    (store_script_param_1, ":party_no"),

    (assign,":speed_multiplier",100),

    (try_begin),
      #(this_or_next|eq,":party_no","p_main_party"),
      (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
      (party_get_skill_level, ":pathfinding_skill", ":party_no", skl_pathfinding),
      (val_mul,":pathfinding_skill",3),
      (val_add,":speed_multiplier",":pathfinding_skill"),
    (try_end),

    (try_begin),
      #(party_has_flag, ":party_no", pf_is_ship),
      (party_get_slot, ":ship_type", ":party_no", slot_party_ship_type),
      (gt, ":ship_type", 0),
      (try_begin),
        (eq, ":ship_type", 1),
        (val_add, ":speed_multiplier", 15),
      (else_try),
        (eq, ":ship_type", 2),
        (val_add, ":speed_multiplier", 20),
      (else_try),
        (eq, ":ship_type", 3),
        (val_add, ":speed_multiplier", 5),
      (else_try),
        (eq, ":ship_type", 4),
        (val_add, ":speed_multiplier", 10),
      (try_end),
    (try_end),

    # (try_begin),
      # (eq,":party_no","p_main_party"),
      # (eq,"$g_move_fast", 1),
      # (val_mul,":speed_multiplier",2),
    # (try_end),

    (try_begin),
        (get_party_ai_behavior, ":behavior", ":party_no"),
        (eq, ":behavior", ai_bhvr_driven_by_party),
        (val_add,":speed_multiplier",10),
    (try_end),

    (try_begin),
        (party_get_template_id, ":template_id", ":party_no"),
        (eq, ":template_id", "pt_manhunters"),
        (val_mul,":speed_multiplier",2),
    (try_end),

    (val_max, ":speed_multiplier", 0),
    (set_trigger_result, ":speed_multiplier"),
   ])
]
