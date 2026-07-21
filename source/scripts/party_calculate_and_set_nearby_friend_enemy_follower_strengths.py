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

party_calculate_and_set_nearby_friend_enemy_follower_strengths_scripts = [
("party_calculate_and_set_nearby_friend_enemy_follower_strengths",
    [
      (store_script_param, ":party_no", 1),
      (assign, ":follower_strength", 0),
      (assign, ":friend_strength", 0),
      (assign, ":enemy_strength", 0),
      (store_faction_of_party, ":party_faction", ":party_no"),
	  ##diplomacy start+ add support for promoted kingdom ladies
      (store_add, ":end_cond", heroes_end, 1),#<- changed active_npcs to heroes
      (try_for_range, ":iteration", heroes_begin, ":end_cond"),#<- changed active_npcs to heroes
        (try_begin),
          (eq, ":iteration", heroes_end),#<- changed active_npcs to heroes
          (assign, ":cur_troop", "trp_player"),
        (else_try),
          (assign, ":cur_troop", ":iteration"),
        (try_end),
		##diplomacy end+

        (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
        (ge, ":cur_troop_party", 0),
        (party_is_active, ":cur_troop_party"),


        #I moved these lines here from (*1) to faster process, ozan.
        (store_troop_faction, ":army_faction", ":cur_troop"),
        (store_relation, ":relation", ":army_faction", ":party_faction"),
        (this_or_next|neq, ":relation", 0),
        (eq, ":army_faction", ":party_faction"),
        #ozan end


        (neq, ":party_no", ":cur_troop_party"),
        (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
        (try_begin),
          (neg|is_between, ":party_no", centers_begin, centers_end),
          (party_slot_eq, ":cur_troop_party", slot_party_ai_state, spai_accompanying_army),
          (party_get_slot, ":commander_party", ":cur_troop_party", slot_party_ai_object),
          (eq, ":commander_party", ":party_no"),
          (val_add, ":follower_strength", ":str"),
        (else_try),
          (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":party_no"),
          (lt, ":distance", 20),

          #(*1)

          (try_begin),
            (lt, ":distance", 5),
            (assign, ":str_divided", ":str"),
          (else_try),
            (lt, ":distance", 10),
            (store_div, ":str_divided", ":str", 2),
          (else_try),
            (lt, ":distance", 15),
            (store_div, ":str_divided", ":str", 4),
          (else_try),
            (store_div, ":str_divided", ":str", 8),
          (try_end),

          (try_begin),
            (this_or_next|eq, ":army_faction", ":party_faction"),
            (gt, ":relation", 0),
            (val_add, ":friend_strength", ":str_divided"),
          (else_try),
            (lt, ":relation", 0),
            (val_add, ":enemy_strength", ":str_divided"),
          (try_end),
        (try_end),
      (try_end),

      (party_set_slot, ":party_no", slot_party_follower_strength, ":follower_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_friend_strength, ":friend_strength"),
      (party_set_slot, ":party_no", slot_party_nearby_enemy_strength, ":enemy_strength"),
      ])
]
