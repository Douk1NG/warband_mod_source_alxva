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

create_kingdom_hero_party_scripts = [
# script_get_percentage_with_randomized_round
# Input: arg1 = troop_no, arg2 = center_no
# Output: $pout_party = party_no
("create_kingdom_hero_party",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),

      (store_troop_faction, ":troop_faction_no", ":troop_no"),

      (assign, "$pout_party", -1),
      (try_begin),
        (eq, "$g_there_is_no_avaliable_centers", 0),
        (set_spawn_radius, 0),
      (else_try),
        (set_spawn_radius, 15),
      (try_end),
      (spawn_around_party, ":center_no", "pt_kingdom_hero_party"),

      (assign, "$pout_party", reg0),

      ###faction icons### dckplmc
      (try_begin),

        (assign, ":icon_faction", ":troop_faction_no"),

        (try_begin),
          (gt, ":troop_faction_no", "fac_commoners"),
          (this_or_next|eq, ":troop_faction_no", "fac_player_faction"),
          (this_or_next|eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (eq, ":troop_faction_no", "$players_kingdom"),
          (neg|is_between, ":troop_faction_no", npc_kingdoms_begin, npc_kingdoms_end),
          (is_between, "$g_player_culture", npc_kingdoms_begin, npc_kingdoms_end),
          (assign, ":icon_faction", "$g_player_culture"),
        (try_end),

          (is_between, ":icon_faction", npc_kingdoms_begin, kingdoms_end),
          (store_sub, ":fac_offset", ":icon_faction", npc_kingdoms_begin),
          (try_begin),
              (faction_slot_eq, ":icon_faction", slot_faction_leader, ":troop_no"),
              (store_add, ":icon", "icon_kingdom_1_king", ":fac_offset"),
              (party_set_icon, "$pout_party", ":icon"),
          (else_try),
              (store_add, ":icon", "icon_kingdom_1_lord", ":fac_offset"),
              (party_set_icon, "$pout_party", ":icon"),
          (try_end),
      (try_end),
      ###

      (party_set_faction, "$pout_party", ":troop_faction_no"),
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_party),
      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
      (str_store_troop_name, s5, ":troop_no"),
      (party_set_name, "$pout_party", "str_s5_s_party"),

      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      #Setting the flag icon
      #normal_banner_begin
      (troop_get_slot, ":cur_banner", ":troop_no", slot_troop_banner_scene_prop),
      (try_begin),
        (gt, ":cur_banner", 0),
        (val_sub, ":cur_banner", banner_scene_props_begin),
        (val_add, ":cur_banner", banner_map_icons_begin),
        (party_set_banner_icon, "$pout_party", ":cur_banner"),
      (else_try),
      #custom_banner_begin
          (eq, ":cur_banner", -1),
          (troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
          (try_begin),
           (ge, ":flag_icon", 0),
           (val_add, ":flag_icon", custom_banner_map_icons_begin),
           (party_set_banner_icon, "$pout_party", ":flag_icon"),
          (try_end),
      (try_end),

      (try_begin),
        #because of below two lines, lords can only hire more than one party_template(stack) at game start once a time during all game.
        (troop_slot_eq, ":troop_no", slot_troop_spawned_before, 0),
        (troop_set_slot, ":troop_no", slot_troop_spawned_before, 1),
        (assign, ":num_tries", 20),
        (try_begin),
          (store_troop_faction, ":troop_kingdom", ":troop_no"),
          (faction_slot_eq, ":troop_kingdom", slot_faction_leader, ":troop_no"),
          (assign, ":num_tries", 50),
        (try_end),

        #(str_store_troop_name, s0, ":troop_no"),
        #(display_message, "{!}str_debug__hiring_men_to_party_for_s0"),

        (try_for_range, ":unused", 0, ":num_tries"),
          (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"),
        (try_end),

        (assign, ":xp_rounds", 0),

        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (try_begin),
          (this_or_next|eq, ":troop_faction_no", "$players_kingdom"),
          (eq, ":troop_faction_no", "fac_player_supporters_faction"),
          (assign, ":xp_rounds", 0),
        (else_try),
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":xp_rounds", 2),
        (else_try),
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":xp_rounds", 1),
        (else_try),
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":xp_rounds", 0),
        (try_end),

        (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
        (store_div, ":renown_xp_rounds", ":renown", 100),
        (val_add, ":xp_rounds", ":renown_xp_rounds"),
        (try_for_range, ":unused", 0, ":xp_rounds"),
          (call_script, "script_upgrade_hero_party", "$pout_party", 4000),
        (try_end),
      (try_end),
  ])
]
