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

multiplayer_event_agent_killed_or_wounded_scripts = [
#script_multiplayer_event_agent_killed_or_wounded
# Input: arg1 = dead_agent_no, arg2 = killer_agent_no
# Output: none
("multiplayer_event_agent_killed_or_wounded",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),

     (multiplayer_get_my_player, ":my_player_no"),
     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":my_player_agent", ":my_player_no"),
       (ge, ":my_player_agent", 0),
       (try_begin),
         (eq, ":my_player_agent", ":dead_agent_no"),
         (store_mission_timer_a, "$g_multiplayer_respawn_start_time"),
       (try_end),
       (try_begin),
         (eq, ":my_player_agent", ":killer_agent_no"),
         (neq, ":my_player_agent", ":dead_agent_no"),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_alive, ":my_player_agent"),
         (neg|agent_is_ally, ":dead_agent_no"),
         (agent_get_horse, ":my_horse_agent", ":my_player_agent"),
         (agent_get_wielded_item, ":my_wielded_item", ":my_player_agent", 0),
         (assign, ":my_item_class", -1),
         (try_begin),
           (ge, ":my_wielded_item", 0),
           (item_get_slot, ":my_item_class", ":my_wielded_item", slot_item_multiplayer_item_class),
         (try_end),
         #SPOIL_THE_CHARGE achievement
         (try_begin),
           (lt, ":my_horse_agent", 0),
           (agent_get_horse, ":dead_agent_horse_agent", ":dead_agent_no"),
           (ge, ":dead_agent_horse_agent", 0),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SPOIL_THE_CHARGE, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SPOIL_THE_CHARGE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_SPOIL_THE_CHARGE),
         (try_end),
         #SPOIL_THE_CHARGE achievement end
         #HARASSING_HORSEMAN achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_bow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_crossbow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_HARASSING_HORSEMAN, 0),
           (lt, ":achievement_stat", 100),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_HARASSING_HORSEMAN, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 100),
           (unlock_achievement, ACHIEVEMENT_HARASSING_HORSEMAN),
         (try_end),
         #HARASSING_HORSEMAN achievement end
         #THROWING_STAR achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THROWING_STAR, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THROWING_STAR, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_THROWING_STAR),
         (try_end),
         #THROWING_STAR achievement end
         #SHISH_KEBAB achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (eq, ":my_item_class", multi_item_class_type_lance),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SHISH_KEBAB, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SHISH_KEBAB, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_SHISH_KEBAB),
         (try_end),
         #SHISH_KEBAB achievement end
         #CHOPPY_CHOP_CHOP achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_axe),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_cleavers),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_axe),
           (this_or_next|eq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (eq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_CHOPPY_CHOP_CHOP),
         (try_end),
         #CHOPPY_CHOP_CHOP achievement end
         #MACE_IN_YER_FACE achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_blunt),
           (eq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_MACE_IN_YER_FACE, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_MACE_IN_YER_FACE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_MACE_IN_YER_FACE),
         (try_end),
         #MACE_IN_YER_FACE achievement end
         #THE_HUSCARL achievement
         (try_begin),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THE_HUSCARL, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THE_HUSCARL, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_THE_HUSCARL),
         (try_end),
         #THE_HUSCARL achievement end
       (try_end),
     (try_end),

     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":player_agent", ":my_player_no"),
       (eq, ":dead_agent_no", ":player_agent"),

       (assign, ":show_respawn_counter", 0),
       (try_begin),
         #TODO: add other game types with no respawns here
         (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
         (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
         (assign, ":show_respawn_counter", 1),
       (else_try),
         (eq, "$g_multiplayer_player_respawn_as_bot", 1),
         (player_get_team_no, ":my_player_team", ":my_player_no"),
         (assign, ":is_found", 0),
         (try_for_agents, ":cur_agent"),
           (eq, ":is_found", 0),
           (agent_is_alive, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_get_team ,":cur_team", ":cur_agent"),
           (eq, ":cur_team", ":my_player_team"),
           (assign, ":is_found", 1),
         (try_end),
         (eq, ":is_found", 1),
         (assign, ":show_respawn_counter", 1),
       (try_end),

       (try_begin),
         #(player_get_slot, ":spawn_count", ":player_no", slot_player_spawn_count),
         (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
         (gt, "$g_multiplayer_number_of_respawn_count", 0),

         (ge, "$g_my_spawn_count", "$g_multiplayer_number_of_respawn_count"),

         (multiplayer_get_my_player, ":my_player_no"),
         (player_get_team_no, ":my_player_team", ":my_player_no"),

         (this_or_next|eq, ":my_player_team", 0),
         (ge, "$g_my_spawn_count", 999),

         (assign, "$g_show_no_more_respawns_remained", 1),
       (else_try),
         (assign, "$g_show_no_more_respawns_remained", 0),
       (try_end),

       (eq, ":show_respawn_counter", 1),

       (start_presentation, "prsnt_multiplayer_respawn_time_counter"),
     (try_end),
     ])
]
