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

display_policy_string_to_reg_scripts = [
("display_policy_string_to_reg", [
    (store_script_param, ":faction_no", 1),
    (store_script_param, reg2, 2), #whether it is third person "the" or first person "our"
    (store_script_param, reg3, 3), #spaces or line breaks as the postfix delimiter

    (str_store_faction_name_link, s5, ":faction_no"),
    (assign, ":string", "str_dplmc_neither_centralize_nor_decentralized"),
    (faction_get_slot, ":centralization", ":faction_no", dplmc_slot_faction_centralization),
    (val_add, ":string", ":centralization"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our government:The goverment of the {s5}} is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_neither_aristocratic_nor_plutocratic"),
    (faction_get_slot, ":aristocraty", ":faction_no", dplmc_slot_faction_aristocracy),
    (val_add, ":string", ":aristocraty"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}The upper class society is {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mixture_serfs"),
    (faction_get_slot, ":serfdom", ":faction_no", dplmc_slot_faction_serfdom),
    (val_add, ":string", ":serfdom"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} people are {s0}.{reg3?^: }"),

    (assign, ":string", "str_dplmc_mediocre_quality"),
    (faction_get_slot, ":quality", ":faction_no", dplmc_slot_faction_quality),
    (val_add, ":string", ":quality"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The} troops have {s0}.{reg3?^: }"),

    ##nested diplomacy start+ add mercantilism
    (assign, ":string", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
    (faction_get_slot, ":mercantilism", ":faction_no", dplmc_slot_faction_mercantilism),
    (val_add, ":string", ":mercantilism"),
    (str_store_string, s0, ":string"),
    (str_store_string, s20, "@{s20}{reg2?Our:The government's} approach to trade is {s0}.{reg3?^: }"),
  ])
]
