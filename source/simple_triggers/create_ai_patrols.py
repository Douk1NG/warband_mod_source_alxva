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



  #create ai patrols
   

create_ai_patrols_simple_triggers = [
(24 * 7,
   [
    (try_for_range, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),

      (assign, ":max_patrols", 0),
      (try_for_range, ":center", towns_begin, towns_end),
        (store_faction_of_party, ":center_faction", ":center"),
        (eq, ":center_faction", ":kingdom"),
        (val_add, ":max_patrols", 1),
      (try_end),

      (assign, ":count", 0),
      (try_for_parties, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":kingdom"),
        (neg|party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"), #not player ordered
        (try_begin),
           #Remove patrols above the maximum number allowed.
           (ge, ":count", ":max_patrols"),
           (try_begin),
              (ge, "$cheat_mode", 1),
              (str_store_faction_name, s4, ":kingdom"),
              (str_store_party_name, s5, ":party_no"),
              (display_message, "@{!}DEBUG - Removed {s5} because {s4} cannot support that many patrols"),
           (try_end),
           (remove_party, ":party_no"),
        (else_try),
           (val_add, ":count", 1),
        (try_end),
      (try_end),

      (try_begin),
        (lt, ":count", ":max_patrols"),

        (store_random_in_range, ":random", 0, 10),
        (le, ":random", 3),

        (assign, ":start_center", -1),
        (assign, ":target_center", -1),

        (try_for_range, ":center", towns_begin, towns_end),
          (store_faction_of_party, ":center_faction", ":center"),
          (eq, ":center_faction", ":kingdom"),

          (eq, ":start_center", -1),
          (eq, ":target_center", -1),

          (assign, ":continue", 1),
          (try_for_parties, ":party_no"),
            (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
            (store_faction_of_party, ":party_faction", ":party_no"),
            (eq, ":party_faction", ":kingdom"),
            (party_get_slot, ":target", ":party_no", slot_party_ai_object),
            (eq, ":target", ":center"),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),

          (call_script, "script_cf_select_random_town_with_faction", ":kingdom"),
          (neq, reg0, -1),

          (assign, ":start_center", reg0),
          (assign, ":target_center", ":center"),
        (try_end),

        (try_begin),
          (neq, ":start_center", -1),
          (neq, ":target_center", -1),
          (store_random_in_range, ":random_size", 0, 3),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          (call_script, "script_dplmc_send_patrol", ":start_center", ":target_center", ":random_size",":kingdom", ":faction_leader"),
        (try_end),
      (try_end),
    (try_end),
    ]),
]
