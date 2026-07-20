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

player_leave_faction_scripts = [
#script_player_leave_faction
# INPUT: arg1 = give_back_fiefs
# OUTPUT: none
("player_leave_faction",
    [
      (store_script_param, ":give_back_fiefs", 1),

      (call_script, "script_check_and_finish_active_army_quests_for_faction", "$players_kingdom"),
      (assign, ":old_kingdom", "$players_kingdom"),
      (assign, ":old_has_homage", "$player_has_homage"),
      (assign, "$players_kingdom", 0),
      (assign, "$player_has_homage", 0),

      (try_begin),
        (neq, ":give_back_fiefs", 0), #ie, give back fiefs = 1, thereby do it
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          ##diplomacy begin
          #native bug fix when giving back fiefs
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_neutral"),
          ##diplomacy end
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),

          #The following line also occurs when a lord is stripped of his fiefs by an indictment
          (party_set_slot, ":cur_center", slot_town_lord, stl_unassigned),
        (try_end),
      (else_try),
        #If you retain the fiefs
        (try_for_range, ":cur_center", centers_begin, centers_end),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", "fac_player_supporters_faction"),
          (party_set_slot, ":cur_center", slot_town_lord, "trp_player"),
          (troop_get_slot, ":cur_banner", "trp_player", slot_troop_banner_scene_prop),
          #custom_banner_begin
          (try_begin),
              (gt, ":cur_banner", 0),
              (val_sub, ":cur_banner", banner_scene_props_begin),
              (val_add, ":cur_banner", banner_map_icons_begin),
              (party_set_banner_icon, ":cur_center", ":cur_banner"),
          (else_try),
            (eq, ":cur_banner", -1),
            (troop_get_slot, ":flag_icon", "trp_player", slot_troop_custom_banner_map_flag_type),
            (try_begin),
               (ge, ":flag_icon", 0),
               (val_add, ":flag_icon", custom_banner_map_icons_begin),
               (party_set_banner_icon, ":cur_center", ":flag_icon"),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":cur_center", villages_begin, villages_end),
          (party_get_slot, ":cur_bound_center", ":cur_center", slot_village_bound_center),
          (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
          (neg|party_slot_eq, ":cur_bound_center", slot_town_lord, "trp_player"),
          (call_script, "script_give_center_to_faction", ":cur_center", ":old_kingdom"),
        (try_end),

        (is_between, ":old_kingdom", kingdoms_begin, kingdoms_end),
        (neq, ":old_kingdom", "fac_player_supporters_faction"),
        (store_relation, ":reln", "fac_player_supporters_faction", ":old_kingdom"),
        (store_sub, ":req_dif", -40, ":reln"),
        (call_script, "script_change_player_relation_with_faction", ":old_kingdom", ":req_dif"),
      (try_end),

      (try_begin),
        (eq, ":old_has_homage", 1),
        (faction_get_slot, ":faction_leader", ":old_kingdom", slot_faction_leader),
        (call_script, "script_change_player_relation_with_troop", ":faction_leader", -20),
      (try_end),

      (try_begin),
        (troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
        (is_between, ":spouse", kingdom_ladies_begin, kingdom_ladies_end),

        (try_begin),
            (ge, "$cheat_mode", 1),
            (str_store_troop_name, s4, ":spouse"),
            (display_message, "@{!}DEBUG - {s4} faction changed by marriage, case 3"),
        (try_end),


        (troop_set_faction, ":spouse", "fac_player_supporters_faction"),
        (call_script, "script_troop_set_title_according_to_faction", ":spouse", "fac_player_supporters_faction"),
      (try_end),

      #Change relations with players_kingdom when player changes factions
      (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
        (neq, ":kingdom", "fac_player_supporters_faction"),
        (store_relation, ":relation_with_old_faction", ":old_kingdom", ":kingdom"),
        (store_relation, ":relation_with_player_faction", "fac_player_faction", ":kingdom"),

        (try_begin),
          (eq, ":old_kingdom", ":kingdom"),
          (val_min, ":relation_with_player_faction", 0),
        (else_try),
          (lt, ":relation_with_old_faction", 0),
          (val_max, ":relation_with_player_faction", 0),
       ##diplomacy start+ do not retain allies of former kingdom
       (else_try),
         (gt, ":relation_with_old_faction", 0),
         (val_min, ":relation_with_player_faction", 0),
       ##diplomacy end+
        (try_end),
        (set_relation, "fac_player_faction", ":kingdom", ":relation_with_player_faction"),
        (set_relation, "fac_player_supporters_faction", ":kingdom", ":relation_with_player_faction"),
      (try_end),

      (call_script, "script_update_all_notes"),
      (assign, "$g_recalculate_ais", 1),

        ##diplomacy begin
        ##disband player patrols
      #SB : build one string instead of one for each party
      (try_begin),
        (str_clear, s6),
        (assign, ":num_parties", 0),
        # (ge, ":give_back_fiefs", 1),
        (try_for_parties, ":party_no"),
          (party_is_active, ":party_no"),
          (party_slot_eq,":party_no", slot_party_type, spt_patrol),
          #SB : add other checks such as faction and home center ownership
          (store_faction_of_party, ":party_faction", ":party_no"),
          (eq, ":party_faction", ":old_kingdom"),
          (party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
          # (party_slot_eq, ":home_center", slot_town_lord, "trp_player"), #this may no longer be true

          #build string
          (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
          (str_store_party_name, s50, ":target_party"),
          (try_begin),
            (eq, ":num_parties", 0),
            (str_store_string_reg, s51, s50),
          (else_try),
            (eq, ":num_parties", 1),
            (str_store_string, s51, "str_s50_and_s51"),
          (else_try),
            (str_store_string, s51, "str_s50_comma_s51"),
          (try_end),
          # (display_log_message, "@Your soldiers patrolling {s6} disbanded because you left the faction!", message_defeated),
          (try_begin), #do not give back fiefs, keep the patrols
            (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
            # (eq, ":give_back_fiefs", 0),
            (party_get_slot, ":town_lord", ":home_center", slot_town_lord),
            (eq, ":town_lord", "trp_player"),
            (party_set_faction, ":party_no", "fac_player_supporters_faction"),
            # (remove_party, ":party_no"),
          (else_try), #we assume ":give_back_fiefs" also returns patrols
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":town_lord"),
            (party_set_faction, ":party_no", ":old_kingdom"),
            (party_set_flags, ":party_no", pf_default_behavior,1),
          (try_end),
        (try_end),
        (try_begin),
          (gt, ":num_parties", 0),
          (faction_get_color, ":color", ":old_kingdom"),
          (assign, reg6, ":give_back_fiefs"),
          (display_log_message, "@Your soldiers patrolling {s51} {reg6?returned:disbanded} because you left the faction!", ":color"),
        (try_end),
      (try_end),
        ##diplomacy end
    ])
]
