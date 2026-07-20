# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_troops import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

get_spawn_report_line_scripts = [
#script_get_spawn_report_line
# INPUT: arg1 = party_template, arg2 = max_parties (cap), arg3 = has_lair (1/0)
# OUTPUT: s0 = "<count>/<cap>  cd <hours>h  lair <0/1>"  (reg1..reg4 also set)
("get_spawn_report_line",
 [
  (store_script_param, ":party_template", 1),
  (store_script_param, ":cap", 2),
  (store_script_param, ":has_lair", 3),

  (store_num_parties_of_template, ":num", ":party_template"),

  (party_template_get_slot, ":cd", ":party_template", slot_party_template_respawn_cooldown),
  (val_max, ":cd", 0),
  (store_current_hours, ":cur_hours"),
  (store_sub, ":cd_left", ":cd", ":cur_hours"),
  (try_begin),
    (lt, ":cd_left", 0),
    (assign, ":cd_left", 0),
  (try_end),

  (assign, ":lair_active", 0),
  (try_begin),
    (eq, ":has_lair", 1),
    (party_template_get_slot, ":lair_party", ":party_template", slot_party_template_lair_party),
    (gt, ":lair_party", 1),
    (assign, ":lair_active", 1),
  (try_end),

   (assign, reg1, ":num"),
   (assign, reg2, ":cap"),
   (assign, reg3, ":cd_left"),
   (assign, reg4, ":lair_active"),
    (str_store_string, s0, "@{reg1}/{reg2}  cd {reg3}h  lair {reg4}"),
   ])
]
