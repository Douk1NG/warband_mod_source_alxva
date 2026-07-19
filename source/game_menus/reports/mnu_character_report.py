# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

character_report_menu = [
("character_report",0,
   "{s9}",
   "none",
   [(try_begin),
      (gt, "$g_player_reading_book", 0),
      (player_has_item, "$g_player_reading_book"),
      (str_store_item_name, s8, "$g_player_reading_book"),
      (str_store_string, s9, "@You are currently reading {s8}."),
    (else_try),
      (assign, "$g_player_reading_book", 0),
      (str_store_string, s9, "@You are not reading any books."),
    (try_end),
    (assign, ":num_friends", 0),
    (assign, ":num_enemies", 0),
    (str_store_string, s6, "str_dplmc_none"),
    (str_store_string, s8, "str_dplmc_none"),
    (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive_pretender),
	  (call_script, "script_troop_get_player_relation", ":troop_no"),
      (assign, ":player_relation", reg0),
      #(troop_get_slot, ":player_relation", ":troop_no", slot_troop_player_relation),
      (try_begin),
        (gt, ":player_relation", 20),
        (try_begin),
          (eq, ":num_friends", 0),
          (str_store_troop_name, s8, ":troop_no"),
        (else_try),
          (eq, ":num_friends", 1),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_troop_name, s7, ":troop_no"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
        (val_add, ":num_friends", 1),
      (else_try),
        (lt, ":player_relation", -20),
        (try_begin),
          (eq, ":num_enemies", 0),
          (str_store_troop_name, s6, ":troop_no"),
        (else_try),
          (eq, ":num_enemies", 1),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{s5} and {s6}"),
        (else_try),
          (str_store_troop_name, s5, ":troop_no"),
          (str_store_string, s6, "@{!}{s5}, {s6}"),
        (try_end),
        (val_add, ":num_enemies", 1),
      (try_end),
    (try_end),

	#lord recruitment changes begin
	(str_clear, s12),
	(try_begin),
		(gt, "$player_right_to_rule", 0),
		(assign, reg12, "$player_right_to_rule"),
		(str_store_string, s12, "str__right_to_rule_reg12"),
	(try_end),

	#Sexual Stats
	#(troop_get_slot, reg21, "trp_player", slot_troop_encounters),
	#(troop_get_slot, reg22, "trp_player", slot_troop_assaults),
	#(str_store_string, s9, "@Encounters: {reg21}"),
	#(str_store_string, s9, "@Assaults: {reg22}"),

	(str_clear, s15),
	(try_begin),
		(this_or_next|gt, "$claim_arguments_made", 0),
		(this_or_next|gt, "$ruler_arguments_made", 0),
		(this_or_next|gt, "$victory_arguments_made", 0),
		(this_or_next|gt, "$lords_arguments_made", 0),
		(eq, 1, 0),

		(assign, reg3, "$claim_arguments_made"),
		(assign, reg4, "$ruler_arguments_made"),
		(assign, reg5, "$victory_arguments_made"),
		(assign, reg6, "$lords_arguments_made"),
		(assign, reg7, "$benefit_arguments_made"),

		(str_store_string, s15, "str_political_arguments_made_legality_reg3_rights_of_lords_reg4_unificationpeace_reg5_rights_of_commons_reg6_fief_pledges_reg7"),
	(try_end),

	#lord recruitment changes begin

    (assign, reg3, "$player_honor"),
    (troop_get_slot, reg2, "trp_player", slot_troop_renown),

    (str_store_string, s9, "str_renown_reg2_honour_rating_reg3s12_friends_s8_enemies_s6_s9"),

    (call_script, "script_get_number_of_hero_centers", "trp_player"),
    (assign, ":no_centers", reg0),
    (try_begin),
      (gt, ":no_centers", 0),
      (try_for_range, ":i_center", 0, ":no_centers"),
        (call_script, "script_troop_get_leaded_center_with_index", "trp_player", ":i_center"),
        (assign, ":cur_center", reg0),
        (try_begin),
          (eq, ":i_center", 0),
          (str_store_party_name, s8, ":cur_center"),
        (else_try),
          (eq, ":i_center", 1),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{s7} and {s8}"),
        (else_try),
          (str_store_party_name, s7, ":cur_center"),
          (str_store_string, s8, "@{!}{s7}, {s8}"),
        (try_end),
      (try_end),
      (str_store_string, s9, "@Your estates are: {s8}.^{s9}"),
    (try_end),
    (try_begin),
      (gt, "$players_kingdom", 0),

      (str_store_faction_name, s8, "$players_kingdom"),
      (try_begin),
	  ##diplomacy start+ Handle player is co-ruler of NPC faction
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),
	  (else_try),
	  ##diplomacy end+
        (this_or_next|is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
        (neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
        #(str_store_string, s9, "@You are a lord of {s8}.^{s9}"),
        (str_store_string, s9, "str_you_are_a_lord_lady_of_s8_s9"),
      (else_try),
        (str_store_string, s9, "str_you_are_king_queen_of_s8_s9"),
      (try_end),

    (try_end),
    ],
    [

	#lord recruitment changes begin

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase Right to Rule",
       [
	   (val_add, "$player_right_to_rule", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),


	("continue",[(eq,"$cheat_mode",1),
		(str_store_troop_name, s14, "$g_talk_troop"),
	],"{!}CHEAT! - increase your relation with {s14}",
       [
	   (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("cheat_slots",[(eq,"$cheat_mode",1),
        (str_store_troop_name, s14, "$g_talk_troop"),
	],"{!}CHEAT! - Access {s14} troop slots",
       [
	   # (assign, "$g_talk_troop", "trp_player"),
	   (jump_to_menu, "mnu_display_troop_slots"),
       ]
       ),



	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase honor",
       [
	   (val_add, "$player_honor", 10),
	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase renown",
       [
	   (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
	   (val_add, ":renown", 50),
	   (troop_set_slot, "trp_player", slot_troop_renown, ":renown"),

	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[(eq,"$cheat_mode",1)],"{!}CHEAT! - increase persuasion",
       [
	   (troop_raise_skill, "trp_player", "skl_persuasion", 1),

	   (jump_to_menu, "mnu_character_report"),
       ]
       ),

	("continue",[],"Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),

	#lord recruitment changes end

	   ]
  )
]
