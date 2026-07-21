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

memorize_division_placements_scripts = [
("memorize_division_placements", [
      (set_fixed_point_multiplier, 100),
      (call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
      (assign, ":num_enemies", reg0),

      (try_for_range, ":division", 0, 9),
        (class_is_listening_order, "$fplayer_team_no", ":division"),
        (store_add, ":slot", slot_team_d0_size, ":division"),
        (team_slot_ge, "$fplayer_team_no", ":slot", 1),

        (store_add, ":slot", slot_team_d0_formation, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_formation_space, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (store_add, ":slot", slot_faction_d0_mem_formation_space, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (agent_get_position, pos1, "$fplayer_agent_no"),
        (try_begin),
          (neq, ":num_enemies", 0),	#more than 0 enemies still alive?
          (call_script, "script_point_y_toward_position", pos1, Enemy_Team_Pos),
        (try_end),
        # (call_script, "script_get_formation_destination", Current_Pos,
        # "$fplayer_team_no", ":division"),
        (team_get_order_position, Current_Pos, "$fplayer_team_no", ":division"),	#use this to capture Native Advance and Fall Back positioning
        (position_transform_position_to_local, Temp_Pos, pos1, Current_Pos), #Temp_Pos = vector to division w.r.t.  leader facing enemy

        (position_get_x, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_x_flag, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (position_get_y, ":value", Temp_Pos),
        (store_add, ":slot", slot_faction_d0_mem_relative_y, ":division"),
        (faction_set_slot, "fac_player_faction", ":slot", ":value"),

        (store_add, ":slot", slot_team_d0_type, ":division"),
        (team_get_slot, ":value", "$fplayer_team_no", ":slot"),
        (call_script, "script_str_store_division_type_name", s1, ":value"),
        (store_add, reg0, ":division", 1),
        (display_message, "@The placement of {s1} division {reg0} memorized."),
      (try_end),])
]
