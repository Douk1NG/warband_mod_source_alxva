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



  # Patrol ai
   

patrol_ai_simple_triggers = [
(2,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_patrol),

      # (call_script, "script_party_remove_all_prisoners", ":party_no"), #SB : retain prisoners

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),
        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),

        (try_begin),
          (gt, ":target_party", 0),
          (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
          (le, ":distance_to_target", 5),
          (try_begin), #SB : drop off prisoners
            (le, ":distance_to_target", 3),
            (is_between, ":target_party", walled_centers_begin, walled_centers_end),
            (call_script, "script_party_add_party_prisoners", ":target_party", ":party_no"),
            (call_script, "script_party_remove_all_prisoners", ":party_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
            (eq, ":ai_state", spai_retreating_to_center),
            (try_begin),
              (le, ":distance_to_target", 1),
              (call_script, "script_party_add_party", ":target_party", ":party_no"),
              (remove_party, ":party_no"),
            (try_end),
          (else_try),
            (party_get_position, pos1, ":target_party"),
            (party_set_ai_behavior,":party_no", ai_bhvr_patrol_location),
            (party_set_ai_patrol_radius, ":party_no", 1),
            (party_set_ai_target_position, ":party_no", pos1),
          (try_end),
          
        # (else_try),
          # #remove party?
        (try_end),

      (try_end),
    (try_end),
    ]),
]
