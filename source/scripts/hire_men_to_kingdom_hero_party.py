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

hire_men_to_kingdom_hero_party_scripts = [
# script_cf_reinforce_party
# Input: arg1 = troop_no (hero of the party)
# Output: none
("hire_men_to_kingdom_hero_party",
    [
      (store_script_param_1, ":troop_no"),

      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),

      #while hiring reinforcements party leaders can only use 3/4 of their budget. This value is holding in ":hiring budget".
      (assign, ":hiring_budget", ":cur_wealth"),
      (val_mul, ":hiring_budget", 3),
      (val_div, ":hiring_budget", 4),

      (call_script, "script_party_get_ideal_size", ":party_no"),
      (assign, ":ideal_size", reg0),
      (store_mul, ":ideal_top_size", ":ideal_size", 3),
      (val_div, ":ideal_top_size", 2),

	  #(try_begin),
	  #	(ge, "$cheat_mode", 1),
      #  (str_store_troop_name, s7, ":troop_no"),
      #  (assign, reg9, ":cur_wealth"),
      #  (display_message, "@{!}DEBUGS : {s7} total budget is {reg9}"),
      #  (assign, reg6, ":ideal_size"),
      #  (assign, reg7, ":ideal_top_size"),
      #  (assign, reg8, ":hiring_budget"),
      #  (display_message, "str_debug__hiring_men_to_s7_ideal_size__reg6_ideal_top_size__reg7_hiring_budget__reg8"),
      #(try_end),

      (party_get_num_companions, ":party_size", ":party_no"),

      (store_faction_of_party, ":party_faction", ":party_no"),
      (try_begin),
        (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
        (eq, ":party_faction", "$players_kingdom"),
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
      (else_try),
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (try_begin),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":reinforcement_cost", reinforcement_cost_hard),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":reinforcement_cost", reinforcement_cost_moderate),
        (else_try),
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":reinforcement_cost", reinforcement_cost_easy),
        (try_end),
      (try_end),

      (assign, ":num_rounds", 1),
      (try_for_range, ":unused", 0 , ":num_rounds"),
        (try_begin),
          (lt, ":party_size", ":ideal_size"),
          (gt, ":hiring_budget", ":reinforcement_cost"),
          (gt, ":party_no", 0),
          (call_script, "script_cf_reinforce_party", ":party_no"),
          (val_sub, ":cur_wealth", ":reinforcement_cost"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
        (else_try),
          (gt, ":party_size", ":ideal_top_size"),
          (store_troop_faction, ":troop_faction", ":troop_no"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (assign, ":total_regulars", 0),
          (assign, ":total_regular_levels", 0),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3), #reducing the chance of the faction troops' removal
            (try_end),
            (val_mul, ":stack_level", ":stack_size"),
            (val_add, ":total_regulars", ":stack_size"),
            (val_add, ":total_regular_levels", ":stack_level"),
          (try_end),
          (gt, ":total_regulars", 0),
          (store_div, ":average_level", ":total_regular_levels", ":total_regulars"),
          (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (store_character_level, ":stack_level", ":stack_troop"),
            (store_troop_faction, ":stack_faction", ":stack_troop"),
            (try_begin),
              (eq, ":troop_faction", ":stack_faction"),
              (val_mul, ":stack_level", 3),
            (try_end),
            (store_sub, ":level_dif", ":average_level", ":stack_level"),
            (val_div, ":level_dif", 3),
            (store_add, ":prune_chance", 10, ":level_dif"),
            (gt, ":prune_chance", 0),
            (call_script, "script_get_percentage_with_randomized_round", ":stack_size", ":prune_chance"),
            (gt, reg0, 0),
            (party_remove_members, ":party_no", ":stack_troop", reg0),
          (try_end),
        (try_end),
      (try_end),
  ])
]
