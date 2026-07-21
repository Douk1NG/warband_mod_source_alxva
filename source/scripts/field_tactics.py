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

field_tactics_scripts = [
("field_tactics", [
      (store_script_param, ":include_ranged", 1),

      (assign, ":largest_team_size", 0),
      (assign, ":battle_size", 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":team_size", ":ai_team", slot_team_size),
        (gt, ":team_size", 0),
        (team_get_slot, ":team_cav_size", ":ai_team", slot_team_num_cavalry),
        (store_add, ":team_adj_size", ":team_size", ":team_cav_size"),	#double count cavalry to capture effect on battlefield
        (val_add, ":battle_size", ":team_adj_size"),

        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (neg | teams_are_enemies, ":ai_team", "$fplayer_team_no"),
          (team_get_slot, ":player_team_adj_size", "$fplayer_team_no", slot_team_adj_size),
          (val_add, ":team_adj_size", ":player_team_adj_size"),	#ally team takes player team into account
          (team_set_slot, "$fplayer_team_no", slot_team_adj_size, ":team_adj_size"),	#and vice versa
        (try_end),
        (team_set_slot, ":ai_team", slot_team_adj_size, ":team_adj_size"),

        (lt, ":largest_team_size", ":team_adj_size"),
        (assign, ":largest_team_size", ":team_adj_size"),
      (try_end),

      #apply tactics to every AI team
      (set_show_messages, 0),
      (try_for_range, ":ai_team", 0, 4),
        (team_get_slot, ":ai_team_size", ":ai_team", slot_team_adj_size),
        (gt, ":ai_team_size", 0),

        (assign, ":do_it", 0),
        (try_begin),
          (neq, ":ai_team", "$fplayer_team_no"),
          (assign, ":do_it", 1),
        (else_try),
          (main_hero_fallen),    #have AI take over for mods with post-player battle action
          (eq, AI_Replace_Dead_Player, 1),
          (assign, ":do_it", 1),
        (try_end),
        (eq, ":do_it", 1),

        (team_get_slot, ":ai_faction", ":ai_team", slot_team_faction),
        (try_begin),
          (neq, AI_for_kingdoms_only, 0),
          (neq, ":ai_faction", fac_deserters),	#deserters have military training
          (neq, ":ai_faction", fac_black_khergits),
          (neq, ":ai_faction", fac_dark_knights),
          #(neq, ":ai_faction", fac_mountain_bandits),	#scoti, frank and dena pirates have military training Chief anade
          (neg | is_between, ":ai_faction", kingdoms_begin, kingdoms_end),

          (call_script, "script_formation_end", ":ai_team", grc_everyone),
          (team_get_movement_order, reg0, ":ai_team", grc_everyone),
          (try_begin),
            (neq, reg0, mordr_charge),
            (team_give_order, ":ai_team", grc_everyone, mordr_charge),
          (try_end),

        #uses tactics
        (else_try),
          (val_mul, ":ai_team_size", 100),
          (store_div, ":team_percentage", ":ai_team_size", ":largest_team_size"),
          (store_div, ":team_battle_presence", ":ai_team_size", ":battle_size"),
          (try_begin),
            (eq, ":include_ranged", 1),
            (try_begin),
              (store_mod, ":team_phase", ":ai_team", 2),
              (eq, ":team_phase", 0),
              (assign, ":time_slice", 0),
            (else_try),
              (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
            (try_end),

            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (this_or_next | eq, reg0, ":time_slice"),
            (eq, "$battle_phase", BP_Setup),
            (call_script, "script_team_field_ranged_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
          (try_end),

          (try_begin),
            (gt, "$fplayer_team_no", 0),	#not a spectator
            (neg | main_hero_fallen),
            (store_add, ":slot", slot_team_d0_target_team, grc_infantry),
            (team_slot_eq, ":ai_team", ":slot", "$fplayer_team_no"),
            (store_add, ":slot", slot_team_d0_target_division, grc_infantry),
            (team_get_slot, ":enemy_division", ":ai_team", ":slot"),
            (store_add, ":slot", slot_team_d0_size, ":enemy_division"),
            (team_slot_ge, "$fplayer_team_no", ":slot", 1),
            (store_add, ":slot", slot_team_d0_fclock, ":enemy_division"),
            (team_get_slot, ":fclock", "$fplayer_team_no", ":slot"),
            (store_mod, reg0, ":fclock", Reform_Trigger_Modulus),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (else_try),
            (store_mod, reg0, "$ranged_clock", Reform_Trigger_Modulus),
            (store_mod, ":team_phase", ":ai_team", 2),
            (eq, ":team_phase", 0),
            (assign, ":time_slice", 0),
          (else_try),
            (store_div, ":time_slice", Reform_Trigger_Modulus, 2),
          (try_end),

          (eq, reg0, ":time_slice"),
          (call_script, "script_team_field_melee_tactics", ":ai_team", ":team_percentage", ":team_battle_presence"),
        (try_end),
      (try_end),
      (set_show_messages, 1),])
]
