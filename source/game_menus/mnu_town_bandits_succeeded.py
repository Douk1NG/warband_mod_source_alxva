# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

town_bandits_succeeded_menu = [
(
    "town_bandits_succeeded",mnf_disable_all_keys,
    "The {s4} fall before you as wheat to a scythe! Soon you stand alone in the streets\
 while {reg4?most of your attackers: the bandit} lie unconscious, dead or dying.\
 Searching the {reg4?bodies:body}, you find a purse which must have belonged to a previous victim of {reg4?these brute:this lowlife}.\
 Or perhaps, it was {reg4?given to them:provided} by someone who wanted to arrange a suitable ending to your life.",
    "none",
    [
      # (party_set_slot, "$current_town", slot_center_has_bandits, 0), #we need this
      (party_get_slot, ":bandit_troop", "$current_town", slot_center_has_bandits),
      (assign, "$g_last_defeated_bandits_town", "$g_encountered_party"),
      (try_begin),
        (check_quest_active, "qst_deal_with_night_bandits"),
        (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
        (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, "$g_encountered_party"),
        (call_script, "script_succeed_quest", "qst_deal_with_night_bandits"),
      (try_end),
      #SB : variable rewards, since we have different bandits in play
      (call_script, "script_game_get_join_cost", ":bandit_troop"),
      (store_mul, ":xp_reward", "$num_center_bandits", reg0),
      (try_begin), #reduce bonus exp, since town missions troops don't use horses
        (troop_is_mounted, ":bandit_troop"),
        (val_div, ":xp_reward", 2),
      (try_end),
      (add_xp_to_troop, ":xp_reward", "trp_player"),
      (call_script, "script_game_get_upgrade_cost", ":bandit_troop"), #20, 40, 80
      (store_mul, ":gold_reward", "$num_center_bandits", reg0),
      (call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
      #SB : string setup
      (str_store_troop_name_by_count,s4, ":bandit_troop", "$num_center_bandits"),
      (store_sub, reg4, "$num_center_bandits", 1),
    ],
    [
      ("continue",[],"Continue...",[
        (party_set_slot, "$current_town", slot_center_has_bandits, 0),
        (change_screen_return),
      ]),
    ],
  )
]
