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

####################################################################################################################
# DICKPLOMACY MOD SCRIPTS
# 
# This file contains scripts specific to the Dickplomacy mod extension.
# Includes: adult content (start_fucking), gambling (d6_roll, mmc_gamblers_header),
# decapitation (vc_decap_*), custom armor systems, shield bash, and body display.
####################################################################################################################

dickplomacy_scripts = [
  # value
  #OUTPUT:
  # none
  ("start_fucking",
   [
     (store_script_param, ":training_param", 1),
     (store_script_param, ":scene", 2),

		  (set_jump_mission,"mt_fucking"),
		  (modify_visitors_at_site, ":scene"),
		  (reset_visitors),

       (try_for_range, ":i", 0, ":training_param"),
         (troop_get_slot, ":cur_troop", "trp_temp_array_a", ":i"),
         (troop_get_slot, ":cur_troop_dna", "trp_temp_array_b", ":i"),
		 (ge, ":cur_troop", 0),

		(call_script, "script_dplmc_store_troop_is_female_reg", ":cur_troop", 65),
		(assign, ":is_female", reg65),

        (try_begin),
            (eq, "$g_player_is_captive", 1),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 2, af_override_horse|af_override_body|af_override_weapons),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 3, af_override_horse|af_override_body),
            (mission_tpl_entry_set_override_flags, "mt_fucking", 4, af_override_horse|af_override_body),
        (try_end),

		 #(neq, ":cur_troop", "bandit_leaders_end"),
		 (try_begin),
			(eq, ":i", 0),
			(assign, ":cur_entry_point", 1),
		 (else_try),
			(eq, ":i", 1),
			(try_begin),
				(eq, "$g_sex_position", 0),
				(assign, ":cur_entry_point", 2),
			(else_try),
				(assign, ":cur_entry_point", 3),
			(try_end),
			(try_begin),
				(eq, ":is_female", 1),
				(mission_tpl_entry_add_override_item,"mt_fucking",":cur_entry_point","itm_strapon"),
			(try_end),
		 (else_try),
			(eq, ":i", 2),
			(assign, ":cur_entry_point", 5),
		 (else_try),
			(eq, ":i", 3),
			(assign, ":cur_entry_point", 4),
			(try_begin),
				(eq, ":is_female", 1),
				(mission_tpl_entry_add_override_item,"mt_fucking",":cur_entry_point","itm_strapon"),
			(try_end),
		 (else_try),
			(assign, ":cur_entry_point", 0),
		 (try_end),


         (try_begin),
            (troop_get_type, ":type", ":cur_troop"),
            (lt, ":type", 2),
            (val_add, ":type", 2),
            (troop_set_type, ":cur_troop", ":type"),
         (try_end),
         (try_begin),
           (this_or_next|troop_is_hero, ":cur_troop"),
            (lt, ":cur_troop_dna", 0),
            (set_visitor, ":cur_entry_point", ":cur_troop"),
         (else_try),
            (set_visitor, ":cur_entry_point", ":cur_troop", ":cur_troop_dna"),
         (try_end),
       (try_end),

		(set_visitor, 0, "trp_bandit_leaders_end"),

		  (jump_to_scene,":scene"),
		  (change_screen_mission),



     ]),




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
  ),

  # script_d6_roll # "script_d6_roll"
  # Input: arg1 = none
  # Output: reg0 = mesh
  # Output: reg1 = pip
  ("d6_roll",
   [(store_script_param, ":d6", 1),
    (try_begin),
        (try_begin),
		    (eq,":d6", 0),
		    (store_random_in_range,":d6",1,7),
		(try_end),
		(try_begin),
		    (eq,":d6",1),
		    (assign,reg0,"mesh_mmc_dice_1"),
        (else_try),
		    (eq,":d6",2),
		    (assign,reg0,"mesh_mmc_dice_2"),
        (else_try),
		    (eq,":d6",3),
		    (assign,reg0,"mesh_mmc_dice_3"),
		(else_try),
		    (eq,":d6",4),
		    (assign,reg0,"mesh_mmc_dice_4"),
    	(else_try),
		    (eq,":d6",5),
		    (assign,reg0,"mesh_mmc_dice_5"),
    	(else_try),
		    (eq,":d6",6),
		    (assign,reg0,"mesh_mmc_dice_6"),
    	(try_end),
	  (assign,reg1,":d6"),
	(try_end),
   ]),

# "script_draw_d6_side"
# Description: for prsnt_dices_game
# Input:
# Output: none
 ("draw_d6_side",
   [(store_script_param, ":line", 1),
    (store_script_param, ":column", 2),
    (store_script_param, ":side", 3),#1-6
    #(store_script_param, ":present_obj", 4),
    (assign,":dice_x",220),
    (try_begin),
	    (store_mul,":offset_x",":column",55),
	    (val_add,":dice_x",":offset_x"),
        (assign,":dice_y",380),
        (assign,":offset_y",70),
    (try_end),
    (try_begin),
        (gt,":side",6),
        (val_sub,":side",6),
    (try_end),
	(try_begin),
        (eq, ":line", 1),
            (try_begin),
                (gt,"$g_presentation_obj_1", 0),
			    (overlay_set_display, "$g_presentation_obj_1", 0),
			(try_end),
    (else_try),
        (eq, ":line", 2),
            (try_begin),
                (gt,"$g_presentation_obj_2", 0),
			    (overlay_set_display, "$g_presentation_obj_2", 0),
			(try_end),
		(val_add,":dice_x",25),
        (val_sub, ":dice_y", ":offset_y"),
    (else_try),
        (eq, ":line", 3),
            (try_begin),
                (gt,"$g_presentation_obj_3", 0),
			    (overlay_set_display, "$g_presentation_obj_3", 0),
			(try_end),
		(val_sub,":dice_x",25),
		(val_mul,":offset_y",2),
        (val_sub, ":dice_y", ":offset_y"),
 	(try_end),
	(try_begin),
        (call_script, "script_d6_roll",":side"),
			(try_begin),
                (eq, ":line", 1),
                (create_mesh_overlay, "$g_presentation_obj_1", reg0),
				(assign, ":present_obj", "$g_presentation_obj_1"),
			(else_try),
                (eq, ":line", 2),
				(create_mesh_overlay, "$g_presentation_obj_2", reg0),
				(assign, ":present_obj", "$g_presentation_obj_2"),
			(else_try),
                (eq, ":line", 3),
				(create_mesh_overlay, "$g_presentation_obj_3", reg0),
				(assign, ":present_obj", "$g_presentation_obj_3"),
			(try_end),
        (position_set_x, pos1, ":dice_x"),
        (position_set_y, pos1, ":dice_y"),#380
		(overlay_set_position, ":present_obj", pos1),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 633),
        (overlay_set_size, ":present_obj", pos1),
    (try_end),
 ]),

