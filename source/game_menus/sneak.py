# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

sneak_menus = [
  (
    "sneak_into_town_suceeded",0,
    "Disguised in the garments of a poor {reg1?cheater:{s1}}, you fool the guards and make your way into the town.",
    "none",
    [(assign, reg1, "$cheat_mode"),
     (call_script, "script_get_disguise_string", "$sneaked_into_town", 1),

     # (try_begin),
       # (eq, "$sneaked_into_town", disguise_pilgrim),
       # (assign, ":string", "str_pilgrim_disguise"),
     # (try_end),
    ],
    [
      ("continue",[],"Continue...",
       [
           # (assign, "$sneaked_into_town",1),
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  ),
  (
    "sneak_into_town_caught",0,
    "As you try to sneak in, one of the guards recognizes you and raises the alarm!\
 You must flee back through the gates before all the guards in the town come down on you!",
    "none",
    [
       (assign,"$auto_menu","mnu_captivity_start_castle_surrender"),
    ],
    [
      ("sneak_caught_fight",[],"Try to fight your way out!",
       [
           (assign,"$all_doors_locked",1),
           (party_get_slot, ":sneak_scene", "$current_town", slot_town_center), # slot_town_gate),
           (modify_visitors_at_site,":sneak_scene"),
           (reset_visitors),

           (set_jump_mission, "mt_sneak_caught_fight"),

           (try_begin),
             (this_or_next|eq, "$talk_context", tc_escape),
             (eq, "$talk_context", tc_prison_break),
             (assign, ":entry_no", 7),
           (else_try),
             (party_slot_eq, "$current_town", slot_party_type, spt_town),
             #(set_visitor,0,"trp_player"),
             (assign, ":entry_no", 0),
           (else_try),
             #(set_visitor,1,"trp_player"),
             (assign, ":entry_no", 1),
           (try_end),

           (try_begin),
             (gt, "$sneaked_into_town", disguise_none), #setup disguise
             (assign, ":override_state", af_override_everything),
             (mission_tpl_entry_set_override_flags, "mt_sneak_caught_fight", ":entry_no", ":override_state"),
                        #SB : script call to assign correct disguise, with weapons
             (call_script, "script_set_disguise_override_items", "mt_sneak_caught_fight", ":entry_no", 1),
           (try_end),

           (set_jump_entry, ":entry_no"),

           #(store_faction_of_party, ":town_faction","$current_town"),
           #(faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
           #(faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
           #(try_begin),
           #  (gt, ":tier_2_troop", 0),
           #  (gt, ":tier_3_troop", 0),
           #  (assign,reg0,":tier_3_troop"),
           #  (assign,reg1,":tier_3_troop"),
           #  (assign,reg2,":tier_2_troop"),
           #  (assign,reg3,":tier_2_troop"),
           #(else_try),
           #  (assign,reg0,"trp_swadian_skirmisher"),
           #  (assign,reg1,"trp_swadian_crossbowman"),
           #  (assign,reg2,"trp_swadian_infantry"),
           #  (assign,reg3,"trp_swadian_crossbowman"),
           #(try_end),
           #(assign,reg4,-1),
           #(shuffle_range,0,5),
           #(set_visitor,2,reg0),
           #(set_visitor,3,reg1),
           #(set_visitor,4,reg2),
           #(set_visitor,5,reg3),


           #(set_jump_mission, "mt_sneak_caught_fight"),
           (set_passage_menu, "mnu_town"),
           (jump_to_scene,":sneak_scene"),
           (change_screen_mission),
        ]),
      ("sneak_caught_surrender",[],"Surrender.",
       [
           (jump_to_menu,"mnu_captivity_start_castle_surrender"),
        ]),
    ]
  ),
  (
    "sneak_into_town_caught_dispersed_guards",0,
    "You drive off the guards and cover your trail before running off, easily losing your pursuers in the maze of streets.",
    "none",
    [],
    [
      ("continue",[],"Continue...",
       [
           (try_begin),
               (eq, "$sneaked_into_town", 0),
               (assign, "$sneaked_into_town",1),
           (try_end),

           (assign, "$town_entered", 1),
           #(assign, "$g_mt_mode", tcm_disguised),
           (jump_to_menu,"mnu_town"),
        ]),
    ]
  ),
  (
    "sneak_into_town_caught_ran_away",0,
    "You make your way back through the gates and quickly retreat to the safety of the countryside.{s11}",
    "none",
    [

	(str_clear, s11),
	(assign, ":at_least_one_escaper_caught", 0),

	(assign, ":end_cond", kingdom_ladies_end),
	(try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
	  (try_begin),
        (troop_slot_eq, ":prisoner", slot_troop_mission_participation, mp_prison_break_escaped),
        (assign, "$talk_context", tc_hero_freed),
        (assign, reg14, ":prisoner"),
        (call_script, "script_setup_troop_meeting", ":prisoner", -1),
        (troop_set_slot, ":prisoner", slot_troop_mission_participation, -1),

        (troop_get_slot, ":prison_center", ":prisoner", slot_troop_prisoner_of_party),
        (party_remove_prisoners, ":prison_center", ":prisoner", 1),
        (troop_set_slot, ":prisoner", slot_troop_prisoner_of_party, -1),

        (assign, ":end_cond", -1), #maybe more than 1 should be able to escape?
	  (else_try),
		(troop_slot_eq, ":prisoner", slot_troop_mission_participation, mp_prison_break_caught),
		(str_store_troop_name, s12, ":prisoner"),
		(try_begin),
			(eq, ":at_least_one_escaper_caught", 0),
			(str_store_string, s11, "str_s11_unfortunately_s12_was_wounded_and_had_to_be_left_behind"),
		(else_try),
			(str_store_string, s11, "str_s11_also_s12_was_wounded_and_had_to_be_left_behind"),
		(try_end),
		(assign, ":at_least_one_escaper_caught", 1),
	  (try_end),

	  (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new
	(try_end),
	],
    [
      ("continue",[],"Continue...",
       [
           (assign,"$auto_menu",-1),
           (store_encountered_party,"$last_sneak_attempt_town"),
           (store_current_hours,"$last_sneak_attempt_time"),
           (change_screen_return),
        ]),
    ]
  ),
]
