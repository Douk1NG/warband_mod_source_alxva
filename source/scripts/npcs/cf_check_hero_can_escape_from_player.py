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

cf_check_hero_can_escape_from_player_scripts = [
# script_cf_check_hero_can_escape_from_player
# Input: arg1 = troop_no
# Output: none (can fail)
("cf_check_hero_can_escape_from_player",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":quest_target", 0),
      (try_begin),
        (check_quest_active, "qst_persuade_lords_to_make_peace"),
        (this_or_next|quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_target_troop, ":troop_no"),
        (quest_slot_eq, "qst_persuade_lords_to_make_peace", slot_quest_object_troop, ":troop_no"),
        (assign, ":quest_target", 1),
      (else_try),
        (ge, ":troop_no", "trp_sea_raider_leader"),
        (lt, ":troop_no", "trp_bandit_leaders_end"),
        (try_begin),
          (check_quest_active, "qst_learn_where_merchant_brother_is"),
          (assign, ":quest_target", 1), #always catched
        (else_try),
          (assign, ":quest_target", -1), #always run.
        (try_end),
      (try_end),

      (assign, ":continue", 0),
      (try_begin),
        (eq, ":quest_target", 0), #if not quest target
        (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (assign, ":continue", 0),
      (else_try),
        (eq, ":quest_target", 0), #if not quest target
        (store_random_in_range, ":rand", 0, 100),
        (lt, ":rand", hero_escape_after_defeat_chance),
        (assign, ":continue", 1),
      (else_try),
        (eq, ":quest_target", -1), #if (always run) quest target
        (assign, ":continue", 1),
      (try_end),

      (eq, ":continue", 1),
  ])
]
