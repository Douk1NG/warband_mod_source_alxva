# -*- coding: cp1254 -*-
# package initializer for center_management menus

from game_menus.center_management.mnu_center_manage import center_manage_menu
from game_menus.center_management.mnu_center_improve import center_improve_menu

center_management_menus = []
center_management_menus.extend(center_manage_menu)
center_management_menus.extend(center_improve_menu)

