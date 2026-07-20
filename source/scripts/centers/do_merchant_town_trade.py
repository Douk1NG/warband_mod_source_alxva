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

do_merchant_town_trade_scripts = [
#script_get_enterprise_name
# INPUT: arg1 = party_no (of the merchant), arg2 = center_no
##diplomacy start+
# If optional economic changes are enabled, the benefits are applied to both
# the town of origin and the destination, instead of just the latter.
##diplomacy end+
("do_merchant_town_trade",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":center_no"),

	  (party_get_slot, ":origin", ":party_no", slot_party_last_traded_center),

	  (try_begin),
		(eq, "$cheat_mode", 2),
		(str_store_party_name, s4, ":center_no"),
		(str_store_party_name, s5, ":origin"),
		(display_message, "@{!}DEBUG -- Caravan trades in {s4}, originally from {s5}"),
	  (try_end),

	  (call_script, "script_add_log_entry", logent_party_traded, ":party_no", ":origin", ":center_no", -1),

      (call_script, "script_do_party_center_trade", ":party_no", ":center_no", 4), #it was first 10 then increased 20 then increased 30, now I decrease it to back 6. Because otherwise prices do not differiate much. Trade become useless in game.

      (assign, ":total_change", reg0),
      #Adding the earnings to the wealth (maximum changed price is the earning)
      (val_div, ":total_change", 2),
      (str_store_party_name, s1, ":party_no"),
      (str_store_party_name, s2, ":center_no"),
      (assign, reg1, ":total_change"),

      #Adding tariffs to the town
      (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),

	  (assign, ":tariffs_generated", ":total_change"),
      (val_mul, ":tariffs_generated", ":prosperity"),
	  ##diplomacy start+
	  #Move the next two lines further down to reduce rounding error
	  #(val_div, ":tariffs_generated", 100),
	  #(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages

	  #Re-wrote the "diplomacy" section here for greater clarity.
	  (assign, ":percent", 100),
      (try_begin), # trade agreement
        (store_faction_of_party, ":party_faction", ":party_no"),
        (store_faction_of_party, ":center_faction", ":center_no"),

        (store_add, ":truce_slot", ":party_faction", slot_faction_truce_days_with_factions_begin),
        (val_sub, ":truce_slot", kingdoms_begin),
  	    (faction_get_slot, ":truce_days", ":center_faction", ":truce_slot"),
  	    ##nested diplomacy start+ replace "20" with a named constant
  	    #(gt, ":truce_days", 20),
  	    (gt, ":truce_days", dplmc_treaty_trade_days_expire),
  	    ##nested diplomacy end+
  	    (val_add, ":percent", 30),
      (try_end),

	  #If economic changes are enabled, divide the tariffs between the source and destination.
	  (assign, ":origin_tariffs_generated", 0),#we will need this variable later, if it is set
	  (try_begin),
	    #Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		#give half the tariffs to the origin
		(ge, ":tariffs_generated", 0),
		(party_get_slot, ":origin_accumulated_tariffs", ":origin", slot_center_accumulated_tariffs),
		(store_div, ":origin_tariffs_generated", ":tariffs_generated", 2),
		(val_sub, ":tariffs_generated", ":origin_tariffs_generated"),
		#apply plutocracy/aristocracy modifier, and any modifier from a trade treaty
		(store_faction_of_party, ":origin_faction", ":center_no"),
		(faction_get_slot, ":aristocracy", ":origin_faction", dplmc_slot_faction_aristocracy),
		(val_mul, ":aristocracy", -5),
		(store_add, ":origin_percent", ":percent", ":aristocracy"),
		(val_mul, ":origin_tariffs_generated", ":origin_percent"),
		(val_add, ":origin_tariffs_generated", 50),#for rounding
		(val_div, ":origin_tariffs_generated", 100),
		#apply the delayed division from before (leaving the steps separated for clarity)
		(val_add, ":origin_tariffs_generated", 50),
		(val_div, ":origin_tariffs_generated", 100),#adjust for having been multiplied by prosperity
		(val_add, ":tariffs_generated", 5),
		(val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
		#now we have the final value of origin_tariffs_generated
		(val_add, ":origin_accumulated_tariffs", ":origin_tariffs_generated"),
		(party_set_slot, ":origin", slot_center_accumulated_tariffs, ":origin_accumulated_tariffs"),
		#print economic debug message if enabled
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":origin_tariffs_generated"),
		(str_store_party_name, s4, ":origin"),
		(assign, reg5, ":origin_accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),

	  #For this town: apply the faction plutocracy/aristocracy modifier
      (faction_get_slot, ":aristocracy", ":center_faction", dplmc_slot_faction_aristocracy),
      (val_mul, ":aristocracy", -5),
      (val_add, ":percent", ":aristocracy"),
      (val_mul, ":tariffs_generated", ":percent"),
   	  (val_add, ":tariffs_generated", 50),
      (val_div, ":tariffs_generated", 100),
	  #apply the delayed division from before (leaving the steps separated for clarity)
   	  (val_add, ":tariffs_generated", 50),
 	  (val_div, ":tariffs_generated", 100),#adjust for having been multiplied by prosperity
	  (val_add, ":tariffs_generated", 5),
	  (val_div, ":tariffs_generated", 10), #10 for caravans, 20 for villages
	  ##diplomacy end+
	  (val_add, ":accumulated_tariffs", ":tariffs_generated"),

	  (try_begin),
		(ge, "$cheat_mode", 3),
		(assign, reg4, ":tariffs_generated"),
		(str_store_party_name, s4, ":center_no"),
		(assign, reg5, ":accumulated_tariffs"),
		(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
	  (try_end),

      (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
      ##diplomacy start+
	  #If economic changes are enabled, 50% chance that the origin rather than
	  #the destination will receive the chance for prosperity increase.
	  (assign, ":benefit_center", ":center_no"),
	  (try_begin),
		#Economic changes must be enabled
		(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
		#verify the origin is a real town or village and not a placeholder value
		(ge, ":origin", 0),
		(this_or_next|is_between, ":origin", towns_begin, towns_end),
		(this_or_next|is_between, ":origin", villages_begin, villages_end),
		(this_or_next|party_slot_eq, ":origin", slot_party_type, spt_town),
			(party_slot_eq, ":origin", slot_party_type, spt_village),
		(ge, ":tariffs_generated", 0),
		#50% chance
		(store_random_in_range, ":rand", 0, 64),
		(lt, ":rand", 32),
		(assign, ":benefit_center", ":origin"),
	  (try_end),
	  ##diplomacy end+
      #Adding 1 to center prosperity with 18% for each caravan in that center
      (try_begin),
        (store_random_in_range, ":rand", 0, 80),
		##diplomacy start+ in next line, changed center_no to benefit_center
        (call_script, "script_center_get_goods_availability", ":benefit_center"),
		##diplomacy end+
		(assign, ":hardship_index", reg0),
		(gt, ":rand", ":hardship_index"),
      (try_begin),
        (store_random_in_range, ":rand", 0, 100),
        (gt, ":rand", 82),
		##diplomacy start+ in next line, changed center_no to benefit_center
		(call_script, "script_change_center_prosperity", ":benefit_center", 1),
		##diplomacy end+
		(val_add, "$newglob_total_prosperity_from_caravan_trade", 1),
      (try_end),
     (try_end),
  ])
]
