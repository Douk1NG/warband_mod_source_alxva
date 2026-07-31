# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *



   # Process alarms - perhaps break this down into several groups, with a modula
   

process_vassal_ai_simple_triggers = [
(1, #this now calls 1/3 of all centers each time, thus hopefully lightening the CPU load
   [
    (call_script, "script_process_alarms"),

    (call_script, "script_allow_vassals_to_join_indoor_battle"),

    (call_script, "script_process_kingdom_parties_ai"),
     
    #SB : add spotting check, moved to less time-consuming slot
    (call_script, "script_get_max_skill_of_player_party", "skl_spotting"),
    (store_add, ":spotting", reg0, 3),
    (val_div, ":spotting", 2), #1 to 9 now
    (try_for_parties, ":bandit_camp"),
      (gt, ":bandit_camp", "p_spawn_points_end"),
      #Can't have party is active here, because it will fail for inactive parties
      (party_get_template_id, ":template", ":bandit_camp"), #SB : fix template range
      (is_between, ":template", "pt_steppe_bandit_lair", "pt_bandit_lair_templates_end"),

      (store_distance_to_party_from_party, ":distance", "p_main_party", ":bandit_camp"),
      (lt, ":distance", ":spotting"),
      (party_set_flags, ":bandit_camp", pf_disabled, 0),
      (party_set_flags, ":bandit_camp", pf_always_visible, 1),
    (try_end),
   ]),
]
