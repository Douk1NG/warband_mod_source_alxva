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


  #Troop AI: Village farmers thinking
  

village_farmer_ai_simple_triggers = [
(8,
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_village_farmer),
         (party_is_in_any_town, ":party_no"),
         (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
         (party_get_cur_town, ":cur_center", ":party_no"),

         (assign, ":can_leave", 1),
         (try_begin),
           (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
           (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
           (assign, ":can_leave", 0),
         (try_end),
         (eq, ":can_leave", 1),

         (try_begin),
           (eq, ":cur_center", ":home_center"),

		   #Peasants trade in their home center
		   (call_script, "script_do_party_center_trade", ":party_no", ":home_center", 3), #this needs to be the same as the center
		   (store_faction_of_party, ":center_faction", ":cur_center"),
           (party_set_faction, ":party_no", ":center_faction"),
           (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":market_town"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":market_town"),
           #SB : pick up up to 5 spare items in elder's inventory
           (try_begin), #technically we can just sell from the inventory directly and skip all this work
             (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
             (party_get_slot, ":town_elder", ":home_center", slot_town_elder),
             (try_begin), #reaccumulate wealth, since we can't store the party's gold use a slot
               (party_get_slot, ":cur_wealth", ":party_no", slot_town_wealth),
               (troop_add_gold, ":town_elder", ":cur_wealth"),
               (party_set_slot, ":party_no", slot_town_wealth, 0),
             (try_end),
             (party_get_slot, ":num_items", ":party_no", slot_party_next_looted_item_slot),
             # (this_or_next|eq, ":num_items", 0),
             (lt, ":num_items", num_party_loot_slots), #not capped
             (val_add, ":num_items", slot_party_looted_item_1),
             (troop_get_inventory_capacity, ":inv_cap", ":town_elder"),
             (try_for_range, ":item_slot", 10, ":inv_cap"),
               (troop_get_inventory_slot, ":item_no", ":town_elder", ":item_slot"),
               (gt, ":item_no", -1),
               (item_get_type, ":itp", ":item_no"),
               (neq, ":itp", itp_type_goods), #whatever crap player sells
               (party_set_slot, ":party_no", ":num_items", ":item_no"),
               (store_add, ":imod_slot", ":num_items", num_party_loot_slots),
               (troop_get_inventory_slot_modifier, ":imod_no", ":town_elder", ":item_slot"),
               (party_set_slot, ":party_no", ":imod_slot", ":imod_no"),
               (troop_set_inventory_slot, ":town_elder", ":item_slot", -1), #remove
               (try_begin), #only 5 permited
                 (ge, ":num_items", slot_party_looted_item_1 + num_party_loot_slots),
                 (assign, ":inv_cap", 0),
               (else_try),
                 (val_add, ":num_items", 1),
               (try_end),
             (try_end),
           (try_end),
           
         (else_try),
           (try_begin),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),

             (call_script, "script_do_party_center_trade", ":party_no", ":cur_ai_object", 3), #raised from 10
             (assign, ":total_change", reg0),
		     #This is roughly 50% of what a caravan would pay

             #Adding tariffs to the town
             (party_get_slot, ":accumulated_tariffs", ":cur_ai_object", slot_center_accumulated_tariffs),
             (party_get_slot, ":prosperity", ":cur_ai_object", slot_town_prosperity),

			 (assign, ":tariffs_generated", ":total_change"),
			 (val_mul, ":tariffs_generated", ":prosperity"),
			 ##diplomacy start+
			 (val_add, ":tariffs_generated", 50),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 100),
			 ##diplomacy start+
			 (val_div, ":tariffs_generated", 5),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 20), #10 for caravans, 20 for villages
			 (val_add, ":accumulated_tariffs", ":tariffs_generated"),
			 ##diplomacy begin
        (try_begin), #no tariffs for infested villages and towns
          (party_slot_ge, ":cur_ai_object", slot_village_infested_by_bandits, 1),
          (assign,":accumulated_tariffs", 0),
        (try_end),
	     ##diplomacy end
			 (try_begin),
				(ge, "$cheat_mode", 3),
				(assign, reg4, ":tariffs_generated"),
				(str_store_party_name, s4, ":cur_ai_object"),
				(assign, reg5, ":accumulated_tariffs"),
				(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
			 (try_end),

             (party_set_slot, ":cur_ai_object", slot_center_accumulated_tariffs, ":accumulated_tariffs"),

             #Increasing food stocks of the town
             (party_get_slot, ":town_food_store", ":cur_ai_object", slot_party_food_store),
             (call_script, "script_center_get_food_store_limit", ":cur_ai_object"),
             (assign, ":food_store_limit", reg0),
             (val_add, ":town_food_store", 1000),
             (val_min, ":town_food_store", ":food_store_limit"),
             (party_set_slot, ":cur_ai_object", slot_party_food_store, ":town_food_store"),

             #Adding 1 to village prosperity
             (try_begin),
               (store_random_in_range, ":rand", 0, 100),
               (lt, ":rand", 5), #was 35
               (call_script, "script_change_center_prosperity", ":home_center", 1),
			   (val_add, "$newglob_total_prosperity_from_village_trade", 1),
             (try_end),
           (try_end),

           #Moving farmers to their home village
           (party_set_slot, ":party_no", slot_party_ai_object, ":home_center"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":home_center"),
         (try_end),
       (try_end),
    ]),
]
