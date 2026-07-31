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



  #Hiring men with hero wealths (once a day)
  #Hiring men with center wealths (once a day)
  

hero_wealth_hiring_simple_triggers = [
(24,
   [
   #SB : move this unscoped variable up
     (options_get_campaign_ai, ":reduce_campaign_ai"),
     ##diplomacy start+
     ##change to allow promoted kingdom ladies to hire troops
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
     (try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
     ##diplomacy end+
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (ge, ":party_no", 1),
       (party_is_active, ":party_no"),
       (party_get_attached_to, ":cur_attached_party", ":party_no"),
       (is_between, ":cur_attached_party", centers_begin, centers_end),
       (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege

       (store_faction_of_party, ":party_faction", ":party_no"),
       (try_begin),
         (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
         (eq, ":party_faction", "$players_kingdom"),
         (assign, ":num_hiring_rounds", 1),
         (store_random_in_range, ":random_value", 0, 2),
         (val_add, ":num_hiring_rounds", ":random_value"),
       (else_try),
         # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
         (try_begin),
           (eq, ":reduce_campaign_ai", 0), #hard (2x reinforcing)
           (assign, ":num_hiring_rounds", 2),
         (else_try),
           (eq, ":reduce_campaign_ai", 1), #medium (1x or 2x reinforcing)
           (assign, ":num_hiring_rounds", 1),
           (store_random_in_range, ":random_value", 0, 2),
           (val_add, ":num_hiring_rounds", ":random_value"),
         (else_try),
           (eq, ":reduce_campaign_ai", 2), #easy (1x reinforcing)
           (assign, ":num_hiring_rounds", 1),
         (try_end),
       (try_end),

       (try_begin),
         (faction_slot_eq,  ":party_faction", slot_faction_marshall, ":troop_no"),
         (val_add, ":num_hiring_rounds", 1),
       (try_end),

       (try_for_range, ":unused", 0, ":num_hiring_rounds"),
         (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men with current wealth
       (try_end),
     (try_end),

      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
       # (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
       #SB : useless condition
        (party_slot_ge, ":center_no", slot_town_lord, active_npcs_begin), #center belongs to someone.
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege

        (store_faction_of_party, ":center_faction", ":center_no"),
        ##diplomacy start+ Player culture cleanup (do this once here, instead of separately for each type)
        (try_begin),
          (gt, ":center_faction", "fac_commoners"),
          (this_or_next|eq, ":center_faction", "fac_player_faction"),
          (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
          (eq, ":center_faction", "$players_kingdom"),
          (neg|is_between, ":center_faction", npc_kingdoms_begin, npc_kingdoms_end),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":center_faction", "$g_player_culture"),
        (try_end),
        ##diplomacy end+
        
        (try_begin),
          (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
          (eq, ":center_faction", "$players_kingdom"),
          (assign, ":reinforcement_cost", reinforcement_cost_moderate),
          (assign, ":num_hiring_rounds", 1),#player's center is already excluded
        (else_try),
         # (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
          (assign, ":reinforcement_cost", reinforcement_cost_moderate),
          (try_begin),
            (eq, ":reduce_campaign_ai", 0), #hard (1x or 2x reinforcing)
            (assign, ":reinforcement_cost", reinforcement_cost_hard),
            (store_random_in_range, ":num_hiring_rounds", 0, 2),
            (val_add, ":num_hiring_rounds", 1),
          (else_try),
            (eq, ":reduce_campaign_ai", 1), #moderate (1x reinforcing)
            (assign, ":reinforcement_cost", reinforcement_cost_moderate),
            (assign, ":num_hiring_rounds", 1),
          (else_try),
            (eq, ":reduce_campaign_ai", 2), #easy (none or 1x reinforcing)
            (assign, ":reinforcement_cost", reinforcement_cost_easy),
            (store_random_in_range, ":num_hiring_rounds", 0, 2),
          (try_end),
        (try_end),
        #SB : initial budget to top
        (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),

        (faction_get_slot, ":pt_a", ":center_faction", slot_faction_reinforcements_a),
        (faction_get_slot, ":pt_b", ":center_faction", slot_faction_reinforcements_b),
        (faction_get_slot, ":pt_c", ":center_faction", slot_faction_reinforcements_c),
        # do village reinforcement loops
        (try_for_range, ":village_reinforcements", villages_begin, villages_end),
          
          (gt, ":num_hiring_rounds", 0),
          (party_slot_eq, ":village_reinforcements", slot_village_state, svs_normal), ## Not if the village is being raided or is looted
          (party_slot_eq, ":village_reinforcements", slot_village_bound_center, ":center_no"),
          (store_div, ":hiring_budget", ":cur_wealth", 2),
          (gt, ":hiring_budget", ":reinforcement_cost"),
          
          (party_get_slot, ":result", ":village_reinforcements", slot_village_reinforcement_party),
          (try_begin), #inactive, etc
            (this_or_next|le, ":result", 0),
            (neg|party_is_active, ":result"),
            (spawn_around_party, ":village_reinforcements", "pt_center_reinforcements"),
            (assign, ":result", reg0),
                       
              ###faction icons### dckplmc
              (try_begin),
                  (is_between, ":center_faction", npc_kingdoms_begin, kingdoms_end),
                  (store_sub, ":fac_offset", ":center_faction", npc_kingdoms_begin),
                  (try_begin),
                      (store_add, ":icon", "icon_kingdom_1_soldier_b", ":fac_offset"), 
                      (party_set_icon, ":result", ":icon"),
                  (try_end),
              (try_end),
              ###
            
          (try_end),
          # (party_get_num_companions, ":num_companions", ":result"), #should be 0, unless this is run before current party reaches there
          # (lt, ":num_companions", 25),

          (store_random_in_range, ":rand", 0, 100),
          (try_begin),
            (is_between, ":center_faction", kingdoms_begin, kingdoms_end),
            (faction_get_slot, ":dplmc_quality", ":center_faction", dplmc_slot_faction_quality),
            (val_clamp, ":dplmc_quality", -3, 4),
            (val_add, ":rand", ":dplmc_quality"),
            # (val_clamp, ":rand", 0, 101),
          (try_end),
          
          # (try_begin),
            # (is_between, ":rand", 0, 45),  ## Get weakest template
            # (party_add_template, ":result", ":pt_a"),
          # (else_try),
            # (is_between, ":rand", 40, 85), ## Get stronger template
            # (party_add_template, ":result", ":pt_b"),
          # (else_try),
            # (ge, ":rand", 85), ## Get strongest template
            # (party_add_template, ":result", ":pt_c"),
          # (try_end),
          
          (try_begin),
            (lt, ":rand", 65),
            (party_add_template, ":result", ":pt_a"),
          (else_try),
            (lt, ":rand", 100),
            (party_add_template, ":result", ":pt_b"),
          (else_try), #small chance based on faction quality
            (party_add_template, ":result", ":pt_c"),
          (try_end),
          #one reinforcement per village at a time
          (try_begin), #a new party
            (neg|party_slot_eq, ":village_reinforcements", slot_village_reinforcement_party, ":result"),
            (party_set_faction, ":result", ":center_faction"),
            (party_set_slot, ":result", slot_party_type, spt_reinforcement),
            (party_set_slot, ":result", slot_party_ai_object, ":center_no"),
            (party_set_slot, ":result", slot_party_home_center, ":village_reinforcements"),
            (party_set_slot, ":village_reinforcements", slot_village_reinforcement_party, ":result"),
            (str_store_party_name, s5, ":village_reinforcements"),
            (party_set_name, ":result", "str_s5_reinf"),
            # (call_script, "script_party_name_associate", ":result", ":village_reinforcements"),
            (party_set_ai_behavior,":result", ai_bhvr_travel_to_party),
            (party_set_ai_object,":result", ":center_no"),
            (party_set_flags, ":result", pf_default_behavior, 1),
          (try_end),
          (val_sub, ":cur_wealth", ":reinforcement_cost"),
          (val_sub, ":num_hiring_rounds", 1),
        (try_end),
        (try_for_range, ":unused", 0, ":num_hiring_rounds"),
          (store_div, ":hiring_budget", ":cur_wealth", 2),
          (gt, ":hiring_budget", ":reinforcement_cost"),
          (call_script, "script_cf_reinforce_party", ":center_no"),
          (val_sub, ":cur_wealth", ":reinforcement_cost"),
          (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
        (try_end),
       #SB : move to bottom
        (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
      (try_end),

     #this is moved up from below , from a 24 x 15 slot to a 24 slot
     (try_for_range, ":center_no", centers_begin, centers_end),
       #(neg|is_between, ":center_no", castles_begin, castles_end),
       (store_random_in_range, ":random", 0, 30),
       (le, ":random", 10),
	   
       (call_script, "script_get_center_ideal_prosperity", ":center_no"),
       (assign, ":ideal_prosperity", reg0),
       (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
       (try_begin),
	     (eq, ":random", 0), #with 3% probability it will gain +10/-10 prosperity even it has higher prosperity than its ideal prosperity.
         (try_begin),
           (store_random_in_range, ":random", 0, 2),
           (try_begin),
             (eq, ":random", 0),
             (neg|is_between, ":center_no", castles_begin, castles_end), #castles always gain positive prosperity from surprise income to balance their prosperity.
             (call_script, "script_change_center_prosperity", ":center_no", -10),
             (val_add, "$newglob_total_prosperity_from_convergence", -10),
           (else_try),     
             (call_script, "script_change_center_prosperity", ":center_no", 10),
             (val_add, "$newglob_total_prosperity_from_convergence", 10),
           (try_end),
         (try_end),
       (else_try),
         (gt, ":prosperity", ":ideal_prosperity"),
         (call_script, "script_change_center_prosperity", ":center_no", -1),
         (val_add, "$newglob_total_prosperity_from_convergence", -1),
       (else_try),
         (lt, ":prosperity", ":ideal_prosperity"),
         (call_script, "script_change_center_prosperity", ":center_no", 1),
         (val_add, "$newglob_total_prosperity_from_convergence", 1),
       (try_end),
     (try_end),
    ]),
]
