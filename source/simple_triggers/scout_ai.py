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



  # Scout ai
   

scout_ai_simple_triggers = [
(0.2,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_scout),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (this_or_next|eq, ":ai_behavior", ai_bhvr_travel_to_point),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),

        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
        (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
        (le, ":distance_to_target", 1),

        (try_begin),
          (eq, ":target_party", "p_main_party"),

          (party_get_slot, ":mission_target", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_scout", ":mission_target", 0),

          (remove_party, ":party_no"),
        (else_try),
          (neq, ":target_party", "p_main_party"),
          (party_get_slot, ":hours", ":party_no", dplmc_slot_party_mission_diplomacy),

          (try_begin),
            (le, ":hours", 100),
            (disable_party, ":party_no"),
            (val_add, ":hours", 1),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":hours"),

            (try_begin),
              (store_random_in_range, ":random", 0, 1000),
              (eq, ":random", 0),
              (str_store_party_name, s11, ":target_party"),
              (display_log_message, "@It is rumoured that a spy has been caught in {s11}.", 0xFF0000),
              (remove_party, ":party_no"),
            (try_end),

          (else_try),
            (enable_party, ":party_no"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", "p_main_party"),
            (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":target_party"),
          (try_end),

        (try_end),
      (try_end),
    (try_end),
    ]),
]
