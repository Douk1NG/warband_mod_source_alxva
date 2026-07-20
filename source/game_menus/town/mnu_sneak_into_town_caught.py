# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

sneak_into_town_caught_menu = [
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
  )
]
