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



 #process messengers
 

process_messengers_simple_triggers = [
(0.5,
 [
  (try_for_parties, ":party_no"),
    (party_slot_eq,":party_no", slot_party_type, spt_messenger),

    (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
    (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),

    (try_begin),
      (party_is_active, ":target_party"),
      (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
      (str_store_party_name, s14, ":party_no"),
      (str_store_party_name, s15,":target_party"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (assign, reg0, ":distance_to_target"),
        (display_message, "@Distance between {s14} and {s15}: {reg0}"),
      (try_end),

      (try_begin),
        (le, ":distance_to_target", 1),

        (try_begin), # returning to p_main_party
          (eq, ":target_party", "p_main_party"),
          (party_get_slot, ":party_leader", ":party_no", slot_party_orders_object),
          (party_get_slot, ":success", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_messenger", ":party_leader", ":success"),
          (remove_party, ":party_no"),
        (else_try), # patrols
          (party_slot_eq, ":target_party", slot_party_type, spt_patrol),
          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),

          #SB : quick string to strings
          (try_begin),
            (eq, ":message", spai_undefined),
            (remove_party, ":target_party"),
          (else_try),
            (eq, ":message", spai_retreating_to_center),
            (str_store_party_name, s5, ":orders_object"),
            (party_set_name, ":target_party", "str_s5_transfer"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_state, spai_retreating_to_center),
            (party_set_aggressiveness, ":target_party", 0),
            (party_set_courage, ":target_party", 3),
            (party_set_ai_initiative, ":target_party", 100),
          (else_try),
            (str_store_party_name, s5, ":orders_object"),
            (party_set_name, ":target_party", "str_s5_patrol"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_orders_type, ":message"),
          (try_end),

          (remove_party, ":party_no"),
        (else_try), # SB : reached a center (waypoint) as target troop has not yet spawned
          (is_between, ":target_party", walled_centers_begin, walled_centers_end),
          (party_get_slot, ":target_troop", ":party_no", dplmc_slot_party_origin),
          (try_begin), #retarget
            (troop_get_slot, ":leaded_party", ":target_troop", slot_troop_leaded_party),
            (gt, ":leaded_party", 0),
            (party_is_active, ":leaded_party"),
            (neg|party_is_in_town, ":leaded_party", ":target_party"), #camping for some reason
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", ":leaded_party"),
            (party_set_slot, ":party_no", slot_party_ai_object, ":leaded_party"), #drop down to the condition below
          (try_end),
        (else_try), # reached any other target
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (display_log_message, "@Your messenger reached {s13}.", 0x00FF00),
            (assign, "$g_talk_troop", ":party_leader"), #debug
          (try_end),

          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),
          (assign, ":success", 0),
          (try_begin),
            (party_set_slot, ":target_party", slot_party_commander_party, "p_main_party"),
          	(store_current_hours, ":hours"),
          	(party_set_slot, ":target_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
          	(party_set_slot, ":target_party", slot_party_orders_object, ":orders_object"),
          	(party_set_slot, ":target_party", slot_party_orders_type, ":message"),

          	(party_set_slot, ":target_party", slot_party_orders_time, ":hours"),
            (call_script, "script_npc_decision_checklist_party_ai", ":party_leader"), #This handles AI for both marshal and other parties


            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (display_message, "@{s14}"), #debug
            (try_end),

            (try_begin),
              (eq, reg0, ":message"),
              (eq, reg1, ":orders_object"),
              (assign, ":success", 1),
            (try_end),
            (call_script, "script_party_set_ai_state", ":target_party", reg0, reg1),
          (try_end),

          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", "p_main_party"),
          (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
          (party_set_slot, ":party_no", slot_party_orders_object, ":party_leader"),
          (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":success"),
        (try_end),
      (try_end),
    (else_try),
      #SB : it's to its
      (display_log_message, "@Your messenger has lost its way and gave up your mission!", message_defeated),
      (remove_party, ":party_no"),
    (try_end),
  (try_end),
 ]),
]
