# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

collect_taxes_complete_menu = [
(
    "collect_taxes_complete",mnf_disable_all_keys,
    ##diplomacy start+
    ##Replace "him" with "{reg4?her:him}"
    "You've collected {reg3} denars in taxes from {s3}. {s19} will be expecting you to take the money to {reg4?her:him}.",
    ##diplomacy end+
    "none",
    [(str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     (str_store_troop_name, s19, ":quest_giver"),
     ##diplomacy start+

     (try_begin),
       (eq, "$qst_collect_taxes_halve_taxes", 0),
       (call_script, "script_change_player_relation_with_center", "$current_town", -2),
     (try_end),
     (call_script, "script_succeed_quest", "qst_collect_taxes"),

     #SB : add renown to tax collector
     (try_begin),
       (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
       (neq, reg1, "trp_player"),
       (call_script, "script_change_troop_renown", reg1, dplmc_companion_skill_renown),
     (try_end),

     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     ##Store quest giver gender to reg4
     (call_script, "script_dplmc_store_troop_is_female_reg", ":quest_giver", 4), #SB : use other script
     ##diplomacy end+
     ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
    ]
  )
]
