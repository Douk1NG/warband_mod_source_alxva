# -*- coding: cp1254 -*-
# package initializer for locations menus

from game_menus.locations.mnu_zendar import zendar_menu
from game_menus.locations.mnu_salt_mine import salt_mine_menu
from game_menus.locations.mnu_four_ways_inn import four_ways_inn_menu
from game_menus.locations.mnu_test_scene import test_scene_menu
from game_menus.locations.mnu_battlefields import battlefields_menu
from game_menus.locations.mnu_dhorak_keep import dhorak_keep_menu
from game_menus.locations.mnu_join_siege_outside import join_siege_outside_menu

locations_menus = []
locations_menus.extend(zendar_menu)
locations_menus.extend(salt_mine_menu)
locations_menus.extend(four_ways_inn_menu)
locations_menus.extend(test_scene_menu)
locations_menus.extend(battlefields_menu)
locations_menus.extend(dhorak_keep_menu)
locations_menus.extend(join_siege_outside_menu)

