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

agents_cheer_during_training_scripts = [
("agents_cheer_during_training", [
      (party_get_morale, ":cur_morale", "p_main_party"),
      (assign, ":boundary", 150),
    #first aid double-stacks since it's not a battle
      (try_for_agents, ":agent_no"),
        (agent_is_active, ":agent_no"),
        (agent_is_human, ":agent_no"),
        # (agent_get_troop_id, ":troop_no", ":agent_no"), #a spectator
        (neg|agent_has_item_equipped, ":agent_no", "itm_practice_boots"),
        (store_random_in_range, ":random_no", ":cur_morale", 250),
        (gt, ":random_no", ":boundary"),
        (val_add, ":boundary", 15),
        (agent_set_animation, ":agent_no", "anim_cheer"),
        (store_random_in_range, ":random_no", 0, 100),
        (agent_set_animation_progress, ":agent_no", ":random_no"),
      (try_end),
    ])
]
