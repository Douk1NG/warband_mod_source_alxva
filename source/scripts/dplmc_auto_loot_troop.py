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

dplmc_auto_loot_troop_scripts = [
####################################
# let this troop take its pick from the loot pool
("dplmc_auto_loot_troop", [
	# (try_begin),
		(store_script_param, ":troop", 1),
		(store_script_param, ":pool", 2),
		(store_script_param, ":sreg", 3), #SB : new param for storing changes

		(troop_get_slot,":upg_armor", ":troop",dplmc_slot_upgrade_armor),
		(troop_get_slot,":upg_horses",":troop",dplmc_slot_upgrade_horse),

		# dump whatever rubbish is in the main inventory
		(troop_get_inventory_capacity, ":inv_cap", ":troop"),
		(try_for_range, ":i_slot", dplmc_ek_alt_items_end, ":inv_cap"), #SB raise from 10, skip over civilian stuff
			(troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
			(troop_add_item, ":pool", ":item", ":imod"), #put it back in the pool
			(troop_set_inventory_slot, ":troop", ":i_slot", -1), # delete it
		(try_end),

        #clear slot
        # (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1),
          # (troop_slot_eq, ":troop", ":slot_no", 0), #0 is keep
          # (troop_set_slot, "trp_heroes_end", ":slot_no", 999999),
        # (else_try), #otherwise we reset to default
          # (troop_set_slot, "trp_heroes_end", ":slot_no", -1),
        # (try_end),

        #SB : loop, calculate current item's score
        # (assign, ":slot_no", dplmc_slot_upgrade_wpn_0 - 1),
        (try_for_range, ":item_slot", ek_item_0, ek_head),
          #SB : clear the pool troop's ek_slots
          (troop_set_inventory_slot, ":pool", ":item_slot", -1), #delete it
          (store_add, ":slot_no", dplmc_slot_upgrade_wpn_0, ":item_slot"), #pre-increment
          (troop_get_slot, ":item_preference", ":troop", ":slot_no"),
          (gt, ":item_preference", 0), #0 is keep
          (troop_get_inventory_slot, ":item", ":troop", ":item_slot"),
          (ge, ":item", 0), #initial item check
          (troop_get_inventory_slot_modifier, ":imod", ":troop", ":item_slot"),

          (try_begin),
            (store_mod, ":item_type", ":item_preference", meta_itp_mask),
            (item_get_type, ":itp", ":item"),
            (neq, ":itp", ":item_type"),
            (troop_set_inventory_slot, ":troop", ":item_slot", -1), #delete it
            (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
            (assign, ":item", -1), #so we fail this loop
          (try_end),
          (ge, ":item", 0),
          #SB : cache the original equipment to see changes
          (troop_set_inventory_slot, ":pool", ":item_slot", ":item"),
          (troop_set_inventory_slot_modifier, ":pool", ":item_slot", ":imod"),

          (call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
          (assign, ":cur_value", reg0),
          #check to see whether damage is preferred
          (try_begin),
            (call_script, "script_cf_item_type_has_advanced_autoloot", ":item_type"),
            (store_div, ":dmg_type", ":item_preference", meta_dmg_mask),
            (neq, ":dmg_type", 0),
            (item_get_swing_damage, ":swing_damage", ":item"),
            (item_get_thrust_damage, ":thrust_damage", ":item"),
            (try_begin),
              (ge, ":swing_damage", ":thrust_damage"),
              (item_get_swing_damage_type, ":item_dmg_type", ":item"),
            (else_try),
              (lt, ":swing_damage", ":thrust_damage"),
              (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
            (try_end),
            #check if it matches preference
            (val_add, ":item_dmg_type", 1),
            (eq, ":dmg_type", ":item_dmg_type"),
            (val_mul, ":cur_value", 4),
          (try_end),
          (troop_set_slot, "trp_heroes_end", ":slot_no", ":cur_value"),
        (else_try),
          (eq, ":item_preference", 0), #0 is keep
          (troop_set_slot, "trp_heroes_end", ":slot_no", 999999),
        (else_try), #whether no item or discarded
          (lt, ":item", 0),
          (troop_set_slot, "trp_heroes_end", ":slot_no", 0),
        (try_end),

        # (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, dplmc_slot_upgrade_wpn_3 + 1),
          # (troop_get_slot, reg0, ":troop", ":slot_no"),
          # (troop_get_slot, reg1, "trp_heroes_end", ":slot_no"),
          # (store_sub, reg2, ":slot_no", dplmc_slot_upgrade_wpn_0),
          # (troop_get_inventory_slot, ":item", ":troop", reg2),
          # (try_begin),
            # (eq, ":item", -1),
            # (str_store_string, s1, "str_dplmc_none"),
          # (else_try),
            # (str_store_item_name, s1, ":item"),
          # (try_end),

          # (display_message, "@upgrading slot {reg2} with {reg0}, cur score for {s1}: {reg1}"),
        # (try_end),

		(try_for_range, ":i_slot", ek_head, ek_food),
			(troop_get_inventory_slot, ":item", ":troop", ":i_slot"),
            (troop_set_inventory_slot, ":pool", ":i_slot", -1), #delete it
			(ge, ":item", 0),
            (troop_set_inventory_slot, ":pool", ":i_slot", ":item"), #store it
			(troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_slot"),
            (troop_set_inventory_slot_modifier, ":pool", ":i_slot", ":imod"), #store it
			(try_begin),
				(neq, ":upg_armor", 0), # we're upgrading armors
				(is_between, ":i_slot", ek_head, ek_horse), # it's an armor slot
				(troop_set_inventory_slot, ":troop", ":i_slot", -1), #delete it
				(troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
			(else_try),
				(neq, ":upg_horses", 0), # we're upgrading horses
				(eq, ":i_slot", ek_horse), # it's a horse slot
				(troop_set_inventory_slot, ":troop", ":i_slot", -1), #delete it
				(troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
			(try_end),
		(try_end),

		# clear best matches
		(assign, ":best_helmet_slot", -1),
		(assign, ":best_helmet_val", 0),
		(assign, ":best_body_slot", -1),
		(assign, ":best_body_val", 0),
		(assign, ":best_boots_slot", -1),
		(assign, ":best_boots_val", 0),
		(assign, ":best_gloves_slot", -1),
		(assign, ":best_gloves_val", 0),
		(assign, ":best_horse_slot", -1),
		(assign, ":best_horse_val", 0),

		# Now search through the pool for the best items
		(troop_get_inventory_capacity, ":inv_cap", ":pool"),
		(try_for_range, ":i_slot", ek_food + 1, ":inv_cap"), #SB: skip cached items
			(troop_get_inventory_slot, ":item", ":pool", ":i_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":i_slot"),
			(call_script, "script_dplmc_troop_can_use_item", ":troop", ":item", ":imod"),
			(eq, reg0, 1), # can use
			#(call_script, "script_get_item_value_with_imod", ":item", ":imod"),  # use the following instead

			#### Autoloot improved by rubik begin
			# get item_score instead of price
			(call_script, "script_dplmc_get_item_score_with_imod", ":item", ":imod"),
			#### Autoloot improved by rubik end
			(assign, ":score", reg0),
			(item_get_type, ":item_type", ":item"),

			(try_begin),
				(eq, ":item_type", itp_type_horse), #it's a horse
				(eq, ":upg_horses", 1), # we're upgrading horses
				(gt, ":score", ":best_horse_val"),
				(assign, ":best_horse_slot", ":i_slot"),
				(assign, ":best_horse_val", ":score"),
			(else_try), #SB : move armor checks here
				(is_between, ":item_type", itp_type_head_armor, itp_type_hand_armor + 1), # we're checking armor
				(eq, ":upg_armor", 1), # we're upgrading armor
				(try_begin),
					(eq, ":item_type", itp_type_head_armor),
					(gt, ":score", ":best_helmet_val"),
					(assign, ":best_helmet_slot", ":i_slot"),
					(assign, ":best_helmet_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_body_armor),
					(gt, ":score", ":best_body_val"),
					(assign, ":best_body_slot", ":i_slot"),
					(assign, ":best_body_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_foot_armor),
					(gt, ":score", ":best_boots_val"),
					(assign, ":best_boots_slot", ":i_slot"),
					(assign, ":best_boots_val", ":score"),
				(else_try),
					(eq, ":item_type", itp_type_hand_armor),
					(gt, ":score", ":best_gloves_val"),
					(assign, ":best_gloves_slot", ":i_slot"),
					(assign, ":best_gloves_val", ":score"),
				(try_end),
            (else_try), #SB : move weapon checks back here
              (assign, ":limit", dplmc_slot_upgrade_wpn_3 + 1),
              (try_begin), #check for denying use on horseback
                  (this_or_next|gt, ":best_horse_val", 0),
                  (eq, ":upg_horses", 1), # we're upgrading horses
                  (this_or_next|item_has_property, ":item", itp_cant_use_on_horseback),
                  (this_or_next|item_has_property, ":item", itp_cant_reload_on_horseback),
                  (item_has_property, ":item", itp_cant_reload_while_moving_mounted),
                  (assign, ":limit", 0),
              (try_end),
              (try_for_range, ":slot_no", dplmc_slot_upgrade_wpn_0, ":limit"),
                (troop_get_slot, ":item_preference", ":troop", ":slot_no"),
                (neq, ":item_preference", 0), #not keep current
                (store_div, ":damage_type", ":item_preference", meta_dmg_mask),
                (val_mod, ":item_preference", meta_dmg_mask), #get the itp + meta
                (call_script, "script_item_get_type_aux", ":item"),
                (this_or_next|eq, ":item_preference", reg0), #either same meta-type
                (eq, ":item_preference", ":item_type"), #or matching base itp

                #check to see whether damage is preferred
                (try_begin),
                  (neq, ":damage_type", 0),
                  (item_get_swing_damage, ":swing_damage", ":item"),
                  (item_get_thrust_damage, ":thrust_damage", ":item"),
                  (try_begin),
                    (ge, ":swing_damage", ":thrust_damage"),
                    (item_get_swing_damage_type, ":item_dmg_type", ":item"),
                  (else_try),
                    (lt, ":swing_damage", ":thrust_damage"),
                    (item_get_thrust_damage_type, ":item_dmg_type", ":item"),
                  (try_end),
                  #check if it matches preference
                  (val_add, ":item_dmg_type", 1),
                  (eq, ":damage_type", ":item_dmg_type"),
                  (val_mul, ":score", 4),
                (try_end),
                #if current score is not ge, replace item and score
                (neg|troop_slot_ge, "trp_heroes_end", ":slot_no", ":score"),
                (troop_set_slot, "trp_heroes_end", ":slot_no", ":score"),
                (assign, ":limit", -1), #loop break
                (store_sub, ":item_slot", ":slot_no", dplmc_slot_upgrade_wpn_0), #ek item slots
                (troop_get_inventory_slot, ":item_no", ":troop", ":item_slot"),
                (try_begin),
                  (eq, ":item_no", -1),
                  (troop_set_inventory_slot, ":pool", ":i_slot", -1),
                (else_try), #replace into pool
                  (troop_get_inventory_slot_modifier, ":imod_no", ":troop", ":item_slot"),
                  (troop_set_inventory_slot, ":pool", ":i_slot", ":item_no"),
                  (troop_set_inventory_slot_modifier, ":pool", ":i_slot", ":imod_no"),
                (try_end),
                (troop_set_inventory_slot, ":troop", ":item_slot", ":item"),
                (troop_set_inventory_slot_modifier, ":troop", ":item_slot", ":imod"),
                # (try_begin),
                  # (str_store_item_name, s1, ":item"),
                  # (try_begin),
                    # (eq, ":item_no", -1),
                    # (str_store_string, s2, "str_dplmc_none"),
                  # (else_try),
                    # (str_store_item_name, s2, ":item_no"),
                  # (try_end),
                  # (assign, reg1, ":score"),
                  # (display_message, "@{s1} better than {s2}, score of {reg1}"),
                # (try_end),
              (try_end),
            (try_end),
        (try_end),

		# Now we know which ones are the best. Give them to the troop.
		(try_begin),
			(assign, ":best_slot", ":best_helmet_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_head, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_head, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_body_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_body, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_body, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_boots_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_foot, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_foot, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_gloves_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_gloves, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_gloves, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		(try_begin),
			(assign, ":best_slot", ":best_horse_slot"),
			(ge, ":best_slot", 0),
			(troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
			(ge, ":item", 0),
			(troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			(troop_set_inventory_slot, ":troop", ek_horse, ":item"),
			(troop_set_inventory_slot_modifier, ":troop", ek_horse, ":imod"),
			(troop_set_inventory_slot, ":pool", ":best_slot", -1),
		(try_end),

		# (try_for_range, ":i_slot", ek_item_0, ek_head),
			# (store_add, ":trp_slot", ":i_slot", dplmc_slot_upgrade_wpn_0),
			# (troop_get_slot, ":type", ":troop", ":trp_slot"),
			# (gt, ":type", 0), #we're upgrading for this slot
			# (call_script, "script_dplmc_scan_for_best_item_of_type", ":pool", ":type", ":troop"), #search for the best
			# (assign, ":best_slot", reg0),
			# (neq, ":best_slot", -1), #got something
			# (troop_get_inventory_slot, ":item", ":pool", ":best_slot"), #get it
			# (ge, ":item", 0),
			# (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
			# (troop_set_inventory_slot, ":pool", ":best_slot", -1), #remove from pool
			# (troop_set_inventory_slot, ":troop", ":i_slot", ":item"), #add to slot
			# (troop_set_inventory_slot_modifier, ":troop", ":i_slot", ":imod"),
		# (try_end),

        #SB : string storage
        (try_begin),
          (neq, ":sreg", -1),
          (str_store_troop_name, ":sreg", ":troop"),
          (assign, ":num_changes", 0),
          (assign, ":last_change", 0),
          #three cases : discarded item -1, no change 0, change 1 (upgraded/swapped depending on item flags)
          (try_for_range, ":i_slot", ek_item_0, ek_food),
            (troop_get_inventory_slot, ":old_item", ":pool", ":i_slot"),
            (troop_get_inventory_slot, ":new_item", ":troop", ":i_slot"),
            (try_begin),
              (gt, ":old_item", -1),
              (troop_get_inventory_slot_modifier, ":old_imod", ":pool", ":i_slot"),
              (store_add, ":imod_no", ":old_imod", "str_imod_plain"),
              # (str_store_string, s10, ":imod_no"),
              # (str_store_item_name, s20, ":old_item"),
              # (display_message, "@old:{s10}{s20}"),
            (else_try),
              (assign, ":old_imod", imod_plain),
            (try_end),
            (try_begin),
              (gt, ":new_item", -1),
              (troop_get_inventory_slot_modifier, ":new_imod", ":troop", ":i_slot"),
              (store_add, ":imod_no", ":new_imod", "str_imod_plain"),
              # (str_store_string, s10, ":imod_no"),
              # (str_store_item_name, s20, ":new_item"),
              # (display_message, "@new:{s10}{s20}"),
            (else_try),
              (assign, ":new_imod", imod_plain),
            (try_end),

            # #placeholder swap strings
            # (str_clear, s0), #sreg
            # (str_clear, s1), #new string
            # (str_clear, s10), #imod
            # (str_clear, s20), #item

            (try_begin), #keep current
              (is_between, ":i_slot", ek_item_0, ek_head),
              (store_add, ":upgrade_slot", ":i_slot", dplmc_slot_upgrade_wpn_0),
              (troop_slot_eq, ":troop", ":upgrade_slot", 0),
              (assign, ":item_changed", 0),
            (else_try), #same
              (eq, ":new_item", ":old_item"),
              (eq, ":old_imod", ":new_imod"),
              (assign, ":item_changed", 0),
            (else_try), #discarded
              (eq, ":new_item", -1),
              (gt, ":old_item", -1),
              (assign, ":item_changed", 2),
              (assign, ":item_no", ":old_item"),
              (assign, ":imod_no", ":old_imod"),
            (else_try), #swapped/equipped
              (gt, ":new_item", -1),
              (assign, ":item_changed", 1),
              (assign, ":item_no", ":new_item"),
              (assign, ":imod_no", ":new_imod"),
            (try_end),

            #build string
            (try_begin),
              (gt, ":item_changed", 0),
              (val_add, ":imod_no", "str_imod_plain"),
              (str_store_string, s10, ":imod_no"), #this comes with a space
              (str_store_item_name, s20, ":item_no"),

              (try_begin),
                (neq, ":last_change", 1),
                (eq, ":item_changed", 1),
                (str_store_string, s1, "@equipped {s10}{s20}"),
              (else_try),
                (neq, ":last_change", 2),
                (eq, ":item_changed", 2),
                (str_store_string, s1, "@discarded {s10}{s20}"),
              (else_try), #same as before, no need to qualify
                (str_store_string, s1, "@{s10}{s20}"),
              (try_end),
              (str_store_string_reg, s0, ":sreg"),
              (try_begin), #no comma for first part
                (eq, ":num_changes", 0),
                (str_store_string, ":sreg", "str_s0_s1"),
              (else_try),
                (str_store_string, ":sreg", "str_dplmc_s0_comma_s1"),
              (try_end),
              # (assign, reg1, ":num_changes"),
              # (display_message, "@{reg1} : {s1}"),
              (val_add, ":num_changes", ":item_changed"),
              (assign, ":last_change", ":item_changed"),
            (try_end),
          (try_end),
          (try_begin), #discard if we didn't touch the inventory at all
            (le, ":num_changes", 0), #this is a flag, not a count
            (str_clear, ":sreg"),
          (try_end),
        (try_end),

    # (try_end),
])
]
