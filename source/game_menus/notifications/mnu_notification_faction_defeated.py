# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

notification_faction_defeated_menu = [
(
    "notification_faction_defeated",0,
    "Faction Eliminated^^{s1} is no more!",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", npc_kingdoms_begin, kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue",[],"Continue...",
       [
         (try_begin),
           (is_between, "$supported_pretender", pretenders_begin, pretenders_end),
           (troop_slot_eq, "$supported_pretender", slot_troop_original_faction, "$g_notification_menu_var1"),

           #All rebels switch to kingdom
           (try_for_range, ":cur_troop", heroes_begin, heroes_end),
             (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_lady),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (troop_set_faction, ":cur_troop", "$g_notification_menu_var1"),
             (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", "$g_notification_menu_var1"),
             (try_begin),
               (this_or_next|eq, "$g_notification_menu_var1", "$players_kingdom"),
               (eq, "$g_notification_menu_var1", "fac_player_supporters_faction"),
               (call_script, "script_check_concilio_calradi_achievement"),
             (try_end),
           (else_try), #all loyal lords gain a small bonus with the player
             (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "$g_notification_menu_var1"),
             (call_script, "script_troop_change_relation_with_troop", ":cur_troop", "trp_player", 5),
           (try_end),
           ###(((rebels_switch FIX
           (try_for_range, ":cur_troop", kingdom_ladies_begin, kingdom_ladies_end),
             (store_troop_faction, ":cur_faction", ":cur_troop"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (troop_set_faction, ":cur_troop", "$g_notification_menu_var1"),
             (call_script, "script_troop_set_title_according_to_faction", ":cur_troop", "$g_notification_menu_var1"),
           (try_end),
           ###)))

           (try_for_parties, ":cur_party"),
             (store_faction_of_party, ":cur_faction", ":cur_party"),
             (eq, ":cur_faction", "fac_player_supporters_faction"),
             (party_set_faction, ":cur_party", "$g_notification_menu_var1"),
           (try_end),

           (assign, "$players_kingdom", "$g_notification_menu_var1"),
           (try_begin),
            (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
            (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),
            (troop_set_faction, ":spouse", "$g_notification_menu_var1"),
           (try_end),


           (call_script, "script_add_notification_menu", "mnu_notification_rebels_switched_to_faction", "$g_notification_menu_var1", "$supported_pretender"),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_state, sfs_active),
           (faction_set_slot, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),

           (faction_get_slot, ":old_leader", "$g_notification_menu_var1", slot_faction_leader),
           #(troop_set_slot, ":old_leader", slot_troop_change_to_faction, "fac_commoners"),
           (call_script, "script_change_troop_faction", ":old_leader", "fac_commoners"), #dckplmc - prevent possible respawn before actual faction changes
           #SB : renown loss of under 25%
           (troop_get_slot, ":old_renown", ":old_leader", slot_troop_renown),
           (store_random_in_range, ":renown_loss", 10, 25),
           (val_mul, ":renown_loss", ":old_renown"),
           (val_div, ":renown_loss", 100),
           (val_sub, ":old_renown", ":renown_loss"),
           (troop_set_slot, ":old_leader", slot_troop_renown, ":old_renown"),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_leader, "$supported_pretender"),
           (troop_set_faction, "$supported_pretender", "$g_notification_menu_var1"),

           (faction_get_slot, ":old_marshall", "$g_notification_menu_var1", slot_faction_marshall),
           (try_begin),
             (ge, ":old_marshall", 0),
             (troop_get_slot, ":old_marshall_party", ":old_marshall", slot_troop_leaded_party),
             (party_is_active, ":old_marshall_party"),
             (party_set_marshal, ":old_marshall_party", 0),
           (try_end),

           (faction_set_slot, "$g_notification_menu_var1", slot_faction_marshall, "trp_player"),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_state, sfai_default),
           (faction_set_slot, "$g_notification_menu_var1", slot_faction_ai_object, -1),
           (troop_set_slot, "$supported_pretender", slot_troop_occupation, slto_kingdom_hero),
           (call_script, "script_change_troop_renown", "$supported_pretender", 1000), #SB : keep existing renown
           (val_div, ":renown_loss", 2), #and add to it half of what old king lost
           (call_script, "script_change_troop_renown", "$supported_pretender", ":renown_loss"),
           # (troop_set_slot, "$supported_pretender", slot_troop_renown, 1000),

           (party_remove_members, "p_main_party", "$supported_pretender", 1),
           (call_script, "script_troop_set_title_according_to_faction", "$supported_pretender", "$g_notification_menu_var1"),
           (troop_set_auto_equip, "$supported_pretender",1), #SB : diplomacy suggestion: claimants
           (call_script, "script_set_player_relation_with_faction", "$g_notification_menu_var1", 12), #dckplmc
           (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
             (neq, ":cur_kingdom", "$g_notification_menu_var1"),
             (store_relation, ":reln", ":cur_kingdom", "fac_player_supporters_faction"),
             (set_relation, ":cur_kingdom", "$g_notification_menu_var1", ":reln"),
           (try_end),
           (assign, "$supported_pretender", 0),
           (assign, "$supported_pretender_old_faction", 0),
           (assign, "$g_recalculate_ais", 1),
           (call_script, "script_update_all_notes"),
         (try_end),
         (change_screen_return),
        ]),
     ]
  )
]
