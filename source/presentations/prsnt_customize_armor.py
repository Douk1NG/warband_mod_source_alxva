# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

customize_armor = ("customize_armor", prsntf_manual_end_only, 0, [
    (ti_on_presentation_load,
     [(set_fixed_point_multiplier, 1000),

      (assign, "$g_presentation_credits_obj_1", -1),		#tableau_custom_armor_window
      (assign, "$g_presentation_credits_obj_2", -1),		#tattoo
      (assign, "$g_presentation_credits_obj_3", -1),		#text - previous item
      (assign, "$g_presentation_credits_obj_4", -1),		#text - next item
      (assign, "$g_presentation_credits_obj_5", -1),		#button - set fix
      (assign, "$g_presentation_obj_item_select_1", -1),	#dropboxes - item components
	  (assign, "$g_dthehun_sync_random", 0),		#for character tableau random component alpha mask sync.

	  #background screen
      (try_begin),
        (create_mesh_overlay, reg0, "mesh_custom_bg"),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 1000),
        (position_set_y, pos1, 1000),
        (overlay_set_size, reg0, pos1),
      (try_end),
      #character background window
     # (try_begin),
     #   (create_mesh_overlay, reg0, "mesh_mp_score_a"),
     #   (position_set_x, pos1, 295),
     #   (position_set_y, pos1, 115),
     #   (overlay_set_position, reg0, pos1),
     #   (position_set_x, pos1, 1000),
     #   (position_set_y, pos1, 1000),
     #   (overlay_set_size, reg0, pos1),
     # (try_end),

      (item_get_slot, ":sub_part_total", "$g_current_opened_item_details", slot_item_num_components),
      (item_get_slot, ":script_no", "$g_current_opened_item_details", slot_item_init_script),

#COMBOS2 begin
	  (try_begin),
        (gt, ":script_no", 0),
        (assign, ":cur_x", 15),
        (assign, ":cur_y", 627),
		(position_set_x, pos3, 800),
		(position_set_y, pos3, 800),
        (try_for_range, ":sub_part", 0, ":sub_part_total"),
		#button (empty)
			#(assign, ":cur_mesh_slot", -1),
			(item_get_type, ":item_type", "$g_current_opened_item_details"),
			(try_begin), #armor or helmet?
				(eq, ":item_type", itp_type_body_armor),
				(assign, ":cur_mesh_slot", slot_troop_armor_slots_begin),
			(else_try),
				(eq, ":item_type", itp_type_head_armor),
				(assign, ":cur_mesh_slot", slot_troop_helm_slots_begin),
			(try_end),
			(val_add, ":cur_mesh_slot", ":sub_part"),
			#try: (ge, ":cur_mesh_slot", 0), # <- item is helm or armor
			(create_image_button_overlay, ":overlay", "mesh_custom_button_up", "mesh_custom_button_down"),
			(position_set_x, pos1, ":cur_x"),
			(position_set_y, pos1, ":cur_y"),
			(overlay_set_position, ":overlay", pos1),
		#item_image
			(store_add, ":mesh_x", ":cur_x", 50),
			(store_add, ":mesh_y", ":cur_y", 50),
			(position_set_x, pos2, ":mesh_x"),
			(position_set_y, pos2, ":mesh_y"),
			(troop_get_slot, ":cur_value", "$g_current_opened_troop_dthehun", ":cur_mesh_slot"),
			(call_script, ":script_no", -1, "$g_current_opened_troop_dthehun", ":sub_part", ":cur_value"), #-> s1(item_name), reg0(item_no)
			(try_begin),
				(neg|str_is_empty, s1),
				(assign, ":item_no", reg0),
				(create_mesh_overlay_with_item_id, reg0, ":item_no"),		  # <- 0: Invalid Item, n: Item Copmponent
			(else_try),
				(create_mesh_overlay_with_item_id, reg0, "itm_chest_b"), # <- RANDOM - add item overlay keep indexes unchanged
			(try_end),
			(overlay_set_position, reg0, pos2),
			(overlay_set_size, reg0, pos3),
			(val_sub, ":cur_y", 100), #resize this depending on amount in each combo?
			(try_begin),
				(lt, ":cur_y", 0),	#new column for combos #DtheHun
				(assign, ":cur_y", 627),
				(val_add, ":cur_x", 100),
				(position_set_x, pos1, ":cur_x"),
			(try_end),
		(try_end),
        #store as global
        (assign, "$g_presentation_obj_item_select_1", ":sub_part"),

		(try_begin),
		#show component selection palette
			(neq, "$g_presentation_state", 0),	#1-14
			(try_begin),
				(le, "$g_presentation_state", ":sub_part_total"),
				(assign, "$g_presentation_obj_item_select_1", "$g_presentation_state"), # remember selected mesh
			(try_end),
	#	  (assign, reg0, "$g_presentation_state"),
	#	  (display_message, "@State: {reg0}"),
			(assign, ":cur_y", 627),
			(assign, ":cur_x", 885),
			(position_set_x, pos1, ":cur_x"),
			(position_set_y, pos1, ":cur_y"),
			(assign, ":sub_part", "$g_presentation_state"),
			(val_sub, ":sub_part", 1), #0-13
			(call_script, ":script_no", -1, "$g_current_opened_troop_dthehun", ":sub_part", 0), #-> s1(item_name), reg0(item_no)
			(assign, ":sub_total", "$g_custom_armor_param_count"),		 		#$g <- setted up in init script
			(try_for_range, ":sub_material", 0, ":sub_total"),	#add 0.-> n. element
				(call_script, ":script_no", -1, "$g_current_opened_troop_dthehun", ":sub_part", ":sub_material"),
				(neg|str_is_empty, s1),	# -> no empty button after last component (CENSURE bypass problem)
				(create_image_button_overlay, ":overlay", "mesh_custom_button_up", "mesh_custom_button_down"),
				(position_set_x, pos1, ":cur_x"),
				(position_set_y, pos1, ":cur_y"),
				(overlay_set_position, ":overlay", pos1),
				(try_begin),
				#add subcomponent images
					(neg|str_is_empty, s1),
					(assign, ":item_no", reg0),
					(create_mesh_overlay_with_item_id, reg0, ":item_no"),
					(store_add, ":mesh_x", ":cur_x", 50),
					(store_add, ":mesh_y", ":cur_y", 50),
					(position_set_x, pos2, ":mesh_x"),
					(position_set_y, pos2, ":mesh_y"),
					(overlay_set_position, reg0, pos2),
					(overlay_set_size, reg0, pos3),
				(try_end),
				(val_sub, ":cur_y", 100),
				(try_begin),
					(lt, ":cur_y", 0),	#new column for combos #DtheHun
					(assign, ":cur_y", 625),
					(val_sub, ":cur_x", 100),
					(position_set_x, pos1, ":cur_x"),
				(try_end),
			(try_end),
		(try_end),
      (try_end),
	#COMBOS2 end

	#TEXT: NUM OF COMPONENTS
      (assign, reg1, ":sub_part_total"),
      (val_max, reg1, 0),
      (str_store_item_name, s1, "$g_current_opened_item_details"),
      (create_text_overlay, reg0, "@{s1} has {reg1} variable components", tf_center_justify|tf_single_line|tf_with_outline),
      (position_set_x, pos1, 500),
      (position_set_y, pos1, 680),
      (overlay_set_position, reg0, pos1),
      (overlay_set_color, reg0, 0xFFFFFF),
	#CHARACTER DISPLAY
      (create_image_button_overlay_with_tableau_material, "$g_presentation_credits_obj_1", -1, "tableau_custom_armor_window", "$g_current_opened_troop_dthehun"),
      (position_set_x, pos1, 320),	#380
      (position_set_y, pos1, 130),	#200
      (overlay_set_position, "$g_presentation_credits_obj_1", pos1),
      (position_set_x, pos1, 1500),
      (position_set_y, pos1, 1500),
      (overlay_set_size, "$g_presentation_credits_obj_1", pos1),
	#TATTOO
      (try_begin),
	  	(troop_get_type, ":is_female", "$g_current_opened_troop_dthehun"),
		(ge, ":is_female", 1),
		(assign, ":colors_begin", "str_ca_skin"),
		(assign, ":colors_end", "str_ca_custom"),
		(val_add, ":colors_end", 1),
        (create_combo_label_overlay, "$g_presentation_credits_obj_2"),		#2DIR BUTTON - TATTOO SELECT
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 80),
        (overlay_set_position, "$g_presentation_credits_obj_2", pos1),
        (try_for_range, ":color", ":colors_begin", ":colors_end"),
          (overlay_add_item, "$g_presentation_credits_obj_2", ":color"), 	# string no
        (try_end),
        (troop_get_slot, ":cur_color", "$g_current_opened_troop_dthehun", slot_troop_tattoo),
        (overlay_set_val, "$g_presentation_credits_obj_2", ":cur_color"), 	# label index (0,1,2,3...)
      (try_end),
	  (try_begin),
	    (item_slot_ge, "$g_current_opened_item_details", slot_item_num_components, 1),	#item is customizable
	#SELECTED ITEM ICON
		(position_set_y, pos1, 600),
		(try_begin),
			(eq, 1, 0), # NOT DISPLAY
			(create_mesh_overlay_with_item_id, reg0, "$g_current_opened_item_details", tf_center_justify|tf_single_line|tf_with_outline),	#BUTTON - ITEM SELECT
			(position_set_x, pos1, 490),
			(overlay_set_position, reg0, pos1),
		(try_end),
	#OTHER EQUIPPED ITEM - PREVIOUS
		(assign, ":had_active", 0),
		(assign, ":first_item", -1),
		(assign, ":end",  ek_foot),
		(try_for_range_backwards, ":item_slot", ek_item_0, ":end"),
			(troop_get_inventory_slot, ":item_no", "$g_current_opened_troop_dthehun", ":item_slot"),
			(gt, ":item_no", -1),										#has equipped item in the slot
			(item_slot_ge, ":item_no", slot_item_num_components, 1),	#item is customizable
			(try_begin),
				(eq, ":had_active", 0),
				(try_begin),
					(eq, ":first_item", -1),
					(assign, ":first_item", ":item_no"),
				(try_end),
				(try_begin),
					(eq, ":item_no", "$g_current_opened_item_details"),
					(assign, ":had_active", 1),
				(try_end),
			(else_try),
				(eq, ":had_active", 1),
				(assign, ":next_item", ":item_no"),
				(assign, ":end", -1), #END CYCLE
				(assign, ":had_active", 2),
			(try_end),
		(try_end),
		(try_begin),
			(eq, ":had_active", 1), #last item was active, no next item setted -> set first item (could remain the same)
			(assign, ":next_item", ":first_item"),
		(try_end),
		(try_begin),
			(neq, ":next_item", "$g_current_opened_item_details"), #only if next item is not the same as the selected
			(create_mesh_overlay_with_item_id, "$g_presentation_credits_obj_3", ":next_item", tf_center_justify|tf_single_line|tf_with_outline),	#BUTTON - ITEM SELECT
			#(str_store_item_name, s1, ":next_item"),
			#(create_button_overlay, "$g_presentation_credits_obj_3", "@{s1}", tf_center_justify|tf_single_line|tf_with_outline),	#BUTTON - ITEM SELECT
			(position_set_x, pos1, 360),
			#(position_set_y, pos1, 600),
			(overlay_set_position, "$g_presentation_credits_obj_3", pos1),
			(assign, ":prev_item", ":next_item"),
		#OTHER EQUIPPED ITEM - NEXT
			(assign, ":had_active", 0),
			(assign, ":first_item", -1),
			(assign, ":end",  ek_foot),
			(try_for_range, ":item_slot", ek_item_0, ":end"),
				(troop_get_inventory_slot, ":item_no", "$g_current_opened_troop_dthehun", ":item_slot"),
				(gt, ":item_no", -1),										#has equipped item in the slot
				(item_slot_ge, ":item_no", slot_item_num_components, 1),	#item is customizable
				(try_begin),
					(eq, ":had_active", 0),
					(try_begin),
						(eq, ":first_item", -1),
						(assign, ":first_item", ":item_no"),
					(try_end),
					(try_begin),
						(eq, ":item_no", "$g_current_opened_item_details"),
						(assign, ":had_active", 1),
					(try_end),
				(else_try),
					(eq, ":had_active", 1),
					(assign, ":next_item", ":item_no"),
					(assign, ":end", -1), #END CYCLE
					(assign, ":had_active", 2),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":had_active", 1), #last item was active, no next item setted -> set first item (could remain the same)
				(assign, ":next_item", ":first_item"),
			(try_end),
			(try_begin), # add button only if prev item != next item (there are more than 2 customizable items equipped)
				(neq, ":prev_item", ":next_item"),
				(create_mesh_overlay_with_item_id, "$g_presentation_credits_obj_4", ":next_item", tf_center_justify|tf_single_line|tf_with_outline),	#BUTTON - ITEM SELECT
				#(str_store_item_name, s1, ":next_item"),
				#(create_button_overlay, "$g_presentation_credits_obj_4", "@{s1}", tf_center_justify|tf_single_line|tf_with_outline),	#BUTTON - ITEM SELECT
				(position_set_x, pos1, 620),
				#(position_set_y, pos1, 600),
				(overlay_set_position, "$g_presentation_credits_obj_4", pos1),
			(try_end),
		  (try_end),
		#SET FIX
		  (position_set_y, pos1, 30),
		  (create_game_button_overlay, "$g_presentation_credits_obj_5", "@Fix"),		#BUTTON - SET FIX
		  (position_set_x, pos1, 500),
		  (overlay_set_position, "$g_presentation_credits_obj_5", pos1),
		#RANDOMIZE
		  (create_game_button_overlay, "$g_presentation_obj_profile_banner_selection_1", "@Mix"),	#BUTTON - RANDOMIZE
		  (position_set_x, pos1, 320),
		  (overlay_set_position, "$g_presentation_obj_profile_banner_selection_1", pos1),
	  (try_end),
	#DONE
	  (create_game_button_overlay, "$g_presentation_obj_profile_banner_selection_2", "str_done"),	#BUTTON - DONE
      (position_set_x, pos1, 680),
	  (position_set_y, pos1, 30),
      (overlay_set_position, "$g_presentation_obj_profile_banner_selection_2", pos1),
      (presentation_set_duration, 999999),
    ]),

    (ti_on_presentation_mouse_enter_leave,
       [(store_trigger_param_1, ":object"),
		(eq, 1, 0),	#NOT IN USE
        (try_begin),
          (eq, ":object", "$g_presentation_credits_obj_1"),
          (store_trigger_param_2, ":enter_leave"),
          (try_begin),
            (eq, ":enter_leave", 0),
            (try_begin),
              (assign, ":item_modifier", imod_plain),
              (item_get_type, ":item_type", "$g_current_opened_item_details"),
              (try_begin),
                (is_between, ":item_type", itp_type_head_armor, itp_type_pistol), #head/body/foot/hand
                (val_add, ":item_type", ek_head - itp_type_head_armor),
              (else_try), #pretty sure you can't customize ammo but w/e
                (this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_goods),
                (is_between, ":item_type", itp_type_pistol, itp_type_animal),
                #find it on the troop
                (try_for_range, ":slot_no", ek_item_0, ek_head),
                  (troop_get_inventory_slot, ":item_no", "$g_current_opened_troop_dthehun", ":slot_no"),
                  (eq, ":item_no", "$g_current_opened_item_details"),
                  (assign, ":item_type", ":slot_no"),
                (try_end),
              (try_end),
              (is_between, ":item_type", ek_item_0, ek_horse), #validate input
              (troop_get_inventory_slot_modifier, ":item_modifier", "$g_current_opened_troop_dthehun", ":item_type"),
              # (overlay_get_position, pos0, ":object"),
              (mouse_get_position, pos0),
              (show_item_details_with_modifier, "$g_current_opened_item_details", ":item_modifier", pos0, 100),
            (try_end),
          (else_try),
            (eq, ":enter_leave", 1),
            (close_item_details),
          (try_end),
        (try_end),
        ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
	#  (assign, reg0, ":object"),
    #  (assign, reg1, ":value"),
	#  (display_message, "@reg = object: {reg0} value: {reg1}"),
        (assign, ":continue", 0),
		(item_get_slot, ":sub_part_total", "$g_current_opened_item_details", slot_item_num_components),
		#(item_get_slot, ":script_no", "$g_current_opened_item_details", slot_item_init_script),
		(try_begin),
	#CHARACTER window
          (eq, ":object", "$g_presentation_credits_obj_1"), #tableau, switch view sides
          (val_add, "$g_custom_armor_angle", 1),
          (val_mod, "$g_custom_armor_angle", 6), #60x6
		(else_try),
	#TATTOO toggler
          (eq, ":object", "$g_presentation_credits_obj_2"), #combolabel, switch tattoos
		  (troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_tattoo, ":value"),
        (else_try),
	#RANDOMIZE reset slots to (-1)
			(eq, ":object", "$g_presentation_obj_profile_banner_selection_1"),
			(item_get_type, ":item_type", "$g_current_opened_item_details"),
			(try_begin), #armor or helmet?
				(eq, ":item_type", itp_type_body_armor),
				(assign, ":begin", slot_troop_armor_slots_begin),
			(else_try),
				(eq, ":item_type", itp_type_head_armor),
				(assign, ":begin", slot_troop_helm_slots_begin),
			(try_end),
			(store_add, ":end", ":begin", ":sub_part_total"),
			(try_for_range, ":slot_no", ":begin", ":end"),
				(troop_set_slot, "$g_current_opened_troop_dthehun", ":slot_no", -1), # randomize = -1
			(try_end),
        (else_try),
	#SET FIX, from "trp_array_a"
			(eq, ":object", "$g_presentation_credits_obj_5"),
			(item_get_type, ":item_type", "$g_current_opened_item_details"),
			(try_begin), #armor or helmet?
				(eq, ":item_type", itp_type_body_armor),
				(assign, ":begin", slot_troop_armor_slots_begin),
			(else_try),
				(eq, ":item_type", itp_type_head_armor),
				(assign, ":begin", slot_troop_helm_slots_begin),
			(try_end),
			(store_add, ":end", ":begin", ":sub_part_total"),
			(try_for_range, ":slot_no", ":begin", ":end"),
				(troop_get_slot, ":last_val", "trp_temp_array_a", ":slot_no"), # <- saved before tableou alpha (new randomization)
				(troop_set_slot, "$g_current_opened_troop_dthehun", ":slot_no", ":last_val"),
			(try_end),
        (else_try),
	#DONE - close
          (eq, ":object", "$g_presentation_obj_profile_banner_selection_2"),
          (assign, ":continue", -1),
          (presentation_set_duration, 0),																		 #- /NOT IN USE
        (else_try),
	#COMBOS - item components || subcomponents palette
		  (ge, "$g_presentation_obj_item_select_1", 0),	#	-1: by default, 0:for 1 customizable element, ...
		# object -> selected component index
		  (store_sub, ":mesh_num", ":object", 1),
		  (val_div, ":mesh_num", 2),
		  (val_add, ":mesh_num", 1),
		  (assign, "$g_presentation_state", ":mesh_num"), #(1-14)
		  (val_sub, ":mesh_num", 1),	#(0-13)
	#	(assign, reg0 ,":sub_part_total"),
	#	(display_message, "@SPT: {reg0}"),
			(try_begin),
				(gt, "$g_presentation_state", ":sub_part_total"), #$g_presentation_state - has the mesh num (no+1)
				(assign, "$g_presentation_state", "$g_presentation_obj_item_select_1"),	# keep open palette for last mesh
				(store_sub, ":component", ":mesh_num", ":sub_part_total"),
	#		  (assign, reg0 ,":mesh_num"),
	#		  (display_message, "@MN: {reg0}"),

				(store_sub, ":cur_mesh_slot", "$g_presentation_obj_item_select_1", 1),
				(item_get_type, ":item_type", "$g_current_opened_item_details"),
				(try_begin),
					(eq, ":item_type", itp_type_body_armor),
					(val_add, ":cur_mesh_slot", slot_troop_armor_slots_begin),
				(else_try),
					(eq, ":item_type", itp_type_head_armor),
					(val_add, ":cur_mesh_slot", slot_troop_helm_slots_begin),
				(try_end),

				(try_begin),
				# CENSORED
					#(eq, "$g_cenzura", 1),
					(eq, 1, 0),
					(eq, ":item_type", itp_type_body_armor),	# body armor component
					(assign, ":censure_response", 0),
					(try_begin),
						(eq, ":component", 0),						# remove
						(try_begin),
							(eq, ":cur_mesh_slot", slot_troop_armor_slots_begin + 0),	#SKIN -> grant CHEST piece and PANTY
							(try_begin),
								(troop_get_slot, ":substitute", "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 1),
								(eq, ":substitute", 0),	# not has chest piece
								(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 1, 1),	#equip first CHEST
								(assign, ":censure_response", 1),
							(try_end),
							(try_begin),
								(troop_get_slot, ":substitute", "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 2),
								(eq, ":substitute", 0),	# not has panty
								(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 2, 1),	#equip first PANTY
								(assign, ":censure_response", 1),
							(try_end),
						(else_try),
							(eq, ":cur_mesh_slot", slot_troop_armor_slots_begin + 1),	#CHEST -> grant SKIN piece
							(troop_get_slot, ":substitute", "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 0),
							(le, ":substitute", 0),	# not has skin piece || random
							(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 0, 1),	#equip first SKIN
							(assign, ":censure_response", 1),
						(else_try),
							(eq, ":cur_mesh_slot", slot_troop_armor_slots_begin + 2),	#PANTY -> grant SKIN piece (not assassin)
							(troop_get_slot, ":substitute", "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 0),
							(le, ":substitute", 1),	# not has skin piece || has assassin skin (no bottom) || random
							(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 0, 2),	#equip second SKIN
							(assign, ":censure_response", 1),
						(try_end),
					(else_try),
						(eq, ":component", 1),						# add first
						(eq, ":cur_mesh_slot", slot_troop_armor_slots_begin + 0),	#SKIN -> grant PANTY (assassin skin has no bottom)
						(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 2, 1),	#equip first panty
					(try_end),
					(try_begin),
						(eq, ":censure_response", 1),
						(store_random_in_range, ":censure_response", "str_censure_response_0", "str_censure_response_end"),
						(str_store_troop_name, s0, "$g_current_opened_troop_dthehun"),
						(str_store_string, s1, ":censure_response"),
						(try_begin),
							(eq, "$g_current_opened_troop_dthehun", "trp_player"),
							(assign, ":text_color", 0xFFFFFF),
						(else_try),
							(assign, ":text_color", 0x00FF00),
						(try_end),
						(display_message, "@[{s0}]: {s1}", ":text_color"),
					(try_end),
				(try_end),
				#SPECIAL CASES (assa cover, Angela cover)
				(try_begin),
					(eq, ":item_type", itp_type_body_armor),	# body armor component
					(try_begin),
						(this_or_next|eq, ":component", 1),						# add assa cover
						             (eq, ":component", 2),						# add Angela cover
						(eq, ":cur_mesh_slot", slot_troop_armor_slots_begin + 4),	#SKIRT: assa cover -> grant something to hang it from
						(try_begin),
							(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 0, 1), 	#has assa skin
							(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 1), 	#has assa panty
							(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 2), 	#has Angela panty
							(troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 3, 1), 				#has assa belt
						(else_try),	#<- there is nothing to hanging on it
							(troop_set_slot, "$g_current_opened_troop_dthehun", slot_troop_armor_slots_begin + 2, 1),	#equip assa panty
						(try_end),
					(try_end),
				(try_end),
				# Do the change anyway (if the game mode is CENSORED, substitution has already been granted at this point)
				(troop_set_slot, "$g_current_opened_troop_dthehun", ":cur_mesh_slot", ":component"), # set(remove) component mesh
			(try_end),

        (try_end),
        (try_begin),
          (eq, ":continue", 0),
          (start_presentation, "prsnt_customize_armor"),
          (try_begin), #refresh me
            # (in_meta_mission),
            (get_player_agent_no, ":player_agent"),
            (gt, ":player_agent", -1),
            (agent_has_item_equipped, ":player_agent", "$g_current_opened_item_details"),
            (agent_unequip_item, ":player_agent", "$g_current_opened_item_details"),
			(agent_set_slot, ":player_agent", slot_agent_has_been_here_before, 0), # use troop slots
            (agent_equip_item, ":player_agent", "$g_current_opened_item_details"),
          (try_end),
        (try_end),
      ]),


	(ti_on_presentation_mouse_press, #click on items
       [
		(store_trigger_param_1, ":object"),
		(assign, ":continue", 0),
		(try_begin),
	  #ITEM toggler - previous
			(eq, ":object", "$g_presentation_credits_obj_3"),
			(assign, "$g_presentation_state", 0),
			(assign, ":continue", 1),
			(assign, ":had_active", 0),
			(assign, ":first_item", -1),
			(assign, ":end",  ek_foot),
			(try_for_range_backwards, ":item_slot", ek_item_0, ":end"),
				(troop_get_inventory_slot, ":item_no", "$g_current_opened_troop_dthehun", ":item_slot"),
				(gt, ":item_no", -1),										#has equipped item in the slot
				(item_slot_ge, ":item_no", slot_item_num_components, 1),	#item is customizable
				(try_begin),
					(eq, ":had_active", 0),
					(try_begin),
						(eq, ":first_item", -1),
						(assign, ":first_item", ":item_no"),
					(try_end),
					(try_begin),
						(eq, ":item_no", "$g_current_opened_item_details"),
						(assign, ":had_active", 1),
					(try_end),
				(else_try),
					(eq, ":had_active", 1),
					(assign, ":next_item", ":item_no"),
					(assign, ":end", -1), #END CYCLE
					(assign, ":had_active", 2),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":had_active", 1), #last item was active, no next item setted -> set first item (could remain the same)
				(assign, ":next_item", ":first_item"),
			(try_end),
			(assign, "$g_current_opened_item_details", ":next_item"),
        (else_try),
	  #ITEM toggler - next
			(eq, ":object", "$g_presentation_credits_obj_4"),
			(assign, "$g_presentation_state", 0),
			(assign, ":continue", 1),
			(assign, ":had_active", 0),
			(assign, ":first_item", -1),
			(assign, ":end",  ek_foot),
			(try_for_range, ":item_slot", ek_item_0, ":end"),
				(troop_get_inventory_slot, ":item_no", "$g_current_opened_troop_dthehun", ":item_slot"),
				(gt, ":item_no", -1),										#has equipped item in the slot
				(item_slot_ge, ":item_no", slot_item_num_components, 1),	#item is customizable
				(try_begin),
					(eq, ":had_active", 0),
					(try_begin),
						(eq, ":first_item", -1),
						(assign, ":first_item", ":item_no"),
					(try_end),
					(try_begin),
						(eq, ":item_no", "$g_current_opened_item_details"),
						(assign, ":had_active", 1),
					(try_end),
				(else_try),
					(eq, ":had_active", 1),
					(assign, ":next_item", ":item_no"),
					(assign, ":end", -1), #END CYCLE
					(assign, ":had_active", 2),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":had_active", 1), #last item was active, no next item setted -> set first item (could remain the same)
				(assign, ":next_item", ":first_item"),
			(try_end),
			(assign, "$g_current_opened_item_details", ":next_item"),
        (try_end),
        (try_begin),
          (eq, ":continue", 1),
          (start_presentation, "prsnt_customize_armor"),
		(try_end),
	  ]),

	#ESC - close
	(ti_on_presentation_run, # remove body mesh on ESC quit from scene customization (also adding ESC quit to map action menu customization)
       [
        #(store_trigger_param_1, ":cur_time"),
        #(gt, ":cur_time", 500),
        (try_begin),
          #(this_or_next|key_clicked, key_space),
          #(this_or_next|key_clicked, key_enter),
          (key_clicked, key_escape),
          (presentation_set_duration, 0),
		(try_end),
	  ]),
    ])
