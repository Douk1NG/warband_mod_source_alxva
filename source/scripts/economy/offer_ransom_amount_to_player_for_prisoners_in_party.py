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

offer_ransom_amount_to_player_for_prisoners_in_party_scripts = [
("offer_ransom_amount_to_player_for_prisoners_in_party",
    [(store_script_param, ":party_no", 1),
     (assign, ":result", 0),
     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
     (try_for_range, ":i_stack", 0, ":num_stacks"),
       (eq, ":result", 0),
       (party_prisoner_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
       (troop_is_hero, ":stack_troop"),
       (this_or_next|troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
       (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_lady),
       (store_troop_faction, ":stack_troop_faction", ":stack_troop"),
       (store_random_in_range, ":random_no", 0, 100),
       (try_begin),
         (faction_slot_eq, ":stack_troop_faction", slot_faction_state, sfs_active),
         (le, ":random_no", 5),
         (neq, "$g_ransom_offer_rejected", 1),
         (assign, ":num_stacks", 0), #break
         (assign, ":result", 1),
         (assign, "$g_ransom_offer_troop", ":stack_troop"),
         (assign, "$g_ransom_offer_party", ":party_no"),
         (jump_to_menu, "mnu_enemy_offer_ransom_for_prisoner"),
       (try_end),
     (try_end),

     #SB : offer ransom for kingdom ladies as per conditions in dialogues
     (try_begin),
       (is_between, ":party_no", walled_centers_begin, walled_centers_end),
       (assign, ":end", kingdom_ladies_end),
       (store_faction_of_party, ":faction_no", ":party_no"),
       (try_for_range, ":heroes", kingdom_ladies_begin, ":end"),
         (troop_slot_eq, ":heroes", slot_troop_cur_center, ":party_no"),
         (troop_slot_eq, ":heroes", slot_troop_prisoner_of_party, ":party_no"),
         (troop_slot_eq, ":heroes", slot_troop_occupation, slto_kingdom_lady),
         (store_faction_of_troop, ":lady_faction", ":heroes"),
         (neq, ":lady_faction", ":faction_no"),
         (faction_slot_eq, ":lady_faction", slot_faction_state, sfs_active),
         (store_random_in_range, ":random_no", 0, 100),
         (le, ":random_no", 5),
         (neq, "$g_ransom_offer_rejected", 1),
         (assign, ":end", 0), #break
         (assign, ":result", 1),
         (assign, "$g_ransom_offer_troop", ":heroes"),
         (assign, "$g_ransom_offer_party", ":party_no"),
         (jump_to_menu, "mnu_enemy_offer_ransom_for_prisoner"),
       (try_end),
     (try_end),
     (assign, reg0, ":result"),
     ])
]
