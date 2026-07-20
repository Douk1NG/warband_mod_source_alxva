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

dplmc_print_subordinate_says_sir_madame_to_s0_scripts = [
#script_dplmc_print_subordinate_says_sir_madame_to_s0
#
#In a number of circumstances a subordinate (a soldier in the player's employ) will refer
#to him as "sir" or "madame".  This is intended as a sign of respect, but becomes
#unintentionally disrespectful if the player would ordinarily merit a higher title.
#
#This function does not take into account the personal characteristics of the speaker in
#any way.  That logic should occur elsewhere.
#
#input: none
#output: reg0 gets a number corresponding to the title used
("dplmc_print_subordinate_says_sir_madame_to_s0",
        [
        (assign, ":highest_honor", 1),#{sir/madame}
        #1: str_dplmc_sirmadame
        #2: str_dplmc_my_lordlady
        #3: str_dplmc_your_highness
        (try_begin),
            #disable extra honors when the player is not recognized
            (gt, "$sneaked_into_town", disguise_none),
            (assign, ":highest_honor", 1),
        (else_try),
            #initialize variables for following steps
            (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
            (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
            #check if the player is the spouse of one of a widely recognized monarch,
            #or if the player is the ruler of one of the starting kingdoms (this can't happen but check anyway)
            (ge, ":player_spouse", 1),
            (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
                (this_or_next|faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
                (faction_slot_eq, ":faction_no", slot_faction_leader, ":player_spouse"),
                (val_max, ":highest_honor", 3),
            (try_end),
            (this_or_next|is_between, ":player_spouse", kings_begin, kings_end),
            (this_or_next|is_between, ":player_spouse", pretenders_begin, pretenders_end),
                (ge, ":highest_honor", 3),
            (val_max, ":highest_honor", 3),
            #Do not continue, since you've already used the highest available honor.
        (else_try),
            #the player is head of his own faction
            (ge, "$players_kingdom", 0),
            #faction leader is player, or faction leader is spouse and spouse is valid
            (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
                (faction_slot_eq, "$players_kingdom", slot_faction_leader, ":player_spouse"),
            (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
                (ge, ":player_spouse", 1),

            (faction_slot_eq, "$players_kingdom", slot_faction_state, sfs_active),
            (try_begin),
                #If you have sufficient right-to-rule and renown, your subjects
                #will call you "highness".
                (ge, "$player_right_to_rule", 10),
                (store_sub, reg0, 75 + 75, "$player_right_to_rule"),
                (val_mul, reg0, 1200 // 75),#minimum required renown (as an aside, 1200 is evenly divisibly by 75)
                #examples: at right to rule 50, renown must be at least 1600
                #          at right to rule 99, renown must be at least 816
                #          at right to rule 10, renown must be at least 2240
                (ge, ":player_renown", reg0),
                (val_max, ":highest_honor", 3),
            (else_try),
                #"Highness" is also used if the player's kingdom holds meaningful territory.
                (try_begin),
                    #Recalculate the cached value if it's suspicious
                    (faction_slot_eq, "$players_kingdom", slot_faction_num_castles, 0),
                    (faction_slot_eq, "$players_kingdom", slot_faction_num_towns, 0),
                    (call_script, "script_faction_recalculate_strength", "$players_kingdom"),
                (else_try),
                    #Recalculate the cached value if it's obviously wrong
                    (this_or_next|neg|faction_slot_ge, "$players_kingdom", slot_faction_num_castles, 0),
                    (neg|faction_slot_ge, "$players_kingdom", slot_faction_num_towns, 0),
                    (call_script, "script_faction_recalculate_strength", "$players_kingdom"),
                (try_end),
                #Territory points: castles = 2, towns = 3 (ignore villages)
                (faction_get_slot, ":territory_points", "$players_kingdom", slot_faction_num_towns),
                (val_mul, ":territory_points", 3),
                (faction_get_slot, reg0, "$players_kingdom", slot_faction_num_castles),
                (val_add, ":territory_points", reg0),
                (val_add, ":territory_points", reg0),
                #If the player owns even a single center, that's worth at least "my lord" from his followers
                (ge, ":territory_points", 1),
                (val_max, ":highest_honor", 2),
                #By default there are around 48 castles and 22 towns on the map, for a total of 70
                #centers, and 162 "points" if weighting castles = 2 and towns = 3.
                (store_sub, ":global_points", towns_end, towns_begin),
                (val_mul, ":global_points", 3),
                (store_sub, reg0, castles_end, castles_begin),
                (val_add, ":global_points", reg0),
                (val_add, ":global_points", reg0),
                #By default there are 6 NPC kingdoms, averaging 8 castles and 3.66... towns or
                #27 points each (although the initial distribution of territory is not even).
                (store_sub, ":number_kingdoms", npc_kingdoms_end, npc_kingdoms_begin),
                (val_max,  ":number_kingdoms", 1),
                #Territory must be at least 3/4 the total points divided by number of initial kingdoms.
                #Right to rule applied as a percentage bonus, scaled so that you gain recognition with
                #75% right to rule and a 50% size kingdom.

                #What I want is: ( (RtR * 2/3) + 100 ) * territory * kingdoms >= globe * 3/4
                #This is equivalent to: (RtR * 2 + 300) * territory * kingdoms * 4 >= globe * 9
                #The re-ordering is because of rounding.
                (store_mul, ":target_points", ":global_points", 9),
                (store_mul, reg0, "$player_right_to_rule", 2),
                (val_add, reg0, 300),
                (val_mul, reg0, ":territory_points"),
                (val_mul, reg0, ":number_kingdoms"),
                (val_mul, reg0, 4),
                (ge, reg0, ":target_points"),
                (val_max, ":highest_honor", 3),
            (try_end),
            #stop evaluation if you reached highest honor
            (ge, ":highest_honor", 3),
        (else_try),
            #the player is a vassal of one of the initial kingdoms
            (is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
            (val_max, ":highest_honor", 1),
            (eq, "$player_has_homage", 1),#<- can fail
            (val_max, ":highest_honor", 2),
        (try_end),

        (try_begin),
           (ge, ":highest_honor", 3),
           (str_store_string, s0, "str_dplmc_your_highness"),
        (else_try),
           (eq, ":highest_honor", 2),
           (str_store_string, s0, "str_dplmc_my_lordlady"),
        (else_try),
           (str_store_string, s0, "str_dplmc_sirmadam"),
        (try_end),

          ##Special cases
        (try_begin),
          (eq, "$sneaked_into_town", disguise_none),
          (is_between, "$g_talk_troop", companions_begin, companions_end),
          (ge, ":highest_honor", 1),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_met, 0),
          (this_or_next|neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_inactive),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, 0),
          (neg|troop_slot_eq, "$g_talk_troop", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
          (troop_get_slot, ":honorific", "$g_talk_troop", slot_troop_honorific),
          (ge, ":honorific", "str_npc1_honorific"),
          (str_store_string, s0, ":honorific"),
        (else_try),
          (eq, ":highest_honor", 1),
          (is_between, "$g_talk_troop", heroes_begin, heroes_end),
          (str_store_string, s0, "str_dplmc_sirmadame"),
        (try_end),

        (assign, reg0, ":highest_honor"),
    ])
]