### Dice game ### Three Cards ### END ###
   #COMBAT OSP BEGIN
#Shield Bash Script
("shield_bash",[
(this_or_next|multiplayer_is_server),
(neg|game_in_multiplayer_mode),
(get_player_agent_no,":player_agent"),
(store_skill_level,":shield_level", "skl_shield", "trp_player"),
(store_sub, ":player_shield_bash_time", 15, ":shield_level"),
(val_div,":player_shield_bash_time",3),
(store_mission_timer_a, ":current_time"),
(agent_get_slot, ":slot_last_shield_bash_time", ":player_agent", 27),
(store_add, ":time_to_shield_bash", ":player_shield_bash_time",":slot_last_shield_bash_time"),

(store_add, ":shieldstat", 1, ":shield_level"),
(store_mul, ":bash_radius", 13, ":shieldstat"),
(try_begin),
(ge, ":current_time", ":time_to_shield_bash"),
(try_begin),
(gt, ":player_agent", 0),
(agent_get_animation, ":anim", ":player_agent",0),
(agent_get_horse, ":my_horse", ":player_agent"),
(agent_get_wielded_item, ":shield_item", ":player_agent", 1),
(try_begin),
	(neq, ":anim", "anim_human_shield_bash"),
	(eq, ":my_horse", -1),
	(item_get_type, ":item_type", ":shield_item"),
	(eq, ":item_type", itp_type_shield),
	(agent_set_animation, ":player_agent","anim_human_shield_bash"),
	(agent_get_position, pos63,":player_agent"),
	(position_move_y,pos63,50),
	(agent_get_troop_id, ":id", ":player_agent"),
	(troop_get_type, ":type", ":id"),
	(try_begin),
		(eq, ":type", tf_male),
		(agent_play_sound, ":player_agent", "snd_man_grunt"), # Keep it down, this is a library.
		(agent_set_slot, ":player_agent", 27, ":current_time"),
	(else_try),
		(agent_play_sound, ":player_agent", "snd_woman_grunt"),	# Shhh...
        (agent_set_slot, ":player_agent", 27, ":current_time"),
	(try_end),
	(try_for_agents,":agent"),
		(gt, ":agent", 0),
		(neg|agent_is_ally,":agent"),#don't bash allies
		(agent_is_human, ":agent"),#stop if not human
		(agent_is_active,":agent"),
		(agent_is_alive,":agent"),
		(try_begin),
			(agent_get_position,pos62,":agent"),
			(get_distance_between_positions,":dist",pos63,pos62),
			(lt,":dist",":bash_radius"),# Now based on shield skill, not doing this for NPCs because that might get expensive.
			(agent_get_horse, ":horse", ":agent"),
			(eq, ":horse", -1),
			(neq,":agent",":player_agent"),
			(agent_play_sound, ":player_agent", "snd_wooden_hit_low_armor_high_damage"),
			(position_move_y,pos62,-25),
			(agent_set_position, ":agent", pos62),
			(try_begin),
				(store_random_in_range, ":rand", 3, 10), # No chance for critical strike unless shield skill +3
				(gt, ":shield_level", ":rand"),
				(agent_set_animation, ":agent","anim_shield_strike"),
			(else_try),
				(agent_set_animation, ":agent", "anim_shield_strike_small"),
			(try_end),
		(try_end),
	(try_end),
	(try_end),
(try_end),
(else_try),
#(display_message, "@You don't have enough shield skill to shield bash again this soon."),
# This message is super spammy and it's absolutely useless after the first time the palyer ever sees it.
(try_end),
]),


#RAMARAUNT SCRIPT - with code from Xenoargh's shield bashing OSP.
#AI shield bashing script
("agent_shield_bash",[
(this_or_next|multiplayer_is_server),
(neg|game_in_multiplayer_mode),
(store_script_param, ":agent", 1),
(agent_get_troop_id, ":troop_id", ":agent"),
(store_skill_level,":shield_level", "skl_shield", ":troop_id"),
(gt, ":shield_level", 5),
(store_sub, ":agent_shield_bash_time", 13, ":shield_level"),
(store_mission_timer_a, ":current_time"),
#Ren - I don't think we need all these nested trys but I'm not familiar enough with this script to mess with it.
(try_begin),
(agent_get_wielded_item, ":shield_item", ":agent", 1),
(neq, ":shield_item", -1),
(neq, ":shield_item", 0),
(item_get_type, ":item_type", ":shield_item"),
(eq, ":item_type", itp_type_shield),
(agent_get_slot, ":slot_last_shield_bash_time", ":agent", 27),
(store_add, ":time_to_shield_bash", ":agent_shield_bash_time",":slot_last_shield_bash_time"),
(try_begin),
(ge, ":current_time", ":time_to_shield_bash"),
(try_begin),
(gt, ":agent", 0),
(agent_get_animation, ":anim", ":agent",0),
(agent_get_horse, ":my_horse", ":agent"),
(try_begin),
	(neq, ":anim", "anim_human_shield_bash"),
	(eq, ":my_horse", -1),
	(agent_set_animation, ":agent","anim_human_shield_bash"),
	(agent_get_position, pos63,":agent"),
	(position_move_y,pos63,75),#75 cm directly ahead, so it's not a cuboid space around player center
	(agent_get_troop_id, ":id", ":agent"),
	(troop_get_type, ":type", ":id"),
	(try_begin),
		(eq, ":type", tf_male),
		(agent_play_sound, ":agent", "snd_man_grunt"),
		(agent_set_slot, ":agent", 27, ":current_time"),
	    #(display_message, "@{s2} has shield bashed!"),
	(else_try),
		(agent_play_sound, ":agent", "snd_woman_grunt"),
        (agent_set_slot, ":agent", 27, ":current_time"),
		#(display_message, "@{s2} has shield bashed!"),
	(try_end),
	(try_for_agents,":victims"),
		(gt, ":victims", 0),
		(agent_get_team, ":victim_team", ":victims"),
		(agent_get_team, ":agent_team", ":agent"),
		(teams_are_enemies, ":victim_team", ":agent_team"), #don't bash allies
		(agent_is_human, ":victims"),#stop if not human
		(agent_is_active,":victims"),
		(agent_is_alive,":victims"),
		(try_begin),
			(agent_get_position,pos62,":victims"),
			(get_distance_between_positions,":dist",pos63,pos62),
			(lt,":dist",100),#Set this to whatever you like- 1 meter radius clears a big section of crowd
			(agent_get_horse, ":horse", ":victims"),
			(eq, ":horse", -1),
			(neq,":agent",":victims"),
			(agent_play_sound, ":victims", "snd_wooden_hit_low_armor_high_damage"),
			(position_move_y,pos62,-25),
			(agent_set_position, ":victims", pos62),
			(try_begin),
				(store_random_in_range, ":rand", 6, 10), # No chance for critical strike unless shield skill +3
				(gt, ":shield_level", ":rand"),
				(agent_set_animation, ":agent","anim_shield_strike"),
			(else_try),
				(agent_set_animation, ":agent", "anim_shield_strike_small"),
			(try_end),
            (try_begin),
                (get_player_agent_no,":player"),
                (eq,":victims",":player"),
                (display_message, "@You have been shield bashed!"),
            (try_end),
		(try_end),
	(try_end),
	(try_end),
(try_end),
(try_end),
(try_end),
]),
#End Shield Bash Script

