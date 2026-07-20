# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

arena_duel_fight_menu = [
("arena_duel_fight",0,
   "You and your opponent prepare to duel.",
   "none",
   [
      (troop_get_slot, ":leader_troop_faction", "$g_duel_troop", slot_troop_original_faction),
      (try_begin),
        (eq, ":leader_troop_faction", fac_kingdom_1),
        (set_background_mesh, "mesh_pic_swad"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_2),
        (set_background_mesh, "mesh_pic_vaegir"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_3),
        (set_background_mesh, "mesh_pic_khergit"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_4),
        (set_background_mesh, "mesh_pic_nord"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_5),
        (set_background_mesh, "mesh_pic_rhodock"),
      (else_try),
        (eq, ":leader_troop_faction", fac_kingdom_6),
        (set_background_mesh, "mesh_pic_sarranid_encounter"),
      (try_end),
   ],
   [
     ("continue",[],"Continue...",
      [
        (assign, "$g_leave_encounter", 0),
        (assign, ":closest_town", "$g_encountered_party"),

        #restructure this to take into account $g_start_arena_fight_at_nearest_town
        (try_begin), #check if the parameter is necessary
          (neg|is_between, ":closest_town", walled_centers_begin, walled_centers_end),
          (is_between, "$g_start_arena_fight_at_nearest_town", walled_centers_begin, walled_centers_end),
          (assign, ":closest_town", "$g_start_arena_fight_at_nearest_town"),
          (assign, "$g_start_arena_fight_at_nearest_town", 0),
        (try_end),

        (try_begin),
          (is_between, ":closest_town", towns_begin, towns_end),
          (party_get_slot, ":duel_scene", ":closest_town", slot_town_arena),
        (else_try), #SB : duels at castle arena
          (is_between, ":closest_town", castles_begin, castles_end),
          (party_get_slot, ":duel_scene", ":closest_town", slot_castle_exterior),
        (else_try),
          (party_get_current_terrain, ":terrain", "p_main_party"),
          (eq, ":terrain", rt_snow),
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_3"),
        (else_try),
          (this_or_next|eq, ":terrain", rt_desert),
          (eq, ":terrain", rt_steppe), #this is the actual steppe scene
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_4"),
        (else_try),
          (assign, ":duel_scene", "scn_training_ground_ranged_melee_1"),
        (try_end),
        (modify_visitors_at_site, ":duel_scene"),
        (reset_visitors),
        # (set_visitor, 0, "trp_player"),
        # (set_visitor, 1, "$g_duel_troop"),
        (troop_set_slot, "trp_tournament_participants", 0, "trp_player"),
        (troop_set_slot, "trp_tournament_participants", 1, "$g_duel_troop"),
        (set_jump_mission, "mt_duel_with_lord"),
        #SB : check relative standing, 0 = (higher renown)
        (try_begin),
          (troop_is_hero, "$g_duel_troop"),
          (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
          (troop_slot_ge, "$g_duel_troop", slot_troop_renown, ":player_renown"),
          #swap positions
          (troop_set_slot, "trp_tournament_participants", 1, "trp_player"),
          (troop_set_slot, "trp_tournament_participants", 0, "$g_duel_troop"),
        (try_end),
        #SB : set up additional equipment, do not always use sword_medieval_a
        (troop_get_slot, ":faction", "$g_duel_troop", slot_troop_original_faction),
        (try_begin),
          (this_or_next|eq, ":faction", "fac_kingdom_1"),
          (eq, ":faction", "fac_kingdom_5"),
          (store_random_in_range, ":weapon", "itm_sword_medieval_a", "itm_sword_viking_1"),
        (else_try),
          (eq, ":faction", "fac_kingdom_3"),
          (assign, ":weapon", "itm_sword_khergit_1"),
        (else_try),
          (this_or_next|eq, ":faction", "fac_kingdom_2"),
          (eq, ":faction", "fac_kingdom_4"),
          (store_random_in_range, ":weapon", "itm_sword_viking_1", "itm_sword_viking_3_small"),
        # (else_try),
          # (eq, ":faction", "fac_kingdom_5"), #no requirement
          # (assign, ":weapon", "itm_military_cleaver_b"),
        (else_try),
          (eq, ":faction", "fac_kingdom_6"),
          (assign, ":weapon", "itm_scimitar"),
        (else_try),
          (assign, ":weapon", "itm_arena_sword"),
        (try_end),

        (try_for_range, ":cur_entry_point", 0, 2),
          (troop_get_slot, ":cur_troop", "trp_tournament_participants", ":cur_entry_point"),
          (try_begin), #within the courtyard, 23/24 is guard entry
            (is_between, ":closest_town", castles_begin, castles_end),
            (val_add, ":cur_entry_point", 2), #to use the new mission template entries 3 & 4
          (try_end),

          (mission_tpl_entry_clear_override_items, "mt_duel_with_lord", ":cur_entry_point"),
          #weapon, make sure they have no difficulty requirement
          (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":weapon"),
          # (item_get_type, ":type", ":weapon"),
          # (try_begin),
            # (is_between, ":type", itp_type_pistol, itp_type_bullets),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_cartridges2"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_dagger"),#backup
          # (else_try),
            # (eq, ":type", itp_type_crossbow),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_practice_bolts_9_amount"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_estoc"),#backup
          # (else_try),
            # (eq, ":type", itp_type_bow),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", "itm_practice_arrows_10_amount"),
            # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":backup"),#backup
          # (try_end),

          #armor, they're statistically almost the same
          # (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
          # (val_min, ":renown", 2000),
          # (store_div, ":armor", ":renown", 500),#0 to 3
          # (val_add, ":armor", "itm_heraldic_mail_with_surcoat"),
          # (mission_tpl_entry_add_override_item, "mt_duel_with_lord", ":cur_entry_point", ":armor"),

          (set_visitor, ":cur_entry_point", ":cur_troop"),
        (try_end),

        (jump_to_scene, ":duel_scene"),
        (jump_to_menu, "mnu_arena_duel_conclusion"),
        (change_screen_mission),
      ]),
    ]
  )
]
