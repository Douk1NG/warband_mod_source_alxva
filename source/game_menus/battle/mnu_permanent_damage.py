# ======================================================================
# SHARED DEPENDENCY
# Entity: permanent_damage (menu)
# Called by menus in 2 domains: battle, captivity
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

permanent_damage_menu = [
(
    "permanent_damage",mnf_disable_all_keys,
    "{s0}",
    "none",
    [
      (assign, ":end_cond", 1),
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":random_attribute", 0, 4),
        (store_attribute_level, ":attr_level", "trp_player", ":random_attribute"),
        (try_begin),
          (gt, ":attr_level", 3),
          (neq, ":random_attribute", ca_charisma),
          (try_begin),
            (eq, ":random_attribute", ca_strength),
            (str_store_string, s0, "@Some of your tendons have been damaged in the battle. You lose 1 strength."),
          (else_try),
            (eq, ":random_attribute", ca_agility),
            (str_store_string, s0, "@You took a nasty wound which will cause you to limp slightly even after it heals. You lose 1 agility."),
##          (else_try),
##            (eq, ":random_attribute", ca_charisma),
##            (str_store_string, s0, "@After the battle you are aghast to find that one of the terrible blows you suffered has left a deep, disfiguring scar on your face, horrifying those around you. Your charisma is reduced by 1."),
          (else_try),
##            (eq, ":random_attribute", ca_intelligence),
            (str_store_string, s0, "@You have trouble thinking straight after the battle, perhaps from a particularly hard hit to your head, and frequent headaches now plague your existence. Your intelligence is reduced by 1."),
          (try_end),
        (else_try),
          (lt, ":end_cond", 200),
          (val_add, ":end_cond", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq, ":end_cond", 200),
        (try_begin),
          (eq, "$g_next_menu", -1),
          (leave_encounter),
          (change_screen_return),
        (else_try),
          (jump_to_menu, "$g_next_menu"),
        (try_end),
      (else_try),
        (troop_raise_attribute, "trp_player", ":random_attribute", -1),
      (try_end),
      ],
    [
      ("s0",
       [
         (store_random_in_range, ":random_no", 0, 4),
         (try_begin),
           (eq, ":random_no", 0),
           (str_store_string, s0, "@Perhaps I'm getting unlucky..."),
         (else_try),
           (eq, ":random_no", 1),
           (str_store_string, s0, "@Retirement is starting to sound better and better."),
         (else_try),
           (eq, ":random_no", 2),
           (str_store_string, s0, "@No matter! I will persevere!"),
         (else_try),
           (eq, ":random_no", 3),
			  ##diplomacy start+ Don't use troop_get_type for gender
			  #(troop_get_type, ":is_female", "trp_player"),#<- replaced
           (try_begin),
             #(eq, ":is_female", 1),#<- replaced
			 (eq, "$character_gender", tf_female),#<- added
             (str_store_string, s0, "@What did I do to deserve this?"),
           (else_try),
             (str_store_string, s0, "@I suppose it'll make for a good story, at least..."),
           (try_end),
			  ##diplomacy end+
         (try_end),
         ],
       "{s0}",
       [
         (try_begin),
           (eq, "$g_next_menu", -1),
           (leave_encounter),
           (change_screen_return),
         (else_try),
           (jump_to_menu, "$g_next_menu"),
         (try_end),
         ]),
      ]
  )
]
