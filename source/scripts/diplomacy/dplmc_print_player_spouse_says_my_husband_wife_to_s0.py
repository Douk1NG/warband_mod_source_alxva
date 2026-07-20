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

dplmc_print_player_spouse_says_my_husband_wife_to_s0_scripts = [
# "script_dplmc_prepare_hero_center_points_ignoring_center"
#
#INPUT:
#  arg1: troop_no
#  arg2: whether the first letter must be capitalized
#
#OUTPUT:
#    s0: a string that can be substituted for "my {husband/wife}" or "my love"
("dplmc_print_player_spouse_says_my_husband_wife_to_s0",
   [
     (store_script_param_1, ":troop_no"),
     (store_script_param_2, ":capitalized"),

 	 (assign, ":save_reg0", reg0),
	 (assign, ":save_reg6", reg6),
	 (assign, ":save_reg7", reg7),
	 #(assign, reg6, ":capitalized"),
	 (assign, reg7, 0),

    #Base switch is 50 (i.e. where the "brave champion" greeting starts)
    (try_begin),
      (lt, ":troop_no", 1),#bad value
      (assign, reg0, 0),
      (assign, reg6, lrep_none),
    (else_try),
	   (call_script, "script_troop_get_player_relation", ":troop_no"),#write relation to reg0
      (troop_get_slot, reg6, ":troop_no", slot_lord_reputation_type),#write relation to reg6
      (eq, reg6, lrep_conventional),#...jumps to next branch (keeping reg0 and reg6) if this isn't true
		(val_add, reg0, 25),#from 25+
	 (else_try),
      (eq, reg6, lrep_otherworldly),
		(val_add, reg0, 30),#from 20+
	 (else_try),
      (eq, reg6, lrep_moralist),
      (store_sub, reg7, "$player_honor", 10),
      (val_clamp, reg7, -40, 31),
      (val_add, reg0, reg7),
      (assign, reg7, 0),
    (else_try),
      (eq, reg6, lrep_ambitious),
      (assign, reg7, -10),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
            (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
         (val_add, reg7, 10),
         (party_slot_eq, ":center_no", slot_party_type, spt_town),
         (val_add, reg7,  10),
      (try_end),
      (val_clamp, reg7, -10, 30),
      (val_add, reg0, reg7),
      (assign, reg7, 0),
    (else_try),
      (eq, reg6, lrep_adventurous),
      (val_add, reg7, 20),#from 30+
    (else_try),
      (eq, reg6, lrep_none),
      (is_between, reg6, heroes_begin, heroes_end),
      (val_sub, reg0, 20),#from 70+
    (else_try),
      (eq, reg6, lrep_cunning),
      (val_sub, reg0, 20),#from 70+
    (else_try),
      (this_or_next|eq, reg6, lrep_debauched),
      (this_or_next|eq, reg6, lrep_quarrelsome),
      (this_or_next|eq, reg6, lrep_selfrighteous),
      (val_sub, reg0, 30),#from 80+
	 (try_end),

    (try_begin),
       (ge, reg0, 50),
       (assign, reg7, 1),
    (try_end),

    (try_begin),
       #Embellishment: diminuitive pet-names
       (eq, reg6, lrep_debauched),
       (gt, ":troop_no", 0),
       (store_character_level, ":player_level", "trp_player"),
       (store_character_level, ":troop_level", ":troop_no"),
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (this_or_next|ge, ":troop_level", ":player_level"),
       (this_or_next|troop_slot_ge, ":troop_no", slot_troop_renown, ":player_renown"),
          (lt, reg0, 50),
       (assign, reg6, ":capitalized"),#Whether the first letter needs to be upper case
       (str_store_string, s0, "@{reg6?M:m}y poppet"),
    (else_try),
       #The basic idea.  Further embellishments may come.
       (assign, reg6, ":capitalized"),#Whether the first letter needs to be upper case
       (str_store_string, s0, "str_dplmc_reg6my_reg7spouse"),
    (try_end),

	 #Revert registers
	 (assign, reg0, ":save_reg0"),
	 (assign, reg6, ":save_reg6"),
	 (assign, reg7, ":save_reg7"),
   ])
]
