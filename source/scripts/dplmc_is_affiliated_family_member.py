# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_is_affiliated_family_member (script)
# Called by menus in 3 domains: castle, town, village
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

dplmc_is_affiliated_family_member_scripts = [
("dplmc_is_affiliated_family_member",
  [
      (store_script_param, ":troop_id", 1),

      (assign, ":is_affiliated_family_member", 0),
	  ##nested diplomacy start+
	  (assign, ":save_reg1", reg1),#<- Save reg1 which gets overwritten by script_dplmc_troop_get_family_relation_to_troop
	  ##nested diplomacy end+
      (try_begin),
        (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
        (try_begin),
		  ##nested diplomacy start+ add use of dplmc_slot_troop_affiliated
		  (this_or_next|troop_slot_eq, ":troop_id", dplmc_slot_troop_affiliated, 3),
		  ##diplomacy end+
          (eq, "$g_player_affiliated_troop", ":troop_id"),
          (assign, ":is_affiliated_family_member", 1),
        (else_try),
          (is_between, ":troop_id", lords_begin, kingdom_ladies_end),
		  ##nested diplomacy start+
          #(call_script, "script_troop_get_family_relation_to_troop", ":troop_id", "$g_player_affiliated_troop"),
		  (call_script, "script_dplmc_troop_get_family_relation_to_troop", ":troop_id", "$g_player_affiliated_troop"),
		  ##nested diplomacy end+
          (gt, reg0, 0),
          (call_script, "script_troop_get_relation_with_troop", "$g_player_affiliated_troop", ":troop_id"),
          (ge, reg0, -10),
		  (assign, ":is_affiliated_family_member", 1),
        (try_end),
      (try_end),
	  ##nested diplomacy start+
	  (assign, reg1, ":save_reg1"),#revert register
	  ##nested diplomacy end+
      (assign, reg0, ":is_affiliated_family_member"),
  ])
]
