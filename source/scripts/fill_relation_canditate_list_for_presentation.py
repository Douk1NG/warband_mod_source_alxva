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

fill_relation_canditate_list_for_presentation_scripts = [
("fill_relation_canditate_list_for_presentation",
    [
        (store_script_param, ":pres_type", 1),
        (store_script_param, ":base_candidates_y", 2),

        # Type of list from global variable: 0 courtship, 1 known lords
        (try_begin),
        ## For courtship:
            (eq, ":pres_type", 0),

            (try_for_range_backwards, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
                (troop_slot_ge, ":lady", slot_troop_met, 1), # met or better
                (troop_slot_eq, ":lady", slot_troop_spouse, -1), # unmarried

                # use faction filter
                (store_troop_faction, ":lady_faction", ":lady"),
                (val_sub, ":lady_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":lady_faction"),

                (call_script, "script_troop_get_relation_with_troop", "trp_player", ":lady"),
                (gt, reg0, 0),
                (assign, reg3, reg0),

                (str_store_troop_name, s2, ":lady"),

                (store_current_hours, ":hours_since_last_visit"),
                (troop_get_slot, ":last_visit_hour", ":lady", slot_troop_last_talk_time),
                (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
                (store_div, ":days_since_last_visit", ":hours_since_last_visit", 24),
                (assign, reg4, ":days_since_last_visit"),

                #(str_store_string, s1, "str_s1_s2_relation_reg3_last_visit_reg4_days_ago"),
                (str_store_string, s1, "@{s2}: {reg3}, {reg4} days"),

                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":lady"),

                # candidate found, store troop id for later use
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":lady"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## End courtship relations
        (else_try),
        ## For lord relations
            (eq, ":pres_type", 1),

            # Loop to identify
            (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                (troop_set_slot, ":active_npc", slot_troop_temp_slot, 0),
            (try_end),

            (try_for_range, ":unused", active_npcs_begin, active_npcs_end),

                (assign, ":score_to_beat", 101),
                (assign, ":best_relation_remaining_npc", -1),

                (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
                        (troop_slot_eq, ":active_npc", slot_troop_temp_slot, 0),
                        (troop_slot_ge, ":active_npc", slot_troop_met, 1),
                        (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),

                        (call_script, "script_troop_get_player_relation", ":active_npc"),
                        (assign, ":relation_with_player", reg0),
                        (le, ":relation_with_player", ":score_to_beat"),

                        (assign, ":score_to_beat", ":relation_with_player"),
                        (assign, ":best_relation_remaining_npc", ":active_npc"),
                (try_end),
                (gt, ":best_relation_remaining_npc", -1),

                (str_store_troop_name, s4, ":best_relation_remaining_npc"),
                (assign, reg4, ":score_to_beat"),

                (str_store_string, s1, "@{s4}: {reg4}"),
                (troop_set_slot, ":best_relation_remaining_npc", slot_troop_temp_slot, 1),

                # use faction filter
                (store_troop_faction, ":npc_faction", ":best_relation_remaining_npc"),
                (val_sub, ":npc_faction", kingdoms_begin),
                (this_or_next|eq, "$g_jrider_faction_filter", -1),
                (eq, "$g_jrider_faction_filter", ":npc_faction"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":best_relation_remaining_npc"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":best_relation_remaining_npc"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
        ## END Lords relations
        (else_try),
        ## Character and Companions
            (eq, ":pres_type", 2),

            # companions
            (try_for_range_backwards, ":companion", companions_begin, companions_end),
                (troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),

                (str_store_troop_name, s1, ":companion"),

        (try_begin),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
                    (str_store_string, s1, "@{s1}(gathering support)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
                    (str_store_string, s1, "@{s1} (intelligence)" ),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
                    (neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
                    (str_store_string, s1, "@{s1} (ambassy)"),
                (else_try),
                        (eq, ":companion", "$g_player_minister"),
                    (str_store_string, s1, "@{s1} (minister"),
                (else_try),
                    (main_party_has_troop, ":companion"),
                    (str_store_string, s1, "@{s1} (under arms)"),
                (else_try),
                    (troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                    (str_store_string, s1, "@{s1} (attempting to rejoin)"),
                (else_try),
                    (troop_slot_ge, ":companion", slot_troop_cur_center, 1),
                    (str_store_string, s1, "@{s1} (separated after battle)"),
                (try_end),
                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", ":companion"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", ":companion"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # END companions

            # Wife/Betrothed
            # END Wife/Betrothed

            (try_begin),
            # Character
                (str_store_troop_name, s1, "trp_player"),

                # candidate found,
                # create custom listbox entry, set the container first
                (store_mul, ":y_mult", "$num_charinfo_candidates", 16), # adapt y position to entry number, was 18
                (store_add, ":line_y", ":base_candidates_y", ":y_mult"),

                (call_script, "script_overlay_container_add_listbox_item", ":line_y", "trp_player"),

                #store troop id for later use (could be merged with the object id)
                (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$num_charinfo_candidates"),
                (troop_set_slot, "trp_temp_array_c", ":current_storage_index", "trp_player"),

                # update entry counter
                (val_add, "$num_charinfo_candidates", 1),
            (try_end),
            # End Character

        (try_end),
        ## END Character and Companions
    ])
]
