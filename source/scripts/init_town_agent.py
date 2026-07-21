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

init_town_agent_scripts = [
# script_init_town_agent
# Input: none
# Output: none
("init_town_agent",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_troop_id, ":troop_no", ":agent_no"),
      (set_fixed_point_multiplier, 100),
      (assign, ":stand_animation", -1),
      (try_begin),
        (this_or_next|is_between, ":troop_no", armor_merchants_begin, armor_merchants_end),
        (is_between, ":troop_no", weapon_merchants_begin, weapon_merchants_end),
        (try_begin),
          (troop_get_type, ":cur_troop_gender", ":troop_no"),
          (eq, ":cur_troop_gender", 0),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (else_try),
          (agent_set_animation, ":agent_no", "anim_stand_townguard"),
        (end_try),
      (else_try),
        (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
        (assign, ":stand_animation", "anim_stand_lady"),
      (else_try),
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (assign, ":stand_animation", "anim_stand_lord"),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, soldiers_end),
        (assign, ":stand_animation", "anim_stand_townguard"),
      (try_end),
      (try_begin),
        (ge, ":stand_animation", 0),
        (agent_set_stand_animation, ":agent_no", ":stand_animation"),
        (agent_set_animation, ":agent_no", ":stand_animation"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
      ])
]
