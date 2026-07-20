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

update_volunteer_troops_in_village_scripts = [
#script_update_volunteer_troops_in_village
# INPUT: arg1 = center_no
# OUTPUT: none
("update_volunteer_troops_in_village",
    [
       (store_script_param, ":center_no", 1),
       (party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
       (party_get_slot, ":center_culture", ":center_no", slot_center_culture),


##	   (try_begin),
##		(eq, "$cheat_mode", 2),
##	    (str_store_party_name, s4, ":center_no"),
##	    (str_store_faction_name, s5, ":center_culture"),
##	    (display_message, "str_updating_volunteers_for_s4_faction_is_s5"),
##	   (try_end),

       (faction_get_slot, ":volunteer_troop", ":center_culture", slot_faction_tier_1_troop),
       (assign, ":volunteer_troop_tier", 1),
       (store_div, ":tier_upgrades", ":player_relation", 10),
       (try_for_range, ":unused", 0, ":tier_upgrades"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 10),
         (store_random_in_range, ":random_no", 0, 2),
         (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", ":random_no"),
         (try_begin),
           (le, ":upgrade_troop_no", 0),
           (troop_get_upgrade_troop, ":upgrade_troop_no", ":volunteer_troop", 0),
         (try_end),
         (gt, ":upgrade_troop_no", 0),
         (val_add, ":volunteer_troop_tier", 1),
         (assign, ":volunteer_troop", ":upgrade_troop_no"),
       (try_end),

       (assign, ":upper_limit", 8),
       (try_begin),
         (ge, ":player_relation", 4),
         (assign, ":upper_limit", ":player_relation"),
         (val_div, ":upper_limit", 2),
         (val_add, ":upper_limit", 6),
       (else_try),
         (lt, ":player_relation", 0),
         (assign, ":upper_limit", 0),
       (try_end),


##diplomacy begin
      (assign, ":percent", 100),
      (try_begin), #-30% if not owner
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (val_sub, ":percent", 30),
      (try_end),
      (try_begin), #1%/4 renown
        (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
        (val_div, ":player_renown", 4),
        (val_add, ":percent", ":player_renown"),
      (try_end),
      (try_begin), #1%/3 honour
        (assign, ":player_honour", "$player_honor"),
        (val_div, ":player_honour", 3),
        (val_add, ":percent", ":player_honour"),
      (try_end),
      (try_begin), #+5% if king
        (faction_get_slot, ":faction_leader", "fac_player_supporters_faction", slot_faction_leader),
        (eq, ":faction_leader", "trp_player"),
        (val_add, ":percent", 5),

        (try_begin), #-5% for each point of serfdom
          (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
          (neq, ":serfdom", 0),
          (val_mul, ":serfdom", 5),
          (val_sub, ":percent", ":serfdom"),
        (try_end),

        (try_begin),  #+5% if king of village
          (store_faction_of_party, ":faction", ":center_no"),
          (eq, ":faction", "fac_player_supporters_faction"),
          (val_add, ":percent", 5),
        (try_end),
      (try_end),

      (try_begin),
        (gt, ":upper_limit", 0),
        (val_clamp, ":percent", 0, 201),
        (val_mul, ":upper_limit", ":percent"),
        (val_div, ":upper_limit", 100),
      (try_end),

##diplomacy end


       (val_mul, ":upper_limit", 3),
       (store_add, ":amount_random_divider", 2, ":volunteer_troop_tier"),
       (val_div, ":upper_limit", ":amount_random_divider"),

       (store_random_in_range, ":amount", 0, ":upper_limit"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_type, ":volunteer_troop"),
       (party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":amount"),
     ])
]
