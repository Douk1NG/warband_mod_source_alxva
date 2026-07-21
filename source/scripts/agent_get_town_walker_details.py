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

agent_get_town_walker_details_scripts = [
# script_agent_get_town_walker_details
# This script assumes this is one of town walkers.
# Input: agent_id
# Output: reg0: town_walker_type, reg1: town_walker_dna
("agent_get_town_walker_details",
    [(store_script_param, ":agent_no", 1),
     (agent_get_entry_no, ":entry_no", ":agent_no"),
     (store_sub, ":walker_no", ":entry_no", town_walker_entries_start),

     (store_add, ":type_slot", slot_center_walker_0_type, ":walker_no"),
     (party_get_slot, ":walker_type", "$current_town", ":type_slot"),
     (store_add, ":dna_slot", slot_center_walker_0_dna,  ":walker_no"),
     (party_get_slot, ":walker_dna", "$current_town", ":dna_slot"),
     (assign, reg0, ":walker_type"),
     (assign, reg1, ":walker_dna"),
     (assign, reg2, ":walker_no"),
  ])
]
