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

agent_reassign_team_scripts = [
("agent_reassign_team",
    [
      (store_script_param, ":agent_no", 1),
      (get_player_agent_no, ":player_agent"),
      (try_begin),
        (ge, ":player_agent", 0),
        (agent_is_human, ":agent_no"),
        (agent_is_ally, ":agent_no"),
        (agent_get_party_id, ":party_no", ":agent_no"),
        #SB : pre-process this instead of calculating per agent
        (party_slot_eq, ":party_no", slot_party_temp_slot_1, -1),
        # (neq, ":party_no", "p_main_party"),
        # (assign, ":continue", 1),
        # (store_faction_of_party, ":party_faction", ":party_no"),
        # (try_begin),
          # (eq, ":party_faction", "$players_kingdom"),
          # (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
          # (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
          # (assign, ":continue", 0),
        # (else_try),
          # (party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),
          # (neg|is_between, ":leader_troop_id", active_npcs_begin, active_npcs_end),
          # (assign, ":continue", 0),
        # (try_end),
        # (eq, ":continue", 1),
        (agent_get_team, ":player_team", ":player_agent"),
        (val_add, ":player_team", 2),
        (agent_set_team, ":agent_no", ":player_team"),
      (try_end),
      ])
]
