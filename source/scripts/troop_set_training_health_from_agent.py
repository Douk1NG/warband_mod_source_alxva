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

troop_set_training_health_from_agent_scripts = [
("troop_set_training_health_from_agent", [
      (party_get_skill_level, ":first_aid", "p_main_party", "skl_first_aid"),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        # (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        (agent_get_troop_id, ":troop_no", ":agent_no"),
        (troop_is_hero, ":troop_no"),
        (store_troop_health, ":health", ":troop_no", 0), #this is not yet deducted
        (store_agent_hit_points, ":hp", ":agent_no", 0),
        (val_sub, ":hp", ":health"), #this is the difference
        (try_begin),
          (agent_is_alive, ":agent_no"),
          (store_skill_level, ":skill", "skl_first_aid", ":troop_no"),
          (val_add, ":skill", ":first_aid"),
        (else_try),
          (assign, ":skill", ":first_aid"),
        (try_end),
        (val_mul, ":skill", -5),  #as per skill description
        (val_add, ":skill", 100), # 100 - skill effect
        #apply skill effect and set health
        (val_mul, ":hp", ":skill"),
        (val_div, ":hp", 100),
        (val_add, ":hp", ":health"), #subtract modified difference
        (troop_set_health, ":troop_no", ":hp", 0),
      (try_end),
    ])
]
