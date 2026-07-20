# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

kingdom_army_quest_report_to_army_menu = [
(
##diplomacy end+ fix gender of pronoun
    "kingdom_army_quest_report_to_army",mnf_scale_picture,
    "{s8} sends word that {reg4?she:he} wishes you to join {reg4?her:his} new military campaign.\
 You need to bring at least {reg13} troops to the army,\
 and are instructed to raise more men with all due haste if you do not have enough.",
##diplomacy end+
    "none",
    [
        (set_background_mesh, "mesh_pic_messenger"),
        (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
        (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
        (call_script, "script_get_information_about_troops_position", ":quest_target_troop", 0),
        (str_clear, s9),
        (try_begin),
          (eq, reg0, 1), #troop is found and text is correct
          (str_store_string, s9, s1),
        (try_end),
        (str_store_troop_name, s8, ":quest_target_troop"),
        (assign, reg13, ":quest_target_amount"),
		##diplomacy start+
      #Set gender with script
		#(troop_get_type, reg4, ":quest_target_troop"), #<- OLD
		(call_script, "script_dplmc_store_troop_is_female_reg", ":quest_target_troop", 4),
		##diplomacy end+
      ],
    [
      ("continue",[],"Continue...",
       [
           (quest_get_slot, ":quest_target_troop", "qst_report_to_army", slot_quest_target_troop),
           (quest_get_slot, ":quest_target_amount", "qst_report_to_army", slot_quest_target_amount),
           (str_store_troop_name_link, s13, ":quest_target_troop"),
           (assign, reg13, ":quest_target_amount"),
           (setup_quest_text, "qst_report_to_army"),
           ##diplomacy start+ fix gender of pronoun
           (str_store_string, s2, "@{s13} asked you to report to {reg4?her:him} with at least {reg13} troops."),
           ##diplomacy end+
           (call_script, "script_start_quest", "qst_report_to_army", ":quest_target_troop"),
           (call_script, "script_report_quest_troop_positions", "qst_report_to_army", ":quest_target_troop", 3),
           (change_screen_return),
        ]),
     ]
  )
]
