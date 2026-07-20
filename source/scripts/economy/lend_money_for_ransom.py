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

lend_money_for_ransom_scripts = [
("lend_money_for_ransom", [
    (store_script_param_1, ":lord_no"), #usually $g_talk_troop
    (try_begin),
      (troop_get_slot, ":ransom_amount", ":lord_no", slot_troop_player_debt),
      (le, ":ransom_amount", 0),
      (store_script_param_2, ":ransom_amount"),
    (try_end),
    (quest_get_slot, ":cur_ransom", "qst_rescue_prisoner", slot_quest_target_state),
    (val_add, ":cur_ransom", ":ransom_amount"), #actual amount to give

    #set up quests
    (quest_set_slot, "qst_rescue_prisoner", slot_quest_target_state, ":cur_ransom"),
    (assign, reg0, ":cur_ransom"),
    #the amount calculated at the start, will differ from expected ransom
    (quest_get_slot, reg1, "qst_rescue_prisoner", slot_quest_target_amount),
    (str_store_string, s1, "@You have raised {reg0}/{reg1} denars for the ransom"),
    (add_quest_note_from_sreg, "qst_rescue_prisoner", 4, s1, 1), #0:date, 1:giver, 2:desc 3:time

    #move actual gold
    (troop_add_gold, "trp_player", ":ransom_amount"),
    (try_begin),
      (troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
      (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":lord_no"),
      (val_add, ":ransom_amount", dplmc_ransom_debt_mask), #masking this from "real" debt
      (troop_set_slot, ":lord_no", slot_troop_player_debt, ":ransom_amount"),
    (try_end),

    ]
  )
]
