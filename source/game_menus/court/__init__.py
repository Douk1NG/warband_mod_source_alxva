# -*- coding: cp1254 -*-
# package initializer for court menus

from game_menus.court.mnu_choose_banner import choose_banner_menu
from game_menus.court.mnu_garden import garden_menu
from game_menus.court.mnu_lady_visit import lady_visit_menu
from game_menus.court.mnu_establish_court import establish_court_menu

court_menus = []
court_menus.extend(choose_banner_menu)
court_menus.extend(garden_menu)
court_menus.extend(lady_visit_menu)
court_menus.extend(establish_court_menu)

