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

blackjack = ("blackjack", 0, 0,#
   [
     (ti_on_presentation_load,
      [

        (set_fixed_point_multiplier, 1000),
        (assign,"$g_presentation_obj_1",-1), #
        (assign,"$g_presentation_obj_2",-1), #
        (assign,"$g_presentation_obj_3",-1), #
        (assign,"$g_presentation_obj_4",-1), #
        (assign,"$g_presentation_obj_5",-1), #
        (assign,"$g_presentation_obj_6",-1), #
        (assign,"$g_presentation_obj_7",-1), #
        (assign,"$g_presentation_obj_8",-1), #
        (assign,"$g_presentation_obj_9",-1), #
        (assign,"$g_presentation_obj_10",-1), #
        (assign,"$g_presentation_obj_11",-1), #
        (assign,"$g_presentation_obj_12",-1), #
        (assign,"$g_presentation_credits_obj_1",-1), #
        (assign,"$g_presentation_credits_obj_2",-1), #
        (assign,"$g_presentation_credits_obj_3",-1), #
        (assign,"$g_presentation_credits_obj_4",-1), #
        (assign,"$g_presentation_credits_obj_5",-1), #
        (assign,reg1,0),#
        (assign,reg21,0),#
        (assign,reg22,0),
        (assign,reg23,0),
        (assign,reg24,0),
        (assign,reg25,0),
        (assign,reg26,0),
        (assign,reg27,0),
        (assign,reg28,0),
        (assign,reg29,0),
        (assign,reg30,0),
        (assign,reg31,0),
        (assign,reg32,0),
        (assign,reg33,0),
        (assign,reg34,0),
        (assign,reg35,0),
        (assign,reg36,0),
        (assign,reg37,0),
        (assign,reg38,0),
        (assign,reg39,0),
        (assign, reg51, 1),#
        (assign, reg52, 0),#
        (assign, reg53, 0),#
        (assign, reg54, 0),#
        (assign, reg55, 0),#
        (assign, reg56, 0),#
        (assign, reg57, 0),#
        (assign, reg58, 0),#
        (assign, reg60, 0),#
        (assign, reg61, 0),#
        (assign, reg62, 0),#
        (assign, reg63, 0),#

        (create_mesh_overlay, reg1, "mesh_wood_table"),#
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),

        (str_store_troop_name, s1, "$g_talk_troop"),#
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
         # "mesh_21_troop_portrait"
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "$g_talk_troop"),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 7),#700
        (position_set_y, pos1, 500),#500
        (overlay_set_position, reg1, pos1),
         # "mesh_21_troop_portrait"
        (create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "trp_player"),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 750),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 740),#7
        (position_set_y, pos1, 45),#20
        (overlay_set_position, reg1, pos1),


         #$g_presentation_obj_1
        (create_image_button_overlay, "$g_presentation_obj_1", "mesh_21_button", "mesh_21_button_down"),
        (position_set_x, pos1, 650),#250
        (position_set_y, pos1, 160),#160
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 450),
        (overlay_set_size, "$g_presentation_obj_1", pos1),
        (create_text_overlay, reg1, "@Hit"),#
        (position_set_x, pos1, 660),#260
        (position_set_y, pos1, 160),#160
        (overlay_set_position, reg1, pos1),
        (overlay_set_color, reg1, 0xffffff),
         #$g_presentation_obj_2
        (create_image_button_overlay, "$g_presentation_obj_2", "mesh_21_button", "mesh_21_button_down"),
        (position_set_x, pos1, 650),#250
        (position_set_y, pos1, 100),#100
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 450),
        (overlay_set_size, "$g_presentation_obj_2", pos1),
        (create_text_overlay, reg1, "@Stay"),#
        (position_set_x, pos1, 660),#260
        (position_set_y, pos1, 100),#100
        (overlay_set_position, reg1, pos1),
        (overlay_set_color, reg1, 0xffffff),
         #$g_presentation_obj_3
        (create_image_button_overlay, "$g_presentation_obj_3", "mesh_21_button", "mesh_21_button_down"),
        (position_set_x, pos1, 650),#250
        (position_set_y, pos1, 40),#40
        (overlay_set_position, "$g_presentation_obj_3", pos1),
        (position_set_x, pos1, 300),
        (position_set_y, pos1, 450),
        (overlay_set_size, "$g_presentation_obj_3", pos1),
        (create_text_overlay, reg1, "@Double"),#
        (position_set_x, pos1, 660),#260
        (position_set_y, pos1, 40),#40
        (overlay_set_position, reg1, pos1),
        (overlay_set_color, reg1, 0xffffff),

        (create_mesh_overlay, reg1, "mesh_text_bar"),#
        (position_set_x, pos1, 240),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 740),
        (position_set_y, pos1, 305),
        (overlay_set_position, reg1, pos1),

        (str_store_string, s1, "@Bet: {reg51} Denar(s)"),#
        (create_text_overlay, "$g_presentation_obj_4", s1),#
        (position_set_x, pos1, 755),#30
        (position_set_y, pos1, 355),#300
        (overlay_set_position, "$g_presentation_obj_4", pos1),
        (overlay_set_color, "$g_presentation_obj_4", 0xfffccc),
        (store_troop_gold,reg1,"trp_player"),#
        (create_text_overlay, "$g_presentation_obj_5", "@Money: {reg1} Denar(s)"),
        (position_set_x, pos1, 755),#30
        (position_set_y, pos1, 325),#270
        (overlay_set_position, "$g_presentation_obj_5", pos1),
        (overlay_set_color, "$g_presentation_obj_5", 0xfffccc),

        (presentation_set_duration, 999999),
        ]),
      (ti_on_presentation_run,#
       [
        (store_trigger_param_1, ":cur_time"),
        (set_fixed_point_multiplier, 1000),

        (ge, ":cur_time",500),
        #ce shi
        #(try_begin),
        #        (key_clicked, key_t),
        #        (display_message, "@reg52={reg52}"),
        #        (display_message, "@reg53={reg53}"),
        #        (display_message, "@reg54={reg54}"),
        #        (display_message, "@reg55={reg55}"),
        #(try_end),
        #ce shi

        (try_begin),
          (eq, reg50, 0),#
          (assign, reg50, 3),#
          (create_mesh_overlay, "$g_presentation_obj_6", "mesh_text_bar"),#
          (position_set_x, pos1, 350),
          (position_set_y, pos1, 1800),
          (overlay_set_size, "$g_presentation_obj_6", pos1),
          (position_set_x, pos6, 330),
          (position_set_y, pos6, 250),
          (create_slider_overlay, "$g_presentation_obj_7", 1, 50),#
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (position_set_x, pos7, 510),
          (position_set_y, pos7, 360),
          (create_text_overlay, "$g_presentation_obj_8", "@Bet: {reg51} Denar(s)"),#
          (position_set_x, pos8, 420),
          (position_set_y, pos8, 400),
          (create_mesh_overlay, "$g_presentation_obj_9", "mesh_button_used"),#
          (position_set_x, pos1, 350),
          (position_set_y, pos1, 500),
          (overlay_set_size, "$g_presentation_obj_9", pos1),
          (position_set_x, pos9, 453),
          (position_set_y, pos9, 284),
          (create_button_overlay, "$g_presentation_obj_10", "@Done", tf_center_justify),#
          (position_set_x, pos1, 1400),
          (position_set_y, pos1, 1400),
          (overlay_set_size, "$g_presentation_obj_10", pos1),
          (position_set_x, pos10, 500),
          (position_set_y, pos10, 284),
          (overlay_set_position, "$g_presentation_obj_6", pos6),
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (overlay_set_position, "$g_presentation_obj_7", pos7),
          (overlay_set_position, "$g_presentation_obj_8", pos8),
          (overlay_set_position, "$g_presentation_obj_9", pos9),
          (overlay_set_position, "$g_presentation_obj_10", pos10),
        (try_end),#

        (try_begin),#
          (eq, reg50, 4),#
          (play_sound, "snd_dealing_cards"),
          (assign, reg50, 5),
          (assign, reg58,":cur_time"),
          (position_set_x, pos13, 320),#
          (position_set_y, pos13, 265),
          (position_set_x, pos14, 450),#
          (position_set_y, pos14, 400),
          (assign, reg63, 0),#
        (try_end),
        (try_begin),
          (eq, reg50, 5),
          (lt, reg63, 30),#
          (store_sub, ":time_p",":cur_time",reg58),
          (ge, ":time_p",20),
          (assign, reg58,":cur_time"),
          (position_get_x, ":x_13",pos13),
          (val_add, ":x_13",3),
          (position_set_x, pos13, ":x_13"),
          (create_mesh_overlay, reg1, "mesh_poker_back"),#
          (overlay_set_position, reg1, pos13),
          (overlay_set_size, reg1, pos14),#
          (val_add, reg63,1),
        (else_try),
          (eq, reg63, 30),
          (assign, reg63, 0),
          (assign, reg50, 1),#
          (assign, reg58,":cur_time"),
        (try_end),

        (eq, reg50, 1),#
        (store_sub, ":time_p",":cur_time",reg58),
        (ge, ":time_p",700),#

        (try_begin),
          (eq, reg21, 0),#
          (assign,":reang_low","mesh_poker_heart_a"),
          (assign,":reang_high","mesh_poker_red_joker"),
           #
          (store_random_in_range,":rp",":reang_low",":reang_high"),
          (assign,reg21,":rp"),#
          (store_sub,":banker_points",":rp",":reang_low"),
          (val_add,":banker_points",1),
          (try_begin),
            (le,":banker_points",13),
          (else_try),
            (val_mod,":banker_points",13),
            (try_begin),
              (eq,":banker_points",0),
              (assign,":banker_points",13),
            (try_end),
          (try_end),
          (val_min,":banker_points",10),#
          (val_add, reg52, ":banker_points"),#
          (val_add, reg53, ":banker_points"),#
          (try_begin),
            #(this_or_next|eq,reg21,"mesh_poker_heart_a"),
            #(this_or_next|eq,reg21,"mesh_poker_spade_a"),
            #(this_or_next|eq,reg21,"mesh_poker_diamond_a"),
            #(eq,reg21,"mesh_poker_club_a"),
            (this_or_next|eq,reg21,407),
            (this_or_next|eq,reg21,420),
            (this_or_next|eq,reg21,433),
            (eq,reg21,446),
            (val_add, reg53, 10),#
          (try_end),
          (create_mesh_overlay, "$g_presentation_credits_obj_1", "mesh_poker_back"),#
          (overlay_set_position, "$g_presentation_credits_obj_1", pos13),#
          (overlay_set_size, "$g_presentation_credits_obj_1", pos14),#
          (position_set_x, pos11, 350),#
          (position_set_y, pos11, 500),
          (copy_position,pos60,pos11),#
          (overlay_animate_to_position, "$g_presentation_credits_obj_1",300, pos11),#
          #
          (try_for_range, ":unused", 0, 200),
            (eq,reg22,0),#
            (store_random_in_range,":rp",":reang_low",":reang_high"),
            (neq,":rp",reg21),#
            (assign,reg22,":rp"),#
          (try_end),
          (store_sub,":banker_points",":rp",":reang_low"),
          (val_add,":banker_points",1),
          (try_begin),
            (le,":banker_points",13),
          (else_try),
            (val_mod,":banker_points",13),
            (try_begin),
              (eq,":banker_points",0),
              (assign,":banker_points",13),
            (try_end),
          (try_end),
          (val_min,":banker_points",10),#
          (val_add, reg52, ":banker_points"),#
          (val_add, reg53, ":banker_points"),#
          (try_begin),
            (eq, reg53, reg52),#
            #(this_or_next|eq,reg22,"mesh_poker_heart_a"),
            #(this_or_next|eq,reg22,"mesh_poker_spade_a"),
            #(this_or_next|eq,reg22,"mesh_poker_diamond_a"),
            #(eq,reg22,"mesh_poker_club_a"),
            (this_or_next|eq,reg22,407),
            (this_or_next|eq,reg22,420),
            (this_or_next|eq,reg22,433),
            (eq,reg22,446),
            (val_add, reg53, 10),#
          (try_end),
          (create_mesh_overlay, "$g_presentation_credits_obj_2", reg22),#
          (overlay_set_position, "$g_presentation_credits_obj_2", pos13),#
          (overlay_set_size, "$g_presentation_credits_obj_2", pos14),#
          (position_get_x,":x_p",pos11),
          (val_add,":x_p",150),#
          (position_set_x, pos11, ":x_p"),
          #(position_move_x, pos11, 150),#
          (overlay_animate_to_position, "$g_presentation_credits_obj_2",300, pos11),#

           #
          (try_for_range, ":unused", 0, 200),
            (eq,reg23,0),#
            (store_random_in_range,":rp",":reang_low",":reang_high"),
            (neq,":rp",reg21),#
            (neq,":rp",reg22),#
            (assign,reg23,":rp"),#
          (try_end),
          (store_sub,":player_points",":rp",":reang_low"),
          (val_add,":player_points",1),
          (try_begin),
            (le,":player_points",13),
          (else_try),
            (val_mod,":player_points",13),
            (try_begin),
              (eq,":player_points",0),
              (assign,":player_points",13),
            (try_end),
          (try_end),
          (val_min,":player_points",10),#
          (val_add, reg54, ":player_points"),#
          (val_add, reg55, ":player_points"),#
          (try_begin),
            #(this_or_next|eq,reg23,"mesh_poker_heart_a"),
            #(this_or_next|eq,reg23,"mesh_poker_spade_a"),
            #(this_or_next|eq,reg23,"mesh_poker_diamond_a"),
            #(eq,reg23,"mesh_poker_club_a"),
            (this_or_next|eq,reg23,407),
            (this_or_next|eq,reg23,420),
            (this_or_next|eq,reg23,433),
            (eq,reg23,446),
            (val_add, reg55, 10),#
          (try_end),
          (create_mesh_overlay, "$g_presentation_credits_obj_3", reg23),#
          (overlay_set_position, "$g_presentation_credits_obj_3", pos13),#
          (overlay_set_size, "$g_presentation_credits_obj_3", pos14),#
          (position_set_x, pos12, 200),#
          (position_set_y, pos12, 30),
          (overlay_animate_to_position, "$g_presentation_credits_obj_3",300, pos12),#
          #
          (try_for_range, ":unused", 0, 200),
            (eq,reg24,0),#
            (store_random_in_range,":rp",":reang_low",":reang_high"),
            (neq,":rp",reg21),#
            (neq,":rp",reg22),#
            (neq,":rp",reg23),#
            (assign,reg24,":rp"),#
          (try_end),
          (store_sub,":player_points",":rp",":reang_low"),
          (val_add,":player_points",1),
          (try_begin),
            (le,":player_points",13),
          (else_try),
            (val_mod,":player_points",13),
            (try_begin),
              (eq,":player_points",0),
              (assign,":player_points",13),
            (try_end),
          (try_end),
          (val_min,":player_points",10),#
          (val_add, reg54, ":player_points"),#
          (val_add, reg55, ":player_points"),#
          (try_begin),
            (eq, reg55, reg54),#
            #(this_or_next|eq,reg24,"mesh_poker_heart_a"),
            #(this_or_next|eq,reg24,"mesh_poker_spade_a"),
            #(this_or_next|eq,reg24,"mesh_poker_diamond_a"),
            #(eq,reg24,"mesh_poker_club_a"),
            (this_or_next|eq,reg24,407),
            (this_or_next|eq,reg24,420),
            (this_or_next|eq,reg24,433),
            (eq,reg24,446),
            (val_add, reg55, 10),#
          (try_end),
          (create_mesh_overlay, "$g_presentation_credits_obj_4", reg24),#
          (overlay_set_position, "$g_presentation_credits_obj_4", pos13),#
          (overlay_set_size, "$g_presentation_credits_obj_4", pos14),#
          (position_get_x,":x_p",pos12),
          (val_add,":x_p",60),
          (position_set_x, pos12, ":x_p"),
          #(position_move_x, pos12, 100),#
          (overlay_animate_to_position, "$g_presentation_credits_obj_4",300, pos12),#

          (assign, reg58, ":cur_time"),
        (try_end),

        (gt,reg24,0),#
        (store_sub, ":time1",":cur_time",reg58),
        (ge, ":time1",1200),#

        (try_begin),
          (eq,reg25,0),#
          (eq,reg56,0),#
          (try_begin),
            (eq,reg53,21),#
            (eq,reg55,21),#
            (play_sound, "snd_get_coins"),
            (display_message, "@Draw, your bet will be returned to you."),
            (call_script, "script_troop_add_gold", "trp_player", reg51),
            (play_sound, "snd_get_coins"),
            (assign,reg56,3),
          (else_try),
            (eq,reg53,21),#
            (val_div, reg51, 2),
            (troop_remove_gold, "trp_player", reg51),
            (play_sound, "snd_money_paid"),
            (display_message, "@The banker has a Blackjack! You lose 50% more of your bets!"),
            (play_sound, "snd_get_coins"),
            (assign,reg56,1),
          (else_try),
            (eq,reg55,21),#
            (val_mul, reg51, 5),
            (val_div, reg51, 2),
            (call_script, "script_troop_add_gold", "trp_player", reg51),
            (display_message, "@You have a Blackjack! You win 50% more of your bets!"),
            (play_sound, "snd_get_coins"),
            (assign,reg56,2),
          (try_end),

          (neq,reg56,0),#
          (try_begin),
            (eq,reg61,0),#
            (assign,reg61,1),
            (create_mesh_overlay, reg1, reg21),#
            (overlay_set_position, reg1, pos60),
            (overlay_set_size, reg1, pos14),
          (try_end),
          (store_troop_gold,reg1,"trp_player"),
          (str_store_string, s1, "@Bet: 0 Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_4", s1),
          (str_store_string, s1, "@Money: {reg1} Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_5", s1),
          (assign,reg58,":cur_time"),#
        (try_end),

        (try_begin),
          (gt,reg24,0),#
          (eq,reg56,0),#

          (ge, reg57, 1),#

          (try_begin),
            (gt,reg52,21),#
            (val_mul,reg51,2),
            (display_message, "@The bankers hand value is over 21. You win!"),
            (call_script, "script_troop_add_gold", "trp_player", reg51),
            (play_sound, "snd_get_coins"),
            (assign,reg56,2),
          (else_try),
            (gt,reg54,21),#
            (display_message, "@Your hand value is over 21. You lose!"),
            (play_sound, "snd_get_coins"),
            (assign,reg56,1),
          (else_try),
            (eq,reg60,1),#
            (eq,reg61,1),#
            (try_begin),
              (assign,":win",0),#
              (try_begin),
                (le,reg53,21),#
                (gt,reg53,reg55),#
                (assign,":win",1),
              (else_try),
                (gt,reg52,reg55),#
                (assign,":win",1),
              (try_end),
              (eq,":win",1),#
              (assign,reg56,1),#
              (display_message, "@The banker has a higher hand value. You lose!"),
              (play_sound, "snd_get_coins"),
              (overlay_set_text, "$g_presentation_obj_4", "@Bet: 0 Denar(s)"),
            (else_try),
              (assign,":win",0),#
              (try_begin),
                (le,reg55,21),#
                (gt,reg55,reg53),#
                (assign,":win",1),
              (else_try),
                (gt,reg54,reg53),#
                (assign,":win",1),
              (try_end),
              (eq,":win",1),#
              (assign,reg56,2),#
              (display_message, "@You have a higher hand value. You win!"),
              (val_mul, reg51, 2),
              (call_script, "script_troop_add_gold", "trp_player", reg51),
            (play_sound, "snd_get_coins"),
            (else_try),
              (display_message, "@Draw, the bets be returned to you."),
              (call_script, "script_troop_add_gold", "trp_player", reg51),
              (play_sound, "snd_get_coins"),
              (assign,reg56,3),#
            (try_end),
          (try_end),
          (neq,reg56,0),#
          (try_begin),
            (eq,reg61,0),#
            (assign,reg61,1),
            (create_mesh_overlay, reg1, reg21),#
            (overlay_set_position, reg1, pos60),
            (overlay_set_size, reg1, pos14),
          (try_end),
          (store_troop_gold,reg1,"trp_player"),
          (str_store_string, s1, "@Bet: 0 Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_4", s1),
          (str_store_string, s1, "@Money: {reg1} Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_5", s1),
          (assign,reg58,":cur_time"),#
        (try_end),

        (try_begin),
          (neq,reg56,0),#
          (store_sub,":time",":cur_time",reg58),
          (ge,":time",800),#
          (assign,reg50,2),#

          (try_begin),
            (eq,reg56,1),
            (play_sound, "snd_get_coins"),
            (str_store_string, s1, "@You lose. Try again?"),
          (else_try),
            (eq,reg56,2),
            (play_sound, "snd_get_coins"),
            (str_store_string, s1, "@You win! Try again?"),
          (else_try),
            (eq,reg56,3),
            (play_sound, "snd_get_coins"),
            (str_store_string, s1, "@Draw. Try again?"),
          (try_end),
          (create_text_overlay, reg1, "@{s1}", tf_center_justify),
          (position_set_x, pos1, 480),
          (position_set_y, pos1, 480),
          (overlay_set_position, reg1, pos1),#
          (position_set_x, pos1, 2000),
          (position_set_y, pos1, 2000),
          (overlay_set_size, reg1, pos1),#
          (overlay_set_color, reg1, 0xffffff),

          (create_button_overlay, "$g_presentation_obj_11", "@Yes", tf_center_justify),
          (position_set_x, pos1, 450),
          (position_set_y, pos1, 370),
          (overlay_set_position, "$g_presentation_obj_11", pos1),
          (position_set_x, pos1, 1500),
          (position_set_y, pos1, 1500),
          (overlay_set_size, "$g_presentation_obj_11", pos1),
          (overlay_set_color, "$g_presentation_obj_11", 0xffffff),
          (create_button_overlay, "$g_presentation_obj_12", "@NO", tf_center_justify),
          (position_set_x, pos1, 500),
          (position_set_y, pos1, 370),
          (overlay_set_position, "$g_presentation_obj_12", pos1),
          (position_set_x, pos1, 1500),
          (position_set_y, pos1, 1500),
          (overlay_set_size, "$g_presentation_obj_12", pos1),
          (overlay_set_color, "$g_presentation_obj_12", 0xffffff),
        (try_end),

        (try_begin),
          (eq, reg56, 0),
          (eq, reg57, 0),
          (assign, reg57, 1),
        (try_end),

         #AI
        (try_begin),
          (eq, reg56, 0),
          (eq,reg60,0),
          (this_or_next|eq, reg61, 1),
          (eq, reg57, 2),
          (neq, reg57, 3),
          (assign, reg57, 3),
          (assign,reg58,":cur_time"),
        (try_end),
        (try_begin),
          (eq, reg56, 0),
          (eq,reg60,0),
          (eq, reg57, 3),
          (store_sub,":time",":cur_time",reg58),
          (ge,":time",700),
          (try_begin),
            (gt, reg52, 16),
            (le, reg52, 21),
            (assign,reg60,1),
            (display_message, "@Banker stay."),
            (create_text_overlay, reg1, "@Stay"),
            (position_set_x, pos1, 255),
            (position_set_y, pos1, 650),
            (overlay_set_position, reg1, pos1),
            (position_set_x, pos1, 1600),
            (position_set_y, pos1, 1600),
            (overlay_set_size, reg1, pos1),
            (overlay_set_color, reg1, 0x11dd11),
          (else_try),
            (le, reg52, 16),
            (assign, ":banker_hit", 0),
            (try_begin),
              (le, reg53, 16),
              (play_sound, "snd_card_flip"),
              (assign, ":banker_hit", 1),
            (else_try),
              (gt, reg53, 16),
              (store_sub,":oo", reg53, 16),
              (val_mul,":oo", 30),
              (store_random_in_range,":rp",0,100),
              (try_begin),
                (gt,":rp",":oo"),
                (play_sound, "snd_card_flip"),
                (assign, ":banker_hit", 1),
              (else_try),
                (assign,reg60,1),
                (display_message, "@Banker stay."),
                (create_text_overlay, reg1, "@Stay"),
                (position_set_x, pos1, 255),
                (position_set_y, pos1, 650),
                (overlay_set_position, reg1, pos1),
                (position_set_x, pos1, 1400),
                (position_set_y, pos1, 1400),
                (overlay_set_size, reg1, pos1),
                (overlay_set_color, reg1, 0x11dd11),
              (try_end),
            (try_end),
            (eq, ":banker_hit", 1),

            (assign,":reang_low","mesh_poker_heart_a"),
            (assign,":reang_high","mesh_poker_red_joker"),
            (assign,":cur_card",0),
            (try_for_range, ":unused", 0, 300),
              (eq,":cur_card",0),
              (store_random_in_range,":rp",":reang_low",":reang_high"),
              (neq,":rp",reg21),
              (neq,":rp",reg22),
              (neq,":rp",reg23),
              (neq,":rp",reg24),
              (neq,":rp",reg25),
              (neq,":rp",reg26),
              (neq,":rp",reg27),
              (neq,":rp",reg28),
              (neq,":rp",reg29),
              (neq,":rp",reg30),
              (neq,":rp",reg31),
              (neq,":rp",reg32),
              (neq,":rp",reg33),
              (neq,":rp",reg34),
              (neq,":rp",reg35),
              (neq,":rp",reg36),
              (neq,":rp",reg37),
              (neq,":rp",reg38),
              (neq,":rp",reg39),
              (assign,":cur_card",":rp"),
            (try_end),
            (try_begin),
              (eq,reg25,0),
              (assign,reg25,":cur_card"),
            (else_try),
              (eq,reg26,0),
              (assign,reg26,":cur_card"),
            (else_try),
              (eq,reg27,0),
              (assign,reg27,":cur_card"),
            (else_try),
              (eq,reg28,0),
              (assign,reg28,":cur_card"),
            (else_try),
              (eq,reg29,0),
              (assign,reg29,":cur_card"),
            (else_try),
              (eq,reg30,0),
              (assign,reg30,":cur_card"),
            (else_try),
              (eq,reg31,0),
              (assign,reg31,":cur_card"),
            (else_try),
              (eq,reg32,0),
              (assign,reg32,":cur_card"),
            (else_try),
              (eq,reg33,0),
              (assign,reg33,":cur_card"),
            (else_try),
              (eq,reg34,0),
              (assign,reg34,":cur_card"),
            (else_try),
              (eq,reg35,0),
              (assign,reg35,":cur_card"),
            (else_try),
              (eq,reg36,0),
              (assign,reg36,":cur_card"),
            (else_try),
              (eq,reg37,0),
              (assign,reg37,":cur_card"),
            (else_try),
              (eq,reg38,0),
              (assign,reg38,":cur_card"),
            (else_try),
              (eq,reg39,0),
              (assign,reg39,":cur_card"),
            (try_end),
            (store_sub,":banker_points",":cur_card",":reang_low"),
            (val_add,":banker_points",1),
            (try_begin),
              (le,":banker_points",13),
            (else_try),
              (val_mod,":banker_points",13),
              (try_begin),
                (eq,":banker_points",0),
                (assign,":banker_points",13),
              (try_end),
            (try_end),
            (val_min,":banker_points",10),
            (val_add, reg52, ":banker_points"),
            (val_add, reg53, ":banker_points"),
            (try_begin),
              (eq, reg53, reg52),
              #(this_or_next|eq,":cur_card","mesh_poker_heart_a"),
              #(this_or_next|eq,":cur_card","mesh_poker_spade_a"),
              #(this_or_next|eq,":cur_card","mesh_poker_diamond_a"),
              #(eq,":cur_card","mesh_poker_club_a"),
              (this_or_next|eq,":cur_card",407),
              (this_or_next|eq,":cur_card",420),
              (this_or_next|eq,":cur_card",433),
              (eq,":cur_card",446),
              (val_add, reg53, 10),
            (try_end),
            (create_mesh_overlay, "$g_presentation_credits_obj_5", ":cur_card"),
            (overlay_set_position, "$g_presentation_credits_obj_5", pos13),
            (overlay_set_size, "$g_presentation_credits_obj_5", pos14),
            (position_get_x,":x_p",pos11),
            (val_add,":x_p",60),
            (position_set_x, pos11, ":x_p"),
            #(position_move_x, pos11, 60),
            (overlay_animate_to_position, "$g_presentation_credits_obj_5",300, pos11),
          (try_end),
          (assign, reg57, 1),
          (assign,reg58,":cur_time"),
        (try_end),
        ]),

      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_7"),
          (try_begin),
            (neq, reg51, ":value"),
            (assign, reg51, ":value"),
          (try_end),
          (overlay_set_val, "$g_presentation_obj_7", reg51),
          (str_store_string, s1, "@Bet: {reg51} Denar(s)"),
          (overlay_set_text, "$g_presentation_obj_8", s1),
        (else_try),
          (eq, ":object", "$g_presentation_obj_10"),
          (store_troop_gold,reg1,"trp_player"),
          (try_begin),
            (lt,reg1,reg51),
            (display_message, "@You don't have enough money."),
          (else_try),
            (troop_remove_gold, "trp_player", reg51),
            (play_sound, "snd_money_paid"),
            (position_set_x, pos1, 1400),
            (position_set_y, pos1, 1400),
            (overlay_set_position, "$g_presentation_obj_6", pos1),
            (overlay_set_position, "$g_presentation_obj_7", pos1),
            (overlay_set_position, "$g_presentation_obj_8", pos1),
            (overlay_set_position, "$g_presentation_obj_9", pos1),
            (overlay_set_position, "$g_presentation_obj_10", pos1),
            (store_troop_gold,reg1,"trp_player"),
            (str_store_string, s1, "@Bet: {reg51} Denar(s)"),
            (overlay_set_text, "$g_presentation_obj_4", s1),
            (str_store_string, s1, "@Money: {reg1} Denar(s)"),
            (overlay_set_text, "$g_presentation_obj_5", s1),
            (assign, reg50, 4),
          (try_end),
        (else_try),
          (eq, ":object", "$g_presentation_obj_11"),
          (store_troop_gold,reg1,"trp_player"),
          (try_begin),
            (lt,reg1,1),
            (display_message, "@You don't have enough money."),
          (else_try),
            (presentation_set_duration, 0),
            (assign, reg50,0),
            (start_presentation, "prsnt_blackjack"),
          (try_end),
        (else_try),
          (eq, ":object", "$g_presentation_obj_12"),
          (assign, "$black_jack",0),
          (assign,reg1,0),
          (assign,reg21,0),
          (assign,reg22,0),
          (assign,reg23,0),
          (assign,reg24,0),
          (assign,reg25,0),
          (assign,reg26,0),
          (assign,reg27,0),
          (assign,reg28,0),
          (assign,reg29,0),
          (assign,reg30,0),
          (assign,reg31,0),
          (assign,reg32,0),
          (assign,reg33,0),
          (assign,reg34,0),
          (assign,reg35,0),
          (assign,reg36,0),
          (assign,reg37,0),
          (assign,reg38,0),
          (assign,reg39,0),
          (assign, reg51, 0),
          (assign, reg50, 0),
          (assign, reg52, 0),
          (assign, reg53, 0),
          (assign, reg54, 0),
          (assign, reg55, 0),
          (assign, reg56, 0),
          (assign, reg57, 0),
          (assign, reg58, 0),
          (assign, reg60, 0),
          (assign, reg61, 0),
          (assign, reg62, 0),
          (assign, reg63, 0),
          (presentation_set_duration, 0),
        (try_end),

        (eq, reg56, 0),
        (eq, reg57, 1),
        (eq, reg61, 0),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (assign,":reang_low","mesh_poker_heart_a"),
          (assign,":reang_high","mesh_poker_red_joker"),
          (assign,":cur_card",0),
          (try_for_range, ":unused", 0, 300),
            (eq,":cur_card",0),
            (store_random_in_range,":rp",":reang_low",":reang_high"),
            (neq,":rp",reg21),
            (neq,":rp",reg22),
            (neq,":rp",reg23),
            (neq,":rp",reg24),
            (neq,":rp",reg25),
            (neq,":rp",reg26),
            (neq,":rp",reg27),
            (neq,":rp",reg28),
            (neq,":rp",reg29),
            (neq,":rp",reg30),
            (neq,":rp",reg31),
            (neq,":rp",reg32),
            (neq,":rp",reg33),
            (neq,":rp",reg34),
            (neq,":rp",reg35),
            (neq,":rp",reg36),
            (neq,":rp",reg37),
            (neq,":rp",reg38),
            (neq,":rp",reg39),
            (assign,":cur_card",":rp"),
          (try_end),

          (try_begin),
            (eq,reg25,0),
            (assign,reg25,":cur_card"),
          (else_try),
            (eq,reg26,0),
            (assign,reg26,":cur_card"),
          (else_try),
            (eq,reg27,0),
            (assign,reg27,":cur_card"),
          (else_try),
            (eq,reg28,0),
            (assign,reg28,":cur_card"),
          (else_try),
            (eq,reg29,0),
            (assign,reg29,":cur_card"),
          (else_try),
            (eq,reg30,0),
            (assign,reg30,":cur_card"),
          (else_try),
            (eq,reg31,0),
            (assign,reg31,":cur_card"),
          (else_try),
            (eq,reg32,0),
            (assign,reg32,":cur_card"),
          (else_try),
            (eq,reg33,0),
            (assign,reg33,":cur_card"),
          (else_try),
            (eq,reg34,0),
            (assign,reg34,":cur_card"),
          (else_try),
            (eq,reg35,0),
            (assign,reg35,":cur_card"),
          (else_try),
            (eq,reg36,0),
            (assign,reg36,":cur_card"),
          (else_try),
            (eq,reg37,0),
            (assign,reg37,":cur_card"),
          (else_try),
            (eq,reg38,0),
            (assign,reg38,":cur_card"),
          (else_try),
            (eq,reg39,0),
            (assign,reg39,":cur_card"),
          (try_end),

          (store_sub,":player_points",":cur_card",":reang_low"),
          (val_add,":player_points",1),
          (try_begin),
            (le,":player_points",13),
          (else_try),
            (val_mod,":player_points",13),
            (try_begin),
              (eq,":player_points",0),
              (assign,":player_points",13),
            (try_end),
          (try_end),
          (val_min,":player_points",10),
          (val_add, reg54, ":player_points"),
          (val_add, reg55,":player_points"),
          (try_begin),
            (eq, reg55, reg54),
            #(this_or_next|eq,":cur_card","mesh_poker_heart_a"),
            #(this_or_next|eq,":cur_card","mesh_poker_spade_a"),
            #(this_or_next|eq,":cur_card","mesh_poker_diamond_a"),
            #(eq,":cur_card","mesh_poker_club_a"),
            (this_or_next|eq,":cur_card",407),
            (this_or_next|eq,":cur_card",420),
            (this_or_next|eq,":cur_card",433),
            (eq,":cur_card",446),
            (val_add, reg55, 10),
          (try_end),
          (create_mesh_overlay, "$g_presentation_credits_obj_5", ":cur_card"),
          (overlay_set_position, "$g_presentation_credits_obj_5", pos13),
          (overlay_set_size, "$g_presentation_credits_obj_5", pos14),
          (position_get_x,":x_p",pos12),
          (val_add,":x_p",60),
          (position_set_x, pos12, ":x_p"),
          (overlay_animate_to_position, "$g_presentation_credits_obj_5",300, pos12),

          (try_begin),
            (eq, reg62, 1),
            (assign, reg61, 1),
            (create_mesh_overlay, reg1, reg21),
            (overlay_set_position, reg1, pos60),
            (overlay_set_size, reg1, pos14),
          (try_end),

          (assign, reg57, 2),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (display_message, "@You stay."),
          (create_text_overlay, reg1, "@Stay"),
          (position_set_x, pos1, 660),
          (position_set_y, pos1, 100),
          (overlay_set_position, reg1, pos1),
          (overlay_set_color, reg1, 0x11dd11),
          (create_mesh_overlay, reg1, reg21),
          (overlay_set_position, reg1, pos60),
          (overlay_set_size, reg1, pos14),
          (assign, reg61, 1),
          (assign, reg57, 2),
        (else_try),
          (eq, ":object", "$g_presentation_obj_3"),
          (try_begin),
            (store_troop_gold,reg1,"trp_player"),
            (lt,reg1,reg51),
            (display_message, "@You don't have enough money."),
          (else_try),
            (eq, reg25, 0),
            (assign, reg62, 1),
            (display_message, "@Double down! You can only get one card again."),
            (troop_remove_gold, "trp_player", reg51),
            (play_sound, "snd_money_paid"),
            (val_mul, reg51, 2),
            (store_troop_gold,reg1,"trp_player"),
            (str_store_string, s1, "@Bet: {reg51} Denar(s)"),
            (overlay_set_text, "$g_presentation_obj_4", s1),
            (str_store_string, s1, "@Money: {reg1} Denar(s)"),
            (overlay_set_text, "$g_presentation_obj_5", s1),
          (else_try),
            (display_message, "@Not right now."),
          (try_end),
        (try_end),
        ]),
     ])
