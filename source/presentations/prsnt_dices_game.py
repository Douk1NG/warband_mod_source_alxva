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

dices_game = ("dices_game", 0, 0,#dices game reg0
   [
    (ti_on_presentation_load,
       [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),
        #(call_script, "script_pos_helper",1),
        (call_script, "script_mmc_gamblers_header"),
        ]),

    (ti_on_presentation_run,#
       [#(call_script, "script_pos_helper",2),
	    (store_trigger_param_1, ":cur_time"),
        (set_fixed_point_multiplier, 1000),
		(ge, ":cur_time",500),
		    (try_begin),
		        (eq, reg50, 0),
                (assign, reg50, 1),
                (create_mesh_overlay, "$g_presentation_obj_6", "mesh_3card_window"),
                (position_set_x, pos6, 335),
                (position_set_y, pos6, 265),
                (position_set_x, pos1, 500),#
                (position_set_y, pos1, 500),#
                (overlay_set_size, "$g_presentation_obj_6", pos1),
		        (store_troop_gold,":plr_gold","trp_player"),#
		            (try_begin),
			            (ge,":plr_gold",50),
                        (assign,":bet50",50),
 			        (else_try),
			            (assign,":bet50",":plr_gold"),
		            (try_end),

			        (try_begin),
		                (eq,"$g_gamble",1),
     			        (assign,reg51,"$temp"),
			        (else_try),
                        (create_slider_overlay, "$g_presentation_obj_7", 1, ":bet50"),#
                        (overlay_set_val, "$g_presentation_obj_7", reg51),
                        (position_set_x, pos7, 510),
                        (position_set_y, pos7, 360),
			        (try_end),
                (create_text_overlay, "$g_presentation_obj_8", "@Bet: {reg51} Denar(s)"),#
                (position_set_x, pos8, 450),
                (position_set_y, pos8, 400),
                (create_game_button_overlay, "$g_presentation_obj_10", "@Done", tf_center_justify),#
                (position_set_x, pos10, 500),
                (position_set_y, pos10, 284),
                (overlay_set_position, "$g_presentation_obj_6", pos6),
		            (try_begin),
			            (eq,"$g_gamble",0),
                        (overlay_set_val, "$g_presentation_obj_7", reg51),
                        (overlay_set_position, "$g_presentation_obj_7", pos7),
		            (try_end),
                (overlay_set_position, "$g_presentation_obj_8", pos8),
                (overlay_set_position, "$g_presentation_obj_10", pos10),
            (try_end),

            (try_begin),
		        (eq, reg50, 2),
                (assign, reg50, 3),
                (create_game_button_overlay, "$g_presentation_obj_14", "@Roll Dice", tf_center_justify),#
                (position_set_x, pos1, 475),
                (position_set_y, pos1, 515),
                (overlay_set_position, "$g_presentation_obj_14", pos1),
	        (try_end),

		    (try_begin),
		        (eq, reg50, 4),
                (assign, reg50, 5),
                (call_script, "script_d6_roll",0),# d6_1
                (assign, reg10, reg1),
                (call_script, "script_d6_roll",0),# d6_2
		        (assign, reg20, reg1),
                # (call_script, "script_d6_roll",0),# d6_3
		        # (assign, reg30, reg1),
		    	(store_add, reg3, reg10, reg20),
				# (val_add,reg3,reg30),
			        (try_begin),
                        (store_random_in_range,reg11,1,7),# dice1 start side
                        (store_random_in_range,reg21,1,7),# dice2 start side
						# (store_random_in_range,reg31,1,7),# dice3 start side
                            (try_begin),
                                (gt, reg11, reg10),
                                (val_add, reg10, 6),
			                (try_end),
			        	    (try_begin),
                                (gt,reg21,reg20),
                                (val_add,reg20,6),
					        (try_end),
			        	    # (try_begin),# dice3
                                # (gt,reg31,reg30),# dice3
                                # (val_add,reg30,6),# dice3
					        # (try_end),# dice3
				    (try_end),
				(assign, reg5, 0),
				(assign, reg6, 0),
                (assign, reg58,":cur_time"),
		    (try_end),

		    (try_begin),
		        (eq, reg50, 5),
                (eq, reg6, 0),
		        (lt, reg5, 6),
				(store_sub, ":time_pass",":cur_time",reg58),
                (ge, ":time_pass",200),
                (assign, reg58,":cur_time"),
                (val_add, reg5,1),
				    (try_begin),
    	    	        (le, reg11, reg10),
	                    (call_script, "script_draw_d6_side",1,reg5,reg11),
						(val_add, reg11, 1),
					(try_end),
					(try_begin),
				        (le,reg21,reg20),
	                    (call_script, "script_draw_d6_side",2,reg5,reg21),
						(val_add,reg21,1),
					(try_end),
					# (try_begin),# dice3
				        # (le,reg31,reg30),# dice3
	                    # (call_script, "script_draw_d6_side",3,reg5,reg31),# dice3
						# (val_add,reg31,1),# dice3
					# (try_end),
			(else_try),
                (eq, reg50, 5),
                (eq, reg5, 6),
			    (assign, reg6, 1),
                (assign, reg50, 6),
                (assign, reg58,":cur_time"),
		    (try_end),
		(ge, reg6, 1),
		    (try_begin),
                (eq, reg6, 1),
                (eq, reg50, 6),
                (assign, reg50, 7),
                (eq, reg5, 6),
                (str_store_string, s1, "@{reg3}"),
                (create_text_overlay, "$g_presentation_obj_15", "@{s1}", tf_center_justify),
                (position_set_x, pos1, 850),
                (position_set_y, pos1, 470),
                (overlay_set_position, "$g_presentation_obj_15", pos1),#sum
                (position_set_x, pos1, 5000),
                (position_set_y, pos1, 5000),
                (overlay_set_size, "$g_presentation_obj_15", pos1),
                (assign, reg50, 8),
		    (try_end),

		    (try_begin),
		        (eq, reg50, 8),
                (assign, reg50, 9),
		    	(overlay_set_display, "$g_presentation_obj_14", 0),
	            (str_store_troop_name, s1, "$g_talk_troop"),
                (create_game_button_overlay, "$g_presentation_obj_14", "@{s1} Rolls", tf_center_justify),#
                (position_set_x, pos1, 475),
                (position_set_y, pos1, 515),
                (overlay_set_position, "$g_presentation_obj_14", pos1),
	        (try_end),

			(try_begin),
		        (eq, reg50, 10),#80
                (assign, reg50, 11),
		    	(overlay_set_display, "$g_presentation_obj_1", 0),
		    	(overlay_set_display, "$g_presentation_obj_2", 0),
				#(overlay_set_display, "$g_presentation_obj_3", 0),# dice3
                (call_script, "script_d6_roll",0),# d6_1
                (assign, reg10, reg1),
                (call_script, "script_d6_roll",0),# d6_2
		        (assign, reg20, reg1),
				(store_add, reg4, reg10, reg20),
                # (call_script, "script_d6_roll",0),# d6_3
		        # (assign, reg30, reg1),
				# (val_add,reg4,reg30),
			        (try_begin),
                        (store_random_in_range,reg11,1,7),# dice1 start side
                        (store_random_in_range,reg21,1,7),# dice2 start side
						# (store_random_in_range,reg31,1,7),# dice3 start side
                            (try_begin),
                                (gt, reg11, reg10),
                                (val_add, reg10, 6),
			                (try_end),
			        	    (try_begin),
                                (gt,reg21,reg20),
                                (val_add,reg20,6),
					        (try_end),
			        	    # (try_begin),# dice3
                                # (gt,reg31,reg30),# dice3
                                # (val_add,reg30,6),# dice3
					        # (try_end),# dice3
				    (try_end),
				(assign, reg5, 0),
				(assign, reg6, 2),
                (assign, reg58,":cur_time"),
		    (try_end),

		    (try_begin),
		        (eq, reg50, 11),
                (eq, reg6, 2),
		        (lt, reg5, 6),
				(store_sub, ":time_pass",":cur_time",reg58),
                (ge, ":time_pass",200),
                (assign, reg58,":cur_time"),
                (val_add, reg5,1),
				    (try_begin),
    	    	        (le, reg11, reg10),
	                    (call_script, "script_draw_d6_side",1,reg5,reg11),
						(val_add, reg11, 1),
					(try_end),
					(try_begin),
				        (le,reg21,reg20),
	                    (call_script, "script_draw_d6_side",2,reg5,reg21),
						(val_add,reg21,1),
					(try_end),
					# (try_begin),# dice3
				        # (le,reg31,reg30),# dice3
	                    # (call_script, "script_draw_d6_side",3,reg5,reg31),# dice3
						# (val_add,reg31,1),# dice3
					# (try_end),
			(else_try),
		        (eq, reg50, 11),
                (eq, reg5, 6),
			    (assign, reg6, 3),
                (assign, reg50, 12),
		    (try_end),
	(gt, reg6, 2),
		(try_begin),
		    (eq, reg50, 12),
            (eq, reg6, 3),
            (str_store_string, s1, "@{reg4}"),
            (create_text_overlay, "$g_presentation_obj_15", "@{s1}", tf_center_justify),
            (position_set_x, pos1, 130),
            (position_set_y, pos1, 180),
            (overlay_set_position, "$g_presentation_obj_15", pos1),#sum
            (position_set_x, pos1, 5000),
            (position_set_y, pos1, 5000),
            (overlay_set_size, "$g_presentation_obj_15", pos1),
            (assign, reg50, 13),
		(try_end),

		(try_begin),
		    (str_clear,s1),
		    (eq, reg50, 13),
			(overlay_set_display, "$g_presentation_obj_14", 0),
			(assign, reg50, 14),
                (try_begin),
                    (eq,reg3,reg4),
					(str_clear,s1),
                    (str_store_string, s1, "@Draw! Bet Twice?"),# Bet Twice?
					(assign, reg50, 15),
				(else_try),
	                (gt, reg3, reg4),
                    (val_mul,reg51,2),
					(call_script, "script_troop_add_gold", "trp_player", reg51),
                    (str_store_string, s1, "@You win! Try again?"),
				(else_try),
                    (gt, reg4, reg3),
                    (str_store_string, s1, "@You lose. Try again?"),
                (try_end),
                (create_text_overlay, reg1, "@{s1}", tf_center_justify),
                (position_set_x, pos1, 480),
                (position_set_y, pos1, 650),
                (overlay_set_position, reg1, pos1),#
                (position_set_x, pos1, 2000),
                (position_set_y, pos1, 2000),
                (overlay_set_size, reg1, pos1),#
                (create_mesh_overlay, reg1, "mesh_3card_window"),
                (position_set_x, pos1, 306),#
                (position_set_y, pos1, 580),#
                (overlay_set_position, reg1, pos1),
                (position_set_x, pos1, 500),#
                (position_set_y, pos1, 300),#
                (overlay_set_size, reg1, pos1),

                (create_game_button_overlay, "$g_presentation_obj_12", "@Yes", tf_center_justify),
                (position_set_x, pos1, 400),
                (position_set_y, pos1, 600),
                (overlay_set_position, "$g_presentation_obj_12", pos1),

                (create_game_button_overlay, "$g_presentation_obj_13", "@No", tf_center_justify),
                (position_set_x, pos1, 560),
                (position_set_y, pos1, 600),
                (overlay_set_position, "$g_presentation_obj_13", pos1),
		(try_end),
       ]),

      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        (try_begin),
		  (eq,"$g_gamble",0),
          (eq, ":object", "$g_presentation_obj_7"),#
          (try_begin),
            (neq, reg51, ":value"),
            (assign, reg51, ":value"),
          (try_end),
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (str_store_string, s1, "@Bet: {reg51} Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_8", s1),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),#
          (store_troop_gold,reg1,"trp_player"),#
          (try_begin),
            (lt,reg1,reg51),#
            (display_message, "@You don't have enough money."),
          (else_try),
            (troop_remove_gold, "trp_player", reg51),#
            (play_sound, "snd_money_paid"),
            (overlay_set_display, "$g_presentation_obj_6", 0),
		      (try_begin),
			    (eq,"$g_gamble",0),
			    (overlay_set_display, "$g_presentation_obj_7", 0),
			  (try_end),
            (overlay_set_display, "$g_presentation_obj_8", 0),
            (overlay_set_display, "$g_presentation_obj_10", 0),
            (store_troop_gold,reg1,"trp_player"),#
            (str_store_string, s1, "@Bet: {reg51} Denar(s)"),#
            (overlay_set_text, "$g_presentation_obj_4", s1),
            (str_store_string, s1, "@Money: {reg1} Denar(s)"),#
            (overlay_set_text, "$g_presentation_obj_5", s1),
            (assign, reg50, 2),
          (try_end),
		(try_end),
        (try_begin),
		    (eq, reg50, 3),
            (eq, ":object", "$g_presentation_obj_14"),#Roll Dice button
            (play_sound, "snd_dice_roll"),
		    (assign, reg50, 4),
		(try_end),
        (try_begin),
		    (eq, reg50, 9),
            (eq, ":object", "$g_presentation_obj_14"),#Oppo Roll Dice button
            (play_sound, "snd_dice_roll"),
		    (assign, reg50, 10),
		(try_end),

        (try_begin),#DRAW
	      (eq, reg50, 15),#
		  (eq,reg3,reg4),#
		  (assign,"$g_gamble",0),
          (eq, ":object", "$g_presentation_obj_12"),#yes
          (store_troop_gold,reg1,"trp_player"),#
          (try_begin),
            (lt,reg1,reg51),#
            (display_message, "@You don't have enough money."),
          (else_try),
            (presentation_set_duration, 0),
		    (assign,"$g_gamble",1),
			(val_mul,reg51,2),
			(assign,"$temp",reg51),
            (call_script, "script_troop_add_gold", "trp_player", reg51),
            (assign, reg50,0),
            (start_presentation, "prsnt_dices_game"),
          (try_end),
        (else_try),
          (eq, ":object", "$g_presentation_obj_13"),#no
		  #(call_script, "script_troop_add_gold", "trp_player", reg51),
          (assign,reg1,0),#
          (assign, reg51, 1),
          (presentation_set_duration, 0),
        (try_end),

        (try_begin),
	      (eq, reg50, 14),#12
          (eq, ":object", "$g_presentation_obj_12"),#yes
          (store_troop_gold,reg1,"trp_player"),#
          (try_begin),
            (lt,reg1,1),#
            (display_message, "@You don't have enough money."),
          (else_try),
            (presentation_set_duration, 0),
            (assign, reg50,0),
			(assign,"$g_gamble",0),
            (start_presentation, "prsnt_dices_game"),
          (try_end),
        (else_try),
          (eq, ":object", "$g_presentation_obj_13"),#no
		  (assign,"$g_gamble",0),
          (presentation_set_duration, 0),
        (try_end),
        ]),
     ])
