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

three_card = ("three_card", 0, 0,#find the lady
   [
     (ti_on_presentation_load,
      [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),

#Little Pos Helper by Kuba begin
#		(create_text_overlay, "$g_little_pos_helper", "@00,00"),
#		(overlay_set_color, "$g_little_pos_helper", 0xFFFFFFFF),
#		(position_set_x, pos1, 10),
#		(position_set_y, pos1, 700),
#		(overlay_set_position, "$g_little_pos_helper", pos1),
#Little Pos Helper by Kuba end

		(assign,"$g_presentation_obj_card1",-1),
		(assign,"$g_presentation_obj_card2",-1),
        (assign,"$g_presentation_obj_card3",-1),
        (assign,"$g_presentation_obj_1",-1), # mesh king of spades
        (assign,"$g_presentation_obj_2",-1), # mesh queen of heart
        (assign,"$g_presentation_obj_3",-1), # mesh king of clubs
        (assign,"$g_presentation_obj_4",-1), # text "@Bet: {reg51} Denar(s)"
        (assign,"$g_presentation_obj_5",-1), # text "@Money: {reg1} Denar(s)"
        (assign,"$g_presentation_obj_6",-1), # "mesh_text_bar"
        (assign,"$g_presentation_obj_7",-1), # slider
        (assign,"$g_presentation_obj_8",-1), # text "@Bet: {reg51} Denar(s)" above slider
        (assign,"$g_presentation_obj_9",-1), # win or lose window
        (assign,"$g_presentation_obj_10",-1), #done button
        (assign,"$g_presentation_obj_11",-1), #find the lady
        (assign,"$g_presentation_obj_12",-1),#yes
        (assign,"$g_presentation_obj_13",-1),#no
        (assign,"$g_presentation_obj_14",-1),#start game button
        (assign,"$g_presentation_obj_15",-1),
        (assign,"$g_presentation_obj_16",-1),
        (assign,"$g_presentation_obj_17",-1),
		(assign, reg1,0),
		(assign, reg2,0),
		(assign, reg3,0),
        (assign, reg50, 0),
        (assign, reg51, 1),
        (assign, reg52, 0),
        (assign, reg55, 1),
        (assign, reg58, 0),
		(str_clear,s1),
        (create_mesh_overlay, reg1, "mesh_3card_table"),#mesh_wood_table
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),

        (str_store_troop_name, s1, "$g_talk_troop"),# NPC
        (create_text_overlay, reg1, "@{s1}", tf_center_justify),
        (position_set_x, pos1, 120),#820
        (position_set_y, pos1, 470),#470
        (overlay_set_position, reg1, pos1),#
        (overlay_set_color, reg1, 0xffffff),
        (str_store_troop_name, s1, "trp_player"),#
        (create_text_overlay, reg1, "@{s1}", tf_center_justify),
        (position_set_x, pos1, 815),#120
        (position_set_y, pos1, 8),#8
        (overlay_set_position, reg1, pos1),#
        (overlay_set_color, reg1, 0xffffff),
         # "mesh_jack_black_portrait"
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "$g_talk_troop"),#-1
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 7),#700
        (position_set_y, pos1, 500),#500
        (overlay_set_position, reg1, pos1),
         #"mesh_trp_player_portrait"
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "trp_player"),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 740),#7
        (position_set_y, pos1, 45),#20
        (overlay_set_position, reg1, pos1),