#VIKING CONQUEST DECAP STUFF - NOTE THIS CODE IS SLIGHTLY ALTERED CODE FROM VC, WHICH IS LEGAL AS LONG AS YOU GIVE CREDIT - Ramaraunt
("cf_vc_decap_check_if_possible",
	[
    #Check if the player has decapitation enabled first
    (try_begin),
    (ge, "$g_decapitation_enabled", 1),
    (store_script_param_1, ":inflicted_agent_id"),
	(store_script_param_2, ":damage"),
	(store_script_param, ":weapon_id",3),
	(store_script_param, ":attacker_id", 4),

	# Can't be: player, hero or horse nor female
	(agent_is_non_player, ":inflicted_agent_id"),
	(agent_get_troop_id, ":troop_inflicted", ":inflicted_agent_id"),
	(neg | troop_is_hero,":troop_inflicted"),
	(agent_is_human, ":inflicted_agent_id"),
	(troop_get_type, ":is_female", ":troop_inflicted"),
	(val_mod, ":is_female", 2),
	(neq, ":is_female", 1),

	#test if head hit
	(agent_get_position, pos1, ":inflicted_agent_id"),
	(get_distance_between_positions, ":distance", pos1, pos0),
	(is_between, ":distance", 90, 185), # *zing*

	#test if within melee range (this stops most ranged decaps unless they are SUPER close, which doesnt happen often so its ok)
	(agent_get_position, pos2, ":attacker_id"),
	(get_distance_between_positions, ":distance", pos2, pos1),
	(is_between, ":distance", 0, 200),


	# test weapon: cutting damage from a weapon (no missiles)
	(gt, ":weapon_id", 0),
	(item_get_swing_damage_type, ":damage_type", ":weapon_id"),
	(eq, ":damage_type", cut),

	# test to make sure it's a huge hit
	(ge, ":damage", 40),

	# test if agent is dying from the hit
	(store_agent_hit_points, ":inflicted_hp", ":inflicted_agent_id", 1),
	(store_sub, ":inflicted_new_hp", ":inflicted_hp", ":damage"),
	(le, ":inflicted_new_hp", 0),
    (try_end),
      ]),

("cf_vc_decap_probability",
    [(store_script_param_1, ":inflicted_agent_id"),
      (store_script_param_2, ":attacker_agent_id"),
      (store_script_param, ":weapon_id",3),

      (agent_is_human, ":inflicted_agent_id"),
      (agent_is_human, ":attacker_agent_id"),
      (gt, ":weapon_id", 0),
	  (get_player_agent_no,":player"),
	  (agent_get_troop_id, ":player_troop", ":player"),

      ### Probability ###
      #BASE: 5
      #IF PLAYER
      #	BASE: +5
      #	IF MOUNTED +30
      #	IF STR>15 : +10
      #	IF PS>7 : +10
      #IF BOT
      #	IF MOUNTED +10
      #IF AXE +5
      #IF HAS HELMET -5
      #MIN CHANCE: 5
      (assign, ":base_chance", 5),

      (try_begin),

        # Mounted bot
        (agent_get_horse, ":horse_id", ":attacker_agent_id"),
        (try_begin),
          (agent_is_non_player, ":attacker_agent_id"),

          (try_begin),
            (neq, ":horse_id", -1),
            (val_add, ":base_chance", 10),
          (try_end),

          #Player bonus
        (else_try),
		  (eq,":attacker_agent_id",":player"),
		  (store_attribute_level, ":skill", ":player_troop", ca_strength),
          (val_add, ":base_chance", ":skill"),
          (try_begin),
            (neq, ":horse_id", -1),
            (val_add, ":base_chance", 30),
          (try_end),
        (try_end),


        # Helmet
        (try_begin),
          (agent_get_item_slot, ":head_gear", ":inflicted_agent_id", ek_head),
          (ge, ":head_gear", 1),
          (item_get_head_armor, ":armor", ":head_gear"),
          (gt, ":armor", 20),
          (val_sub, ":base_chance", 5),
        (try_end),

        (val_max, ":base_chance", 5),
      (try_end),

      (store_random_in_range, ":rand", 0, 101),

      #(val_div, ":base_chance", 2),#VC-3296
      # Debugging
      (ge, ":base_chance", ":rand"),]),

  # Description: for decapitation -> blood, helmet, spawn head
  # Input: inflicted_agent_id, head_position
  # Output: none
  ("vc_decap_special_effects",
    [
    #Check if the player has decapitation enabled first
    (try_begin),
    (ge, "$g_decapitation_enabled", 1),
    (store_script_param_1, ":inflicted_agent_id"),

      # Checks if agent was using a helmet
      (try_begin),
        (agent_get_item_slot, ":head_gear", ":inflicted_agent_id", ek_head),
        (ge, ":head_gear", 1),
        (assign, ":spawn_for_timer", 60),

        # helmet on the ground
        (copy_position, pos2, pos1),
        (position_move_x, pos2, 20, 0),
        (position_move_z, pos2, -30, 0),
        (store_random_in_range, ":rot_x", 10, 40),
        (store_random_in_range, ":rot_z", 15, 75),
        (position_rotate_x, pos2, ":rot_x", 1),
        (position_rotate_z, pos2, ":rot_z", 1),
        (position_set_z_to_ground_level, pos2),
        (position_move_y, pos2, -5, 1),
        (set_spawn_position, pos2),
        (spawn_item, ":head_gear", 0, ":spawn_for_timer"),

        (agent_unequip_item, ":inflicted_agent_id", ":head_gear"),
      (try_end),

      # equip invisible head on agent
      (agent_equip_item, ":inflicted_agent_id", "itm_untitled"),

      # blood
      (copy_position, pos2, pos0),
      (set_spawn_position, pos2),
      (particle_system_burst, "psys_game_blood", pos2, 5),

      # fake head
      (spawn_scene_prop, "spr_physics_head"),
      (assign, ":head_id", reg0),

      (prop_instance_enable_physics, ":head_id", 1),

      # makes sure the agent dies
      (agent_set_hit_points,":inflicted_agent_id", 0, 1),
      (try_end),
      ]),


