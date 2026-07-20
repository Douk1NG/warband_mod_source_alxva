# -*- coding: cp1254 -*-
# package initializer for scenes menus

from game_menus.scenes.mnu_four_ways_inn import four_ways_inn_menu
from game_menus.scenes.mnu_zendar import zendar_menu
from game_menus.scenes.mnu_salt_mine import salt_mine_menu
from game_menus.scenes.mnu_dhorak_keep import dhorak_keep_menu
from game_menus.scenes.mnu_battlefields import battlefields_menu

scenes_menus = []
scenes_menus.extend(four_ways_inn_menu)
scenes_menus.extend(zendar_menu)
scenes_menus.extend(salt_mine_menu)
scenes_menus.extend(dhorak_keep_menu)
scenes_menus.extend(battlefields_menu)

