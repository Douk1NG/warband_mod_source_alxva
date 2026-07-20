# -*- coding: cp1254 -*-
"""Shared Python helper functions used by extracted scripts."""
from header_common import *
from header_operations import *
from module_constants import *
from ID_strings import str_key_0

def keys_array():
    keys_list = []
    for key_no in xrange(len(keys)):
        keys_list.append((troop_set_slot, "trp_temp_array_a", key_no, keys[key_no]))
        keys_list.append((troop_set_slot, "trp_temp_array_b", key_no, str_key_0 + key_no))
    return keys_list[:]

def make_noswing_weapons(items):
    noswing_weapons = []
    for i_item in xrange(len(items)):
        noswing_name = 'noswing_' + items[i_item][0]
        i_noswing = find_object(items, noswing_name)
        if i_noswing > -1:
            noswing_weapons.append((item_set_slot, i_item, slot_item_alternate, i_noswing))
            noswing_weapons.append((item_set_slot, i_noswing, slot_item_alternate, i_item))
    return noswing_weapons[:]
