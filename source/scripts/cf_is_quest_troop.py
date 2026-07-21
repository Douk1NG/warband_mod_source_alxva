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

cf_is_quest_troop_scripts = [
##  #script_get_available_mercenary_troop_and_amount_of_center
("cf_is_quest_troop",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":is_quest_troop", 0),
      (try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
        (check_quest_active, ":cur_quest"),
        (quest_get_slot, ":quest_troop_1", ":cur_quest", slot_quest_target_troop),
        (quest_get_slot, ":quest_troop_2", ":cur_quest", slot_quest_object_troop),
        (quest_get_slot, ":quest_troop_3", ":cur_quest", slot_quest_giver_troop),
        (this_or_next|eq, ":quest_troop_1", ":troop_no"),
        (this_or_next|eq, ":quest_troop_2", ":troop_no"),
        (eq, ":quest_troop_3", ":troop_no"),
        (assign, ":is_quest_troop", 1),
      (try_end),
      (eq, ":is_quest_troop", 1),
  ])
]
