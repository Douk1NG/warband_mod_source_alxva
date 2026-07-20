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

dplmc_time_sorted_heroes_for_center_scripts = [
# script_dplmc_time_sorted_heroes_for_center
# Input: arg1 = center_no, arg2 = party_no_to_collect_heroes
# Output: none, adds heroes to the party_no_to_collect_heroes party
# The catch is that it returns heroes who haven't been met in a day
# or more before others, for greater use in feasts.
("dplmc_time_sorted_heroes_for_center",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":party_no_to_collect_heroes"),
      (party_clear, ":party_no_to_collect_heroes"),

      #SB: include these heroes in sorting
      (try_begin),
        (eq, "$g_player_court", ":center_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (faction_slot_eq, ":center_faction", slot_faction_leader, "trp_player"),
        ##diplomacy start+
        #It's not exactly clear if this would work for kingdom ladies.  If they
        #can go from slto_kingdom_lady to slto_inactive, this could take them
        #from there to slto_kingdom_hero unintentionally.
        #
        #Because of this, don't enable this for now.  Elsewhere (where defections
        #occur) add alternate behavior for promoted kingdom ladies.
        #
        #TODO: Later, make sure that kingdom ladies are never inactive normally,
        #so this loop can be expanded to work with them.
        ##diplomacy end+
        (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
          (store_faction_of_troop, ":active_npc_faction", ":active_npc"),
          (eq, ":active_npc_faction", "fac_player_supporters_faction"),
          (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_inactive),
          (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she is not prisoner in any center.
          (neg|troop_slot_ge, ":active_npc", slot_troop_prisoner_of_party, 0), #if he/she does not have a party
          (neq, ":active_npc", "$g_player_minister"),
          (party_add_members, ":party_no_to_collect_heroes", ":active_npc"),
          # (set_visitor, ":cur_pos", ":active_npc"),
          # (val_add,":cur_pos", 1),
        (try_end),
      (try_end),

     #Non-attached pretenders (make sure they're not thrown under the bus)
     (try_for_range, ":pretender", pretenders_begin, pretenders_end),
        (neq, ":pretender", "$supported_pretender"),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, ":center_no"),
        (party_add_members, ":party_no_to_collect_heroes", ":pretender", 1),
     (try_end),

     #Heroes you haven't spoken to in 24+ hours
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", 24, -1),

     #Heroes you haven't spoken to in 12 to 24 hours
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", 12, 24),

     #Everyone else
     (call_script, "script_dplmc_time_sorted_heroes_for_center_aux",
         ":center_no", ":party_no_to_collect_heroes", -1, 12),
  ])
]
