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

event_hero_taken_prisoner_by_player_scripts = [
#Hunting scripts end
# Input: arg1 = troop_no
# Output: none
("event_hero_taken_prisoner_by_player",
    [
      (store_script_param_1, ":troop_no"),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (try_begin),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (else_try),
          (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
          (quest_set_slot, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
          (val_mul, ":troop_no", -1),
        (try_end),
        (neg|check_quest_concluded, "qst_persuade_lords_to_make_peace"),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, 0),
        (neg|quest_slot_ge, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, 0),
        (call_script, "script_succeed_quest", "qst_persuade_lords_to_make_peace"),
      (try_end),
      (call_script, "script_update_troop_location_notes", ":troop_no", 0),
  ])
]
