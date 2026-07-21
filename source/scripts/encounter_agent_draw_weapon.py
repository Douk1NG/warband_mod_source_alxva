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

encounter_agent_draw_weapon_scripts = [
# script_remove_troop_from_prison
#input: none, based on $g_talk_agent
#output: none, agent wields first available weapon to show aggression
("encounter_agent_draw_weapon",
    [
        (store_conversation_agent, "$g_talk_agent"),
        (try_begin),
          (agent_get_item_slot, ":item_no", "$g_talk_agent", ek_item_0),
          (gt, ":item_no", 0),
          (agent_set_wielded_item, "$g_talk_agent", ":item_no"),
        (try_end),

    ])
]
