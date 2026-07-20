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

bank_quickview = ("bank_quickview", 0, mesh_companion_overview, #mesh_companion_overview
   [
     (ti_on_presentation_load,
      [
	    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

#		(str_clear, s0),
 #       (create_text_overlay, reg0, "@Hello, {s0}", tf_scrollable),
 #       (position_set_x, pos1, 50),
  #      (position_set_y, pos1, 50),
 ###       (overlay_set_position, reg0, pos1),
 #       (position_set_x, pos1, 550),
 #       (position_set_y, pos1, 630),
  #      (overlay_set_area_size, reg0, pos1),
 #       (set_container_overlay, reg0),




		###HEADLINES###
		(assign, ":x_poshl", 155),
		(assign, ":y_pos", 581),
		(assign, ":jq_size", pos0),
		(position_set_x, ":jq_size", 720),
		(position_set_y, ":jq_size", 775),

        (create_text_overlay, reg1, "@Town", tf_center_justify),
    	(overlay_set_size, reg1, ":jq_size"),
 		(position_set_x, pos1, ":x_poshl"),
        (position_set_y, pos1, ":y_pos"),
        (overlay_set_position, reg1, pos1),

        (create_text_overlay, reg1, "@Acres", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 120),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),

        (create_text_overlay, reg1, "@Owned", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 108),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),

        (create_text_overlay, reg1, "@Balance", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 112),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),

		(create_text_overlay, reg1, "@Assets", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 105),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),

        (create_text_overlay, reg1, "@Debt", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 105),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),

        (create_text_overlay, reg1, "@Deadline", tf_center_justify),
       	(overlay_set_size, reg1, ":jq_size"),
		(val_add, ":x_poshl", 120),
 		(position_set_x, pos1, ":x_poshl"),
        (overlay_set_position, reg1, pos1),


		(str_clear, s0),
		(create_text_overlay, reg0, s0, tf_scrollable),
        (position_set_x, pos1, 10),
        (position_set_y, pos1, 100),
        (overlay_set_position, reg0, pos1),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 450),
        (overlay_set_area_size, reg0, pos1),
		(set_container_overlay, reg0),

		(assign, ":jq_value", 100),
		(assign, ":jq_size", 0),
		(assign, ":x_pos", 0),
		(assign, ":y_pos", 547),
		(str_clear, s9),
		(str_clear, s8),


        (assign, reg2, 0),#total_acres
        (assign, reg3, 0),#player_acres
        (assign, reg4, 0),#balance
        (assign, reg5, 0),#assets
		(assign, reg6, 0),#debt
		(assign, reg7, 0),#deadline

		(try_for_range, ":center_no", towns_begin, towns_end),
			(party_get_slot, ":land_town", ":center_no", slot_town_acres),
			(party_get_slot, ":land_player", ":center_no", slot_player_acres),
			(party_get_slot, ":assets", ":center_no", slot_assets),
			(party_get_slot,":debt",":center_no",slot_debt),
			(party_get_slot, ":deadline", ":center_no", slot_deadline),
			(party_get_slot, ":population", ":center_no", slot_center_population),
			(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),

			(store_add, ":land_total", ":land_town", ":land_player"),

			(store_div, ":acres_needed", ":population", 200),
			(store_sub, ":surplus", ":land_total", ":acres_needed"),
			(store_sub, ":revenue", ":prosperity", 50),
			(val_add, ":revenue", 100),
			(assign, ":rent_player", 0),
			(assign, ":upkeep_player", 0),
			(try_begin),
				(gt, ":land_player", 0),												# 	Fix
			(try_begin),															#	Player Balance
				(le, ":land_total", ":acres_needed"),
				(store_mul, ":rent_player", ":land_player", ":revenue"),
			(else_try),
				(store_mul, ":penalty", ":surplus", -1),
				(val_add, ":penalty", ":revenue"),
				(try_begin),
					(ge, ":penalty", 85),
					(store_mul, ":rent_player", ":land_player", ":penalty"),
				(else_try),
					(store_sub, ":non_rented", ":surplus", 15),
						(store_sub, ":land_rented", ":land_player", ":non_rented"),					# Fixed, wrong display # if player owned too much land due to val_sub usage
						(store_mul, ":rent_player", ":land_rented", 85),
					(store_mul, ":upkeep_player", ":non_rented", -50),
				(try_end),
			(try_end),
			(try_end),

			(store_add, ":balance", ":rent_player", ":upkeep_player"),

			(val_add, ":jq_value", 1),

			#center center name
			(val_add, ":x_pos", 118),
			(str_store_party_name,s9, ":center_no"),
			(str_store_string, s1, "@{s9}"),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#center land in acres
			(val_add, ":x_pos", 135),
			(assign, reg2, ":land_total"),
			(create_text_overlay, reg1, "@{reg2}", tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#Player land in city
			(val_add, ":x_pos", 113),
			(assign, reg3, ":land_player"),
			(str_store_string, s1, "@{reg3}"),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#city Balance
			(val_add, ":x_pos", 110),
			(assign, reg4, ":balance"),
			(str_store_string, s1, "@{reg4}"),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#Player assets in city
			(val_add, ":x_pos", 110),
			(assign, reg4, ":assets"),
			(str_store_string, s1, "@{reg4}"),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#city Debt
			(val_add, ":x_pos", 105),
			(assign, reg5, ":debt"),
			(str_store_string, s1, "@{reg5}"),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			#city Deadline
			(val_add, ":x_pos", 105),
			(try_begin),
				(gt, ":deadline", 0),
				(call_script, "script_game_get_date_text", 1, ":deadline"),
			(else_try),
				(str_store_string, s1, "@None"),
			(try_end),
			(create_text_overlay, reg1, s1, tf_left_align),
			(position_set_x, pos3, ":x_pos"),
			(position_set_y, pos3, ":y_pos"),
			(overlay_set_position, reg1, pos3),
			(position_set_x, pos3, 750),
			(position_set_y, pos3, 850),
			(overlay_set_size, reg1, pos3),

			(assign, ":x_pos", 0),
			(assign, ":x_poshl", 165),
			(val_sub, ":y_pos", 23),#linebreak
			(ge, ":x_pos", 950),
			(assign, ":x_pos", 0),
			(val_sub, ":y_pos", 23),
		(try_end), #Center-Bank Loop End

	  (set_container_overlay, -1),

	  		 #Back to menu - graphical button
	    (create_game_button_overlay, "$g_jq_Return_to_menu", "@_Return to menu_"),
	    (position_set_x, pos1, 500),
        (position_set_y, pos1, 23),
        (overlay_set_position, "$g_jq_Return_to_menu", pos1),
		(assign, "$g_jq_Back_to_shop", 0), ##BUGFIX - savegame compatability
		(assign, "$jq_nr", 0), ##BUGFIX - savegame compatability

	  ]),
	 (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"),
		(try_begin),
			(eq, ":object", "$g_jq_Return_to_menu"),
			(presentation_set_duration, 0),
		(try_end),
		]),
	])
