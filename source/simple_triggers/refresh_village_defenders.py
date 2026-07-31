# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *



  # Refresh number of cattle in villages
  

refresh_village_defenders_simple_triggers = [
(24 * 7,
   [
     (try_for_range, ":village_no", centers_begin, centers_end),
	  (neg|is_between, ":village_no", castles_begin, castles_end),
      (party_get_slot, ":num_cattle", ":village_no", slot_center_head_cattle),
      (party_get_slot, ":num_sheep", ":village_no", slot_center_head_sheep),
      (party_get_slot, ":num_acres", ":village_no", slot_center_acres_pasture),
	  (val_max, ":num_acres", 1),

	  (store_mul, ":grazing_capacity", ":num_cattle", 400),
	  (store_mul, ":sheep_addition", ":num_sheep", 200),
	  (val_add, ":grazing_capacity", ":sheep_addition"),
	  (val_div, ":grazing_capacity", ":num_acres"),
	  (try_begin),
		(eq, "$cheat_mode", 1),
	    (assign, reg4, ":grazing_capacity"),
		(str_store_party_name, s4, ":village_no"),
	    #(display_message, "@{!}DEBUG -- Herd adjustment: {s4} at {reg4}% of grazing capacity"),
	  (try_end),


      (store_random_in_range, ":random_no", 0, 100),
      (try_begin), #Disaster
        (eq, ":random_no", 0),#1% chance of epidemic - should happen once every two years
        (val_min, ":num_cattle", 10),

        (try_begin),
#          (eq, "$cheat_mode", 1),
#          (str_store_party_name, s1, ":village_no"),
#          (display_message, "@{!}Cattle in {s1} are exterminated due to famine."),
           ##diplomacy start+ Add display message for the player's own fiefs
		   #(store_distance_to_party_from_party, ":dist", "p_main_party", ":village_no"),
		   #(this_or_next|lt, ":dist", 30),
	          (gt, "$g_player_chamberlain", 0),
		   (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
		   (party_get_slot, reg4, ":village_no", slot_center_head_cattle),
		   (val_sub, reg4, ":num_cattle"),
		   (gt, reg4, 0),
		   (str_store_party_name_link, s4, ":village_no"),
		   (display_log_message, "@A livestock epidemic has killed {reg4} cattle in {s4}."),
		   ##diplomacy end+
        (try_end),

      (else_try), #Overgrazing
	    (gt, ":grazing_capacity", 100),

         (val_mul, ":num_sheep", 90), #10% decrease at number of cattles
         (val_div, ":num_sheep", 100),

         (val_mul, ":num_cattle", 90), #10% decrease at number of sheeps
         (val_div, ":num_cattle", 100),

       (else_try), #superb grazing
         (lt, ":grazing_capacity", 30),

         (val_mul, ":num_cattle", 120), #20% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (val_add, ":num_cattle", 1),

         (val_mul, ":num_sheep", 120), #20% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (val_add, ":num_sheep", 1),

       (else_try), #very good grazing
         (lt, ":grazing_capacity", 60),

         (val_mul, ":num_cattle", 110), #10% increase at number of cattles
         (val_div, ":num_cattle", 100),
		(val_add, ":num_cattle", 1),

         (val_mul, ":num_sheep", 110), #10% increase at number of sheeps
         (val_div, ":num_sheep", 100),
		(val_add, ":num_sheep", 1),

     (else_try), #good grazing
	    (lt, ":grazing_capacity", 100),
         (lt, ":random_no", 50),

         (val_mul, ":num_cattle", 105), #5% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (try_begin), #if very low number of cattles and there is good grazing then increase number of cattles also by one
           (le, ":num_cattle", 20),
			(val_add, ":num_cattle", 1),
		(try_end),

         (val_mul, ":num_sheep", 105), #5% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (try_begin), #if very low number of sheeps and there is good grazing then increase number of sheeps also by one
           (le, ":num_sheep", 20),
			(val_add, ":num_sheep", 1),
		(try_end),


     (try_end),

     (party_set_slot, ":village_no", slot_center_head_cattle, ":num_cattle"),
     (party_set_slot, ":village_no", slot_center_head_sheep, ":num_sheep"),
    (try_end),
    ]),
]
