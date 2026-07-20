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

setup_talk_info_companions_scripts = [
#script_setup_talk_info
#script_setup_talk_info_companions
("setup_talk_info_companions",
    [
      ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      (try_begin),
         (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	     (assign, "$character_gender", 1),
      (else_try),
	     (assign, "$character_gender", 0),
      (try_end),
	  ##diplomacy end+
      (call_script, "script_dplmc_npc_morale", "$g_talk_troop", 1), #SB : number + bar string in s63
      (assign, ":troop_morale", reg0),
      (talk_info_set_relation_bar, ":troop_morale"),
      (talk_info_set_line, 3, s63),

      (str_store_troop_name, s61, "$g_talk_troop"),
      (talk_info_set_line, 0, s61),
      # (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, ":troop_morale"),
      (str_store_string, s62, "str_morale_reg1"),
      (talk_info_set_line, 1, s62),
  ])
]
