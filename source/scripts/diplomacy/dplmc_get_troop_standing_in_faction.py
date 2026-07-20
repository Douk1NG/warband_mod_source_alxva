# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_get_troop_standing_in_faction (script)
# Called by menus in 11 domains: battle, camp, castle, center_management, diplomacy, notifications, reports, siege, tournament, town, village
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

dplmc_get_troop_standing_in_faction_scripts = [
#script_dplmc_get_terrain_code_for_battle
#
#INPUT: arg1  :troop_no
#       arg2  :faction_no
#
#OUTPUT:
#       reg0  A constant with the value DPLMC_FACTION_STANDING_<something>
#
## Constants defined in module_constants.py
#DPLMC_FACTION_STANDING_LEADER = 60
#DPLMC_FACTION_STANDING_LEADER_SPOUSE = 50
#DPLMC_FACTION_STANDING_MARSHALL = 40
#DPLMC_FACTION_STANDING_LORD = 30
#DPLMC_FACTION_STANDING_DEPENDENT = 20
#DPLMC_FACTION_STANDING_MEMBER = 10#includes mercenaries
#DPLMC_FACTION_STANDING_PETITIONER = 5
#DPLMC_FACTION_STANDING_UNAFFILIATED = 0
##diplomacy end+
("dplmc_get_troop_standing_in_faction",
 [
    (store_script_param_1, ":troop_no"),
    (store_script_param_2, ":faction_no"),

    (assign, ":standing", DPLMC_FACTION_STANDING_UNAFFILIATED),
    (assign, ":original_faction_no", ":faction_no"),
    (try_begin),
        #Translate fac_player_faction
        (eq, ":faction_no", "fac_player_faction"),
        (assign, ":faction_no", "fac_player_supporters_faction"),
    (try_end),

    (try_begin),
       (this_or_next|lt, ":troop_no", 0),#Do nothing, bad troop ID
          (lt, ":faction_no", 0),#Do nothing, bad faction
    (else_try),
       #Because of how this script is used, if fac_player_supporters_faction is active,
       # this always reports that the player is its leader (even though that is sometimes
       # untrue, for example in a claimant quest)
       (eq, ":troop_no", "trp_player"),#Short-circuit the remainder if these are true
       (eq, ":faction_no", "fac_player_supporters_faction"),
       (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
       # (neg|is_between, "$supported_pretender", pretenders_begin, pretenders_end), #SB : claimant exception
       (assign, ":standing", DPLMC_FACTION_STANDING_LEADER),
    (else_try),
		(try_begin),
			#Translate fac_player_supporters_faction
			(eq, ":faction_no", "fac_player_supporters_faction"),
			(gt, "$players_kingdom", 0),
			(assign, ":faction_no", "$players_kingdom"),
		(try_end),

        (store_faction_of_troop, ":troop_faction", ":troop_no"),
        (try_begin),
           #Translate fac_player_supporters_faction
           (this_or_next|eq, ":troop_no", "trp_player"),
           (this_or_next|eq, ":troop_faction", "fac_player_faction"),
           (eq, ":troop_faction", "fac_player_supporters_faction"),
           (assign, ":troop_faction", "fac_player_supporters_faction"),
           (gt, "$players_kingdom", 0),
           (assign, ":troop_faction", "$players_kingdom"),
        (try_end),
        (eq, ":troop_faction", ":faction_no"),#<- Short-circuit the remainder if this is false
        (assign, ":standing", DPLMC_FACTION_STANDING_MEMBER),

        (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
        (try_begin),
           #Faction leader
           (eq, ":faction_leader", ":troop_no"),
           (assign, ":standing", DPLMC_FACTION_STANDING_LEADER),
        (else_try),
           #Spouse of faction leader
           (gt, ":faction_leader", -1),
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
              (troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
           #Deal with possible uninitialized slot
           (this_or_next|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
           (this_or_next|neq, ":faction_leader", 0),
              (is_between, ":troop_no", heroes_begin, heroes_end),
           (assign, ":standing", DPLMC_FACTION_STANDING_LEADER_SPOUSE),
        (else_try),
           #Faction marshall
           (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
           (assign, ":standing", DPLMC_FACTION_STANDING_MARSHALL),
        (else_try),
           #If the troop is the player, if he has homage he is a lord.
           #Otherwise he is a mercenary.
           (eq, ":troop_no", "trp_player"),
           (try_begin),
              (this_or_next|eq, ":faction_no", "fac_player_supporters_faction"),
              (ge, "$player_has_homage", 1),
              (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
           (else_try),
              #If the player is married to a lord/lady in the faction, the
              #homage variable should always be set to 1+, but add a separate
              #check just in case.
              (troop_get_slot, reg0, "trp_player", slot_troop_spouse),
              (is_between, reg0, heroes_begin, heroes_end),
              (store_faction_of_troop, reg0, reg0),
              (this_or_next|eq, reg0, "fac_player_supporters_faction"),
              (eq, reg0, ":faction_no"),
              (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
           (try_end),
        (else_try),
            #None of the following conditions apply for non-heroes
            (this_or_next|lt, ":troop_no", heroes_begin),
                (neg|troop_is_hero, ":troop_no"),
        (else_try),
           #For kingdom heroes, part 1 (check lordship based on occupation)
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
           (this_or_next|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_lord_rejoined),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
           (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
        (else_try),
           #For kingdom ladies
           (this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
              (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
           (assign, ":standing", DPLMC_FACTION_STANDING_DEPENDENT),
        (else_try),
           #For petitioners
           (eq, ":original_faction_no", "fac_player_supporters_faction"),
           (is_between, ":troop_no", lords_begin, lords_end),
           (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
           (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
           (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
           (assign, ":standing", DPLMC_FACTION_STANDING_PETITIONER),
        (else_try),
            #For kingdom heroes, part 2 (all non-companion active NPCs)
            (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
            (neg|is_between, ":troop_no", companions_begin, companions_end),
            (assign, ":standing", DPLMC_FACTION_STANDING_LORD),
        (try_end),
    (try_end),

    (assign, reg0,  ":standing"),
 ])
]
