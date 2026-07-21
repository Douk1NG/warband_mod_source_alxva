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

mmc_gamblers_header_scripts = [
# #Formations Scripts
### Three Cards ### Dice game ###
# "script_mmc_gamblers_header"
# Description: create presentation header for mmc gamblers
# Input1:
# Output: none
("mmc_gamblers_header",
   [	(assign,"$g_presentation_obj_1",-1), # mesh king of spades
        (assign,"$g_presentation_obj_2",-1), # mesh queen of heart
        (assign,"$g_presentation_obj_3",-1), # mesh king of clubs
        (assign,"$g_presentation_obj_4",-1), # text "@Bet: {reg51}Denar"
        (assign,"$g_presentation_obj_5",-1), # text "@Money: {reg1}Denar"
        (assign,"$g_presentation_obj_6",-1), # "mesh_text_bar"
        (assign,"$g_presentation_obj_7",-1), # slider
        (assign,"$g_presentation_obj_8",-1), # text "@Bet: {reg51}Denar" above slider
        (assign,"$g_presentation_obj_9",-1), # win or lose window
        (assign,"$g_presentation_obj_10",-1),#done button
        (assign,"$g_presentation_obj_11",-1),#find the lady
        (assign,"$g_presentation_obj_12",-1),#yes
        (assign,"$g_presentation_obj_13",-1),#no
        (assign,"$g_presentation_obj_14",-1),#start game button
        (assign,"$g_presentation_obj_15",-1),
        (assign,"$g_presentation_obj_16",-1),
        (assign,"$g_presentation_obj_17",-1),
		(assign, reg1,0),
		(assign, reg2,0),
		(assign, reg3,0),
		(assign, reg4,0),
		(assign, reg5,0),
        (assign, reg50, 0),
        (assign, reg51, 1),
        (assign, reg52, 0),
        (assign, reg53, 0),#
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
#"mesh_jack_black_portrait"
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
#info window right
        (create_mesh_overlay, reg1, "mesh_3card_window"),#3card_textbar#text_bar
        (position_set_x, pos1, 780),#700
        (position_set_y, pos1, 310),#270
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 250),#
        (position_set_y, pos1, 200),#
        (overlay_set_size, reg1, pos1),

        (str_store_string, s1, "@Bet: {reg51}Denar"),#
        (create_text_overlay, "$g_presentation_obj_4", s1),#
        (position_set_x, pos1, 790),#755
        (position_set_y, pos1, 355),#355
        (overlay_set_position, "$g_presentation_obj_4", pos1),
        (overlay_set_color, "$g_presentation_obj_4",),#0xfffccc
        (store_troop_gold,reg1,"trp_player"),#
        (create_text_overlay, "$g_presentation_obj_5", "@Money: {reg1}Denar"),
        (position_set_x, pos1, 790),#755
        (position_set_y, pos1, 325),#325
        (overlay_set_position, "$g_presentation_obj_5", pos1),
        (overlay_set_color, "$g_presentation_obj_5"),#0xfffccc
    ]
  )
]
