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

companion_get_mission_string_scripts = [
("companion_get_mission_string", [
        (store_script_param, ":companion", 1),
        (try_begin), #do not impose conditions here, do so from calling script
            # (this_or_next|main_party_has_troop, ":companion"),
            # (this_or_next|troop_slot_ge, ":companion", slot_troop_current_mission, 1),
                # (eq, "$g_player_minister", ":companion"),
            (str_store_troop_name, s4, ":companion"),
            (str_clear, s5),
            (str_clear, s8),
            (troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),
            (troop_get_slot, ":mission", ":companion", slot_troop_current_mission),
            (try_begin),
                (le, ":days_left", 0),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (eq, ":days_left", 1),
                (str_store_string, s5, "str_expected_back_imminently"),
            (else_try),
                (assign, reg3, ":days_left"),
                (str_store_string, s5, "str_expected_back_in_approximately_reg3_days"),
            (try_end),


            (try_begin),
                (eq, ":mission", npc_mission_kingsupport),
                (str_store_string, s8, "str_gathering_support"),
            (else_try),
                (this_or_next|eq, ":mission", npc_mission_gather_intel),
                (eq, ":mission", dplmc_npc_mission_rescue_prisoner), #new mission
                (troop_get_slot, ":town_with_contacts", ":companion", slot_troop_town_with_contacts),
                (str_store_party_name, s9, ":town_with_contacts"),
                (try_begin),
                  (eq, ":mission", npc_mission_gather_intel),
                  (str_store_string, s8, "str_gathering_intelligence"),
                (else_try),
                  (eq, ":mission", dplmc_npc_mission_rescue_prisoner),
                  (str_store_string, s8, "str_preparing_prison_break"),
                (try_end),
            (else_try),
                (this_or_next|is_between, ":mission", npc_mission_peace_request, npc_mission_rejoin_when_possible),
                (is_between, ":mission", dplmc_npc_mission_war_request, dplmc_npc_mission_rescue_prisoner),

                (troop_get_slot, ":faction", ":companion", slot_troop_mission_object),
                (str_store_faction_name, s9, ":faction"),
                (str_store_string, s8, "str_diplomatic_embassy_to_s9"),
            # (else_try), #diplomacy missions

            (else_try),
                (eq, ":companion", "$g_player_minister"),
                (str_store_string, s8, "str_serving_as_minister"),
                (try_begin),
                  (is_between, "$g_player_court", centers_begin, centers_end),
                  (str_store_party_name, s9, "$g_player_court"),
                  (str_store_string, s5, "str_in_your_court_at_s9"),
                (else_try),
                  (str_store_string, s5, "str_awaiting_the_capture_of_a_fortress_which_can_serve_as_your_court"),
                (try_end),
            (else_try),
                (eq, ":mission", npc_mission_rejoin_when_possible),
                (str_store_string, s8, "str_attempting_to_rejoin_party"),
            (else_try),
                (main_party_has_troop, ":companion"),
                (str_store_string, s8, "str_under_arms"),
                (str_store_string, s5, "str_in_your_party"),
            (else_try),    #Companions who are in a center
                (troop_slot_ge, ":companion", slot_troop_cur_center, centers_begin),
                (str_store_string, s8, "str_separated_from_party"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),    #Companions who are (imprisoned) in a center
                (troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),
                (str_store_string, s8, "str_missing_after_battle"),
                (str_store_string, s5, "str_whereabouts_unknown"),
            (else_try),
                (try_begin),
                    (check_quest_active, "qst_lend_companion"),
                    (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_companion", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (else_try),
                    (check_quest_active, "qst_lend_surgeon"),
                    (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
                    (quest_get_slot, ":lord", "qst_lend_surgeon", slot_quest_giver_troop),
                    (str_store_troop_name, s5, ":lord"),
                    (str_store_string, s8, "str_accompanying_s5"),
                    (str_store_string, s5, "str_on_loan"),
                (try_end),
            (try_end),

            (str_store_string, s0, "str_s4_s8_s5"),
        (try_end),
        ]
      )
]
