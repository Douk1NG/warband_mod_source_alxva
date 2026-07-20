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

update_report_to_army_quest_note_scripts = [
# script_cf_get_random_enemy_center_within_range
("update_report_to_army_quest_note",
   [
     (store_script_param, ":faction_no", 1),
     (store_script_param, ":new_strategy", 2),
     (store_script_param, ":old_faction_ai_state", 3),

     (try_begin),
     (le, "$number_of_report_to_army_quest_notes", 13),

     (faction_get_slot, ":faction_marshal", ":faction_no", slot_faction_marshall),

     (try_begin), #updating quest notes for only report to army quest
       (eq, ":faction_no", "$players_kingdom"),
       (neq, ":new_strategy", ":old_faction_ai_state"),
       (check_quest_active, "qst_report_to_army"),
       (ge, ":faction_marshal", 0),

       (str_store_troop_name_link, s11, ":faction_marshal"),
       (store_current_hours, ":hours"),
       (call_script, "script_game_get_date_text", 0, ":hours"),

       (try_begin),
         (this_or_next|eq, ":new_strategy", sfai_attacking_enemies_around_center),
         (this_or_next|eq, ":new_strategy", sfai_attacking_center),
         (eq, ":new_strategy", sfai_gathering_army),
         (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
         (ge, ":faction_object", 0),
         (str_store_party_name_link, s21, ":faction_object"),
       (try_end),

       (try_begin),
         (eq, ":new_strategy", sfai_gathering_army),

         (try_begin),
           (ge, "$g_gathering_reason", 0),
           (str_store_party_name_link, s21, "$g_gathering_reason"),
           (str_store_string, s14, "str_we_should_prepare_to_defend_s21_but_we_should_gather_our_forces_until_we_are_strong_enough_to_engage_them"),
         (else_try),
           (str_store_string, s14, "str_it_is_time_to_go_on_the_offensive_and_we_must_first_assemble_the_army"),
         (try_end),

         (str_store_string, s14, "@({s1}) {s11}: {s14}"),
         (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
         (val_add, "$number_of_report_to_army_quest_notes", 1),
       (else_try),
         (eq, ":new_strategy", sfai_attacking_enemies_around_center),

         (try_begin),
           (is_between, ":faction_object", walled_centers_begin, walled_centers_end),
           (str_store_string, s14, "str_we_should_ride_to_break_the_siege_of_s21"),
           (str_store_string, s14, "@({s1}) {s11}: {s14}"),
           (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
           (val_add, "$number_of_report_to_army_quest_notes", 1),
         (else_try),
           (is_between, ":faction_object", villages_begin, villages_end),
           (str_store_string, s14, "str_we_should_ride_to_defeat_the_enemy_gathered_near_s21"),
           (str_store_string, s14, "@({s1}) {s11}: {s14}"),
           (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
           (val_add, "$number_of_report_to_army_quest_notes", 1),
         (try_end),
       (else_try),
         (this_or_next|eq, ":new_strategy", sfai_attacking_center),
         (eq, ":new_strategy", sfai_raiding_village),

         (try_begin),
           (is_between, ":faction_object", walled_centers_begin, walled_centers_end),
           (str_store_string, s14, "str_we_believe_the_fortress_will_be_worth_the_effort_to_take_it"),
           (str_store_string, s14, "@{s14} ({s21})"),
           (str_store_string, s14, "@({s1}) {s11}: {s14}"),
           (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
           (val_add, "$number_of_report_to_army_quest_notes", 1),
         (else_try),
           (is_between, ":faction_object", villages_begin, villages_end),
           (str_store_string, s14, "str_we_shall_leave_a_fiery_trail_through_the_heart_of_the_enemys_lands_targeting_the_wealthy_settlements_if_we_can"),
           (str_store_string, s14, "@{s14} ({s21})"),
           (str_store_string, s14, "@({s1}) {s11}: {s14}"),
           (add_quest_note_from_sreg, "qst_report_to_army", "$number_of_report_to_army_quest_notes", s14, 0),
           (val_add, "$number_of_report_to_army_quest_notes", 1),
         (try_end),
       (try_end),
     (try_end),
     (try_end),
   ])
]
