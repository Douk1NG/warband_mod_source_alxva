# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

collect_taxes_failed_menu = [
(
    "collect_taxes_failed",mnf_disable_all_keys,
##diplomacy start+ fix gender of pronoun
    "You could collect only {reg3} denars as tax from {s3} before the revolt broke out.\
 {s1} won't be happy, but some silver will placate {reg4?her:him} better than nothing at all...",
##diplomacy end+
    "none",
    [#SB : set up picture
     (try_begin),
       (eq, "$character_gender", tf_male),
       (set_background_mesh, "mesh_pic_escape_1"),
     (else_try),
       (eq, "$character_gender", tf_male),
       (set_background_mesh, "mesh_pic_escape_1_fem"),
     (try_end),
     (str_store_party_name, s3, "$current_town"),
     (quest_get_slot, ":quest_giver", "qst_collect_taxes", slot_quest_giver_troop),
     ##diplomacy start+ store gender of quest giver in reg4
     (call_script, "script_dplmc_store_troop_is_female", ":quest_giver"),
     (assign, reg4, reg0),
     ##diplomacy end+
     (str_store_troop_name, s1, ":quest_giver"),
     (quest_get_slot, reg3, "qst_collect_taxes", slot_quest_gold_reward),
     (call_script, "script_fail_quest", "qst_collect_taxes"),
     (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4),
     (rest_for_hours, 0, 0, 0), #stop resting
     ],
    [
      ("continue", [], "Continue...",
        [#SB : lose renown
          (call_script, "script_change_troop_renown", "trp_player", -2),
          (change_screen_map),
        ]),
    ]
  )
]
