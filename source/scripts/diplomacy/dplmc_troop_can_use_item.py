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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_troop_can_use_item_scripts = [
#recruiter kit end
####################################################################################
#
# Autoloot Scripts begin
# ---------------------------------------------------
####################################################################################
#### Autoloot improved by rubik begin
# ("dplmc_init_item_difficulties", set_item_difficulty()),
#### Autoloot improved by rubik end
###################################
# Can a troop qualify to use this item?
# Returns 1 = yes, 0 = no.
("dplmc_troop_can_use_item",
   [
      (store_script_param, ":troop", 1),
      (store_script_param, ":item", 2),
      (store_script_param, ":item_modifier", 3),

      # (item_get_slot, ":difficulty", ":item", dplmc_slot_item_difficulty),
      (item_get_difficulty, ":difficulty", ":item"),
      (item_get_type, ":type", ":item"),
      (try_begin),
        (eq, ":difficulty", 0), # don't apply imod modifiers if item has no requirement
      (else_try),
        (eq, ":item_modifier", imod_stubborn),
        (val_add, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_timid),
        (val_sub, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_heavy),
        (neq, ":type", itp_type_horse), #heavy horses don't increase difficulty
        (val_add, ":difficulty", 1),
      (else_try),
        (eq, ":item_modifier", imod_strong),
        (val_add, ":difficulty", 2),
      (else_try),
        (eq, ":item_modifier", imod_masterwork),
        (val_add, ":difficulty", 4),
      (try_end),

      (item_get_type, ":type", ":item"),
      (try_begin),
        (eq, ":type", itp_type_horse),
        (store_skill_level, ":skill", skl_riding, ":troop"),
      (else_try),
        (this_or_next|eq, ":type", itp_type_crossbow),
        (this_or_next|eq, ":type", itp_type_one_handed_wpn),
        (this_or_next|eq, ":type", itp_type_two_handed_wpn),
        (this_or_next|eq, ":type", itp_type_polearm),
        (this_or_next|eq, ":type", itp_type_head_armor),
        (this_or_next|eq, ":type", itp_type_body_armor),
        (this_or_next|eq, ":type", itp_type_foot_armor),
        (eq, ":type", itp_type_hand_armor),
        (store_attribute_level, ":skill", ":troop", ca_strength),
      (else_try),
        (eq, ":type", itp_type_shield),
        (store_skill_level, ":skill", skl_shield, ":troop"),
      (else_try),
        (eq, ":type", itp_type_bow),
        (store_skill_level, ":skill", skl_power_draw, ":troop"),
      (else_try),
        (eq, ":type", itp_type_thrown),
        (store_skill_level, ":skill", skl_power_throw, ":troop"),
      (try_end),

      (try_begin),
        (lt, ":skill", ":difficulty"),
        (assign, reg0, 0),
      (else_try),
        (assign, reg0, 1),
      (try_end),
   ])
]
