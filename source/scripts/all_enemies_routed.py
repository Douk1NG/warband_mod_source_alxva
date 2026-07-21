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

all_enemies_routed_scripts = [
("all_enemies_routed", [
  (assign, ":enemies_remaining", 0),
  (try_for_agents, ":agent"),
    (neg|agent_is_ally, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_human, ":agent"),
    (agent_get_slot, ":routing", ":agent", slot_agent_is_running_away),
    (eq, ":routing", 0),
    (val_add, ":enemies_remaining", 1),
  (try_end),
  (assign, reg10, ":enemies_remaining"),
])
]
