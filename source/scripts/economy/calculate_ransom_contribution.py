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

calculate_ransom_contribution_scripts = [
("calculate_ransom_contribution", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (store_script_param_2, ":ransom_size"), #2000 from quest giver, up to 125*strength for other relatives
    #because kingdom ladies aren't landholders, they give it without consequence of debt if quest fails (also less dialogue to write)
    (assign, ":ransom_amount", 0),

    (try_begin),
      (check_quest_active, "qst_rescue_prisoner"),
      (quest_get_slot, ":prisoner", "qst_rescue_prisoner", slot_quest_target_troop),
      (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
      (try_begin),
        #each +-2 relation has 1% effect on calculation to the effect of 50%/150% initial value
        (call_script, "script_troop_get_relation_with_troop", ":lord_no", ":prisoner"),
        (store_div, ":relation", reg0, 2),
        (val_add, ":relation", 100),
        (val_mul, ":ransom_amount", ":relation"),
        (val_div, ":ransom_amount", 100),
      (try_end),
      # problem is this script has variance in output, we can use the cached slot_quest_target_amount
      (call_script, "script_calculate_ransom_amount_for_troop", ":prisoner"),
      (assign, ":ransom", reg0), #original amount
      (val_add, ":ransom_size", ":cur_ransom"),
      (try_begin), #contributed too much, get remainder before arbitrary cap
        (gt, ":ransom_size", ":ransom"),
        (store_sub, ":ransom_amount", ":ransom", ":cur_ransom"),
      (else_try), #give full amount
        (store_sub, ":ransom_amount", ":ransom_size", ":cur_ransom"), #undo adding existing ransom
      (try_end),

      (try_begin), #active npcs have wealth
        (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_wealth", ":lord_no", slot_troop_wealth),
        (val_div, ":cur_wealth", 2), #at most half for contributing
        (val_min, ":cur_wealth", ":ransom"),
        (val_min, ":ransom_amount", ":cur_wealth"), #actual amount the lord can give
      (try_end),
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),
    (assign, reg0, ":ransom_amount"),
    ]
  )
]
