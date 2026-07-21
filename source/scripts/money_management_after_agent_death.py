# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

money_management_after_agent_death_scripts = [
("money_management_after_agent_death",
   [
     (store_script_param, ":killer_agent_no", 1),
     (store_script_param, ":dead_agent_no", 2),

     (assign, ":dead_agent_player_id", -1),

     (try_begin),
       (multiplayer_is_server),
       (ge, ":killer_agent_no", 0),
       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_is_human, ":killer_agent_no"), #if killer agent is not horse
       (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
       (agent_get_team, ":dead_agent_team", ":dead_agent_no"),

       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
       (neq, ":killer_agent_team", ":dead_agent_team"), #if these agents are enemies

       (neq, ":dead_agent_no", ":killer_agent_no"), #if agents are different, do not remove it is needed because in deathmatch mod, self killing passes here because of this or next.

       (try_begin),
         (neg|agent_is_non_player, ":dead_agent_no"),
         (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
         (player_get_slot, ":dead_agent_equipment_value", ":dead_player_no", slot_player_total_equipment_value),
       (else_try),
         (assign, ":dead_agent_equipment_value", 0),
       (try_end),

       (assign, ":dead_agent_team_human_players_count", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),
         (player_get_team_no, ":player_team", ":player_no"),
         (eq, ":player_team", ":dead_agent_team"),
         (val_add, ":dead_agent_team_human_players_count", 1),
       (try_end),

       (try_for_range, ":player_no", 0, ":num_players"),
         (player_is_active, ":player_no"),

         (try_begin),
           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
           (assign, ":one_spawn_per_round_game_type", 1),
         (else_try),
           (assign, ":one_spawn_per_round_game_type", 0),
         (try_end),

         (this_or_next|eq, ":one_spawn_per_round_game_type", 0),
         (this_or_next|player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
         (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),

         (player_get_agent_id, ":agent_no", ":player_no"),
         (try_begin),
           (eq, ":agent_no", ":dead_agent_no"), #if this agent is dead agent then get share from total loot. (20% of total equipment value)
           (player_get_gold, ":player_gold", ":player_no"),

           (assign, ":dead_agent_player_id", ":player_no"),

           #dead agent loot share (32%-48%-64%, norm : 48%)
           (store_mul, ":share_of_dead_agent", ":dead_agent_equipment_value", multi_dead_agent_loot_percentage_share),
           (val_div, ":share_of_dead_agent", 100),
           (val_mul, ":share_of_dead_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_dead_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_dead_agent", 4),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_dead_agent", 2),
             (val_div, ":share_of_dead_agent", 3),
             (val_add, ":player_gold", ":share_of_dead_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_dead_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (else_try),
           (eq, ":agent_no", ":killer_agent_no"), #if this agent is killer agent then get share from total loot. (10% of total equipment value)
           (player_get_gold, ":player_gold", ":player_no"),

           #killer agent standart money (100-150-200, norm : 150)
           (assign, ":killer_agent_standard_money_addition", multi_killer_agent_standard_money_add),
           (val_mul, ":killer_agent_standard_money_addition", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":killer_agent_standard_money_addition", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":killer_agent_standard_money_addition", 4),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":killer_agent_standard_money_addition", 2),
             (val_div, ":killer_agent_standard_money_addition", 3),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
           (else_try),
             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), #(3/3x) share if current mod is siege
           (try_end),

           #killer agent loot share (8%-12%-16%, norm : 12%)
           (store_mul, ":share_of_killer_agent", ":dead_agent_equipment_value", multi_killer_agent_loot_percentage_share),
           (val_div, ":share_of_killer_agent", 100),
           (val_mul, ":share_of_killer_agent", "$g_multiplayer_battle_earnings_multiplier"),
           (val_div, ":share_of_killer_agent", 100),
           (try_begin),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
             (val_mul, ":share_of_killer_agent", 4),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"),
           (else_try),
             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle
             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
             (val_mul, ":share_of_killer_agent", 2),
             (val_div, ":share_of_killer_agent", 3),
             (val_add, ":player_gold", ":share_of_killer_agent"),
           (else_try),
             (val_add, ":player_gold", ":share_of_killer_agent"), #(3/3x) share if current mod is siege
           (try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),
       (try_end),
     (try_end),

     #(below lines added new at 25.11.09 after Armagan decided new money system)
     (try_begin),
       (multiplayer_is_server),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
       (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),

       (ge, ":dead_agent_no", 0),
       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
       (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
       (ge, ":dead_agent_player_id", 0),

       (player_get_gold, ":player_gold", ":dead_agent_player_id"),
       (try_begin),
         (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
         (lt, ":player_gold", ":minimum_gold"),
         (assign, ":player_gold", ":minimum_gold"),
       (try_end),
       (player_set_gold, ":dead_agent_player_id", ":player_gold"),
     (try_end),
     #new money system addition end
     ])
]
