# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from header_skills import *
from header_troops import *
from ID_items import *
from ID_meshes import *
from module_constants import *

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

# Gender branch feature - relative encoding on real troops
# Slot 534: 0 = natural (picker gender), 1 = flipped (opposite)

GENDER_SCRIPTS = [
("kct_flip_troop_gender",
[
    (store_script_param, ":troop", 1),
    (store_script_param, ":flipped", 2),
    (troop_get_slot, ":dummy", ":troop", cstm_slot_troop_dummy),
    (try_begin),
        (eq, ":flipped", 1),
        (try_begin),
            (eq, "$cstm_selected_gender", 0),
            (assign, ":target_gender", 1),
        (else_try),
            (assign, ":target_gender", 0),
        (try_end),
        (troop_set_type, ":troop", ":target_gender"),
        (try_begin),
            (gt, ":dummy", 0),
            (troop_set_type, ":dummy", ":target_gender"),
        (try_end),
        (try_begin),
            (gt, "$cstm_presentation_troop", 0),
            (troop_set_type, "$cstm_presentation_troop", ":target_gender"),
        (try_end),
    (else_try),
        (troop_set_type, ":troop", "$cstm_selected_gender"),
        (try_begin),
            (gt, ":dummy", 0),
            (troop_set_type, ":dummy", "$cstm_selected_gender"),
        (try_end),
        (try_begin),
            (gt, "$cstm_presentation_troop", 0),
            (troop_set_type, "$cstm_presentation_troop", "$cstm_selected_gender"),
        (try_end),
    (try_end),
]),

("kct_flip_subtree",
[
    (store_script_param, ":root", 1),
    (store_script_param, ":flipped", 2),
    (troop_set_slot, ":root", cstm_slot_troop_gender, ":flipped"),
    (call_script, "script_kct_flip_troop_gender", ":root", ":flipped"),
    # Propagate to all descendants via base_troop links (10 passes enough for depth <=7)
    (try_for_range, ":pass", 0, 10),
        (assign, ":any", 0),
        (try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
            (neq, ":troop", ":root"),
            (troop_get_slot, ":parent", ":troop", cstm_slot_troop_base_troop),
            (gt, ":parent", 0),
            (troop_get_slot, ":parent_gender", ":parent", cstm_slot_troop_gender),
            (eq, ":parent_gender", ":flipped"),
            (troop_get_slot, ":cur", ":troop", cstm_slot_troop_gender),
            (neq, ":cur", ":flipped"),
            (troop_set_slot, ":troop", cstm_slot_troop_gender, ":flipped"),
            (call_script, "script_kct_flip_troop_gender", ":troop", ":flipped"),
            (assign, ":any", 1),
        (try_end),
        (eq, ":any", 0),
        (assign, ":pass", 10),
    (try_end),
]),

("kct_reapply_all_genders",
[
    (try_begin),
        (gt, "$cstm_troops_end", 0),
        (neq, "$cstm_troops_begin", "$cstm_troops_end"),
        (try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
            (troop_get_slot, ":flipped", ":troop", cstm_slot_troop_gender),
            (eq, ":flipped", 1),
            (call_script, "script_kct_flip_troop_gender", ":troop", 1),
        (try_end),
    (try_end),
]),
]
