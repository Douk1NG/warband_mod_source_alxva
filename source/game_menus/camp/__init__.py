# -*- coding: cp1254 -*-
# package initializer for camp menus

from game_menus.camp.mnu_camp import camp_menu
from game_menus.camp.mnu_camp_cheat import camp_cheat_menu
from game_menus.camp.mnu_camp_cheat_adv import camp_cheat_adv_menu
from game_menus.camp.mnu_cheat_find_item import cheat_find_item_menu
from game_menus.camp.mnu_cheat_change_weather import cheat_change_weather_menu
from game_menus.camp.mnu_camp_action import camp_action_menu
from game_menus.camp.mnu_camp_recruit_prisoners import camp_recruit_prisoners_menu
from game_menus.camp.mnu_camp_no_prisoners import camp_no_prisoners_menu
from game_menus.camp.mnu_camp_action_sort_inventory import camp_action_sort_inventory_menu
from game_menus.camp.mnu_camp_action_read_book import camp_action_read_book_menu
from game_menus.camp.mnu_camp_action_read_book_start import camp_action_read_book_start_menu
from game_menus.camp.mnu_retirement_verify import retirement_verify_menu
from game_menus.camp.mnu_end_game import end_game_menu

camp_menus = []
camp_menus.extend(camp_menu)
camp_menus.extend(camp_cheat_menu)
camp_menus.extend(camp_cheat_adv_menu)
camp_menus.extend(cheat_find_item_menu)
camp_menus.extend(cheat_change_weather_menu)
camp_menus.extend(camp_action_menu)
camp_menus.extend(camp_recruit_prisoners_menu)
camp_menus.extend(camp_no_prisoners_menu)
camp_menus.extend(camp_action_sort_inventory_menu)
camp_menus.extend(camp_action_read_book_menu)
camp_menus.extend(camp_action_read_book_start_menu)
camp_menus.extend(retirement_verify_menu)
camp_menus.extend(end_game_menu)

