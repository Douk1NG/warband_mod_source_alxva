# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_manage_loot_pool (menu)
# Called by menus in 4 domains: battle, camp, diplomacy, siege
# ======================================================================

# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

dplmc_manage_loot_pool_menu = [
("dplmc_manage_loot_pool", mnf_enable_hot_keys,
		"{s10}^{s30}",
		"none",
		[
			##diplomacy start+
			#Use a different troop!
			#(assign, "$pool_troop", "trp_dplmc_chamberlain"),
			(assign, "$pool_troop", "trp_temp_troop"),
			#Make sure things are initialized
			(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
			##diplomacy end+
			(assign, reg20,0),
			(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
			(try_for_range, ":i_slot", 0, ":inv_cap"),
				(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
				(ge, ":item_id", 0),
				(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
				(val_add, reg20, 1),
			(try_end),
			# reg20 now contains number of items in loot pool
			(try_begin),
				(eq, reg20, 0),
				(str_store_string, s10, "str_dplmc_item_pool_no_items"),
				(str_store_string, s20, "str_dplmc_item_pool_leave"),
			(else_try),
				(eq, reg20, 1),
				(str_store_string, s10, "str_dplmc_item_pool_one_item"),
				(str_store_string, s20, "str_dplmc_item_pool_abandon"),
			(else_try),
				(str_store_string, s10, "str_dplmc_item_pool_many_items"),
				(str_store_string, s20, "str_dplmc_item_pool_abandon"),
			(try_end),
		  ## CC
			(try_begin), #only show when we don't have equipment logs
              (str_is_empty, dplmc_loot_string),
			  (set_fixed_point_multiplier, 100),
              (position_set_x, pos0, 20),
              (position_set_y, pos0, 30),
              (position_set_z, pos0, 80),
			  (set_game_menu_tableau_mesh, "tableau_game_character_sheet", "$lord_selected", pos0),
			(try_end),
		  ## CC

          #SB : str30 shows items looted after script_dplmc_auto_loot_troop was called
          # (try_begin),
            # (neg|str_is_empty, dplmc_loot_string),
            # (str_store_string, s10, "@{s10}^^{s30}"),
          # (try_end),
		],
		[
			("dplmc_auto_loot",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(ge, ":space", 10),
					(gt, reg20, 0),
				],
				##diplomacy start+
				#"Let your heroes select gear from the item pool.",
				"Let your heroes select gear from the items on the ground.",
				##diplomacy end+
				[
					# (set_player_troop, "trp_player"),
					# (assign, "$lord_selected", "trp_player"),
					##diplomacy start+
					(call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
					##diplomacy end+
					(jump_to_menu, "mnu_dplmc_auto_loot")
				]
			),
			("dplmc_auto_loot_no",
				[
					(eq, "$inventory_menu_offset",0),
					(store_free_inventory_capacity, ":space", "$pool_troop"),
					(lt, ":space", 10),
					(disable_menu_option)
				],
				"Insufficient item pool space for auto-upgrade.",
				[]
			),
			("dplmc_loot",
				[],
				##diplomacy start+
				#"Access the item pool.",
				"Access the items on the ground.",
				##diplomacy end+
				[
					(change_screen_loot, "$pool_troop"),
				]
			),

            #SB : improve usability, if only change_screen_loot worked with the player
			("dplmc_loot_player",
				[(is_between, "$lord_selected", companions_begin, companions_end),],
				"Access the captain's inventory.",
                #can't use honorific, since the player troop is the companion and strings will be malformed
				[
					(set_player_troop, "trp_player"),
					(change_screen_equip_other, "$lord_selected"),
					(assign, "$lord_selected", "trp_player"),
				]
			),
      ("dplmc_auto_loot_upgrade_management", [],
##diplomacy start+
#        "Upgrade management of the NPC's equipments.",
         "Update management of NPCs' equipment.",
##diplomacy end+
        [
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          ##nested diplomcy start+ Add error check.

          ##nested diplomacy end+
          (try_begin),
            (is_between, "$lord_selected", companions_begin, companions_end),
            (assign, "$temp", "$lord_selected"),
          (else_try),
            (assign, "$temp", -1),
            (try_for_range, ":stack_no", 0, ":num_stacks"),
              (party_stack_get_troop_id,   ":stack_troop", "p_main_party", ":stack_no"),
              (is_between, ":stack_troop", companions_begin, companions_end),
              (assign, "$temp", ":stack_troop"),
              (assign, ":num_stacks", 0),
            (try_end),
          (try_end),
          ##nested diplomacy start+   Add error check.
          (call_script, "script_dplmc_initialize_autoloot", 0),#argument "0" means this does nothing if deemed unnecessary
          (try_begin),#<- dplmc+ added
            (ge, "$temp", 1),#<- dplmc+ added
            (assign, "$temp_2", -1), #SB : other globals
            (try_for_range, ":item_slot", ek_item_0, ek_food),
              (troop_set_slot, "trp_stack_selection_ids", ":item_slot", 0),
            (try_end),
            (str_clear, dplmc_loot_string),
            (start_presentation, "prsnt_dplmc_autoloot_upgrade_management"),
          (try_end),
          ##nested diplomacy end+
        ]
      ),

      ("dplmc_equip_npcs", [],
        "Equip all NPCs (drag & drop).",
        [
          (call_script, "script_all_toggle_weapons_set", 1),
          (assign, "$g_cur_page_of_loot_pool", 0),
          (assign, "$g_selected_troop", "trp_player"),
          (start_presentation, "prsnt_equip_npcs"),
        ]
      ),

      #all other options will reset player eventually, this is for convenience
      ("dplmc_auto_loot_reset_player", [(neq, "$lord_selected", "trp_player")],
         "Reset current troop to the player",
        [
          (assign, "$lord_selected", "trp_player"),
          (set_player_troop, "$lord_selected"),
        ]
      ),
			("dplmc_leave",
				[],
				"{s20}",
				[
				##diplomacy start+
				#Actually abandon the lost loot
				(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
				(try_for_range, ":i_slot", 10, ":inv_cap"),
					(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					(ge, ":item_id", 0),
					(neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					(troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #delete it
					(troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
				(try_end),

				#(jump_to_menu, "mnu_camp"),
				(set_player_troop, "trp_player"),
				(jump_to_menu, "$dplmc_return_menu"),
				(assign, "$pool_troop", -1), #mark ending
				##diplomacy end+
				]
			),
			##nested diplomacy start+
			#Leave & take everything you can
			("dplmc_leave_and_take_a",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(lt, ":space", reg20),
				(gt, reg20, 0),
				(gt, ":space", 0),
				(assign, reg0, ":space"),
				],
				"Gather {reg0} of the {reg20} items on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(troop_sort_inventory, "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item from pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					#(jump_to_menu, "mnu_camp"),
					(set_player_troop, "trp_player"),
					(jump_to_menu, "$dplmc_return_menu"),
					(assign, "$pool_troop", -1), #mark ending
				]
			),
			("dplmc_leave_and_take_b",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(ge, ":space", reg20),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(store_sub, reg0, reg20, 1),
				],
				"Gather the remaining {reg20} {reg0?items:item} on the ground and leave.",
				[
					(store_free_inventory_capacity, ":space", "trp_player"),
					#Take remaining items for player
					(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
					    (gt, ":space", 0),
					    (troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
					    (ge, ":item_id", 0),
					    (neg|troop_has_item_equipped, "$pool_troop", ":item_id"),
					    (troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":i_slot"),
					    (troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
					    (val_sub, ":space", 1),
					    (troop_set_inventory_slot, "$pool_troop", ":i_slot", -1), #remove item frlom pool
					    (troop_inventory_slot_set_item_amount, "$pool_troop", ":i_slot", 0),
					(try_end),
					(set_player_troop, "trp_player"),
					(jump_to_menu, "$dplmc_return_menu"),
					(assign, "$pool_troop", -1), #mark ending
				]
			),
			("dplmc_leave_and_take_c",
				[
				(store_free_inventory_capacity, ":space", "trp_player"),
				(eq, ":space", 0),
				(gt, reg20, 0),#don't show if nothing is on the ground
				(disable_menu_option),
				],
				"There is no space left in your bags.",
				[
				]
			),
			##nested diplomacy end+
		]
	)
]