# info window right
        (create_mesh_overlay, reg1, "mesh_3card_window"),#3card_textbar#text_bar
        (position_set_x, pos1, 780),#700
        (position_set_y, pos1, 310),#270
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 250),#
        (position_set_y, pos1, 200),#
        (overlay_set_size, reg1, pos1),

        (str_store_string, s1, "@Bet: {reg51} Denar(s)"),#
        (create_text_overlay, "$g_presentation_obj_4", s1),#
        (position_set_x, pos1, 790),#755
        (position_set_y, pos1, 355),#355
        (overlay_set_position, "$g_presentation_obj_4", pos1),
        (overlay_set_color, "$g_presentation_obj_4",),#0xfffccc
        (store_troop_gold,reg1,"trp_player"),#
        (create_text_overlay, "$g_presentation_obj_5", "@Money: {reg1} Denar(s)"),
        (position_set_x, pos1, 790),#755
        (position_set_y, pos1, 325),#325
        (overlay_set_position, "$g_presentation_obj_5", pos1),
        (overlay_set_color, "$g_presentation_obj_5"),#0xfffccc
        ]),

      (ti_on_presentation_run,#
       [
#Little Pos Helper by Kuba begin
#		(mouse_get_position, pos1),
#		(position_get_x, reg1, pos1),
#		(position_get_y, reg2, pos1),
#		(overlay_set_text, "$g_little_pos_helper", "@{reg1},{reg2}"),
#Little Pos Helper by Kuba end
	    (store_trigger_param_1, ":cur_time"),
        (set_fixed_point_multiplier, 1000),
        (ge, ":cur_time",500),
        (try_begin),
		  (eq, reg50, 0),
          (assign, reg50, 1),#3
          (create_mesh_overlay, "$g_presentation_obj_6", "mesh_3card_window"), #"mesh_text_bar"
          (position_set_x, pos6, 335),#685 #345
          (position_set_y, pos6, 265),#482 #217
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
          (create_slider_overlay, "$g_presentation_obj_7", 1, ":bet50"),#
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (position_set_x, pos7, 510),
          (position_set_y, pos7, 360),
          (create_text_overlay, "$g_presentation_obj_8", "@Bet: {reg51} Denar(s)"),#
          (position_set_x, pos8, 450),#420
          (position_set_y, pos8, 400),
          (create_game_button_overlay, "$g_presentation_obj_10", "@Done", tf_center_justify),#
          (position_set_x, pos10, 500),
          (position_set_y, pos10, 284),
          (overlay_set_position, "$g_presentation_obj_6", pos6),
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (overlay_set_position, "$g_presentation_obj_7", pos7),
          (overlay_set_position, "$g_presentation_obj_8", pos8),
          (overlay_set_position, "$g_presentation_obj_10", pos10),
        (try_end),#

        (try_begin),
		    (eq, reg50, 2),
            (assign, reg50, 3),#5
            (position_set_x, pos14, 375),#
            (position_set_y, pos14, 550),
	# King of Spades
            (create_mesh_overlay, "$g_presentation_obj_1", "mesh_3card_kos"),#
            (position_set_x, pos1, 275),
            (position_set_y, pos1, 300),
			(overlay_set_position, "$g_presentation_obj_1", pos1),
			(overlay_set_size, "$g_presentation_obj_1", pos14),#
	# Queen of Heart
            (create_mesh_overlay, "$g_presentation_obj_2", "mesh_3card_qoh"),#
            (position_set_x, pos1, 425),
            (position_set_y, pos1, 300),
			(overlay_set_position, "$g_presentation_obj_2", pos1),
			(overlay_set_size, "$g_presentation_obj_2", pos14),#
	# King of Clubs
            (create_mesh_overlay, "$g_presentation_obj_3", "mesh_3card_koc"),#
            (position_set_x, pos1, 575),
            (position_set_y, pos1, 300),
			(overlay_set_position, "$g_presentation_obj_3", pos1),
			(overlay_set_size, "$g_presentation_obj_3", pos14),#
	#start game button
            (create_game_button_overlay, "$g_presentation_obj_14", "@Start Game", tf_center_justify),#
            (position_set_x, pos1, 475),
            (position_set_y, pos1, 600),
            (overlay_set_position, "$g_presentation_obj_14", pos1),
	    (try_end),

         (try_begin),
		     (eq, reg50, 4),
			 (assign,reg50, 5),
             (overlay_set_display, "$g_presentation_obj_14", 0),#start game button
             (assign,reg58,":cur_time"),
             (overlay_set_display, "$g_presentation_obj_1", 0),
             (overlay_set_display, "$g_presentation_obj_2", 0),
             (overlay_set_display, "$g_presentation_obj_3", 0),

            (try_begin),
                (create_mesh_overlay, "$g_presentation_obj_16", "mesh_3card_back", "mesh_3card_back"),#
                (position_set_x, pos15, 275),
                (position_set_y, pos15, 300),
		    	(overlay_set_position, "$g_presentation_obj_16", pos15),
		     	(overlay_set_size, "$g_presentation_obj_16", pos14),

                (create_mesh_overlay, "$g_presentation_obj_17", "mesh_3card_back", "mesh_3card_back"),#
                (position_set_x, pos16, 425),
                (position_set_y, pos16, 300),
			    (overlay_set_position, "$g_presentation_obj_17", pos16),
			    (overlay_set_size, "$g_presentation_obj_17", pos14),#

                (create_mesh_overlay, "$g_presentation_obj_15", "mesh_3card_back", "mesh_3card_back"),#
                (position_set_x, pos17, 575),
                (position_set_y, pos17, 300),
			    (overlay_set_position, "$g_presentation_obj_15", pos17),
			    (overlay_set_size, "$g_presentation_obj_15", pos14),#

			    (overlay_animate_to_position, "$g_presentation_obj_15",500, pos15),
			    (overlay_animate_to_position, "$g_presentation_obj_16",500, pos16),
                (overlay_animate_to_position, "$g_presentation_obj_17",500, pos17),

			(try_end),
			(assign,reg50, 6),
    	 (try_end),

         (store_add, reg52, 550, reg58),
         (ge, ":cur_time",reg52),

        (try_begin),
		    (eq, reg50, 6),
            (assign, reg50, 7),
            (overlay_set_display, "$g_presentation_obj_15", 0),
			(overlay_set_display, "$g_presentation_obj_16", 0),
            (overlay_set_display, "$g_presentation_obj_17", 0),
            (position_set_x, pos14, 375),#
            (position_set_y, pos14, 550),

                (create_image_button_overlay, "$g_presentation_obj_card1", "mesh_3card_back", "mesh_3card_back"),
                (position_set_x, pos1, 275),
                (position_set_y, pos1, 300),
		    	(overlay_set_position, "$g_presentation_obj_card1", pos1),
		     	(overlay_set_size, "$g_presentation_obj_card1", pos14),

                (create_image_button_overlay, "$g_presentation_obj_card2", "mesh_3card_back", "mesh_3card_back"),
                (position_set_x, pos1, 425),
                (position_set_y, pos1, 300),
			    (overlay_set_position, "$g_presentation_obj_card2", pos1),
			    (overlay_set_size, "$g_presentation_obj_card2", pos14),#

                (create_image_button_overlay, "$g_presentation_obj_card3", "mesh_3card_back", "mesh_3card_back"),
                (position_set_x, pos1, 575),
                (position_set_y, pos1, 300),
			    (overlay_set_position, "$g_presentation_obj_card3", pos1),
			    (overlay_set_size, "$g_presentation_obj_card3", pos14),#

			(assign, reg55, 2),
            (create_mesh_overlay, "$g_presentation_obj_9", "mesh_3card_window"), #"mesh_text_bar"
            (position_set_x, pos1, 375),#
            (position_set_y, pos1, 595),#
            (overlay_set_position, "$g_presentation_obj_9", pos1),
            (position_set_x, pos1, 300),#
            (position_set_y, pos1, 125),#
            (overlay_set_size, "$g_presentation_obj_9", pos1),

            (str_store_string, s1, "@Find the Lady"),
            (create_text_overlay, "$g_presentation_obj_11", "@{s1}", tf_center_justify),
            (position_set_x, pos1, 475),
            (position_set_y, pos1, 600),
            (overlay_set_position, "$g_presentation_obj_11", pos1),#Find the Lady
            (position_set_x, pos1, 2000),
            (position_set_y, pos1, 2000),
            (overlay_set_size, "$g_presentation_obj_11", pos1),
#            (overlay_set_color, "$g_presentation_obj_11", 0xffffff),#
        (try_end),

        (try_begin),
		    (eq, reg50, 8),
            (assign, reg50, 9),
            (overlay_set_display, "$g_presentation_obj_card1", 0),
			(overlay_set_display, "$g_presentation_obj_card2", 0),
            (overlay_set_display, "$g_presentation_obj_card3", 0),
		    (store_random_in_range,":lady",1,4),
			(store_random_in_range,":king",1,3),
			(store_random_in_range,":queen",1,3),
			    (try_begin),
                    (eq,":king",1),
                    (assign,":king1","mesh_3card_kos"),
                    (assign,":king2","mesh_3card_koc"),
		        (else_try),
                    (assign,":king1","mesh_3card_koc"),
                    (assign,":king2","mesh_3card_kos"),
				(try_end),

			    (try_begin),
                    (eq,":queen",1),
                    (assign,":queen1","mesh_3card_qoh"),
                    (assign,":queen2",":king2"),
		        (else_try),
                    (assign,":queen1",":king2"),
                    (assign,":queen2","mesh_3card_qoh"),
				(try_end),

                (try_begin),
				    (eq,reg55, 3),#1card
					    (try_begin),
						    (eq,":lady",1), #win
							(assign,reg55,7),#win
							(assign,":card1","mesh_3card_qoh"),
                            (assign,":card2",":king1"),
                            (assign,":card3",":king2"),
						(else_try),
      					    (assign,reg55,8),#loose
							(assign,":card1",":king1"),
                            (assign,":card2",":queen1"),
                            (assign,":card3",":queen2"),
						(try_end),
				(else_try),
				    (eq,reg55, 4),#2card
					    (try_begin),
						    (eq,":lady",1), #win
							(assign,reg55,7),#win
							(assign,":card1",":king1"),
                            (assign,":card2","mesh_3card_qoh"),
                            (assign,":card3",":king2"),
						(else_try),
						    (assign,reg55,8),#loose
                            (assign,":card1", ":queen1"),#
                            (assign,":card2", ":king1"),#
                            (assign,":card3", ":queen2"),#
						(try_end),
                (else_try),
                    (eq,reg55, 5),#3card
					    (try_begin),
						    (eq,":lady",1), #win
							(assign,reg55,7),#win
							(assign,":card1",":king1"),
                            (assign,":card2",":king2"),
                            (assign,":card3","mesh_3card_qoh"),
						(else_try),
						    (assign,reg55,8),#loose
                            (assign,":card1", ":queen1"),#
                            (assign,":card2", ":queen2"),#
                            (assign,":card3", ":king1"),#
						(try_end),
				(try_end),

                (try_begin),#open cards
				    (position_set_x, pos14, 375),#
                    (position_set_y, pos14, 550),

                    (create_mesh_overlay, reg1, ":card1"),#
                    (position_set_x, pos1, 275),
                    (position_set_y, pos1, 300),
                 	(overlay_set_position, reg1, pos1),
					(overlay_set_size, reg1, pos14),#

                    (create_mesh_overlay, reg2, ":card2"),#
                    (position_set_x, pos1, 425),
                    (position_set_y, pos1, 300),
		            (overlay_set_position, reg2, pos1),
                    (overlay_set_size, reg2, pos14),#

                    (create_mesh_overlay, reg3, ":card3"),#
                    (position_set_x, pos1, 575),
                    (position_set_y, pos1, 300),
	                (overlay_set_position, reg3, pos1),
	                (overlay_set_size, reg3, pos14),#
				(try_end),

                (str_clear,s1),
			    (try_begin),
                    (eq,reg55,7),#
                    (val_mul,reg51,2),
					(call_script, "script_troop_add_gold", "trp_player", reg51),
                    (str_store_string, s1, "@You win! Try again?"),
                (else_try),
                    (str_store_string, s1, "@You lose. Try again?"),
                (try_end),
                (create_text_overlay, reg1, "@{s1}", tf_center_justify),
                (position_set_x, pos1, 480),
                (position_set_y, pos1, 650),
                (overlay_set_position, reg1, pos1),#
                (position_set_x, pos1, 2000),
                (position_set_y, pos1, 2000),
                (overlay_set_size, reg1, pos1),#
#                (overlay_set_color, reg1, 0xffffff),#0xffffff #white

                (create_mesh_overlay, reg1, "mesh_3card_window"),#3card_textbar#text_bar
                (position_set_x, pos1, 306),#700
                (position_set_y, pos1, 580),#270
                (overlay_set_position, reg1, pos1),
                (position_set_x, pos1, 500),#
                (position_set_y, pos1, 300),#
                (overlay_set_size, reg1, pos1),

                (create_game_button_overlay, "$g_presentation_obj_12", "@Yes", tf_center_justify),
                (position_set_x, pos1, 400),#450
                (position_set_y, pos1, 600),
                (overlay_set_position, "$g_presentation_obj_12", pos1),

                (create_game_button_overlay, "$g_presentation_obj_13", "@No", tf_center_justify),
                (position_set_x, pos1, 560),#500
                (position_set_y, pos1, 600),
                (overlay_set_position, "$g_presentation_obj_13", pos1),
        (try_end),
        ]),

      (ti_on_presentation_event_state_change,#
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        (position_set_x, pos13, 1400),
        (position_set_y, pos13, 1400),
        (try_begin),
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
			(overlay_set_display, "$g_presentation_obj_7", 0),
            (overlay_set_display, "$g_presentation_obj_8", 0),
            (overlay_set_display, "$g_presentation_obj_10", 0),

            (store_troop_gold,reg1,"trp_player"),#
            (str_store_string, s1, "@Bet: {reg51} Denar(s)"),#
            (overlay_set_text, "$g_presentation_obj_4", s1),
            (str_store_string, s1, "@Money: {reg1} Denar(s)"),#
            (overlay_set_text, "$g_presentation_obj_5", s1),
            (assign, reg50, 2),#4
          (try_end),
		(try_end),
        (try_begin),
            (eq, ":object", "$g_presentation_obj_14"),#start game button
		    (assign, reg50, 4),#6
		(try_end),

        (try_begin),
	    	(eq, reg50, 7),
		    (eq, reg55, 2),
		        (try_begin),
                    (eq, ":object", "$g_presentation_obj_card1"),
					(assign, reg55, 3),
				(else_try),
	                (eq, ":object", "$g_presentation_obj_card2"),
                    (assign, reg55, 4),
				(else_try),
			        (eq, ":object", "$g_presentation_obj_card3"),
					(assign, reg55, 5),
				(try_end),
            (overlay_set_display, "$g_presentation_obj_11", 0),	#Find the Lady
			(overlay_set_display, "$g_presentation_obj_9", 0),
		    (assign, reg50, 8),
		(try_end),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_12"),#yes
          (store_troop_gold,reg1,"trp_player"),#
          (try_begin),
            (lt,reg1,1),#
            (display_message, "@You don't have enough money."),
          (else_try),
            (presentation_set_duration, 0),
            (assign, reg50,0),
            (start_presentation, "prsnt_three_card"),
          (try_end),
        (else_try),
          (eq, ":object", "$g_presentation_obj_13"),#no
          (assign,reg1,0),#
          (assign, reg51, 1),
          (assign, reg55, 0),#
          (presentation_set_duration, 0),
        (try_end),
        ]),
     ])
