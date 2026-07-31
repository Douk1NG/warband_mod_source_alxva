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



#TEMPORARILY DISABLED, AS READINESS IS NOW A PRODUCT OF NPC_DECISION_CHECKLIST
  # Changing readiness to join army
#   (10,
 #   [
 #     (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#		(eq, 1, 0),
#	    (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#        (assign, ":modifier", 1),
#        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
#          (ge, ":commander_party", 0),
#          (store_faction_of_party, ":faction_no", ":party_no"),
#          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
#          (ge, ":faction_marshall", 0),
#          (troop_get_slot, ":marshall_party", ":faction_marshall", slot_troop_leaded_party),
#          (eq, ":commander_party", ":marshall_party"),
#          (assign, ":modifier", -1),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_join_army, ":readiness"),
#        (assign, ":modifier", 1),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (store_troop_faction, ":troop_faction", ":troop_no"),
#          (eq, ":troop_faction", "fac_player_supporters_faction"),
#          (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (party_get_slot, ":party_ai_state", ":party_no", slot_party_ai_state),
#          (party_get_slot, ":party_ai_object", ":party_no", slot_party_ai_object),
#          #Check if party is following player orders
#          (try_begin),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_state, ":party_ai_state"),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_object, ":party_ai_object"),
#            (assign, ":modifier", -1),
#          (else_try),
#            #Leaving following player orders if the current party order is not the same.
#            (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#            (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#          (try_end),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_follow_orders),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_follow_orders, ":readiness"),
#        (try_begin),
#          (lt, ":readiness", 10),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#        (try_end),
#      (try_end),
 #     ]),

  # Process vassal ai
   

readiness_disabled_simple_triggers = [
(2,
   [
   (assign, "$fuck_stamina", 1), #This should actually be based on stats probably
   (try_begin),
   (eq, "$cheat_mode", 1),
   (assign, "$fuck_stamina", 6),
   (try_end),
   # (try_begin),
       # (neq, "$g_fix_rebel_ladies", 1),
       # (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
         # (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
         # (store_troop_faction, ":cur_faction", ":cur_troop"),
         # (eq, ":cur_faction", "fac_player_supporters_faction"),
         # (faction_get_slot, ":leader", ":cur_faction", slot_faction_leader),
         # (store_faction_of_troop, ":leader_faction", ":leader"),
         # (troop_set_faction, ":cur_troop", ":leader_faction"),
         # (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", ":leader_faction"),
       # (try_end),
       # (assign, "$g_fix_rebel_ladies", 1),
   # (try_end),

   # (try_begin),
       # (neq, "$g_fix_pretender_titles", 1),
       #fix pretender titles save games
       # (try_for_range, ":troop", pretenders_begin, pretenders_end),
           # (store_sub, ":offset", ":troop", pretenders_begin),
           # (store_add, ":kingdom", npc_kingdoms_begin, ":offset"),
           # (faction_slot_eq, ":kingdom", slot_faction_leader, ":troop"),
           # (call_script, "script_troop_set_title_according_to_faction", ":troop", ":kingdom"),
       # (try_end),
       # (assign, "$g_fix_pretender_titles", 1),
   # (try_end),
   
    # EMERGENCY WORKAROUND - root cause NOT yet found.
    # Bug: trp_player (a legitimate member of p_main_party in this mod) leaks into
    # foreign garrisons / other lords' parties after castle sieges (native battle merge).
    # This strips trp_player from any non-p_main_party party where it is a member,
    # while keeping it in p_main_party so siege/garrison leadership works.
    # TODO: find the actual siege merge/split path and remove this once fixed.
    #  (try_begin),
    #       (main_party_has_troop, "trp_player"),
    #       #Strip trp_player from any OTHER party it may be stuck in after a siege merge.
    #       (try_for_parties, ":party_no"),
    #          (neg|eq, ":party_no", "p_main_party"),
    #          (party_count_members_of_type, ":count", ":party_no", "trp_player"),
    #          (gt, ":count", 0),
    #          (party_remove_members, ":party_no", "trp_player", ":count"),
    #       (try_end),
    #    (else_try),
    #       (party_add_members, "p_main_party", "trp_player", 1),
    #       (display_message, "@DEBUG: PLAYER CHARACTER RESTORED TO PARTY",0xFF2222),
    #    (try_end),
   
    #   (call_script, "script_process_kingdom_parties_ai"),
      #moved to below trigger (per 1 hour) in order to allow it processed more frequent.
    ]),
]
