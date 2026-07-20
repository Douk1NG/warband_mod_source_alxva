# -*- coding: cp1254 -*-
# package initializer for custom_battle menus

from game_menus.custom_battle.mnu_custom_battle_end import custom_battle_end_menu
from game_menus.custom_battle.mnu_custom_battle_scene import custom_battle_scene_menu

custom_battle_menus = []
custom_battle_menus.extend(custom_battle_end_menu)
custom_battle_menus.extend(custom_battle_scene_menu)

