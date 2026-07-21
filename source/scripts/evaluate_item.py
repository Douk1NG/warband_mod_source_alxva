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

evaluate_item_scripts = [
("evaluate_item", [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":item_mod", 2),

      (assign, ":ret_val", 0),
      (try_begin),
        (gt, ":item_id", "itm_no_item"),

        (item_get_type, ":item_type", ":item_id"),
        (call_script, "script_get_item_modifier_effects", ":item_type", ":item_mod"),
        (assign, ":damage", reg0),
        (assign, ":speed", reg1),
        (assign, ":armor", reg2),
        (assign, ":hit_points", reg3),

        #Armor
        (try_begin),
          (ge, ":item_type", itp_type_head_armor),
          (le, ":item_type", itp_type_hand_armor),

          #construct comparison value
          (item_get_head_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (item_get_leg_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),

          #Ranged Weapons
        (else_try),
          (call_script, "script_cf_is_weapon_ranged", ":item_id", 1),

          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (val_add, ":damage", ":value"),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),

          (item_get_missile_speed,  ":value", ":item_id"),
          (val_mul, ":damage", ":value"),

          (item_get_accuracy, ":value", ":item_id"),
          (val_mul, ":damage", ":value"),
          (assign, ":ret_val", ":damage"),

          #Melee Weapons
        (else_try),
          (ge, ":item_type", itp_type_one_handed_wpn),
          (le, ":item_type", itp_type_polearm),

          #construct comparison value
          (item_get_thrust_damage, ":value", ":item_id"),
          (item_get_swing_damage, reg2, ":item_id"),
          (val_max, ":value", reg2),  #TW formula.  Also avoids problems with script_switch_to_noswing_weapons
          (val_add, ":damage", ":value"),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":damage", ":value"),

          (item_get_weapon_length, ":value", ":item_id"),
          (convert_to_fixed_point, ":value"),
          (store_sqrt, reg2, ":value"),
          (convert_from_fixed_point, reg2),
          (val_mul, ":damage", reg2),
          (assign, ":ret_val", ":damage"),

          #Shields
        (else_try),
          (eq, ":item_type", itp_type_shield),

          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),

          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_div, ":value", 17),  #attempt to make it comparable to armors
          (val_add, ":armor", ":value"),

          #shields' protection modified by size, speed
          (item_get_weapon_length, ":value", ":item_id"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Thorax_Length),

          (item_get_speed_rating, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (val_div, ":armor", Outfit_Fast_Weapon_Speed),

          (val_mul, ":armor", 3), #fudge factor
          (assign, ":ret_val", ":armor"),

          #Horses
        (else_try),
          (eq, ":item_type", itp_type_horse),

          #construct comparison value
          (item_get_body_armor, ":value", ":item_id"),
          (val_add, ":armor", ":value"),
          (val_mul, ":armor", 4), #figure it takes 3-4 hits to kill a horse, so this is the hit value of each
          #point of armor

          (item_get_hit_points, ":value", ":item_id"),
          (val_add, ":value", ":hit_points"),
          (val_add, ":armor", ":value"),

          (item_get_horse_speed, ":value", ":item_id"),
          (val_add, ":value", ":speed"),
          (val_mul, ":armor", ":value"),
          (assign, ":ret_val", ":armor"),

          #Missiles
        (else_try),
          (this_or_next | eq, ":item_type", itp_type_arrows),
          (this_or_next | eq, ":item_type", itp_type_bolts),
          (eq, ":item_type", itp_type_bullets),
        (try_end),
      (try_end),

      (assign, reg0, ":ret_val"),])
]
