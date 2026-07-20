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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_evaluate_fief_exchange_scripts = [
#Decide whether an NPC wants to exchange a fief or not.
#
# param#1 is NPC being asked
# param#2 is that NPC's fief being asked for
# param#3 is the one asking (usually the player)
# param#4 is the fief being offered in exchange
#
# Result is returned in reg0.  Negative means "no", zero means "yes",
# positive means "yes but you have to pay me this amount".
# If the result is negative, the response string is stored in s14.
("dplmc_evaluate_fief_exchange",
    [
      (store_script_param, ":target_npc", 1),
      (store_script_param, ":target_fief", 2),
      (store_script_param, ":asker", 3),
      (store_script_param, ":offered_fief", 4),

      (assign, ":result", -1),
      (assign, reg0, ":result"),
      (str_store_string, s14, "str_ERROR_string"),

      (try_begin),
          #Both NPCs are valid, and are not same character.  One can be the player.
          (neq, ":target_npc", ":asker"),
          (is_between, ":target_npc", heroes_begin, heroes_end),
          (this_or_next|is_between, ":asker", heroes_begin, heroes_end),
             (eq,":asker","trp_player"),
          #Both fiefs are valid and owned by the lords in the arguments
          (is_between, ":target_fief", centers_begin, centers_end),
          (party_slot_eq, ":target_fief", slot_town_lord, ":target_npc"),
          (is_between, ":offered_fief", centers_begin, centers_end),
          (party_slot_eq, ":offered_fief", slot_town_lord, ":asker"),
          #The lords are in the same faction
          (store_troop_faction, ":target_faction", ":target_npc"),
          (store_troop_faction, ":asker_faction", ":asker"),
          (try_begin),
             #Special handling needed for player faction
             (eq, ":asker", "trp_player"),
             (neg|eq, ":target_faction", ":asker_faction"),
             (assign, ":asker_faction", "$players_kingdom"),
          (try_end),
          (this_or_next|eq, ":target_faction", ":asker_faction"),
             (this_or_next|faction_slot_eq,":target_faction",slot_faction_leader,":asker"),
             (faction_slot_eq,":asker_faction",slot_faction_leader,":target_npc"),
          #Get prosperity for use in later tests
          (party_get_slot, ":target_prosperity", ":target_fief", slot_town_prosperity),
          (party_get_slot, ":offered_prosperity", ":offered_fief", slot_town_prosperity),
          (store_div, ":min_prosperity", ":target_prosperity", 10),
          (val_mul, ":min_prosperity", 10),
          #...take into account relation
          (call_script, "script_troop_get_relation_with_troop", ":target_npc", ":asker"),
          (store_div, ":relation_div_10", reg0, 10),
          (val_sub, ":min_prosperity", ":relation_div_10"),
          #...take into account persuasion
          (store_skill_level, ":asker_persuasion", "skl_persuasion", ":asker"),
          (val_sub, ":min_prosperity", ":asker_persuasion"),
          #...take into account personal (not party) trade skill
          (store_skill_level, ":asker_trade", "skl_trade", ":asker"),
          (val_sub, ":min_prosperity", ":asker_trade"),
          #...don't let it rise above original's prosperity.
          (val_min, ":min_prosperity", ":target_prosperity"),
          #target_type 1 = village, 2 = castle, 3 = town
		  (assign, ":target_type", 0),
          (try_begin),
            (party_slot_eq, ":target_fief", slot_party_type, spt_town),
            (assign, ":target_type", 3),
          (else_try),
            (party_slot_eq, ":target_fief", slot_party_type, spt_castle),
            (assign, ":target_type", 2),
          (else_try),
  		    (party_slot_eq, ":target_fief", slot_party_type, spt_village),
            (assign, ":target_type", 1),
          (try_end),
		  (ge, ":target_type", 1),#break with error if the type was bad
          #offered_type: 1 = village, 2 = castle, 3 = town
		  (assign, ":offered_type", 0),
          (try_begin),
            (party_slot_eq, ":offered_fief", slot_party_type, spt_town),
            (assign, ":offered_type", 3),
          (else_try),
            (party_slot_eq, ":offered_fief", slot_party_type, spt_castle),
            (assign, ":offered_type", 2),
          (else_try),
			(party_slot_eq, ":offered_fief", slot_party_type, spt_village),
            (assign, ":offered_type", 1),
          (try_end),
		  (ge, ":offered_type", 1),#break with error if the type was bad
          #Now execute comparison logic:
          (try_begin),
            #refuse to trade town for a castle or village
            (lt, ":offered_type", ":target_type"),
            (eq, ":target_type", 3),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_town"),
          (else_try),
            #refuse to trade any better type for a worse type
            (lt, ":offered_type", ":target_type"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_castle"),
          (else_try),
            #refuse to trade for something under siege or being raided
            (this_or_next|party_slot_eq, ":offered_fief", slot_village_state, svs_under_siege),
            (party_slot_eq, ":offered_fief", slot_village_state, svs_being_raided),
            (str_store_party_name, s14, ":offered_fief"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_s14_attack"),
          (else_try),
            #accept a trade if the offered type is better
            (lt, ":target_type", ":offered_type"),
            (str_store_string, s14, "str_dplmc_fief_exchange_accept"),
            (assign, ":result", 0),
		  (else_try),
			#refuse to trade away home center (unless trading up for a better type)
			#Target fief is home of NPC...
			(this_or_next|party_slot_eq, ":target_fief", dplmc_slot_center_original_lord, ":target_npc"),
			   (troop_slot_eq, ":target_npc", slot_troop_home, ":target_fief"),
			(neg|party_slot_eq, ":offered_fief", dplmc_slot_center_original_lord, ":target_npc"),
			#...and offered fief is not.
			(neg|troop_slot_eq, ":target_npc", slot_troop_home, ":offered_fief"),
			(this_or_next|neg|is_between, ":target_npc", companions_begin, companions_end),
				(neg|troop_slot_eq, ":target_npc", slot_troop_town_with_contacts, ":offered_fief"),
			(str_store_party_name, s14, ":target_fief"), #Line added by zerilius
			(str_store_string, s14, "str_dplmc_fief_exchange_refuse_home"),
          (else_try),
            #refuse trade if prosperity is too low
            (lt, ":offered_prosperity", ":min_prosperity"),
            (str_store_string, s14, "str_dplmc_fief_exchange_refuse_rich"),
          (else_try),
            #accept trade for 0 or more denars
            (store_sub, ":result", ":target_prosperity", ":offered_prosperity"),
            (val_mul, ":result", ":target_type"),
            (val_mul, ":result", 36),#Should probably be 60 instead
            #(val_div, ":result", 100),
            (val_add, ":result", 2000),
            (val_max, ":result", 0),
            (try_begin),
               (ge, ":result", 1),
               (assign, reg3, ":result"),
               (str_store_string, s14, "str_dplmc_fief_exchange_accept_reg3_denars"),
            (else_try),
               (str_store_string, s14, "str_dplmc_fief_exchange_accept"),
            (try_end),
          (try_end),
      (try_end),
      (assign, reg0, ":result"),
    ])
]
