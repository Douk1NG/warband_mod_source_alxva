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



  # Policy
   

policy_simple_triggers = [
(30 * 24,
   [
	##nested diplomacy start+
	##If the player is ruler or co-ruler of an NPC kingdom, make sure the
	#policy matches fac_player_supporters_faction.  (It should be synchronized
	#elsewhere, but do it here in case there has been an error.)
	(assign, ":player_is_coruler_of_npc_faction", 0),
	  (try_begin),
		(neq, "$players_kingdom", "fac_player_supporters_faction"),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		(assign, ":player_is_coruler_of_npc_faction", 1),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_serfdom),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom, reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_centralization),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_centralization, reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_quality),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality, reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_aristocracy),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy, reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_mercantilism),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, reg0),
	(try_end),
	##nested diplomacy end+
  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
    (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),

    (faction_get_slot, ":centralization", ":kingdom", dplmc_slot_faction_centralization),
    (faction_get_slot, ":aristocracy", ":kingdom", dplmc_slot_faction_aristocracy),
    (faction_get_slot, ":quality", ":kingdom", dplmc_slot_faction_quality),
    (faction_get_slot, ":serfdom", ":kingdom", dplmc_slot_faction_serfdom),
	 ##nested diplomacy start+
    (faction_get_slot, ":mercantilism", ":kingdom", dplmc_slot_faction_mercantilism),
	 ##nested diplomacy end+

    (try_begin),
      (eq, "$cheat_mode", 1),
      (str_store_faction_name, s9, ":kingdom"),
      (assign, reg1, ":centralization"),
      (display_message, "@{!}DEBUG - centralization {reg1}"),
      (assign, reg1, ":aristocracy"),
      (display_message, "@{!}DEBUG - aristocracy {reg1}"),
      (assign, reg1, ":quality"),
      (display_message, "@{!}DEBUG - quality {reg1}"),
      (assign, reg1, ":serfdom"),
      (display_message, "@{!}DEBUG - serfdom {reg1}"),
		##nested diplomacy start+
      (assign, reg1, ":mercantilism"),
      (display_message, "@{!}DEBUG - mercantilism {reg1}"),
		##nested diplomacy end+
    (try_end),

    (try_begin),
      (is_between, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      ##nested diplomacy start+
      ##Ensure the player isn't the kingdom's ruler or co-ruler
      (this_or_next|neq, ":kingdom", "$players_kingdom"),
      (eq, ":player_is_coruler_of_npc_faction", 0),
      ##Add the chance to move around mercantilism.
      #(store_random_in_range, ":random", 0, 8),
      (store_random_in_range, ":random", 0, 10),
      ##nested diplomacy end+

      (try_begin),
        ##nested diplomacy start+
        #(is_between, ":random", 1, 5),
        (is_between, ":random", 1, 6),
        ##nested diplomacy end+
        (store_random_in_range, ":change", -1, 2),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s12, ":kingdom"),
          (assign, reg1, ":change"),
          (assign, reg2, ":random"),
          (display_message, "@{!}DEBUG - changing {reg1} of {reg2} for {s12}"),
        (try_end),

        (try_begin),
          (eq, ":random", 1),
          (val_add, ":centralization", ":change"),
          (val_max, ":centralization", -3),
          (val_min, ":centralization", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_centralization, ":centralization"),
        (else_try),
          (eq, ":random", 2),
          (val_add, ":aristocracy", ":change"),
          (val_max, ":aristocracy", -3),
          (val_min, ":aristocracy", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_aristocracy, ":aristocracy"),
        (else_try),
          (eq, ":random", 3),
          (val_add, ":quality", ":change"),
          (val_max, ":quality", -3),
          (val_min, ":quality", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_quality, ":quality"),
        (else_try),
          (eq, ":random", 4),
          (val_add, ":serfdom", ":change"),
          (val_max, ":serfdom", -3),
          (val_min, ":serfdom", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_serfdom, ":serfdom"),
          ##nested diplomacy start+
          (eq, ":random", 5),
          (val_add, ":mercantilism", ":change"),
          (val_clamp, ":mercantilism", -3, 4),#-3 min, +3 max
          (faction_set_slot, ":kingdom", dplmc_slot_faction_mercantilism, ":mercantilism"),
          ##nested diplomacy end+
        (try_end),
      (try_end),

    (else_try),

      #only player faction is affected by relation hits
      ##nested diplomacy start+
      ##Don't alter the values of centralization and aristocracy, since that's confusing.
      #(store_mul, ":centralization", ":centralization", -1),
      #(store_mul, ":aristocracy", ":aristocracy", 1),
      #(store_add, ":relation_change", ":centralization", ":aristocracy"),

		(store_sub, ":relation_change", ":aristocracy", ":centralization"),
      ##custodian (merchant) lords like plutocracy, unlike ordinary lords
      (store_mul, ":custodian_change", ":aristocracy", -1),
		(val_sub, ":custodian_change", ":centralization"),
      #benefactor lords like freedom and dislike serfdom
		(store_mul, ":benefactor_change", ":serfdom", -1),
		(val_sub, ":custodian_change", ":centralization"),
      ##nested diplomacy end+
      (try_begin),
        ##nested diplomacy start+
        (this_or_next|neq, ":benefactor_change", 0),
        (this_or_next|neq, ":custodian_change", 0),
        ##nested diplomacy end+
        (neq, ":relation_change", 0),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s9, ":kingdom"),
          (assign, reg1, ":relation_change"),
          (display_message, "@{!}DEBUG - relation_change =  {reg1} for {s9}"),
        (try_end),

        ##diplomacy start+ also include kingdom ladies who are kingdom heroes
        #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
        ##diplomacy end+
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (store_troop_faction, ":faction_no", ":troop_no"),
          (eq, ":kingdom", ":faction_no"),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          ##diplomacy start+
          (neq, ":troop_no", ":faction_leader"),
          (assign, ":change_for_troop", ":relation_change"),
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
             (assign, ":change_for_troop", ":custodian_change"),
          (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
             (assign, ":change_for_troop", ":benefactor_change"),
          (try_end),
          ##Extra penalty for going back on a promise, extra bonus for keeping it
          (assign, ":promise_mod", 0),
          (try_begin),
             ##Following are only relevant for companions
				 (is_between, ":troop_no", companions_begin, companions_end),
             (troop_slot_eq, ":troop_no", slot_troop_kingsupport_state, 1),
             (try_begin),
                #Argument: Lords
                (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_lords),
                (try_begin),
                  #If more than slightly centralized, or more than slightly balanced against aristocrats
                  (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                     (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
                  (val_sub, ":promise_mod", 1),
                (else_try),
                  #If more than slightly decentralized or more than slightly balanced in favor of aristocrats
                  (this_or_next|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, 2),
                  (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, -2),
                  (faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),#redundant
                  (val_add, ":promise_mod", 1),
                (try_end),
             (else_try),
                  #Argument: Commons
                  (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_commons),
                  (try_begin),
                    (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
                    (val_sub, ":promise_mod", 1),
                  (else_try),
                    (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 0),
                    (store_add, ":local_temp", ":serfdom", ":aristocracy"),
                    (lt, ":local_temp", 0),
                    (val_add, ":promise_mod", 1),
                  (try_end),
             (try_end),
         (try_end),
         #Check other broken promises
         (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_lords),
             (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
             (val_sub, ":promise_mod", 1),
         (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_commons),
             (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (val_sub, ":promise_mod", 1),
         (try_end),
         (val_clamp, ":promise_mod", -1, 2),#-1, 0, or 1
         (val_add, ":change_for_troop", ":promise_mod"),

		 (neq, ":change_for_troop", 0),
		 (call_script, "script_change_player_relation_with_troop", ":troop_no", ":change_for_troop"),
        ##diplomacy end+
        (try_end),
      (try_end),
    (try_end),
  (try_end),
  ]),
]
