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

generate_extended_troop_relation_information_string_scripts = [
("generate_extended_troop_relation_information_string",
     [
         (store_script_param, ":troop_no", 1),

         # clear the strings and registers we'll use to prevent external interference
         (str_clear, s1),
         (str_clear, s2),
         (str_clear, s60),
         (str_clear, s42),
         (str_clear, s43),
         (str_clear, s44),
         (str_clear, s45),
         (str_clear, s46),
         (str_clear, s47),
         (str_clear, s48),
         (str_clear, s49),
         (str_clear, s50),
         (assign, reg40,0),
         (assign, reg41,0),
         (assign, reg43,0),
         (assign, reg44,0),
         (assign, reg46,0),
         (assign, reg47,0),
         (assign, reg48,0),
         (assign, reg49,0),
         (assign, reg50,0),
         (assign, reg51,0),

         (try_begin),
             (eq, ":troop_no", "trp_player"),
             (overlay_set_display, "$g_jrider_character_faction_filter", 0),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Honor - $player_honor
             (assign, reg42, "$player_honor"),

             # Right to rule - $player_right_to_rule
             (assign, reg43, "$player_right_to_rule"),

             # Current faction
             (store_add, reg45, "$players_kingdom"),
             (try_begin),
                 (is_between, "$players_kingdom", "fac_player_supporters_faction", npc_kingdoms_end),
                 (str_store_faction_name, s45, "$players_kingdom"),
             (else_try),
                 (assign, reg45, 0),
                 (str_store_string, s45, "@Calradia."),
             (try_end),

             # status
             (assign, ":origin_faction", "$players_kingdom"),
             #SB : gender strings
             (try_begin),
                 (is_between, ":origin_faction", npc_kingdoms_begin, npc_kingdoms_end),
                 (str_store_string, s44, "@sworn {man/woman}"),
             (else_try),
                 (eq, ":origin_faction", "fac_player_supporters_faction"),
                 (str_store_string, s44, "@ruler"),
             (else_try),
                 (str_store_string, s44, "@free {man/woman}"),
             (try_end),

             # Current liege and relation
             (faction_get_slot, ":liege", "$players_kingdom", slot_faction_leader),
             (str_store_troop_name, s46, ":liege"),
             (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
             (else_try),
                 (assign, reg46, ":liege"),
                 (str_clear, s47),
                 (str_clear, s60),

                 # Relation to liege
                 (call_script, "script_get_troop_relation_to_player_string", s47, ":liege"),
             (end_try),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

             #### Final Storage
             (str_store_string, s1, "@{s1} Renown: {reg40}, Controversy: {reg41}^Honor: {reg42}, Right to rule: {reg43}^\
You are a {s44} of {s45}^{reg45?{reg46?Your liege, {s46},{s47}:You are the ruler of {s45}}:}^^Friends: ^Enemies: ^^Fiefs:^  {reg50?{s50}:no fief}"),
         #######################
         # END Player information
         (else_try),
         #######################
         # Lord information
             (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

             # Troop name
             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Get renown - slot_troop_renown
             (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
             (assign, reg40, ":renown"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Get Reputation type - slot_lord_reputation_type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (assign, reg42, "str_personality_archetypes"),
             (val_add, reg42, ":reputation"),
             (str_store_string, s42, reg42),

             (assign, reg42, ":reputation"),
             # Intrigue impatience - slot_troop_intrigue_impatience
             (troop_get_slot, ":impatience", ":troop_no", slot_troop_intrigue_impatience),
             (assign, reg43, ":impatience"),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin), #SB : do not display original faction string if same
               (neq, ":faction", ":origin_faction"),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
               (assign, reg44, 1),
             (else_try), #if same, start line with capitalized Noble
               (assign, reg44, 0),
             (try_end), #actually skip this line altogether if ruler
             (str_store_faction_name, s45, ":faction"),

             # Current liege - deduced from current faction
             (faction_get_slot, ":liege", ":faction", slot_faction_leader),
             (try_begin),
               #When a member of a faction without a valid leader
               (lt, ":liege", 0),
               (assign, reg46, ":liege"),
               (str_store_string, s46, "str_noone"),
               (assign, reg47, 0),
             (else_try),
               (str_store_troop_name, s46, ":liege"),
               (try_begin),
                 (eq, ":liege", ":troop_no"),
                 (assign, reg46, 0),
               (else_try),
                 (assign, reg46, ":liege"),
                 # Relation to liege
                 (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":liege"),
                 (assign, reg47, reg0),
               (end_try),
             (try_end),

             # Promised a fief ?
             (troop_get_slot, reg51, ":troop_no", slot_troop_promised_fief),

             # Holdings
             (call_script, "script_get_troop_holdings", ":troop_no"),

              # slot_troop_prisoner_of_party
              (assign, reg48, 0),
              (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
              (try_end),

              # Days since last meeting
              (store_current_hours, ":hours_since_last_visit"),
              (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
              (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
              (store_div, reg49, ":hours_since_last_visit", 24),

              #### Final Storage (8 lines)
              (str_store_string, s1, "@{s1}{s2} {reg46?Reputed to be {s42}:}^Renown: {reg40}, Controversy: {reg41} {reg46?Impatience: {reg43}:}^\
{reg46?{reg44?{s44} noble:Noble} of the {s45}^Liege: {s46}, Relation: {reg47}:Ruler of the {s45}}^^{reg48?Currently prisoner of the {s48}:}^\
Days since last meeting: {reg49}^^Fiefs {reg51?(was promised a fief):}:^  {reg50?{s50}:no fief}"),
        ######################
        ## END lord infomation
        (else_try),
        #########################
        # kingdom lady, unmarried
             (is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
             (troop_slot_eq, ":troop_no", slot_troop_spouse, -1),

             (str_store_troop_name, s1, ":troop_no"),

             # relation to player
             (str_clear, s2),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s2, ":troop_no"),

             # Controversy - slot_troop_controversy
             (troop_get_slot, ":controversy", ":troop_no", slot_troop_controversy),
             (assign, reg41, ":controversy"),

             # Reputation type
             (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
             (try_begin),
                 (eq, ":reputation", lrep_conventional),
                 (str_store_string, s42, "@conventional"),
             (else_try),
                 (eq, ":reputation", lrep_adventurous),
                 (str_store_string, s42, "@adventurous"),
             (else_try),
                 (eq, ":reputation", lrep_otherworldly),
                 (str_store_string, s42, "@otherwordly"),
             (else_try),
                 (eq, ":reputation", lrep_ambitious),
                 (str_store_string, s42, "@ambitious"),
             (else_try),
                 (eq, ":reputation", lrep_moralist),
                 (str_store_string, s42, "@moralist"),
             (else_try),
                 (assign, reg42, "str_personality_archetypes"),
                 (val_add, reg42, ":reputation"),
                 (str_store_string, s42, reg42),
             (try_end),

             # courtship state - slot_troop_courtship_state
             (troop_get_slot, ":courtship_state", ":troop_no", slot_troop_courtship_state),
             (try_begin),
               (eq, ":courtship_state", 1),
               (str_store_string, s43, "@just met"),
             (else_try),
               (eq, ":courtship_state", 2),
               (str_store_string, s43, "@admirer"),
             (else_try),
               (eq, ":courtship_state", 3),
               (str_store_string, s43, "@promised"),
             (else_try),
               (eq, ":courtship_state", 4),
               (str_store_string, s43, "@breakup"),
             (else_try),
               (str_store_string, s43, "@unknown"),
             (try_end),

             # Current faction - store_troop_faction
             (store_troop_faction, ":faction", ":troop_no"),
             (troop_get_slot, ":origin_faction", ":troop_no", slot_troop_original_faction),

             # Original faction - slot_troop_original_faction
             (try_begin),
               (val_sub, ":origin_faction", npc_kingdoms_begin),
               (val_add, ":origin_faction", "str_kingdom_1_adjective"),
               (str_store_string, s44, ":origin_faction"),
             (end_try),
             (str_store_faction_name, s45, ":faction"),

             # Father/Guardian
             (assign, reg46, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_father, 0),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
                 (assign, reg46, 1),
             (else_try),
                 (troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
             (try_end),
             (str_store_troop_name, s46, ":guardian"),

             # Relation with player
             (str_clear, s47),
             (str_clear, s60),
             (call_script, "script_get_troop_relation_to_player_string", s47, ":guardian"),

             # courtship permission - slot_lord_granted_courtship_permission
             (try_begin),
                 (troop_slot_ge, ":guardian", slot_lord_granted_courtship_permission, 1),
                 (assign, reg45, 1),
             (else_try),
                 (assign, reg45, 0),
             (try_end),

             # betrothed
             (assign, reg48, 0),
             (try_begin),
                 (troop_slot_ge, ":troop_no", slot_troop_betrothed, 0),
                 (troop_get_slot, reg48, ":troop_no", slot_troop_betrothed),
                 (str_store_troop_name, s48, reg48),
                 (assign, reg48, 1),
             (try_end),

             # Days since last meeting
             (store_current_hours, ":hours_since_last_visit"),
             (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
             (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
             (store_div, reg49, ":hours_since_last_visit", 24),

             # Heard poems
             (assign, reg50, 0),
             (str_clear, s50),

             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_heroic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Heroic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_allegoric_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Allegoric {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_comic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Comic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_mystic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Mystic {s50}"),
             (try_end),
             (try_begin),
                 (troop_slot_eq, ":troop_no", slot_lady_courtship_tragic_recited, 1),
                 (val_add, reg50, 1),
                 (str_store_string, s50, "@Tragic {s50}"),
             (try_end),

             #### Final Storage (8 lines)
             (str_store_string, s1, "@{s1}{s2} Controversy: {reg41}^Reputation: {s42}, Courtship state: {s43}^\
Belongs to the {s45}^{reg46?Her father, {s46}:Her guardian, {s46}}{s47}^Allowed to visit: {reg45?yes:no} {reg48?Betrothed to {s48}:}^^\
Days since last meeting: {reg49}^^Poems:^  {reg50?{s50}:no poem heard}"),
        #########################
        # END kingdom lady, unmarried
        (else_try),
        #########################
        # companions
            (is_between, ":troop_no", companions_begin, companions_end),
            (overlay_set_display, "$g_jrider_character_faction_filter", 0),

            (str_store_troop_name, s1, ":troop_no"),

            (troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),

            (assign, reg42, "str_personality_archetypes"),
            (val_add, reg42, ":reputation"),
            (str_store_string, s42, reg42),

            # birthplace
            (troop_get_slot, ":home", ":troop_no", slot_troop_home),
            (str_store_party_name, s43, ":home"),

            # contacts town - slot_troop_town_with_contacts
            (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
            (str_store_party_name, s44, ":contact_town"),

            # current faction of contact town
            (store_faction_of_party, ":town_faction", ":contact_town"),
            (str_store_faction_name, s45, ":town_faction"),

            # slot_troop_prisoner_of_party
            (assign, reg48, 0),
            (try_begin),
                (troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
                (assign, reg48, 1),
                (troop_get_slot, ":prisoner_party", ":troop_no", slot_troop_prisoner_of_party),
                (store_faction_of_party, ":party_faction", ":prisoner_party"),
                (str_store_faction_name, s48, ":party_faction"),
            (try_end),

            # Days since last meeting
            (store_current_hours, ":hours_since_last_visit"),
            (troop_get_slot, ":last_visit_hour", ":troop_no", slot_troop_last_talk_time),
            (val_sub, ":hours_since_last_visit", ":last_visit_hour"),
            (store_div, reg49, ":hours_since_last_visit", 24),

            (try_begin), # Companion gathering support for Right to Rule
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_kingsupport),
                (str_store_string, s50, "@Gathering support"),
            (else_try), # Companion gathering intelligence
                (troop_slot_eq, ":troop_no", slot_troop_current_mission, npc_mission_gather_intel),
                (troop_get_slot, ":contact_town", ":troop_no", slot_troop_town_with_contacts),
                (store_faction_of_party, ":town_faction", ":contact_town"),
                (str_store_faction_name, s66, ":town_faction"),
                (str_store_string, s50, "@Gathering intelligence in the {s66}"),
            (else_try), # Companion on peace mission
                (troop_slot_ge, ":troop_no", slot_troop_current_mission, npc_mission_peace_request),
                (neg|troop_slot_ge, ":troop_no", slot_troop_current_mission, 8),

                (troop_get_slot, ":troop_no", ":troop_no", slot_troop_mission_object),
                (str_store_faction_name, s66, ":faction"),

                (str_store_string, s50, "@Ambassy to {s66}"),
            (else_try), # Companion is serving as minister player has court
                (eq, ":troop_no", "$g_player_minister"),
                (str_store_string, s50, "@Minister"),
            (else_try),
                (str_store_string, s50, "str_dplmc_none"),
        (try_end),

            # days left
            (troop_get_slot, reg50, ":troop_no", slot_troop_days_on_mission),

            #### Final Storage (8 lines)
            (str_store_string, s1, "@{s1}, {s2}^Reputation: {s42}^\
Born at {s43}^Contact in {s44} of the {s45}.^\
^{reg48?Currently prisoner of the {s48}:}^Days since last talked to: {reg49}^^Current mission:^  {s50}{reg50?, back in {reg50} days.:}"),
        #########################
        # END companions
        (try_end),
    ])
]
