# ======================================================================
# SHARED DEPENDENCY
# Entity: dplmc_copy_inventory (script)
# Called by menus in 2 domains: castle, diplomacy
# ======================================================================

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
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

dplmc_copy_inventory_scripts = [
##diplomacy start+
#Importing a script used in Custom Commander.  The inventory copying is used
#as a clever way to make "unmodifiable" views of others' equipment (both the
#PC and NPC have their inventory copied before viewing, and after the window
#closes the copies are written back over the originals).
("dplmc_copy_inventory",
    [
      (store_script_param_1, ":source"),
      (store_script_param_2, ":target"),

      (troop_clear_inventory, ":target"),
      (troop_get_inventory_capacity, ":inv_cap", ":source"),
      (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":item", ":source", ":i_slot"),
        (troop_set_inventory_slot, ":target", ":i_slot", ":item"),
        (troop_get_inventory_slot_modifier, ":imod", ":source", ":i_slot"),
        (troop_set_inventory_slot_modifier, ":target", ":i_slot", ":imod"),
        (troop_inventory_slot_get_item_amount, ":amount", ":source", ":i_slot"),
        (gt, ":amount", 0),
        (troop_inventory_slot_set_item_amount, ":target", ":i_slot", ":amount"),
      (try_end),
    ])
]
