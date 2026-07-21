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

game_get_center_note_scripts = [
#script_game_get_item_buy_price_factor:
# This script is called from the game engine when the notes of a center is needed.
# INPUT: arg1 = center_no, arg2 = note_index
# OUTPUT: s0 = note
("game_get_center_note",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":note_index"),

      (set_trigger_result, 0),
      (try_begin),
        (eq, ":note_index", 0),
        (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
        (try_begin),
          (ge, ":lord_troop", 0),
          (store_troop_faction, ":lord_faction", ":lord_troop"),
          (str_store_troop_name_link, s1, ":lord_troop"),
          (try_begin),
            (eq, ":lord_troop", "trp_player"),
            (gt, "$players_kingdom", 0),
            (str_store_faction_name_link, s2, "$players_kingdom"),
          (else_try),
            (str_store_faction_name_link, s2, ":lord_faction"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          ##diplomacy start+ Show when the city is the home of a lord or is a court
          (assign, ":bound_center", reg0),#Save reg0 to avoid having it randomly change
          (try_begin),
             (eq, "$g_player_court", ":center_no"),

             (store_and, reg1, "$players_kingdom_name_set", rename_center), #SB : specify capitals
             (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is {reg1?your capital:where you make your court}.^"),
          (else_try),
             (neq, ":lord_troop", "trp_player"),
             (neg|is_between, ":center_no", villages_begin, villages_end),
             (call_script, "script_lord_get_home_center", ":lord_troop"),
             (eq, reg0, ":center_no"),
             (call_script, "script_dplmc_get_troop_standing_in_faction", ":lord_troop", ":lord_faction"),
             (try_begin),
                (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} court.^"),
             (else_try),
                (call_script, "script_dplmc_store_troop_is_female", ":lord_troop"),
                (str_store_string, s2, "@{s51} belongs to {s1} of {s2}, and is where {reg0?she:he} makes {reg0?her:his} home.^"),
             (try_end),
          (else_try),#Fall through to normal behavior
          ##diplomacy end+
          (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
          ##diplomacy start+
          (try_end),
          (assign, reg0, ":bound_center"),#Revert reg0 to avoid having it randomly change
          ##diplomacy end+
        (else_try),
          (str_clear, s2),
          ##diplomacy start+ Don't hide notes for centers with no lords.
          (store_faction_of_party, ":lord_faction", ":center_no"),
          (str_store_string, s1, "str_noone"),
          (try_begin),
             (ge, ":lord_faction", 1),
             (str_store_faction_name_link, s2, ":lord_faction"),
          (else_try),
             (str_store_string, s2, "str_noone"),
          (try_end),
          (str_store_party_name, s50, ":center_no"),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (str_store_string, s51, "@The town of {s50}"),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
            (str_store_party_name_link, s52, ":bound_center"),
            (str_store_string, s51, "@The village of {s50} near {s52}"),
          (else_try),
            (str_store_string, s51, "@{!}{s50}"),
          (try_end),
          (try_begin),
             (is_between, ":lord_faction", kingdoms_begin, kingdoms_end),
             (faction_slot_eq, ":lord_faction", slot_faction_state, sfs_active),
             (str_store_string, s2, "@{s51} belongs to {s2} but has not yet been granted to a lord.^"),
          (else_try),
             (str_store_string, s2, "@{s51} belongs to {s2}.^"),
          (try_end),
          ##diplomacy end+
        (try_end),
        (try_begin),
          (is_between, ":center_no", villages_begin, villages_end),
          ##diplomacy start+ Show market town if it differs from the bound center
          (party_get_slot, ":market_center", ":center_no", slot_village_market_town),
          (try_begin),
             (is_between, ":market_center", centers_begin, centers_end),
             (neq, ":market_center", ":center_no"),
             (neg|party_slot_eq, ":center_no", slot_village_bound_center, ":market_center"),
             (str_store_party_name_link, s8, ":market_center"),
             (str_store_string, s2, "@{s2}Its market town is {s8}.^"),
          (try_end),
          ##diplomacy end+
        (else_try),
          (assign, ":num_villages", 0),
          (try_for_range_backwards, ":village_no", villages_begin, villages_end),
            (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
            (try_begin),
              (eq, ":num_villages", 0),
              (str_store_party_name_link, s8, ":village_no"),
            (else_try),
              (eq, ":num_villages", 1),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{s7} and {s8}"),
            (else_try),
              (str_store_party_name_link, s7, ":village_no"),
              (str_store_string, s8, "@{!}{s7}, {s8}"),
            (try_end),
            (val_add, ":num_villages", 1),
          (try_end),
          (try_begin),
            (eq, ":num_villages", 0),
            (str_store_string, s2, "@{s2}It has no villages.^"),
          (else_try),
            (store_sub, reg0, ":num_villages", 1),
            (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
          (try_end),
        (try_end),
        (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
        #(party_get_slot, reg7, ":center_no", slot_town_prosperity),
        (str_store_string, s0, "@{s2}Its prosperity is: {s50}", 0),

        (set_trigger_result, 1),
      (try_end),
     ])
]
