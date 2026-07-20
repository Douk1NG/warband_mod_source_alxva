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

setup_talk_info_scripts = [
("setup_talk_info",
    [
      # ##diplomacy start+ Ensure $character_gender is set correctly (it should have been set during character creation)
      # (try_begin),
         # (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
         # (assign, "$character_gender", tf_female),
      # (else_try),
         # (assign, "$character_gender", tf_male),
      # (try_end),
      # ##diplomacy end+
      #SB : redo order
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (str_store_troop_name, s61, "$g_talk_troop"),
      # (str_store_string, s61, "@{!} {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      # (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, "@{!} {s61}"),
      (talk_info_set_line, 1, "str_relation_reg1"),
      (call_script, "script_describe_relation_to_s63", "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ])
]
