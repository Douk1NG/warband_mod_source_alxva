# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

agent_apply_training_health_scripts = [
("agent_apply_training_health", [
      (store_script_param_1, ":agent_no"),
      # (store_script_param_2, "$current_town"),

      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
      (party_get_slot, ":relation", "$current_town", slot_center_player_relation), #range from -100 to 100
      (store_sub, ":relation", 200, ":relation"), #300 to 100

      (store_troop_health, ":health", "trp_player", 0), #this is not yet deducted
      (store_agent_hit_points, ":hp", ":agent_no", 0),

      (val_sub, ":hp", ":health"), #this is the difference (non-positive)
      (try_begin),
        (agent_is_alive, ":agent_no"),
        (store_skill_level, ":skill", "skl_first_aid", "trp_player"),
      (else_try),
        (assign, ":skill", 0),
      (try_end),
      (val_add, ":skill", ":first_aid"),
      (val_mul, ":skill", -5),  #as per skill description
      (val_add, ":skill", 100), # 100 - skill effect
      #apply skill effect, relation effect and set health
      (val_mul, ":hp", ":skill"),
      (val_div, ":hp", 100),
      (val_mul, ":hp", ":relation"),
      (val_div, ":hp", 200),
      (val_add, ":health", ":hp"), #subtract modified difference
      (val_max, ":health", 5),
      (troop_set_health, "trp_player", ":health", 0),
    ])
]
