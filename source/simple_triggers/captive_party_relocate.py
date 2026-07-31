# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

captive_party_relocate_simple_triggers = [
(0,
   [
      # (try_begin),
        # (eq, "$bug_fix_version", 0),

        # #fix for hiding test_scene in older savegames
        # (disable_party, "p_test_scene"),
        # #fix for correcting town_1 siege type
        # (party_set_slot, "p_town_1", slot_center_siege_with_belfry, 0),
        # #fix for hiding player_faction notes
        # (faction_set_note_available, "fac_player_faction", 0),
        # #fix for hiding faction 0 notes
        # (faction_set_note_available, "fac_no_faction", 0),
        # #fix for removing kidnapped girl from party
        # (try_begin),
          # (neg|check_quest_active, "qst_kidnapped_girl"),
          # (party_remove_members, "p_main_party", "trp_kidnapped_girl", 1),
        # (try_end),
        # #fix for not occupied but belong to a faction lords
        # (try_for_range, ":cur_troop", lords_begin, lords_end),
          # (try_begin),
            # (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
            # (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
            # (is_between, ":cur_troop_faction", "fac_kingdom_1", kingdoms_end),
            # (troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
          # (try_end),
        # (try_end),
        # #fix for an error in 1.105, also fills new slot values
        # (call_script, "script_initialize_item_info"),

        # (assign, "$bug_fix_version", 1),
      # (try_end),

      (eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),
]