#VIKING CONQUEST END
#COMBAT OSP END

#custom armor
  #script_add_troop_to_custom_armor_tableau
  # INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
  # OUTPUT: none
  ("add_troop_to_custom_armor_tableau",	# NOT USED YET - Pure Somebody code
    [
       (store_script_param, ":troop_no",1),
       (store_mul, ":side", "$g_custom_armor_angle", 60), #add some more sides

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),

	   (cur_tableau_set_override_flags, af_override_weapons),

       (init_position, pos2),
       (position_rotate_z, pos2, ":side"),
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (val_clamp, "$g_custom_armor_angle", 0, anim_walk_forward_crouch - anim_walk_backward),
       (store_add, ":animation", "$g_custom_armor_angle", "anim_walk_backward"),

       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

	   (try_begin), #shouldn't be necessary, it's already on the troop (player character) - good for hand items
         (gt, "$g_current_opened_item_details", -1),
         (cur_tableau_add_override_item, "$g_current_opened_item_details"),
       (try_end),

		(call_script, "script_show_body_on_tableau", ":troop_no"), # force show body item for tattoos, and loins if cenzored
		#custom armor

       (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30),
       (position_rotate_x, pos8, -60),
       (cur_tableau_add_sun_light, pos8, 155,155,155),
     ]),
