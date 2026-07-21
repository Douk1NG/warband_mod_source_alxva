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

update_tavern_travellers_scripts = [
#script_update_ransom_brokers
# INPUT: none
# OUTPUT: none
("update_tavern_travellers",
    [
    (try_for_range, ":town_no", towns_begin, towns_end),
      (neg|party_slot_ge, ":town_no", slot_center_is_besieged_by, 1), #keep in center
      (party_set_slot, ":town_no", slot_center_tavern_traveler, 0),
    (try_end),

    (try_for_range, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
      (store_random_in_range, ":town_no", towns_begin, towns_end),
      (troop_get_slot, ":cur_center", ":troop_no", slot_troop_cur_center),
      (assign, ":end_cond", 15), #default tries to set info faction slot
      (try_begin), #not landed, skip condition
        (le, ":cur_center", 0),
        (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"),
      (else_try),
        (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
        (neg|party_slot_ge, ":cur_center", slot_center_is_besieged_by, 1), #can't travel
        (party_set_slot, ":town_no", slot_center_tavern_traveler, ":troop_no"),
        (troop_set_slot, ":troop_no", slot_troop_cur_center, ":town_no"), #SB : set troop slot
        (store_faction_of_party, ":cur_faction", ":cur_center"),
        (neq, ":cur_faction", "$players_kingdom"),
        (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":cur_faction"),
        (assign, ":end_cond", 0), #we set this above
      (try_end),

      #info faction
      (try_for_range, ":unused", 0, ":end_cond"),
        (store_random_in_range, ":info_faction", npc_kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":info_faction", slot_faction_state, sfs_active),
        (neq, ":info_faction", "$players_kingdom"),
        # (neq, ":info_faction", "fac_player_supporters_faction"),
        (party_set_slot, ":town_no", slot_center_traveler_info_faction, ":info_faction"),
        (assign, ":end_cond", 0),
      (try_end),
    (try_end),

     #SB : let its own script update every 24 hours
	 # (troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "p_town_1"),
     ])
]
