# -*- coding: cp1254 -*-
# package initializer for join_battle menus

from game_menus.join_battle.mnu_order_attack_begin import order_attack_begin_menu
from game_menus.join_battle.mnu_order_attack_2 import order_attack_2_menu
from game_menus.join_battle.mnu_pre_join import pre_join_menu
from game_menus.join_battle.mnu_join_battle import join_battle_menu
from game_menus.join_battle.mnu_join_order_attack import join_order_attack_menu

join_battle_menus = []
join_battle_menus.extend(order_attack_begin_menu)
join_battle_menus.extend(order_attack_2_menu)
join_battle_menus.extend(pre_join_menu)
join_battle_menus.extend(join_battle_menu)
join_battle_menus.extend(join_order_attack_menu)

