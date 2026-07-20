# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
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

equip_best_melee_weapon_scripts = [
("equip_best_melee_weapon", [
      (store_script_param, ":agent", 1),
      (store_script_param, ":force_shield", 2),
      (store_script_param, ":force_length", 3),
      (store_script_param, ":fire_order", 4),

      (agent_get_wielded_item, ":cur_wielded", ":agent", 0),
      (try_begin),
        (call_script, "script_cf_is_weapon_ranged", ":cur_wielded", 0),
        (agent_get_ammo, ":ammo", ":agent", 1),
        (gt, ":ammo", 0),

      (else_try),
        #priority items
        (assign, ":shield", itm_no_item),
        (assign, ":weapon", itm_no_item),
        (try_for_range, ":item_slot", ek_item_0, ek_head),
          (agent_get_item_slot, ":item", ":agent", ":item_slot"),
          (gt, ":item", itm_no_item),
          (item_get_type, ":weapon_type", ":item"),
          (try_begin),
            (eq, ":weapon_type", itp_type_shield),
            (assign, ":shield", ":item"),
          (else_try),
            (eq, ":weapon_type", itp_type_thrown),
            (eq, ":fire_order", aordr_fire_at_will),
            # (agent_get_ammo, ":ammo", ":agent", 0), #assume infantry would have no
            # other kind of ranged weapon
            # (gt, ":ammo", 0),
            (assign, ":weapon", ":item"),	#use thrown weapons first
          (try_end),
        (try_end),

        #select weapon
        (try_begin),
          (eq, ":weapon", itm_no_item),
          (assign, ":cur_score", 0),
          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (gt, ":item", itm_no_item),
            (item_get_type, ":weapon_type", ":item"),
            (neq, ":weapon_type", itp_type_shield),

            (try_begin),
              (item_has_property, ":item", itp_two_handed),
              (assign, reg0, 1),
            (else_try),
              (assign, reg0, 0),
            (try_end),

            (this_or_next | eq, reg0, 0),
            (this_or_next | eq, ":force_shield", 0),
            (eq, ":shield", itm_no_item),

            (try_begin),
              (call_script, "script_cf_is_weapon_ranged", ":item", 1),

            (else_try),
              (try_begin),
                (neq, ":force_length", 0),
                (item_get_weapon_length, ":item_length", ":item"),
                (try_begin),
                  (lt, ":cur_score", ":item_length"),
                  (assign, ":cur_score", ":item_length"),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (troop_is_guarantee_horse, ":troop_id"),
                (agent_get_horse, ":horse", ":agent"),
                (le, ":horse", 0),
                (try_for_range, ":item_slot", ek_item_0, ek_head),
                  (agent_get_item_slot, ":item", ":agent", ":item_slot"),
                  (gt, ":item", itm_no_item),
                  (item_get_type, ":weapon_type", ":item"),
                  (eq, ":weapon_type", itp_type_one_handed_wpn),
                  (item_get_swing_damage, ":swing", ":item"),
                  (gt, ":swing", 19),
                  (assign, ":weapon", ":item"),
                (try_end),
              (else_try),
                (agent_get_troop_id, ":troop_id", ":agent"),
                (assign, ":imod", imod_plain),
                (try_begin),    #only heroes have item modifications
                  (troop_is_hero, ":troop_id"),
                  (try_for_range, ":troop_item_slot",  ek_item_0, ek_head),    # heroes have only 4 possible weapons (equipped)
                    (troop_get_inventory_slot, reg0, ":troop_id", ":troop_item_slot"),  #Find Item Slot with same item ID as Equipped Weapon
                    (eq, reg0, ":item"),
                    (troop_get_inventory_slot_modifier, ":imod", ":troop_id", ":troop_item_slot"),
                  (try_end),
                (try_end),
                (call_script, "script_evaluate_item", ":item", ":imod"),
                (lt, ":cur_score", reg0),
                (assign, ":cur_score", reg0),
                (assign, ":weapon", ":item"),
              (try_end),
            (try_end),  #melee weapon
          (try_end),  #weapon slot loop
        (try_end),  #select weapon

        #equip selected items if needed
        (try_begin),
          (neq, ":cur_wielded", ":weapon"),
          (try_begin),
            (gt, ":shield", itm_no_item),
            (agent_get_wielded_item, reg0, ":agent", 1),
            (neq, reg0, ":shield"),	#reequipping secondary will UNequip (from experience)
            (agent_set_wielded_item, ":agent", ":shield"),
          (try_end),
          (gt, ":weapon", itm_no_item),
          (agent_set_wielded_item, ":agent", ":weapon"),
        (try_end),
      (try_end),])
]
