# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_store_troop_is_female_reg (script)
# Called by menus in 8 domains: castle, diplomacy, kingdom_management, notifications, siege, taxes, tournament, town
# ======================================================================

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

dplmc_store_troop_is_female_reg_scripts = [
("dplmc_store_troop_is_female_reg",
  [
    (store_script_param_1, ":troop_no"),
    (store_script_param_2, ":reg_no"),
    (ge, ":troop_no", 0),
    (troop_get_type, ":is_female", ":troop_no"),
	(val_mod, ":is_female", 2), # Makes even number skins "0" odd number "1" - tf_female is eqal to 1
        ##Can asign to registers 0,1,2,3, 65, or 4
    (try_begin),
      (eq, ":reg_no", 4),
      (assign, reg4, ":is_female"),
    (else_try),
      (eq, ":reg_no", 3),
      (assign, reg3, ":is_female"),
    (else_try),
      (eq, ":reg_no", 2),
      (assign, reg2, ":is_female"),
    (else_try),
      (eq, ":reg_no", 1),
      (assign, reg1, ":is_female"),
    (else_try),
      (eq, ":reg_no", 0),
      (assign, reg0, ":is_female"),
    (else_try),
      (eq, ":reg_no", 65),
      (assign, reg65, ":is_female"),
    (else_try),
      ##default to reg4
      (assign, reg4, ":reg_no"),
      (display_message, "@{!} ERROR: called script dplmc-store-troop-is-female-reg with bad argument {reg4}"),
      (assign, reg4, ":is_female"),
    (try_end),
  ])
]
