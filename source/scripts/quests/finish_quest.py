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

finish_quest_scripts = [
# script_troop_get_player_relation
# Input: arg1 = quest_no, arg2 = finish_percentage
# Output: none
("finish_quest",
    [
      (store_script_param_1, ":quest_no"),
      (store_script_param_2, ":finish_percentage"),

      (quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
      (quest_get_slot, ":quest_importance", ":quest_no", slot_quest_importance),
      (quest_get_slot, ":quest_xp_reward", ":quest_no", slot_quest_xp_reward),
      (quest_get_slot, ":quest_gold_reward", ":quest_no", slot_quest_gold_reward),

      (try_begin),
        (lt, ":finish_percentage", 100),
        (val_mul, ":quest_xp_reward", ":finish_percentage"),
        (val_div, ":quest_xp_reward", 100),
        (val_mul, ":quest_gold_reward", ":finish_percentage"),
        (val_div, ":quest_gold_reward", 100),
        #Changing the relation factor. Negative relation if less than 75% of the quest is finished.
        #Positive relation if more than 75% of the quest is finished.
        (neq, ":quest_importance", -1), #has to have a value assigned
        (assign, ":importance_multiplier", ":finish_percentage"),
        (val_sub, ":importance_multiplier", 75),
        (val_mul, ":quest_importance", ":importance_multiplier"),
        (val_div, ":quest_importance", 100),
      (try_end),
      #SB : separate condition
      (try_begin),
        (neq, ":quest_importance", -1), #has to have a value assigned
        (val_mul, ":quest_importance", 4), #was div 4. Relation was increasing very less. I changed it to mul 4.
        (val_add, ":quest_importance", 1),
        (call_script, "script_change_player_relation_with_troop", ":quest_giver", ":quest_importance"),
      (try_end),

      (add_xp_as_reward, ":quest_xp_reward"),
      (call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
      (call_script, "script_end_quest", ":quest_no"),

  ])
]
