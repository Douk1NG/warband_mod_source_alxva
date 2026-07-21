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

game_event_undetect_party_scripts = [
#script_game_event_undetect_party:
# This script is called from the game engine when player party inspects another party.
# INPUT:
# param1: Party-id
("game_event_undetect_party",
    [
        (store_script_param_1, ":party_id"),
        (try_begin),
          (party_slot_eq, ":party_id", slot_party_type, spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":leader", ":party_id", 0),
          ##diplomacy start+ support for promoted kingdom ladies
          (is_between, ":leader", heroes_begin, heroes_end),
          (this_or_next|troop_slot_eq, ":leader", slot_troop_occupation, slto_kingdom_hero),
          ##diplomacy end+
          (is_between, ":leader", active_npcs_begin, active_npcs_end),
          (call_script, "script_update_troop_location_notes", ":leader", 0),
        (try_end),
  ])
]
