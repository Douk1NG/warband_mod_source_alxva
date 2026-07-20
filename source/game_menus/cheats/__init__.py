# -*- coding: cp1254 -*-
# package initializer for cheats menus

from game_menus.cheats.mnu_party_cheat import party_cheat_menu
from game_menus.cheats.mnu_cheat_find_item import cheat_find_item_menu
from game_menus.cheats.mnu_camp_cheat import camp_cheat_menu
from game_menus.cheats.mnu_town_cheats_2 import town_cheats_2_menu
from game_menus.cheats.mnu_test_scene import test_scene_menu
from game_menus.cheats.mnu_camp_cheat_adv import camp_cheat_adv_menu
from game_menus.cheats.mnu_town_cheats import town_cheats_menu
from game_menus.cheats.mnu_cheat_change_weather import cheat_change_weather_menu
from game_menus.cheats.mnu_cheat_reports import cheat_reports_menu

cheats_menus = []
cheats_menus.extend(party_cheat_menu)
cheats_menus.extend(cheat_find_item_menu)
cheats_menus.extend(camp_cheat_menu)
cheats_menus.extend(town_cheats_2_menu)
cheats_menus.extend(test_scene_menu)
cheats_menus.extend(camp_cheat_adv_menu)
cheats_menus.extend(town_cheats_menu)
cheats_menus.extend(cheat_change_weather_menu)
cheats_menus.extend(cheat_reports_menu)

