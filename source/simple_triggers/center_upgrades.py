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



  # Checking center upgrades
  

center_upgrades_simple_triggers = [
(12,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot, ":cur_improvement", ":center_no", slot_center_current_improvement),
      (gt, ":cur_improvement", 0),
      (party_get_slot, ":cur_improvement_end_time", ":center_no", slot_center_improvement_end_hour),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", ":cur_improvement_end_time"),
      (party_set_slot, ":center_no", ":cur_improvement", 1),
      (party_set_slot, ":center_no", slot_center_current_improvement, 0),
      (call_script, "script_get_improvement_details", ":cur_improvement"),
      (try_begin),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (str_store_party_name, s4, ":center_no"),
        (display_log_message, "@Building of {s0} in {s4} has been completed."),
      (try_end),
      (try_begin),
        (is_between, ":center_no", villages_begin, villages_end),
        (try_begin),
          (eq, ":cur_improvement", slot_center_has_fish_pond),
          (call_script, "script_change_center_prosperity", ":center_no", 5),
        (else_try), #SB : show garrison for debug
          (eq, ":cur_improvement", slot_center_has_manor),
          (party_set_flags, ":center_no", pf_hide_defenders, 0),
        # (else_try),
          # (eq, ":cur_improvement", slot_center_has_messenger_post),
        (try_end),
      
      (try_end),
    (try_end),
    ]),
]