#DtheHun
  ("init_custom_armor1",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_armor_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 8),
	(try_begin), #SKIN none, assassin*, leather
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 3), #2 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_skin_0"),
    (else_try), #CHEST none, loin, sonja, risty
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_bra_0"),
	(else_try), #PANTY none, morag*, chain, risty, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_panty_0"),
	(else_try), #BELT none, assassin*, sonja, angela, risty
      (eq, ":sub_part", 3),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_belt_0"),
    (else_try), #BUTT none, assassin*, angela?, sonja, loin
      (eq, ":sub_part", 4),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_ass_0"),
    (else_try), #KNEE none, scale, sonja, assassin
      (eq, ":sub_part", 5),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_knee_0"),
    (else_try), #PAULDRON LEFT none, plate, scale, assa_pauld, sonja, risty
      (eq, ":sub_part", 6),
      (is_between, ":sub_comp", 0, 6), #5 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_pdn_l_0"),
    (else_try), #PAULDRON RIGHT none, plate, scale, assa_pauld, sonja, risty
      (eq, ":sub_part", 7),
      (is_between, ":sub_comp", 0, 6), #5 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_pdn_r_0"),
    (else_try), #ELBOW LEFT none, plate, assassin_sleeves
      (eq, ":sub_part", 8),
      (is_between, ":sub_comp", 0, 3), #2 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_elb_l_0"),
    (else_try), #ELBOW RIGHT none, plate, plate, assassin_sleeves
      (eq, ":sub_part", 9),
      (is_between, ":sub_comp", 0, 3), #2 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_elb_r_0"),
    (else_try), #BRACER LEFT none, plate, sonja, Risty
      (eq, ":sub_part", 10),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_brc_l_0"),
    (else_try), #BRACER RIGHT none, plate, sonja, Risty
      (eq, ":sub_part", 11),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_brc_r_0"),
	(else_try), #NECK none,
      (eq, ":sub_part", 12),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_neck_0"),
    (else_try), #CAPE none,
      (eq, ":sub_part", 13),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca1_cape_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  ),

  ("init_custom_armor2",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_armor_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 10),
	(try_begin), #SKIN none, assassin*, chainmail, leather
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_skin_0"),
    (else_try), #CHEST none, scale, angela, sonja, -loin, -risty
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 6), #5 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_bra_0"),
	(else_try), #PANTY none, assassin*, chain, risty, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_panty_0"),
	(else_try), #BELT none, assassin*, sonja, angela, -risty
      (eq, ":sub_part", 3),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_belt_0"),
    (else_try), #BUTT none, assassin*, angela, scale, sonja, loin
      (eq, ":sub_part", 4),
      (is_between, ":sub_comp", 0, 6), #5 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_ass_0"),
    (else_try), #KNEE none, angela, plated_assassin, assassin, sonja, -scale
      (eq, ":sub_part", 5),
      (is_between, ":sub_comp", 0, 6), #5 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_knee_0"),
    (else_try), #PAULDRON LEFT none, plate, scale, assa_pauld, ang_shoul, ang_pauld, assa_shoul, sonja,-risty
      (eq, ":sub_part", 6),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_pdn_l_0"),
    (else_try), #PAULDRON RIGHT none, plate, scale, assa_pauld, ang_shoul, ang_pauld, assa_shoul, sonja, -risty
      (eq, ":sub_part", 7),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_pdn_r_0"),
    (else_try), #ELBOW LEFT none, plate, assassin_sleeves, angela
      (eq, ":sub_part", 8),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_elb_l_0"),
    (else_try), #ELBOW RIGHT none, plate, assassin_sleeves, angela
      (eq, ":sub_part", 9),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_elb_r_0"),
    (else_try), #BRACER LEFT none, plate, sonja, angela,  Risty
      (eq, ":sub_part", 10),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_brc_l_0"),
    (else_try), #BRACER RIGHT none, plate, sonja, angela, Risty
      (eq, ":sub_part", 11),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_brc_r_0"),
    (else_try), #NECK none, -sonja
      (eq, ":sub_part", 12),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_neck_0"),
    (else_try), #CAPE none, -angela
      (eq, ":sub_part", 13),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca2_cape_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  ),

  ("init_custom_armor3",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_armor_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 12),
	(try_begin), #SKIN none, assassin*, chainmail, leather
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_skin_0"),
    (else_try), #CHEST none, plate, scale, angela, -loin, -sonja, -risty
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 7), #6 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_bra_0"),
	(else_try), #PANTY none, morag*, chain, risty, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_panty_0"),
	(else_try), #BELT none, assassin*, ?angela, sonja, -risty
      (eq, ":sub_part", 3),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_belt_0"),
    (else_try), #BUTT none, assassin*, ?angela, scale, sonja, -loin
      (eq, ":sub_part", 4),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_ass_0"),
    (else_try), #KNEE none, plate, plated_assassin, angela, -assassin, -sonja, -scale
      (eq, ":sub_part", 5),
      (is_between, ":sub_comp", 0, 7), #6 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_knee_0"),
    (else_try), #PAULDRON LEFT none, plate, scale, assa_shoul, ang_pauld, ang_shold, -assa_pauld, -sonja, -risty,
      (eq, ":sub_part", 6),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_pdn_l_0"),
    (else_try), #PAULDRON RIGHT none, plate, scale, assa_shoul, ang_pauld, ang_shold, -assa_pauld, -sonja, -risty,
      (eq, ":sub_part", 7),
      (is_between, ":sub_comp", 0, 9), #8 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_pdn_r_0"),
    (else_try), #ELBOW LEFT none, plate, angela, -assassin_sleeves
      (eq, ":sub_part", 8),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_elb_l_0"),
    (else_try), #ELBOW RIGHT none, plate, angela, -assassin_sleeves
      (eq, ":sub_part", 9),
      (is_between, ":sub_comp", 0, 4), #3 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_elb_r_0"),
    (else_try), #BRACER LEFT none, plate, sonja, angela, Risty
      (eq, ":sub_part", 10),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_brc_l_0"),
    (else_try), #BRACER RIGHT none, plate, sonja, angela, Risty
      (eq, ":sub_part", 11),
      (is_between, ":sub_comp", 0, 5), #4 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_brc_r_0"),
    (else_try), #NECK none, -sonja
      (eq, ":sub_part", 12),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_neck_0"),
    (else_try), #CAPE none, -angela
      (eq, ":sub_part", 13),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_ca3_cape_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  ),

  ("init_plate_helm_dthun",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_helm_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 5),
	(try_begin), #DECORATION: none, plate_wings, angela_wings
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 3), #2 + none
      (store_add, ":value", ":sub_comp", "itm_cph_dec_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  ),
  ("init_angela_helm",
    [
    (store_script_param, ":agent_no", 1),
    #(store_script_param, ":troop_no", 2),
    (store_script_param, ":sub_part", 3),
    (store_script_param, ":sub_comp", 4),
	(str_clear, s1),
  #SAVE AGENT ARMOR SLOT FOR SCENE
	(try_begin),
		(neq, ":agent_no", -1),
		(store_add, ":agent_armor_slot", slot_agent_helm_slots_begin, ":sub_part"),
		(agent_set_slot, ":agent_no", ":agent_armor_slot", ":sub_comp"),
	(try_end),
  #MAKE COMPONENT MESH STRING OUTPUT
    (assign, ":value", -1),
    (assign, "$g_custom_armor_param_count", 5),
	(try_begin), #FACE: none, angela
      (eq, ":sub_part", 0),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_face_0"),
	(else_try), #WING_UP: none, angela
      (eq, ":sub_part", 1),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_wings_up_0"),
	(else_try), #WING_DOWN: none, angela
      (eq, ":sub_part", 2),
      (is_between, ":sub_comp", 0, 2), #1 + none
      (store_add, ":value", ":sub_comp", "itm_cah_wings_down_0"),
	(else_try), #END
      (assign, "$g_custom_armor_param_count", 0),
    (try_end),
    (try_begin),
      (neq, ":value", -1),
      (str_store_item_name, s1, ":value"), 	#<- item name (string)
    (try_end),
	(assign, reg0, ":value"), 				#<- item_no
    ]
  ),
#/custom armor
  ("sir_lady", [ #male 1, female 0, (player, talk_troop) -> (reg33, reg6)
		(troop_get_type, ":is_female", "trp_player"),
		(try_begin),
			(ge, ":is_female", 1),
			(assign, reg33, 0),
		(else_try),
			(assign, reg33, 1),
		(try_end),
		#(troop_get_type, ":is_female", "$g_talk_troop"),
		#(try_begin),
		#	(ge, ":is_female", 1),
		#	(assign, reg6, 0),
		#(else_try),
		#	(assign, reg6, 1),
		#(try_end),
	]
  ),

#DtheHun

  #script_add_troop_to_custom_armor_tableau
  # INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
  # OUTPUT: reg0 (-1):do nothing, (0):equip body, (1):equip loincloth - for additional troop equip if must (character -> face morpf)
  ("show_body_on_tableau",
    [
		(store_script_param, ":troop_no", 1),
		(assign, reg0, -1),
		(try_begin),
			(troop_get_type, ":is_female", ":troop_no"),
			(ge, ":is_female", 1),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
			(eq, ":item_no", -1), #-1:none equipped
			(cur_tableau_clear_override_items),
			(cur_tableau_set_override_flags, af_override_everything), # makes it possible to set_override ek_body item without adding it to troop
			(try_begin),
				#(eq, "$g_cenzura", 1),
				(eq, 0, 1),
				(cur_tableau_add_override_item, "itm_loincloth"),
				(assign, reg0, 1),
			(else_try),
				(cur_tableau_add_override_item, "itm_body_fem"),
				(assign, reg0, 0),
			(try_end),
			(try_for_range, ":item_slot", ek_head, ek_horse), # do removed clothes back
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
				(ge, ":item_no", 0),
				(cur_tableau_add_override_item, ":item_no"),
			(try_end),
		(try_end),
     ]),

  #script_add_troop_to_custom_armor_tableau
  # INPUT: troop_no, item (g_current_opened_item_details), side (g_custom_armor_angle)
  # OUTPUT: none
  ("remove_body_from_inventory",
    [
		(store_script_param, ":troop_no", 1),
		(troop_get_type, ":is_female", ":troop_no"),
		(try_begin),
			(ge, ":is_female", 1),	#check: body/loincloth equipped ->remove it from inventory (equipped in character window for face morph scene)
			(try_begin),	# troop has it from opening character tab till next inventory opening -> can lose it in battle, has unique flag -> won't see back (hopefully noone equips it)
				(troop_has_item_equipped, ":troop_no", "itm_body_fem"),
				(troop_remove_item, ":troop_no", "itm_body_fem"),
			(else_try),
				(troop_has_item_equipped, ":troop_no", "itm_loincloth"),
				(troop_remove_item, ":troop_no", "itm_loincloth"),
			(else_try),
				#(eq, "$g_cenzura", 1),
				(eq, 0, 1),
				(try_begin),
					(troop_has_item_equipped, ":troop_no", "itm_loin_top"),
					(troop_remove_item, ":troop_no", "itm_loin_top"),
				(else_try),
					(troop_has_item_equipped, ":troop_no", "itm_loin_skirt"),
					(troop_remove_item, ":troop_no", "itm_loin_skirt"),
				(try_end),
			(try_end),
		(try_end),
     ]),

  ("done_skin",
	[
		(store_script_param, ":agent_no", 1),
		(try_begin),
			(agent_is_active, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(troop_get_type, ":is_female", ":troop_no"),
			(ge, ":is_female", 1),
			(agent_get_item_slot, ":body_armor", ":agent_no", ek_body),
			(try_begin),
				(neq, ":body_armor", -1),
				(agent_unequip_item, ":agent_no", ":body_armor"),	# (may have changed in inventory, and have the same base name -> changes only second time without unequipping)
			(try_end),
			(try_begin),
				(this_or_next|eq, ":body_armor", -1),
				(this_or_next|eq, ":body_armor", "itm_body_fem"), # <- remained back from character window equip
				(this_or_next|eq, ":body_armor", "itm_loin_top"),
				(eq, ":body_armor",  "itm_loin_skirt"),	# <- trp_looter_woman
				(try_begin), #Nincs -> cenzura -> "loincloth" felvesz
					(eq, "$g_cenzura", 1),
					(agent_equip_item, ":agent_no", "itm_loincloth"),
				(else_try), #Volt rajta?
					(this_or_next|eq, ":body_armor", -1),
					(eq, ":body_armor", "itm_body_fem"),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
					(try_begin),
					#Had the troop clothes training before mission?
						#mtf_override body -> equip loin parts corresponding to base armor components (bra?, bottom?)
						(gt, ":item_no", -1),
						(neq, ":item_no", "itm_body_fem"), # <- remained back from character window equip
						(try_begin), #save first customizable
						#Custom
							(item_slot_ge, ":item_no", slot_item_num_components, 1),
							(assign, ":cur_mesh_slot", slot_troop_armor_slots_begin), 	#0.: skin slot
							(try_begin),
							#Has Skin -> loincloth
								(troop_get_slot, ":skin", ":troop_no", ":cur_mesh_slot"),
								(neq, ":skin", 0),
								(agent_equip_item, ":agent_no", "itm_loincloth"),
							(else_try),
							#!Skin, Panty, Bra -> loincloth
								(val_add, ":cur_mesh_slot", 1),							#1.: chest slot
								(troop_get_slot, ":bra", ":troop_no", ":cur_mesh_slot"),
								(val_add, ":cur_mesh_slot", 1),							#2.: panty slot
								(troop_get_slot, ":panty", ":troop_no", ":cur_mesh_slot"),
							   #(eq, ":skin", 0),
								(neq, ":bra", 0),
								(neq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loincloth"),
							(else_try),
							#!Skin, Bra, !Panty -> loin_top
							   #(eq, ":skin", 0),
								(neq, ":bra", 0),
								(eq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loin_top"),
							(else_try),
							#!Skin, !Bra, Panty -> loin_skirt
							   #(eq, ":skin", 0),
								(eq, ":bra", 0),
								(neq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_loin_skirt"),
							(else_try),
							#!Skin, !Bra, !Panty -> body for TATTOOS
							   #(eq, ":skin", 0),
							   #(eq, ":bra", 0),
							   #(eq, ":panty", 0),
								(agent_equip_item, ":agent_no", "itm_body_fem"),
							(try_end),
						(else_try),
						#Egyeb ruha	-> "loincloth" felvesz
							(agent_equip_item, ":agent_no", "itm_loincloth"),
						(try_end),
					(else_try),
					#Was nude before mission -> body for TATTOOS
						(agent_equip_item, ":agent_no", "itm_body_fem"),
					(try_end),
				(try_end),
			(else_try),	#Equip back original item
				(agent_equip_item, ":agent_no", ":body_armor"),
			(try_end),
		(try_end),
	]
  ),

  ("set_custom_armor_slots",
	[
	   #set slots random for everyone
		(try_for_range, ":npc", 0, "trp_coop_companion_equipment_ui_0"),
			(try_for_range, ":slot_no", slot_troop_armor_slots_begin, slot_troop_helm_slots_end),
				(troop_set_slot, ":npc", ":slot_no", -1), # random = -1
			(try_end),
		(try_end),

	    #(display_message, "@Initializing troop slots DONE"),

	   #Light
		(item_set_slot, "itm_custom_armor1", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor1", slot_item_init_script, "script_init_custom_armor1"),
	   #Medium
		(item_set_slot, "itm_custom_armor2", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor2", slot_item_init_script, "script_init_custom_armor2"),
	   #Heavy
		(item_set_slot, "itm_custom_armor3", slot_item_num_components, 14), #14 customizable
		(item_set_slot, "itm_custom_armor3", slot_item_init_script, "script_init_custom_armor3"),
	   #Plate Helm
		(item_set_slot, "itm_plate_helm_dthun", slot_item_num_components, 1), #1 customizable
		(item_set_slot, "itm_plate_helm_dthun", slot_item_init_script, "script_init_plate_helm_dthun"),
	   #Angela Helm
		(item_set_slot, "itm_angela_helm", slot_item_num_components, 3), #3 customizable
		(item_set_slot, "itm_angela_helm", slot_item_init_script, "script_init_angela_helm"),
		#(try_for_range, ":slot_no", slot_item_player_slots_begin, slot_item_player_slots_end + 1), # troop slots added insted item slots
		#  (item_set_slot, "itm_plate_helm_dthun", ":slot_no", -1), # random = -1
		#(try_end),

		#(display_message, "@Initializing armor slots DONE"),

		#(troop_set_slot, "trp_player", slot_troop_tattoo, 0),
	]
  ),

  #script_find_customizable_item_equipped_on_troop
  # INPUT: 	troop_no
  # OUTPUT: none
  # SETS: 	item (g_current_opened_item_details)
  ("find_customizable_item_equipped_on_troop",
	[

	#Here's my lazy way.
	 (store_script_param, ":troop_no", 1),
	 (assign, "$g_current_opened_item_details", -1),
	 (assign, ":begin", ek_item_0), #should add a global as iterator
     (try_for_range, ":item_slot", ":begin", ek_foot),
		(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
		(gt, ":item_no", -1),
		(this_or_next|eq, ":item_no", itm_custom_armor1),
		(this_or_next|eq, ":item_no", itm_custom_armor2),
		(this_or_next|eq, ":item_no", itm_custom_armor3),
		(this_or_next|eq, ":item_no", itm_plate_helm_dthun),
		(eq, ":item_no", itm_angela_helm),
		(assign, "$g_current_opened_item_details", ":item_no"),
	 (else_try),
		(troop_get_type, ":is_female", ":troop_no"),
		(eq, ":is_female", 5),
		(assign, "$g_current_opened_item_details", "itm_body_fem"),
     (try_end),
	 (gt, "$g_current_opened_item_details", -1),
	# (store_script_param, ":troop_no", 1),
	# (assign, "$g_current_opened_item_details", -1),
	# (assign, ":begin", ek_item_0), #should add a global as iterator
    # (try_for_range_backwards, ":item_slot", ":begin", ek_foot),	#backwards: body armor first
	#	(troop_get_inventory_slot, ":item_no", ":troop_no", ":item_slot"),
	#	(gt, ":item_no", -1),
	#	(item_slot_ge, ":item_no", slot_item_num_components, 1),
	#	(assign, "$g_current_opened_item_details", ":item_no"),
	#	(assign, ":begin", ek_foot),
    # (else_try),	#to be able to change tattoo without custom item # Good idea but leads to unexpected results with the other body, best to just disable it.
	#	(troop_get_type, ":is_female", ":troop_no"),
	#	(ge, ":is_female", 1),
	#	(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
	#	(try_begin),
	#		(gt, ":item_no", -1),
	#		(assign, "$g_current_opened_item_details", ":item_no"),
	#	(else_try),
	#		(assign, "$g_current_opened_item_details", "itm_body_fem"),
	#	(try_end),
    # (try_end),
	]
  ),
  #script_item_add_component
  # INPUT: 	1:agent_no, 2:troop_no, 3:use_agent_slots, 4:item_script_no, 5:mesh_num, 6:random_begin, 7:random_end, 8:special_part
  # 	$g_presentation_obj_item_select_2, reg1(:troop_item_slots_begin), reg2(:agent_item_slots_begin)
  # OUTPUT: ":special_part" (reg3)
  # SETS: 	item (g_current_opened_item_details)
  ("custom_item_prepare_component",
	[
	  (store_script_param, ":agent_no", 1),
	  (store_script_param, ":troop_no", 2),
      (store_script_param, ":use_agent_slots", 3),
	  (store_script_param, ":item_script_no", 4),
      (store_script_param, ":mesh_num", 5),
	  (store_script_param, ":random_begin", 6),
	  (store_script_param, ":random_end", 7),
	  (store_script_param, ":special_part", 8),	#(has requirements) 0: nothing, 1: assa. cover, 2:symm. with prev, 3: angela cover
	#GET
	  (store_add, ":troop_item_slot_no", reg1 , ":mesh_num"),
	  (store_add, ":agent_item_slot_no", reg2 , ":mesh_num"),	#<- only body

	  (try_begin),
		(try_begin),
			(eq, ":use_agent_slots", 0),
			(troop_get_slot, ":value", ":troop_no", ":troop_item_slot_no"), # slot_troop_armor_slots_begin + :mesh_num (0-13)
		(else_try),
			(agent_get_slot, ":value", ":agent_no", ":agent_item_slot_no"), #
		(try_end),
      #RANDOMIZE
		(eq, ":value", -1),
		(try_begin),
			(eq, "$g_dthehun_sync_random", 1),
			(troop_get_slot, ":value", "trp_temp_array_a", ":troop_item_slot_no"), # get prev random for tableau mask be sync.
		(else_try),
			(store_random_in_range, ":value", ":random_begin", ":random_end"),
			(try_begin), #special_part
			  #ass cover
				(eq, ":special_part", 1),
				(try_begin),
					(this_or_next|eq, ":value", 1),	# assassin
								 (eq, ":value", 2),	# Angela
					(try_begin),
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 0, 1), 	#has assa skin
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 1), 	#has assa panty
						(this_or_next|troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 2, 2), 	#has Angela panty
						(troop_slot_eq, "trp_temp_array_a", slot_troop_armor_slots_begin + 3, 1), 				#has assa belt
					(else_try),	#<- there is nothing to hanging on it
						(store_random_in_range, ":value", 1, ":random_end"), #<- new shuffle
						(eq, ":value", 1),
						(assign, ":value", 0),
					(try_end),
				(try_end),
			(else_try),
			  # symm. with previous component
				(eq, ":special_part", 2),
				(store_random_in_range, ":rand", 0, 6),	#(less than 16.66% could be asymmetric)
				(ge, ":rand", 1),
				(store_sub, ":prev_troop_item_slot_no", ":troop_item_slot_no", 1),
				(troop_get_slot, ":prev_value", "trp_temp_array_a", ":prev_troop_item_slot_no"),
				(assign, ":value", ":prev_value"),
			(try_end),
		(try_end),
	  (try_end),
	  (troop_set_slot, "trp_temp_array_a", ":troop_item_slot_no", ":value"), # remember randomization for tableau alpha
	  (try_begin),
		(neq, ":value", 0),
		(call_script, ":item_script_no", ":agent_no", ":troop_no", ":mesh_num", ":value"),#
		(neg|str_is_empty, s1),
		(cur_item_add_mesh, s1),
	  (try_end),
	]
  ),

  #script_set_calves - This is for SANDALS!!!
  # INPUT: 	1:agent_no, 2:troop_no,2, reg1(:troop_item_slots_begin), reg2(:agent_item_slots_begin)
  # OUTPUT:	NONE
 #("set_calves", [
#	(store_trigger_param_1, ":agent_no"), # -1 if not in scene
#	(store_trigger_param_2, ":troop_no"),
#	(try_begin),
#		(eq, ":agent_no", -1),	#not in scene (presentation)
#		(is_between, ":troop_no", "trp_town_1_armorer", "trp_merchants_end"),	#trade - item from merchant inventory gives merchant no despite player equips it
#		(assign, ":troop_no", "trp_player"),
#	(try_end),
#	(try_begin),
#		(troop_get_type, ":troop_type", ":troop_no"),
#		(try_begin),
#			(this_or_next|eq, ":troop_type", tf_female), #female || tf_woman_nude || calfwoman (don't change male!)
#			(this_or_next|eq, ":troop_type", tf_woman_nude),
#			(eq, ":troop_type", tf_calfwoman),
#			(try_begin),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_risty_sandals"), #tf_calfwoman and has sandals on -> no change
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_sonja_boots"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_sonja_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_diabassa_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_plate_armor_dthun"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor3"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor2"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_custom_armor1"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_risty_armor"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_scale_armor_dthun"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loincloth"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loin_top"),
#				(this_or_next|troop_has_item_equipped , ":troop_no", "itm_loin_skirt"),
#				(troop_has_item_equipped , ":troop_no", "itm_body_fem"),
#				(try_begin),
#					(this_or_next|eq, ":troop_type", tf_female),(eq, ":troop_type", tf_woman_nude),
#					(troop_set_type, ":troop_no", tf_calfwoman),
#					(assign, ":troop_changed", 1),
#				(try_end),
#			(else_try),
#				(eq, ":troop_type", tf_calfwoman),
#				(troop_set_type, ":troop_no", tf_female),
#				(assign, ":troop_changed", 1),
#			(try_end),
#			(ge, ":agent_no", 0), # in scene - warnings from map else
#			(eq, ":troop_changed", 1),
#			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
#			(ge, ":item_no", 0), # has body armor -> must refresh to see the change in scene
#			(agent_unequip_item, ":agent_no", ":item_no"),
#			(agent_equip_item, ":agent_no", ":item_no"),
#		(try_end),
#	(try_end),
#	]
 # ),

 # script_roll_for_charisma
 # ex:
 # (call_script, "script_roll_for_charisma", Difficulty_Modifier, Target_Troop, Propositioning_Troop),
 # Outputs none
 ("roll_for_charisma", [
  (store_trigger_param_1, ":difmod"),
  (store_trigger_param_2, ":target"), # Should default to 0, which is the player troop
  (store_trigger_param_3, ":roller"),

  (assign, ":end", 0),

    (store_attribute_level, ":cha", ":roller", ca_charisma),
    (assign, ":required_cha", 12),
	(val_add, ":required_cha", ":difmod"),
    (troop_get_slot, ":renown", ":roller", slot_troop_renown),
    (val_div, ":renown", 100),

    (store_skill_level, ":persuasion", "skl_persuasion", ":roller"),

    (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":target", ":roller"),
    (assign, ":target_gender", reg0),
	(assign, ":roller_gender", reg1),

    (try_begin),
		# Same-gender is a lot harder.
		(eq, ":target_gender", ":roller_gender"),
        (val_add, ":required_cha", 8),
    (else_try),
		# Women are harder.
		(eq, ":target_gender", 1),
        (val_add, ":required_cha", 6),
	(else_try),
		# Men are easier.
        (eq, ":target_gender", 0),
        (val_sub, ":required_cha", 6),
    (try_end),

    (try_begin),
        (is_between, ":target", heroes_begin, heroes_end),

        (val_div, ":renown", 2),

        (try_begin), # Noble ladies are even harder.
            (is_between, ":target", kingdom_ladies_begin, kingdom_ladies_end),
            (val_add, ":required_cha", 10),
            (try_begin),
                (this_or_next|troop_slot_eq, ":target", slot_lord_reputation_type, lrep_moralist),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_conventional),
                (val_add, ":required_cha", 10),
            (else_try),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_adventurous),
                (val_sub, ":required_cha", 5),
            (else_try),
                (troop_slot_eq, ":target", slot_lord_reputation_type, lrep_ambitious),
                (val_add, ":required_cha", 5),
                (val_sub, ":required_cha", ":renown"),
            (try_end),
        (try_end),
    (try_end),

	(try_begin), # Pretenders are MUCH harder. O . O . F .
		(eq, ":target", "$supported_pretender"),
		(troop_get_slot, ":troop_renown", ":target", slot_troop_renown),
		(try_begin),
			(gt, ":troop_renown", ":renown"),
			(store_sub, ":renown_diff", ":troop_renown", ":renown"),
			(val_div, ":renown_diff", 50),
			(val_add, ":required_cha", ":renown_diff"),
		(try_end),
		(val_add, ":required_cha", 20),
	(try_end),

    (call_script, "script_troop_get_relation_with_troop", ":roller", ":target"),
    (assign, ":rel", reg0),
    (try_begin), # Negative relation is a no-go
        (lt, ":rel", 0),
        (assign, ":end", 1),
    (try_end),
    (val_div, ":rel", 5), # Every 5 relation is equal to 1 Cha
    (val_sub, ":required_cha", ":rel"),
    (val_sub, ":persuasion"),
    (val_sub, ":required_cha", ":renown"),

    (val_max, ":required_cha", 9),

    (try_begin),
        (ge, "$cheat_mode", 1),
		(eq, ":roller", "trp_player"),
        (assign, reg0, ":required_cha"),
        (display_message, "@Required Charisma: {reg0}"),
    (try_end),

	(eq, ":end", 0),
    (ge, ":cha", ":required_cha"),
  ]),

  # script_change_player_controversy
]
