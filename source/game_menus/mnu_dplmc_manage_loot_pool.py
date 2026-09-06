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
			# fix 2026-09-06: multi-pool count. Sum items across all 3 pools.
			(try_for_range, ":pool_idx", 0, 3),
				(try_begin),
					(eq, ":pool_idx", 0),
					(assign, ":count_pool", "$pool_troop"),
				(else_try),
					(eq, ":pool_idx", 1),
					(assign, ":count_pool", "trp_dplmc_pool_2"),
				(else_try),
					(eq, ":pool_idx", 2),
					(assign, ":count_pool", "trp_dplmc_pool_3"),
				(try_end),
				(troop_get_inventory_capacity, ":inv_cap", ":count_pool"),
				(try_for_range, ":i_slot", 0, ":inv_cap"),
					(troop_get_inventory_slot, ":item_id", ":count_pool", ":i_slot"),
					(ge, ":item_id", 0),
					(neg|troop_has_item_equipped, ":count_pool", ":item_id"),
					(val_add, reg20, 1),
				(try_end),
			(try_end),
			# reg20 now contains number of items across all 3 loot pools
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
					# fix 2026-09-06: lowered min free-space from 10 to 1 so the
					# auto-loot button stays enabled after large battles that
					# nearly fill trp_temp_troop. Risk: companion dumps to a
					# full pool will silently drop items (troop_add_item has
					# no error path). Acceptable for now; pre-sort cleanup
					# is the next round if item loss is reported.
					(ge, ":space", 1),
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
			("dplmc_loot_pool_2",
				[],
				"Access loot pool 2.",
				[
					(change_screen_loot, "trp_dplmc_pool_2"),
				]
			),
			("dplmc_loot_pool_3",
				[],
				"Access loot pool 3.",
				[
					(change_screen_loot, "trp_dplmc_pool_3"),
				]
			),
			# fix 2026-09-06: manual 3-way distribute. Sorts all 3 pools
			# by value (best on top), then moves the bottom 1/3 of each
			# pool to the next one. Use this when pool 1 (trp_temp_troop)
			# is full and the auto-loot button is greyed out / dumps
			# would silently fail. Doing it manually keeps the
			# distribution predictable; the auto version interfered with
			# the auto-loot flow in unexpected ways.
			#
			# -------------------------------------------------------------------------
			# KNOWN LIMITATION: this script does NOT split evenly across runs.
			# The 1/3 calculation is by slot index, not by item count. After
			# the first move, pool 2 holds the moved items at the END of its
			# inventory (slots N..N+59), so when the second move reads
			# "bottom 1/3 of pool 2" by slot index it picks a mix of pre-existing
			# items and the just-moved ones, not necessarily the least valuable
			# by value. pool 3 is therefore not a clean "bottom tier".
			#
			# The proper fix is to (troop_sort_inventory, "trp_dplmc_pool_2")
			# AGAIN after the first move and before the second one. Same for
			# pool 3 if a third pass is added. NOT done here because the user
			# prefers the current behavior; revisit if a future save shows
			# items clustered in the wrong pool after multiple distributes.
			#
			# Other risks to watch for:
			# - troop_add_item silently DROPS the item if the destination pool
			#   is full. If a user runs distribute repeatedly without clearing
			#   pool 3 first, items can be lost without warning.
			# - The "bottom 1/3" by slot index treats empty slots and full
			#   slots the same. If pool 2 already has 30+ items, the second
			#   move will pull from BOTH pool 1 leftovers AND pool 2 originals,
			#   mixing tiers unpredictably.
			# - threshold for triggering distribute lives in
			#   dplmc_auto_loot_all (auto path) and is currently disabled.
			#   The menu only exposes the manual button.
			# -------------------------------------------------------------------------
			("dplmc_pool_distribute",
				[],
				"Distribute items across 3 pools (sort + split).",
				[
					(troop_sort_inventory, "trp_temp_troop"),
					(troop_sort_inventory, "trp_dplmc_pool_2"),
					(troop_sort_inventory, "trp_dplmc_pool_3"),
					# bottom 1/3 of pool 1 -> pool 2
					(troop_get_inventory_capacity, ":cap1", "trp_temp_troop"),
					(store_div, ":start1", ":cap1", 3),
					(try_for_range_backwards, ":i_slot", ":start1", ":cap1"),
						(troop_get_inventory_slot, ":item", "trp_temp_troop", ":i_slot"),
						(ge, ":item", 0),
						(troop_get_inventory_slot_modifier, ":imod", "trp_temp_troop", ":i_slot"),
						(troop_add_item, "trp_dplmc_pool_2", ":item", ":imod"),
						(troop_set_inventory_slot, "trp_temp_troop", ":i_slot", -1),
					(try_end),
					# bottom 1/3 of pool 2 -> pool 3
					(troop_get_inventory_capacity, ":cap2", "trp_dplmc_pool_2"),
					(store_div, ":start2", ":cap2", 3),
					(try_for_range_backwards, ":i_slot", ":start2", ":cap2"),
						(troop_get_inventory_slot, ":item", "trp_dplmc_pool_2", ":i_slot"),
						(ge, ":item", 0),
						(troop_get_inventory_slot_modifier, ":imod", "trp_dplmc_pool_2", ":i_slot"),
						(troop_add_item, "trp_dplmc_pool_3", ":item", ":imod"),
						(troop_set_inventory_slot, "trp_dplmc_pool_2", ":i_slot", -1),
					(try_end),
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
				#Actually abandon the lost loot in all 3 pools
				(try_for_range, ":pool_idx", 0, 3),
					(try_begin),
						(eq, ":pool_idx", 0),
						(assign, ":abandon_pool", "$pool_troop"),
					(else_try),
						(eq, ":pool_idx", 1),
						(assign, ":abandon_pool", "trp_dplmc_pool_2"),
					(else_try),
						(eq, ":pool_idx", 2),
						(assign, ":abandon_pool", "trp_dplmc_pool_3"),
					(try_end),
					(troop_get_inventory_capacity, ":inv_cap", ":abandon_pool"),
					(try_for_range, ":i_slot", 10, ":inv_cap"),
						(troop_get_inventory_slot, ":item_id", ":abandon_pool", ":i_slot"),
						(ge, ":item_id", 0),
						(neg|troop_has_item_equipped, ":abandon_pool", ":item_id"),
						(troop_set_inventory_slot, ":abandon_pool", ":i_slot", -1), #delete it
						(troop_inventory_slot_set_item_amount, ":abandon_pool", ":i_slot", 0),
					(try_end),
				(try_end),

				#(jump_to_menu, "mnu_camp"),
				(set_player_troop, "trp_player"),
				(jump_to_menu, "$dplmc_return_menu"),
				(assign, "$pool_troop", -1), #mark ending
				##diplomacy end+
				]
			),
			##nested diplomacy start+
			#Leave & take everything you can (from all 3 pools)
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
					#Take remaining items for player from all 3 pools
					(try_for_range, ":pool_idx", 0, 3),
						(gt, ":space", 0),
						(try_begin),
							(eq, ":pool_idx", 0),
							(assign, ":take_pool", "$pool_troop"),
						(else_try),
							(eq, ":pool_idx", 1),
							(assign, ":take_pool", "trp_dplmc_pool_2"),
						(else_try),
							(eq, ":pool_idx", 2),
							(assign, ":take_pool", "trp_dplmc_pool_3"),
						(try_end),
						(troop_get_inventory_capacity, ":inv_cap", ":take_pool"),
						(troop_sort_inventory, ":take_pool"),
						(try_for_range, ":i_slot", 10, ":inv_cap"),
							(gt, ":space", 0),
							(troop_get_inventory_slot, ":item_id", ":take_pool", ":i_slot"),
							(ge, ":item_id", 0),
							(neg|troop_has_item_equipped, ":take_pool", ":item_id"),
							(troop_get_inventory_slot_modifier, ":imod", ":take_pool", ":i_slot"),
							(troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
							(val_sub, ":space", 1),
							(troop_set_inventory_slot, ":take_pool", ":i_slot", -1), #remove item from pool
							(troop_inventory_slot_set_item_amount, ":take_pool", ":i_slot", 0),
						(try_end),
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
					#Take remaining items for player from all 3 pools
					(try_for_range, ":pool_idx", 0, 3),
						(try_begin),
							(eq, ":pool_idx", 0),
							(assign, ":take_pool", "$pool_troop"),
						(else_try),
							(eq, ":pool_idx", 1),
							(assign, ":take_pool", "trp_dplmc_pool_2"),
						(else_try),
							(eq, ":pool_idx", 2),
							(assign, ":take_pool", "trp_dplmc_pool_3"),
						(try_end),
						(troop_get_inventory_capacity, ":inv_cap", ":take_pool"),
						(try_for_range, ":i_slot", 10, ":inv_cap"),
							(gt, ":space", 0),
							(troop_get_inventory_slot, ":item_id", ":take_pool", ":i_slot"),
							(ge, ":item_id", 0),
							(neg|troop_has_item_equipped, ":take_pool", ":item_id"),
							(troop_get_inventory_slot_modifier, ":imod", ":take_pool", ":i_slot"),
							(troop_add_item, "trp_player", ":item_id", ":imod"),#give item to player
							(val_sub, ":space", 1),
							(troop_set_inventory_slot, ":take_pool", ":i_slot", -1), #remove item frlom pool
							(troop_inventory_slot_set_item_amount, ":take_pool", ":i_slot", 0),
						(try_end),
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
