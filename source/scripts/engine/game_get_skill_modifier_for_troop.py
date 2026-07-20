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

game_get_skill_modifier_for_troop_scripts = [
#script_game_get_skill_modifier_for_troop
# This script is called from the game engine when a skill's modifiers are needed
# INPUT: arg1 = troop_no, arg2 = skill_no
# OUTPUT: trigger_result = modifier_value
("game_get_skill_modifier_for_troop",
   [(store_script_param, ":troop_no", 1),
    (store_script_param, ":skill_no", 2),
    (assign, ":modifier_value", 0),
    (try_begin),
      (eq, ":skill_no", "skl_wound_treatment"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_wound_treatment_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_trainer"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_training_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (else_try),
      (eq, ":skill_no", "skl_surgery"),
      (call_script, "script_get_troop_item_amount", ":troop_no", "itm_book_surgery_reference"),
      (gt, reg0, 0),
      (val_add, ":modifier_value", 1),
    (try_end),
    (set_trigger_result, ":modifier_value"),
    ])
]
