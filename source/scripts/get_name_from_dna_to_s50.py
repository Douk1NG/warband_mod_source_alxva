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

get_name_from_dna_to_s50_scripts = [
("get_name_from_dna_to_s50",
    [(store_script_param, ":dna", 1),
     (store_sub, ":num_names", names_end, names_begin),
     (store_sub, ":num_surnames", surnames_end, surnames_begin),
     (assign, ":selected_name", ":dna"),
     (val_mod, ":selected_name", ":num_names"),
     (assign, ":selected_surname", ":dna"),
     (val_div, ":selected_surname", ":num_names"),
     (val_mod, ":selected_surname", ":num_surnames"),
     (val_add, ":selected_name", names_begin),
     (val_add, ":selected_surname", surnames_begin),
     (str_store_string, s50, ":selected_name"),
     (str_store_string, s50, ":selected_surname"),
     ])
]
