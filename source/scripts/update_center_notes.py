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

update_center_notes_scripts = [
#script_update_faction_notes
# INPUT: center_no
# OUTPUT: none
("update_center_notes",
    [
##      (store_script_param, ":center_no", 1),
##
##     (party_get_slot, ":lord_troop", ":center_no", slot_town_lord),
##     (try_begin),
##       (ge, ":lord_troop", 0),
##       (store_troop_faction, ":lord_faction", ":lord_troop"),
##       (str_store_troop_name_link, s1, ":lord_troop"),
##       (try_begin),
##         (eq, ":lord_troop", "trp_player"),
##         (gt, "$players_kingdom", 0),
##         (str_store_faction_name_link, s2, "$players_kingdom"),
##       (else_try),
##         (str_store_faction_name_link, s2, ":lord_faction"),
##       (try_end),
##       (str_store_party_name, s50, ":center_no"),
##       (try_begin),
##         (party_slot_eq, ":center_no", slot_party_type, spt_town),
##         (str_store_string, s51, "@The town of {s50}"),
##       (else_try),
##         (party_slot_eq, ":center_no", slot_party_type, spt_village),
##         (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
##         (str_store_party_name_link, s52, ":bound_center"),
##         (str_store_string, s51, "@The village of {s50} near {s52}"),
##       (else_try),
##         (str_store_string, s51, "@{!}{s50}"),
##       (try_end),
##       (str_store_string, s2, "@{s51} belongs to {s1} of {s2}.^"),
##     (else_try),
##       (str_clear, s2),
##     (try_end),
##     (try_begin),
##       (is_between, ":center_no", villages_begin, villages_end),
##     (else_try),
##       (assign, ":num_villages", 0),
##       (try_for_range_backwards, ":village_no", villages_begin, villages_end),
##         (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
##         (try_begin),
##           (eq, ":num_villages", 0),
##           (str_store_party_name_link, s8, ":village_no"),
##         (else_try),
##           (eq, ":num_villages", 1),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{s7} and {s8}"),
##         (else_try),
##           (str_store_party_name_link, s7, ":village_no"),
##           (str_store_string, s8, "@{!}{s7}, {s8}"),
##         (try_end),
##         (val_add, ":num_villages", 1),
##       (try_end),
##       (try_begin),
##         (eq, ":num_villages", 0),
##         (str_store_string, s2, "@{s2}It has no villages.^"),
##       (else_try),
##         (store_sub, reg0, ":num_villages", 1),
##         (str_store_string, s2, "@{s2}{reg0?Its villages are:Its village is} {s8}.^"),
##       (try_end),
##     (try_end),
##     (call_script, "script_get_prosperity_text_to_s50", ":center_no"),
##     (add_party_note_from_sreg, ":center_no", 0, "@{s2}Its prosperity is: {s50}", 0),
##     (add_party_note_tableau_mesh, ":center_no", "tableau_center_note_mesh"),
     ])
]
