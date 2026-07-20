# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

invite_player_to_faction_menu = [
(
    "invite_player_to_faction",mnf_scale_picture,
##diplomacy start+ fix gender of pronouns
    "You receive an offer of vassalage!^^\
 {s8} of {s9} has sent a royal herald to bring you an invititation in {reg4?her:his} own hand.\
 You would be granted the honour of becoming a vassal {lord/lady} of {s9},\
 and in return {s8} asks you to swear an oath of homage to {reg4?her:him} and fight in {reg4?her:his} military campaigns,\
 offering you the fief of {s2} for your loyal service.\
 {reg4?She:He} will surely be offended if you do not take the offer...",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (faction_get_slot, "$g_invite_faction_lord", "$g_invite_faction", slot_faction_leader),
        ##diplomacy start+ store gender in reg4
        (call_script, "script_dplmc_store_troop_is_female", "$g_invite_faction_lord"),
        (assign, reg4, reg0),
        ##diplomacy start+
        (str_store_troop_name, s8, "$g_invite_faction_lord"),
        (str_store_faction_name, s9, "$g_invite_faction"),
        (str_store_party_name, s2, "$g_invite_offered_center"),
      ],
    [
      ("faction_accept",[],"Accept!",
       [(str_store_troop_name,s1,"$g_invite_faction_lord"),
        (setup_quest_text,"qst_join_faction"),

        (str_store_troop_name_link, s3, "$g_invite_faction_lord"),
        (str_store_faction_name_link, s4, "$g_invite_faction"),
        (quest_set_slot, "qst_join_faction", slot_quest_giver_troop, "$g_invite_faction_lord"),
        (quest_set_slot, "qst_join_faction", slot_quest_expiration_days, 30),
        ##diplomacy start+ fix gender of pronoun
        (str_store_string, s2, "@Find and speak with {s3} of {s4} to give {reg4?her:him} your oath of homage."),
        ##diplomacy end+
        (call_script, "script_start_quest", "qst_join_faction", "$g_invite_faction_lord"),
        (call_script, "script_report_quest_troop_positions", "qst_join_faction", "$g_invite_faction_lord", 3),
        (jump_to_menu, "mnu_invite_player_to_faction_accepted"),
        ]),
      ("faction_reject",[],"Decline the invitation.",
       [(call_script, "script_change_player_relation_with_troop", "$g_invite_faction_lord", -3),
        (assign, "$g_invite_faction", 0),
        (assign, "$g_invite_faction_lord", 0),
        (assign, "$g_invite_offered_center", 0),
        (change_screen_return),
        ]),
     ]
  )
]
