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




#Party AI: pruning some of the prisoners in each center (once a week)
  

party_ai_prisoner_pruning_simple_triggers = [
(24*7,
   [
   #SB : save g_talk_troop
       (assign, ":save_talk_troop", "$g_talk_troop"),
       (assign, "$g_talk_troop", ransom_brokers_begin), #to get the right price
       (try_for_range, ":center_no", centers_begin, centers_end),
         (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":center_no"),
         (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
           (neg|troop_is_hero, ":stack_troop"),
           (party_prisoner_stack_get_size, ":stack_size",":center_no",":stack_no"),
           (store_random_in_range, ":rand_no", 0, 40),
           (val_mul, ":stack_size", ":rand_no"),
           (val_div, ":stack_size", 100),
           (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
		   ##diplomacy start+ add prisoner value to center wealth
		   (try_begin),
		      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#must be explicitly enabled
			  (ge, ":center_no", 1),
			  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			  (party_slot_ge, ":center_no", slot_town_lord, 1),#"wealth" isn't used for player garrisons
			  (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
			  (lt, ":cur_wealth", 6000),
              #SB : calculate real prisoner price
              (call_script, "script_game_get_prisoner_price", ":stack_troop"),
			  (store_mul, ":ransom_profits", ":stack_size", reg0),#a fraction of what it could be sold for (50 would be a rule of thumb)
              (val_div, ":ransom_profits", 10),
              #SB : ransom broker doubles profit
              (try_begin),
                (party_slot_ge, ":center_no", slot_center_ransom_broker, ransom_brokers_begin),
                (val_mul, ":ransom_profits", 5),
                (val_div, ":ransom_profits", 2),
              (try_end),
			  (val_add, ":cur_wealth", ":ransom_profits"),
			  (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
		   (try_end),
		   ##diplomacy end+
         (try_end),
       (try_end),
       (assign, "$g_talk_troop", ":save_talk_troop"),
    ]),
]
