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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

game_context_menu_get_buttons_scripts = [
#script_game_context_menu_get_buttons:
# This script is called from the game engine when the player clicks the right mouse button over a party on the map.
# INPUT: arg1 = party_no
# OUTPUT: none, fills the menu buttons
("game_context_menu_get_buttons",
   [
     (store_script_param, ":party_no", 1),
     (try_begin),
       (neq, ":party_no", "p_main_party"),
       (context_menu_add_item, "@Move here", cmenu_move),
     (try_end),

     (try_begin),
       (is_between, ":party_no", centers_begin, centers_end),
       (context_menu_add_item, "@View notes", cmenu_notes),
     (else_try),
       (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
       (gt, ":num_stacks", 0),
       (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
       ##diplomacy start+ support for promoted kingdom ladies
       (is_between, ":troop_no", heroes_begin, heroes_end),
       (this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       ##diplomacy end+
       (is_between, ":troop_no", active_npcs_begin, active_npcs_end),
       (context_menu_add_item, "@View notes", cmenu_notes), #move this to same slot
       # Lav modifications start (custom lord notes)
       (context_menu_add_item, "@Add custom note", 3),
       # Lav modifications end (custom lord notes)
     (try_end),

     (try_begin),
       (neq, ":party_no", "p_main_party"),
       (store_faction_of_party, ":party_faction", ":party_no"),

       (this_or_next|eq, ":party_faction", "$players_kingdom"),
       (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
       (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),

       (neg|is_between, ":party_no", centers_begin, centers_end),

       (context_menu_add_item, "@Accompany", cmenu_follow),
     (try_end),

      #SB : debug cheats
      (try_begin),
        (ge, "$cheat_mode", 1),
        (try_begin),
           (neq, ":party_no", "p_main_party"),
           (context_menu_add_item, "@Attach", cmenu_attach),
           # (context_menu_add_item, "@Reinforce", cmenu_reinforce),
           (context_menu_add_item, "@Inspect", cmenu_encounter),
           # (context_menu_add_item, "@Exchange", cmenu_exchange),
        (try_end),
        (try_begin),
          (party_get_num_attached_parties, ":num_attached", ":party_no"),
          (gt, ":num_attached", 0),
          (try_begin),
            (eq, ":party_no", "p_main_party"),
            (party_get_attached_party_with_rank, ":attached_party", "p_main_party", 0),
            (str_store_party_name, s1, ":attached_party"),
            (set_fixed_point_multiplier, 1000),
            (party_get_position, pos1, ":party_no"),
            (position_get_x, reg1, pos1),
            (position_get_y, reg2, pos1),
            (context_menu_add_item, "@Detach {s1} at {reg1},{reg2}", cmenu_attach),
          (try_end),
          (context_menu_add_item, "@Detach All", cmenu_detach),
        (try_end),

        (try_begin),
          (party_get_battle_opponent, ":other_party", ":party_no"),
          (party_is_active, ":other_party"),
          (context_menu_add_item, "@Win Battle", cmenu_winbattle),
          (context_menu_add_item, "@Lose Battle", cmenu_losebattle),
        # (else_try),
          # (context_menu_add_item, "@Wound All", cmenu_wound),
          # (context_menu_add_item, "@Heal All", cmenu_heal),
        (try_end),

        # (try_begin),
          # (is_between, ":party_no", centers_begin, centers_end),
          # (context_menu_add_item, "@Spawn Bandits", cmenu_spawnbandit),
        # (try_end),
      (try_end),
  ])
]
