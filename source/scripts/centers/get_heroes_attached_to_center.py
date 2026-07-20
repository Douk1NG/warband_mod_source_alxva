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

get_heroes_attached_to_center_scripts = [
# script_get_heroes_attached_to_center
# Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
# Output: none, adds heroes to the party_no_to_collect_heroes party
("get_heroes_attached_to_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),
      (call_script, "script_get_heroes_attached_to_center_aux", ":center_no", ":party_no_to_collect_heroes"),

#rebellion changes begin -Arma
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

#     (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
#        (faction_slot_eq, ":rebel_faction", slot_faction_state, sfs_inactive_rebellion),
#        (faction_slot_eq, ":rebel_faction", slot_faction_inactive_leader_location, ":center_no"),
#        (faction_get_slot, ":pretender", ":rebel_faction", slot_faction_leader),
#        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
#     (try_end),
#rebellion changes end


  ])
]
