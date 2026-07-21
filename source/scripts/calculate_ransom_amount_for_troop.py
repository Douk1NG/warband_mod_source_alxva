# ======================================================================
# SHARED DEPENDENCY
# Entity: calculate_ransom_amount_for_troop (script)
# Called by menus in 2 domains: diplomacy, town
# ======================================================================

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

calculate_ransom_amount_for_troop_scripts = [
("calculate_ransom_amount_for_troop",
    [(store_script_param, ":troop_no", 1),
     (store_troop_faction, ":faction_no", ":troop_no"),
     (assign, ":ransom_amount", 400),

	 (assign, ":male_relative", -9), #for kingdom ladies, otherwise a number otherwise unused in slot_town_lord
     (try_begin),
       (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
       (val_add, ":ransom_amount", 4000),
	 (else_try),
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
       (val_add, ":ransom_amount", 2500), #as though a renown of 1250 -- therefore significantly higher than for roughly equivalent lords
	   (call_script, "script_get_kingdom_lady_social_determinants", ":troop_no"),
	   (assign, ":male_relative", reg0),
     (try_end),

     (assign, ":num_center_points", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (this_or_next|party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
		 (party_slot_eq, ":cur_center", slot_town_lord, ":male_relative"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":num_center_points", 4),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":num_center_points", 2),
       (else_try),
         (val_add, ":num_center_points", 1),
       (try_end),
     (try_end),
     (val_mul, ":num_center_points", 500),
     (val_add, ":ransom_amount", ":num_center_points"),
     (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
     (val_mul, ":renown", 2),
     (val_add, ":ransom_amount", ":renown"),
     (store_mul, ":ransom_max_amount", ":ransom_amount", 3),
     (val_div, ":ransom_max_amount", 2),
     (store_random_in_range, ":random_ransom_amount", ":ransom_amount", ":ransom_max_amount"),
     (val_div, ":random_ransom_amount", 100),
     (val_mul, ":random_ransom_amount", 100),
     (assign, reg0, ":random_ransom_amount"),
     ])
]
