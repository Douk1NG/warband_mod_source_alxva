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

setup_party_meeting_scripts = [
("setup_party_meeting",
    [
      (store_script_param_1, ":meeting_party"),
      (try_begin),
        (lt, "$g_encountered_party_relation", 0), #hostile
#        (call_script, "script_music_set_situation_with_culture", mtf_sit_encounter_hostile),
      (try_end),
      (call_script, "script_get_meeting_scene"), (assign, ":meeting_scene", reg0),
      (modify_visitors_at_site,":meeting_scene"),(reset_visitors),
      (set_visitor,0,"trp_player"),
      (party_stack_get_troop_id, ":meeting_troop",":meeting_party",0),
      (party_stack_get_troop_dna,":troop_dna",":meeting_party",0),
      (set_visitor,17,":meeting_troop",":troop_dna"),
      (set_jump_mission,"mt_conversation_encounter"),
      (jump_to_scene,":meeting_scene"),
      (change_screen_map_conversation, ":meeting_troop"),
  ])
]
